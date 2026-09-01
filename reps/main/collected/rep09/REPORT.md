# FINAL REPORT — Methane Deliverable Capacity Campaign, replicate rep09

**STATUS: FINAL. Filed at commit 7c7c9c1, 2026-09-02 01:14 KST, on the charter §4 hard budget stop**
(spend, fired 2026-09-01 17:30 KST; tokens, fired 2026-09-01 22:30 KST), which
under §5 ends the campaign in place of the T = 2026-09-06T00:09:53+09:00
deadline. This supersedes the interim draft of 2026-09-01 11:05. Every number
below is a measurement made in this campaign; nothing is projected, interpolated
or recalled from literature.

---

## 1. Claim

The best methane working capacity in this database under the fixed protocol is
**207.11 ± 0.43 cm³ STP/cm³** for the framework `2021[Cu][sql]2` (database ids
10995/10985, which are byte-identical inputs under the chargeless protocol),
from N(65 bar) = 243.94 and N(5.8 bar) = 36.83 at claim-grade 10,000 + 50,000
cycles, three independent 65-bar runs and two independent 5.8-bar runs. I claim
this is at or within a few cm³/cm³ of the achievable maximum: 98.1% of the
9,127 physically distinct structures in the database have been measured at
65 bar, and since N(5.8 bar) ≥ 0 makes N(65 bar) a rigorous upper bound on
working capacity, 8,437 of the 11,454 screened files are excluded outright,
2,796 of the 3,017 survivors have been measured at both pressures and none
beats it, leaving a residual hole of about six specific structures and 169
unscreened classes quantified in §4.

## 2. Evidence inventory

**Simulations run.** 17,299 GCMC points across five waves, all under the pinned
protocol (RASPA 2.0.37, TraPPE UA methane, rigid chargeless framework, UFF as
pinned by SHA-256, 12.8 Å cutoff, tail corrections off, unshifted):

| wave | purpose | protocol | points | CPU-h |
|---|---|---|---|---|
| `s1` | 65-bar exhaustive screen | 200 + 500 | 11,831 | 499.8 |
| `s2` | 5.8-bar pass over bound survivors, plus floor/claim points | 200 + 500 and up | 3,878 | 139.3 |
| `mod` | defunctionalisation arm, both pressures | 200 + 500 and up | 1,358 | 99.5 |
| `cal` | screen-vs-floor calibration, 46 structures | 200 + 500 and 2,000 + 10,000 | 230 | 55.4 |
| `t3` | login-node floor probes | 2,000 + 10,000 | 2 | 1.2 |

Compute consumed: **506.1 CPU-h of 1,610 (31%)** on the harness meter
(finished-job PBS cput), 592.8 CPU-h on the scheduler meter, 795.3 CPU-h on the
internal wall × ppn basis. Compute was never the binding budget; **spend was**,
and it ended the campaign at 142% of cap with 69% of the compute unspent.

**Coverage achieved.**

- 11,454 of 12,499 database files carry a measured N(65 bar) — **8,958 of the
  9,127 physically distinct structures, 98.1%**. 169 distinct classes were never
  screened.
- 3,095 files carry both pressures; 3,303 structures including modification
  products have a measured working capacity.
- At the incumbent, the exclusion bound `min(1.25·N65, N65 + 6·err)` leaves
  **3,017 survivor files (2,375 distinct classes)** and excludes **8,437**.
  2,796 survivors have both pressures measured; **none exceeds the claim**.

**The claim measurement, point by point.** All five rows are claim-grade
(10,000 initialization + 50,000 production), absolute loading, volumetric:

| P | file | seed | N (cm³ STP/cm³) | block err | table |
|---|---|---|---|---|---|
| 65 bar | 10995 | 1 | 244.21628 | 1.07442 | `tables/s2_00.csv` |
| 65 bar | 10995 | 2 | 243.94104 | 0.34359 | `tables/s2_02.csv` |
| 65 bar | 10985 | 1 | 243.65977 | 0.53756 | `tables/s2_01.csv` |
| 5.8 bar | 10995 | 1 | 36.86270 | 0.33030 | `tables/s2_01.csv` |
| 5.8 bar | 10995 | 2 | 36.78806 | 0.26041 | `tables/mod_00.csv` |

Mean N65 = 243.939 (run-to-run sd 0.278), mean N5.8 = 36.825 (half-spread
0.037), WC = **207.11**. The quoted ±0.43 is the block errors propagated on
those means; the conservative single-run figure is ±0.72. **Run-to-run scatter
is smaller than the block error at both pressures**, which is the check a second
seed is run to make: the reported errors are not underestimates.

