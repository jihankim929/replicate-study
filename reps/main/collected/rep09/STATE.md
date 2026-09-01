# STATE — rep09

## CAMPAIGN CLOSED — 2026-09-02 01:20 KST

**This campaign is over.** Both charter §4 hard budget stops have fired (spend
$397.93 / $280 = 142%, 2026-09-01 17:30 KST; tokens 36.48 M / 32 M = 114%,
2026-09-01 22:30 KST). Under §5 that ends the campaign in place of the deadline
T = 2026-09-06T00:09:53+09:00, which was never reached. The mandatory §7 final
report is **filed** at `REPORT.md`, status FINAL.

**Nothing further is to be submitted, run, or queued.** All three rep09 daemons
(`bin/autopilot.sh`, `bin/login_driver.sh`, `bin/tick.sh`) have been stopped and
`logs/STOP_LOGIN` is in place; the twelve remaining cluster jobs (eight in PBS, plus four the mjs staging queue promoted after those cleared) have been
removed. Daemons belonging to rep04 and rep06 run under the same UNIX user and
are **not** mine — check `/proc/<pid>/cwd` before touching any process.

**Final result.** `2021[Cu][sql]2` (database ids 10995 and 10985, byte-identical
inputs under the chargeless protocol): working capacity **207.11 ± 0.43
cm³ STP/cm³**, from N(65 bar) = 243.939 and N(5.8 bar) = 36.825, claim-grade
10,000 + 50,000 cycles, three independent 65-bar runs and two 5.8-bar runs.
Runner-up 6782 `2016[Cu][pts]3` at 199.86.

**Final coverage.** 8,958 of 9,127 distinct structures screened at 65 bar
(98.1%); 8,437 of 11,454 screened files excluded outright by the rigorous
N65 bound; 3,017 survivors, 2,796 of them measured at both pressures, none
beating the claim. Residual hole: 221 survivors lacking a 5.8-bar point (about
six of them live threats once conditioned on the measured N58-vs-N65 relation)
and 169 unscreened classes.

**Where the numbers come from.** `bin/final_summary.py` (leaderboards and
coverage), `bin/final_ceiling.py` (the two holes), `bin/final_risk.py` (residual
risk). Run them against `tables/*_NN.csv` to reproduce every figure in
`REPORT.md` without reading a single raw output file. The closing LOG.md entry
of 2026-09-02 01:20 KST carries the full account, the correction from 207.25 to
207.11, and the two closing `[CHARTER-READ]` entries.

**2026-09-02 01:16 KST update.** A resume prompt arrived after close. INBOX.md carries nothing new but the half-hourly HARD STOP repetition - no cap lift, no ruling, no escalation answer. The campaign stays closed; see the LOG.md entry of this timestamp for the reasoning and the [CHARTER-READ] on section 8. Spend has risen to $406.38, 145% of cap, on session cost alone. Nothing is running: both queues empty, no rep09 process alive. Do NOT restart the daemons in bin/.

**Everything below this line is the working state as of 2026-08-30 20:00 and is
retained as history. It is superseded by this section and by `REPORT.md`.**

---

# STATE — current beliefs and open tasks

*(Self-sufficient: this file alone must suffice to resume the campaign.)*
*(Last updated 2026-08-30 14:30 KST, launch +18.8 h.)*

## Resume here, in this order

1. `bash bin/daemons.sh up` — restores the two login-node loops (`autopilot`,
   `tick`). They are plain shell loops and nothing else restarts them.
2. `tail -3 logs/progress.tsv` — one line per 10 min: points per wave, CPU-h,
   live slots, best numbers, and an **`alerts`** column. **A non-zero `alerts`
   means jobs are dying, not queueing.** Read `logs/ALERT`, then the named
   `jobs/<chunk>.out`.
3. `bash bin/status.sh` for detail. Do not run ad-hoc scheduler queries.

**A flat point count does not mean a starved queue.** It looked exactly like
one for eight hours on 2026-08-30 while every dispatched job was crashing; see
Errors below. Check `alerts` first, always.

## Fixed facts

- Deadline **T = 2026-09-06T00:09:53+09:00** (launch 2026-08-29T19:41:39 +168 h
  + 4.4704 h of recorded fleet pause). ~156 h remain. **This supersedes the
  19:41 figure that STATE and `bin/status.sh` carried before the pause.**
- Budgets: **1610 CPU-h**, **US$280 spend**, **32M tokens**, **12 live jobs**,
  queue `long`, prefix `rep09_`.
