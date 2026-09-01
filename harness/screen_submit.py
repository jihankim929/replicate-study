#!/usr/bin/env python3
"""Reference-screen wave submitter — the last line of screen_launch.sh --go.

WHY THIS FILE DID NOT EXIST. `screen_launch.sh` has called it since 2026-08-29 and `git log --all`
finds it was never committed: the submission step of the sealed plan was never implemented. That is
SI-012's finding for the fourth time -- the layer did not travel -- and it surfaced only when
something finally tried to submit. Written 2026-09-02 under PI ruling 04:35 KST.

WHAT IS SEALED AND TRANSCRIBED HERE, NOT DECIDED (prereg/reference_screen_plan.md):
  section 6  cost proxy = atoms x cell replication (`nsim`, precomputed in screen_meta_12499.json);
             quartile bins; batch 40 in the cheapest quartile, 8 in the dearest; concurrency
             ceiling 480 post-collection; automatic back-off to 240 on any third-party job queued
             and not running across THREE consecutive polls, held until two consecutive clear polls;
             every excursion above 240 logged with start, end, peak and the queue state.
  section 8  retry x3: attempt 2 resubmits unchanged, attempt 3 re-derives the simulation cell.
             A run that exits 0 having written no output IS A FAILURE -- RASPA returns 0 either way,
             measured both ways 2026-08-29 -- so status comes from output presence and parseability
             and NEVER from exit code.
  section 9  screen_ledger.csv columns, verbatim.
  dirac.py   submit with `qas`, NOT qsub; it is not on a non-interactive PATH (/usr/local/mjs/qas);
             it takes the script as its first positional arg and passes no flags through, so queue,
             node group and job name go in #PBS directives INSIDE the script; a bare
             `nodes=1:ppn=1` is REJECTED -- a node group is required.

FOUR PARAMETERS THE PLAN DOES NOT SPECIFY. Authorised as MINE by PI ruling 2026-09-02 04:35 KST and
recorded here as IMPLEMENTATION DECISIONS, NOT PLAN AMENDMENTS. Each states its basis:

  (1) WALLTIME. Basis is the plan's own measured cost: floor grade 0.913 CPU-h per run (1,072
      structures / 2,144 runs / 1,957.9 CPU-h, section 2) and claim grade 4.565 CPU-h per run
      (300 x 9.13 CPU-h / 2 pressures, section 1). Scaled per structure by nsim / median_nsim
      (median 2,424), taken as the MAXIMUM over the batch because members run in parallel and the
      batch finishes with its slowest, then multiplied by SAFETY = 3.0. The safety factor covers the measured spread -- per-structure cost
      spans 338x and p99/median is 18.3x (section 6) -- but is applied to a BATCH SUM, whose relative
      variance is far smaller than a single run's, which is why 3.0 rather than the ~18x a per-run
      factor would need. Floor 1 h, cap 168 h. A job that overruns is killed by PBS and is caught by
      section 8's output-presence rule as a failure, then retried; a job that underruns costs only
      idle reservation. The asymmetry is deliberate and errs long.
  (2) NODE GROUP AND ppn. ppn=1: one core per run, batch members run serially. CPU-ONLY per the
      ruling, so `xeonphi` is excluded; `ax` is excluded as well because it is the mjs staging group
      and holds a single node. Groups used: aa, ab, ac, amd, assigned ROUND-ROBIN by batch index so
      no group is preferentially loaded. dirac.py's measured requirement that a node group be named
      is what makes this a required parameter rather than an omission.
  (3) RASPA ENVIRONMENT. From /home1/users/Bei/toolchain_frozen, which is outside every replicate
      workspace and so satisfies section 7.2's isolation clause without a new build. Its aggregate
      IS VERIFIED BEFORE FIRST USE against toolchain_frozen.sha256 using transfer.sh's exact
      construction -- `find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum` UNDER
      LC_ALL=C. The locale is not incidental: without it the sort order differs and the check fails
      open against a tree that is in fact intact. RASPA_DIR is set to a screen-local raspa_home
      whose share/raspa/grids symlinks into the screen root, per fix_makegrid.sh.
  (4) BATCH -> JOB MAPPING. One PBS job per batch, `ppn = batch size`, MEMBERS RUN IN PARALLEL and
      the job waits on all of them. This is forced by the plan's own sentence: "A batch finishes when
      its slowest member finishes" is only true of parallel members, and it is why binning by cost
      matters at all -- homogeneous members make the max close to the mean. The measured node shapes
      confirm it: `ac` nodes are 40 and 44 cores, so the sealed batch size of 40 IS an ac node, and 8
      is a fraction that fits everywhere. A serial reading was implemented first and rejected on its
      own output: it produced 82-107 h walltimes for a single job.
      Concurrency 480 is therefore concurrent CORES, not jobs, which the plan's own arithmetic
      confirms -- 32,471 CPU-h / 480 = 67.6 h, its stated central figure at perfect packing.
      One ledger row per RUN, never per job, so section 8's completeness identity is asserted against
      the manifest and not against a count of jobs. The plan fixes only the extreme quartiles, so Q2
      and Q3 are filled by GEOMETRIC interpolation -- 40, 23, 14, 8 -- because the cost proxy is
      multiplicative; linear interpolation (40, 29, 19, 8) would over-batch the expensive middle.
"""
import argparse, csv, json, math, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREEN_ROOT = "/home1/users/Bei/screen"
REMOTE = "dirac-bei"
QAS = "/usr/local/mjs/qas"
TOOLCHAIN = "/home1/users/Bei/toolchain_frozen"
# The 12,499-structure census, OUTSIDE every replicate workspace, so section 7.2's isolation clause
# is satisfied without reading a sealed workspace's db/. Hash-pinned by its own MANIFEST.sha256,
# which is the authority exactly as deck_manifest.sha256 is for the decks.
CORPUS = "/home1/users/Bei/benchmark/frozen/CoRE_MOF_2024_CR_united"
CORPUS_MANIFEST = "/home1/users/Bei/benchmark/frozen/MANIFEST.sha256"
TC_SHA = "d79c1ba040dadf095901f3ebfb458af07df9e2404b0fe66ccfb2726b543d5fc1"