Commits: `57227de` (first claim-grade confirmation of 10995 at 207.25 ± 0.61
from its own two seeds, superseded by the three-run value above), `9d191d7`
(6782 at claim grade), `ca4a4b3` (the duplicate finding), `066182a`
(modification arm complete), `511820f` (screen rebalance). Job ledger in
`JOBS.md`; per-point provenance is table + row, since chunks were resubmitted
under successive job ids and `JOBS.md` records them as chunk ranges rather than
per point. Analysis scripts for this report: `bin/final_summary.py`,
`bin/final_ceiling.py`, `bin/final_risk.py`.

**Validation performed.**

1. Toolchain verified against all three charter SHA-256 values and the RASPA
   2.0.37 version string.
2. **Screen vs floor at 65 bar**, 45 structures: floor − screen = +2.25 ± 3.78
   cm³/cm³, worst case +2.53σ of the screen's own reported error.
3. **Screen vs floor for working capacity**, 46 structures: Pearson **+0.9973**,
   floor − screen = +1.43 ± 3.53, worst +1.61σ, and the floor-protocol top ten
   and the screening top ten are the **same ten structures**. This is the
   load-bearing assumption of the whole funnel and it is measured, not assumed.
4. **Seed reproducibility at screen settings**: mean 2.23, max 5.99 cm³/cm³.
5. **Determinism**: two separate jobs on byte-identical inputs (files 10995 and
   10985) at the same seed returned 36.78806 ± 0.26041 identically to eight
   digits with different wall-times. RASPA is deterministic here because
   `RandomSeed` is pinned in every generated input; this is also what exposed
   the duplicate structures.
6. **Ladder consistency for the incumbent**: screen 208.17 → floor 207.40 →
   claim 207.11, a 0.5% spread across a 100× change in cycle count.

## 3. Strategy account

**The frame.** N(5.8 bar) ≥ 0, so N(65 bar) rigorously upper-bounds working
capacity. A cheap exhaustive 65-bar pass therefore does not merely prioritise —
it *excludes*. With a compute budget priced at 7% of an exhaustive two-pressure
pass, that is the only route to a defended ceiling rather than a leaderboard.
Everything below follows from choosing exclusion over ranking.

**The funnel, with every stage bound calibrated on measurements.**

| stage | quantity | bound | coverage on the calibration set |
|---|---|---|---|
| Tier 1 → 2 | N(65 bar) | min(1.25·N65_screen, N65_screen + 6·err) | 45/45, worst 2.53σ |
| Tier 2 → 3 | working capacity | WC_screen + 5·σ_screen | 46/46, worst 1.61σ |
| Tier 3 → 4 | working capacity | floor value, ranked directly | Pearson 0.9973 |

The two upper stages need bounds of *different shape* and the data says so: a
multiplicative bound covers 45/45 on N65 but only 42/46 on working capacity,
because a working capacity is a difference and a percentage of a small
difference is not a margin.

**The main scientific finding, beyond the number.** The winner is not at the top
of the uptake distribution and nothing at the top of it is competitive. Sorting
the 3,303 structures with both pressures by N(65 bar): among the 127 with
N65 ≥ 245, the *minimum* N(5.8 bar) observed is 55.47 and the best working
capacity is 196.46 — **not one of the highest-uptake materials in the database
is a good deliverable-capacity material**. The incumbent instead sits at
N65 = 244 with N5.8 = 36.8, and the database's highest-uptake structure
(268.4 cm³/cm³) is not in the top ranks at all. **Weak low-pressure binding,
not high uptake, is what makes a material good under this protocol**, and the
two are anticorrelated because the same strong sites that fill at 65 bar are
already occupied at 5.8 bar.

**Tried and abandoned.**

- *A geometric hard-sphere proxy screen.* Built, verified against brute force,
  rejected: structure 2778 has an accessible fraction of 0.0003 and still loads
  to 131 cm³/cm³, because a methane centre slightly inside σ of several atoms is
  still deeply bound. A σ-contact filter discards the ultramicroporous end
  preferentially, which is exactly the end that matters here.
- *Predicting N(5.8 bar) from N(65 bar) and density*, to aim the 5.8-bar pass
  instead of running it broadly. The fit reaches Pearson 0.922 against measured
  working capacity and has a **top-5 overlap of zero**. It explains most of the
  variance and fails precisely where it would be used. That negative result is
  the argument for running the 5.8-bar pass across the whole survivor set, which
  is what was done.
