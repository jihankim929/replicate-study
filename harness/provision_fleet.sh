#!/usr/bin/env bash
# Provision + transfer the waiting main-phase replicates, SERIALLY, with retries.
#
# The first attempt ran provision->transfer in a tight loop with no retry and no abort. When the
# cluster went unreachable it produced three TRANSFER FAILED lines, carried on to the next
# replicate, and would have finished "successfully" with a half-built fleet. A fleet is not a
# thing you want partially built: replicate N+1 launching against an empty db/ is a silent-wrong
# campaign, not an error.
#
# Rules here:
#   * serial, never concurrent -- concurrent ssh is what preceded the outage
#   * up to RETRIES attempts per replicate, with a pause between
#   * consecutive failures ABORT the run rather than grinding through the roster
#   * a reachability check before each replicate, so a dead cluster stops the loop immediately
#
#   ./harness/provision_fleet.sh [rep02 rep03 ...]    # default: every main id except rep01
set -uo pipefail
cd "$(dirname "$0")/.."
RETRIES=3; PAUSE=45; CONSEC_ABORT=2

IDS="$*"
if [ -z "$IDS" ]; then
  IDS=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(' '.join(i for i in C.RATIFIED['phases']['main']['ids'] if i!='rep01'))")
fi

OK=""; BAD=""; CONSEC=0
for R in $IDS; do
  echo "=== $R ==="
  if ! ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei 'true' 2>/dev/null; then
    echo "  cluster unreachable -- stopping before $R rather than failing through the roster"
    BAD="$BAD $R"; break
  fi
  done_ok=0
  for attempt in $(seq 1 $RETRIES); do
    rm -rf "reps/main/$R" "reps/main/$R-provision-receipt.json"
    if python3 harness/provision.py "$R" --dest reps/main --remote-root "/home1/users/Bei/ws/$R" >/dev/null 2>&1 \
       && bash harness/transfer.sh "$R" --dest reps/main 2>&1 | tail -3 \
       && bash harness/fix_makegrid.sh "$R" >/dev/null 2>&1; then
      echo "  $R OK (attempt $attempt)"; done_ok=1; break
    fi
    echo "  $R attempt $attempt failed"; sleep $PAUSE
  done
  if [ "$done_ok" = 1 ]; then OK="$OK $R"; CONSEC=0
  else BAD="$BAD $R"; CONSEC=$((CONSEC+1))
    [ "$CONSEC" -ge "$CONSEC_ABORT" ] && { echo "  ABORT: $CONSEC consecutive failures"; break; }
  fi
done
echo "=== provisioned:$OK"
echo "=== failed/skipped:$BAD"
[ -z "$BAD" ] || exit 1
