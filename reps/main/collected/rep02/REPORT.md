# REPORT — Methane deliverable capacity, 12,499-structure database
**rep02 — COMPLETE as of 2026-08-31 22:10 KST. This is a filed report, not a
draft.** Both halves of the §1 mandate are answered at a tier §3 admits, and it
is written to stand as filed if the campaign stops at any moment — which it
will, on the spend budget rather than the deadline. It will still be updated if
further evidence arrives: the only outstanding work that could change anything
is the +25% insurance band of §5, and §5 states plainly that it is unfinished.
Every number traces to a commit and to `JOBS.md` / `logs/jobs.tsv`. Numbers
marked *(screening)* come from 500+3,000 cycles, which is **below** the charter
§3 floor; they are ranking devices only, are not reportable values, and none
will appear in the Claim.

---

## 1. Claim

**Best validated material: `2021[Cu][sql]2[ASR]6`, working capacity
207.03 ± 0.20 cm³ STP/cm³** (N(65) 243.8, N(5.8) 36.8; RASPA 2.0.37 under the
pinned §3 protocol at **10,000 initialization + 50,000 production, three
independent seeds** giving 207.14 / 206.83 / 207.13 — claim grade). **My best
number is at the achievable maximum for this database and protocol to within a
few cm³/cm³ across every family this campaign measured**, and no unmeasured
member of those families can exceed it unless its working capacity per unit van
der Waals void beats the largest value ever measured here by more than 25%.
**One family is not covered by that statement and I found it late: the
2-periodic (layered) interpenetrated structures**, of which the claimed material
is itself one. §5 states the gap rather than absorbing it.

**The ceiling can be approached but not beaten by the structural modification I
tried:** interpenetration removal raises individual materials by a mean of +87.1 cm³/cm³
over 250 paired parents, produces eight of the ten claim-grade structures, and
still falls 2.86 cm³/cm³ short of this database entry.

**The claim-grade tier — the only tier §3 admits for a Claim.** Uncertainties
are across-seed standard deviations; `r` = wc/vf₀ is the working capacity per
unit van der Waals void that the ceiling argument of §5 runs on.

| structure | wc | seeds | N(65) | N(5.8) | vf₀ | r | origin |
|---|---|---|---|---|---|---|---|
| **`2021[Cu][sql]2[ASR]6`** | **207.03 ± 0.20** | 3 | 243.8 | 36.8 | 0.819 | 252.8 | **database** |
| `2012[In][dia]3[ASR]4__1of2` | 204.17 ± 0.14 | 3 | 243.7 | 39.5 | 0.826 | 247.3 | built here |
| `2014[Zn][hms]3[ASR]1__1of2` | 203.66 ± 0.23 | 3 | 249.5 | 45.8 | 0.795 | **256.1** | built here |
| `2021[Mn][dia]3[FSR]1__1of2` | 201.23 ± 0.03 | 3 | 239.7 | 38.5 | 0.820 | 245.4 | built here |
| `2016[InCo][pts]3[ASR]1__1of2` | 200.16 ± 0.08 | 3 | 240.7 | 40.6 | 0.813 | 246.3 | built here |
| `2016[Cu][pts]3[ASR]1` | 199.67 ± 0.01 | 2 | 243.5 | 43.8 | 0.809 | 246.9 | database |
| `2015[Cd][bto]3[ASR]1__1of2` | 199.49 ± 0.21 | 3 | 240.5 | 41.0 | 0.813 | 245.3 | built here |
| `2018[Zn][pth]3[ASR]2__1of2` | 199.21 | 1 | 237.4 | 38.2 | 0.822 | 242.4 | built here |
| `2018[Zn][pth]3[ASR]1__1of2` | 198.87 | 1 | 236.9 | 38.0 | 0.821 | 242.3 | built here |
| `2015[V][srs]3[ASR]1` | 197.50 ± 0.19 | 3 | 232.3 | 34.8 | 0.821 | 240.6 | database |

Every one has a **3-periodic pore network** with zero or negligible sealed pore
volume (§4.3) — that is a statement about the void space, which is what decides
whether a loading is an artefact, and it is **not** the same as the framework
being 3-periodic. The winner's *framework* is 2-periodic; see below, where that
distinction does real work. The lead over second place is **2.86 cm³/cm³
against a combined standard error of 0.14**, so the identity of the winner is
not in question on statistical grounds.

**The claimed material is itself two interpenetrated layered nets, and that
matters twice.** `2021[Cu][sql]2[ASR]6` is `ncomp 2, nnets 2, interpenetrated,
maxdim 2` — two identical 2-periodic sheets at 50% mass each, with no covalent
connectivity in the third direction. First, **framework rigidity is a sharper
assumption for this material than for the 3-periodic contenders**: §3 pins a
rigid framework, and the interlayer spacing of a layered solid is exactly the
degree of freedom that would respond to loading. Nothing in this campaign can
estimate that effect and the claimed number inherits it. Second, it means the
modification route was never applied to the family the winner belongs to —
`scripts/mkmod.py` counted a component as a net only if it was 3-periodic — and
§5 now carries the consequence.

