#!/usr/bin/env bash
# (d-pre) PULL — bring the sixteen main-phase records off the cluster into reps/main/collected/.
#
# WHY THIS EXISTS. transfer.sh only ever PUSHES (`rsync -a "$LOCAL/" "dirac-bei:$WS/"`), and
# collect.sh reads from a LOCAL workspace that the main phase never had: the sixteen have lived on
# bnode0 for their whole campaign. The smoke was pulled by hand on the macOS host that is now
# retired, so the inbound half of collection has never existed in this harness. That gap is what
# refused Stage 0/1 twice at screen_launch.sh's §7.1 barrier. This is the missing half, and nothing
# more: it copies out, it never edits in.
#
# AUTHORISED by PI ruling 2026-09-02 04:20 KST as mechanical execution: rsync per the smoke's
# completed shape, COLLECTION.md per that template, every pulled record file verified byte-identical
# against harness/state/sealed_attestation_20260902.json. THE SEAL IS THE AUTHORITY. Any mismatch
# halts and reports; it does not warn and continue.
#
# READ-ONLY WITH RESPECT TO THE WORKSPACES. Every remote command here is rsync-out, sha256sum or
# git-log. Nothing writes to /home1/users/Bei/ws/.
#
#   ./harness/pull_collect.sh --dry-run   # exercise the whole path, write nothing
#   ./harness/pull_collect.sh             # pull, verify against the seal, write COLLECTION.md
set -euo pipefail
cd "$(dirname "$0")/.."

REMOTE="dirac-bei"; WSROOT="/home1/users/Bei/ws"
OUT="reps/main/collected"
SEAL="harness/state/sealed_attestation_20260902.json"
# The eight files the seal's manifest covers, IN THE SEAL'S ORDER. The recomputation below is only
# valid if this list and its order match the manifest exactly -- see §4 of the 02:35 REPORTS entry.
SEALED_FILES="LOG.md STATE.md REPORT.md JOBS.md ESCALATIONS.md INBOX.md WORKSPACE.json usage.json"
# Collected alongside them for the smoke's shape; NOT part of the seal, so never hashed into it.
EXTRA_FILES="AUDIT.jsonl"

DRY=""; [ "${1:-}" = "--dry-run" ] && DRY=1
[ -f "$SEAL" ] || { echo "REFUSED — no seal at $SEAL; there is nothing to verify against." >&2; exit 2; }
IDS=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(' '.join(C.RATIFIED['phases']['main']['ids']))")
N=$(echo $IDS | wc -w)
echo "pull: $N replicates from $REMOTE:$WSROOT -> $OUT${DRY:+  (DRY RUN — nothing written)}"

DEST="$OUT"; [ -n "$DRY" ] && DEST="$(mktemp -d)"
mkdir -p "$DEST"

# --- 1. pull ------------------------------------------------------------------------------------
for R in $IDS; do
  D="$DEST/$R"; mkdir -p "$D"
  # --ignore-missing-args so an absent optional file is not a transfer failure; presence is
  # asserted by the seal check below, never by rsync's exit code.
  rsync -a --ignore-missing-args \
    $(for f in $SEALED_FILES $EXTRA_FILES; do printf '%s ' "$REMOTE:$WSROOT/$R/$f"; done) "$D/" 2>/dev/null || true
  # charter §6: history must not be rewritten. Captured remotely -- the .git trees are not pulled.
  ssh -o BatchMode=yes -o ConnectTimeout=60 "$REMOTE" \
    "cd $WSROOT/$R && git log --format='%H %ad %s' --date=iso" > "$D/git-log.txt" 2>/dev/null || true
  # The smoke normalises the §7 report to FINAL_REPORT.md and records the name as filed. Both are
  # kept: REPORT.md is the name the SEAL hashes and the name §7.1's gate reads, so it is binding
  # and is not renamed; FINAL_REPORT.md is the smoke's shape, written as a copy, not a move.
  if [ -s "$D/REPORT.md" ]; then
    cp "$D/REPORT.md" "$D/FINAL_REPORT.md"; printf 'REPORT.md\n' > "$D/REPORT_FILENAME_AS_FILED"
  fi
  printf '  %-6s %s\n' "$R" "$(cd "$D" && ls $SEALED_FILES 2>/dev/null | wc -l)/8 sealed files, $(wc -l < "$D/git-log.txt" | tr -d ' ') commits"
