#!/usr/bin/env python3
"""Figure-4 interim queue submitter. ONE CORE PER JOB, behind a top-up window.

GEOMETRY. One PBS job per run, `ppn=1` with the node group NAMED -- `qas` rejects a bare
`nodes=1:ppn=1`, which is a syntax requirement and was never a verdict on job size (REPORT 019,
measured on job 3475270: placed in under 30 seconds against >24 h unplaced for ppn=23).

WALLTIME. The sealed SAFETY=3.0 was justified on a BATCH SUM, whose relative variance is small.
Per run the spread is 338x and p99/median 18.3x, so a batch-sized factor would kill runs. But
over-requesting ONE core is nearly free, where over-requesting 23 was not -- so this errs long
deliberately: base x (nsim/median) x 12, floor 3 h, cap 72 h.

NODE GROUPS ARE MEASURED, NOT LISTED. `ax` (mjs staging) and `xeonphi` (CPU-only ruling) are
excluded by POLICY and never come back. Every other group is admitted only if pbsnodes reports it
has at least one core on a node that is not `down`/`offline`. This is not a new rule -- it is
implementation decision (2), eligibility by measured node state -- but it is now measured at every
submit instead of written down once. THE REASON: the geometry ruling re-admitted `ab` because its
6-core nodes no longer failed a batch-size test, which is a SHAPE argument and correct. `ab`'s two
nodes are also DOWN, which is a STATE fact the shape argument does not touch. Round-robin over a
static list sent 25% of the first requeue to dead hardware and they sat unplaceable -- the exact
failure this whole geometry change exists to fix. Measuring at submit is what stops that recurring
silently when any other group goes down.

SUBMISSION IS ASYNCHRONOUS AND RETURNS NO JOB ID. `qas.py` prints the qsub FILENAME and then the
mjs daemon's reply; it never prints a PBS id. The daemon queues the job itself and dispatches it to
PBS later, so a submitted job is visible in `qinfo` (mjs) FIRST and in `qstat` (PBS) only after
dispatch. Anything that counts our jobs must count the UNION of both listings or it will
under-count and over-submit. Ids are resolved after the fact by matching the job NAME.

SUBMISSION ORDER IS NOT CONSTRUCTION ORDER, AND MUST NOT BE. PI ruling 2026-09-03 reorders the
remaining queue to (1) sample -> (2b) descriptor tail -> its top-100 promotion -> (2a) agent tail ->
(3) claims. The naive way to apply that -- reordering the list that `load_queue` enumerates -- WOULD
RENAME EVERY JOB IN FLIGHT, because a job's name is `f4_<seq>_<leg>` and `seq` is that enumeration.
The in-flight guard, the resume match and `reconcile()` all key on the name, so a shifted seq would
make ~580 running jobs invisible to the guard and resubmit every one of them as a duplicate: fault
(c) of REPORT 046, systematically. So SEQ IS ASSIGNED IN CANONICAL CONSTRUCTION ORDER AND NEVER
MOVES, and only the iteration order changes, by a stable sort on SUBMIT_ORDER after seq is fixed.
Names are therefore invariant under any future reorder as well.

THE TOP-100 PROMOTION IS DATA-DEPENDENT AND CANNOT BE ENUMERATED YET. Its members are the 100
highest working capacities from (2b)'s floor pass, which has not run. It is a real segment with a
real position in the order, whose membership file is written by `harness/fig4_milestone.py` when
(2b) closes; until that file exists the segment is EMPTY and the queue simply skips it. Its seq
numbers are appended ABOVE the canonical block, so they cannot collide with a name already issued.

WINDOW. Never more than --window jobs in flight (PBS queued+running UNION mjs), topped up as jobs
land. The sealed concurrency rules are unchanged and still apply on top: ceiling 480 RUNNING (at
ppn=1 one job is one core), backed off to 240 when third-party jobs are queued-and-not-running
across THREE consecutive polls, released after TWO consecutive clear polls, every excursion above
240 logged to screen/excursions.jsonl with the queue state that justified it. The sealed submitter
approximated the three-poll rule with a single poll because it ran once; this loop polls, so it
implements the rule as written.
"""
import argparse, collections, csv, itertools, json, os, subprocess, sys, time, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REMOTE = "dirac-bei"
SCREEN = "/home1/users/Bei/screen"
QAS = "/usr/local/mjs/qas"
QINFO = "/usr/local/mjs/qinfo"
POLICY_EXCLUDED = {"ax", "xeonphi"}
BASE_CPU_H = {"floor": 0.913, "claim": 4.565}
CYCLES = {"floor": (2000, 10000), "claim": (10000, 50000)}
MEDIAN_NSIM = 2424
SAFETY = 12.0
CONC_SEALED, CONC_BACKOFF = 480, 240
# Seconds to let the mjs daemon register a tranche before believing a listing of it, and the
# largest tranche to hand it at once. 540 in one go made registration lag by minutes; smaller
# tranches keep the lag inside SETTLE and keep the window count honest between top-ups.
SETTLE, CHUNK = 45, 120

