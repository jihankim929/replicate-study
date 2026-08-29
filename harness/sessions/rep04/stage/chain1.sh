#!/bin/bash
# chain1.sh — runs detached on the login node.
# Waits for the descriptor sweep to finish, merges and ranks it, selects the
# GCMC calibration sample, and submits the calibration job.  Everything it does
# is deterministic and already decided; it makes no scientific choice.
WS=/home1/users/Bei/ws/rep04
export PATH=$PATH:/usr/local/mjs
export REP04_WS=$WS
cd $WS
exec >> $WS/logs/chain1.log 2>&1
echo "=== chain1 start $(date +%H:%M:%S) ==="

# 1. wait for the descriptor sweep (bounded: 3 h)
S=$(date +%s)
while true; do
  D=$(cat $WS/results/desc/*.csv 2>/dev/null | grep -vc "^sid")
  [ "$D" -ge 12499 ] && { echo "desc complete: $D"; break; }
  [ $(( $(date +%s) - S )) -ge 10800 ] && { echo "desc TIMEOUT at $D"; break; }
  sleep 60
done

# 2. merge + rank + select
python3 $WS/bin/rank.py merge > $WS/logs/rank_merge.txt 2>&1
python3 $WS/bin/rank.py select 72 >> $WS/logs/rank_merge.txt 2>&1
echo "rank done: $(wc -l < $WS/manifest/calib_sids.txt) calibration structures"

# 3. build and submit the calibration GCMC job (floor cycles, both pressures,
#    grid-free — this is the set the screening surrogate is calibrated against,
#    so it must be free of any grid approximation)
echo "sid,P_Pa,ninit,nprod,seed,grid,wall_s,rc,uc,rho_kgm3,n_uc,n_uc_err,vol_cm3cm3,vol_err,molkg,molkg_err,henry,ok" > $WS/results/calib.csv
rm -f $WS/jobs/calib.tasks
while read s; do
  echo "$s 6500000 2000 10000 calib 0 no" >> $WS/jobs/calib.tasks
  echo "$s 580000 2000 10000 calib 0 no"  >> $WS/jobs/calib.tasks
done < $WS/manifest/calib_sids.txt
python3 $WS/bin/mkjob.py calib $WS/jobs/calib.tasks 16 amd 24 case > /dev/null
qas $WS/jobs/calib.pbs
echo "calib submitted: $(wc -l < $WS/jobs/calib.tasks) cases"
echo "=== chain1 end $(date +%H:%M:%S) ==="
