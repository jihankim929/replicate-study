# FINAL REPORT — Methane Deliverable Capacity Campaign (rep04)

> **STATUS: FILED 2026-09-01 16:10 KST, under charter §5 (early filing).**
> This is the final report. Filed at 79% of the spend budget — the §4 budget that binds —
> with the deliverable complete rather than at exhaustion with it half-written, which is
> what charter §5 (Rev 24) instructs: *an honest report of a verified intermediate result
> outranks an ambitious campaign with no filed claim.* Every number below is from a
> simulation run in this campaign and traceable to `results/*.csv`, `JOBS.md` and the git
> history. The Claim rests only on runs at the §3 claim-grade cycle count
> (10,000 initialization + 50,000 production, grid-free). Screening numbers are labelled as
> such wherever they appear.

## 1. Claim

**S10985** (`2021[Cu][sql]2[ASR]6`) delivers a methane working capacity of
**206.8 ± 0.6 cm³ STP/cm³** — N(65 bar) − N(5.8 bar) at 298 K, absolute, volumetric —
at claim-grade cycles (seed 0; N(65) = 243.66, N(5.8) = 36.86).
It leads the next claim-grade structure (S06782, 199.68) by **7.1 cm³/cm³**.

**Ceiling position: this is at or very near the achievable maximum for this database and
protocol.** Every one of the 11830 structures below φ = 0.26 is bounded at **203.8 cm³/cm³**
by a regression calibrated on 266 GCMC pairs and applied with the largest residual ever
observed rather than a Gaussian tail; the 669 structures at φ ≥ 0.26 are the only ones that
could exceed that, and **224 of them are measured individually**. The database maximum is
therefore `max(203.8, best measured in the φ ≥ 0.26 band)`, which resolves to 206.8.
I do not expect it to be exceeded by more than a few cm³/cm³. The exposure is the
unmeasured remainder of that band, stated in §4.

## 2. Evidence inventory

All simulations: RASPA 2.0.37 (commit `4467e14c`), TraPPE united-atom methane, rigid
chargeless framework, pinned UFF set (sha256 triple verified against §3), cutoff 12.8 Å,
unshifted, tail corrections off, 298 K, absolute loading. **All reported numbers are
grid-free**; no grid-based number is promoted. Compute used: busy=616.2 sched=828.0 inflight=311.3 total=831.8 CPU-h of 1610 (51.7%) running=calib5,claim0,claim1,claim2,t1a0,t1a1,t1a5.

**Protocol verification.** The applied parameters were read back from RASPA's own output
echo rather than trusted from my input files: `CutOff VDW 12.800000`, `shift/k_B 0.0` on
every pair, `tailcorrection: no` on every pair, `CH4_sp3` at 148.0 K / 3.73 Å, CH4–Zn mixing
reproducing Lorentz–Berthelot to five figures, and the 12.7375 volumetric factor derived
independently from the primitive cell volume. Commit `d53a1e5`.

**Claim-grade capacities (10,000 + 50,000, same seed both legs, grid-free).**

| structure | seed | DC | ± | N(65) | N(5.8) | screening DC |
|---|---|---|---|---|---|---|
| S10985 | 0 | **206.80** | 0.63 | 243.66 | 36.86 | 207.45 |
| S06782 | 2 | **199.68** | 0.45 | 243.48 | 43.80 | 199.57 |
| S06782 | 0 | **199.67** | 0.77 | 243.54 | 43.87 | 199.57 |
| S06178 | 1 | **197.28** | 0.80 | 232.14 | 34.86 | 197.61 |
| S04477 | 2 | **196.26** | 0.68 | 242.27 | 46.01 | 196.81 |
| S04477 | 0 | **196.24** | 0.36 | 242.26 | 46.01 | 196.81 |
| S10394 | 2 | **196.00** | 0.44 | 237.70 | 41.71 | 196.41 |
| S08808 | 0 | **191.42** | 0.74 | 251.28 | 59.85 | 191.86 |

**Screening.** A Widom-insertion descriptor sweep over all 12,499 structures (mjs 3020,
19 CPU-h, commit `a241d39`) produced `manifest/desc_all.csv`. GCMC screening at the §3 floor
count (2,000 + 10,000) has produced **266 complete pressure pairs**, of which **224 lie in the
φ ≥ 0.26 band** that the ceiling argument says is the only place a winner can live.