- Usage (`usage.json`, the authoritative meter): **157.4 CPU-h scheduler**,
  **7.04M of 32M tokens at 16:00 on 2026-08-30**, up from 1.42M at 11:44 --
  5.6M in four and a half hours of session activity. **The token and spend
  budgets will bind long before the deadline if that rate continues**, because
  cost is dominated by re-reading accumulated context on every turn and spend
  counts cache reads that the token meter does not. Rationing rule adopted:
  at most one check-in an hour, every command returning a handful of lines,
  and all repetitive work moved into cluster-side loops
  (`autopilot`, `tick`, `login_driver`) that need no turn at all. My own results-side accounting
  (sum of per-point wall) reads 302 CPU-h; the harness meter is lower and is
  the one the cap is judged on. I plan against the conservative (higher) figure.
- Target: max working capacity `N(65 bar) − N(5.8 bar)`, 298 K, **absolute**
  loading, cm³ STP/cm³, over the 12,499 CIFs in `db/`.
- Toolchain verified against all three charter SHA-256 values; RASPA 2.0.37.
  `RASPA_DIR=<ws>/raspa_home`, binary `toolchain/raspa/bin/simulate`.
- Login-node interactive compute is **not** metered (INBOX ruling 2026-08-30).
- `qas` lives at `/usr/local/mjs/qas`; it is not on the non-interactive PATH.

## The cluster, and why it is the binding constraint

`mjs` gates on a per-user core limit per node class **and** a class total over
all users (`molsim_job_scheduler.py:500-506`; limits in
`/usr/local/mjs/config.txt`). All sixteen replicates submit as UNIX user `Bei`,
so the caps are one shared pool: ax 32, aa 38, amd 80, ac 102 = **252 cores for
the whole fleet**. At this stamp `quse` shows Bei at 38/38 aa, 78/80 amd,
102/102 ac, and **0/32 ax** — ax is unreachable because another user is at
64/64 of the ax class total. Dispatch order is (node class, that user usage,
submission time); with one user it is FIFO. Practical consequences:

- Keep all 12 slots occupied at all times; a free slot is throughput lost.
- A queued job position is its submission time. Do not churn submissions.
- Small `ppn` fits through the per-user limit check when the class is nearly
  full (that check `continue`s rather than blocking the class), so a ppn=1/2
  job dispatches when a ppn=8 one cannot.

## Machinery (`bin/`)

`cifutil.py` (CIF parse, cell matrix, unit-cell replication for 12.8 Å) ·
`prep_cif.py` (db CIF → RASPA CIF, labels → `X_`, charges dropped, geometry
untouched) · `gcmc.py` (one point → one CSV row) · `run_batch.py` (pool over a
task file; idempotent, skips points already ok in the output CSV) ·
`mkjobs.py` (chunks + PBS, resumable) · `remaining.py` · `census.sh` (live
rep09 jobs: mjs queue union `qstat -f` names) · `autopilot.sh` (submits from
`jobs/autopilot.plan`, capped at 12 live; **running as pid 2865800**, survives
session loss) · `aggregate.py` · `cal_report.py` (calibration analysis →
`tables/cal_wc.csv`) · `rank.py` · `select.py` · `modify.py`
(defunctionalisation) · `geom.py` (set aside, see Belief 1) ·
`status.sh` (**use this, not ad-hoc queries**) · `tick.sh` (one line of state
to `logs/progress.tsv` every 10 min, including the `alerts` column) ·
`daemons.sh` (report, and with `up` restore, the two loops) ·
`test_no_shadow.py` (asserts no `bin/*.py` shadows a stdlib module; the
autopilot preflights it and refuses to submit on failure) ·
`test_neighbours.py` (KD-tree bond perception == the original routine) ·
`survey_mod.py` · `mkmods.py` · `family.py`.

## Beliefs

1. **No geometric proxy screen.** `geom.py` matches brute force and is still
   useless: structure 2778, ρ = 2.20 g/cm³, has hard-sphere accessible fraction
   0.0003 for a methane probe and still loads to 131 cm³/cm³ at −2585 K per
   molecule. A σ-contact filter would preferentially discard ultramicroporous
   winners.
2. **N(65 bar) rigorously upper-bounds working capacity** (N(5.8 bar) ≥ 0), so
   the 65-bar screen *excludes* rather than merely deprioritises. This is the
   backbone of the ceiling argument: an exhaustive 65-bar screen plus a
   calibrated margin turns "I did not test everything" into "everything I did
   not test cannot beat the winner".