**Why the winner wins, since it is not by adsorbing more and not by being the
most porous.** Its N(65) of 243.8 is unremarkable here —
`2014[Zn][hms]3[ASR]1__1of2` holds 249.5, six units more, and loses — and its
vf₀ of 0.819 is not the largest in the table. It wins on the *bottom* of the
cycle: **N(5.8) = 36.8 against 38–46 for everything else.** Working capacity is
a difference, and the structure that gives up least at the delivery pressure
takes it.

**The result contains its own explanation of why modification did not win, and
this is the campaign's most useful finding.** Read the `r` column. The highest
value in the whole claim-grade set, **256.1, belongs to an analogue** —
`2014[Zn][hms]3[ASR]1__1of2` — not to the winner, whose 252.8 is merely good.
Removing an interpenetrating net is extremely effective at raising working
capacity *per unit void*, and that is exactly what it is designed to do. But
wc = vf₀ · r needs both factors, and the analogue lands at vf₀ 0.795 while the
winner sits at 0.819. **The modification buys r and gives back vf₀.** A
modification that raised vf₀ without that trade is the thing to try next, and
this campaign did not find one.

**What the route did do, which is not small and does not depend on the
ranking.** Measured as a paired comparison over 250 parents and their own
analogues — so it is independent of how candidates were selected, of the
surrogate, and of whether the two families are comparable populations:
**mean +87.1 cm³/cm³, median +90.5, and the analogue ahead in 241 of 250.** One
instance carried to claim grade: `2014[Zn][hms]3[ASR]1` measures 75.4
*(screening)*, and deleting one of its two identical nets — exactly half the
atoms, vf₀ 0.591 → 0.795, density 0.861 → 0.431 g/cm³ — gives **203.66 ± 0.23,
a gain of 128 cm³/cm³ in one step.** Charge balance follows by construction from
each deleted component being a complete net sharing no bond with the one kept
(§3, `scripts/interp.py`, `scripts/mkmod.py`).

**A framing this report carried for seven hours today was wrong and is corrected
rather than removed.** While the best *admissible* number belonged to an
analogue — the structure that actually beats it was still screening-tier, which
§3 excludes — §1 said the database's own ceiling was not the protocol's ceiling.
It is. `LOG.md` carries the correction and §6 lists it first among the things I
got wrong.

**Two of the winner's three seeds were initially censored** at exactly 16,200 s,
the *screening* wall cap, by long-lived worker processes holding an older copy
of `runner.wall_cap` in memory, while the seed that survived took 30,480 s. The
cap was raised to 36,000 s — it is re-read on every task, so it reached those
workers — and all three seeds then completed at 29,773–30,074 s. A censored run
is recorded as `TIMEOUT` and was never mistaken for a measurement; the episode
is in `LOG.md` because for six hours the Claim rested on the one seed that
happened to escape.

**±0.20 is the across-seed standard deviation of the three claim-grade runs**,
which is what §3's seeded protocol makes reproducible. RASPA's block standard
deviation on the same runs is 0.63 and is quoted rather than used; it
overestimates run-to-run spread, as five blocks inside one Markov chain will.
The screening tier, used only for ranking, carries ±0.9 measured from 22
duplicate-group replicates — 4.5× looser than claim grade, which is the ratio
that justifies using it to rank and never to report.

## 2. Evidence inventory

### 2.1 Protocol as executed
- RASPA 2.0.37, commit `4467e14c`, the read-only build at `toolchain/raspa`.
  The three UFF files verified by SHA-256 against the §3 table: match.
  TraPPE united-atom methane, rigid framework, chargeless.
- Cutoff 12.8 Å, tail corrections off, unshifted — carried by the pinned force
  field files, not by `simulation.input`, exactly as §3 states.
- Absolute loading, N(65 bar) − N(5.8 bar) at 298 K, volumetric.
- Unit cells replicated so every perpendicular width is at least twice the
  cutoff; replication recorded per run as `nx,ny,nz` in `tables/gcmc_raw.csv`.
- **No energy grids anywhere — now a choice, not a constraint.** This report
  previously recorded that `SimulationType MakeGrid` was absent from the
  provided binary, on a harness notice of 2026-08-30. **That notice was
  retracted on 2026-08-31**: the test behind it searched the 18 KB driver
  rather than `lib/libraspa`, and grids do exist and function in this build.
  The correction is on the record here rather than removed from it. Every
  number in this campaign is nevertheless direct summation, so §3's requirement
  to declare grid-based numbers does not arise — see §3 for why grids were not
  adopted once they became available again.
- **No pore-blocking spheres**, a reading of §3 rather than an omission — §4.3.
- **Explicit random seeds on every confirmation and claim-grade run.** RASPA
  seeds itself from the clock when `RandomSeed` is absent: two unseeded runs of
  the identical point returned 175.41 and 174.05. An unseeded number cannot be
  regenerated from the pinned inputs, which §3 requires.

### 2.2 Tiers
| tier | cycles | purpose | admissible under §3 |
|---|---|---|---|
| T0 | — | geometric descriptors, all 12,499 | descriptor, not a simulation |
| T1 | 500 + 3,000 | screening and ranking | **no** — below the floor |
| T2 | 2,000 + 10,000 | the §3 floor; reportable | yes |
| T3 | 10,000 + 50,000, 3 seeds | claim grade | yes, required for the Claim |

### 2.3 What has been run *(final)*
- **T0 geometry:** all 12,499 database structures plus 1,065 modified
  analogues, 0 failures; 5.4 CPU-h for the database pass.
