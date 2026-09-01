# FINAL REPORT — Methane Deliverable Capacity Campaign, replicate **rep03**

## FILING DECLARATION - 2026-09-01

**This report is filed and this campaign is closed.** I state it explicitly,
in response to the PI ruling of 2026-09-01T03:52:50Z recorded in INBOX.md,
because a filing is a judgement I have to make and not one the harness should
infer from a status line. The campaign ended on the section 4 hard spend stop,
which section 5 makes terminal, at 100.2% of the $280 cap on 2026-09-01 at
00:19 KST. It did not reach T (2026-09-06T15:28:14+09:00) and it did not
exhaust compute, which stood at about 12% used; spend was the binding limit
throughout and that is the campaign's central operational finding.

The deliverable is the five section 7 sections below, unchanged by this
declaration. Its claim is a working capacity of 207.05 +/- 0.21 cm3 STP/cm3 for
2021[Cu][sql]2[ASR]6, and its ceiling position is that the leader is very
likely at or near the achievable maximum for this database and protocol,
explicitly not proven, with the shortfall named rather than glossed: the sweep
that would have converted the bound into a measurement reached 8 of its 124
structures.

Cluster jobs submitted before the stop may still be writing into results/ after
this filing. Nothing in this report depends on them, and no further result will
be collected, analysed or reported. No work follows this declaration.

**STATUS: FINAL as of the last revision below.** This file has been kept
continuously filable since 2026-08-31 so that a compliant §7 report exists at
every moment, not only at T (§5, Rev 24). Spend passed 84% at 22:16 KST on
2026-08-31 against a hard stop at 100%, and §5 ends the campaign at a budget
stop as surely as at the deadline, so this is written to be read as the final
report rather than as a draft awaiting one. Where work was still running when it
was written, that is stated as such and the number is given as it stood.

Every number below is a measurement from this campaign with a commit and a job
behind it; nothing is projected, interpolated or recalled.

*Revised 2026-08-31 04:35 KST — launch +32.9 h, T = 2026-09-06T15:28:14+09:00,
155.0 h remaining.*
*(An earlier revision was stamped 05:25 / +33.7 h. That was an estimate of
elapsed time, not a clock reading; the login node read 04:27 at the time.
Corrected here and in LOG.md rather than silently.)*
* Compute 97.5 / 1,610 CPU-h (6.1%). Spend $86.17 / $280
(30.8%). Tokens 2.84M / 32M.*

> **Record correction (§6).** The file previously committed at this path, in
> commit `6f263f0`, contained **another replicate's report** (`rep09`) — an
> exhaustive-65-bar-screen strategy, a `cal_00` calibration set, and a finding
> that MakeGrid is unavailable, none of which are this campaign's. That commit's
> *message* correctly describes this campaign's report; its *content* does not.
> This is the second instance of cross-replicate file contamination here, after
> STATE.md on 2026-08-30 12:09. The present file replaces it in a new commit;
> per §6 nothing is amended or deleted. Nothing in this report derives from the
> contaminated file.

---

## 1. Claim

*(§7 requires this section to be at most three sentences; the supporting
detail that previously sat here has moved to §2.)*

**The best material found is `2021[Cu][sql]2[ASR]6` (db index 10985), with a
methane working capacity of 207.05 ± 0.21 cm³ STP/cm³ at 298 K between 5.8 and
65 bar** — absolute loading per §2, measured at §3 Claim grade (10,000 + 50,000
cycles, direct evaluation, three independent seeds), the uncertainty being
run-to-run scatter over those seeds. **I do not claim this is the database
maximum:** an empirical power law in `vf_neg` excludes 58% of the 9,115 distinct
frameworks outright and the surrogate's measured error distribution places no
unmeasured framework within 2σ of the leader, but the sweep that would have
converted those bounds into a measurement reached only 8 of its 124 structures
before the budget ended the campaign. **On the evidence actually in hand the
leader is very likely at or near the ceiling for this database and protocol —
"very likely" is the correct strength, and the claim is not that it was proven.**

## 2. Evidence inventory

### The Claim in detail

| seed | N(5.8 bar) | N(65 bar) | WC |
|---|---|---|---|
| 101 | 36.8647 | 243.674 | 206.809 |
| 102 | 36.7783 | 243.928 | 207.150 |
| 103 | 36.7328 | 243.930 | 207.197 |
| | | **mean** | **207.052** |

ρ = 358.3 kg/m³. All six tasks claim-grade: 10,000 initialization + 50,000
production cycles, **direct** mode (no energy grid), both pressures taken from
the same seed in each pair. Queue `04_claim`, complete 6/6.