3. **The screen's discrepancy from the floor protocol is noise, not bias.**
   45 structures (one loads zero) carry both the 200+500 screen and the
   2,000+10,000 floor at 65 bar: floor - screen = **+2.25 +- 3.78 cm3/cm3**,
   and in units of the screen's own reported `err_v` the gap runs -0.62 to
   **+2.53 sigma** (p50 +0.33, p90 +1.29). The -18.29% that once fixed the
   margin belongs to a structure loading 46 cm3/cm3 with err_v = 17.2, i.e.
   +0.60 sigma. Seed-pair scatter at screen settings: mean 2.23, max 5.99.
   **Exclusion rule in force:**
   **N65_true <= min(1.25 x N65_screen, N65_screen + 6*err_v)** - both branches
   cover 45/45 so their minimum does too, verified `covers 45, fails 0`.
   Exclude a structure only when that bound falls below WC*. Survivors over the
   screened set: 2,024 at WC* = 197.6, 1,067 at 230, 798 at 240; scale by 1.83
   for the full database. `bin/margin.py` and `bin/frontier.py` regenerate it;
   reasoning in LOG.md at 13:30.
   Residual risk, named: a badly under-equilibrated structure can report a
   small `err_v` around a wrong mean, and no multiple of it would catch that.

3b. **The screening working capacity ranks candidates almost perfectly, and
   this is the calibration Tier 3 rests on.** 46 structures now carry all four
   points (screen and floor, at both pressures). floor WC - screening WC =
   **+1.43 +- 3.53** cm3/cm3, max +1.61 sigma of the screening WC's own error,
   and **Pearson(screening WC, floor WC) = +0.9973**. The floor top ten and the
   screening top ten are the *same ten structures*; the largest rank
   displacement over all 46 is five places and it happens at ranks 36-41.
   Screening errors at the two pressures are correlated -- same
   under-converged sampling of the same framework -- so they cancel in the
   difference instead of adding.
   **Tier 2 -> Tier 3 bound: WC_floor <= WC_screen + 5*sigma_screen**
   (46/46 covered already at 4 sigma). A multiplicative bound is the wrong
   shape for a difference and covers only 42/46; the multiplicative branch
   belongs on N65, not on WC. `bin/wcbias.py` regenerates this.

4. **N65 predicts WC well enough to rank, not well enough to decide.** Over
   the same 46, WC/N65 has mean 0.388, sd 0.191, range 0.000 … 0.850, yet
   Pearson(N65_screen, WC_floor) = 0.843 and Pearson(N65_floor, WC_floor)
   = 0.836. The correlation survives the seven-fold spread in the ratio
   because **the ratio itself rises with N65**: Pearson(N65, ratio) = +0.597.
   There is no adverse trade-off between uptake and released fraction in this
   database, so the best working capacities are expected near the top of the
   N65 distribution rather than in its middle. Two corollaries: the
   density-ordered screen is looking in the right place, and N5.8 carries
   essentially no standalone information (Pearson(N5.8, WC) = +0.008).
   Both pressures are still needed on every surviving candidate — the residual
   scatter around a 0.84 correlation is tens of cm³/cm³ — but the earlier
   claim that ranking on N65 "would have picked the wrong winner" was too
   strong and is corrected here.
   Ratio by density band (n = 46): rho < 0.5 -> 0.850 (n=1), 0.5-1.0 -> 0.622
   (n=6), 1.0-1.5 -> 0.333 (n=26), 1.5-2.0 -> 0.315 (n=10), 2.0-2.5 -> 0.489
   (n=3).
5. **Density is a real but weak prior.** Pearson(ρ, WC_floor) = −0.599 over the
   46. N65 by density band peaks at an interior optimum near ρ = 0.5–0.6, but
   band *maxima* fall far more slowly than band means (268.0, 264.8, 250.6,
   247.9, 227.1 against means 223.5, 211.1, 187.0, 165.3, 148.7), which is the
   empirical case against truncating the screen at any density threshold.
   Tasks still run in ascending-ρ order so partial completion covers the
   promising end.
6. **Energy grids are unavailable** — confirmed by Bei as an infrastructure
   fact: the provided binary contains no MakeGrid code path. Not a usage error,
   will not be fixed this campaign. Screening runs without them.
7. Screen cost falls steeply with density (292 s per point at ρ = 0.5–0.7 down
   to 117 s at 1.1–1.2) and the database median is ρ = 1.255, so the expensive
   part of the screen is the part already done. Whole-database Tier 1
   projection: **285–447 CPU-h**.
