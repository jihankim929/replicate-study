#!/bin/bash
# One-line-per-fact campaign status.  Never dumps raw output.
export PATH=$PATH:/usr/local/mjs
WS=/home1/users/Bei/ws/rep04
cd $WS
echo "T-minus: $(python3 -c "
import datetime
d=datetime.datetime.strptime('2026-09-05 19:41:33','%Y-%m-%d %H:%M:%S')
n=datetime.datetime.now()
h=(d-n).total_seconds()/3600.0
print('%.1f h to deadline (now %s)'%(h,n.strftime('%m-%d %H:%M')))")"
echo "RUNNING: $(qstat -u Bei 2>/dev/null | awk '/rep04_/{printf "%s(%s,%score,%s) ",$4,$10,$7,$11}')"
echo "PENDING: $(qinfo 2>/dev/null | awk '/rep04_/{printf "%s(%s) ",$3,$2}')"
echo "OTHERBEI: $(qstat -u Bei 2>/dev/null | grep -c 'rep0[^4]') jobs; free-amd=$(quse 2>/dev/null | awk '/User: Bei/{f=1} f&&/^amd/{print 80-$2; exit}') free-aa=$(quse 2>/dev/null | awk '/User: Bei/{f=1} f&&/^aa/{print 38-$2; exit}')"
for f in results/*.csv; do
  [ -e "$f" ] || continue
  echo "RESULT $f: $(( $(wc -l < $f) - 1 )) rows"
done
if [ -d results/desc ]; then
  echo "DESC: $(cat results/desc/*.csv 2>/dev/null | grep -vc '^sid' ) structures done"
fi
echo "CPUH: $(python3 bin/cpuh.py 2>/dev/null)"