**Reproducibility of the screen.** 25 claim-grade legs reproduce their floor-cycle values to
within 0.65 cm³/cm³ everywhere measured (five of the 8 capacities slightly low, mean −0.33,
range −0.65 to +0.11). The floor screen, and therefore the regression and the bound built on
it, are sound at about the 0.3% level.

**Seed replication at claim grade.** S04477 differs by 0.02 across two independent seeds; S06782 differs by 0.01 across two independent seeds.
The quoted block errors (0.36–0.80) are an order of magnitude larger than the measured
seed spread, so the ± on the Claim is conservative.

**Structural sanity of the head (§9).** Minimum interatomic distances over all periodic
images for the top structures are 0.86–1.14 Å with **zero** pairs below 0.8 Å — ordinary
bond lengths, not overlaps. The porosity of the leaders is real. Commit `1beec51`.

*(Job IDs, per-structure numbers and per-commit traceability: `JOBS.md`, `LOG.md`,
`results/*.csv`. Repository HEAD at filing: `b23066c`.)*

## 3. Strategy account

**Chosen:** a cheap Widom descriptor surrogate over the whole database to *rank* rather than
to *predict*, calibrated against GCMC on a stratified set before being trusted; then GCMC at
floor cycles over the head and down the porosity ordering; then claim-grade cycles with
independent seeds on the finalists.

**The key strategic turn** was to identify which half of the ceiling argument could carry
weight, and to place the measured/inferred boundary where it does. Below φ = 0.26 the claim
rests on a calibrated statistical bound; at and above φ = 0.26 it rests on measuring
structures individually. A physical bound (accessible volume × deliverable density) was
initially cast as primary and was **demoted to corroboration**: the φ cut it implies swings
from 0.220 to 0.332 with an arbitrary choice of the φ floor used to estimate maximum density,
and at high porosity the envelope reduces to 0.409 × 507 = 207.5, meaning the leader *is* the
envelope rather than sitting under it. It still explains why the screen boundary sits where
it does.

**The statistical half, and its stress tests.** Fitting DC = 17.45 + 1.757 × surrogate
(σ = 7.4, largest residual +29.2) over 266 pairs spanning the full range, and applying the
*largest residual ever observed* rather than a Gaussian tail, **zero of the 11830 structures
below φ = 0.26 can reach the leader** — the best of them, at surrogate 89.4, bounds at 203.8.
Three stress tests all cut the same way: refitting on only the 156 pairs with surrogate ≤ 90
(the region that does the excluding) gives a slightly *higher* bound of 204.3, so the head
structures are not driving it; a quadratic term is negative, so the relation saturates and
linear extrapolation is conservative; and residual spread is no larger in the bands that do
the excluding than elsewhere.

**Deduplication was removed from the argument entirely.** ASR/FSR structure pairs are
near-identical, and an earlier version of this report used that to merge them — with a regex
bug that stripped the *index* as well as the tag and over-merged up to 43 distinct structures
into one supposed twin group. Corrected in commit `0b84498`. Every structure is now counted
individually everywhere in this report; twin pairs are used only as reproducibility checks.

**Abandoned — tabulated energy grids.** Validated as accurate (0.2 Å grids reproduce
grid-free loadings to better than 0.5%) but not useful: the speed-up is 2.6× at 5.8 bar and
nil at 65 bar, because a grid tabulates only the guest–framework potential while
high-pressure cost is dominated by guest–guest. Grid-free everywhere keeps one method behind
every number. (A harness notice claimed MakeGrid was absent from the build; it had grepped
`bin/simulate`, an 18 KB driver, while the code is in `lib/libraspa2.so`. Escalated for the
fleet, not relied on here.)

**Abandoned — resubmitting jobs to reorder work.** All sixteen replicates share one scheduler
account, so queue position is scarcer than compute; one qrm-and-resubmit cost ~1.5 h of
position. The replacement is to rewrite a *queued* job's task list in place, since PBS reads
it at runtime. That technique carries its own hazard, recorded in §4.

## 4. Uncertainty and limitations

