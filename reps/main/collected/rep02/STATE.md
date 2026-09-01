# STATE - current beliefs and open tasks
_Updated 2026-08-31 04:40 KST. **Deadline 2026-09-06 14:08:17 KST**
(`deadline_kst` in WORKSPACE.json is the only authority; it moved twice - the
4.4704 h fleet pause and 13.9786 h restored for the 2026-08-30/31 harness-fault
outage). ~154 h left. The session was down 13.98 h; the cluster never stopped,
and everything below is reconciled against what landed while it was._

## CAMPAIGN CLOSED — hard stop, 2026-09-01 12:00 KST
**There are no open tasks. This section is a terminal record, not a resumption
brief.** The harness issued `HARD STOP — spend_usd budget at 100%. No further
submissions. A final report in the §7 format remains mandatory: file it from the
state you are in.` `usage.json`: `spend_usd 281.63 / 280.0`, `spend_level
"stop"`. No submission has been made since, and none will be.

**`REPORT.md` is the final filing.** Complete in the fixed §7 order, finished
and relabelled from DRAFT to COMPLETE on 2026-08-31 so that a stop at any moment
would leave a filed report rather than a draft.

**Result.** `2021[Cu][sql]2[ASR]6`, **207.03 ± 0.20 cm³ STP/cm³**, claim grade
(10,000+50,000, three seeds), leading second place by 2.86 against a combined
standard error of 0.14. Ceiling established by exhaustion for the database and
the 3-periodic modification family; **open** for the 2-periodic family the
winner itself belongs to — 145 analogues built and geometrically described, none
measurable, risk bounded by a measured 1-in-429 base rate. Interpenetration
removal: +87.1 mean over 250 paired parents, eight of ten claim-grade places,
2.86 short, because it buys r and gives back vf₀.

**Budgets at the close.** Spend $281.63 / $280 — the only one that ever bound.
Compute 869 CPU-h by the workers' own accounting (757 by the scheduler meter) of
1,610. Deadline 2026-09-06T14:08, never reached, 98 h unused.

**If anyone picks this up later**, the one unresolved question and how to settle
it are in REPORT.md §5 and §6: screen `prep/mod3_live.txt` in the bound order it
is already queued in, starting with `2021[Cu][sql]2[ASR]6__1of2` (vf₀ 0.9095,
bound 238.0) — the analogue of the claimed material itself.


## Where the campaign stands  (2026-08-31 04:40)
**Best measured: `2021[Cu][sql]2[ASR]6`, wc 208.0 cm3/cm3** (N65 244.3,
N5.8 36.3, f_pocket 0.000, ndim 3), screening cycles only. It wins on the low
end, not the high one: its N65 is ordinary for the top group and its N5.8 is
7 units below the field, which is the mechanism the working-capacity definition
rewards.

**The modification route now owns the top of the board.** Three of the top four
and seventeen of the top twenty-five are interpenetration-removal analogues:
2012[In][dia]3[ASR]4__1of2 204.2, 2014[Zn][hms]3[ASR]1__1of2 202.5,
2021[Mn][dia]3[FSR]1__1of2 201.4. The former database leader
2016[Cu][pts]3[ASR]1 (200.3 screening, 199.6 at floor tier) is fifth.
Paired parent-vs-analogue over 250 pairs: **mean +87.1, median +90.5, helped in
241/250**. This is the answer to charter section 2's "by what means", and it is
a large effect, not a marginal one.

**The claim tier is queued and running.** Four finalists within 8.0 of the
leader, 3 seeds x 2 pressures at 10,000+50,000 = 24 tasks, ~62 CPU-h. They were
put at the head of `queue/w2` (not the fresh `queue/w3`, now `queue/w3_retired`)
because the workers already dispatched were inside w2 and the chain is only
re-read between qworker invocations - a queue the chain reaches "eventually" is
not a queue that runs today.

**The database frontier is closed.** At the largest r yet measured over the
whole database (254.0) there are **zero unmeasured structures** whose geometric
bound vf0 x r can reach 208.0. Under the calibrated +20% margin, 512 unmeasured
remain, all queued, 159 CPU-h. If the incumbent rises to 218 the frontier is 26
structures; at 239 it is empty.

