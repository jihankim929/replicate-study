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
# The first run of this probe used SLEEP=120 and sampled for exactly 120s. PBS dispatched at
# roughly 7-8 jobs per 15s, so `running` was still climbing monotonically (52, 18 still queued)
# when the earliest jobs began exiting and the window closed. That is a DISPATCH RAMP, not a
# ceiling, and the script called it a cap. The walltime must exceed the time to dispatch all N
# with margin, and the verdict must require a PLATEAU rather than a maximum.
SLEEP=420
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
  # qdel does not take effect instantly, so counting once immediately after it reports a
  # frightening number that is merely stale. Loop until clear, and say so if it is not.
  # Job ids MUST come from qselect, not from a qstat column. `qstat -u` truncates the id to
  # its column width -- "3472261.bnode0.kaist.a" instead of "...kaist.ac.kr" -- and qdel
  # rejects that as "illegally formed job identifier" while returning rc=0, so the first two
  # runs of this probe deleted NOTHING and the jobs merely expired on their own. That is the
  # same defect as the "Lm 58" this script exists to disprove: a value read off a formatted
  # display column instead of from a machine-readable source. Do not reintroduce it.
  ssh -o BatchMode=yes -o ConnectTimeout=120 dirac-bei '
    export PATH=$PATH:/usr/local/pbs/bin
    for pass in 1 2 3 4 5 6; do
      probe=""
      for j in $(qselect -u Bei 2>/dev/null); do
        nm=$(qstat -f "$j" 2>/dev/null | awk -F"= " "/Job_Name/{print \$2}" | tr -d " \r")
        case "$nm" in '"$TAG"'_*) probe="$probe $j" ;; esac
      done
      [ -z "$probe" ] && break
      qdel $probe >/dev/null 2>&1
      sleep 8
    done
    n=$(qstat -u Bei 2>/dev/null | grep -c '"$TAG"'_)
    echo "   remaining probe jobs: $n"
    [ "$n" = "0" ] || echo "   !! probe jobs still present -- qdel by hand before leaving"
    rm -rf /home1/users/Bei/limitprobe
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

echo "-- sampling concurrency (a ceiling is a PLATEAU with work still queued, not a maximum) --"
MAXRUN=0; PREV=-1; PLATEAU=0; LASTQ=0; CLIMBING=1
SAMPLES=$(( (SLEEP - 60) / 15 ))     # stop before the earliest jobs start exiting
for i in $(seq 1 "$SAMPLES"); do
  read -r R Q <<<"$(ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei "
    export PATH=\$PATH:/usr/local/pbs/bin
    qstat -u Bei 2>/dev/null | grep ${TAG}_ | awk '{print \$10}' | sort | uniq -c |
      awk '/ R\$/{r=\$1} / Q\$/{q=\$1} END{printf \"%d %d\", r+0, q+0}'")"
  R=${R:-0}; Q=${Q:-0}
  [ "$R" -gt "$MAXRUN" ] && MAXRUN=$R
  # A plateau is consecutive samples at the same running count WHILE work is still queued.
  # Without the "still queued" clause, a burst that has fully dispatched looks like a ceiling.
  if [ "$R" -eq "$PREV" ] && [ "$Q" -gt 0 ]; then PLATEAU=$((PLATEAU+1)); else PLATEAU=0; fi
  PREV=$R; LASTQ=$Q
  printf '   t+%3ds  running=%-4s queued=%-4s  max_seen=%-4s plateau=%s\n' \
    "$((i*15))" "$R" "$Q" "$MAXRUN" "$PLATEAU"
  # Decisive early exit: strictly more than the value under test are running at once.
  if [ "$R" -gt 58 ]; then CLIMBING=0; break; fi
  # Decisive the other way: held flat for 4 samples (60s) with jobs still waiting.
  if [ "$PLATEAU" -ge 4 ]; then CLIMBING=0; break; fi
  sleep 15
done

echo
TS=$(date -u +%FT%TZ)
if [ "$MAXRUN" -gt 58 ]; then
  VERDICT="no_cap_at_58"
  echo "== $MAXRUN concurrent jobs ran from one account =="
  echo "   > 58. The 'Lm 58' column is a DISPLAY ARTIFACT of qstat -q's two-character field,"
  echo "   not a limit. Confirms max_user_run = 580."
elif [ "$PLATEAU" -ge 4 ]; then
  VERDICT="real_cap"
  echo "== ceiling observed: $MAXRUN concurrent, held flat with $LASTQ still queued =="
  echo "   A real per-user cap at or below 58 is in force. Fleet reachability is affected;"
  echo "   see config.fleet_reachability() and prereg/seal_notes.md."
else
  VERDICT="inconclusive"
  echo "== INCONCLUSIVE: reached $MAXRUN and was still climbing when the window closed =="
  echo "   This is a dispatch ramp, not a ceiling. Re-run with a longer --sleep."
fi
printf '{"ts":"%s","burst":%d,"sleep_s":%d,"queue":"%s","observed_max_running":%d,"queued_at_end":%d,"plateau_samples":%d,"value_under_test":58,"verdict":"%s"}\n' \
  "$TS" "$N" "$SLEEP" "$QUEUE" "$MAXRUN" "$LASTQ" "$PLATEAU" "$VERDICT" >> "$LEDGER"
echo "   logged -> $LEDGER"
