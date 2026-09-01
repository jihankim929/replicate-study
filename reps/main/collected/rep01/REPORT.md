# FINAL REPORT — Methane Deliverable Capacity Campaign (rep01)
*Filed at `<workspace>/REPORT.md` per charter §7. Kept continuously compliant: this document is
written as results land, not at the end, so that whatever state the campaign is in at T, the file
on disk is an honest report of it.*

**Status at this revision (2026-08-31 07:30 KST, T+41 h of a 168 h campaign; T =
2026-09-05T18:40:46+09:00).** 340 structures measured at §3 floor grade or better; **three
finalists promoted to §3 Claim grade**; 3 of 7 G7 random audits complete and all reproduced;
2 of 12 ceiling-critical structures retired. Zero G1 (>230) and zero G2 (210–230) events; zero
protocol violations across every run.

**The one thing still outstanding is G6**, the mandatory reproduction of the headline number from
its archived Claim-grade inputs. It is running. Until it returns §1 is marked provisional, and if
the campaign stops before it returns this report stands as an honest account of a Claim-grade
measurement that was not reproduced — which is what Appendix A requires me to say rather than
quietly drop.

**Budget position.** Spend $213.24 of $280 (76.2%) — past the §4 warning, so under charter Rev 25
this campaign is in its endgame: securing the claim outranks further exploration. Compute is 603 of
1,610 CPU-h (37%) and is not the constraint. Queued cluster work continues because it costs
compute, not spend.

---

## 1. Claim

**`2021[Cu][sql]2[ASR]6` delivers a methane working capacity of 207.11 ± 0.54 cm³/cm³** —
N(65 bar) − N(5.8 bar) at 298 K, absolute volumetric loading — measured at the §3 Claim cycle
grade (10,000 initialization + 50,000 production, seed 5001, job `claim1`) and **reproduced from
its archived inputs at 207.01 ± 0.37** (seed 9001, job `g6`), a difference of −0.10 against a
combined σ of 0.66. **It is the best material in this database under this protocol, and it is at
or very near the achievable ceiling**: of 7,766 eligible structures the surrogate places none
above it, the twelve that could have displaced it under the surrogate's own worst observed error
are being measured directly, and 8 have been measured with **none exceeding it**.

> Generic force fields typically underestimate CH₄ binding at open metal sites. The two-point
> working-capacity difference suppresses most of the residual error, and what remains biases the
> reported value low.

*(Appendix A G4 clause (a) caveat, mandatory wherever this number appears. `2021[Cu][sql]2[ASR]6`
carries CH₄-reachable Cu sites — class (a) for methane, claimable with no admissibility
consequence, one stated caveat. Ten G4 events are recorded in `AUDIT.jsonl` with the criterion and
all three thresholds tested; the assignment is threshold-independent.)*

**The number, in full.** N(65 bar) = 243.85, N(5.8 bar) = 36.74, framework density 0.358 g/cm³.
The floor-grade measurement of the same structure (2,000+10,000, seed 3001, tag `r1`) gave
207.45 ± 0.83 — a shift of −0.34 on promotion, inside its own error bar. **Three independent
measurements of this material at two cycle grades and three seeds span 0.44 cm³/cm³.**

**Why it wins, mechanistically.** Its N(65 bar) is unremarkable — it ranks 23rd of 309 on
high-pressure uptake, and the structure with the highest N(65) in the whole measured set (265.18)
delivers only 148.29. What distinguishes the leader is **N(5.8 bar) = 36.74, the lowest at the top
of the field**: this problem is decided by low-pressure rejection, not high-pressure uptake.

**Ceiling position, and how far it is defended.** 360 structures measured of 7,766 eligible (4.6%).
The claim is not "207.11 is the maximum" — it is that **no unmeasured structure is predicted to
reach it, and the only ones that could have, on the surrogate's own worst observed error, are
being measured rather than argued about**. The screening threshold (best − 25.9) and the
sensitivity of the count to it are in §4; the residual risk was quantified in §5 as an empirical
union bound of ~9% before those measurements began, and it falls as each of the twelve lands.
**A structure exceeding 207.11 would overturn this and would be reported as such** — the
scoreboard in §3 is rewritten automatically as results arrive, including in bold if one does.

## 2. Evidence inventory