**The modification family is now closed by construction, not by prediction.**
The original 664 analogues came from the 697 parents whose *predicted*
post-removal vf0 landed in 0.74-0.88 - a cost heuristic that is also exactly
the objection an adversarial reader raises ("you only modified the ones you
expected to win"). `scripts/mod2.sh` built the remaining 401 all-3-periodic
interpenetrated parents, measured their true geometry into `tables/geom_mod.csv`,
and `scripts/mod2q.py` queued the 315 that the +20% r-margin cannot exclude into
`queue/w4` (~98 CPU-h). Their vf0 runs 0.642-0.913, median 0.710, so most sit
below the window as expected - but **18 are on the bare frontier** and had to be
measured rather than argued away.

**k has moved, and it moved because of a modified structure.** Max r over
everything measured is now **261.7**, held by `2020[Zn][pcu]3[ASR]7__1of2`, not
by any database entry (database max 254.0). Six modified structures exceed the
database r envelope for their own vf0 bin, by up to +6.0%. The ceiling argument
must therefore be stated over the union of the two families, which is what
`mod2q.py` does.


## Budget position - spend is the binding budget, not compute
- **Spend `usage.json` -> $170.17 / $280 = 60.8%.** This is the one that binds
  (charter section 4). The 75% warning is $210. It is driven by session context
  x turn count, not by cluster work: cluster jobs are effectively free against
  it. Therefore **queue generously and turn rarely**.
- Compute: `cpu_h_scheduler` 510.6 / 1610 (31.7%); `scripts/cpuacct.py`, which
  sums the workers own per-task wall times, gives **638.9 / 1610 (39.7%)**. The
  gap is now 1.25x, not the 2x recorded on 2026-08-30. Plan against 638.9.
  ~970 CPU-h remain; committed valuable work is ~190 (claim 62, floor ~30,
  mod2 98), so compute is not the constraint.
- Tokens 6.46M / 32M (20%).
- Charter section 5 Rev 24 (added 2026-08-30): at the 75% spend warning,
  prioritise claim-grade verification of the current best candidate over
  further exploration and keep REPORT.md continuously current. Not yet
  triggered, but the plan below is already ordered that way.


## Operational facts (do not relearn)
- mjs meta-scheduler; per-user core caps shared by ALL sibling replicates
  (ax 32, aa 38, amd 80, ac 102 for user Bei) — confirmed by the harness as a
  single fleet-wide pool with no per-replicate reservation.
- Dispatch order = node class, then that user's usage, then submission time.
  **Never qrm a waiting job** — position is forfeited.
- Payloads can be edited in place while a job waits: mjs runs `qsub <path>` at
  dispatch, so change the work, never the `#PBS` lines.
- **Keep the work queue deep.** Seven workers idled out and exited when the
  queue ran dry. `QW_IDLE_EXIT` in the job script sets the tolerance.
- `qas` lives at `/usr/local/mjs/qas`, not on the non-interactive PATH.
- RASPA `SimulationType MakeGrid` **does** exist and work in this build. The
  2026-08-30 harness notice saying otherwise was retracted 2026-08-31 (it had
  searched the 18 KB driver, not `lib/libraspa`). All GCMC in this campaign is
  nevertheless plain direct summation, now by choice: see REPORT.md section 3.
- **No simulation on the login node.** Charter section 4 and the 2026-08-31
  compliance notice. Everything GCMC goes through `qas`. The only rep02 process
  on bnode0 is `scripts/supervisor.sh`, which sleeps 10 min between ticks and
  runs harvest/collect for seconds. Long *analysis* passes (the access sweep on
  2026-08-30, which ran hours) should have gone through the scheduler too and
  will from now on.
- The login node is heavily loaded; ssh sometimes refuses (exit 255). Retry.
- RASPA_DIR=<ws>/raspa_home, PYTHONPATH=<ws>/pylib.
- Heredocs sent through `ssh dirac-bei '...'` break on any apostrophe in the
  text. Write the file locally and pipe it in instead.
- `pkill` here is **not** procps `pkill` — it is an mjs tool with a different
  argument grammar and it kills nothing. Kill by PID from `ps -u Bei`.
- **Anything long started over ssh must go out under `setsid nohup ... &`
  with stdin from /dev/null.** The agent session is restarted often and a bare
  `ssh 'python3 ...'` dies with it. This has cost two runs. Long analyses also
  write incrementally and skip what is already in their output file, so a kill
  costs minutes rather than the whole job.
- Python is 3.6: no `subprocess.run(capture_output=...)`, no f-strings in
  scripts that must run on the compute nodes.

## Pipeline
`queue/w1/tasks.tsv` (append-only, 1-based line number = task id, claimed via
O_EXCL in `queue/w1/claim/`) -> workers (`scripts/qworker.py`) ->
`queue/w1/res/*.jsonl` -> `scripts/harvest.py` -> `tables/geom.csv` and
`tables/gcmc_raw.csv` -> `scripts/collect.py <out.csv> <in.csv>` ->
`tables/t1_wc.csv` -> `scripts/model.py` -> `tables/pred_all.csv`.
Analyses: `scripts/ceiling.py` (order statistics + GPD), `scripts/bound.py`
(geometric ceiling), `scripts/cpuacct.py` + `scripts/status.sh` (budget/status).
`scripts/reprio.py` re-orders the unclaimed tail by geometric bound.
`scripts/subw.sh <name> <ppn> <prop> [walltime]` submits one more worker.
`scripts/mktasks.py <qdir> <init> <prod> <list> [--seeds N]` appends tasks.
`scripts/bulk.py` measures bulk methane under the pinned protocol.
`scripts/exclude.py` prints the frontier, the margin and the r(vf0) envelope.
`scripts/access.py` separates percolating channels from sealed pockets.

## How work is prioritised — queue/CHAIN
Worker jobs no longer have a queue baked in. `scripts/worker_chain.sh` reads
**`queue/CHAIN`** — one queue directory per line, priority order — on every
pass, so the whole fleet's priorities change by editing that one file, with no
resubmission and no touching of pending payloads. This matters because dispatch
takes up to fifteen hours here and what a job was told to do at submission is
rarely still the most useful thing when it starts.
- The chain is **cycled, not walked once**: work appended to a priority queue
  after a job started is picked up on the next pass.
- The **last** queue in the chain gets a one-hour stint cap (`CHAIN_STINT`),
  because qworker only idles out when it has nothing to claim, so a worker that
  entered the 3,300-task bulk queue would otherwise never look up again.
- qworker reads its idle tolerance from `<qdir>/idle_exit` **in preference to
  the environment**; the chain writes that file to match its intent.
- `scripts/repoint.py` rewrites the payload of every *pending* mjs job onto the
  chain. It replaces only the trailing qworker line and asserts the `#PBS`
  block is byte-identical afterwards. Never touch `#PBS` lines: they were
  parsed at submission and the queue position costs hours to regain.
- `scripts/reprio.py <queue_dir>` re-orders a queue's unclaimed tail:
  confirmation tier (init >= 2000) first, then by descending geometric bound.

### DANGER: a claim file means three different things
A claim file exists for a task that was **done**, one that is **being done**,
and one that was **moved** by `reprio.py` (which claims a task and re-appends
it, so after any re-queue *every live task has a claimed twin earlier in the
file*). Only the file's contents distinguish them — `reprio:<host>` for moved,
`<host>:<pid>` for a worker, a `dedup:`/note string for administratively
blocked.
**Any pass that reasons about which tasks are "already handled" must look only
at unclaimed lines.** A pass that treated claimed twins as coverage blocked all
4,025 open tasks and took both queues to zero open (2026-08-30 13:50). It was
undone exactly because the claim files carried a distinctive message — always
write one. No workers were lost only because `idle_exit` happened to be 1,800 s
at the time; the chain writes 60 s into the priority queue at other times, and
three minutes of empty queue would then have cost the slots.
### DANGER 2: de-duplicate on the MEASUREMENT, not the structure
The key is **(signature, init, prod, seed, pressure)**. Keying on the signature
alone blocked 56 floor-tier tasks because the same structure had a live
screening task — but a 2,000+10,000 run is not a duplicate of a 500+3,000 run,
it is the tier the charter admits while the other is not. That silently
cancelled the confirmation tier the Claim depends on while the leaderboard kept
moving and nothing looked wrong (2026-08-30 13:58).
- Current state: **946 tasks blocked** as genuinely identical measurements,
  under the correct key. The tier-blind version blocked 2,516; the smaller
  number is the real saving.
- Signatures: `tables/dupes.csv` (database), `tables/mod_sig.csv` (modified).
- **Re-check the confirmation list whenever the leaderboard moves.** The list
  was built when the top was all database structures; modified candidates
  climbed into the top eighteen with no floor-tier task queued at all.

Current chain: `queue/w2` (confirmation tier) then `queue/w1` (screening).
`queue/w2` holds the first T2 wave: 12 structures at the charter floor
(2,000+10,000), ~10 CPU-h, being the top of the screening table minus two that
would cost 9 and 8 CPU-h while sitting 12 and 23 units below the leader.
**The two jobs already running were dispatched before this and serve `queue/w1`
directly; only newly dispatched jobs follow the chain.**

## Validated
- Toolchain SHA-256 matches charter section 3; RASPA 2.0.37.
- Geometry field checked against analytic excluded volume: +/-6e-4 in volume
  fraction, cubic and triclinic, periodic wrap correct.
- Screening cycles (500+3000) vs charter floor (2000+10000), now on **17**
  structures and recomputed from `gcmc_raw.csv` keyed on cycle count:
  **delta = +0.200 +/- 1.341, max 3.45.** Screening is unbiased for ranking.
  (Do **not** compute this from `t1_wc.csv` — that table is built from
  `gcmc_raw` including the floor rows, so for a structure measured at both
  settings the "screening" value read back is the floor value. That
  contamination produced eight exact zeros before it was caught.)

## The database is 9,127 distinct structures, not 12,499
`scripts/dupes.py` / `tables/dupes.csv`: 6,616 entries lie in 3,244 duplicate
groups (3,168 pairs, 24 triples, 52 quadruples) — **27.0% redundancy**. The
signature is cell parameters plus a hash of the sorted, wrapped
element-and-coordinate list, so symmetry-related and origin-shifted copies are
missed and this is a **lower bound** on redundancy.
- `ceiling.py` now uses **N = 9,127** and defaults to `tables/t1_uniform.csv`,
  never `t1_wc.csv` (which now carries the tail-enriched wave 2).
- **The tail counts barely move.** Inverse-multiplicity weighting of the
  uniform sample gives essentially the same expected counts on the distinct
  basis as the raw counts on the entry basis (21 vs 21 above 184.9, 42 vs 42
  above 179.9, 190 vs 188 above 169.5), because duplicated structures are not
  concentrated in the tail. What changes is the population statement, not the
  tail estimate.
- **The leaderboard must be de-duplicated when presented.**
  `2015[V][srs]3[ASR]1` and `2015[V][srs]3[FSR]1` are one material, not second
  and third place. The leader `2016[Cu][pts]3[ASR]1` is in a group of one.
- Two of the 52 frontier structures are bit-identical to already-measured ones
  (125.2 and 171.6, both far below the leader), so the live frontier is **50**.

## Screening-tier uncertainty: +/- 0.9 cm3/cm3, from 22 free replicates
22 duplicate groups have more than one independently measured member. Each is a
replicate of the same structure under the same protocol: **within-group spread
mean 0.91, median 0.76, max 2.21**, with examples across the whole range
including 198.8/196.9, 181.8/181.7, 180.4/179.7 at the top. This supersedes the
four-run seed test on a single mid-range structure as the screening-tier
uncertainty basis. **The screening ranking is trustworthy at the top to about
one place and no better** — the current top three are separated by 1.5 units.

## Seeds: mandatory, and why
**RASPA seeds itself from the clock or pid when `RandomSeed` is absent.**
Measured: the same structure, pressure and cycle count returned 175.41 and
174.05 on two unseeded runs, while seeds 1/2/3 gave 175.13/174.90/173.20.
An unseeded result cannot be regenerated from the pinned inputs, which charter
section 3 requires of every reported value.
- `mktasks.py` now always writes an explicit seed (default 1). Every
  confirmation and claim-grade run carries one. [CHARTER-READ] logged.
- The twelve unseeded floor-tier runs are **kept and reported as an extra
  independent sample**, not discarded — the numbers are sound, only their
  provenance is incomplete — and re-queued with seed 1.
- **Uncertainty**: the across-seed spread is the primary estimate (sd ~1.0 at
  500+3000 on the test structure). RASPA's block standard deviations ran
  1.0-4.6 on the same four runs, so they bracket but overestimate it. Report
  the seed spread; quote the block sd alongside.
- Surrogate CV: wc MAE 8.1-8.4, R2 0.94 on 597 training structures.
- In-pore density N65/vf_0 never exceeds liquid methane (max 433 vs 590) —
  an independent physical check the numbers were not fitted to pass.
- Bulk methane reference converged: 54.76 +/- 0.74 at 2000+10000 and
  54.64 +/- 1.27 at 10000+50000, 30 A box.
- **Accessibility sweep complete**: 2,135 structures (bound > 150), 0 failures,
  `tables/access.csv`. The closed-pore artefact is real — 75 of them have no
  percolating channel at all (ndim 0, f_pocket 1.000), and two already-measured
  structures are among them, `2016[Cu][nbo]3[ASR]25` (wc 120.7) and
  `2022[Cu][tbo]3[FSR]10` (wc 116.9), both **disqualified**, kept on the record.
  But **all 230 frontier structures are 3-periodic**, max f_pocket 0.084, p90
  0.0002, and the top twelve measured are 0.000-0.002. The exclusion argument
  is not holed by sealed pores and no leader's number has to be thrown away.

## The modification route (charter section 2: "by what means")
Interpenetration removal, chosen because it is charge-balanced **by
construction** where linker vacancies and functionalisation are not: if the
framework bond graph falls into components sharing no bond, each is a complete
net, so deleting one leaves the rest balanced.
- `scripts/interp.py` finds components and computes each one's **periodicity**
  from cycles in its quotient graph (3 = framework, 2 = sheet, 0 = molecule). A
  component counts as a net only if it carries >15% of the mass, extends in >=2
  directions, and contains a metal. This is what stops the counterion case:
  `2015[Ag][nbo]3[ION]4` has seven components, one 3-periodic net at 66% mass
  and six ions at 5.7% each, and is correctly not flagged.
- Database-wide: **1,817 of 12,499 interpenetrated, 1,112 with all nets
  3-periodic.** `tables/interp.csv`.
- Rationale: wc = vf0 x r with r peaking near vf0 0.78. An interpenetrated
  framework is low in vf0 because a second net fills its pores; removing it
  takes vf0 0.55 -> 0.775 and 0.60 -> 0.80, into the peak.
- `scripts/mkmod.py` built **664 analogues** into `mod/` from the 697 whose
  predicted post-removal vf0 lands in 0.74-0.88. 663 have all nets identical in
  composition. 33 targets were refused for carrying non-net components.
  Provenance in `tables/mod_index.csv`; names are `<parent>__1of<k>`.
- `cifio.find_cif(name)` resolves `mod/` before `db/`, so `geom.py`,
  `mkrun.py` and therefore the whole GCMC path reach modified candidates.
  **Nothing is ever written into `db/`.**
- Only 3-periodic cases are modified. Removing one of two stacked 2-periodic
  sheets is defensible on the same argument but is a larger structural claim,
  and is reported as available and not pursued.
- `tables/geom_mod.csv` gives true vf0; `scripts/predmod.py` ranks by surrogate
  and by envelope bound and queues the union of the two top-120 lists.
- **None of the 664 duplicates a database entry** — every one is genuinely new.
  But 235 duplicate groups cover 486 of them, so there are only 413 distinct
  modified structures; duplicate parents give duplicate children.
  `tables/mod_sig.csv`.
- `scripts/modeval.py` evaluates the route as a **paired** comparison (parent
  with and without its net) and doubles as an independent test of the r(vf0)
  envelope on a family built by a different mechanism. 14 measured so far:
  **0 exceed the envelope**, 0 beat the leader, 0 parents measured yet.
- **All 664 are accessibility-checked** (`tables/access_mod.csv`): 639
  3-periodic, 15 2-periodic, 10 1-periodic, **none sealed, none above 2%
  pocket volume**. `access.py` had `db/` hard-coded and covered none of them
  until 2026-08-30 13:55; it now uses `cifio.find_cif`.
- **Coverage is now complete rather than ranked.** All 413 distinct analogues
  are measured or queued (277 added, 86 CPU-h) and all 186 remaining parents
  are queued (58 CPU-h). Reporting a modification route from a
  surrogate-ranked subset invites the objection that the ranking chose its own
  winners.
- **A modified candidate is currently second overall**:
  `2015[Cd][bto]3[ASR]1__1of2` at 199.2 against the database leader's 200.3 —
  a gap inside the +/- 0.9 screening reproducibility, so they are statistically
  tied. Needs floor-tier, claim-grade and its parent before this can be said in
  the report. Queued.

## Known limitations of the descriptor table
- `lcd` is 2*gmax and the field is capped at GCAP = 6.0 A, so every largest
  cavity diameter above 12 A reads exactly 12.0. Ten of the twelve most porous
  measured structures are at that cap. **Do not lean on lcd above vf0 ~ 0.75**,
  in the surrogate or in the report; vf at the various probe sizes is
  uncensored and carries the information.

## In flight (2026-08-31 04:40)
- 12 jobs, the cap: 5 running (bnode18 set writing `queue/w2`, bnode19 set
  writing `queue/w1`), 7 pending in mjs and all seven verified on the chain by
  `scripts/repoint.py`. w2_1 and w2_4 hit their 24 h walltime within ~5 and ~9 h
  and free two slots for chain workers.
- Chain: `queue/w2` (claim tier, then floor tier) -> `queue/w4` (mod2 frontier)
  -> `queue/w1` (bulk screening, ~1,760 open, low bound, expendable).
- `queue/w2` head is the 24 claim-grade tasks, ordered by geometric bound, so
  2012[In][dia] runs before the leader 2021[Cu][sql]2[ASR]6. All 24 finish in
  ~15 h of wall on one 6-core worker; no reason to hand-reorder.
- **`qworker.py` now reserves `<qdir>/wall_cap` before claiming a task.** It
  used to check only that elapsed time was under MAX_WALL, so a worker with ten
  minutes left would claim a twelve-hour claim-grade task and be killed by PBS
  mid-run - work lost and a claim file left behind looking like coverage.
  `queue/w2/wall_cap` = 28800, `queue/w4/wall_cap` = 16200. Reserve is 0 where
  the file is absent, so screening behaviour is unchanged.


## Throughput: the campaign is not at risk, and here is why
Only ~12 cores are actually turning. The whole open tail is ~3,370 tasks x
559 s = ~520 CPU-h = ~44 h of wall at that rate, which would be tight. But the
open tail no longer has to be finished. After the bound-ordered re-queue, the
tasks that can still change the answer are the ones whose structure has a
geometric bound above the incumbent: **881 tasks (bound > 175), ~137 CPU-h,
~11 h at 12 cores**. Everything below that cannot beat 186.4 unless the bound
itself is wrong, and its only remaining value is sharpening the surrogate and
the extreme-value tail. So the stopping rule is: screen down the bound order
until the bound crosses the best confirmed wc, then move compute to T2/T3.

## Can the exclusion argument actually be closed? Yes, and with room
The frontier is only as good as k = max r, and k can only rise as more is
measured, so what matters is how the cost of closing grows if it does. From
`scripts/exclude.py` (0.31 CPU-h per structure screened, both pressures):

| k | vf0 > | frontier | unmeasured | not queued | CPU-h to close |
|---|---|---|---|---|---|
| 238.9 (now) | 0.780 | 230 | 221 | 0 | 69 |
| 250 | 0.746 | 427 | 404 | 0 | 125 |
| 260 | 0.717 | 649 | 614 | 1 | 190 |
| 270 | 0.690 | 987 | 936 | 4 | 290 |
| 285 | 0.654 | 1502 | 1428 | 140 | 443 |
| 300 | 0.621 | 2327 | 2220 | 733 | 688 |

Closing today's frontier costs **69 CPU-h**. Wave 2 as queued already covers
the frontier out to k ~ 270 with four structures missing. Even k = 300 costs
688 CPU-h against ~1,386 real CPU-h remaining. **The argument is closeable
across any plausible movement in k**, so the sequencing is: measure the current
frontier, see whether k moves, extend only if it does. Do not pre-buy the
k = 300 set — that is 620 CPU-h of insurance against a 26% move.

And a better incumbent makes the argument *easier*, not harder: at W = 195 the
frontier falls to 112 unmeasured, at W = 205 to 30, at W = 215 to 6.

## The confirmation tiers, costed — read this before submitting T2 or T3
Cost scales with cycles: T2 is 3.43x a screening run and T3 is 17.14x, applied
to the measured screening wall time of that same structure (both pressures
summed). The spread across candidates is enormous and it decides the plan:

| rank | structure | wc | T1 (s) | T2 (h) | T3 (h/seed) |
|---|---|---|---|---|---|
| 1 | 2020[Cu][pts]3[ASR]2 | 186.4 | 714 | 0.68 | 3.40 |
| 2 | 2006[Zn][pcu]3[ASR]9 | 184.9 | 773 | 0.74 | 3.68 |
| 3 | 2016[Cu][nbo]3[ASR]33 | 179.9 | 2452 | 2.33 | 11.67 |
| 6 | 2020[Al][fmz]3[ASR]1 | 174.1 | 9597 | 9.14 | **45.70** |
| 14 | 2019[Zr][sqc]3[ASR]1 | 163.1 | 8675 | 8.26 | **41.31** |

- The two leaders are cheap. The expensive outliers are all well below them, so
  claim-grade runs are only owed to genuine contenders and the 45 h cases do
  not arise unless the ranking changes after wave 2.
- **Two limits will bite and both are fixable.** `queue/wall_cap` is 16,200 s
  per (structure, pressure) task, and the workers carry `#PBS walltime=24:00:00`.
  A T3 pressure point on a mid-cost structure runs 5-10 h, on an expensive one
  over 20 h. Queue `long` has **no walltime limit** (`qstat -q` shows `--`, and
  a sibling replicate holds 72 h jobs), so the claim tier gets its own workers
  at `walltime=72:00:00`.
- **The claim tier gets its own queue directory**, `queue/w2`, served only by
  those long-walltime workers. `qworker.py` already takes the queue directory
  as an argument. If T3 tasks sat in `queue/w1` a 24 h screening worker could
  claim a 20 h task and be killed mid-run, losing the work and the slot.
- Repeatability, free: 2020[Cu][tbo]3[ASR]5 was screened twice and returned
  159.1 and 158.3, a 0.8 spread at screening cycles.

## Next actions
1. **Do not poll.** The supervisor (`scripts/supervisor.sh`, setsid on the login
   node) harvests, refills slots and writes `logs/tick.log` every 10 min. Read
   that. Sleep 30-60 min between checks; spend is the binding budget and it is
   paid per turn.
2. When the claim-grade runs land: recompute the leader with its across-seed
   spread, re-run `exclude.py` (k may move again), and write the Claim.
3. When `queue/w4` reports: re-run `mod2q.py` (it re-derives k) and
   `modeval.py`. If a mod2 structure exceeds the envelope, k rises and the
   frontier has to be re-closed - that is the live falsification test.
4. Accessibility for any mod2 structure that enters the top group:
   `scripts/access.py` (it now resolves via `cifio.find_cif`, so `mod/` is
   covered). No finalist may be reported without it.
5. Keep REPORT.md current after every one of the above. The deadline is hard
   and a budget stop ends the campaign the same way.
6. Not pursued and reported as such: removing one of two stacked 2-periodic
   sheets (15 such analogues exist in mod/), and any modification route other
   than interpenetration removal.


## Decisions on record
- Absolute loading (charter section 2); no pore-blocking spheres ([CHARTER-READ] section 3).
- Screening runs below the section 3 floor are ranking devices only; every reported
  number will come from >= 2000+10000 and every Claim number from 10000+50000.
- Work-queue priority is the geometric bound vf_0 x k: a structure whose bound
  falls below the best measured wc cannot win, so it is screened last.