done

# --- 2. independent remote fingerprint, taken AFTER the copy --------------------------------------
# This is what makes the pull a snapshot rather than an assertion, exactly as the smoke's step 2 was.
ATT="$DEST/BELL_FINGERPRINT.log"
{
  echo "PULL FINGERPRINT $(date -u +%FT%TZ) / $(TZ=Asia/Seoul date '+%F %H:%M:%S KST')"
  for R in $IDS; do
    ssh -o BatchMode=yes -o ConnectTimeout=60 "$REMOTE" \
      "cd $WSROOT/$R 2>/dev/null && sha256sum $SEALED_FILES 2>/dev/null" | sed "s|^|$R |" || echo "$R UNREACHABLE"
  done
} > "$ATT"
echo "  fingerprint: $(awk 'NF==3 && length($2)==64' "$ATT" | wc -l | tr -d ' ') hashes"

# --- 3. VERIFY AGAINST THE SEAL — the authority. Mismatch halts. ----------------------------------
echo
echo "=== verifying pulled records against $SEAL ==="
python3 - "$DEST" "$SEAL" "$SEALED_FILES" <<'PY'
import hashlib, json, subprocess, sys, os
dest, sealp, files = sys.argv[1], sys.argv[2], sys.argv[3].split()
seal = json.load(open(sealp))["per_replicate"]
bad, ok = [], 0
for r in sorted(seal):
    d = os.path.join(dest, r)
    missing = [f for f in files if not os.path.isfile(os.path.join(d, f))]
    if missing:
        bad.append((r, "missing: " + " ".join(missing))); continue
    # Reproduce the seal exactly: `sha256sum <files in seal order>` output TEXT, hashed.
    out = subprocess.run(["sha256sum", *files], cwd=d, capture_output=True, text=True).stdout
    got = hashlib.sha256(out.encode()).hexdigest()
    exp = seal[r]["record_sha256"]
    if got != exp:
        per = {f: hashlib.sha256(open(os.path.join(d, f), 'rb').read()).hexdigest() for f in files}
        rem = {}
        for line in open(os.path.join(dest, "BELL_FINGERPRINT.log")):
            p = line.split()
            if len(p) == 3 and p[0] == r: rem[p[2]] = p[1]
        diff = [f for f in files if rem.get(f) and rem[f] != per[f]]
        bad.append((r, f"record_sha256 {got[:16]} != sealed {exp[:16]}" +
                    (f"; differs from remote: {' '.join(diff)}" if diff else "; local copy matches remote — the SEAL disagrees")))
    else:
        ok += 1
        print(f"  {r}  OK  {exp[:16]}...")
for r, why in bad:
    print(f"  {r}  MISMATCH  {why}")
print(f"\n  verified {ok}/{len(seal)}")
if bad:
    print("\nHALT — the collection does not reproduce the seal. Nothing downstream may proceed:")
    print("the seal is the authority, and a collection that disagrees with it is a failed")
    print("collection, not a collected one. No COLLECTION.md written.")
    sys.exit(9)
PY

# --- 4. COLLECTION.md, per the smoke's template ---------------------------------------------------
[ -n "$DRY" ] && { echo; echo "DRY RUN complete — verification ran, nothing written to $OUT"; rm -rf "$DEST"; exit 0; }
echo
echo "=== writing COLLECTION.md ==="
"$(dirname "$0")/write_collection_md.sh" "$OUT" "$IDS"
echo "  $OUT/COLLECTION.md"
echo
echo "collection complete — §7.1 may now be re-checked with ./harness/screen_launch.sh --check"