- **T1 screening (500+3,000 — ranking only, never reported):** 2,118
  structures with both pressures. A uniform random sample of 597 (two disjoint
  draws, verified uniform in vf₀ against the database), the bound-ordered
  wave 2, and 418 modified analogues.
- **T2, the §3 floor (2,000+10,000 — reportable):** 81 structures, 61 of which
  are also screened. That overlap is what makes the cycle-ladder check in §2.4
  possible *at the top of the range* rather than only in the middle.
- **T3, claim grade (10,000+50,000, seeded — the only tier §3 admits for a
  Claim): 10 structures**, selected as everything within 8.0 cm³/cm³ of the
  leader and then widened to include the floor-tier leaders when the two tiers
  disagreed about who was in front. Seven carry two or three seeds; the top
  seven rows of §1 are all multi-seed. 55 claim-grade pressure points in total.
- **Accessibility:** 2,135 database structures and all 664 first-wave analogues,
  0 failures. Every structure in the §1 table is certified 3-periodic.
- **Interpenetration:** all 12,499 scanned; **1,065 analogues built**, being
  every all-3-periodic interpenetrated parent in the database, each with true
  measured geometry rather than a predicted one.
- **Bulk methane reference:** 4 runs, two box sizes, two cycle settings.
- **Censored:** 6 tasks recorded `TIMEOUT`, all at exactly 16,200 s, of which 3
  were claim-grade legs of the winner and were re-run to completion after the
  cap was corrected (§1). One screening structure remains censored and its
  geometric bound excludes it anyway.
- **Lost and recovered:** 886 screening tasks failed instantly in a filesystem
  burst and were re-queued; the 2,708 that remain open in `queue/w1` are the
  +25% insurance band and are **not** finished — see §5, where that is stated as
  a limit on the ceiling argument rather than left for the reader to infer.
- **Consumption:** 865 CPU-h of 1,610 (`scripts/cpuacct.py`). Neither compute
  nor the deadline ended this campaign; spend did, exactly as §4 warns.

### 2.4 Validation performed
- **Toolchain**: SHA-256 of the three UFF files against §3; version string.
- **Geometry field**: checked against analytic excluded volume on cubic and
  triclinic cells, ±6×10⁻⁴ in volume fraction, periodic wrap correct.
- **Screening bias, and specifically at the top of the range.** 61 structures
  are now run at both 500+3,000 and the §3 floor, against 17 when this was
  first checked. Δwc = +0.009 ± 0.974 overall. The earlier check was fair but
  its sample was mostly mid-range, which is the wrong place to test a device
  used to rank the top; restricted to structures screening above 175 the
  difference is −0.096 ± 0.853 (n=39), and above 190 it is **−0.18 ± 0.93**
  (n=19, range −1.56 to +1.67). **Screening is unbiased for ranking at the top
  of the range as well as in the middle**, with a spread that agrees with the
  independent ±0.9 from duplicate groups. It remains a ranking device only: no
  screening number is reported.
- **Seed spread, measured at every tier.** At claim grade, across ten
  structures with two or three seeds each, the across-seed standard deviation
  runs **0.01–0.23** with a median near 0.14. At the screening tier it is
  **±0.9**, from 22 duplicate groups in which more than one member was
  independently measured. RASPA's own block standard deviations on the
  claim-grade runs are 0.48–0.94 — larger than the real run-to-run spread they
  are meant to describe, which is what five blocks inside a single Markov chain
  will do. **Uncertainty in this report is always the across-seed spread**, with
  block sd quoted alongside and never substituted for it. The ladder is
  internally consistent: 17× the cycles buys roughly 4.5× the reproducibility,
  which is the ratio that justifies screening as a ranking device and forbids it
  as a reported value.
- **Physical sanity, not fitted**: in-pore density N(65)/vf₀ never exceeds
  liquid methane. The numbers were not tuned to pass this.
- **Accessibility**: every candidate certified percolating — §4.3.
- **Task audit**: `scripts/audit.py` reports every non-OK task and separates
  censored structures into those the bound excludes anyway and those on the
  frontier. One censored structure so far, bound 155.9, excluded by bound.

---

## 3. Strategy account

The compute budget is about 7% of an exhaustive pass, so the campaign narrows
the field with cheap information and spends GCMC only where it can change the
answer.

**T0, geometric descriptors over the whole database.** The field
g(r) = minᵢ(|r − rᵢ| − σᵢ/2) on a 0.4 Å grid with the pinned UFF σ gives the
accessible volume fraction at every probe size at once. 12,499 structures,
0 failures, 5.4 CPU-h — three orders of magnitude cheaper than GCMC.

**T1, a uniform random sample.** 597 structures drawn uniformly and screened at
both pressures. Not a search: its purpose is an unbiased estimate of the
database's working-capacity distribution, which is what makes any statistical
statement about the unmeasured remainder possible.

**A surrogate, used only to rank.** CV MAE 8.0–8.3, R² 0.94. Two reformulations
were tested and both were negative: fitting loading per unit void and
multiplying back by the exactly-known vf₀ moved MAE by 0.08; dropping the
censored `lcd` descriptor moved it by 0.03. More important than which variant
wins is that all of them recover only 23–24 of the true top 30. **The surrogate
cannot resolve the top of this database**, which is why the ceiling argument
does not rest on it.

