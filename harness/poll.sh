#!/usr/bin/env bash
# One operational poll of the whole smoke fleet. Run every 10 minutes (ratified interval).
#   harvest finished cput -> meter compute -> meter tokens -> watchdog -> fleet -> escalations
#   -> restart watch -> queue-depth covariate -> divergence panel
set -uo pipefail
cd "$(dirname "$0")/.."
echo "=========== poll $(date -u +%FT%TZ) ==========="
# Active replicates come from the registry that launch_sessions.sh writes, never from a list
# baked into this file. See SI-019.
ACTIVE=$(cat harness/state/active_replicates 2>/dev/null | tr '\n' ' ')
[ -n "$ACTIVE" ] || { echo "[poll] no active replicates registered — nothing to watch"; exit 0; }

for REP in $ACTIVE; do
  ./harness/harvest_cput.sh "$REP" 2>/dev/null || echo "  [harvest] $REP unreachable"
  ./harness/meter_compute.sh "$REP" 2>/dev/null || echo "  [meter-compute] $REP unreachable"
done
for REP in $ACTIVE; do
  # Transcript dir is keyed on the session's LOCAL cwd, not the remote workspace. The first
  # version derived it from the remote path and therefore silently metered nothing.
  CWD="$PWD/harness/sessions/$REP"
  SD="$HOME/.claude/projects/$(printf '%s' "$CWD" | sed 's|/|-|g')"
  if [ -d "$SD" ]; then
    python3 harness/meter_tokens.py --session-dir "$SD" --remote-ws "/home1/users/Bei/ws/$REP" 2>/dev/null \
      || echo "  [meter-tokens] $REP: metering failed"
  else
    echo "  [meter-tokens] $REP: no session transcripts yet ($SD)"
  fi
done
echo "  --- replicate escalations ---"
for REP in $ACTIVE; do
  ./harness/escalate_remote.sh "$REP" 2>/dev/null | sed "s/^/  /" \
    || echo "  [escalate] $REP: could not read workspace"
done
for REP in $ACTIVE; do
  ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei "cat /home1/users/Bei/ws/$REP/usage.json 2>/dev/null" \
    | sed "s/^/  [$REP usage] /"
done
echo "  --- watchdog (charter section 4: budgets, liveness) ---"
for REP in $ACTIVE; do ./harness/watchdog_remote.sh "$REP" 2>&1 | sed 's/^/  /'; done
echo "  --- transcript audit (charter section 4) ---"
for REP in $ACTIVE; do python3 harness/audit_transcript.py "$REP" 2>/dev/null | sed 's/^/  /'; done
./harness/restart_watch.sh 2>/dev/null | sed 's/^/  /'
echo "  --- escalations ---"
python3 harness/escalate.py --queue 2>/dev/null | sed 's/^/  /'
echo "  --- shared-queue depth (crowding covariate, Flag I) ---"
python3 harness/queue_depth.py 2>&1 | sed 's/^/  /'
echo "  --- mechanical divergence panel ---"
python3 harness/divergence.py 2>&1 | sed 's/^/  /'
