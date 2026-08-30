#!/bin/bash
# Pull-based GCMC worker.
#
# usage: qworker.sh <queuefile> <rundir> <resfile> <max_seconds> [idle_exit_s]
#
# Why pull and not push: the mjs scheduler stores a job's *path* and runs
# `qsub` on it whenever a slot opens, which on this cluster can be hours after
# submission.  A static task list baked in at submission time would therefore be
# stale by the time it ran, and re-submitting to change it resets the job's FIFO
# position.  Workers instead claim lines from a queue file I can rewrite at any
# time, so priority always reflects what I know now, not what I knew when the
# job was queued.
#
# Claiming is `mkdir`, which is atomic, so many workers across many nodes can
# share one queue with no lock.  A `.done` marker distinguishes finished tasks
# from tasks claimed by a worker that then died.
set -u
WS=${WSROOT:-/home1/users/Bei/ws/rep12}
Q=$1; RUNDIR=$2; RES=$3; MAXS=$4; IDLE=${5:-900}
CLAIM=$WS/work/claimed
mkdir -p "$CLAIM" "$RUNDIR" "$(dirname "$RES")"
export RASPA_DIR=$WS/raspa_home
export LD_LIBRARY_PATH=$WS/toolchain/raspa/lib:${LD_LIBRARY_PATH:-}
RASPA=$WS/toolchain/raspa/bin/simulate
START=$(date +%s)
idle=0

while true; do
  now=$(date +%s); el=$((now-START))
  [ "$el" -ge "$MAXS" ] && { echo "worker: time budget reached"; break; }
  [ -f "$WS/work/STOP" ] && { echo "worker: STOP file"; break; }

  got=""
  while IFS='|' read -r cif press ncyc ninit tag gspc; do
    [ -z "${cif:-}" ] && continue
    case "$cif" in \#*) continue;; esac
    if mkdir "$CLAIM/$tag" 2>/dev/null; then got="$cif|$press|$ncyc|$ninit|$tag|$gspc"; break; fi
  done < "$Q"

  if [ -z "$got" ]; then
    idle=$((idle+60))
    [ "$idle" -ge "$IDLE" ] && { echo "worker: queue empty"; break; }
    sleep 60; continue
  fi
  idle=0

  IFS='|' read -r cif press ncyc ninit tag gspc <<< "$got"
  d="$RUNDIR/$tag"
  rm -rf "$d"
  python3 "$WS/bin/mkinput.py" "$cif" "$press" "$ncyc" "$ninit" "$d" "$gspc" >/dev/null 2>&1
  if [ ! -f "$d/simulation.input" ]; then
    echo "$tag,\"$cif\",$press,$ncyc,$ninit,$gspc,,,,,,0,MKINPUT_FAIL" >> "$RES"
    touch "$CLAIM/$tag/.done"; continue
  fi
  t0=$(date +%s)
  ( cd "$d" && $RASPA > raspa.stdout 2>&1 )
  rc=$?
  t1=$(date +%s)
  f=$(ls "$d"/Output/System_0/output_*.data 2>/dev/null | head -1)
  if [ -z "$f" ] || [ ! -s "$f" ]; then
    echo "$tag,\"$cif\",$press,$ncyc,$ninit,$gspc,,,,,,$((t1-t0)),NOOUT_rc$rc" >> "$RES"
  else
    python3 "$WS/bin/extract.py" "$f" "$tag" "$cif" "$press" "$ncyc" "$ninit" "$gspc" $((t1-t0)) >> "$RES"
    gzip -f "$f"
  fi
  rm -rf "$d/Movies" "$d/VTK" "$d/Restart"
  touch "$CLAIM/$tag/.done"
done
exit 0