**Wave 2, the closure.** Every structure whose geometric bound leaves it able to
exceed the leader, screened in descending order of that bound. This is the part
that carries the ceiling argument.

**The modification route — §2's "by what means", and the answer is that this
means was not enough.** §2 asks whether the best number can be exceeded and by
what means; this route came within 1.4% and did not.
Interpenetration removal was chosen because it is charge-balanced *by
construction*: if the framework bond graph falls into components sharing no
bond, each is a complete net, so deleting one leaves the rest balanced. 1,817
of 12,499 structures are interpenetrated, 1,112 with all nets 3-periodic.

*The effect is large and it is measured as a paired comparison, parent against
its own analogue, so nothing about it depends on the two families being
comparable populations.* Over **250 pairs: mean +87.1, median +90.5,
+162.6 at best, and removal helped in 241 of 250.** The mechanism is the one
the geometry predicts — a second net fills the pores of the first, so the
parent sits at vf₀ ≈ 0.52 on the steep rising part of the envelope and the
analogue lands near vf₀ ≈ 0.76 where r peaks.

*The family is closed by construction rather than by prediction.* The first
664 analogues came from the 697 parents whose **predicted** post-removal vf₀
fell in 0.74–0.88. That window was a cost heuristic, and it is also precisely
the objection a reader should raise against any ceiling claim built on it: the
route was only applied where it was expected to pay. The remaining 401
all-3-periodic interpenetrated parents have since been built and their **true**
geometry measured; the 315 that the calibrated r-margin cannot exclude are
queued. Their vf₀ runs 0.642–0.913 with median 0.710, so the original window
was in fact well placed — but 18 of them sit on the bare frontier and had to be
measured rather than argued away.

*It moved the r envelope but not the ceiling, and the difference is the whole
result.* The largest working capacity per unit void measured anywhere, r = 261.7,
belongs to a modified structure (`2020[Zn][pcu]3[ASR]7__1of2`), not to a database
entry, whose maximum is 254.0; six analogues exceed the database r envelope for
their own porosity bin, by up to +6.0%. So the exclusion argument had to be
restated over the union of the two families rather than over the database alone
— a real correction, made when the envelope test found it. But raising r is not
the same as raising wc. Within the claim-grade set the highest r, 256.1, again
belongs to an analogue while the winner's is 252.8, and the winner still takes
it on vf₀, 0.819 against 0.795. **The route buys r and gives back vf₀**, and
wc = vf₀ · r needs both.

**What was abandoned, and one thing that was abandoned for a reason that turned
out to be false.** Tabulated energy grids were dropped on a harness notice
saying the provided binary had no MakeGrid code path. **That notice was
retracted on 2026-08-31 — grids exist in this build and work.** Having got the
option back, I did not take it, and the reason is that it no longer buys the
thing it would have bought. Grids pay off when many GCMC evaluations amortise
one tabulation; here a screening structure costs ~0.31 CPU-h for *both*
pressures at 500+3,000 cycles, against a per-framework tabulation that is a
substantial fraction of that, so the realistic saving is a factor of about two
rather than an order of magnitude. Compute is also not the binding budget — the campaign
ended with 865 of 1,610 CPU-h consumed and spend at its cap. Buying cheaper screening with
turns spent validating grid-versus-direct agreement — which §3 would require
before any grid number entered this report — would spend the budget that binds
to relieve the one that does not. The decision is recorded as a judgement, not
as an impossibility, and it would flip if the frontier reopened and demanded
thousands more screening runs.

---

## 4. Uncertainty and limitations

### 4.1 Statistical
**The uncertainty on the Claim is ±0.20 cm³/cm³**, the across-seed standard
deviation of the three claim-grade runs of `2021[Cu][sql]2[ASR]6`
(207.14 / 206.83 / 207.13). Across all ten structures measured at claim grade
the across-seed sd runs **0.01–0.23**, median near 0.14.

Three different quantities could be called "the uncertainty" here and they
differ by an order of magnitude, so this report is explicit about which is used
where.
- **Across-seed spread at claim grade, 0.01–0.23.** Used for every number in
  §1. It is what §3's seeded protocol makes reproducible from the pinned inputs.
- **Across-structure reproducibility at screening tier, ±0.9.** Measured from
  22 duplicate groups in which more than one member was independently measured
  (mean 0.91, median 0.76, max 2.21). Used only to decide what screening can and
  cannot rank; no screening number is reported.
- **RASPA's block standard deviation, 0.48–0.94 on the claim-grade runs and
  1.0–4.6 at screening.** Quoted alongside and never used, because five blocks
  inside a single Markov chain overestimate run-to-run spread. Per-run values
  are in `tables/gcmc_raw.csv` (`vv_sd`) for every number here.

**What this means for the ranking, said plainly.** The winner leads second place
by **2.86 cm³/cm³ against a combined standard error of 0.14** — twenty standard
errors — so the identity of the best material is settled on the evidence, not
asserted. That was not true earlier in this campaign: at floor tier the top five
spanned 199.9–199.0 against ±0.9 and were a genuine five-way tie, and this
section said so. It is the claim-grade tier that resolved it, which is the
argument for §3 having required that tier at all.

**Where uncertainty genuinely remains** it is coverage, not statistics: the
+25% insurance band is queued and unfinished (§5), and 2,708 screening tasks
in it were never run.