- **Coverage is the binding limitation on the Claim.** 224 of the 669 structures at φ ≥ 0.26
  have complete pressure pairs — **33% of the band the ceiling argument says is the only
  place a winner could live.** The screen ran in descending φ, so the unmeasured remainder is
  its lower-porosity part, where the statistical bound is tightest; but this is an assertion
  about 669 structures of which under a third are measured, and it is the honest reason to
  doubt that S10985 is *the* database maximum.
- **The margin over the statistical bound is 3.0 cm³/cm³ and it has narrowed.** The best
  sub-0.26-φ structure bounds at 203.8 against a leader of 206.80. On the smaller sample of
  2026-08-31 those figures were 199.2 and 207.45. The bound rose because the fitted slope
  rose with more data; it is stated with the largest residual ever observed, so it is
  conservative, but the gap is now small enough that it is the number to watch.
- **The scheduled work that did not run.** The edge set (structures below φ 0.26 with high
  surrogate values) and the surrogate 75–80 tail sat at the bottom of every task list and
  were not reached. They were scheduled and reachable; compute and spend ran out first.
- **Seeds and cycle count are measured and small**, so they are *not* a limitation: seed
  spread on a complete claim-grade capacity is 0.01–0.02 cm³/cm³, and claim-grade agrees with
  floor cycles to within 0.65 everywhere. An earlier draft of this report called the
  claim-grade-vs-floor shift systematic on the first five points; the next three did not
  support that, and it is scatter with a slight negative mean.
- **Instrumentation failures found in my own work, all corrected on the record.** My compute
  meter counted three long-finished jobs as still running (they were killed and never wrote
  an END line), inflating it by 62% and very nearly tripping an automatic HALT at under half
  the real budget. A task-list repair script rewrote lists belonging to running jobs; because
  writes are rename-based the running jobs were unaffected, but the edits were inert and five
  claim-completing legs were briefly scheduled nowhere. Both are in `LOG.md`. The common
  shape — inferring a state from the absence of a record — is the main methodological
  lesson of this campaign.
- **Not verified:** that the linear DC-vs-surrogate relation holds outside the sampled range;
  that any structure in the unmeasured φ ≥ 0.26 remainder does not exceed the leader; and the
  behaviour of structures above φ 0.6, where only 5 are measured.

## 5. Self-assessment

Confidence that the true maximum for this database and protocol lies in **200–215 cm³/cm³**:
**high**. Two independent arguments bracket it — a calibrated bound excluding 11830 structures
below φ 0.26, and direct measurement of the porosity range where capacity actually peaks.
The measured maximum by porosity band shows a clear interior peak:

| φ band | measured | best screening DC |
|---|---|---|
| 0.0–0.1 | 17 | 147.5 (S00220) |
| 0.1–0.2 | 3 | 131.1 (S07773) |
| 0.2–0.3 | 51 | 184.9 (S00375) |
| 0.3–0.4 | 110 | 199.6 (S06782) |
| 0.4–0.5 | 51 | 207.5 (S10985) |
| 0.5–0.6 | 29 | 183.4 (S02844) |
| 0.6–1.0 | 5 | 148.0 (S03579) |

Capacity rises to the 0.4–0.5 band and **falls above it**, now on 34 structures above φ 0.5
rather than the 2 an earlier draft rested on. That closes the standing worry that the head
sat at the edge of its own sample and the frontier lay toward higher porosity: it does not.

Confidence that **S10985 specifically** is *the* database maximum: **moderate, and limited by
coverage alone.** Its 7.1 cm³/cm³ lead is some 350× the measured seed noise, so the ordering
of the head is not a Monte Carlo artefact. The doubt is that 445 of 669 structures in the
candidate band remain unmeasured.

**What would change my mind:** any structure in the unmeasured φ ≥ 0.26 remainder measuring
above 206.8, which is possible and is the reason the ceiling claim is stated as a bound rather
than a certainty; a structure with φ > 0.5 measuring above ~200, which would reverse the
turnover that 34 measurements now support; or a measured deliverable density above ~800 cm³
STP per cm³ of accessible volume, which would lift the physical bound and re-admit thousands
of lower-porosity structures.

---

# POST-FILING CORRECTION — 2026-09-02 01:xx KST

