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
  SD="$HOME/.claude/projects/-home1-users-Bei-ws-$REP"
  [ -d "$SD" ] && python3 harness/meter_tokens.py --session-dir "$SD" \
      --remote-ws "/home1/users/Bei/ws/$REP" 2>/dev/null || echo "  [meter-tokens] $REP: no session transcripts yet"
done
for REP in s01 s02; do
  ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei "cat /home1/users/Bei/ws/$REP/usage.json 2>/dev/null" \
    | sed "s/^/  [$REP usage] /"
done
echo "  --- transcript audit (charter section 4) ---"
for REP in s01 s02; do python3 harness/audit_transcript.py "$REP" 2>/dev/null | sed 's/^/  /'; done
./harness/restart_watch.sh 2>/dev/null | sed 's/^/  /'
echo "  --- escalations ---"
python3 harness/escalate.py --queue 2>/dev/null | sed 's/^/  /'