# Claim-grade decks live in stage0 for the 300 pre-registered calibration structures and in stage2
# for the 563 the tail needs that stage0 never had (harness/fig4_gen_claim_decks.py). Floor-grade is
# always stage1, which covers all 12,499. Resolved per structure, never assumed.
STAGE_FLOOR = "stage1"

# Construction order fixes seq (and therefore every job name). Never reorder this list.
CANONICAL_ORDER = ["sample", "agent_tail", "descriptor_tail", "claims"]
# Submission order, PI ruling 2026-09-03. Reorder THIS freely; names do not move.
SUBMIT_ORDER = ["sample", "descriptor_tail", "promotion", "agent_tail", "claims"]

# Amendment 2026-09-04. Two ITERATION-order changes, and nothing else.
#
# (a) WITHIN the descriptor tail, submit in descending helium void fraction, most porous first.
# (b) The descriptor tail no longer waits for the sample to close: its remaining runs are
#     interleaved 1:1 with the sample's remaining runs.
#
# BOTH ARE ITERATION ORDER ONLY. `seq` is assigned in CANONICAL_ORDER above, before any of this
# runs, so every job name is unchanged -- verified 2,932 of 2,932 seq assignments unmoved. The
# alternative, reordering analysis/fig4_descriptor_tail.csv so the enumeration itself changes, is
# the exact fault the 2026-09-03 amendment exists to prevent: it would renumber the tail's 858
# structures and shift `claims` behind them, and any tail job in flight at the time would go
# invisible to the in-flight guard and be resubmitted as a duplicate. The tail has nothing in
# flight today, so that reordering would happen to be survivable today and would silently stop
# being survivable the moment it has. Iteration order is survivable always.
TAIL_ORDER_BY = "vf_he"          # column in analysis/fig4_descriptor_tail.csv, descending
INTERLEAVE = ("sample", "descriptor_tail")   # 1:1 over REMAINING runs, not over the full segments
# Written by harness/fig4_milestone.py when (2b)'s floor pass closes. Absent until then.
PROMOTION_FILE = "analysis/fig4_top100_promotion.json"

# Dedupe against the Stage 0 ppn=1 requeue: this structure's claim-grade pair is produced there, as
# one of the 46 runs orphaned by the two killed ppn=23 jobs. Running it here too would be the same
# duplication the PI's dedupe ruling removed. Its FLOOR pair is a different grade and still runs.
PRODUCED_ELSEWHERE = {("2016[Cu][nbo]3[ASR]23", "claim"): "stage0_requeue"}