**The ± is run-to-run, not a within-run statistic**: sd over the three
independent seeds is **0.212** (standard error of the mean 0.122, full range
206.809–207.197). That is what §7.1 asks for and it is deliberately not RASPA's
block estimate — the five blocks share one equilibrated starting configuration
and measure within-run sampling error rather than reproducibility. Here the two
happen to agree closely (block SEs 0.21–0.37 per point), which is worth
recording, but the quoted figure is the one measured for the purpose.

**On the ceiling.** Two independent instruments bound the unmeasured remainder:
a power law in `vf_neg` excluding **58%** of representatives outright (§3), and
the surrogate's own error distribution, which places no unmeasured framework
within 2σ of the leader and grants only 40 of 9,072 any chance of beating it
even at the largest residual ever observed in this database. Those 40 were a
list rather than an abstraction, so `07_cand` was built to simulate all of them
(widened to 124 for margin) — **the intended ceiling claim was not "probably
nothing beats it" but "every framework that could plausibly beat it was
simulated".** That sweep reached **8 of 124**, top return 187.8 against 207.05,
before the budget stopped the campaign; it is consistent with the leader
standing and it is not the verification it was designed to be.

All numbers trace to `results/*.tsv`, merged by `bin/wcjoin.py` into
`data/wc_all.csv`; jobs are recorded in `JOBS.md`.

| wave | what | protocol | status |
|---|---|---|---|
| `05_bench` | 15-structure stratified benchmark, grid **and** direct | floor, both P | **complete**, 30/30 |
| `02_cyc` | crossed grade × seed on one structure | floor + claim | **complete**, 2/2 |
| `03_claimtest` | claim-grade protocol proof | 10k + 50k | **complete**, 1/1 |
| `06_seed` | 3 structures × 3 fresh seeds, direct | floor, both P | **complete**, 18/18 |
| `07_top0` | top 24 by surrogate `wc_mf` | floor, grid, both P | **complete, 24/24** |
| `09_descr_uniq` | descriptors, all distinct representatives | — | **complete**, 8,892 |
| `04_claim` | leader × 3 seeds, **direct** | 10k + 50k | **complete, 6/6** — supplies §1 |
| `06_vfneg` | 5 `vf_neg` bins × 16, stratified (see §3 retraction) | floor, grid, both P | **72/80 returned**, test held |
| `07_cand` | every unmeasured framework that could plausibly beat the leader | floor, grid, both P | **8/124 — incomplete**, top 187.8 |
| `08_screen` | 1,000 TOP by `wc_mf` + 195 stratified TAIL | floor, grid, both P | 4/1,195 structures |
| `05_kadv` | 60 structures on predicted k | — | **retired unrun**, see §3 |

**The material.** `2021[Cu][sql]2[ASR]6`, db index 10985. Unit cell
**C₁₂₈Cu₄H₉₆N₁₆**, 244 atoms, a = b = 24.167 Å, c = 22.589 Å, α = 72.78°,
β = 107.22°, γ = 128.21°, V = 9,789 Å³. **Density 358.3 kg/m³** — against a
database median of 1,255, this is among the lightest frameworks present, and the
whole of its advantage is there. A copper framework of **sql** topology with
N-donor linkers (C:N = 8:1, consistent with a Cu paddlewheel and azolate/pyridyl
struts), filed under the as-synthesised solvent-removed code. Pore geometry:
largest cavity **11.56 Å**, largest percolating sphere **7.0 Å**, percolating;
helium void fraction 0.519, methane-probe void fraction 0.408, favourable-energy
volume fraction `vf_neg` 0.500. Henry constant φ = 6.88, well
distributed rather than concentrated in deep wells (`umin` = −1,467 K).

That combination is exactly what the physics of a *working* capacity rewards, and
it is worth stating because it is the mechanism behind the number rather than a
description of it: a large accessible volume delivers the 65-bar loading, while a
moderate binding strength leaves the pore mostly *empty* at 5.8 bar. The
campaign's own counter-example makes the point — 2014[Co][twt]3[ASR]1 has the
highest 65-bar uptake in the benchmark at 263.9 and reaches only WC 119.1,
because it still holds 144.8 at the discharge pressure. Note that under the
chargeless protocol of §3 the chemistry enters only through UFF Lennard-Jones
parameters; no electrostatic contribution to this result is modelled, and that is
a limitation of the protocol, not a property of the material.