8. **Defunctionalisation raises working capacity, by removing binding sites
   rather than by adding volume.** Four source/product pairs at screen
   settings on both pressures: dWC = +0.5, +16.3, +7.2, +15.0 cm³/cm³, while
   N65 *fell* in three of the four. N5.8 falls faster than N65, and WC is a
   difference. No pair is individually significant (~1.2 sigma at screen
   precision); the sign pattern plus a mechanism stated in advance is what
   carries. Best product so far: **104426** (4xF stripped from
   `2013[SiCu][pcu]3[ASR]1`), screening WC 192.0, screening N65 268.3 — the
   latter ties the best of all 6,818 database structures screened.
9. **The arm is narrow.** Only 209 of the 1,054 structures with
   N65_screen >= 200 carry any removable terminal group at all (845 have
   none), and in the top 300 by N65 the figure is 58. Defunctionalisation
   cannot be the main route to the ceiling; it is a bounded probe that may
   lift the single best candidate.
10. **A handful of structures will time out, not more.** Framework atoms after
   replication: p50 2,424, p99 7,488, p100 23,166; 109 structures exceed 8,000
   and 14 exceed 16,000. Exactly one point has timed out in 6,819 (id 3680,
   16,500 atoms, 7,200 s cap). Cost scales roughly as atoms times molecules, so
   the heavy tail needs a longer cap, not a different protocol.

## Current best numbers

| | value |
|---|---|
| Best **floor-protocol** WC measured so far | **197.61 ± 0.77** cm³/cm³, id 6178 `2015[V][srs]3[ASR]1`, ρ = 0.437, N65 = 232.58, N5.8 = 34.97, ratio 0.850 |
| Best **screening** WC, database structure | 184.8, id 4426 `2013[SiCu][pcu]3[ASR]1` (N65 255.5, N5.8 70.7) |
| Best **screening** WC, modified structure | 192.0, id 104426, 4xF -> H on 4426 |
| Best screen N65 seen (6,818 structures) | 268.0, id 9930 `2020[Al][fmz]3[ASR]1`, ρ = 0.526 |
| Screen N65 quantiles (6,818, density-biased sample) | p50 128.8, p90 214.6, p99 244.7, p100 268.0 |

6178 came out of a **random** sample of 46. That a random 46 already contains a
197.6 says the top of this database is high, and it sets the bar the claim has
to clear.


## Pre-registered predictions (recorded 2026-08-30 13:15, to be scored)

The screened 6,818 are a **representative** ~55% sample, not the light half
(KS D = 0.0048 vs 0.0244 critical). On that basis:

1. Max N(65 bar) over the 5,681 unscreened structures lands in **265-285**,
   most likely near 272.
2. It exceeds the current best of 268.0 with probability near **0.455** (the
   distribution-free exchangeability number), not the 0.77-0.99 an exponential
   tail fit gives -- the gap between them is evidence the tail is bounded,
   which is what the family decomposition also says.
3. The database maximum N(65 bar) is therefore within ~20 cm³/cm³ of 268.0,
   and since WC <= N65 that bounds the ceiling argument before the screen ends.

A 300 appearing in the unscreened half would falsify all three and force the
ceiling section to be rewritten. `bin/predict_unscreened.py` regenerates these.

## The funnel, calibrated end to end

| stage | quantity | bound in force | calibration |
|---|---|---|---|
| Tier 1 -> Tier 2 | N(65 bar) | min(1.25 x N65_screen, N65_screen + 6*err_v) | 45/45, worst 2.53 sigma |
| Tier 2 -> Tier 3 | working capacity | WC_screen + 5*sigma_screen | 46/46 at 4 sigma, worst 1.61 sigma |
| Tier 3 -> Tier 4 | working capacity | floor value, ranked directly | Pearson 0.9973 screen vs floor |

Nothing about the plan is now uncertain except how much cluster time arrives.

## Tier plan and budget

| Tier | Set | Protocol | Est. CPU-h | Status |
|---|---|---|---|---|
| 1 | all 12,499 | 65 bar, 200+500 | 285–447 | **54.6% done**, 5 chunks queued |
| 1v | 46 probe | 65 bar screen x2 seeds; both P at floor | 25 | **done** |
| 1w | same 46 | **5.8 bar at screen settings** | 2 | **done**, login node, 30-min batch |
| 2 | the 2,019 survivors of the N65 bound | 5.8 bar, 200+500 | ~85 | 5 chunks queued, task lists extended and ordered N65-descending |
| 3 | top ~200 by screening WC | both P, 2,000+10,000 (floor) | ~210 | not started |
| 4 | top ~10 x 3 seeds | both P, 10,000+50,000 (claim) | ~190 | not started |
| M | 209 defunctionalised products of the N65 >= 200 set | both P, 200+500 | ~20 | **built, 4 chunks in the plan as `mod_00..03`** |

