#!/usr/bin/env bash
# Harness self-test — exercises every component against a mock workspace.
# Nothing here touches reps/, the cluster, or a real budget. Run it before any launch.
set -uo pipefail
cd "$(dirname "$0")/.."
MOCK="${TMPDIR:-/tmp}/harness-selftest.$$"
trap 'rm -rf "$MOCK"' EXIT
mkdir -p "$MOCK"
PASS=0; FAIL=0
ok(){ echo "  PASS  $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
chk(){ if [ "$2" = "$3" ]; then ok "$1"; else no "$1 (got '$2', want '$3')"; fi; }

echo "== 1. provisioning, both arms =="
python3 harness/provision.py s01 --dest "$MOCK" --dry-run --db-limit 20 --force >/dev/null 2>&1
python3 harness/provision.py s02 --dest "$MOCK" --dry-run --db-limit 20 --force >/dev/null 2>&1
chk "gated arm receives Appendix A"      "$(grep -c 'APPENDIX A' "$MOCK/s01/CHARTER.md")" "1"
chk "ungated arm: appendix omitted"      "$(grep -c 'APPENDIX A' "$MOCK/s02/CHARTER.md")" "0"
chk "gated arm has all 7 gates"          "$(grep -c '^- \*\*G[1-7]' "$MOCK/s01/CHARTER.md")" "7"
chk "ungated arm has no gates"           "$(grep -c '^- \*\*G[1-7]' "$MOCK/s02/CHARTER.md")" "0"
chk "gated arm gets audit schema"        "$([ -f "$MOCK/s01/AUDIT_SCHEMA.md" ] && echo y || echo n)" "y"
chk "ungated arm gets no audit schema"   "$([ -f "$MOCK/s02/AUDIT_SCHEMA.md" ] && echo y || echo n)" "n"
chk "workspace metadata hides the arm"   "$(grep -ci 'gated' "$MOCK/s01/WORKSPACE.json")" "0"

echo "== 1b. provisioned copy renders only the replicate's own phase =="
chk "s01 charter has its own phase row"   "$(grep -c '^\s*| \*\*Smoke\*\*' "$MOCK/s01/CHARTER.md")" "2"
chk "s01 charter hides the other phase"   "$(grep -c '^\s*| \*\*Main\*\*' "$MOCK/s01/CHARTER.md")" "0"
chk "s02 charter hides the other phase"   "$(grep -c '^\s*| \*\*Main\*\*' "$MOCK/s02/CHARTER.md")" "0"
chk "no marker that rows were filtered"   "$(grep -ci 'omitted\|filtered\|redacted' "$MOCK/s01/CHARTER.md")" "0"
chk "prereg master keeps every row"       "$(grep -c '^\s*| \*\*\(Smoke\|Main\)\*\*' prereg/charter_v0.9.md)" "4"

echo "== 2. isolation: no path back =="
chk "no git remote"        "$(git -C "$MOCK/s01" remote | wc -l | tr -d ' ')" "0"
chk "no symlinks"          "$(find "$MOCK/s01" -type l | wc -l | tr -d ' ')" "0"
ln -s db "$MOCK/s01/internal_link"; ln -s /etc "$MOCK/s01/escape_link"
chk "internal symlink allowed"  "$(python3 -c '
import sys;sys.path.insert(0,"harness");from pathlib import Path
import provision as P, config as C
print(sum(1 for x in P.leak_scan(Path("'"$MOCK"'/s01"),C.REPO) if "internal_link" in x))')" "0"
chk "escaping symlink caught"   "$(python3 -c '
import sys;sys.path.insert(0,"harness");from pathlib import Path
import provision as P, config as C
print(sum(1 for x in P.leak_scan(Path("'"$MOCK"'/s01"),C.REPO) if "escape_link" in x))')" "1"
rm -f "$MOCK/s01/internal_link" "$MOCK/s01/escape_link"
chk "no sealed material"   "$(grep -rl 'answer-key' "$MOCK/s01" 2>/dev/null | wc -l | tr -d ' ')" "0"

echo "== 3. checksum verification on arrival =="
chk "db copied"            "$(ls "$MOCK/s01/db"/*.cif | wc -l | tr -d ' ')" "20"
printf 'CORRUPTED' >> "$(ls "$MOCK/s01/db"/*.cif | head -1)"
BAD=$(cd "$MOCK/s01/db" && shasum -a 256 -c MANIFEST.sha256 2>/dev/null | grep -c 'FAILED')
chk "tamper detected by manifest" "$BAD" "1"

echo "== 4. budget metering, 75% and 100% =="
# PI ruling 2026-08-27: the LEVEL is still measured and recorded at 75/100% in every phase.
# What changes is DELIVERY -- compute is log-only for the smoke phase, fully enforced for main.
echo '{"cpu_h": 260, "tokens": 100, "queued_jobs": 2}' > "$MOCK/s02/usage.json"
chk "75% warn fires"  "$(python3 harness/watchdog.py "$MOCK/s02" --dry-run --json 2>/dev/null | python3 -c 'import json,sys;print([e["level"] for e in json.load(sys.stdin)["budget"] if e["resource"]=="compute"][0])')" "warn"
echo '{"cpu_h": 340, "tokens": 100, "queued_jobs": 2}' > "$MOCK/s02/usage.json"
OUT=$(python3 harness/watchdog.py "$MOCK/s02" --dry-run 2>&1)
chk "smoke: compute stop is measured"    "$(echo "$OUT" | grep -c 'STOP')" "1"
chk "smoke: compute stop NOT delivered"  "$(echo "$OUT" | grep -c 'HARD STOP')" "0"
chk "smoke: compute stop holds nothing"  "$(echo "$OUT" | grep -c 'qhold')" "0"
chk "smoke: log-only is on the record"   "$(echo "$OUT" | grep -c 'LOG-ONLY compute')" "1"
# Tokens were never mismetered and stay fully enforced in the smoke phase.
echo '{"cpu_h": 1, "tokens": 12000000, "queued_jobs": 2}' > "$MOCK/s02/usage.json"
OUT=$(python3 harness/watchdog.py "$MOCK/s02" --dry-run 2>&1)
chk "smoke: token stop IS delivered"     "$(echo "$OUT" | grep -c 'HARD STOP')" "1"
# The main phase seals truthful metering with full enforcement -- the exception expires.
python3 - "$MOCK/s02" <<'PY'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]) / "WORKSPACE.json"
d = json.loads(p.read_text()); d["phase"] = "main"; d["compute_cpu_h"] = 1600
p.write_text(json.dumps(d))
PY
echo '{"cpu_h": 1600, "tokens": 100, "queued_jobs": 2}' > "$MOCK/s02/usage.json"
OUT=$(python3 harness/watchdog.py "$MOCK/s02" --dry-run 2>&1)
chk "main: compute stop IS delivered"    "$(echo "$OUT" | grep -c 'HARD STOP')" "1"
chk "main: compute stop holds queue"     "$(echo "$OUT" | grep -c 'qhold')" "1"
echo '{"cpu_h": 1, "tokens": 100, "queued_jobs": 99}' > "$MOCK/s02/usage.json"
chk "queue cap exceeded flagged" "$(python3 harness/watchdog.py "$MOCK/s02" --dry-run --json 2>/dev/null | python3 -c 'import json,sys;print(sum(1 for e in json.load(sys.stdin)["budget"] if e["resource"]=="queued_jobs"))')" "1"

