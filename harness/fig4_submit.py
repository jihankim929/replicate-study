#!/usr/bin/env python3
"""Figure-4 interim queue submitter. ONE CORE PER JOB.

Implements the geometry ratified in REPORT 020 (implementation decision (4) revised): one PBS job
per run, `ppn=1` with the node group NAMED -- `qas` rejects a bare `nodes=1:ppn=1`, which is a
syntax requirement and was never a verdict on job size. Groups round-robin over aa/ab/ac/amd.
`ax` stays excluded (mjs staging group, a policy reason that did not expire with the shape reason)
and `xeonphi` stays excluded (CPU-only ruling).

WALLTIME. The sealed SAFETY=3.0 was justified on a BATCH SUM, whose relative variance is small.
Per run the spread is 338x and p99/median 18.3x, so a batch-sized factor would kill runs. But
over-requesting ONE core is nearly free, where over-requesting 23 was not -- so this errs long
deliberately: base x (nsim/median) x 12, floor 3 h, cap 72 h.

WINDOW. Never more than --window jobs queued-and-not-running plus running, topped up as jobs land.
The sealed back-off (ceiling 480 -> 240 on third-party queueing) is unchanged and still applies to
concurrency; this window is about not dumping thousands of jobs into the server at once.
"""
import argparse, csv, json, os, subprocess, sys, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REMOTE = "dirac-bei"
SCREEN = "/home1/users/Bei/screen"
QAS = "/usr/local/mjs/qas"
GROUPS = ["aa", "ab", "ac", "amd"]
BASE_CPU_H = {"floor": 0.913, "claim": 4.565}
CYCLES = {"floor": (2000, 10000), "claim": (10000, 50000)}
MEDIAN_NSIM = 2424
SAFETY = 12.0

TPL = """#!/bin/bash
#PBS -N {name}
#PBS -q long
#PBS -l nodes=1:ppn=1:{group}
#PBS -l walltime={wt}
#PBS -j oe
#PBS -o {root}/logs/{name}.log
set -u
export LC_ALL=C
export RASPA_DIR={root}/raspa_home
D={root}/runs/{rel}
mkdir -p "$D" && cd "$D" || exit 1
cp {root}/decks/{rel}/simulation.input .
S=$(date -u +%s)
{root}/toolchain/raspa/bin/simulate -i simulation.input > raspa.stdout 2>&1
RC=$?
E=$(date -u +%s)
# section 8: RASPA returns 0 whether or not it succeeded. Status is decided by output presence
# and parseability, NEVER by $RC.
OUT=$(ls Output/System_0/*.data 2>/dev/null | head -1)
if [ -n "$OUT" ] && grep -qE 'Average loading absolute .*molecules/unit cell' "$OUT" 2>/dev/null; then
  ST=ok
else
  ST=failed
fi
printf '%s,%s,%s,%s,%s,%s\\n' "{rel}" "$ST" "$RC" "$S" "$E" "$(hostname)" >> {root}/logs/fig4.runs
"""

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)

def remote(script):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=60", REMOTE,
                           "bash", "-s"], input=script, capture_output=True, text=True)

def walltime(nsim, grade):
    h = BASE_CPU_H[grade] * (nsim / MEDIAN_NSIM) * SAFETY
    h = max(3.0, min(72.0, h))
    return f"{int(h):02d}:{int((h%1)*60):02d}:00"

def load_queue(meta):
    """Ordered, deduplicated on (structure, grade). Order is the PI's: sample, agent tail,
    descriptor tail, remaining claims."""
    def ids(p, col="structure_id"):
        with open(ROOT/p) as fh:
            first = fh.readline()
            if not first.startswith("#"): fh.seek(0)
            return [r[col] for r in csv.DictReader(fh)]
    q, seen = [], set()
    def add(structs, grade, seg):
        for s in structs:
            k = (s, grade)
            if k in seen: continue
            seen.add(k); q.append(dict(structure_id=s, grade=grade, segment=seg))
    add(ids("analysis/fig4_sample_20260903.csv"), "floor", "sample")
    add(json.loads((ROOT/"analysis/fig4_agent_tail.json").read_text()), "claim", "agent_tail")
    add(ids("analysis/fig4_descriptor_tail.csv"), "floor", "descriptor_tail")
    add(json.loads((ROOT/"analysis/fig4_claims_rest.json").read_text()), "claim", "claims")
    for r in q:
        r["nsim"] = meta.get(r["structure_id"], {}).get("nsim", MEDIAN_NSIM)
    return q

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--test", action="store_true", help="build and submit exactly ONE job, then stop")
    a.add_argument("--window", type=int, default=600)
    a.add_argument("--dry-run", action="store_true")
    a = a.parse_args()
    meta = json.loads((ROOT/"screen/screen_meta_12499.json").read_text())
    q = load_queue(meta)
    print(f"queue: {len(q)} runs (deduplicated on structure+grade)")
    stage = {"floor": "stage1", "claim": "stage0"}
    jd = ROOT/"screen/jobs/fig4"; jd.mkdir(parents=True, exist_ok=True)
    made = []
    for i, r in enumerate(q if not a.test else q[:1]):
        for leg in (("p05",) if a.test else ("p05", "p65")):
            rel = f'{stage[r["grade"]]}/{r["structure_id"]}/{leg}'
            name = f'f4_{"t" if a.test else i}_{leg}'
            (jd/f"{name}.pbs").write_text(TPL.format(
                name=name, group=GROUPS[i % len(GROUPS)], wt=walltime(r["nsim"], r["grade"]),
                root=SCREEN, rel=rel))
            made.append((name, rel, r["segment"], r["grade"]))
        if a.test: break
    print(f"wrote {len(made)} job script(s) to screen/jobs/fig4/")
    for n, rel, seg, g in made: print(f"  {n}  {rel}  [{seg}/{g}]")
    if a.dry_run:
        print("dry-run: nothing transferred, nothing submitted"); return 0
    sh(["rsync", "-a", f"{jd}/", f"{REMOTE}:{SCREEN}/jobs/fig4/"])
    out = remote(f'mkdir -p {SCREEN}/logs {SCREEN}/runs\ncd {SCREEN}/jobs/fig4\n'
                 + "".join(f'printf "%s " "{n}.pbs"; {QAS} "{n}.pbs" 2>&1 | tr "\\n" " "; echo\n'
                           for n, _, _, _ in made))
    print(out.stdout.strip() or out.stderr.strip())
    return 0

if __name__ == "__main__":
    sys.exit(main())