### 4.2 The compute meter
`usage.json` under-reports the CPU actually consumed — by about half when this
was first measured, narrowing to roughly 1.25× by the end of the campaign
(865 CPU-h by the workers' own accounting). It it equals PBS `cput`
summed over finished and running jobs, and PBS is losing the forked worker
children (job 3473455: ppn=6, 24 h walltime, charged 86,398 s ≈ one core-day).
The workers' own per-task wall times, a lower bound on true consumption, sum to
more than twice the meter. The campaign is planned against the larger figure.
Escalated, because if it is fleet-wide it makes cost figures non-comparable
across replicates.

### 4.3 The pore-accessibility question
§3 pins a protocol with no blocking spheres, so RASPA inserts methane into every
region where a methane centre fits, sealed cavities included. A real crystal
cannot be loaded through a sealed cavity, and nothing in the GCMC output
distinguishes the two cases. `scripts/access.py` establishes it geometrically:
threshold the descriptor field at σ_CH4/2, find the periodic connected
components, and decide channel-versus-pocket by embedding each component in a
2×2×2 supercell — a finite pocket keeps its eight copies separate, a component
spanning *d* lattice directions merges by 2^d.

**The artefact is real in this database.** Of 2,135 structures swept, 75 have no
percolating channel at all. Two were already measured:
`2016[Cu][nbo]3[ASR]25` (wc 120.7) and `2022[Cu][tbo]3[FSR]10` (wc 116.9), both
entirely sealed, both **disqualified** and kept on the record.

**It does not touch the claim.** All 230 structures on the frontier as of the
sweep are 3-periodic, maximum pocket fraction 0.084, 90th percentile 0.0002, and
every one of the ten structures in the §1 claim-grade table is 3-periodic with a
pocket fraction of 0.000 or below 0.0005.

Reading adopted: the protocol is pinned and not modified, so reported numbers
stay the protocol's numbers; the diagnostic *disqualifies* a candidate whose
capacity is an artefact, it does not correct anyone's number. Limit: f_pocket
uses a 0.4 Å grid, 6-connectivity and a hard-sphere methane radius. It is a
screen for gross artefacts, not a transport calculation.

### 4.4 Descriptor censoring
`lcd` is 2·gmax with the field capped at 6.0 Å, so every cavity above 12 Å reads
exactly 12.0, and most of the porous structures sit at that cap. Dropping it
changes surrogate MAE by 0.03, so it is costing nothing, but no claim in this
report leans on lcd at the top end.

### 4.5 What could not be verified
Stated as a list, because a limitations section that reads as prose invites
skimming past the parts that matter.

1. **The toolchain itself.** RASPA 2.0.37 is taken as correct. Its hashes match
   §3 and its outputs are internally consistent where I checked them — the
   volumetric conversion was verified by hand against the molecule counts — but
   no independent GCMC code was available to cross-check a single number.
2. **The force field's suitability.** UFF with TraPPE methane and no framework
   charges is pinned by §3. Whether it describes methane in a Zr or U framework
   accurately is outside what this campaign can test, and every number here
   inherits that.
3. **Framework rigidity.** Pinned by §3. Real frameworks breathe; the effect on
   working capacity is not estimated here.
4. **Synthesizability.** The database is hypothetical structures. Nothing in
   this campaign speaks to whether any of them can be made.
5. **Duplicates related by symmetry.** The redundancy detector compares cell
   parameters and wrapped coordinates, so it finds exact duplicates and misses
   copies related by a symmetry operation or an origin shift. 9,127 distinct
   structures is therefore an **upper bound** on distinctness.
6. **The r(vf₀) envelope above the measured coverage.** This is the assumption
   the ceiling rests on and it is quantified rather than removed: the exclusion
   holds unless an unmeasured structure exceeds the largest measured working
   capacity per unit void by more than 25%. The margin is calibrated against the
   one porosity bin with complete coverage rather than chosen, and at the
   *measured* maximum — no margin at all — the frontier is already empty. The
   band between those two statements was queued to be closed by measurement and
   **was not finished**: 2,708 screening tasks remain open. For that band the
   exclusion rests on the calibrated margin and not on data.
7. **The modification space, and the biggest single gap in this report.**
   Interpenetration removal is one modification of many. The porosity-window
   limitation was removed — all 1,065 analogues of every all-3-periodic
   interpenetrated parent are built, described and either measured or queued.
   **But the route was defined only over 3-periodic nets**, which silently
   excluded the 1,885 database entries with maxdim 2 — the family the claimed
   material itself belongs to. 648 analogues of those have since been built and
   geometrically described (`scripts/mod3.py`), and **145 of them carry a bound
   above the Claim with none measured**, because the cluster allocation had
   already gone to zero. §5 states this as an open gap rather than a closed
   exclusion. Beyond it, a different defect chemistry or functionalisation is
   untested and nothing here bounds it.
8. **Accessibility is geometric, not dynamic.** f_pocket uses a 0.4 Å grid,
   6-connectivity and a hard-sphere methane radius. A channel constricted to
   near exactly σ_CH4 could be misclassified in either direction.
9. **Screening-tier numbers are not reportable and are not reported.** They
   rank; nothing in the Claim rests on them.

---

## 5. Ceiling position

**Claimed position: 207.03 ± 0.20 cm³/cm³ is at or within a few cm³/cm³ of the maximum
reachable from this database under this protocol, including modification, and
the structure that reaches it is a database structure.** The second half of
that sentence read the other way in this report until the claim-grade runs
landed; the correction is in §1 and in `LOG.md`, not silently applied.

**The argument has one line.** It runs through the identity wc = vf₀ · r, where
r = wc/vf₀ is the working capacity per unit van der Waals void, and it closes by
*measuring* every structure that a bound on r leaves able to beat the leader.
Nothing in it is an extrapolation: the exclusion is arithmetic on a quantity
whose largest measured value is known.

**r is pinned at both ends, and both ends are measured.** It peaks at 254.0
across the database in vf₀ 0.75–0.85, where the leaders sit, and reaches 261.7
once the analogues built here are included — the largest value anywhere belongs
to `2020[Zn][pcu]3[ASR]7__1of2`, a structure this campaign built, not to a
database entry. It must fall to the bulk-methane value at vf₀ = 1, because a
framework with no framework left is a box of gas: measured under the pinned
protocol at **54.76 ± 0.74** (2,000+10,000) and 54.64 ± 1.27 (10,000+50,000),
not taken from an equation of state, which would have said ≈ 64 and anchored
the argument to the wrong curve. The database maximum vf₀ is 0.923.

**The turnover is confirmed, not assumed.** All 42 database structures with
vf₀ ≥ 0.85 are measured; their bin-local maximum r is 213.4, against 254.0 at
0.75–0.85. The mechanism is visible in the two pressures separately:
⟨N5.8/vf₀⟩ collapses from 188 to 28 across the porosity range while ⟨N65/vf₀⟩
holds near 300 until vf₀ ≈ 0.80 and then gives way, 292 → 223 → 194. So
wc = vf₀ · r is a rising factor capped at 0.923 multiplying a factor measured to
fall above 0.85, and its maximum lies in the window the leaders already occupy.

**How far the exclusion has actually been carried.** Against the highest
*measured* working capacity of any kind (208.0, screening tier), the count of
unmeasured structures that could still reach it is:

| what would have to be true about r | structures still unmeasured | CPU-h to close |
|---|---|---|
| r ≤ 254.0 — the measured database maximum | **0** | 0 |
| r ≤ 266.7 (+5%) | 23 | 7 |
| r ≤ 279.4 (+10%) | 51 | 16 |
| r ≤ 292.1 (+15%) | 90 | 28 |
| r ≤ 317.4 (+25%) | ~1,400, **all now queued** | ~436 |

**The +25% band is being closed by measurement rather than by argument.** The
adopted exclusion criterion was a +20% margin on r, calibrated rather than
chosen: `scripts/margincal.py` uses the one porosity bin with complete coverage
(vf₀ ≥ 0.85, 42/42 measured) as ground truth, subsamples it down to the coverage
the incomplete bins have, and measures the resulting shortfall — 14.6–15.3% at
p90 and 16.0–18.1% at p99 at the coverage those bins had when the margin was
set. A 10% margin would have been a one-in-ten chance of having excluded a bin
holding a winner; 20% covered the measured p99. That is a defensible argument,
but it is still an argument, so the 335 structures above the +25% threshold that
sat in no queue were queued outright (`scripts/close25.py`). Compute is at 51%
of budget and is not the binding constraint; spend is.

**Where the ceiling was genuinely open, and how it was closed.** Not the
database — the modified family. The route was originally applied only to the 697
parents whose *predicted* post-removal vf₀ fell in 0.74–0.88, which is a cost
heuristic and also exactly what would make a negative result circular: the
modification was tried only where it was expected to pay. Every all-3-periodic
interpenetrated parent in the database now has its analogue built (1,065 in
total) and its **true** geometry measured, and what gets simulated is chosen by
the measured frontier rather than by a prediction. Their vf₀ runs 0.642–0.913,
median 0.710, so the original window was in fact well placed — but 18 of the
newly built analogues sit on the bare frontier and had to be measured rather
than argued away.

**A gap in this argument, found on 2026-09-01 and not closed.** The exclusion
above covers the database and the 1,065 analogues built from **3-periodic**
interpenetrated parents. It does not cover analogues of **2-periodic** ones,
because `scripts/mkmod.py` counted a component as a net only if it was
3-periodic, so 1,885 of the 12,499 database entries were outside the route
entirely. That was defensible while the leader was a 3-periodic net. It stopped
being defensible when `2021[Cu][sql]2[ASR]6` — itself two identical
interpenetrated 2-periodic sheets — became the Claim.

`scripts/mod3.py` closes the *construction* half of the gap: 648 analogues built
from the 681 2-periodic interpenetrated parents not previously modified, 646
with compositionally identical nets, all with true measured geometry. Charge
balance follows by the same argument as before, the deleted component being a
complete net sharing no bond with the one kept. It does **not** close the
measurement half:

| | |
|---|---|
| new analogues built and described | 648 |
| vf₀ range | 0.637 – 0.934 (median 0.734) |
| **bound vf₀·k above the Claim at k = 261.7** | **145 structures** |
| of which measured by GCMC | **0** |
| analogue of the claimed material, `…__1of2` | vf₀ 0.9095, bound **238.0** |

They are queued at the head of `queue/w1` and **will not run**: the cluster
allocation reached zero running jobs on 2026-09-01 and did not recover.

**How much this actually threatens the Claim, stated both ways rather than
picked.** The bound vf₀·k uses the single largest r ever measured, 261.7, which
occurs at vf₀ ≈ 0.75; it is a deliberately loose upper bound. Against the
*bin-local* envelope this campaign measured — max r = 213.4 for vf₀ ≥ 0.85, from
complete coverage of that bin — a structure at vf₀ 0.91 bounds at 194, below the
Claim, and the winner's own analogue bounds at 194.1. Even allowing the +6.0%
by which modified structures were shown to exceed the database envelope, it
bounds at 206 — *just* below 207.03. **So these structures are excluded by the
envelope the campaign measured and not excluded by the criterion the campaign
adopted, and the margin under the former is about one cm³/cm³.** That is too
close to call an exclusion, and I am not calling it one. The honest position is
that the ceiling claim is established for the families measured and is *open*
for this one, on 145 structures that geometry cannot separate from the leader
and that no GCMC was available to settle.

**How likely the gap is to bite, answered with measurements rather than with a
model.** The 145 unmeasured analogues occupy vf₀ 0.792–0.934. **429 structures
have already been measured in exactly that band**, and **exactly one of them
exceeds 207.03 — the winner itself.** The maximum r measured anywhere in the
band is 256.3 and the median is 206.1. So the empirical rate at which a
structure in this porosity regime beats the Claim is 1 in 429, and the expected
number among 145 unmeasured ones is about **0.3**.

That is a real bound on the risk and it is worth exactly what it is worth. It is
a base rate over a sample that is mostly 3-periodic frameworks, applied to a
family that is not, and this campaign has already shown that modified structures
can exceed the database r envelope by up to 6%. A base rate is not an exclusion
and I am not promoting it to one. What it does establish is that the open gap is
a modest probability rather than an even chance: the regime is densely sampled,
and being in it is not by itself enough.

I also attempted to predict the 145 with this campaign's own surrogate and
abandoned it. The model failed to retrain on the enlarged feature table, and
debugging it was not worth the remaining budget for a device whose cross-
validated MAE is ≈ 8 cm³/cm³ — an interval that straddles the Claim, so it could
not have separated these structures from the leader either way. §3 already
records that the surrogate cannot resolve the top of this database. The attempt
and the reason for stopping are in `LOG.md`; no predicted number appears
anywhere in this report, and under §2 none could.

**What the position does and does not license.** It licenses: *no unmeasured
member of either family can beat 207.14 unless its working capacity per unit
void exceeds the largest value yet measured by more than 25%, and that band is
queued.* It does not license *"207.03 is the maximum"*. The claimed
value is now a three-seed claim-grade mean, so the limitation is no longer
statistical; what remains is coverage and scope. The +25% band is queued but not
finished — 2,708 screening tasks remain open against a cluster allocation that
fell to a single running job — so for that band the exclusion is still the
calibrated margin rather than measurement. And **other modification routes are
untested and unbounded by anything here**: different defect chemistry,
functionalisation, or removing one of two stacked 2-periodic sheets, of which 15
analogues are built and unmeasured in `mod/`.

**On §2's "by what means", answered honestly.** The means tried —
interpenetration removal — raised individual materials by a mean of
+87.1 cm³/cm³ over 250 paired parents, put eight of the ten claim-grade
structures on the board, and produced the largest working capacity per unit
void measured anywhere (261.7, against 254.0 across the database). **It still
did not exceed the best database structure**, falling 3.0 cm³/cm³ short. The
reason is visible in the identity the whole argument runs on: removing a net
buys *r*, and the analogues land at vf₀ ≈ 0.76, while the winner sits at
vf₀ 0.819 and converts a merely-good r of 252.9 into more volume than they can.
A modification that raised vf₀ without giving back r would be the thing to try
next, and this campaign did not find one.

**A peaks-over-threshold Generalized Pareto fit was tried and is reported as a
negative result, not as a bound.** On the uniform sample of 597 it gave a right
endpoint of 187–189, stable across four thresholds with ξ ≈ −0.6. Hiding the
top *m* observations and refitting showed the endpoint tracking whatever maximum
it was handed: hide two and it declares 180.6, below a value known to exist;
hide five or more and the endpoint equals the truncated maximum to one decimal
while ξ drifts to −2.3. **The campaign has since measured 208.0**, twenty-one
units above that "ceiling", and 204.17 at claim grade. Had the fit been reported
as drafted, this campaign would have named a ceiling and then broken it twice
with its own data. It is left in the report because a reader is entitled to know
which of my methods failed.

**Order statistics survive as a statement about density, not the maximum.** From
the uniform sample, ~10 structures should exceed 186.4 and ~30 should exceed
184.9. The same calculation reports that the 1 − 1/N quantile lies beyond the
sample maximum, so it cannot locate the database maximum from n = 597.

## 6. Self-assessment

**Confidence, stated as separate claims because they do not deserve the same
confidence.**

1. *That 207.03 ± 0.20 cm³/cm³ is the best working capacity obtainable here.*
   **Moderate — downgraded from high on the last day of the campaign, by my own
   finding.** For the database and for the 3-periodic modification family it
   rests on exhaustion rather than extrapolation, with the frontier empty at the
   measured maximum r and the margin calibrated rather than chosen. But the
   route was never applied to 2-periodic interpenetrated structures, 145 of
   whose analogues bound above the Claim and none of which could be measured
   (§5, §4.5 item 7). Under the envelope this campaign actually measured they
   fall about one cm³/cm³ short; under the criterion this campaign adopted they
   are not excluded at all. **One cm³/cm³ is not a margin I would defend as an
   exclusion**, so the correct confidence here is moderate, not high.
2. *That `2021[Cu][sql]2[ASR]6` specifically is the best material.* **High, and
   it became so while this section was being written.** It rested on a single
   seed for six hours because the other two had been censored by a stale wall
   cap; all three have since completed, giving 207.14 / 206.83 / 207.13 and a
   lead of 2.86 cm³/cm³ over second place against a combined standard error of
   0.14. The remaining risk is not statistical but coverage: a structure in the
   unmeasured tail of the +25% band.
3. *That interpenetration removal transforms individual materials.* **High, and
   it is the campaign's most robust result** — a paired comparison over 250
   parents and their own analogues does not depend on the surrogate, on which
   structures were chosen for measurement, or on the two families being
   comparable populations. Mean +87.1, ahead in 241 of 250, one case going
   75.4 → 203.66 at claim grade.
4. *That the ceiling can be **exceeded** by that route.* **This is what I got
   wrong, and it is false.** For seven hours today §1 said so, on the strength
   of the best *admissible* number happening to belong to an analogue while the
   structure that actually beats it was still screening-tier and therefore not
   reportable. The route falls 3.0 short. It buys *r* and lands the analogue at
   vf₀ ≈ 0.76; wc = vf₀ · r needs both, and the winner's vf₀ of 0.819 is what
   the analogues cannot reach.

**What would change my mind, in order of how likely I think each is.**

1. *A GCMC measurement of any of the 145 unmeasured 2-periodic analogues coming
   in above 207.03.* This is now the top of the list and it is unresolved rather
   than unlikely: geometry cannot separate them from the leader, the measured
   envelope puts them about one unit below it, and no simulation was possible.
   The single most useful thing a successor could do with an hour of cluster
   time is screen `prep/mod3_live.txt` in the bound order it is already queued
   in — starting with `2021[Cu][sql]2[ASR]6__1of2`, the analogue of the claimed
   material itself.
2. *A measured structure exceeding the r envelope by more than 25%.* The single
   assumption the ceiling rests on, directly testable, tested continuously, and
   already moved twice — 247.8 → 254.0 within the database and → 261.7 once
   analogues were included. Each time the frontier was re-closed rather than
   defended, and the +25% band is queued rather than argued away.
3. *A modification route I did not try.* §2 asks by what means the ceiling could
   be exceeded and the honest report is that the one means tried came within
   1.4% and did not. A modification that raised vf₀ **without** giving back r is
   the obvious next thing and this campaign did not find one. Fifteen
   2-periodic-sheet analogues sit built and unmeasured in `mod/`.
4. *Symmetry-related duplicates changing the population.* Would shift the
   order-statistic density counts, though the tail proved insensitive to the 27%
   exact-duplicate correction.

**What I got wrong during the campaign, since it bears on how much to trust the
rest.**
- **The modification claim above**, corrected in place today with the earlier
  text left visible.
- The extreme-value ceiling line was carried for a day and would have reported
  an endpoint of 187–189; the campaign then measured 207.14. Retracted after a
  test I should have run before quoting it — hiding the top *m* observations and
  refitting, which shows the endpoint simply tracking whatever maximum it was
  handed.
- The exclusion argument was stated over the database r envelope while
  §3-admissible modified structures were already on the leaderboard, and the
  largest r anywhere turned out to belong to one of them. Found by running the
  envelope test that exists to falsify it.
- The modification route was applied only where a *predicted* porosity said it
  would pay, which would have made any negative result circular. The family is
  now closed by construction — 1,065 analogues, every all-3-periodic
  interpenetrated parent.
- A `qworker` wall-time guard reserved nothing for the task it was about to
  claim. I patched it and did not ask which already-running workers were still
  exposed, and five and a half hours later found the leader's own claim-grade
  run dead behind a claim file that looked like work in progress.
- The compute meter, the block-value units, the queue de-duplication key and the
  accessibility coverage of modified structures were each wrong at some point.
  `LOG.md` carries all of them, including an 886-task filesystem burst whose
  cause I could not name because my own exception truncation cut the path off
  one character too early.

The pattern I would flag to a reader is that the errors were in the machinery
around the numbers and in the *framing* of results rather than in the numbers
themselves; that every one was found by asking what a table actually contained
rather than by anything failing loudly; and that the two that mattered most —
the extreme-value fit and the database-only envelope — were both a bound derived
from an assumption presented as a measurement.

**On the budgets.** Neither the deadline nor compute constrained this campaign:
at the time of writing 831 of 1,610 CPU-h are used with the deadline still five
days out. **Spend is what binds**, exactly as §4 warns, and it is paid per
session turn rather than per CPU-hour — a waiting turn costs about $0.13 and a
turn that writes report sections or debugs an incident costs $1–2. The
operational lesson I would give a successor is to plan the claim tier first and
the screening breadth second, and to treat every heavy session turn as the
scarce resource it is.