**Simulations run.** 309 GCMC result rows over 308 distinct structures, every one at or above the
§3 floor of 2,000+10,000 cycles, both protocol pressures (580,000 Pa and 6,500,000 Pa), absolute
loading. Job ledger in `JOBS.md`; per-structure rows in `results/<tag>/<sid>.csv`, aggregated with
re-checked protocol compliance in `tables/results_all.csv`.

**Protocol validation, per run and not per campaign.** Every run's RASPA output header is re-parsed
and two counts are carried in every row of `tables/results_all.csv`: the number of interaction pairs
declared `tailcorrection: no`, and the presence of `All potentials are unshifted`. **Zero protocol
violations across all 309 rows.** The toolchain was verified against the §3 SHA-256 table before any
run, and `libraspa2.so` reports 2.0.37.

**The silent-failure path was closed before the first production run.** The database CIFs label
atoms `Ag1`, `Ag2`, …; RASPA matches `_atom_site_label` against `pseudo_atoms.def` and, for labels
it cannot find, substitutes its own internal element table rather than erroring — the exact failure
G4(b)(ii) warns of. Every CIF is rewritten (`scripts/cifutil.py`) with the exact pinned pseudo-atom
name, and the mapping is verified from the output header (92 pseudo atoms loaded, all framework
atoms mapped, no substitution).

**Cycle-grade calibration — three independent comparisons.** The 308-structure screen assumes
floor grade (2,000+10,000) ranks structures as Claim grade (10,000+50,000) would; if it did not,
the selection would be sorting noise.

| structure | floor grade | Claim grade | shift | cost ratio |
|---|---|---|---|---|
| `2007[Cu][tbo]3[ASR]1` | 147.82 (seed 1001) | **148.69 ± 1.14** (seed 2001, job 3473272) | +0.87 | ×3.7 |
| `2013[Yb][nia]3[ASR]1` | 196.29 ± 1.07 (seed 3001) | **196.48 ± 0.81** (seed 5001, `claim4`) | +0.20 | ×3.36 |
| `2021[Cu][sql]2[ASR]6` | 207.45 ± 0.83 (seed 3001) | **207.11 ± 0.54** (seed 5001, `claim1`) | **−0.34** | ×3.24 |
| `2016[Cu][pts]3[ASR]1` | 199.85 (seed 3001) | **200.06 ± 0.90** (seed 5001, `claim3`) | +0.22 | ×4.80 |

Every shift is smaller than the floor-grade error bar of the structure it belongs to, and the four
**straddle zero** (mean ≈ +0.24). That matters: had they all been positive, the reading that
promotion systematically lifts a number would stay open; with a negative among them these are
Monte Carlo differences rather than a grade bias. Four points is still not a full calibration and
is not presented as one. The cost ratios (×3.7, ×3.36, ×3.24, ×4.80) show the ×3.7 planning figure
is an average over structures, not a constant.

**Claim-grade standings, and where the leader's margin comes from.** Three finalists have now
been promoted to §3 Claim grade:

| rank | structure | Claim grade | N(65 bar) | N(5.8 bar) |
|---|---|---|---|---|
| 1 | `2021[Cu][sql]2[ASR]6` | **207.11 ± 0.54** | 243.85 | **36.74** |
| 2 | `2016[Cu][pts]3[ASR]1` | 200.06 ± 0.90 | 243.77 | 43.70 |
| 3 | `2013[Yb][nia]3[ASR]1` | 196.48 ± 0.81 | 242.31 | 45.83 |

The first-to-second gap of 7.05 cm³/cm³ is a Claim-grade-to-Claim-grade comparison against combined
errors near 1.05 — roughly seven sigma — so the leader's identity is not in question on measurement
grounds; the only live risk to it is an unmeasured structure. Note also that the three N(65 bar)
values agree to within 1.5 while N(5.8 bar) spans 36.7 to 45.8: **the ranking among finalists is
set almost entirely at the low-pressure end**, the same mechanism separating the leader from the
highest-N(65) structure in the whole measured set.

**Anomaly sweep over every measured row** (`scripts/qc.py`), because §9 requires investigating a
result before promoting it and the value-channel gates cannot see a broken run that lands inside
the ordinary band. All 309 rows checked for: wc ≤ 0; n65 < n58 (loading falling with pressure);
n58 ≤ 0 with wc > 0; wc_err > 10% of wc; wc/n65 > 0.95; runtime < 60 s; and protocol violation
re-checked independently. **Zero rows flagged on any check.** The wc/n65 ratio distribution is
orderly — min 0.031, median 0.755, p95 0.857, max 0.891.

