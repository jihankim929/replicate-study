#!/bin/bash
# One-line-per-topic campaign status. Never dumps raw output into the session.
cd /home1/users/Bei/ws/rep09
echo "TIME  $(date -Iseconds)  deadline 2026-09-05T19:41:39+09:00"
echo "QUEUE $(/usr/local/mjs/qinfo 2>/dev/null | grep -c rep09_) rep09 jobs in mjs queue; running: $(qstat -a 2>/dev/null | grep -c rep09_)"
/bin/python3 - <<'PY'
import csv, glob, os, collections
WS="/home1/users/Bei/ws/rep09"
tot_pts=0; tot_cpu=0.0; per=collections.defaultdict(lambda:[0,0.0,0])
for p in sorted(glob.glob(WS+"/tables/*_[0-9][0-9].csv")):
    wave=os.path.basename(p).rsplit("_",1)[0]
    for r in csv.DictReader(open(p)):
        try: w=float(r["wall_s"])
        except Exception: continue
        per[wave][0]+=1; per[wave][1]+=w
        if r["status"]!="ok": per[wave][2]+=1
        tot_pts+=1; tot_cpu+=w
for wave,(n,w,bad) in sorted(per.items()):
    print("WAVE  %-6s points=%-6d cpu_h=%7.2f  nonok=%d" % (wave,n,w/3600.0,bad))
print("CPU   total_from_results=%.1f h of 1610 (%.1f%%)  [job wall x ppn is the charged basis; see accounting.md]"
      % (tot_cpu/3600.0, 100*tot_cpu/3600.0/1610))
PY
