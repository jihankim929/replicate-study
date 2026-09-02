#!/usr/bin/env python3
"""Requeue the Stage 0 runs orphaned by the two unplaceable ppn=23 jobs, under ppn=1.

WHAT HAPPENED. `3474520` (`scr1_0_0000`, 23 runs) and `3474522` (`scr1_0_0002`, 23 runs) sat Q for
35 hours with `comment = Not Running: Not enough of the right type of nodes are available`. Both
were qdel'd 2026-09-03 06:08:19Z on the PI's order. `tracejob` returns the deletion line and NO
`Exit_status` and NO `resources_used` for either -- unlike the control job 3474481, which was killed
while RUNNING and still reports cput. So these two consumed NOTHING: there is no cost observation
here at all, not even a censored floor, and NO row is written to censored_observations.csv. A
right_censored row with lower_bound 0 would assert a measurement that was never taken.

THE LEDGER IS NOT EDITED. The 46 attempt-1 rows still read `submitted` and are LEFT THAT WAY. Ruling
(1) is that no ledger entry is ever edited, and section 8 decides status from output presence when
the run is harvested -- these produced no output, so the harvest will write `failed` by its own rule,
which is ruling (1)'s stated governing principle for unfinished-not-faulty runs. Writing `failed`
here by hand would pre-empt section 8 and edit an entry. What I know that the ledger does not yet
say is recorded in `screen/cancelled_runs.csv` instead -- the same separation of concerns that
`censored_observations.csv` already uses: the ledger records what happened to the run, the side
record records what is known about it.

GEOMETRY. One PBS job per run, ppn=1, node group named, round-robin aa/ab/ac/amd -- REPORT 019's
ruling, measured on job 3475270 which placed in under 30 seconds. Walltime by the per-run rule in
fig4_submit (base x nsim/median x 12, floor 3 h, cap 72 h): the sealed SAFETY=3.0 was justified on a
batch SUM whose relative variance is small, and does not transfer to a single run.

The DECK IS UNCHANGED and byte-identical to attempt 1's -- section 8's "attempt 2 resubmits
unchanged" is satisfied. Only the reservation geometry differs, which is implementation decision (4).
"""
import argparse, csv, json, subprocess, sys, datetime, pathlib, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("f4", ROOT / "harness/fig4_submit.py")
f4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f4)

REMOTE, SCREEN, QAS = f4.REMOTE, f4.SCREEN, f4.QAS
DEAD = {"scr1_0_0000": "3474520", "scr1_0_0002": "3474522"}