Total ≈ 900–1,100 CPU-h against 1,610.

**Why the Tier-2 threshold of N65 >= 200 is a prioritisation, not an
exclusion.** Under the bound in force a structure is excluded only when
min(1.25 x N65_screen, N65_screen + 6*err_v) < WC*. Against the current
WC* = 197.6 that leaves 2,024 of the 6,818 screened alive, not 1,054. Tier 2
runs the 5.8-bar pass on survivors in descending-N65 order, so a partly
finished wave has still covered everything that could lead; it is extended down
the ranking as Tier 1 completes, with the threshold recomputed against whatever
WC* is by then. If the best WC reaches 240 the survivor set falls to 798
screened (~1,463 full database) and the extension shrinks.

## Open tasks

- [ ] **Tier 1**: chunks `s1_04,05,06,07,10` queued; `s1_11` is a one-point
      rescue of id 3680 at ppn=2 with a 28,800 s cap. `s1_02` was retired
      (job 3443 `qrm`ed): it was complete but for 3680 and the watchdog was
      re-queueing an 8-core job to retry one point.
- [ ] **Tier 2** `s2_00..04` queued (1,054 ids, `manifests/s2_ids.txt`).
      Extend to N65_screen >= 158 once Tier 1 finishes.
- [ ] **cal_01** queued: 5.8 bar at screen settings on the 46 calibration
      structures. This is the missing calibration — it measures
      WC_screen vs WC_floor directly, which is what the Tier 2 → Tier 3
      exclusion margin has to rest on. Until it lands, no Tier-3 cut is
      defensible.
- [ ] Tier 3 and 4 not started. Trigger: Tier 2 coverage of the N65 >= 158 set.
- [ ] **Modification arm built.** 209 products in `mods/`, registered in
      `manifests/mods.csv` with source id, group tally and atom counts; ids are
      source id + 100000 so they can never collide with a database id, and
      `gcmc.manifest()` overlays them so a product runs the identical prep,
      pinned input and parser as a database structure. Wave `mod_00..03`
      (418 points, both pressures, screen settings) is in
      `jobs/autopilot.plan` and takes slots as s1 chunks finish. Survivors go
      to Tier 3 alongside database structures.
- [ ] Charter §3 compliance for the arm: substituent -> H on the same bond
      vector, monovalent for monovalent, so every surviving atom keeps its
      formal charge and the framework stays neutral by construction. The recipe
      is `bin/modify.py`, the source id is in `manifests/mods.csv`, so every
      product regenerates from the repository alone.

## Errors on the record

- **2026-08-30, ~00:00 to 11:50 — every dispatched job died at its first line
  and I did not notice.** `bin/select.py` shadowed the stdlib `select` module;
  every script here puts `bin/` first on `sys.path`; `run_batch.py` imports
  `multiprocessing`, which reaches `selectors`, which does `select.select`.
  Chunks `s1_02,04,05,06,07,10,11` exited in under a second with a traceback
  and no rows, and `autopilot.sh` resubmitted each to the back of a FIFO queue
  shared by sixteen replicates. **No compute billed; about eight hours of queue
  position lost.** The screen has been frozen at 6,819 since 03:55 for this
  reason as well as for contention. Root cause removed at 11:50 (rename to
  `bin/candidates.py`) before I understood it, so queued jobs import correctly
  at dispatch and no resubmission was needed. Guards now in place:
  `bin/test_no_shadow.py`, an autopilot preflight that submits nothing on
  failure, `logs/ALERT`, and the ticker's `alerts` column. **The underlying
  mistake was not the module name — it was three status views that could not
  tell "not progressing" from "failing", and never reading `jobs/*.out`.**
- `pgrep -f autopilot.sh` matches the `pgrep` command's own arguments and
  reported a dead autopilot as running. `bin/daemons.sh` matches
  `^bash bin/<name>.sh` through `ps` instead.

- 20:44 2026-08-29 watchdog double-submitted `s1_00`/`s1_01` (live count 14 >
  cap 12) because it read only the mjs queue listing, which drops dispatched
  jobs. Withdrawn before dispatch, no GCMC work duplicated. Fixed via
  `census.sh`.