**Coverage.** **122 distinct frameworks** carry a paired two-pressure RASPA
working capacity (15 benchmark, 24 `07_top0`, 72 `06_vfneg`, 8 `07_cand`,
4 `08_screen`, plus seed and cycle replicates); all **9,116 representatives** carry descriptors. (`data/descr_all.csv`
holds 9,163 OK rows, but 47 of those are non-representatives scored by the
earlier all-12,499 pass; anything ranked or counted is filtered to
`data/unique.csv` first.) Against the database's **9,115 distinct frameworks**
(see below) that is **0.4% simulated, 100% ranked**.

**The screening protocol is retrospectively validated at the top of the range.**
The leader's floor-grade grid number was 207.21 ± 2.50; its claim-grade direct
number, averaged over three seeds, is **207.05 ± 0.21**. Changing *both* the
cycle count (5×) and the energy treatment (grid → direct) moved the working
capacity by **−0.16 cm³/cm³** — a twelfth of the floor-grade block error, a
quarter of the floor-grade seed sigma, and **0.08% of the value**.
The 2.47× cheaper grid screen was therefore not buying speed at the cost of
accuracy, and the several hundred floor-grade screening numbers this campaign
rests on can be read at face value. That is a result about the method, and it
could only be established by paying for the expensive number once.

**Validation performed.**

- *Toolchain.* All three pinned UFF SHA-256 values verified 2026-08-29; RASPA
  2.0.37 confirmed. Absolute loading confirmed to be the parsed field, not
  excess (§2). Chargeless protocol enforced (`ChargeMethod None`,
  `UseChargesFromCIFFile no` — the CIFs carry DDEC6 charges that must not be
  used).
- *Database.* 12,499 CIFs are **9,115 distinct frameworks**; 3,383 (27.1%) are
  duplicates filed under a second CoRE-MOF solvent-treatment code. No two CIFs
  are byte-identical, so this required a cell+composition proxy followed by
  re-hashing all 6,732 members of multi-member groups on sorted (element,
  fractional coordinate) lists. `bin/dedupe.py` → `data/unique.csv`. A residual
  check (`bin/dupchk.py`, `bin/dupchk2.py`) found 43 further ASR/FSR pairs whose
  eight descriptors are identical; the CIFs show these are the *same framework*,
  differing in exactly one column — the **DDEC6 partial charge** — which the
  chargeless protocol of §3 ignores, making them byte-equivalent simulation
  inputs. `dedupe.py` had already merged 42 of the 43, so the corrected count is
  **9,115** and the leader is not double-counted.
- *Run-to-run reproducibility.* `06_seed`: pooled seed sd **0.60 cm³/cm³** over
  3 structures × 3 seeds. Independently, `02_cyc` gives 0.56 at floor grade.
  **At claim grade it is far tighter.** `04_claim` has returned N(5.8 bar) on the
  leader at two independent seeds: **36.8647** (block SE 0.299) and **36.7783**
  (0.222), a **seed spread of 0.086** — consistent with the 0.012 `02_cyc`
  measured at claim grade on a different structure, and an order of magnitude
  below the floor-grade sigma. Claim-grade runs reproduce; floor-grade runs
  scatter at ~0.6, and that difference is what the cycle count buys.
- *Grid and floor versus direct and claim, on the leader itself.* Floor-grade
  grid gives N(5.8) = 36.6735; claim-grade direct gives 36.821 (mean of two
  seeds). At 65 bar, floor-grade grid gives 243.885 against a claim-grade direct
  three-seed mean of 243.844. **On the working capacity the two protocols differ
  by 0.16 cm3/cm3, 0.08% of the value** (see §3). This is the campaign's only
  evidence at *claim* cycles for the grid/direct equivalence that the benchmark
  established at floor cycles alone, and it is what licenses every floor-grade
  grid number elsewhere in this report.
- *Cycle-count convergence.* `02_cyc` crossed grade against seed on
  2010[Eu][pcu]3[ASR]1 at 5.8 bar: claim-grade at two seeds agrees to **0.012**,
  floor-grade at the same two seeds differs by **0.563**. An earlier apparent
  0.65 floor-vs-claim shift was **seed scatter, not a convergence bias** —
  the confound is resolved and the item is closed.
- *Grid versus direct.* All 15 benchmark structures, both pressures, floor
  cycles: mean **+0.005**, median +0.017, mean absolute 0.549, range −1.19 …
  +1.60 cm³/cm³ — mean bias two orders of magnitude below the seed scatter.
  Grids are also **2.47× cheaper** (0.258 vs 0.639 CPU-h per structure at two
  pressures), which makes §4's 1.83 CPU-h/structure figure ~7× pessimistic for
  this database. This licenses grids for **screening only**; claim-grade runs
  are direct.