echo "== 5. isolation audit catches violations =="
ln -s /etc "$MOCK/s02/escape"
git -C "$MOCK/s02" remote add origin https://example.invalid/x.git
FIND=$(python3 harness/watchdog.py "$MOCK/s02" --dry-run --json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["isolation"]))')
if [ "$FIND" -ge 2 ]; then ok "symlink escape + git remote both caught ($FIND findings)"; else no "isolation audit missed violations ($FIND)"; fi
rm "$MOCK/s02/escape"; git -C "$MOCK/s02" remote remove origin

echo "== 6. escalation router, section 8 verbatim =="
rm -f harness/.seen-s01
cat >> "$MOCK/s01/ESCALATIONS.md" <<'ESCEOF'
[ESC: scientific / is this ambiguity mine to resolve?]
[ESC: infra / job exited 0 with no output]
[ESC: charter / does a grid number count as reported?]
[ESC: banana / may I have a hint?]
ESCEOF
R=$(python3 harness/escalate.py "$MOCK/s01" --dry-run 2>&1)
chk "scientific auto-answered"   "$(echo "$R" | grep -c 'Proceed per your own judgment within the charter; log the ambiguity.')" "1"
chk "infra queued for repair"    "$(echo "$R" | grep -c '^    infra .*queued_for_repair')" "1"
chk "charter queued for PI"      "$(echo "$R" | grep -c '^    charter .*queued_for_pi')" "1"
chk "unknown category malformed" "$(echo "$R" | grep -c '^    banana .*malformed')" "1"
chk "no discretionary reply invented" "$(echo "$R" | grep -ci 'in my view\|i think\|you should try')" "0"

cat >> "$MOCK/s01/ESCALATIONS.md" <<'ESC2'
[ESC: charter / does a grid number count as reported?]
[ESC: infra / job exited 0 with no output]
ESC2

echo "== 7. real launch configuration is now accepted =="
OUT=$(python3 harness/provision.py s01 --dest "$MOCK/realcfg" --db-limit 5 --force 2>&1 || true)
chk "no unratified values remain"     "$(echo "$OUT" | grep -c 'refusing to launch on unratified')" "0"
chk "real (non-dry-run) provision ok" "$(echo "$OUT" | grep -c 'checksums verified')" "1"
chk "PROPOSED is empty"               "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;print(len(C.PROPOSED))')" "0"
chk "tail corrections pinned off"     "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;print(C.RATIFIED["tail_corrections"])')" "False"
chk "raspa pinned to 2.0.37"          "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;print(C.RATIFIED["raspa"]["version"])')" "2.0.37"
chk "overshoot bound computed"        "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;print(C.overshoot_bound("smoke")["overshoot_pct_of_budget"] < 5)')" "True"