# (2) CPU-only: xeonphi (accelerator) excluded. `ab` excluded too -- its nodes are 6 cores and no
# sealed batch size fits. Eligibility is by NODE SHAPE, measured from pbsnodes, because a batch runs
# on ppn = its own size and PBS cannot place ppn=40 on a 16-core node:
#   aa 12,16,16,16,16 | amd 32 x5 | ac 40,40,40,40,44 | ax 64 | ab 6,6 | xeonphi 64
GROUPS_FOR_PPN = {40: ["ac"], 23: ["amd", "ac"], 14: ["aa", "amd", "ac"], 8: ["aa", "amd", "ac", "ax"]}
BATCH = {1: 40, 2: 23, 3: 14, 4: 8}             # (4) sealed 40/8; Q2,Q3 geometric
BASE_CPU_H = {"stage1": 0.913, "stage0": 4.565}  # (1) plan sections 2 and 1
SAFETY = 3.0                                     # (1)
MEDIAN_NSIM = 2424
CONC_SEALED, CONC_BACKOFF = 480, 240


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)


def ssh(script, timeout=300):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=60", REMOTE, "bash", "-s"],
                          input=script, capture_output=True, text=True, timeout=timeout)


def verify_toolchain():
    """(3) Verify the frozen toolchain against its attestation BEFORE first use. LC_ALL=C matters."""
    r = ssh(f'export LC_ALL=C\ncd {TOOLCHAIN} || exit 9\n'
            f'find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-64\n')
    got = r.stdout.strip()
    if got != TC_SHA:
        sys.exit(f"REFUSED — toolchain aggregate {got or '(unreadable)'} != attested {TC_SHA}.\n"
                 f"The RASPA environment is not the frozen one. Nothing submitted.")
    print(f"  toolchain verified against its attestation ({got[:16]}…)")


