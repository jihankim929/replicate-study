#!/usr/bin/env python3
"""Extract cycle-convergence trajectories from archived RASPA outputs.

Every run in the smoke archive was written with PrintEvery = cycles/5, so each output carries five
running-average checkpoints at 20/40/60/80/100 % of production. That is the whole dataset: a run's
own running average at fraction f of its length is the estimate a run of length f*L would have
produced, up to the difference in equilibration.

WHAT THIS MEASURES AND WHAT IT DOES NOT. The checkpoints give the WITHIN-RUN statistical
convergence -- how fast the running mean settles toward its own limit. They do not give the
cross-fidelity BIAS, i.e. whether a short run's converged value differs systematically from a long
one's, because that needs paired runs at two fidelities and the archive holds two such structures.
The two questions are reported separately and never summed.

Working capacity needs both pressures at the same cycle count, so runs are paired by
(structure, replicate) and WC is reconstructed at each checkpoint.
"""
import glob, json, os, re, sys, collections

CYC = re.compile(r"Number of cycles:\s*(\d+)")
INIT = re.compile(r"Number of initializing cycles:\s*(\d+)")
EQ = re.compile(r"Number of equilibration cycles:\s*(\d+)")
PE = re.compile(r"Print every:\s*(\d+)")
CUR = re.compile(r"^Current cycle:\s*(\d+) out of (\d+)", re.M)
# the cm^3 STP/cm^3 running average lives on the continuation line of "absolute adsorption"
ABS = re.compile(r"absolute adsorption:.*?\n\s*([\d.eE+-]+)\s*\(avg\.\s*([\d.eE+-]+)\)\s*\[cm\^3 STP/g\],\s*"
                 r"([\d.eE+-]+)\s*\(avg\.\s*([\d.eE+-]+)\)\s*\[cm\^3 STP/cm", re.S)


def parse(path):
    try:
        txt = open(path, errors="ignore").read()
    except Exception:
        return None
    mc = CYC.search(txt)
    if not mc:
        return None
    cycles = int(mc.group(1))
    if cycles < 100:
        return None
    pe = int(PE.search(txt).group(1)) if PE.search(txt) else 0
    init = int(INIT.search(txt).group(1)) if INIT.search(txt) else 0
    eq = int(EQ.search(txt).group(1)) if EQ.search(txt) else 0
    # walk the production checkpoints in order, taking the running average that follows each
    pts = []
    for m in CUR.finditer(txt):
        c = int(m.group(1))
        seg = txt[m.end(): m.end() + 6000]
        a = ABS.search(seg)
        if a:
            pts.append((c, float(a.group(4))))          # cm^3 STP/cm^3, running average
    # pressure and structure from the filename
    base = os.path.basename(path)
    mp = re.search(r"_([\d.]+e\+?\d+|\d+)\.data$", base)
    pressure = float(mp.group(1)) if mp else None
    ms = re.match(r"output_(.+?)_\d+\.\d+\.\d+_", base)
    stem = ms.group(1) if ms else base
    return {"path": path, "stem": stem, "pressure": pressure, "cycles": cycles,
            "init": init, "eq": eq, "print_every": pe, "points": pts}


def main():
    files = glob.glob("reps/smoke/*/**/Output/System_0/*.data", recursive=True)
    out = []
    for f in files:
        r = parse(f)
        if r and len(r["points"]) >= 2:
            out.append(r)
    json.dump(out, open("harness/logs/convergence_traces.json", "w"))
    byc = collections.Counter(r["cycles"] for r in out)
    print(f"  parsed {len(out)} runs with >=2 checkpoints")
    for c, n in sorted(byc.items(), reverse=True):
        pts = [len(r["points"]) for r in out if r["cycles"] == c]
        print(f"    {c:>6} cycles: {n:>5} runs, checkpoints/run min {min(pts)} max {max(pts)}")


if __name__ == "__main__":
    main()