- *Pre-registered falsification test of the screening surrogate.* Before the
  data, on 2026-08-30 12:35, the condition was recorded: if all 24 structures in
  `07_top0` return below the then-best 186.0, the surrogate is not what the
  benchmark said and the screen design must be revisited. **24 of 24 returned;
  best 207.21, median 187.50, 15 of 24 above 186.0.** The condition was not met.
  Within the top-24 band itself (`wc_mf` 116-130) the rank correlation is
  **r = 0.883**, so the surrogate discriminates *inside* the narrow top band and
  not merely across the 25-186 range where it was calibrated - the top of the
  ranking is genuinely the top of the database.

## 3. Strategy account

**The frame.** The budget is ~7% of an exhaustive two-pressure pass, so the
field must be narrowed by something cheaper than GCMC. I built a mean-field
surrogate (`wc_mf`) from a tabulated CH₄–framework energy field and validated it
against RASPA before spending on its output: r = 0.984 over the benchmark, with
near-perfect rank agreement. It is a **ranking** device only — it is biased low
by ~0.6× and underestimates tight pores badly — so the screen is designed to
reach well below the top of its ranking.

**Two rankings that are actively wrong for this objective, and were rejected.**
Ranking on 65-bar uptake, or on the Henry constant φ, selects the wrong
materials: φ **anti**correlates with working capacity at −0.687, because strong
binding fills the pore before the 5.8-bar working window opens.
2014[Co][twt]3[ASR]1 has the benchmark's highest 65-bar uptake (263.9) and
reaches only WC 119.1, because it still holds 144.8 at 5.8 bar. Any strategy
screening on uptake alone would name the wrong winner.

**Instrument validation bought before instrument output.** `07_top0` (9 CPU-h,
the falsification test) was deliberately ordered *ahead of* the 97 CPU-h
descriptor pass whose ranking it tests. Spending 97 CPU-h extending an
unvalidated instrument before running the 9 CPU-h test of whether it works would
have been buying more output from something unknown.

**What the completed descriptor pass established.** The finished ranking over
9,116 representatives is far thinner at the top than an early 224-structure
preview suggested: 2 structures at `wc_mf` ≥ 129.6, 10 at ≥ 120, 29 at ≥ 116,
122 at ≥ 110, 587 at ≥ 90, against a median of 11.0. **`07_top0` therefore turns
out to have already measured 23 of the 29 structures at `wc_mf` ≥ 116 — very
nearly the entire top of the completed ranking.** The descriptor pass did not
reveal a better band; it established that there is no better band to reveal,
which is the more useful of the two outcomes for the ceiling half of the mandate.

**A calibration bias found and recorded.** The linear calibration
`WC = 1.4934·wc_mf + 19.78` (leave-one-out RMS 13.3) predicted 213 for the best
of `07_top0` and 193 for the weakest. All 24 residuals came back **negative**,
-4.7 to -14.6, mean **-8.9**, rms 9.3. The outcome sits inside the quoted ±13 interval, but a
residual set with no sign changes is bias, not scatter: the fit was made over
the full benchmark range (25–186) and a linear form runs out at the top of a
saturating relationship. Consequence: the surrogate's *absolute* predictions are
not used to decide where to stop screening; only its ranks are used.

**Abandoned: structural modification as a primary strategy.** 2,126 of 3,852
name-families already contain both an ASR and an FSR member at a median density
difference of 0 — the de-solvated framework a modification would build usually
*already exists in the database as a separate CIF* and needs only screening at
0.258 CPU-h. Kept available for a narrow evidence-driven case (an FSR structure
with no ASR sibling and a clearly solvent-blocked pore), not pursued generally.

**Abandoned: a hard-sphere volumetric ceiling bound.** `N(65) ≤ ρ_max · vf_ch4 ·
22414` is invalid on this database and fails large: 2016[Cd][pts]3[ION]1 has
`vf_ch4` = 0.0006 and still adsorbs 126.4 cm³/cm³, implying up to 340× liquid
methane density. A σ-contact filter would preferentially discard
ultramicroporous structures, which are not uniformly bad — that one still
reaches WC 47.6.