def orphan_runs():
    out = []
    for job in sorted(DEAD):
        txt = (ROOT / f"screen/jobs/wave1/{job}.pbs").read_text()
        line = [l for l in txt.splitlines() if l.startswith("for REL in ")][0]
        for rel in line[len("for REL in "):].split("; do")[0].split():
            stage, stem, pc = rel.split("/")
            out.append(dict(job=job, jobid=DEAD[job], rel=rel, stage=stage, stem=stem, pc=pc))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    runs = orphan_runs()
    # Node groups are MEASURED, never a static list: `ab` is admitted by the geometry ruling on a
    # SHAPE argument, and its two nodes are DOWN, which is a STATE fact that argument does not
    # touch. A static round-robin sent 12 of these 46 to dead hardware on the first pass.
    groups, _, _, _, _ = f4.cluster_state()
    GROUPS = f4.eligible_groups(groups)
    print(f"eligible node groups (measured): {GROUPS}  "
          + ", ".join(f"{g} usable {v['usable']} free {v['free']}" for g, v in sorted(groups.items())))
    if not GROUPS:
        sys.exit("REFUSING: no node group has a usable core")
    meta = json.loads((ROOT / "screen/screen_meta_12499.json").read_text())
    led = list(csv.DictReader(open(ROOT / "screen/screen_ledger.csv")))
    q1 = [r for r in led if r["job"] in DEAD]
    print(f"orphaned runs: {len(runs)} across {len(DEAD)} killed jobs, "
          f"{len({r['stem'] for r in runs})} distinct structures")
    print(f"attempt-1 ledger rows for those jobs: {len(q1)} (left untouched, status "
          f"{sorted({r['status'] for r in q1})})")
    if len(runs) != len(q1):
        sys.exit(f"REFUSING: {len(runs)} runs in the job scripts but {len(q1)} ledger rows")

    jd = ROOT / "screen/jobs/s0requeue"
    if jd.exists():
        for f in jd.glob("*.pbs"):
            f.unlink()
    jd.mkdir(parents=True, exist_ok=True)
    made = []
    for i, r in enumerate(runs):
        nsim = meta[r["stem"]]["nsim"]
        wt = f4.walltime(nsim, "claim")
        name = f"s0rq_{i:03d}_{r['pc']}"
        # These are reference-screen Stage 0 runs, not Figure-4 queue items, so they record to
        # the screen's own run log. The first 46 went out before this was noticed and write to
        # fig4.runs; they are demultiplexed by rel against fig4_ledger.csv, which lists exactly
        # which rels the Figure-4 queue submitted. Noted rather than papered over.
        (jd / f"{name}.pbs").write_text(f4.TPL.format(
            name=name, group=GROUPS[i % len(GROUPS)], wt=wt, root=SCREEN, rel=r["rel"]
        ).replace("/logs/fig4.runs", "/logs/s0requeue.runs"))
        made.append(dict(name=name, nsim=nsim, wt=wt, **r))
    print(f"wrote {len(made)} job scripts -> screen/jobs/s0requeue/ "
          f"(walltime {min(m['wt'] for m in made)}-{max(m['wt'] for m in made)})")
    if a.dry_run:
        print("DRY RUN - nothing transferred, nothing submitted")
        for m in made[:3]:
            print(f"  {m['name']}  {m['rel']}  nsim={m['nsim']}  wt={m['wt']}")
        return 0

    subprocess.run(["rsync", "-a", "--delete", f"{jd}/", f"{REMOTE}:{SCREEN}/jobs/s0requeue/"],
                   check=True)
    out = f4.remote(f'mkdir -p {SCREEN}/logs {SCREEN}/runs\ncd {SCREEN}/jobs/s0requeue\n'
                    + "".join(f'printf "%s " "{m["name"]}.pbs"; {QAS} "{m["name"]}.pbs" 2>&1 '
                              f'| tr "\\n" " "; echo\n' for m in made))
    ids = {}
    for line in out.stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and p[0].endswith(".pbs"):
            ids[p[0][:-4]] = p[1]
    print(f"submitted {len(ids)} / {len(made)}")
    if len(ids) != len(made):
        print("  NOTE: not all accepted; see stderr below")
        print(out.stdout.strip()[:2000]); print(out.stderr.strip()[:1000])

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # attempt-2 rows, sealed section 9 columns exactly
    lp = ROOT / "screen/screen_ledger.csv"
    cols = list(led[0].keys())
    with lp.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        for m in made:
            w.writerow(dict(stem=m["stem"], stage=m["stage"], grade="claim",
                            init_cycles=10000, prod_cycles=50000, job=m["name"], walltime=m["wt"],
                            nsim=m["nsim"], quartile="", attempt=2, status="submitted",
                            job_id=ids.get(m["name"], "NOT_ACCEPTED")))
    # the side record
    cp = ROOT / "screen/cancelled_runs.csv"
    new = not cp.exists()
    with cp.open("a", newline="") as fh:
        if new:
            fh.write(
                "# CANCELLED RUNS - screen layer. Created 2026-09-03 on the PI's order to kill the\n"
                "# two unplaceable ppn=23 jobs and requeue their runs under ppn=1.\n"
                "# WHY THIS FILE AND NOT A LEDGER EDIT: ruling (1) is that no ledger entry is ever\n"
                "# edited, and section 8 writes a run's status from OUTPUT PRESENCE at harvest. These\n"
                "# runs produced no output because they never started, so the harvest will write\n"
                "# `failed` by its own rule - which is ruling (1)'s stated principle that an\n"
                "# unfinished-not-faulty run still reads `failed` and the correction lives in the\n"
                "# retry record. This IS that retry record. The attempt-1 rows are untouched.\n"
                "# WHY NO censored_observations.csv ROW: `tracejob` returns no Exit_status and no\n"
                "# resources_used for either job. They consumed nothing. A right-censored row needs a\n"
                "# lower bound from observed consumption; there is none, so there is no cost\n"
                "# observation to record - not a zero one, an absent one.\n"
                "run_rel,stem,stage,grade,orig_job,orig_jobid,cancelled_at,reason,cput_consumed,"
                "retry_attempt,retry_job,retry_jobid\n")
        for m in made:
            fh.write(f'{m["rel"]},{m["stem"]},{m["stage"]},claim,{m["job"]},{m["jobid"]},'
                     f'2026-09-03T06:08:19Z,unplaceable_ppn23_qdel_for_ppn1_requeue,none_never_started,'
                     f'2,{m["name"]},{ids.get(m["name"], "NOT_ACCEPTED")}\n')
    print(f"ledger: +{len(made)} attempt-2 rows; cancelled_runs.csv: +{len(made)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