*Appended after filing, under charter §6 ("errors you discover in your own work are logged and
corrected on the record, never silently fixed or deleted"). The report above is unaltered: this
section states what is wrong with it and what replaces it. The **Claim of §1 is unaffected** —
S10985 at 206.8 ± 0.6 cm³ STP/cm³ is a direct claim-grade measurement, and every claim-grade
result that has landed since filing confirms it. What is corrected is the **ceiling sentence**.*

## C1. What happened

Jobs left running at filing have since completed, adding 71 complete GCMC pairs (266 → 337) and
two further claim-grade structures. Re-checking the filed ceiling against the enlarged set
exposed two defects, one in the filed number and one in the instrument that produced it.

**Defect 1 — the bound was computed on a partial dataset.** Four of the eleven files in
`results/` (`claim.csv`, `edge.csv`, `tier2.csv`, `twin.csv`) carry **no header row**. Every
analysis script in `bin/` that reads them with `csv.DictReader` — `gap2.py`, `ceiling.py`,
`ceilA.py`, `calfit.py` and ~25 others — therefore drops all four files entirely and
additionally mis-reads each one's first data row as field names. `claim.csv` is the
claim-grade file. The filed figure **203.8** came from `gap2.py`, so it was fit **without a
single claim-grade point and without the edge set** — 164 usable rows invisible to it. The
filed sentence pairs that number with a pair-count of 266 computed by `finalrep.py`, which
reads positionally and was never affected; the two numbers therefore come from different
datasets. **`finalrep.py` uses `csv.reader`, so every other number in the report above —
the Claim, the coverage counts, the band table, the seed-noise figures — is unaffected.**
The corrected script is `bin/gap3.py`.

**Defect 2 — the bound grows with sample size by construction.** It is stated as the regression
prediction plus *the largest residual ever observed*. That is a maximum-order statistic: it can
only increase as pairs are added. On 337 pairs correctly parsed, the fit is essentially
unchanged (DC = 20.06 + 1.726·surrogate, σ = 8.2) but the largest residual has grown from +29.2
to **+39.0**, and the bound on the best sub-φ0.26 structure rises from 203.8 to **213.5**.
So more evidence *weakens the stated bound* while leaving the underlying conclusion intact.
That is a design flaw in the ceiling instrument, not a change in the science.

## C2. The corrected ceiling statement

**213.5 exceeds the leader, so `max(bound, best measured)` no longer resolves to 206.8, and the
filed ceiling sentence does not survive as written.** The ceiling position does survive, on
direct measurement rather than on the bound:

- The widened bound flags **19** structures below φ = 0.26 as able, in principle, to reach the
  leader. **15 of the 19 are now measured individually.** The best of them is **S02622 at
  177.1** — 29.7 cm³/cm³ below the leader and ~36 below its own bound. The bound is loose in
  precisely the region that does the excluding.
- Under a **3σ** criterion instead of the max residual, the sub-band bound is **199.1**, still
  below the leader, and **zero** structures below φ = 0.26 reach it.
- **4 structures remain without a complete pair** — S09908, S05154, S05828, S11200. Floor-cycle
  legs for all four were submitted as `rep04_ceil` (mjs 4524) at the time of this correction.

**Corrected ceiling position.** S10985 at 206.8 is at or very near the achievable maximum. The
defence is no longer a single bound but: (a) direct measurement of the φ ≥ 0.26 band, 270 of 669
structures; (b) direct measurement of 15 of the 19 sub-band structures the conservative bound
cannot exclude, all ≤ 177.1; (c) a 3σ statistical bound of 199.1 on the remainder. The residual
exposure is the 399 unmeasured structures at φ ≥ 0.26 — unchanged from §4 as filed, and still
the honest reason this is a bound and not a certainty — plus the 4 named structures above.

## C3. Assessment of the error

Both defects are the same failure the report already names as the methodological lesson of this
campaign: **an instrument reporting confidently against the wrong subject.** The floor lookup,
the compute-rate window and the CPU-hour meter all failed by inferring a state from an absence;
`DictReader` on a headerless file is that again — absence of a header read as absence of data,
silently, with no error raised. I did not catch it at filing because the leaderboard and
coverage scripts parse positionally and agreed with each other; the disagreement only became
visible when a positional count (340 pairs) was set beside a `DictReader` count (321).
Confidence in the Claim is **unchanged (high)**; confidence in the *filed form* of the ceiling
statement was misplaced and is withdrawn in favour of C2.