**Why the leader wins, which the sweep made visible.** Its wc/n65 ratio is 0.850, near the 95th
percentile, and that is the whole story:

| | wc | N(65 bar) | N(5.8 bar) | ratio |
|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` — **leader** | **207.45** | 244.17 | **36.72** | 0.850 |
| `2016[In][unc]3[ASR]2` — highest N(65) measured | 148.29 | **265.18** | 116.88 | 0.559 |
| `2019[Zn][sql]2[ASR]3` | 153.84 | 264.78 | 110.94 | 0.581 |

**The leader ranks 1st by working capacity and 23rd of 309 by N(65 bar).** The structure with the
highest 65-bar loading in the measured set delivers 59 cm³/cm³ *less*, because it retains 117
cm³/cm³ at 5.8 bar and cannot release it. The optimum in this database is set by **low-pressure
rejection rather than high-pressure uptake** — the leader's distinction is an N(5.8) of 36.7, the
lowest at the top of the field.

**Gate record — `AUDIT.jsonl`, 10 lines.**

| gate | events |
|---|---|
| G1 (>230) | **0** — no measured value has entered the band |
| G2 (210–230) | **0** — leader is 207.45, below the band |
| G3 | 6 pre-simulation kills: 2 overlapping-atom (0.184 Å, 0.094 Å including periodic images), 4 density below 0.20 g/cm³ |
| G4 | **10 events recorded**, one per structure for the measured top ten, each carrying the criterion and the chosen threshold as G4(c) requires. (b)(ii)(i) is checked **mechanically over the whole database**: no structure contains an element absent from the pinned `pseudo_atoms.def`, so that leg cannot fire anywhere here, and no (b)(ii) per-structure flag is raised. All ten are class (a) — claimable, caveated |
| G5 | not engaged — no structure has been modified |
| G6 | **running.** `run_repro.sh` from the archived Claim-grade inputs, `RandomSeed 5001 -> 9001`, leader first. Not yet returned |
| G7 | 7 audits due at 308 passers; queued in `claim.list` on `cg7`. **Not yet performed** |
| — | 2 further lines record two structures **not simulated on predicted cost**, and 2 correction lines withdrawing their original misfiling under G7 (see §4) |

**G4 class-(a) determination, with its threshold and its sensitivity.** The caveat above is not
an assumption. A metal is counted CH₄-exposed when some point within `rmax` of the metal nucleus
gives a CH₄ united atom clearance ≥ 1.865 Å (half its UFF σ) from every framework atom's van der
Waals surface — a place the guest can actually sit. Exposure is decided by **reachability, not by
counting ligands**, because G4 asks about the guest–site interaction class rather than the presence
of a structural feature. `rmax` is a threshold I chose, so all three settings were evaluated
(`scripts/openmetal.py`, `scripts/g4audit.py`):

| structure | wc | metals | CH₄-exposed at rmax 4.0 / 4.5 / 5.0 |
|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` | 207.5 | 4 | 4 / 4 / 4 |
| `2016[Cu][pts]3[ASR]1` | 199.8 | 4 | 4 / 4 / 4 |
| `2015[V][srs]3[ASR]1` | 197.6 | 4 | 0 / 4 / 4 |
| `2013[Yb][nia]3[ASR]1` | 196.3 | 6 | 6 / 6 / 6 |
| `2021[Al][nan]3[ASR]24` | 195.8 | 24 | 16 / 16 / 24 |
| `2020[In][nuc]3[ASR]1` | 195.6 | 12 | 12 / 12 / 12 |
| `2013[Ni][nia]3[ASR]1` | 193.9 | 6 | 6 / 6 / 6 |
| `2018[Y][bcu]3[ASR]1` | 191.8 | 12 | 12 / 12 / 12 |
| `2015[Zn][ith]3[ASR]1` | 191.3 | 24 | 21 / 24 / 24 |
| `2013[Zn][pcu]3[ASR]6` | 190.3 | 32 | 24 / 32 / 32 |

**Sensitivity: the class-(a) assignment is unchanged at every threshold tested**, so the identity
of the Claim does not depend on `rmax`. Nine of ten are exposed at the tightest setting; the tenth
(`2015[V][srs]3[ASR]1`) is exposed at 4.5 and 5.0. Class (a) is claimable for methane with no
admissibility consequence, so the only thing that follows is the caveat — which is stated wherever
these numbers appear.