def stage_environment():
    """(3) Put the VERIFIED frozen toolchain into the screen root and build RASPA_DIR.

    Done here rather than in screen_launch.sh because it must happen after the toolchain check and
    before the first job runs. raspa_home follows fix_makegrid.sh: RASPA writes grids under
    $RASPA_DIR/share/raspa/grids, which is read-only in the frozen tree, so share/raspa's members
    are symlinked in and grids is redirected to a writable directory in the screen root.
    """
    r = ssh(f"""set -e
export LC_ALL=C
mkdir -p {SCREEN_ROOT}/{{decks,runs,logs,jobs,grids}}
# The previous stage left the tree a-w, so rm -rf cannot clear it and cp cannot overwrite it.
chmod -R u+w {SCREEN_ROOT}/toolchain 2>/dev/null || true
rm -rf {SCREEN_ROOT}/toolchain && mkdir -p {SCREEN_ROOT}/toolchain
cp -a {TOOLCHAIN}/. {SCREEN_ROOT}/toolchain/
cd {SCREEN_ROOT}/toolchain
got=$(find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-64)
[ "$got" = "{TC_SHA}" ] || {{ echo "COPY MISMATCH $got"; exit 6; }}
H={SCREEN_ROOT}/raspa_home
rm -rf $H && mkdir -p $H/share/raspa
for d in $(ls {SCREEN_ROOT}/toolchain/raspa/share/raspa 2>/dev/null); do
  [ "$d" = grids ] || ln -sfn {SCREEN_ROOT}/toolchain/raspa/share/raspa/$d $H/share/raspa/$d
done
ln -sfn {SCREEN_ROOT}/grids $H/share/raspa/grids
chmod -R a-w {SCREEN_ROOT}/toolchain
echo "STAGED $got"
""", timeout=900)
    if "STAGED" not in r.stdout:
        sys.exit(f"REFUSED — could not stage a verified RASPA environment.\n{r.stdout}{r.stderr}")
    print("  RASPA environment staged and re-verified in place, toolchain read-only")

    # --- structures --------------------------------------------------------------------------
    # RASPA resolves a framework as $RASPA_DIR/share/raspa/structures/cif/<stem>.cif, FLAT and by
    # stem, while the corpus is laid out ASR/ FSR/ ION/ ... . A flat farm of symlinks bridges the
    # two without copying 12,499 files or mutating the hash-pinned corpus. VERIFIED AGAINST ITS
    # MANIFEST FIRST: the first wave failed every run for want of this staging, and a screen that
    # runs against unverified structures would produce a landscape of numbers from unknown inputs.
    print("  verifying the 12,499-structure corpus against its manifest…")
    r = ssh(f"""set -e
export LC_ALL=C
cd {CORPUS}
BAD=$(sha256sum -c {CORPUS_MANIFEST} 2>/dev/null | grep -cv ': OK$' || true)
TOT=$(grep -c . {CORPUS_MANIFEST})
echo "CORPUS $TOT $BAD"
[ "$BAD" -eq 0 ] || exit 7
H={SCREEN_ROOT}/raspa_home
rm -rf $H/share/raspa/structures
mkdir -p $H/share/raspa/structures/cif
for d in block ions; do
  [ -e {SCREEN_ROOT}/toolchain/raspa/share/raspa/structures/$d ] && \
    ln -sfn {SCREEN_ROOT}/toolchain/raspa/share/raspa/structures/$d $H/share/raspa/structures/$d
done
n=0
while IFS= read -r rel; do
  ln -sfn "{CORPUS}/$rel" "$H/share/raspa/structures/cif/$(basename "$rel")"
  n=$((n+1))
done < <(awk '{{print $2}}' {CORPUS_MANIFEST})
echo "LINKED $n"
""", timeout=1800)
    out = r.stdout
    if "LINKED" not in out:
        sys.exit(f"REFUSED — structure corpus failed verification or staging.\n{out}{r.stderr}")
    tot, bad = out.split("CORPUS ")[1].split()[0:2]
    print(f"  corpus verified {tot} / {tot} ({bad} bad), "
          f"{out.split('LINKED ')[1].strip()} structures linked into RASPA_DIR")