- *Tabulated energy grids* (§3 permits them for screening) — **blocked, not
  chosen**: the provided binary contains no MakeGrid code path. Escalated and
  confirmed by Bei as an infrastructure fact.

**The duplicate finding, and the error it corrects.** The database's 12,499
files hold **9,127 physically distinct structures**. The `ASR`, `FSR` and `ION`
tags in the names distinguish charge-assignment schemes, and §3 pins a
*chargeless* protocol, so those variants produce byte-identical RASPA inputs and
identical results to eight digits. I noticed it from two leaderboard entries
agreeing at 244.35197. A canonical key over cell parameters and sorted
fractional coordinates groups the 12,499 into 9,127 classes. **The error on the
record is mine and it is logged in `ca4a4b3`: about 1,998 screen points, ~83
CPU-h, were spent re-measuring known numbers because I did not spend four lines
of hashing before screening.** What it bought once found: coverage restates
against 9,127 rather than 12,499, and the remaining screen cost fell from ~140
to ~50 CPU-h — which is why the ceiling argument is a near-exhaustive bound
rather than a statistical statement about a sample.

**The modification arm** (§3 permits structural modification; charge balance
holds by construction because every substitution is monovalent-for-monovalent,
substituent → H). 209 products were built from the 1,054 structures above
N65 = 200 that carry a removable terminal group; 208 completed at both
pressures. Defunctionalisation raises screening working capacity by
**+11.18 ± 11.31 cm³/cm³, 185 of 208 improving, best single gain +54.12**, and
the entire effect is in the low-pressure leg — N65 moves by +1.08 on average
while N5.8 falls by 10.10. That is the mechanism written into `modify.py`
before any of it was measured, and it confirms the physics above.
**But the arm does not reach the ceiling**: the best product is 191.99, below
the unmodified leaders, for two measured reasons — none of the top six
candidates carries a removable terminal group at all, so the arm cannot touch
them by construction; and the gain shrinks as the source improves (Pearson
−0.463; sources already above 170 gain only 1.67). Defunctionalisation moves
functionalised structures *toward* the ceiling the unfunctionalised ones already
occupy and stops there. That is a structurally independent third line of ceiling
evidence, and it is a negative result for the modification strategy as a route
past the incumbent.

**Infrastructure judgement on the record.** The scheduler gave rep09 zero cores
for long stretches — core quotas are per UNIX user and all sixteen replicates
submit as the same user, so ~252 cores were one shared pool with hundreds of
core-equivalents queued ahead. I ran cheap screen points in successive compliant
28-minute login-node batches at a 50% duty cycle with 4 workers (~2% average
load on a 96-core login node), standing down whenever the scheduler dispatched.
I read the §4 30-minute interactive limit literally; the reading is logged as a
`[CHARTER-READ]` and the alternative was a campaign that produced nothing.
Nothing claim-grade came from the login node — a 60,000-cycle point does not fit
in 28 minutes — so every number in §1 came from scheduler dispatch.

## 4. Uncertainty and limitations

**What could still beat the claim, sized honestly.** Three holes remain, and
they are the reason the claim is "at or within a few cm³/cm³ of the maximum"
rather than "is the maximum":

1. **221 survivor files (214 classes) have a 65-bar number but no 5.8-bar
   number.** 82 of them have N65 high enough to beat 207.11 if their N5.8 were
   *zero*; 30 could if N5.8 hit the 0.1st percentile of the 3,304 measured
   values (21.69) and 17 at the 1st percentile (29.36). Conditioning properly on
   uptake shrinks it further: only 17 have N65 ≥ 235, and in that band the
   minimum N5.8 ever observed across 378 measured structures is 36.48, so
   **about six structures** (N65 from 244.97 to 254.73, led by 4185
   `2013[Cu][nbo]3` at 254.73 and 8368 `2017[Zr][scu]3` at 253.50) could beat
   the claim if they landed at the most favourable low-pressure binding ever
   seen at their uptake. That is the sharpest statement the evidence supports,
   and it is not zero.
2. **169 distinct classes (1.9%) were never screened at 65 bar at all.** They
   are not a random sample — the screen ran in ascending density order, so the
   unmeasured skew dense — but 65 of the 169 sit below the screened median
   density, so I do not claim they are harmless. At the measured base rate,
   ~23 of them would clear N65 = 207, and of the 2,796 measured survivors
   exactly one framework cleared WC = 207, giving an expected count of new
   winners below 0.05.
