"""Split a task list into N PBS jobs and submit them with qas.

usage: submit.py <tasklist> <njobs> <ppn> <jobtag> <rundir> <resdir> [prop]

Each job runs <ppn> runbatch.sh workers over its own sub-list.  Job names are
rep12_<jobtag><nn> (charter s4: jobs carry the replicate id).
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
#PBS -o %(logs)s/%(jobname)s.log
set -u
cd $PBS_O_WORKDIR || exit 1
export WSROOT=%(ws)s
mkdir -p %(rundir)s %(resdir)s
for w in $(seq 0 %(ppnm1)d); do
  bash %(ws)s/bin/runbatch.sh %(sub)s $w %(ppn)d %(rundir)s %(resdir)s/%(jobname)s.$w.csv &
done
wait
echo "DONE %(jobname)s $(date -u +%%FT%%TZ)"
"""


def main():
    tasks, njobs, ppn, tag, rundir, resdir = sys.argv[1:7]
    prop = sys.argv[7] if len(sys.argv) > 7 else "ac"
    njobs, ppn = int(njobs), int(ppn)
    lines = [l.rstrip("\n") for l in open(tasks)
             if l.strip() and not l.startswith("#")]
    os.makedirs(resdir, exist_ok=True)
    os.makedirs(rundir, exist_ok=True)
    logs = os.path.join(WS, "logs")
    pbsdir = os.path.join(WS, "pbs")
    os.makedirs(pbsdir, exist_ok=True)
    subs = [lines[i::njobs] for i in range(njobs)]
    files = []
    for i, s in enumerate(subs):
        if not s:
            continue
        jobname = "rep12_%s%02d" % (tag, i)
        sub = os.path.join(pbsdir, "%s.tasks" % jobname)
        with open(sub, "w") as f:
            f.write("\n".join(s) + "\n")
        p = os.path.join(pbsdir, "%s.pbs" % jobname)
        with open(p, "w") as f:
            f.write(PBS % dict(jobname=jobname, ppn=ppn, ppnm1=ppn - 1,
                               prop=prop, ws=WS, rundir=rundir, resdir=resdir,
                               sub=sub, logs=logs))
        files.append((jobname, p, len(s)))
    out = []
    for jobname, p, n in files:
        r = subprocess.run([QAS, p], stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        out.append("%s ntasks=%d %s" % (jobname, n,
                   r.stdout.decode().strip().replace("\n", " ")))
    print("\n".join(out))


if __name__ == "__main__":
    main()
