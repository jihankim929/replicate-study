"""Submit part of the whole-database descriptor sweep.

usage: subdesc.py <njobs> <ppn> <npts> <prop> <job_offset> <nshards_total>

Shards are strided over the sorted db listing, so any subset of shards can be
submitted independently and the union covers the database exactly once.
Small ppn is deliberate: the ac/amd nodes are 32-44 cores and shared with other
replicates, so a job asking for many cores on one node sits in the queue.
"""
import os, subprocess, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
QAS = "/usr/local/mjs/qas"

PBS = """#!/bin/sh
#PBS -r n
#PBS -q long
#PBS -N %(jobname)s
#PBS -l nodes=1:ppn=%(ppn)d:%(prop)s
#PBS -j oe
#PBS -o %(ws)s/logs/%(jobname)s.log
set -u
cd $PBS_O_WORKDIR || exit 1
export WSROOT=%(ws)s
mkdir -p %(ws)s/desc
for w in %(shards)s; do
  if [ ! -s %(ws)s/desc/shard_$w.csv ]; then
    python3 %(ws)s/bin/descsweep.py $w %(nsh)d %(npts)d %(ws)s/desc/shard_$w.csv &
  fi
done
wait
echo "DONE %(jobname)s $(date -u +%%FT%%TZ)"
"""


def main():
    njobs, ppn, npts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    prop = sys.argv[4]
    off = int(sys.argv[5])
    nsh = int(sys.argv[6])
    os.makedirs(os.path.join(WS, "pbs"), exist_ok=True)
    out = []
    for j in range(njobs):
        gj = off + j
        shards = " ".join(str(s) for s in range(nsh) if s % ((nsh + ppn - 1) // ppn) == 0)
        shards = " ".join(str(gj * ppn + k) for k in range(ppn) if gj * ppn + k < nsh)
        if not shards:
            continue
        jobname = "rep12_desc%02d" % gj
        p = os.path.join(WS, "pbs", jobname + ".pbs")
        with open(p, "w") as f:
            f.write(PBS % dict(jobname=jobname, ppn=ppn, prop=prop, ws=WS,
                               shards=shards, nsh=nsh, npts=npts))
        r = subprocess.run([QAS, p], stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        out.append("%s %s" % (jobname, r.stdout.decode().strip().replace("\n", " ")))
    print("\n".join(out))


if __name__ == "__main__":
    main()
