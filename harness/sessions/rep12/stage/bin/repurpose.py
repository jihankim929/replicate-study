"""Rewrite the body of an already-queued PBS file, keeping its resource line.

The mjs scheduler stores a job's *path* and runs `qsub` on it when a slot opens,
so the file on disk at dispatch time is what runs.  Rewriting the body lets a
job queued hours ago do the work I now know is worth doing, without a `qas`
resubmission that would reset its FIFO position.  The `#PBS -l nodes=` line is
copied verbatim: mjs did its core accounting from that string at submission
time, so changing it would make the scheduler's bookkeeping wrong.

usage: repurpose.py <jobname> <mode:work|desc> [args...]
  work <maxseconds>          -- run ppn pull-based GCMC workers
  desc <shards...>           -- run the descriptor sweep on the given shards
"""
import os, re, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")

HEAD = """#!/bin/sh
#PBS -r n
#PBS -q long
#PBS -N %(jobname)s
#PBS -l %(nodes)s
#PBS -j oe
#PBS -o %(ws)s/logs/%(jobname)s.log
set -u
cd $PBS_O_WORKDIR || exit 1
export WSROOT=%(ws)s
export PYTHONPATH=%(ws)s/pylib
"""

WORK = """mkdir -p %(ws)s/work %(ws)s/runs/scr %(ws)s/tables/scr
for w in $(seq 1 %(ppn)d); do
  bash %(ws)s/bin/qworker.sh %(ws)s/work/queue.txt %(ws)s/runs/scr \\
       %(ws)s/tables/scr/%(jobname)s.$w.csv %(maxs)d &
done
wait
echo "DONE %(jobname)s $(date -u +%%FT%%TZ)"
"""

DESC = """mkdir -p %(ws)s/desc
for w in %(shards)s; do
  if [ ! -s %(ws)s/desc/shard_$w.csv ]; then
    python3 %(ws)s/bin/descsweep.py $w %(nsh)d %(npts)d %(ws)s/desc/shard_$w.csv &
  fi
done
wait
echo "DONE %(jobname)s $(date -u +%%FT%%TZ)"
"""


def main():
    jobname = sys.argv[1]
    mode = sys.argv[2]
    p = os.path.join(WS, "pbs", jobname + ".pbs")
    old = open(p).read()
    m = re.search(r"^#PBS -l (nodes=\S+)", old, re.M)
    nodes = m.group(1)
    ppn = int(re.search(r"ppn=(\d+)", nodes).group(1))
    d = dict(jobname=jobname, nodes=nodes, ws=WS, ppn=ppn)
    if mode == "work":
        d["maxs"] = int(sys.argv[3])
        body = WORK % d
    else:
        d["shards"] = " ".join(sys.argv[3].split(","))
        d["nsh"] = int(sys.argv[4])
        d["npts"] = int(sys.argv[5])
        body = DESC % d
    with open(p, "w") as f:
        f.write(HEAD % d + body)
    print("%s -> %s (%s, ppn=%d)" % (jobname, mode, nodes, ppn))


if __name__ == "__main__":
    main()
