#!/usr/bin/env bash
# Take a sealed attestation over the sixteen main-phase workspace records.
#
# Written 2026-09-02 because the 17:32Z seal was taken by hand and had to be retaken twice -- once
# self-inflicted (it ran before the JOBS.md accounting was written) and once external (the retired
# Mac's poll rewrote INBOX.md in fifteen workspaces at 18:58-19:07Z). A seal that does not cover
# the final write is not a seal, so this script:
#
#   1. REFUSES to seal unless the fleet is quiescent -- both queues zero, no daemons, no writers.
#   2. Records the max mtime of the sealed files per workspace, BEFORE hashing.
#   3. Re-reads those mtimes AFTER hashing and REFUSES if any moved during the seal.
#
# Step 3 is the one the hand-taken seals lacked. It cannot prevent a write after the seal completes;
# it makes a write DURING the seal impossible to miss.
set -euo pipefail
cd "$(dirname "$0")/.."
REMOTE="dirac-bei"; WSROOT="/home1/users/Bei/ws"
FILES="LOG.md STATE.md REPORT.md JOBS.md ESCALATIONS.md INBOX.md WORKSPACE.json usage.json"
OUT="${1:-harness/state/sealed_attestation_$(date -u +%Y%m%dT%H%M%SZ).json}"
PRIOR="harness/state/sealed_attestation_20260902.json"
IDS=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(' '.join(C.RATIFIED['phases']['main']['ids']))")

echo "=== 1. quiescence gate — a seal over a moving fleet is not a seal ==="
Q=$(ssh -o BatchMode=yes -o ConnectTimeout=60 "$REMOTE" '
  echo "PBS=$(qselect -u Bei 2>/dev/null | wc -l)"
  echo "MJS=$(/usr/local/mjs/qinfo 2>/dev/null | grep -cw Bei)"
  n=0; for p in $(ps -u Bei --no-headers -o pid 2>/dev/null); do
    [ -d /proc/$p ] || continue
    c=$(tr "\0" " " < /proc/$p/cmdline 2>/dev/null)
    case "$c" in *until*|*guard*|*cycle*|*watch*|*snap*|*monitor*|*qpos*|*supervisor*|*keepalive*|*autopilot*|*poll*|*meter*) n=$((n+1));; esac
  done; echo "WRITERS=$n"')
echo "$Q" | sed 's/^/  /'
eval "$Q"
[ "$PBS" -eq 0 ] && [ "$MJS" -eq 0 ] || { echo "REFUSED — queues not empty (PBS=$PBS mjs=$MJS)." >&2; exit 3; }
# WRITERS counts this ssh's own shell, whose cmdline contains the word "poll" from this script.
[ "$WRITERS" -le 1 ] || { echo "REFUSED — $WRITERS candidate writer processes alive." >&2; exit 3; }

echo "=== 2. mtimes before ==="
BEFORE=$(ssh -o BatchMode=yes -o ConnectTimeout=60 "$REMOTE" "for r in $IDS; do cd $WSROOT/\$r && echo \"\$r \$(stat -c%Y $FILES | sort -n | tail -1)\"; done")

echo "=== 3. hashing ==="
RAW=$(ssh -o BatchMode=yes -o ConnectTimeout=120 "$REMOTE" "for r in $IDS; do cd $WSROOT/\$r || continue; echo \"\$r|\$(sha256sum $FILES 2>/dev/null | sha256sum | cut -d' ' -f1)|\$(git rev-parse HEAD)|\$(git rev-list --count HEAD)|\$(git status --porcelain | wc -l)\"; done")

echo "=== 4. mtimes after — refuse if anything moved during the seal ==="
AFTER=$(ssh -o BatchMode=yes -o ConnectTimeout=60 "$REMOTE" "for r in $IDS; do cd $WSROOT/\$r && echo \"\$r \$(stat -c%Y $FILES | sort -n | tail -1)\"; done")
if [ "$BEFORE" != "$AFTER" ]; then
  echo "REFUSED — a sealed file changed WHILE the seal was being taken:" >&2
  diff <(echo "$BEFORE") <(echo "$AFTER") >&2 || true
  exit 4
fi
echo "  stable — no sealed file moved during the seal"

python3 - "$OUT" "$PRIOR" "$RAW" "$BEFORE" <<'PY'
import json, sys, datetime
out, prior, raw, mt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
old = json.load(open(prior))
per, mts = {}, dict(l.split() for l in mt.strip().splitlines())
for line in raw.strip().splitlines():
    r, h, head, c, d = line.split("|")
    per[r] = {"record_sha256": h, "head": head, "commits": int(c), "dirty_paths": int(d),
              "final_cpu_h": old["per_replicate"][r]["final_cpu_h"],
              "newest_sealed_mtime": int(mts[r])}
doc = {
 "record": "SEALED COLLECTION ATTESTATION (RESEAL) — all sixteen workspaces",
 "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "status": "SEALED",
 "supersedes": prior,
 "why_retaken": ("The 17:32Z seal was overtaken by an external write: the retired macOS host's "
   "study.poll fired one more full cycle at 18:58:22Z-19:07:05Z and appended harness usage notices "
   "to INBOX.md in fifteen of sixteen workspaces, stopping after rep16 and never reaching rep17 -- "
   "which is why rep17 was the only workspace that still reproduced it. The content was benign and "
   "no replicate ran; the seal was not wrong about 17:32Z, it was overtaken. Authorised by PI "
   "ruling 2026-09-02 04:35 KST. BOTH SEALS REMAIN IN THE RECORD."),
 "authority": "PI ruling 2026-09-02 04:35 KST (option 1 ratified)",
 "manifest": "sha256 over the concatenated sha256sum of LOG.md STATE.md REPORT.md JOBS.md ESCALATIONS.md INBOX.md WORKSPACE.json usage.json, per workspace",
 "taken_under": ("quiescence gate passed (PBS 0, mjs 0, no writer processes) and mtime-stability "
   "verified before and after hashing -- the check the two hand-taken seals lacked"),
 "n": len(per), "all_reachable": len(per) == 16,
 "fleet_final_cpu_h": old["fleet_final_cpu_h"],
 "known_gap": old["known_gap"],
 "per_replicate": per,
}
json.dump(doc, open(out, "w"), indent=2)
print(f"  sealed {len(per)}/16 -> {out}")
PY