**The ceiling instrument, as it now stands: a *binned* `vf_neg` envelope.** The
usable analogue of accessible volume is `vf_neg`, the cell fraction where
U_CH4 < 0. Writing the implied methane density in that region as
`k = N(65) / (vf_neg * 22414 * rho_liq)`, a bound follows for every unsimulated
framework: `WC <= N(65) <= k_max * 590.1 * vf_neg`. Over the 38 measured
structures **k is not constant - it falls monotonically with `vf_neg`**, from 6.34
at `vf_neg` < 0.05 to 0.83 above 0.50, because the U < 0 criterion undercounts
accessible volume in tight pores and the undercount is worst when the pore is
smallest. Forcing one global k makes it cover the ultramicroporous outlier and
then multiply everything, and it excludes only **38.3%** of the database. A
bin-wise envelope excludes **77.1% at margin 1.0 and 56.7% at a safe 1.30
margin** (`bin/ceiling5.py`, over the 9,116 representatives).

**Better: k follows a power law, and the bound follows from it.** Fitting the
*per-structure* measurements rather than the bin maxima (which are order
statistics of samples as small as n = 1):

    k = 0.532 * vf_neg^(-0.607)      n = 38,  R^2 = 0.957

over two decades of `vf_neg`, with x1.16 typical scatter and a worst positive
residual of x1.52. Shifting the law up to cover every measured point gives
`k_env = 0.810 * vf_neg^(-0.607)`, hence for every unsimulated framework

    **WC <= N(65) <= 478.2 * vf_neg^0.393**

The exponent is the substance of it. The bound is **sub-linear in volume**: a
framework with half the favourable volume has 0.76 of the ceiling, not half. That
is the quantitative form of the failure that sank the hard-sphere bound — tight
pores adsorb far more than their accessible volume implies — and it says the
linear-in-volume assumption is wrong by a power of 0.6 in exactly the regime
where most of this database sits.

