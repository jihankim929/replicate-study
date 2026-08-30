#!/bin/bash
# One-line-per-item campaign status.  Charter s4: never poll by dumping raw
# scheduler output into the session.
WS=${WSROOT:-/home1/users/Bei/ws/rep12}
cd "$WS" || exit 1
q=$(/usr/local/mjs/qinfo 2>/dev/null | grep -c rep12_)
r=$(qstat 2>/dev/null | grep -c rep12_)
echo "jobs_in_mjs_queue=$q pbs_visible=$r"
echo "desc_shards=$(ls desc/*.csv 2>/dev/null | wc -l) desc_rows=$(cat desc/*.csv 2>/dev/null | grep -vc '^name')"
for d in tables/*/; do
  n=$(cat "$d"/*.csv 2>/dev/null | wc -l)
  ok=$(cat "$d"/*.csv 2>/dev/null | grep -c ',OK$')
  [ "$n" -gt 0 ] && echo "results $(basename "$d"): lines=$n ok=$ok"
done
cpu=$(cat tables/cpu_used.txt 2>/dev/null || echo 0)
echo "cpu_h_accounted=$cpu"