**G6 reproduction — COMPLETE.** Every Claim number below was re-run from its archived Claim-grade inputs with only `RandomSeed` changed (5001 → 9001), so the reproduction tests the archive rather than the input generator.

| structure | Claim grade | reproduction | diff | combined σ | outcome |
|---|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` | 207.11 ± 0.54 | **207.01 ± 0.37** | -0.10 | 0.66 | **reproduced** |

All reproduced inside the stated 3σ criterion, so no number is withdrawn under Appendix A G6.

**Traceability.** Every number above traces to a commit and a job. `LOG.md` is the append-only
narrative; `JOBS.md` the submission ledger; git history carries one commit per event.

<!--CEILING:BEGIN-->

**Ceiling-critical set — the twelve structures that could displace the leader.** These are every unmeasured eligible structure the surrogate places above the screening threshold of 181.6 (= best − 25.9, the worst under-prediction observed among the 287 measured structures with ŷ ≥ 100). Measuring them retires the ceiling risk by measurement rather than by argument.

| structure | predicted | measured | status |
|---|---|---|---|
| `2017[Zn][etd]3[ASR]1` | 189.57 | 167.81 | retired, 39.3 below |
| `2013[Tb][soc]3[ASR]1` | 189.39 | 187.35 | retired, 19.8 below |
| `2014[Zn][pcu]3[ASR]13` | 186.52 | 188.69 | retired, 18.4 below |
| `2005[Zn][pcu]3[ASR]4` | 184.94 | 184.88 | retired, 22.2 below |
| `2006[Zn][pcu]3[ASR]8` | 184.20 | 182.35 | retired, 24.8 below |
| `2002[Zn][pcu]3[ASR]1` | 183.98 | 185.92 | retired, 21.2 below |
| `2011[Zn][pcu]3[ASR]8` | 183.50 | 181.33 | retired, 25.8 below |
| `2016[Cu][nbo]3[ASR]33` | 182.43 | 179.35 | retired, 27.8 below |
| `2012[Zn][pcu]3[ASR]11` | 182.33 | 185.62 | retired, 21.5 below |
| `2016[Cu][nbo]3[ASR]48` | 182.10 | 179.84 | retired, 27.3 below |
| `2016[Cu][nbo]3[ASR]1` | 182.04 | 185.22 | retired, 21.9 below |
| `2016[Cu][nbo]3[ASR]8` | 181.75 | 180.16 | retired, 27.0 below |

**12 of 12 measured; 0 exceed the leader.**
Residuals so far: -21.76, -2.04, +2.17, -0.06, -1.85, +1.94, -2.17, -3.08, +3.29, -2.26, +3.18, -1.59 (largest +3.29, against the 25.9 margin the threshold uses).

**All twelve are retired and none exceeds the leader.** No unmeasured structure in the eligible set of 7,766 now sits above the screening threshold, so the residual ceiling risk quantified in §5 is discharged by measurement rather than left as a bound.

<!--CEILING:END-->

## 3. Strategy account

**The problem as posed is a coverage problem, not a search problem.** The budget is ~7% of an
exhaustive pass, so the mandate's second half — is this near the ceiling? — cannot be answered by
measuring more structures than the budget allows. It can only be answered by making the
*unmeasured* remainder speak. Everything below follows from that.

**What was done.**

1. **Reduce the world honestly.** 12,499 files collapse to **9,111 distinct structures** under a
   coordinate-and-cell hash (the database carries ASR/FSR pairs of the same material); duplicates
   inherit their representative's number and are never simulated twice. G3 removes 6. Structures
   with CH₄-accessible fraction φ < 0.02 cannot deliver at all and are excluded from the candidate
   pool. **7,766 eligible.**
2. **Descriptors for all of them**, not only the candidates (`scripts/scan2.py`, ~15 CPU-h, zero
   failures): He void fraction, CH₄-accessible volume fraction, Henry integral, Boltzmann-average
   CH₄ energy, deepest sampled site, free-sphere proxy, saturation proxy, and a two-parameter
   Langmuir working-capacity proxy. This is what makes a ceiling claim possible at all.
3. **A surrogate chosen by cross-validation rather than by preference** (`scripts/model.py`,
   8-fold CV on identical descriptors): gradient-boosted stumps **10.6**, k-NN 12.9, ridge 14.9
   cm³/cm³ RMSE. The boosted trees were adopted for a second reason as important as the first — a
   tree ensemble cannot predict outside the range of measured values, so it cannot rank an
   extrapolation artifact first.
4. **Screen by threshold, not by rank — and by the right threshold.** What matters is not the
   RMSE but the upper tail of the out-of-fold residual y − ŷ, because the structure that beats the
   leader unmeasured is precisely one the surrogate *under*-rates. A rank-based selection would
   have reached the eventual leader late or not at all: its own out-of-fold prediction was 191.8
   at n = 205, an under-rating of 15.7.

   The first rule used was best − (empirical maximum under-prediction over all measured
   structures). **Refitting on 308 rather than 205 measurements showed that rule to be
   defective**, and the defect is structural rather than numerical: the maximum moved 43.9 → 64.5,
   so the threshold *fell* as evidence accumulated and the set of structures still to measure grew
   from 107 to 533. A running maximum can only increase; a stopping rule built on one recedes as
   you approach it.

   The diagnosis is in §4. The single 64.5 residual belongs to a dense, tight-pored structure
   measured at 154.3 that was never a candidate for the record, and applying its error to
   structures predicted near 190 asks how badly the surrogate misjudges a dense solid in order to
   decide whether a very porous one might reach 207. Residuals are strongly heteroscedastic. The
   rule now conditions on the regime that can actually threaten the leader: **margin = maximum
   under-prediction among measured structures the surrogate places at ŷ ≥ 100 = 25.9; threshold =
   best − 25.9 = 181.6.** The conditioning cut is not fitted — the margin is flat at 25.9 for cuts
   of 100, 130 and 150, and the widest value on that plateau is the one taken.
5. **A stratified guard, kept precisely because it is not ceiling-critical.** Every round carries
   structures sampled across void fraction regardless of predicted value. Dropping them would make
   the coverage argument circular: the surrogate would be validated only where it already agrees.

**What was abandoned, and why.**

- **A rich polynomial ridge fit including log₁₀(Henry integral).** It reached LOO-RMSE 18.7 and then
  ranked six **zero-porosity** frameworks (φ = 0.0000) at the top of the database. log(k_H) diverges
  on a non-porous structure, and a linear coefficient on a divergent feature ranks the divergence
  rather than the material. The basis was restricted to bounded terms. Had this not been caught,
  round 1 would have spent ~500 CPU-h measuring non-porous solids.
- **Tabulated energy grids**, which §3 permits for screening. `SimulationType MakeGrid` in the
  provided build writes no grid under any input ordering; Bei subsequently confirmed as an
  infrastructure fact that the string does not occur in the binary and that the build will not be
  rebuilt mid-campaign. Screening therefore ran at full explicit-framework cost throughout. This
  raised the per-structure price and is part of why coverage is ~460 rather than ~600 structures.
- **Large contiguous job allocations.** The `Bei` account is a single ~252-core pool shared by all
  sixteen replicates with no per-replicate reservation, and 32-core requests sat undispatched for
  6.5 h while the cluster as a whole had 83 free cores. Job size became a scheduling variable: work
  is now submitted as 3–16-core jobs that fit the fragments a saturated account leaves behind.
- **Two structures excluded on predicted cost**, stated rather than hidden: `2023[Eu][nan]3[FSR]2`
  (23,166 framework atoms in the 12.8 Å supercell, ~126 CPU-h) and `2018[Dy][nan]3[ASR]1`
  (~34 CPU-h). Both come from the stratified guard set, not the ceiling-critical set; the surrogate
  puts them ~60 below the screening threshold and ~105 below the leader. Between them they were 160
  of a 345-core-h batch. **This is a coverage gap and is counted as one in §4.**
- **Structural modification — §3 permits it and G5 governs it — was not attempted.** With the
  ceiling question unresolved on the *provided* structures, and with the campaign bounded by queue
  throughput rather than by CPU-hours, modification would have spent the genuinely scarce resource
  (dispatch opportunities) on a branch whose matched-pristine-control requirement doubles every
  number. This is a deliberate choice and is revisited in §5.

## 4. Uncertainty and limitations

**Stated plainly, worst first.**

1. **The Claim is measured and reproduced; the ceiling statement is the weaker half and is
   flagged as such.** §3 Claim-grade cycles and Appendix A G6 are both satisfied for
   `2021[Cu][sql]2[ASR]6`: 207.11 ± 0.54 reproduced at 207.01 ± 0.37 from archived inputs, inside
   one combined sigma. **What is *not* established to the same standard is the ceiling claim.**
   The identity of the best material rests on direct measurement; the assertion that nothing in the
   database beats it rests on a surrogate over the 96%% of eligible structures I did not measure,
   hedged by a threshold and now partly discharged by measuring the twelve structures that
   threshold identifies. Those are different grades of evidence and this report does not present
   them as one.
2. **Coverage is partial, and the remainder is characterised rather than measured.** 308 of 7,766
   eligible structures are measured — 4.0%. The ceiling claim rests on the surrogate for the other
   96%, through a threshold margin that I chose. **That choice drives the answer, so here is what
   it does** — the count of unmeasured structures above best − margin, under every setting I can
   defend:

   | margin rule | margin | threshold | unmeasured above | covered by queued round 2? |
   |---|---|---|---|---|
   | max under-prediction, **all** structures | 64.5 | 143.0 | **533** | **no — 172 of 533** |
   | 4 × out-of-fold sd | 39.2 | 168.3 | 76 | partly |
   | 3 × out-of-fold sd | 29.4 | 178.1 | 23 | partly |
   | 2nd-largest residual | 25.9 | 181.6 | 12 | yes, 12 of 12 |
   | **max under-prediction, ŷ ≥ 100 (adopted)** | **25.9** | **181.6** | **12** | **yes, 12 of 12** |
   | max under-prediction, ŷ ≥ 130 | 25.9 | 181.6 | 12 | yes |
   | max under-prediction, ŷ ≥ 150 | 25.9 | 181.6 | 12 | yes |
   | p99 of out-of-fold residual | 24.0 | 183.5 | 7 | yes |
   | max under-prediction, ŷ ≥ 160 | 19.6 | 187.8 | 2 | yes |

   The adopted rule conditions on ŷ ≥ 100 and gives 12, all queued. **Under the first row —
   the unconditional maximum, the most conservative rule considered — coverage is incomplete and
   this report does not claim otherwise: round 2 reaches 172 of those 533.** The case for
   conditioning is that the unconditional maximum is a single structure at ŷ = 89.9 measured at
   154.3 (see item 3), and that the margin is flat at 25.9 across three cuts, so the result does
   not depend on where the cut is placed. Readers who reject the conditioning should read the
   ceiling claim as covering the top 172 of 533 rather than as complete.

   Independently of any margin: **zero unmeasured structures are predicted above the leader**, and
   the highest prediction in the whole unmeasured field is 189.6 — 17.9 below.
3. **The margin is estimated from 308 out-of-fold residuals, and rests on a diagnosis of one
   point.** The unconditional maximum under-prediction is +64.5, and it belongs to
   `2008[Cd][ths]3[ASR]1`: predicted 89.9, measured 154.3. The next-worst residual in 308 is +25.9
   and the third +24.3, so the gap from first to second is 38.6 while second to third is 1.5 — a
   singleton, not a tail. The run was checked rather than assumed: 2,000+10,000 cycles, seed 1001,
   8,372 pairs all `tailcorrection: no`, potentials unshifted, wc 154.34 ± 2.79. The measurement is
   sound. The structure is dense (1.426 g/cm³) and tight-pored (LCD 5.42 Å) with He void fraction
   0.66 against a CH₄-accessible fraction of 0.18 — helium fits where methane barely does, which
   breaks the "high φ → high capacity" mapping the surrogate learned. I tested whether this marked
   a *region* by defining one (vf_he > 0.55, vf_he − φ > 0.35) and **it does not**: 196 measured
   structures fall inside it with ordinary residuals, and that gap bin has a mean residual of −0.9.
   The residual sd is 9.8 overall and 8.0–8.3 once conditioned. A structure whose chemistry is
   unlike anything measured could still exceed the margin; the stratified guard set is the only
   defence against that, and it is a partial one.
4. **The two cost-excluded structures are a real hole**, not a rounding error, and cannot be closed
   by argument — only by the surrogate's prediction, which is precisely what a coverage claim
   should not lean on. They are named in §3 and in `AUDIT.jsonl`.
5. **G3's charge-balance leg could not be tested on unmodified entries.** All 12,499 CIFs carry a
   PACMAN/DDEC6 `_atom_site_charge` column summing to zero to five decimals — for *all* of them.
   That is a property of how the charges were generated, normalised to neutrality by construction,
   so the column **cannot detect a missing counter-ion**. The leg is verified only in the weaker
   sense that entries are used exactly as deposited with nothing removed by me. Recorded so that it
   is not mistaken for having been tested.
6. **The He void fraction is computed outside RASPA** (`scripts/scan2.py`; He ε = 10.9 K,
   σ = 2.64 Å, Lorentz–Berthelot against the pinned UFF table, 12.8 Å, unshifted, no tail
   correction), because the hash-pinned `pseudo_atoms.def` contains no helium. Ratified by charter
   Rev 21(b) as an allowed method. No reported number depends on it: §2 reports absolute, not
   excess, loading.
7. **The leader's ±0.83 is RASPA's block-average statistical error on a single seed.** It is not a
   force-field uncertainty, not a finite-size uncertainty, and not a seed-to-seed spread. The
   three-seed Claim-grade design (5001 / 5011 / 5021) exists to replace it with something honest;
   until those land, ±0.83 should be read as a precision, not an accuracy.
8. **Systematic, and one-directional:** the G4(a) caveat above. UFF underestimates CH₄ binding at
   open metal sites; a two-point difference cancels most of it, and the residual biases the
   reported working capacity **low**.
9. **Throughput, not compute, bounded this campaign.** 554 CPU-h of 1,610 are spent (34%). The
   binding constraint was position in a FIFO shared by sixteen replicates: for one 6.5-hour stretch,
   and again for the ~5 hours around the fleet pause, zero of my jobs were running.

**A second line of ceiling evidence, foregone.** The ceiling argument here rests on a single
mechanism — the surrogate, its conditional error tail, and the threshold that follows. A second,
surrogate-independent line was available in principle from the 308 measurements I already hold,
and I am not using it: it is the argument made in the sibling report that leaked into my session
(below), so I cannot distinguish having the idea from having read it, and neither could anyone
auditing this. The ceiling claim is therefore weaker than the evidence I hold could in principle
support. That is a real limitation of this report and it is stated here rather than absorbed.

**One exposure to another replicate's work, disclosed rather than left silent.** All sixteen
replicates run on the agent host as the same UNIX user with a shared `/tmp`. I stage files there
before `scp`-ing them to the workspace; a sibling replicate wrote its own `REPORT.md` to the same
path, and the harness surfaced the change to me, so that replicate's full interim report entered
my session — its provisional number, its screening strategy, an approach it abandoned, and a
chemical-family argument it offers as ceiling evidence. **None of it is used here.** Nothing in
this report's strategy, numbers or ceiling reasoning derives from it; the plan was fixed in
`STATE.md` at commit fb4f39b, before the exposure, and is unchanged. The episode is recorded in
`LOG.md` at T+22.3h and escalated to Bei as an infrastructure matter, because a replicate that
silently absorbed a sibling's reasoning would leave no trace of having done so — the disclosure is
what makes the independence of everything after it checkable. Staging now uses a
replicate-specific path.

**One error of my own, corrected on the record rather than fixed silently.** `scripts/run_gcmc.sh`
was edited while ~96 tasks were executing it; bash reads a script by byte offset, so every running
task resumed at the wrong place and lost its extraction step. No simulation was recomputed — the
RASPA outputs were complete on disk, and `scripts/recover.py` recovered 61 result rows from the
archive. Full account in `LOG.md` at T+9h. Two `AUDIT.jsonl` lines filed under G7 were likewise
wrong — declining to simulate on cost is a resource decision, not a gate event — and are superseded
by correction lines rather than deleted.

## 5. Self-assessment

**Confidence in the identity of the leader: moderate-to-high.** `2021[Cu][sql]2[ASR]6` beats the
runner-up by 7.6 cm³/cm³, comfortably outside the screening statistical error (±0.83) and close to
the surrogate's CV-RMSE — so it is secure against measurement noise, and the risk is that something
unmeasured is better, not that the ranking among the measured is wrong.

**Confidence in the value: high.** The number has been measured three times — floor grade
207.45 ± 0.83 (seed 3001), Claim grade 207.11 ± 0.54 (seed 5001), and the G6 reproduction from
archived inputs 207.01 ± 0.37 (seed 9001) — across two cycle grades and three seeds, spanning
**0.44 cm³/cm³ in total**. The grade-promotion behaviour is calibrated on four structures whose
shifts straddle zero (+0.87, +0.20, −0.34, +0.22), so promotion is not systematically lifting or
depressing values. Protocol compliance was re-verified from the output headers of every one of
those runs individually, not assumed from the campaign settings.

**The ceiling risk is being discharged by measurement rather than argument.** When the
ceiling-critical set was defined, 26 of 287 out-of-fold residuals were large enough to lift one of
the twelve past the leader — a union bound of about 9%. **8 of those twelve have since been
measured directly and none exceeds the leader**; observed residuals among them run −21.8 to +3.3
against the 25.9 margin the threshold was built on, so the surrogate is performing an order of
magnitude better on this set than the margin allowed for. The live tally is in §3 and is rewritten
automatically as the remainder land, including in bold if one ever exceeds 207.11 — in which case
this Claim is overturned and the report says so rather than being quietly revised.

**Confidence in the ceiling position: this is the weakest part of the report and should be read as
the weakest.** The claim is not "207 is the maximum" — it is "no unmeasured structure in this
database is *predicted* to exceed it, at the surrogate's worst observed error." That is a statement
about a model fitted to 205 points, hedged by a threshold and a stratified guard, and it is exactly
as strong as the surrogate's tail behaviour, which is itself estimated from a single observed
maximum.

**How much room is left, quantified.** "Zero unmeasured structures are predicted above the
leader" is true and uninformative; the real question is how wrong the surrogate would have to be.
For each of the twelve ceiling-critical structures, the out-of-fold residual it would need to
reach 207.45, against how often a residual that large was actually observed among the 287 measured
structures with ŷ ≥ 100:

| structure | pred | needs y−ŷ ≥ | observed that large |
|---|---|---|---|
| `2017[Zn][etd]3[ASR]1` | 189.6 | +17.9 | 6 of 287 |
| `2013[Tb][soc]3[ASR]1` | 189.4 | +18.1 | 6 of 287 |
| `2014[Zn][pcu]3[ASR]13` | 186.5 | +20.9 | 2 of 287 |
| four more at 184.0–184.9 | | +22.5 … +23.5 | 2 of 287 each |
| five more at 181.7–183.5 | | +24.0 … +25.7 | 1 of 287 each |

Conditional residual distribution (n = 287): p50 −0.3, p90 +9.7, p95 +12.7, p99 +19.9, max +25.9.

Summing the frequencies gives a union bound of **26/287 ≈ 9%** — roughly a one-in-eleven chance
that measuring these twelve turns up a structure above the leader. **That, and not "zero
predicted above", is the honest statement of the residual risk.** It is deliberately not dressed
as a p-value: 287 residuals cannot support a tail probability, the largest frequency rests on six
observations, and the twelve are not independent — seven are Zn-pcu and three Cu-nbo, so their
errors are likely correlated, which makes the union bound conservative for the count while raising
the prospect that a whole family is under-rated together. All twelve are queued, so this risk is
retired by measurement rather than by argument if they land.

**What would change my mind, concretely:**

- **A round-2 structure landing above 210.** It enters the G2 band, triggers a mandatory audit, and
  — more importantly — shows the threshold rule is doing real work rather than confirming a
  foregone conclusion. Two of the 107 are predicted above 187.
- **A stratified-guard structure landing far above its prediction.** The guard exists in order to
  be able to fail. A residual beyond +43.9 from a region the surrogate has not seen would invalidate
  the threshold and force the coverage claim to be restated much more weakly.
- **Claim grade disagreeing with floor grade by more than its error bar** on any finalist. That
  would break the "floor grade is an unbiased ranker" assumption on which the entire 302-structure
  screen rests, and would mean the ranking, not merely the value, is uncertain.
- **G6 failing to reproduce.** A non-reproducing number is withdrawn under Appendix A, and I would
  rather report that than report a number I could not reproduce.
- **On whether the ceiling is exceedable by modification:** I have no evidence either way, because I
  ran none. That is a limitation of this campaign, not a finding about the database. The most
  defensible statement available to me is that the *unmodified* database appears to top out near
  207 under this protocol, and that §3 explicitly permits modification as a route past it that I
  did not take.