This form is preferred over the bin table for the final claim because it is
smooth (no empty bin inherits a neighbour's value through a rule I invented), it
carries a *measured* residual distribution rather than a safety margin chosen by
eye, and it is predictive. `bin/kfit.py`, `bin/ceiling6.py`, `bin/ceilfinal.py`.

**The operative bound is the refit below; the 38-structure form above is shown
for provenance and is superseded.** Refitted on all 106 structures now measured
(the 38 of the original fit plus 64 from `06_vfneg` and the screen):

    k     = 0.558 · vf_neg^(-0.563)      R² = 0.861
    k_env = 0.941 · vf_neg^(-0.563)      (covers all 106 points)
    ⇒  WC ≤ 555.3 · vf_neg^0.437

**Exclusion: 5,307 of 9,116 representatives — 58.2% — at safety factor 1.00**
(48.6% at 1.15, 39.6% at 1.30).

**That figure has fallen as evidence accumulated, from 62.1% on 38 structures to
58.2% on 106, and the direction is the honest one.** A larger sample finds larger
positive residuals, the envelope that covers them all widens, and the bound
loosens. Any exclusion number quoted from a small sample is therefore an
optimistic one; this is the second time in this campaign that a ceiling figure
has moved down when tested, and I expect the same again if it were tested
harder. The scatter around the law is ×1.25 rms with a worst case of ×1.69. Empty bins inherit k_max from the nearest populated
bin *below* them in `vf_neg`, never above, since inheriting from above would
understate the bound.

**Why this is not yet claimed.** The envelope is held up by almost nothing where
the database actually lives: `vf_neg` 0.05-0.10 has **1** measured structure
against 1,985 representatives, 0.10-0.20 has **2** against 2,127, and 0.20-0.30
has **1** against 907. 5,017 representatives - 55.0% of the database, and its
centre of mass, the median `vf_neg` being 0.080 - rest on four simulations. An
envelope maximum over n = 1 is not a maximum. `06_vfneg` (80 tasks, ~21 CPU-h) is
queued to populate those bins under a **pre-registered falsification condition**
(LOG 2026-08-31 04:35, committed with the queue at 0/20 and nothing returned):
every one of the 80 structures should return `k` below
`k_env = 0.810 * vf_neg^(-0.607)`, and refitting on all 118 points should leave
the exponent within ±0.08 of −0.607. **The envelope is not a bound if any
structure exceeds 1.30 × `k_env`, or if the refitted exponent leaves
[−0.69, −0.53]** — in which case `k` is not controlled by `vf_neg` alone and the
ceiling must be stated as a statistical statement, not a bound.

**RETRACTION (2026-08-31 09:40): this queue's "adversarial" arm is not
adversarial, and the claim that rested on it is withdrawn.** `bin/advcheck.py`
compared the two arms: the highest-`wc_mf` selection reaches `k/k_env` of at most
0.70 (median 0.50) while the *random* arm reaches **0.96 (median 0.70)** — the
control found higher k in both bins that have data, 27% higher at the maximum.
The reason is that `k ∝ vf_neg^-0.607`, so within a bin the dominant term is
where in the bin a structure sits, not how much it adsorbs; high-`wc_mf`
structures are the porous top edge and carry the *lowest* k. **I selected the
safe end of every bin and called it adversarial.** The falsification threshold
itself is unaffected — it is a test on measured k — but `06_vfneg` carries the
evidential weight of a **stratified random sample**, not of a sample built to
break the law, and this report previously claimed the latter.

**Nor is a genuinely adversarial sample constructible here.** The quantity to
stress is the residual from a law that already absorbs `vf_neg`; targeting large
residuals would mean predicting them, and a predictable residual would be folded
into the law. Stratified random sampling is therefore the correct design rather
than a fallback. A related attempt to select on *predicted* k failed for a
neighbouring reason: `k_pred` saturates at 0.90–0.95 across every bin because the
mean-field model never predicts super-liquid packing, while measured k reaches
6.34 — the surrogate cannot see the effect that produces high k, because its own
underestimation in tight pores *is* that effect. That sample is still queued
(`05_kadv`, 60 structures, ~13 CPU-h) but as `vf_neg`-stratified coverage, not
as a test.

The original description, retained for the record: the sample was intended to be
**adversarial**, on the reasoning that within each bin the
highest-`wc_mf` structures, because the bound needs a *maximum* of k and a random
sample would estimate the typical k and underestimate the maximum - the one
number a bound cannot afford to get wrong. Six random draws per bin check that
the adversarial arm is finding the top of its bin and not a correlated corner.

**The ceiling's second leg: the surrogate's own error distribution.**
`bin/ceilstat.py`. Over the 71 structures measured, WC = 1.4139·`wc_mf` + 22.89
with residual sd 10.23 and residuals spanning −23.9 … +24.1. Applied to the
9,072 unmeasured representatives, **not one is within 2σ of 207.21**; 85 are
within 3σ. Because a Gaussian tail is the wrong model for a bounded physical
quantity, the statement that matters uses the **largest residual ever observed
in this database (+24.1)**: granting every unmeasured framework that best-ever
surprise, **40 of 9,072 (0.44%) reach the leader**. This leg bounds WC from the
surrogate's empirical error; the power law bounds it from pore geometry. They
share measurements but not reasoning, and they agree.

**And so the ceiling need not stay an estimate.** At 0.22 CPU-h per structure a
40-framework list is affordable outright. `bin/mkcand.py` selects every
unmeasured representative with `pred + 1.5 × max_residual ≥ 207.21` — the 1.5×
margin is deliberate insurance, because a top-heavy measured sample understates
its own upper tail, and widening 40 → **124 structures (~27 CPU-h)** costs
little against a compute budget 6.4% used. Queued as `07_cand`. **If all 124
return below 207.21, the ceiling claim becomes "every framework that could
plausibly beat the leader under a margined empirical error model was simulated,
and none did."** It would remain exhaustive *within the model*, not absolutely:
a framework whose surrogate value is not merely unlucky but wrong could sit
outside the set, and the guards against that are the random arm of `06_vfneg`
and the TAIL arm of `08_screen`, neither complete.

**Queue order is a decision, and one I declined to change.** With three workers
and everything else queued, the order in which the remaining science runs is the
plan: `04_claim` → `06_vfneg` → `07_cand` → `08_screen`. `07_cand` answers this
report's second question most directly and is the one most likely to finish
usefully; `06_vfneg` supports the ceiling only through a fitted law. I
nevertheless left `06_vfneg` first, because it is the **pre-registered
falsification test** and `07_cand` is the sweep most likely to *confirm* the
leader. Demoting the test that can refute me in favour of the one that can
flatter me, at the moment capacity became scarce, is the shape of a biased
record — and the availability of a respectable scientific justification for it
makes it more dangerous, not less. If `07_cand` does not finish, this report says
so and the ceiling rests on the law plus the statistical argument.

`05_kadv` (60 structures) was built and then **retired unrun**: it was meant to
repair the sampling error above by selecting on predicted k, and it cannot,
because `k_pred` saturates at 0.90–0.95 across every bin while measured k reaches
6.34. Selecting on a near-constant is selecting at random, and the coverage it
would have added is already supplied by `06_vfneg`'s random arm.

**Running now.** `08_screen`: 1,000 TOP by `wc_mf` (range 71.5–118.3, i.e.
everything *below* the band already measured) interleaved with 195 TAIL
structures stratified over `wc_mf` 0–70.4, one TAIL task every six TOP tasks.
The TAIL arm is not a hedge — it is the only **unbiased** WC-vs-`wc_mf`
calibration sample the campaign will have, because a top-N sample is selected on
the predictor, and every statement about unsimulated frameworks rests on that
residual distribution. It is interleaved rather than appended precisely so that
a queue truncated by the deadline still carries it.

## 4. Uncertainty and limitations

- **The ± 0.21 is statistical only, and it is the smallest of this claim's
  uncertainties.** It is run-to-run reproducibility of the pinned protocol —
  what a repeat of *this* calculation would scatter by. It says nothing about
  whether the protocol predicts what a laboratory would measure. The systematic
  terms are not quantifiable from inside §3 and are individually larger:
  **UFF Lennard-Jones parameters** are generic, assigned by element rather than
  fitted to methane adsorption; **the framework is rigid**, so no lattice
  breathing or linker rotation contributes; **the protocol is chargeless** by
  §3, so a framework whose CIF carries DDEC6 charges is simulated without any
  electrostatic contribution — for a Cu paddlewheel with N-donor linkers that is
  a real omission, though methane's negligible dipole makes it a smaller one than
  it would be for CO₂; **the cutoff is 12.8 Å with tail corrections off and
  potentials unshifted**, which §3 pins deliberately and which shifts absolute
  uptake relative to a tail-corrected calculation. Published comparisons of
  generic-force-field GCMC against methane isotherm measurements typically
  differ by 10–20%. **A defensible reading of this claim is therefore
  "207.05 ± 0.21 under the pinned protocol, and 207 ± 30 as a prediction of
  physical reality"** — and the first number is the one the mandate asks for,
  since §2 defines the target by the protocol rather than by experiment.
- **Comparability, not absolute accuracy, is what the protocol buys.** Every
  number in this campaign was produced under identical settings, so the ranking
  and the ceiling argument are internally consistent even where the absolute
  scale is uncertain. That is the right property for a "which material is best"
  question and the wrong one for a "what will this deliver in a tank" question,
  and only the first was asked.
- **0.4% of distinct frameworks have been simulated.** Everything said about the
  other 99.6% currently rests on a surrogate ranking whose absolute calibration
  is known to be biased at the top. This is the largest soft spot in the report.
- **No ceiling position is claimed.** The two candidate instruments are a
  `vf_neg`-based physical bound and a statistical argument from the surrogate's
  residual distribution over the unscreened remainder. The first is not yet
  established, and if it fails the ceiling argument becomes explicitly
  statistical and must be stated as such — a bound on what is *likely*, not a
  bound.
- **A defect in my own analysis code, found and fixed on the record.** I first
  read `07_top0` as 23 of 24 with one null point. It was 24 of 24: the task had
  been executed more than once, one repeat returned `status=OK` with
  `load_vv=nan`, and `bin/wcjoin.py` averaged it into the good value. Patched to
  drop non-finite rows. Established while checking, and load-bearing: the repeats
  are **deterministic re-executions of the same (structure, pressure, seed)**, not
  independent samples - so duplicate counts must never be read as replication.
- **The ceiling exclusion figures above are provisional in the direction that
  matters.** They rest on a k_max taken over a 38-structure sample that is
  top-heavy by construction. If `06_vfneg` finds a higher k in any sparse bin, the
  exclusion percentage falls; it cannot rise. The figures are therefore an
  optimistic estimate of exclusion power, not a conservative one, and are labelled
  as such until that queue returns.
- **A duplicate-detection gap.** `2021[Cu][sql]2[FSR]6` carries descriptors
  identical to the leader `2021[Cu][sql]2[ASR]6` to every printed digit; the
  same holds for the `[V][srs]` and `[Zn][ith]` pairs. The dedupe counts them as
  distinct because their atom lists differ. This does not affect the leader's
  measured number; it affects the denominator of any ceiling claim, so the
  9,116 figure may be slightly high. **RESOLVED 2026-08-31: it was high by one.**
  The 43 identical ASR/FSR pairs differ only in DDEC6 charges, which this
  protocol does not read; `dedupe.py` had already merged 42 of them, and only
  `2020[CuNb][sql]2[ASR]3` (`wc_mf` 5.3, far from the top band) survived as a
  double count. Corrected denominator **9,115**; the leader is unaffected.
- **Capacity, not the CPU-h budget, is the operative constraint.** All 16
  replicates submit as one UNIX user and share the mjs per-class core caps
  (ax 32 / aa 38 / amd 80 / ac 102), so my 12 worker slots over the remaining
  wall time are the real limit, not the 1,610 CPU-h cap of which 6.1% is spent.
- Excess versus absolute: absolute is reported throughout, per §2. With no helium
  void fraction pinned, RASPA reports excess == absolute here in any case.
- **The binding constraint is session spend, not the deadline or compute.** At
  10:40 spend stands at **64.1%** against **7.9% of compute** and 149 h of
  campaign remaining. The burn is a function of how I work, not of the science:
  it measured ~$33/session-hour while I was reading rankings and audit tables
  into the session, and ~$5–9/hour after switching to lean turns that print two
  lines. Roughly 10 session-hours remain at the current rate. The 65-bar claim-grade halves are ~9 h of
  wall clock away and **I may not be awake to collect them**; the cluster keeps
  working, but results landing after my last turn cannot reach this file. Every
  finding above is therefore written in as it is established rather than saved
  for an ending that may not come. If this report ends here, §1's number is
  floor-grade and says so.

## 5. Self-assessment

**Confidence in the leader as a measurement: high.** 207.2 comes from a
validated protocol, with grid mode shown unbiased against direct on 15
structures and floor-grade reproducibility measured at 0.60 cm³/cm³ by two
independent designs. **Confidence in it as the database maximum: moderate, and
better founded than it was.** It is no longer a lucky draw: it is the top of a
completed mean-field ranking over all 9,116 representatives, and the ranking's
top 29 have been simulated nearly exhaustively.

**The pre-registered ceiling test has held, at 64 of 80 structures returned.**
Scored against the *frozen* envelope constants of commit `ca9d5f1` — not against
a curve refitted to include the test data, which would be circular — **zero
structures exceed the 1.30 × `k_env` threshold**, the worst being 0.96
(`2021[Cu][sql]2[ASR]3`, a sibling of the leader in the same Cu-sql family), and
the refitted exponent is **−0.563**, inside the recorded [−0.69, −0.53]. The
worst ratio has climbed 0.86 → 0.91 → 0.96 as the sample grew, which is what a
maximum over a growing sample does; nothing approaches the threshold. R² has
fallen 0.957 → 0.861 over the same span, the honest cost of testing a law outside
the band that produced it.

**On the ceiling as finally filed.** The pre-registered test held: at 72 of 80
structures returned, scored against the frozen envelope, **no structure exceeded
the 1.30 threshold** and the refitted exponent stayed inside the recorded window.
The exhaustive candidate sweep `07_cand` reached **8 of 124** before the budget
ran down, and its highest return was **187.8** against the leader's 207.05 —
consistent with the leader standing, but 8 of 124 is not the exhaustive
verification the design intended, and the claim below does not rest on it.

**Confidence in the eventual ceiling argument: moderate, and revised downward
today.** It has an empirical law with R² = 0.957 over two decades of `vf_neg`
that excludes 58% of the database as refitted on all 106 measured structures,
and an independent statistical leg
that puts no unmeasured framework within 2σ of the leader. But it is an
**empirical** law, not a derivation from first principles; and the sampling I
described as adversarial was not, so the law is being tested by stratified random
sampling with the evidential weight that implies. The strongest thing the ceiling
argument has is not either instrument but `07_cand`: the exhaustive sweep of
every framework that could plausibly beat the leader under a margined error
model. If that completes and none beats 207.21, the claim rests on a measurement
rather than on a fit.

**Two of my own instruments have now failed a check I ran on them** — the
hard-sphere volumetric bound, caught before it was spent on, and the adversarial
sampling, caught only because I had built a random control and thought to compare
the arms. The control is what saved the second one. I take that as the main
methodological lesson of this campaign: the design that includes a way to catch
its own error is worth more than the design that is merely more clever.

**What would change my mind.** (a) A `08_screen` TOP-arm structure at `wc_mf`
well below 116 returning above 207 — that would show the surrogate's rank order
fails outside the band where it was tested, and would put the maximum somewhere
the ranking cannot find. (b) A TAIL-arm structure returning far above its
predicted value, which would break the residual distribution the ceiling
argument needs and force the ceiling to be stated much more weakly. (c) A
claim-grade direct result on the leader differing from 207.2 by more than ~2 —
that would mean grid mode or floor cycles carry a bias at the top of the range
that the benchmark did not detect, and every screening number would have to be
re-read. (d) A `06_vfneg` structure in a sparse bin with k far above that bin's
current k_max, which would flatten the envelope back toward the useless global
constant and force the ceiling to be stated statistically rather than as a bound.