# OVERRIDE DECKS. RASPA segfaults in WriteFrameworkDefinitionCIF (framework.c:2420) -- its startup
# dump of the framework, not the simulation -- for some frameworks whose deck says `UnitCells 1 1 1`.
# It kills the run in about one second with rc=139 and writes no output. Measured 2026-09-05: all 25
# failures in logs/fig4.runs are this crash, all 25 are `UnitCells 1 1 1`, no deck with any other
# UnitCells has ever hit it, and NONE of the 25 has ever succeeded on resubmission -- one structure
# is 0 for 7. Resubmitting an affected run unchanged is therefore not a retry, it is the same
# crash again. It does not reproduce on the login node, only on the compute nodes.
#
# `RemoveAtomNumberCodeFromLabel yes` avoids it. That flag decides whether the trailing digits of a
# CIF atom label are kept in the pseudo-atom NAME; it feeds the output writers, not the potential.
# Verified rather than assumed: same structure, same fixed RandomSeed, flag flipped, loadings
# bit-identical (2013[Cu][pto]3[ASR]1 58.1711522247, 2016[Cu][pts]3[ASR]1 42.9164434888, both
# legs of the pair agreeing to every printed digit). It changes what the run is called, not what it
# computes.
#
# THE CORRECTED DECKS ARE A SEPARATE TREE AND `rel` DOES NOT MOVE. screen/decks/ holds decks whose
# hashes are recorded in screen/deck_manifest.sha256, the REFERENCE SCREEN's manifest, which this
# amendment does not own and has not touched. So the fix lives in screen/decks_fig4/ under the SAME
# rel, listed in screen/fig4_override_deck_manifest.sha256, which the amendment does own. Only the
# job script's `cp` source changes. Keeping `rel` fixed is the point: the run directory, the job
# NAME, the `done` set read back from logs/fig4.runs and every analysis path that pairs p05 with p65
# are all keyed on `rel`, and moving a structure to a new stage would have silently split its two
# legs across two directories and dropped it out of the working-capacity ranking.
OVERRIDE_DECKS = "decks_fig4"
OVERRIDE_MANIFEST = "screen/fig4_override_deck_manifest.sha256"

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
cp {root}/{deck_root}/{rel}/simulation.input .
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


def remote(script, timeout=600):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=60", REMOTE,
                           "bash", "-s"], input=script, capture_output=True, text=True,
                          timeout=timeout)


def walltime(nsim, grade):
    h = BASE_CPU_H[grade] * (nsim / MEDIAN_NSIM) * SAFETY
    h = max(3.0, min(72.0, h))
    return f"{int(h):02d}:{int((h%1)*60):02d}:00"


# ---------------------------------------------------------------- cluster state


def cluster_state():
    """pbsnodes + qstat + qinfo in ONE ssh round trip, with the three listings kept separate.

    Returns groups {name: {usable, free}}, whole-queue (run, queued) across all users, and OUR jobs
    as a UNION of the PBS names and the mjs names -- see the module docstring on why the union is
    mandatory rather than defensive.
    """
    r = remote(f"""
echo '#NODES'
pbsnodes -a 2>/dev/null | awk '
  /^[a-z0-9]/{{if(n!=""){{print n,s,np,used,p}}; n=$1; s=""; np=0; used=0; p=""}}
  /state = /{{s=$3}} /np = /{{np=$3}} /properties = /{{p=$3}}
  /jobs = /{{j=$0; gsub(/[^,]/,"",j); used=length(j)+1}}
  END{{if(n!="")print n,s,np,used,p}}'
echo '#QSTAT'
qstat 2>/dev/null | awk 'NR>2{{print $5}}'
echo '#MINE_PBS'
qstat -u Bei 2>/dev/null | awk 'NR>5{{print $4, $10}}'
echo '#MINE_MJS'
{QINFO} 2>/dev/null | awk '$4=="Bei"{{print $3}}'
""")
    sec, cur = {}, None
    for line in r.stdout.splitlines():
        if line.startswith("#"):
            cur = line[1:]; sec[cur] = []
        elif cur:
            sec[cur].append(line)

    groups = {}
    for line in sec.get("NODES", []):
        p = line.split()
        if len(p) != 5:
            continue
        _, state, np_, used, grp = p
        down = ("down" in state) or ("offline" in state)
        g = groups.setdefault(grp, {"usable": 0, "free": 0})
        if not down:
            g["usable"] += int(np_)
            g["free"] += max(0, int(np_) - int(used))

    run = sum(1 for s in sec.get("QSTAT", []) if s.strip() == "R")
    qd = sum(1 for s in sec.get("QSTAT", []) if s.strip() == "Q")

    mine_pbs = {}
    for line in sec.get("MINE_PBS", []):
        p = line.split()
        if len(p) == 2:
            mine_pbs[p[0]] = p[1]
    mine_mjs = set(sec.get("MINE_MJS", []))
    return groups, run, qd, mine_pbs, mine_mjs


def inflight_names():
    """Job NAMES in flight, PBS union mjs. The only trustworthy answer to 'did it submit?'."""
    r = remote(f'{QINFO} 2>/dev/null | awk \'$4=="Bei"{{print $3}}\'\n'
               f'qstat -u Bei 2>/dev/null | awk \'NR>5{{print $4}}\'\n')
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


def eligible_groups(groups):
    return sorted(g for g, v in groups.items() if g not in POLICY_EXCLUDED and v["usable"] > 0)