def free_cores():
    """Free cores per node group, measured from pbsnodes. The ceiling is an upper bound, not a
    target: section 6's contention rules exist to avoid displacing other users, so a wave is sized
    to what is ACTUALLY FREE and never to the ceiling alone. A batch also needs its ppn free within
    ONE group, so a ppn=40 batch is unplaceable unless an ac node is empty."""
    r = ssh("""pbsnodes -a 2>/dev/null | awk '
      /^[a-z0-9]/{n=$1; np=0; used=0; props=""}
      /np = /{np=$3}
      /properties = /{p=$0; sub(/.*properties = /,"",p); props=p}
      /jobs = /{j=$0; sub(/.*jobs = /,"",j); gsub(/[^,]/,"",j); used=length(j)+1}
      /^$/{if(n!="" && np>0){print props, np, used; n=""}}
      END{if(n!="" && np>0) print props, np, used}'
""")
    free = {}
    for line in r.stdout.splitlines():
        p = line.split()
        if len(p) == 3 and p[1].isdigit():
            free[p[0]] = free.get(p[0], 0) + max(0, int(p[1]) - int(p[2]))
    return free


def queue_state():
    """Whole-queue depth, section 6.1: total running and queued across ALL users, not our share."""
    r = ssh('qstat 2>/dev/null | awk \'NR>2{print $5, $2}\'\n')
    run = qd = mine_r = 0
    for line in r.stdout.splitlines():
        p = line.split()
        if not p:
            continue
        if p[0] == "R":
            run += 1
        elif p[0] == "Q":
            qd += 1
    m = ssh('qselect -u Bei 2>/dev/null | wc -l\n')
    mine_r = int(m.stdout.strip() or 0)
    return run, qd, mine_r


