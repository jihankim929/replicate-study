#!/usr/bin/env bash
# (d) Launch — provision and start the smoke replicates s01 (gated) and s02 (ungated).
#
# Charter clauses enforced here:
#   section 4  workspace isolation: each replicate gets its own tree, no shared state
#   section 5  campaign length comes from the charter's per-phase table, via config.py
#   Appendix A arm assignment: which replicate receives the appendix (provision.py decides)
#
# Usage:
#   ./harness/launch.sh --dry-run                 # local mock, 25 structures, nothing real
#   ./harness/launch.sh --dest reps/smoke         # real provisioning (refuses on unratified budgets)
set -euo pipefail
cd "$(dirname "$0")/.."

DEST="reps/smoke"; DRY=""; DBLIMIT=""; FORCE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY="--dry-run"; DBLIMIT="--db-limit 25";;
    --dest)    DEST="$2"; shift;;
    --force)   FORCE="--force";;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
  shift
done

echo "=== launch: smoke phase, replicates s01 (gated) + s02 (ungated) ==="
[ -n "$DRY" ] && echo "=== DRY RUN — mock workspaces, 25-structure database, no cluster ==="

for REP in s01 s02; do
  echo
  python3 harness/provision.py "$REP" --dest "$DEST" $DRY $DBLIMIT $FORCE
done

echo
echo "=== post-provision verification ==="
for REP in s01 s02; do
  WS="$DEST/$REP"
  python3 harness/watchdog.py "$WS" --dry-run | sed "s/^/  /"
done

echo
echo "=== registry ==="
python3 - "$DEST" <<'PY'
import json,sys,hashlib
from pathlib import Path
dest=Path(sys.argv[1])
rows=[]
for rec in sorted(dest.glob("*-provision-receipt.json")):
    d=json.loads(rec.read_text())
    rows.append((d["replicate_id"],d["arm"],d["phase"],d["db_files"],
                 d["appendix_a_present"],d["charter_sha256"][:12],d["deadline_kst"][:16]))
print(f"  {'rep':<5}{'arm':<9}{'phase':<7}{'db':>6}  {'appA':<6}{'charter':<14}deadline")
for r in rows:
    print(f"  {r[0]:<5}{r[1]:<9}{r[2]:<7}{r[3]:>6}  {str(r[4]):<6}{r[5]:<14}{r[6]}")
if len({r[5] for r in rows})!=len(rows):
    print("  NOTE: two arms share a charter hash -- appendix split did not take effect")
PY
echo
echo "Next: harness/collect.sh --dest $DEST   (at deadline or on early filing)"