# ---------------------------------------------------------------- the queue


def tail_void_fractions():
    """Helium void fraction per descriptor-tail structure, from the tail's OWN selection file.

    That file is the record of how the tail was chosen (`vf_he` top 1,000 plus every remaining
    structure over 15 A `d_max`), so its `vf_he` column is the same number the selection used.
    Reading it here rather than re-deriving from analysis/descriptors.csv keeps the ordering key
    and the membership rule on one source: if they ever disagree, the tail is wrong, not the order.
    """
    out = {}
    with open(ROOT / "analysis/fig4_descriptor_tail.csv") as fh:
        first = fh.readline()
        if not first.startswith("#"):
            fh.seek(0)
        for r in csv.DictReader(fh):
            try:
                out[r["structure_id"]] = float(r[TAIL_ORDER_BY])
            except (KeyError, TypeError, ValueError):
                pass
    return out


def interleave(runs, pair=INTERLEAVE):
    """1:1 interleave of two segments' REMAINING runs; every other segment keeps its place.

    Applied AFTER expand(), so the ratio is over runs that actually remain rather than over the
    segments as constructed -- the sample is 54% finished and an interleave computed over its full
    3,000 runs would not be 1:1 over anything that is still going to be submitted.
    """
    a, b = pair
    A = [r for r in runs if r["segment"] == a]
    B = [r for r in runs if r["segment"] == b]
    if not A or not B:
        return runs                      # nothing to interleave against; leave order untouched
    rest = [r for r in runs if r["segment"] not in pair]
    out = []
    for x, y in itertools.zip_longest(A, B):
        if x is not None:
            out.append(x)
        if y is not None:
            out.append(y)
    return out + rest                    # `rest` is every later segment, still in SUBMIT_ORDER


def load_queue(meta):
    """Ordered, deduplicated on (structure, grade). Order is the PI's: sample, agent tail,
    descriptor tail, remaining claims."""
    def ids(p, col="structure_id"):
        with open(ROOT / p) as fh:
            first = fh.readline()
            if not first.startswith("#"):
                fh.seek(0)
            return [r[col] for r in csv.DictReader(fh)]
    q, seen = [], set()

    def add(structs, grade, seg):
        for s in structs:
            k = (s, grade)
            if k in seen:
                continue
            seen.add(k)
            q.append(dict(structure_id=s, grade=grade, segment=seg))
    add(ids("analysis/fig4_sample_20260903.csv"), "floor", "sample")
    add(json.loads((ROOT / "analysis/fig4_agent_tail.json").read_text()), "claim", "agent_tail")
    add(ids("analysis/fig4_descriptor_tail.csv"), "floor", "descriptor_tail")
    add(json.loads((ROOT / "analysis/fig4_claims_rest.json").read_text()), "claim", "claims")
    # A stable global sequence number assigned over the WHOLE queue, so a job's name does not move
    # when --segments selects a subset, NOR when the submission order is changed. Resume matches on
    # it. This enumeration is the canonical construction order and is not the order we submit in.
    stage0 = {p.name for p in (ROOT / "screen/decks/stage0").iterdir() if p.is_dir()}

    def annotate(r, seq):
        r["seq"] = seq
        r["nsim"] = meta.get(r["structure_id"], {}).get("nsim", MEDIAN_NSIM)
        r["stage"] = (STAGE_FLOOR if r["grade"] == "floor"
                      else ("stage0" if r["structure_id"] in stage0 else "stage2"))
        return r

    for i, r in enumerate(q):
        annotate(r, i)
    base = len(q)          # promotion seqs start above every name ever issued

    # The promotion segment, if (2b) has closed and the list has been written.
    pf = ROOT / PROMOTION_FILE
    if pf.exists():
        promo = json.loads(pf.read_text())
        members = promo["structures"] if isinstance(promo, dict) else promo
        for j, s in enumerate(members):
            if (s, "claim") in seen:      # already produced at claim grade elsewhere in the queue
                continue
            seen.add((s, "claim"))
            q.append(annotate(dict(structure_id=s, grade="claim", segment="promotion"), base + j))

    # SUBMISSION order. Stable sort, so order within a segment is untouched EXCEPT the descriptor
    # tail, which carries a within-segment key (descending void fraction, amendment 2026-09-04).
    # This sort runs AFTER seq is fixed above and does not touch it: names are invariant under it.
    vf = tail_void_fractions()
    q.sort(key=lambda r: (SUBMIT_ORDER.index(r["segment"]),
                          -vf.get(r["structure_id"], 0.0)
                          if r["segment"] == "descriptor_tail" else 0))
    return q