- A log entry was stamped 23:00 when it was written at 22:38; corrected on the
  record in commit 5d44a98.
- `bin/status.sh` carried the pre-pause deadline (19:41) for 4.4 h after the
  harness extended it. Corrected here and in the script.
- Two entries in LOG.md were stamped from my own estimate rather than from the
  cluster clock (12:10 and 12:40 against a true 11:52). Corrected at the foot
  of that section; stamps are now read from the cluster before use.
- `bin/select.py` shadowed the stdlib `select` module for any script that puts
  `bin/` first on `sys.path`, which is all of them; it broke `import numpy` in
  a fresh script. Renamed `bin/candidates.py`. Nothing had imported it, so no
  result is affected.
- `bin/modify.py` bond perception built a full n x n x 3 array per periodic
  image and ran at ~30 s a structure, which would have put a geometry-only
  step over the 30-minute login-node etiquette limit. Rewritten on a KD-tree;
  the old routine is kept as `neighbours_slow` and `bin/test_neighbours.py`
  asserts identical adjacency and identical perceived groups on 11 structures
  spanning 16 to 624 atoms.
- The four pilot product CIFs were deleted while rebuilding `mods/` but their
  rows survived in `manifests/mods.csv`, so `mkmods.py` skipped them as
  already-made and left four manifest rows pointing at absent files. Caught by
  checking, not by a failed run; rows dropped and regenerated.

## Operational reality as of 2026-08-30 20:00 (launch +24.3 h)

- **The scheduler has dispatched nothing to rep09 since 11:50.** Twelve chunks
  queued at ppn=2, front-loaded with claim-grade then floor-grade points, since
  those are the only work the login node cannot do. Queue depth ahead of me is
  draining at ~8 cores/h: ac went 176 -> 132 between 13:08 and 19:55, so
  **ETA for first dispatch is roughly 16 h**, around midday 2026-08-31. That
  still leaves ~100 h, so this is a delay, not yet a loss.
- **A 65-bar floor point cannot be produced on the login node.** Measured
  floor/screen wall ratio p50 18.3, p90 24.6, max 29.7, and under contention a
  44 s screen structure still blew the 1,620 s cap. Login batches therefore do
  Tier-2 screen points and **5.8-bar floor points only** — half of every pair,
  with the 65-bar half waiting on the scheduler.
- Login node: `bin/login_driver.sh`, 4 workers, near-continuous, 28-min
  batches, ~4% of a 96-core node that the fleet already loads to ~84 with 43
  `simulate` processes. Stands down automatically at >=3 running cluster jobs.
- Two escalations filed and queued: fleet contention, and the specific blocker
  that Tiers 3 and 4 require dispatch.

**If the scheduler never dispatches**, the reports Claim will be the best

## Operational reality as of 2026-08-30 20:00 (launch +24.3 h)

- **The scheduler has dispatched nothing to rep09 since 11:50.** Twelve chunks
  queued at ppn=2, front-loaded with claim-grade then floor-grade points, since
  those are the only work the login node cannot do. Queue depth ahead of me is
  draining at ~8 cores/h: ac went 176 to 132 between 13:08 and 19:55, so
  **ETA for first dispatch is roughly 16 h**, around midday 2026-08-31. That
  still leaves ~100 h, so this is a delay, not yet a loss.
- **A 65-bar floor point cannot be produced on the login node.** Measured
  floor/screen wall ratio p50 18.3, p90 24.6, max 29.7, and under contention a
  44 s screen structure still blew the 1,620 s cap. Login batches therefore do
  Tier-2 screen points and **5.8-bar floor points only** - half of every pair,
  with the 65-bar half waiting on the scheduler.
- Login node: `bin/login_driver.sh`, 4 workers, near-continuous, 28-min
  batches, ~4% of a 96-core node that the fleet already loads to ~84 with 43
  `simulate` processes. Stands down automatically at 3 or more running cluster
  jobs.
- Two escalations filed and queued: fleet contention, and the specific blocker
  that Tiers 3 and 4 require dispatch.

**If the scheduler never dispatches**, the report's Claim will be the best
floor-grade number available - currently 197.61 for id 6178 - with the
screening leaderboard as supporting evidence that 10995 at 208.17 and 6782 at
202.14 are better, explicitly labelled screening-grade. That is an honest
incomplete report and section 5 says it is compliant. It is not the intended
outcome, and every queued chunk is arranged to avoid it.