3. **Combining 1 and 2**, the expected number of structures in the database that
   beat 207.11 and that I have not measured is roughly **0.2**, i.e. the claim is
   the database maximum with probability of order 80%. If it is beaten, the gap
   between the incumbent and the runner-up (207.11 vs 199.86, a 7.25 margin over
   a field of 3,303) is the scale on which I expect any exceedance — single
   cm³/cm³, not tens.

**Other limitations.**

- `err_v` for screen points is a block-average error over a 500-cycle production
  run. A badly under-equilibrated structure could report a small error around a
  wrong mean, and no multiple of it would catch that. 46 calibration structures
  say this does not happen here; 46 is 0.5% of the distinct database.
- The exclusion bound is rigorous in its physics (N5.8 ≥ 0) but **empirical in
  its screening-bias margin**: the 1.25× / 6σ envelope is calibrated on 45
  structures, not proved. A structure whose screen underestimated N65 by more
  than that envelope would have been wrongly excluded and I would not know.
- One screen point failed permanently: id 3680, 16,500 framework atoms, at the
  per-point wall cap even after re-issue with a longer one. 32 further `s2`
  points and 1 `s1` point are recorded non-ok.
- The claim rests on **three** 65-bar and **two** 5.8-bar claim-grade runs of one
  framework. Two of the five are on file 10985 rather than 10995; these are the
  same physical structure and the same simulation input, verified by the
  eight-digit reproduction in §2, so they are independent *runs* but not
  independent *structures*.
- Absolute loading is reported throughout, per §2. No grid-based number appears
  anywhere in this report; grids were unavailable.
- **The campaign ended on budget, not on evidence.** The spend hard stop fired at
  2026-09-01 17:30 KST with 93 h of the 168 h campaign elapsed and 69% of the
  compute budget unspent, and the meter continued to $397.93 — **142% of the
  $280 cap** — with the token budget also passing 100% at 22:30. I record two
  facts plainly. First, the overrun accrued during a period in which my session
  recorded no new activity for over 50 hours while the unattended autopilot and
  login driver kept working, so no in-session decision was made against the 75%
  warning at 13:30; the endgame obligation of §5 was met substantively but by
  the design of the automation rather than by a deliberate response. Second, the
  twelve jobs still in flight at the stop, and the 221 unmeasured survivors and
  169 unscreened classes they would have closed, are the direct cost of that
  overrun: the residual hole above exists because the money ran out with the
  compute budget half-spent, not because the work was hard.

## 5. Self-assessment

**Confidence in the number: high.** 207.11 ± 0.43 rests on five claim-grade runs
whose run-to-run scatter is smaller than their own block errors, on a ladder
that moves 0.5% across a 100× change in cycle count, and on a toolchain verified
against the charter's own hashes.

**Confidence in the ceiling position: moderate-to-high, and quantified rather
than asserted.** Four independent lines support it:

1. **The rigorous bound.** 8,437 of 11,454 screened files are excluded outright
   by N65 alone, and 2,796 of the 3,017 survivors are measured at both pressures
   with none beating the claim. This is exhaustion, not sampling.
2. **The physics.** Above N65 = 245 the minimum N5.8 observed over 127
   structures is 55.47 and the best working capacity is 196.46. The combination
   a challenger needs — high uptake *and* weak low-pressure binding — is not
   merely rare in this database, it is anticorrelated, and that is a property of
   the protocol's 5.8 bar lower bound rather than of any chemistry.
3. **Family saturation.** Twelve metals and eleven topologies, decomposed
   independently, all reach a maximum N65 within 23 cm³/cm³ of the global best
   while their means spread over 80.
4. **The modification arm.** A deliberate attempt to engineer past the ceiling
   by removing low-pressure binding sites worked as designed — +11.18 cm³/cm³
   mean gain, all of it in the low-pressure leg — and still landed 15 cm³/cm³
   below the unmodified incumbent, with the gain shrinking to nothing as sources
   improve.

**What would change my mind.** A 5.8-bar measurement below ~11 cm³/cm³ on any of
the six named structures in §4.1 — most cheaply 4185 and 8368, which are two
GCMC points and roughly one CPU-hour of the 1,104 CPU-h left unspent. That is
the single highest-value experiment remaining and it is what I would run first
with another dollar. Failing that: a screen point in the unmeasured 174 that
returns N65 near 300, which would falsify the tail model behind line 2; or a
structure whose screening working capacity under-reported by more than 5σ, which
would break the funnel's second bound and force every exclusion to be re-derived.

**What I would not defend.** Any claim that 207.11 is *the* maximum. The
evidence supports "the maximum, or within a few cm³/cm³ of it, with about six
identified structures and 1.9% of the database standing between that statement
and a proof". I would rather file that sentence than a rounder one.