def expand(q, segments, done, deck_index, inflight=frozenset()):
    """Queue rows -> individual runs (one per pressure leg), skipping finished and deduped work.

    `inflight` is what makes a RESTART safe. Completion alone is not enough to skip a run: a job
    that is queued or running has neither completed nor failed, and resubmitting it would run the
    same structure twice and bill it twice. A run that WAS submitted, is no longer in flight and
    never wrote an `ok` is deliberately NOT skipped -- that is a run that died, and it belongs back
    in the queue. So the skip rule is completion or presence, never "we sent it once".
    """
    runs, skipped = [], {"done": 0, "in_flight": 0, "produced_elsewhere": 0, "no_deck": 0}
    ovr = override_index()
    for r in q:
        if r["segment"] not in segments:
            continue
        if (r["structure_id"], r["grade"]) in PRODUCED_ELSEWHERE:
            skipped["produced_elsewhere"] += 2
            continue
        for leg in ("p05", "p65"):
            rel = f'{r["stage"]}/{r["structure_id"]}/{leg}'
            if rel not in deck_index:
                skipped["no_deck"] += 1
                continue
            if rel in done:
                skipped["done"] += 1
                continue
            if f'f4_{r["seq"]}_{leg}' in inflight:
                skipped["in_flight"] += 1
                continue
            runs.append(dict(rel=rel, leg=leg, name=f'f4_{r["seq"]}_{leg}',
                             deck_root=OVERRIDE_DECKS if rel in ovr else "decks", **r))
    return runs, skipped


def override_index():
    """rels served from OVERRIDE_DECKS instead of decks/. Empty file, or no file, means none."""
    idx = set()
    p = ROOT / OVERRIDE_MANIFEST
    if p.exists():
        for line in p.read_text().splitlines():
            if line.startswith("#") or "  " not in line:
                continue
            idx.add("/".join(line.split("  ", 1)[1].split("/")[:3]))
    return idx


def deck_index():
    idx = set()
    for man in ("screen/deck_manifest.sha256", "screen/fig4_deck_manifest.sha256"):
        p = ROOT / man
        if p.exists():
            for line in p.read_text().splitlines():
                if "  " in line:
                    idx.add("/".join(line.split("  ", 1)[1].split("/")[:3]))
    return idx


def completed():
    """rels already finished ok, from the remote run log. Anything not `ok` is left to be re-run."""
    r = remote(f'cat {SCREEN}/logs/fig4.runs 2>/dev/null')
    done = set()
    for line in r.stdout.splitlines():
        p = line.split(",")
        if len(p) >= 2 and p[1] == "ok":
            done.add(p[0])
    return done


# ---------------------------------------------------------------- submission


def submit(batch, groups, elig, jd):
    """Write, stage and submit one tranche. Group is chosen by most FREE cores, then round-robin,
    so a group that is merely busy still gets work and a group that is down gets none."""
    order = sorted(elig, key=lambda g: -groups[g]["free"])
    for i, r in enumerate(batch):
        r["group"] = order[i % len(order)]
        (jd / f'{r["name"]}.pbs').write_text(TPL.format(
            name=r["name"], group=r["group"], wt=walltime(r["nsim"], r["grade"]),
            root=SCREEN, rel=r["rel"], deck_root=r.get("deck_root", "decks")))
    subprocess.run(["rsync", "-a", "--delete", f"{jd}/", f"{REMOTE}:{SCREEN}/jobs/fig4/"], check=True)
    remote(f'mkdir -p {SCREEN}/logs {SCREEN}/runs\ncd {SCREEN}/jobs/fig4\n'
           + "".join(f'{QAS} "{r["name"]}.pbs" >/dev/null 2>&1\n' for r in batch), timeout=1800)
    # WHETHER A JOB SUBMITTED IS ANSWERED BY THE LISTING, NEVER BY THE EXIT CODE. `qas` hands the
    # job to the mjs daemon over zmq and returns before the daemon has registered it, so its status
    # is unreliable in BOTH directions. Measured on the first 540-job tranche: 68 reported failure
    # and 44 of those were in fact queued and running. Trusting the exit code would have resubmitted
    # all 44 as duplicates. So: settle, then list, then believe the listing.
    time.sleep(SETTLE)
    live = inflight_names()
    ok = {r["name"] for r in batch if r["name"] in live}
    fail = [r["name"] for r in batch if r["name"] not in live]
    return ok, fail