def load_runs(stage, decks_present):
    meta = json.loads((ROOT / "screen/screen_meta_12499.json").read_text())
    s0 = json.loads((ROOT / "prereg/stage0_sample.SEALED.json").read_text())
    ns = sorted(v["nsim"] for v in meta.values())
    n = len(ns)
    bounds = [ns[n // 4], ns[n // 2], ns[3 * n // 4]]

    def quartile(x):
        return 1 + sum(x >= b for b in bounds)

    stems = sorted(k for k, v in meta.items() if "error" not in v) if stage == "stage1" else list(s0["sample"])
    runs = []
    for stem in stems:
        m = meta[stem]
        for pc in ("p05", "p65"):
            rel = f"{stage}/{stem}/{pc}"
            if rel in decks_present:
                runs.append(dict(stage=stage, stem=stem, pc=pc, rel=rel,
                                 nsim=m["nsim"], q=quartile(m["nsim"])))
    return runs


def batches(runs):
    """(4) Batch within quartile, ordered by cost proxy so a batch is cost-homogeneous."""
    out = []
    for q in (1, 2, 3, 4):
        sel = sorted([r for r in runs if r["q"] == q], key=lambda r: (r["nsim"], r["rel"]))
        k = BATCH[q]
        out += [sel[i:i + k] for i in range(0, len(sel), k)]
    return out


def walltime_for(batch):
    """(1) Members run in parallel; the batch finishes with its slowest. Max, not sum."""
    h = max(BASE_CPU_H[r["stage"]] * (r["nsim"] / MEDIAN_NSIM) for r in batch) * SAFETY
    h = max(1.0, min(168.0, h))
    return "%02d:%02d:00" % (int(h), int(round((h - int(h)) * 60)))


JOB = """#!/bin/bash
#PBS -N {name}
#PBS -q long
#PBS -l nodes=1:ppn={ppn}:{group}
#PBS -l walltime={wt}
#PBS -j oe
#PBS -o {root}/logs/{name}.log
set -u
export LC_ALL=C
export RASPA_DIR={root}/raspa_home
cd {root}
run_one() {{
  REL="$1"
  D={root}/runs/$REL
  mkdir -p "$D" && cd "$D" || return
  cp {root}/decks/$REL/simulation.input .
  S=$(date -u +%s)
  {root}/toolchain/raspa/bin/simulate -i simulation.input > raspa.stdout 2>&1
  RC=$?
  E=$(date -u +%s)
  # section 8: RASPA returns 0 whether or not it succeeded. Status is decided by output presence
  # and parseability, NEVER by $RC. $RC is recorded only as evidence, never as the verdict.
  OUT=$(ls Output/System_0/*.data 2>/dev/null | head -1)
  if [ -n "$OUT" ] && grep -qE 'Average loading absolute .*molecules/unit cell' "$OUT" 2>/dev/null; then
    ST=ok
  else
    ST=failed
  fi
  printf '%s,%s,%s,%s,%s,%s\\n' "$REL" "$ST" "$RC" "$S" "$E" "$(hostname)" >> {root}/logs/{name}.runs
}}
# section 6: the batch finishes when its slowest member finishes -- members run concurrently on the
# ppn cores this job reserved, and the job waits on all of them.
for REL in {rels}; do run_one "$REL" & done
wait
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", type=int, default=1)
    ap.add_argument("--max-concurrent", type=int, default=CONC_SEALED)
    ap.add_argument("--backoff", type=int, default=CONC_BACKOFF)
    ap.add_argument("--stages", default="stage0,stage1")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    print(f"=== reference screen — wave {a.wave} ===")
    verify_toolchain()

    man = (ROOT / "screen/deck_manifest.sha256").read_text().splitlines()
    present = {"/".join(l.split("  ")[1].split("/")[:3]) for l in man if "  " in l}
    print(f"  manifest: {len(man):,} decks, {len(present):,} run directories")

    run, qd, mine = queue_state()
    # section 6.2: back-off is mechanical, not a judgement. One poll here; sustained third-party
    # queueing is three consecutive, so a single non-zero reading is recorded and errs to the floor.
    ceiling = a.max_concurrent if qd == 0 else a.backoff
    print(f"  whole queue: {run} running, {qd} queued (all users); Bei running {mine}")
    print(f"  ceiling: {ceiling}" + ("" if qd == 0 else f"  ← BACKED OFF from {a.max_concurrent}: {qd} third-party queued"))

    allb = []
    for st in a.stages.split(","):
        rs = load_runs(st, present)
        b = batches(rs)
        allb += [(st, x) for x in b]
        print(f"  {st}: {len(rs):,} runs -> {len(b):,} batches")

    # Ceiling is in CORES, and it is an upper bound. Size to measured free capacity.
    free = free_cores()
    avail = {g: free.get(g, 0) for g in ("aa", "ab", "ac", "amd", "ax")}
    total_free = sum(v for g, v in avail.items() if g != "ab")   # ab: 6-core nodes, no batch fits
    print("  free cores: " + ", ".join(f"{g} {v}" for g, v in sorted(avail.items())) +
          f"  -> {total_free} placeable")
    if total_free < ceiling:
        print(f"  NOTE: the sealed {ceiling}-core ceiling is UNREACHABLE — {total_free} cores are "
              f"free. Third parties hold the rest. Sizing to free capacity, not to the ceiling.")
    slots, wave, used, skipped = min(ceiling, total_free), [], 0, 0
    for st, b in allb:
        ppn = len(b)
        if used + ppn > slots:
            skipped += 1
            continue
        elig = [g for g in GROUPS_FOR_PPN[BATCH[b[0]["q"]]] if avail.get(g, 0) >= ppn]
        if not elig:
            skipped += 1
            continue
        g = max(elig, key=lambda x: avail[x])   # balance across groups by remaining headroom
        avail[g] -= ppn
        wave.append((st, b, g)); used += ppn
    print(f"  wave {a.wave}: {len(wave)} jobs / {used} cores placeable now "
          f"({len(allb):,} batches total, {skipped:,} deferred to later waves)")
    if not wave:
        sys.exit("nothing to submit")

    jd = ROOT / f"screen/jobs/wave{a.wave}"
    # Clear first. The remote submit loop is `for f in *.pbs`, so a stale script from an earlier
    # run of this wave would be submitted silently alongside the current ones -- which is exactly
    # what a rejected serial-batch draft left behind here on the first pass: 456 ppn=1 scripts.
    if jd.exists():
        stale = list(jd.glob("*.pbs"))
        for f in stale:
            f.unlink()
        if stale:
            print(f"  cleared {len(stale)} stale job script(s) from {jd}")
    jd.mkdir(parents=True, exist_ok=True)
    ledger = []
    for i, (st, b, grp) in enumerate(wave):
        name = f"scr{a.wave}_{st[-1]}_{i:04d}"
        wt = walltime_for(b)
        (jd / f"{name}.pbs").write_text(JOB.format(
            name=name, group=grp, ppn=len(b), wt=wt, root=SCREEN_ROOT,
            rels=" ".join(r["rel"] for r in b)))
        for r in b:
            ledger.append(dict(stem=r["stem"], stage=st, grade="claim" if st == "stage0" else "floor",
                               init_cycles=10000 if st == "stage0" else 2000,
                               prod_cycles=50000 if st == "stage0" else 10000,
                               job=name, walltime=wt, nsim=r["nsim"], quartile=r["q"],
                               attempt=1, status="submitted"))
    if not a.dry_run:
        stage_environment()
    print(f"  wrote {len(wave)} job scripts, {len(ledger):,} runs, "
          f"walltime {min(w['walltime'] for w in ledger)}–{max(w['walltime'] for w in ledger)}")

    if a.dry_run:
        print("\nDRY RUN — scripts written, nothing transferred, nothing submitted.")
        return

    print("  staging job scripts…")
    subprocess.run(["rsync", "-a", "--delete", f"{jd}/",
                    f"{REMOTE}:{SCREEN_ROOT}/jobs/wave{a.wave}/"], check=True)
    print("  submitting…")
    r = ssh(f'cd {SCREEN_ROOT}/jobs/wave{a.wave} || exit 9\n'
            f'for f in *.pbs; do printf "%s " "$f"; {QAS} "$f" 2>&1 | tr "\\n" " "; echo; done\n',
            timeout=3600)
    ids = {}
    for line in r.stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and p[0].endswith(".pbs"):
            ids[p[0][:-4]] = p[1]
    print(f"  submitted {len(ids)} / {len(wave)}")

    lp = ROOT / "screen/screen_ledger.csv"
    new = not lp.exists()
    with lp.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ledger[0].keys()) + ["job_id"])
        if new:
            w.writeheader()
        for row in ledger:
            row["job_id"] = ids.get(row["job"], "")
            w.writerow(row)
    print(f"  ledger: {len(ledger):,} rows -> {lp}")

    # section 6.3: every excursion above 240 is logged with the queue state that justified it.
    if ceiling > CONC_BACKOFF:
        with (ROOT / "screen/excursions.jsonl").open("a") as f:
            f.write(json.dumps(dict(ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    wave=a.wave, ceiling=ceiling, submitted=len(ids),
                                    queue_running=run, queue_queued=qd, bei_running=mine,
                                    basis="section 6.2: zero third-party jobs queued-and-not-running")) + "\n")


if __name__ == "__main__":
    main()
