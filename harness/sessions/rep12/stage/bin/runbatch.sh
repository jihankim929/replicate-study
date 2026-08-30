#!/bin/bash
# Run a shard of a GCMC task list.  One RASPA process at a time per worker.
#
# usage: runbatch.sh <tasklist> <workerid> <nworkers> <rundir> <resultcsv>
# tasklist lines:  <cifname>|<pressure_Pa>|<ncycles>|<ninit>|<tag>|<gridspacing or ->
#
# Result CSV columns:
#   tag,cifname,pressure,ncyc,ninit,grid,loading_cm3cm3,err_cm3cm3,
#   loading_molkg,err_molkg,nmol,sec,status
set -u
WS=${WSROOT:-/home1/users/Bei/ws/rep12}
TASKS=$1; WID=$2; NW=$3; RUNDIR=$4; RES=$5
export RASPA_DIR=$WS/raspa_home
export LD_LIBRARY_PATH=$WS/toolchain/raspa/lib:${LD_LIBRARY_PATH:-}
RASPA=$WS/toolchain/raspa/bin/simulate

i=0
while IFS='|' read -r cif press ncyc ninit tag gspc; do
  [ -z "${cif:-}" ] && continue
  case "$cif" in \#*) continue;; esac
  if [ $((i % NW)) -ne "$WID" ]; then i=$((i+1)); continue; fi
  i=$((i+1))
  d="$RUNDIR/$tag"
  rm -rf "$d"
  if [ "$gspc" = "-" ]; then
    python3 "$WS/bin/mkinput.py" "$cif" "$press" "$ncyc" "$ninit" "$d" >/dev/null 2>&1
  else
    python3 "$WS/bin/mkinput.py" "$cif" "$press" "$ncyc" "$ninit" "$d" "$gspc" >/dev/null 2>&1
  fi
  if [ ! -f "$d/simulation.input" ]; then
    echo "$tag,\"$cif\",$press,$ncyc,$ninit,$gspc,,,,,,0,MKINPUT_FAIL" >> "$RES"
    continue
  fi
  t0=$(date +%s)
  ( cd "$d" && timeout 40000 $RASPA simulation.input > raspa.stdout 2>&1 )
  rc=$?
  t1=$(date +%s)
  f=$(ls "$d"/Output/System_0/output_*.data 2>/dev/null | head -1)
  if [ -z "$f" ] || [ ! -s "$f" ]; then
    echo "$tag,\"$cif\",$press,$ncyc,$ninit,$gspc,,,,,,$((t1-t0)),NOOUT_rc$rc" >> "$RES"
    rm -rf "$d/Movies" "$d/VTK" "$d/Restart"
    continue
  fi
  python3 "$WS/bin/extract.py" "$f" "$tag" "$cif" "$press" "$ncyc" "$ninit" "$gspc" $((t1-t0)) >> "$RES"
  gzip -f "$f"
  rm -rf "$d/Movies" "$d/VTK" "$d/Restart"
done < "$TASKS"
exit 0
