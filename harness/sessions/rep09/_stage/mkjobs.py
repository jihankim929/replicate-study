"""Build interleaved task chunks and PBS scripts for a GCMC wave.

Usage:
  mkjobs.py <wave> <njobs> <ppn> <nodeclass> <init> <prod> <pressures> [idfile]

<pressures> is a comma list in Pa. <idfile>, if given, is a file of structure
ids, one per line; otherwise the whole manifest is used. Points already present
in tables/<wave>.csv with the same pressure/cycles are skipped, so a wave can be
resubmitted after a failure without repeating work.
"""
import os, sys, csv

WS = "/home1/users/Bei/ws/rep09"

PBS = """#!/bin/bash
#PBS -N rep09_{wave}_{k:02d}
#PBS -q long
#PBS -l nodes=1:ppn={ppn}:{cls}
#PBS -j oe
#PBS -o {ws}/jobs/{wave}_{k:02d}.out

cd {ws}
export RASPA_DIR={ws}/raspa_home
export SCRATCH=/tmp/rep09_{wave}_{k:02d}_$PBS_JOBID
mkdir -p $SCRATCH
/bin/python3 {ws}/bin/run_batch.py {ws}/jobs/{wave}_{k:02d}.tasks \\
    {ws}/tables/{wave}_{k:02d}.csv {ppn} nokeep 7200
rm -rf $SCRATCH
echo FINISHED {wave}_{k:02d}
"""


def done_set(wave):
    d = set()
    for k in range(64):
        p = os.path.join(WS, "tables", "%s_%02d.csv" % (wave, k))
        if os.path.exists(p):
            for r in csv.DictReader(open(p)):
                if r.get("status") == "ok":
                    d.add((int(r["idx"]), int(float(r["pressure_Pa"]))))
    return d


def main():
    wave, njobs, ppn, cls = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    init, prod = int(sys.argv[5]), int(sys.argv[6])
    pressures = [int(float(x)) for x in sys.argv[7].split(",")]
    if len(sys.argv) > 8:
        ids = [int(x) for x in open(sys.argv[8]).read().split()]
    else:
        ids = [int(r["id"]) for r in csv.DictReader(
            open(os.path.join(WS, "manifests/structures.csv")))]

    have = done_set(wave)
    tasks = [(i, p) for i in ids for p in pressures if (i, p) not in have]
    os.makedirs(os.path.join(WS, "jobs"), exist_ok=True)

    # interleave so every chunk sees the same cost distribution
    files = []
    for k in range(njobs):
        tp = os.path.join(WS, "jobs", "%s_%02d.tasks" % (wave, k))
        with open(tp, "w") as f:
            for (i, p) in tasks[k::njobs]:
                f.write("%d,%d,%d,%d,1\n" % (i, p, init, prod))
        sp = os.path.join(WS, "jobs", "%s_%02d.pbs" % (wave, k))
        with open(sp, "w") as f:
            f.write(PBS.format(wave=wave, k=k, ppn=ppn, cls=cls, ws=WS))
        files.append(sp)
    print("tasks", len(tasks), "already done", len(have))
    print(" ".join(files))


if __name__ == "__main__":
    main()
