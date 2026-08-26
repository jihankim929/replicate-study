#!/usr/bin/env bash
# One operational poll of the whole smoke fleet. Run every 10 minutes (ratified interval).
#   harvest finished cput -> meter compute -> meter tokens -> watchdog -> fleet -> escalations
set -uo pipefail
cd "$(dirname "$0")/.."
echo "=========== poll $(date -u +%FT%TZ) ==========="
for REP in s01 s02; do
  ./harness/harvest_cput.sh "$REP" 2>/dev/null || echo "  [harvest] $REP unreachable"
  ./harness/meter_compute.sh "$REP" 2>/dev/null || echo "  [meter-compute] $REP unreachable"
done
for REP in s01 s02; do
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
for REP in s01 s02; do
  ./harness/escalate_remote.sh "$REP" 2>/dev/null | sed "s/^/  /" \
    || echo "  [escalate] $REP: could not read workspace"
done
for REP in s01 s02; do
  ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei "cat /home1/users/Bei/ws/$REP/usage.json 2>/dev/null" \
    | sed "s/^/  [$REP usage] /"
done
echo "  --- watchdog (charter section 4: budgets, liveness) ---"
for REP in s01 s02; do ./harness/watchdog_remote.sh "$REP" 2>&1 | sed 's/^/  /'; done
echo "  --- transcript audit (charter section 4) ---"
for REP in s01 s02; do python3 harness/audit_transcript.py "$REP" 2>/dev/null | sed 's/^/  /'; done
./harness/restart_watch.sh 2>/dev/null | sed 's/^/  /'
echo "  --- escalations ---"
python3 harness/escalate.py --queue 2>/dev/null | sed 's/^/  /'
echo "  --- mechanical divergence panel ---"
python3 harness/divergence.py 2>&1 | sed 's/^/  /'
