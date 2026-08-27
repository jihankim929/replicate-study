#!/usr/bin/env bash
# Empirically verify the PBS per-user CONCURRENT RUN limit from the Bei account.
#
# Why this exists. `qstat -q` prints an `Lm` column in a TWO-CHARACTER field. PBS Pro 4.2.10
# renders the per-user run limit there, so a configured 580 displays as "58". The configured
# value is readable directly -- `qmgr -c "list server max_user_run"` -- and on 2026-08-28 it
# read 580 on every queue with no queue-level override and no limit hooks. This script settles
# the question the config file cannot: what the scheduler ACTUALLY lets one account run at once.
#
# The test is a burst of short sleep jobs. It is deliberately: single-core, tiny, walltime-
# capped, tagged so every job is identifiable, and cleaned up unconditionally on exit.
#
#   ./harness/verify_run_limit.sh --dry-run     # print the plan, submit nothing
#   ./harness/verify_run_limit.sh --n 70        # real burst of 70
#
# NOT run automatically by poll.sh. It puts load on a SHARED queue and is a deliberate act.
set -uo pipefail
cd "$(dirname "$0")/.."

N=70                       # must exceed the value under test (58) with margin
SLEEP=180                  # long enough for all to be running at once, short enough to be cheap
QUEUE=long
TAG="limitprobe"
LEDGER=harness/run_limit_probe.jsonl
DRY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --n) N="$2"; shift ;;
    --sleep) SLEEP="$2"; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

echo "== PBS per-user run-limit probe =="
echo "   burst: $N jobs x sleep ${SLEEP}s, queue $QUEUE, tag ${TAG}_"
echo "   value under test: the 'Lm 58' shown by qstat -q"
echo

echo "-- configured limits, read directly (the display column is not evidence) --"
ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei '
  export PATH=$PATH:/usr/local/pbs/bin
  qmgr -c "list server max_user_run" 2>&1 | grep -i max_user_run
  qmgr -c "list queue long max_running"  2>&1 | grep -i max_running
  echo -n "   qstat -q Lm column shows: "; qstat -q 2>/dev/null | awk "/^long/{print \$8}"
'
echo

if [ -n "$DRY" ]; then
  echo "(dry-run) would submit $N jobs, sample concurrency every 15s for ${SLEEP}s, then qdel all ${TAG}_ jobs"
  exit 0
fi

# Cleanup is unconditional: a probe that leaves 70 jobs on a shared queue is worse than no probe.
cleanup() {
  echo "-- cleanup: deleting every ${TAG}_ job --"
  ssh -o BatchMode=yes -o ConnectTimeout=30 dirac-bei '
    export PATH=$PATH:/usr/local/pbs/bin
    ids=$(qstat -u Bei 2>/dev/null | grep '"$TAG"'_ | awk "{print \$1}")
    [ -n "$ids" ] && qdel $ids 2>/dev/null
    sleep 3
    echo -n "   remaining probe jobs: "; qstat -u Bei 2>/dev/null | grep -c '"$TAG"'_ || echo 0
  '
}
trap cleanup EXIT INT TERM

echo "-- submitting --"
ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "
  export PATH=\$PATH:/usr/local/pbs/bin
  cd /home1/users/Bei
  mkdir -p limitprobe && cd limitprobe
  for i in \$(seq 1 $N); do
    printf '#!/bin/bash\n#PBS -N ${TAG}_%03d\n#PBS -q $QUEUE\n#PBS -l select=1:ncpus=1\n#PBS -l walltime=00:10:00\n#PBS -j oe\nsleep $SLEEP\n' \"\$i\" > p\$i.sh
    qsub p\$i.sh >/dev/null 2>&1
  done
  echo \"   submitted $N\"
"

echo "-- sampling concurrency (the observed ceiling is the max RUNNING across samples) --"
MAXRUN=0
SAMPLES=$((SLEEP / 15))
for i in $(seq 1 "$SAMPLES"); do
  read -r R Q <<<"$(ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei "
    export PATH=\$PATH:/usr/local/pbs/bin
    qstat -u Bei 2>/dev/null | grep ${TAG}_ | awk '{print \$10}' | sort | uniq -c |
      awk '/ R\$/{r=\$1} / Q\$/{q=\$1} END{printf \"%d %d\", r+0, q+0}'")"
  R=${R:-0}; Q=${Q:-0}
  [ "$R" -gt "$MAXRUN" ] && MAXRUN=$R
  printf '   t+%3ds  running=%-4s queued=%-4s  max_seen=%s\n' "$((i*15))" "$R" "$Q" "$MAXRUN"
  sleep 15
done

echo
echo "== observed ceiling: $MAXRUN concurrent jobs from one account =="
if [ "$MAXRUN" -gt 58 ]; then
  echo "   > 58 -- the 'Lm 58' column is a DISPLAY ARTIFACT, not a limit."
else
  echo "   <= 58 -- a real per-user cap at or below 58 is in force. Fleet reachability is affected;"
  echo "   see config.fleet_reachability() and prereg/seal_notes.md."
fi
TS=$(date -u +%FT%TZ)
printf '{"ts":"%s","burst":%d,"sleep_s":%d,"queue":"%s","observed_max_running":%d,"value_under_test":58}\n' \
  "$TS" "$N" "$SLEEP" "$QUEUE" "$MAXRUN" >> "$LEDGER"
echo "   logged -> $LEDGER"
