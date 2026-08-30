#!/usr/bin/env bash
# One operational poll of the whole fleet -- WHICHEVER fleet is registered in
# harness/state/active_replicates. This file is phase-agnostic; the cadence it runs at is not.
#
#   CADENCE IS PHASE-SCOPED, and is NOT set here:
#       config.py  "watchdog_poll_minutes": {"smoke": 10, "main": 30}
#   The scheduler holds the live figure -- harness/systemd/study.poll.timer (OnCalendar=*:0/30
#   for main). The overshoot bound that depends on it is 8.33 CPU-h / 2.45 % at smoke and
#   6.00 CPU-h / 0.375 % at main, and watchdog.py computes it from the MEASURED interval
#   between real fires, not from either constant. See SI-023.
#
#   This header used to read "the whole smoke fleet ... every 10 minutes (ratified interval)".
#   Both halves were true of the smoke and only the second half got quoted, which is how a
#   main-phase host came to be polled at the smoke cadence. SI-023, and the same class as
#   SI-018/SI-019: a phase-scoped value read out of phase.
#
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