def ledger_append(rows, path):
    p = ROOT / path
    new = not p.exists()
    cols = ["stem", "stage", "grade", "pressure", "segment", "init_cycles", "prod_cycles",
            "job", "walltime", "nsim", "group", "attempt", "status", "submitted_at"]
    with p.open("a", newline="") as fh:
        if new:
            fh.write("# Figure-4 interim queue ledger. One row per RUN, one run per pressure leg.\n"
                     "# Separate from screen_ledger.csv on purpose: that file is the sealed section 9\n"
                     "# ledger of the reference screen, and these runs belong to the Figure-4\n"
                     "# pre-analysis amendment, not to the sealed screen. `pressure` and `segment`\n"
                     "# are columns here that section 9 does not have -- section 9's column set is\n"
                     "# sealed and its two pressure legs are therefore two identical-looking rows.\n"
                     "# This file is mine, so it records the leg and the segment that produced it.\n")
        w = csv.DictWriter(fh, fieldnames=cols)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def reconcile(q, di):
    """Record in the ledger any f4 job that is in flight but was never written down.

    Needed because the first tranche believed `qas`'s exit code: 44 jobs were queued while
    reporting failure, so they were running with no ledger row. A run with no row is worse than a
    duplicate row -- it spends cluster time that no accounting ever sees. This closes that gap and
    is safe to re-run, since it only ever adds rows for names the listing actually shows.
    """
    live = {n for n in inflight_names() if n.startswith("f4_")}
    have = set()
    lp = ROOT / "screen/fig4_ledger.csv"
    if lp.exists():
        with lp.open() as fh:
            have = {r["job"] for r in csv.DictReader(l for l in fh if not l.startswith("#"))}
    byname = {}
    for r in q:
        for leg in ("p05", "p65"):
            byname[f'f4_{r["seq"]}_{leg}'] = (r, leg)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows, unknown = [], []
    for n in sorted(live - have):
        if n not in byname:
            unknown.append(n); continue
        r, leg = byname[n]
        init, prod = CYCLES[r["grade"]]
        rows.append(dict(stem=r["structure_id"], stage=r["stage"], grade=r["grade"], pressure=leg,
                         segment=r["segment"], init_cycles=init, prod_cycles=prod, job=n,
                         walltime=walltime(r["nsim"], r["grade"]), nsim=r["nsim"], group="",
                         attempt=1, status="submitted_reconciled", submitted_at=now))
    if rows:
        ledger_append(rows, "screen/fig4_ledger.csv")
    print(f"reconcile: {len(live)} f4 in flight, {len(have)} already in ledger, "
          f"+{len(rows)} rows added" + (f", {len(unknown)} UNKNOWN names: {unknown[:5]}" if unknown else ""))
    return len(rows)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--segments", default=",".join(SUBMIT_ORDER),
                   help="comma list of " + ",".join(SUBMIT_ORDER))
    a.add_argument("--window", type=int, default=600)
    a.add_argument("--poll", type=int, default=120)
    a.add_argument("--max-concurrent", type=int, default=CONC_SEALED)
    a.add_argument("--backoff", type=int, default=CONC_BACKOFF)
    a.add_argument("--once", action="store_true", help="one top-up tranche, then exit")
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--reconcile", action="store_true",
                   help="record in-flight jobs missing from the ledger, then exit")
    a = a.parse_args()
    segments = set(a.segments.split(","))

    meta = json.loads((ROOT / "screen/screen_meta_12499.json").read_text())
    q = load_queue(meta)
    di = deck_index()
    if a.reconcile:
        reconcile(q, di); return 0
    done = set() if a.dry_run else completed()
    groups0, _, _, mp0, mm0 = cluster_state()
    inflight0 = set(mp0) | mm0
    runs, skipped = expand(q, segments, done, di, inflight0)
    runs = interleave(runs)
    print(f"queue        : {len(q):,} structure-grade pairs; segments {sorted(segments)}")
    print(f"runs to do   : {len(runs):,}   skipped: {skipped}")
    head = collections.Counter(r["segment"] for r in runs[:200])
    print(f"order        : first 200 runs = " + ", ".join(f"{n} {k}" for k, n in head.most_common()))
    if not runs:
        print("nothing to submit"); return 0

    jd = ROOT / "screen/jobs/fig4"
    jd.mkdir(parents=True, exist_ok=True)
    if a.dry_run:
        groups, mp, mm = groups0, mp0, mm0
        elig = eligible_groups(groups)
        print(f"groups       : " + ", ".join(
            f"{g} usable {v['usable']} free {v['free']}" + ("" if g in elig else " [EXCLUDED]")
            for g, v in sorted(groups.items())))
        print(f"eligible     : {elig}")
        print(f"in flight    : PBS {len(mp)}  mjs {len(mm)}  union {len(set(mp)|mm)}")
        for r in runs[:5]:
            print(f"  {r['name']:>16}  {r['rel']}  {r['segment']}/{r['grade']}  "
                  f"wt={walltime(r['nsim'], r['grade'])}")
        print("DRY RUN - nothing written, transferred or submitted")
        return 0

    pending, submitted, failed = list(runs), 0, []
    hot, clear, ceiling = 0, 0, a.max_concurrent
    while pending:
        groups, run, qd, mine_pbs, mine_mjs = cluster_state()
        elig = eligible_groups(groups)
        if not elig:
            print("no eligible node group has a usable core; waiting"); time.sleep(a.poll); continue
        # sealed section 6.2: three consecutive polls with third-party jobs queued-and-not-running
        # backs off; two consecutive clear polls release it.
        third_q = max(0, qd - sum(1 for s in mine_pbs.values() if s == "Q"))
        if third_q > 0:
            hot += 1; clear = 0
        else:
            clear += 1; hot = 0
        if hot >= 3 and ceiling != a.backoff:
            ceiling = a.backoff
            print(f"  BACKED OFF to {ceiling}: third-party queued-not-running on 3 consecutive polls")
        if clear >= 2 and ceiling != a.max_concurrent:
            ceiling = a.max_concurrent
            print(f"  released to {ceiling}: two consecutive clear polls")

        inflight = set(mine_pbs) | mine_mjs
        mine_run = sum(1 for s in mine_pbs.values() if s == "R")
        room = min(a.window - len(inflight), ceiling - mine_run)
        if room <= 0:
            print(f"  window full: {len(inflight)} in flight (cap {a.window}), "
                  f"{mine_run} running (ceiling {ceiling}); {len(pending):,} left")
            if a.once:
                break
            time.sleep(a.poll); continue

        batch, pending = pending[:min(room, CHUNK)], pending[min(room, CHUNK):]
        ok, fail = submit(batch, groups, elig, jd)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = []
        for r in batch:
            init, prod = CYCLES[r["grade"]]
            rows.append(dict(stem=r["structure_id"], stage=r["stage"], grade=r["grade"],
                             pressure=r["leg"], segment=r["segment"], init_cycles=init,
                             prod_cycles=prod, job=r["name"], walltime=walltime(r["nsim"], r["grade"]),
                             nsim=r["nsim"], group=r["group"], attempt=1,
                             status="submitted" if r["name"] in ok else "not_in_listing",
                             submitted_at=now))
        ledger_append(rows, "screen/fig4_ledger.csv")
        submitted += len(ok); failed += fail
        if fail:
            pending = [r for r in batch if r["name"] in fail] + pending
        print(f"  +{len(ok)} submitted ({submitted:,}/{len(runs):,}); {len(pending):,} left; "
              f"in flight {len(inflight)}; groups {elig}; ceiling {ceiling}")
        if ceiling > CONC_BACKOFF:
            with (ROOT / "screen/excursions.jsonl").open("a") as f:
                f.write(json.dumps({"ts": now, "wave": "fig4", "ceiling": ceiling,
                                    "submitted": len(ok), "queue_running": run, "queue_queued": qd,
                                    "third_party_queued": third_q, "bei_running": mine_run,
                                    "basis": "section 6.2: third-party queued-not-running "
                                             f"{third_q} on this poll, hot streak {hot}"}) + "\n")
        if a.once:
            break
        time.sleep(a.poll)
    print(f"done: {submitted:,} submitted, {len(pending):,} still pending, {len(failed)} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