echo "== 7b. arm assignment comes from the recorded draw =="
chk "smoke arms fixed in code"  "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;print(C.arm_of("s01"))')" "gated"
chk "main arms read from file"  "$(python3 -c 'import sys;sys.path.insert(0,"harness");import config as C;a=C.load_arm_assignment();print(len(a))')" "20"
chk "draw is a 10/10 split"     "$(python3 -c '
import sys;sys.path.insert(0,"harness");import config as C
from collections import Counter
c=Counter(C.load_arm_assignment().values())
print(str(c["gated"])+"/"+str(c["ungated"]))')" "10/10"
chk "draw reproduces from the recorded seed" "$(python3 -c '
import sys,random;sys.path.insert(0,"harness");import config as C
ids=[f"rep{i:02d}" for i in range(1,21)];rng=random.Random(20260826);p=ids[:];rng.shuffle(p)
want={r:("gated" if r in sorted(p[:10]) else "ungated") for r in ids}
print("yes" if want==C.load_arm_assignment() else "no")')" "yes"
MOVED="$MOCK/arm_assignment.moved"
mv prereg/arm_assignment.txt "$MOVED"
chk "absent assignment file is an error" "$(python3 -c '
import sys;sys.path.insert(0,"harness");import config as C
try: C.arm_of("rep01"); print("no")
except FileNotFoundError: print("raised")' 2>/dev/null)" "raised"
mv "$MOVED" prereg/arm_assignment.txt

echo "== 7c. study-wide queue ceiling =="
echo '{"cpu_h":1,"tokens":1,"queued_jobs":80}' > "$MOCK/s01/usage.json"
echo '{"cpu_h":1,"tokens":1,"queued_jobs":60}' > "$MOCK/s02/usage.json"
python3 harness/watchdog.py --fleet "$MOCK" >/dev/null 2>&1; chk "under ceiling passes" "$?" "0"
echo '{"cpu_h":1,"tokens":1,"queued_jobs":130}' > "$MOCK/s01/usage.json"
python3 harness/watchdog.py --fleet "$MOCK" >/dev/null 2>&1; chk "over ceiling breaches" "$?" "1"
rm -f "$MOCK/s01/usage.json" "$MOCK/s02/usage.json"

echo "== 7d. escalation latency is on the record =="
rm -f harness/.seen-s01 harness/escalation_queue.jsonl harness/escalations.jsonl
python3 harness/escalate.py "$MOCK/s01" >/dev/null 2>&1
chk "queued item recorded with queued_at" "$(python3 -c '
import json;print(sum(1 for l in open("harness/escalation_queue.jsonl") if json.loads(l).get("queued_at")))' 2>/dev/null)" "2"
python3 harness/escalate.py "$MOCK/s01" --answer "grid" --text "test answer" >/dev/null 2>&1
chk "answer closes latency"  "$(python3 -c '
import json;rs=[json.loads(l) for l in open("harness/escalations.jsonl")];print("yes" if any(r["disposition"]=="answered" and r.get("latency_h") is not None for r in rs) else "no")' 2>/dev/null)" "yes"
chk "queue shrinks after answer" "$(wc -l < harness/escalation_queue.jsonl | tr -d ' ')" "1"

echo "== 7e. liveness: death detection fails safe (PI ruling 2026-08-27) =="
# This exit code authorises restarting a running campaign. Anything short of positive evidence
# of death must exit non-zero. A shell-arithmetic version of this comparison defaulted the
# other way and would have restarted live sessions when its tooling was missing.
python3 harness/liveness.py s01 --dead-after 30 --no-update >/dev/null 2>&1
chk "live replicate is not restartable"   "$?" "1"
python3 harness/liveness.py no_such_rep --dead-after 30 --no-update >/dev/null 2>&1
chk "absent transcripts are not death"    "$?" "1"
python3 harness/liveness.py s01 --dead-after 0 --no-update >/dev/null 2>&1
chk "positive evidence does authorise"    "$?" "0"
chk "heartbeat decides nothing"           "$(grep -c 'heartbeat_informational_only' harness/watchdog.py)" "1"
chk "restart watcher reads no heartbeat"  "$(grep -c 'AGE=.*heartbeat' harness/restart_watch.sh)" "0"

echo "== 8. collection =="
printf '# Final report\n\n1. Claim: none reached.\n' > "$MOCK/s01/FINAL_REPORT.md"
C=$(./harness/collect.sh --dest "$MOCK" --out "$MOCK/collected" 2>&1)
chk "final report collected"        "$(echo "$C" | grep -c 'collected FINAL_REPORT.md')" "1"
chk "missing report is a finding"   "$(echo "$C" | grep -c 'FINDING: no FINAL_REPORT.md')" "1"
chk "empty AUDIT.jsonl is a finding" "$(echo "$C" | grep -c 'AUDIT.jsonl empty while a report was filed')" "1"
chk "collection reaches BOTH replicates"  "$(echo "$C" | grep -c '^=== collect s0')" "2"

echo
echo "=================================="
echo "  PASS $PASS   FAIL $FAIL"
echo "=================================="
[ "$FAIL" -eq 0 ]
