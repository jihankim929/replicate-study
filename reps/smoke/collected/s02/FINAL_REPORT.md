# FINAL REPORT — Methane Deliverable Capacity Campaign
**Replicate s02 · smoke phase · filed 2026-08-28, deadline T = 2026-08-29 09:00 KST**
Charter §7 format. Every number below traces to `tables/gcmc_results.csv`, rebuildable
from the run directories with `scripts/collect.py`, and to the job names recorded in
`JOBS.md`. Analysis scripts are named at the point of use.

---

## 1. Claim

The best material found in the provided database is **`2021[Cu][sql]2[ASR]6`**, a
Cu–sql layered framework (9,789 Å³, 244 atoms, 0.358 g/cm³, φ_He 0.880), with methane
working capacity **WC = 207.5 ± 1.2 cm³ STP/cm³** (N(65 bar) − N(5.8 bar) at 298 K,
volumetric, absolute; Monte-Carlo error only — §4 gives the cycle-length
systematic, which is bounded only weakly). It leads the runner-up by 5.6σ and the rest of the field by
14σ or more. **On the ceiling: I claim 207.5 is at or very
near the achievable maximum for this database under this protocol.** Over 96.5% of the
database that is a bound rather than an inference from the ranking: every un-simulated
geometry carrying a measured descriptor has WC ≤ 182.0 even when granted the most
efficient pore utilisation observed anywhere in the database (§2c). The remaining
**43 geometries (3.5%) are genuinely unexamined** — I could not bound them and did not
measure them (§2d); they are the one place in this database where a better material
could still hide, and on their crystal densities it is unlikely. The claim is scoped
to the database as provided; structural modification, which §3 permits, was never
attempted and is the other route above 207.5 I cannot rule out.

**Admissibility caveat, stated up front:** all 803 simulations in this campaign ran at
the §3 *floor* of 2,000 initialization + 10,000 production cycles. **No run at
10,000 + 50,000 exists, so the number above does not meet §3's claim-grade standard.**
The reason is a compute overrun described in §3 and §4; I chose to honour the §4 hard
stop rather than spend a further ~10 CPU-h past it to obtain claim-grade confirmation.

---

## 2. Evidence inventory

### Simulations run

| set | runroot | structures | purpose |
|---|---|---|---|
| `s02_desc_000..023` | — | 1,731 files | grid descriptors (φ_He, φ_acc, Boltzmann factor, U_min, LCD) |
| `s02_bench_000..031` | `runs/bench_nogrid` | 8 × 2 P | direct-summation reference |
| `s02_bg_000..007` | `runs/bench_grid` | 8 × 2 P | tabular-grid validation against the above |
| `s02_cal_000..011` | `runs/cal` | 113 | stratified calibration set across the whole database |
| `s02_wA_000..033` | `runs/screen` | 676 | census wave, descending predicted capacity |

**Totals: 805 run directories, 803 complete working capacities, covering 792 of the
1,230 distinct geometries (64.4%).** Rebuild with `python3 scripts/collect.py`, which
re-extracts from the run directories rather than trusting the per-chunk CSVs.

### Validation performed

- **Force field integrity.** RASPA silently invents pseudo-atoms for CIF labels absent
  from `pseudo_atoms.def` and parameterises them from its own internal element table,
  bypassing the pinned UFF set entirely. All frameworks are therefore read from
  `prep/`, where atoms are relabelled `<El>_` to match the pinned file, and
  `scripts/parse_out.py` rejects any run in which a pseudo-atom index > 91 is
  populated. This guard was found by inspection, not by a failure, and it invalidates
  any result produced from `db/` directly. Commit `440b1ab`.
- **Grids reproduce direct summation.** 8 structures run both ways at identical
  settings: mean difference **−0.07σ**, maximum **0.36σ**, no systematic bias
  (grid − direct, cm³/cm³: −0.25, −0.36, −0.02, +0.24, −0.24, +0.32, −0.06, −0.49).
  Commit `bd47981`. **Per §3 I state explicitly: the leader's number is grid-based.**
- **Grid potential checked against brute force.** `scripts/check_grid.py` rebuilds an
  explicit 34,300-atom supercell and sums the potential at 3,000 random points with no
  index arithmetic; agreement with the tabulated grid is at the level expected from
  finite resolution.
- **Fugacity check.** Peng–Robinson fugacity at 65 bar verified against RASPA's own
  printed value (5,674,321.80 Pa) to 8 significant figures.
- **Minimum-image convention audited across every run** (`scripts/minimage2.py`).
  Perpendicular widths are recomputed from the cell matrix per axis and checked against
  the supercell actually simulated: **1,610 run-pressure pairs, all pass**. This matters
  because the database is heavily triclinic — the leader has α 72.8°, β 107.2°,
  γ 128.2° and perpendicular widths (18.77, 18.77, 21.33) Å against lattice constants
  of 24.2/24.2/22.6 Å, so a supercell sized from lattice constants rather than
  perpendicular widths would have silently violated minimum image.
  `cifutil.unit_cells()` sizes from ⌈2·cutoff / w_i⌉ per axis and is correct.
- **The leader was re-read from raw output, not from the parsed table** (§9's
  obligation to investigate a standout). RASPA reports *"Simulation finished, 0
  warnings"* at both pressures; framework density 358.31 kg/m³ matches the CIF; and
  244.0642 ± 0.9690 minus 36.5862 ± 0.6227 cm³ STP/cm³ gives 207.478, reproducing the
  tabulated 207.48. The five production blocks are stationary at both pressures —
  513.8, 513.3, 513.6, 511.9, 515.1 at 65 bar; 76.9, 77.4, 75.9, 77.9, 76.8 at 5.8 bar
  — with no drift from first block to last.
- **Database census.** `scripts/geohash.py` hashes exactly what the chargeless
  protocol reads — cell, elements, fractional coordinates — for all 1,731 files:
  **1,230 distinct geometries**, the 501 duplicates being almost entirely ASR/FSR
  pairs differing only in an unused DDEC charge column. Commit `f337e79`.
- **A parser defect found and corrected on the record.** `parse_out.py` located output
  with `glob`, and every structure name contains `[...]`, which `glob` reads as a
  character class; every result initially returned `NOOUT`. No simulation was lost —
  the run directories retain `Output/` and everything was recovered from disk without
  re-simulating. Commit `bd47981`.

### The leaderboard (top 10 distinct geometries, floor cycles)

| # | structure | WC | ± | N(65 bar) | N(5.8 bar) | φ_He | ρ (g/cm³) | k = WC/φ_He |
|---|---|---|---|---|---|---|---|---|
| 1 | `2021[Cu][sql]2[ASR]6` | **207.48** | 1.15 | 244.06 | 36.59 | 0.880 | 0.358 | 235.8 |
| 2 | `2021[Al][nan]3[ASR]24` | 195.59 | 1.79 | 256.63 | 61.04 | 0.877 | 0.448 | 223.0 |
| 3 | `2023[Cu][nan]3[ASR]8` | 187.94 | 0.71 | 245.14 | 57.20 | 0.857 | 0.524 | 219.3 |
| 4 | `2023[Cu][nan]3[ASR]7` | 185.81 | 0.58 | 240.41 | 54.60 | 0.861 | 0.520 | 215.8 |
| 5 | `2022[Zn][rtl]3[ASR]1` | 185.67 | 0.62 | 228.73 | 43.06 | 0.838 | 0.537 | 221.6 |
| 6 | `2021[Cu][lvt]3[ASR]1` | 185.63 | 1.06 | 214.32 | 28.66 | 0.907 | 0.339 | 204.7 |
| 7 | `2023[Co][nan]3[ASR]9` | 185.44 | 1.38 | 240.11 | 54.72 | 0.860 | 0.511 | 215.6 |
| 8 | `2023[Cu][nan]3[ASR]6` | 183.79 | 0.43 | 236.20 | 52.36 | 0.857 | 0.550 | 214.5 |
| 9 | `2023[Cu][nan]3[ASR]9` | 181.74 | 1.02 | 245.03 | 63.19 | 0.846 | 0.555 | 214.8 |
| 10 | `2021[Zr][flu]3[ASR]1` | 180.78 | 2.21 | 232.72 | 51.97 | 0.831 | 0.621 | 217.5 |

Distribution over the 795 structures measured: max 207.5, p99 183.8, p95 163.1,
median 71.5, min 1.2. The leader is a genuine outlier, not the top of a plateau.

Note rank 6, `2021[Cu][lvt]3[ASR]1`: its void fraction (0.907) is the *highest* in the
top ten and above the leader's 0.880, yet it delivers 22 cm³/cm³ less. The leader wins
on pore utilisation (k = 235.8, the best in the top ten) rather than on porosity alone.
This is worth stating because it means 207.5 is not an artefact of one unusually empty
cell, and because it is why the ceiling argument in (c) uses k rather than φ_He alone.

### The ceiling argument

Screening ran in descending *predicted* capacity, so the un-covered remainder is
exactly the set the predictor ranked low — a biased remainder. The ceiling question
therefore cannot be answered from the ranking, and is instead answered from geometry,
which is measured for every structure and costs no simulation.

**(a) An observed necessary condition.** All 11 geometries with WC ≥ 180 have helium
void fraction **φ_He ≥ 0.788**. The upper envelope of WC against φ_He is monotone
across the covered set:

| φ_He | 0–.1 | .1–.2 | .2–.3 | .3–.4 | .4–.5 | .5–.6 | .6–.7 | .7–.8 | .8–1.0 |
|---|---|---|---|---|---|---|---|---|---|
| n covered | 1 | 11 | 24 | 58 | 177 | 142 | 178 | 100 | 26 |
| max WC | 3.4 | 41.7 | 56.2 | 98.1 | 101.5 | 124.7 | 170.2 | 177.3 | **207.5** |
| n un-screened | 30 | 76 | 108 | 117 | 54 | 8 | 2 | **0** | **0** |

**(b) The high-void region is exhaustively covered.** Every geometry with φ_He ≥ 0.7
has GCMC — 126 of 126, zero un-screened. Of the 34 with φ_He ≥ 0.788, none reached
207.5.

**(c) A bound, not just a threshold, for the 395 un-screened geometries that carry a
descriptor.** Define k = WC / φ_He, the working capacity per unit void. Over the 710
measured geometries the maximum is **k_max = 284.8** (`2021[Zn][lvt]3[ASR]1`); the
leader itself sits at 235.8, so k_max is genuinely conservative. The highest φ_He
among all 395 un-screened descriptor-bearing geometries is **0.639**
(`2024[Ni][sql]2[ASR]1`). Granting any of them the most efficient pore utilisation
ever observed anywhere in this database:

> WC ≤ φ_He × k_max = 0.639 × 284.8 = **182.0 cm³ STP/cm³ < 207.5.**

None of the 395 reaches the leader, with 12% margin, and this does not depend on the
predictor, on the ranking, or on the φ_He threshold in (a). It does rest on one
extrapolation, which I state rather than hide: k_max is the largest value seen in 710
measurements, not a proven maximum. A un-simulated structure could only beat 207.5 by
exceeding the most efficient pore utilisation observed anywhere in this database by
more than 14%, at a void fraction no higher than 0.639.

**(d) 43 geometries are NOT closed by any bound I can construct — the open hole.**
These have neither a GCMC result nor a descriptor (`scripts/skel.py`). They can be
bounded only through crystal density, and the attempt fails honestly:

- *Empirical route.* Across the 1,112 descriptor-bearing geometries, the maximum φ_He
  seen at density ≥ 0.936 g/cm³ (the dark-set minimum) is **0.787**, against the
  threshold of 0.788 in (a). That is a margin of 0.001 over a coincidence of rounding,
  and **I do not regard it as evidence.** An earlier commit (`68b3919`) stated this as
  a closure; that was an overstatement and is corrected here.
- *Bound route.* Calibrating skeletal density ρ_f = ρ/(1−φ_He) over the same 1,112
  geometries gives ρ_f,max = 5.36 g/cm³, hence φ_He ≤ 1 − ρ/ρ_f,max. Combined with
  k_max this leaves **36 of the 43 above 207.5** and closes nothing. The bound stacks
  two independent worst cases — the densest skeleton in the database *and* the most
  efficient pore utilisation in the database — which no real structure achieves, but I
  have no principled way to tighten it without measuring the structures.
- *Geometric route, attempted and discarded.* A bound φ_He ≤ 1 − V_vdW/V_cell from
  summed van der Waals spheres appeared to close all 43 comfortably. It is invalid: a
  union of overlapping spheres is smaller than their volume sum, so the expression
  bounds void fraction from *below*, not above. Recorded because it was briefly
  believed.

So **43 of 1,230 geometries (3.5%) are genuinely unexamined**, and the ceiling claim is
defended over 96.5% of the database rather than all of it. What would close it is
small and specific: descriptors for those 43 structures cost ~0.13 CPU-h at the
measured rate (5.15 CPU-h bought all 1,731), which would place them in (c) or reveal
them as candidates; simulating all 43 outright costs ~23 CPU-h. I did not spend
either — see §3 on the budget stop. On priors they are unpromising: their median
density is 1.29 g/cm³ against ≤ 0.902 for every high-void geometry measured, and none
of the 43 is the kind of light, open framework that populates the top of the
leaderboard. That is a prior, not a measurement, and I report it as one.

**(e) Robustness of (a) and (c) to the descriptor defect.** The grid-sizing defect of
§3 was measured at +8.1% worst case. The highest un-screened φ_He, 0.639, would need
+23.3% to reach the 0.788 threshold; uniform inflations of +8.1%, +15% and +20% move
*no* un-screened geometry across. The bound in (c) survives any inflation below +14.0%
(the point at which φ_He 0.639 would rise to 0.7285 and the bound would touch 207.5),
against a defect measured at +8.1%. (`scripts/margin.py`.)

**(f) An independent GCMC probe of the un-screened region, using no descriptors at
all.** The 113-structure calibration set was drawn stratified across the whole database
before wave A ran, so it samples exactly the region the census never reached. Wave A
stopped at predicted rank 776 of 1,230 (63.1%); the calibration set independently
placed **39 GCMC measurements beyond that depth**, spread out to the 98th percentile of
predicted rank. Their working capacities: **maximum 98.1, median 20.1, minimum 1.2** —
the best of them under half the leader. Across all 113 calibration structures, spanning
the full rank range, the maximum is 170.2.

This line of evidence depends on neither the descriptor tables, nor the k bound, nor
the φ_He threshold — it is direct simulation of the tail. Its limit is sample size: 39
of roughly 454 un-screened geometries is 8.6% coverage, and by the rule of three, zero
exceedances in 39 draws bounds the proportion of the tail above 98.1 at ≲8% with 95%
confidence — approximate, since the sample was stratified rather than uniform. It
cannot exclude a rare outlier, but it does show the tail is not quietly full of good
materials. Consistently, the structure that defines k_max (`2021[Zn][lvt]3[ASR]1`,
k = 284.8) was itself found here, at predicted rank 1013, with WC 98.1 — the predictor
badly under-ranked it, and it still comes nowhere near the leader.


Reproduce with `scripts/analyze.py`, `scripts/ceiling.py`, `scripts/envelope.py`,
`scripts/hole.py`, `scripts/verify.py`, `scripts/bench.py`, `scripts/margin.py`,
`scripts/bound2.py`, `scripts/skel.py`, `scripts/cal.py`.

---

## 3. Strategy account

**Chosen strategy: census, not prediction.** The charter states the budget is
deliberately below the ~3,162 CPU-h an exhaustive pass would cost, and expects the
field to be narrowed. The database census changed that calculus: only 1,230 of the
1,731 files are distinct geometries under the chargeless protocol, and grids had been
benchmarked at 2–6× cheaper than direct summation with no measurable bias. On the cost
figure I then held, a complete census looked affordable, which converts the ceiling
question from an extrapolation into an enumeration. That was the right *aim* — the
ceiling argument in §2 is only strong because coverage is near-complete where it
matters — and it was built on a cost estimate that was wrong.

**What I abandoned: the descriptor→capacity predictor.** Two models were built on the
grid energy histogram. A site-Langmuir model reached Spearman 0.48 with its saturation
parameter pinned at the range edge. A zero-free-parameter Polanyi/local-density model
(`scripts/model.py`) reached Spearman 0.60–0.73, Pearson 0.85–0.90. Its failure mode
is physical, not a coding error: for `2023[Sc][nan]3[FSR]9` it predicts WC 3 against a
simulated 55.9, because the methane-accessible volume is 0.7% of the cell, arranged as
tight deep pockets (U_min −2.8×10³ K) each holding one molecule. Any model converting
*volume* into *density* through a bulk equation of state cannot exceed one molecule
per 48 Å³ and must under-count such materials. Volume-filling and site-counting are
different limits and this database contains both. I stopped investing in the predictor
and demoted it to ordering the census, so that an early stop would still leave the
promising end covered — a decision that turned out to matter, because the census did
stop early.

**A grid-sizing defect, recorded rather than repaired.** `descriptors.py` sized the
fractional grid by the cell's perpendicular width rather than the lattice vector
length, making the real-space step up to ~2.5× coarser than intended in the most
triclinic cells. Fixed in `grid_shape()`, but the descriptor tables in `desc/` were
produced with the earlier sizing. The measured effect is small (worst case tested:
φ_acc 0.0074 → 0.0080) and descriptors only *order* the census and never enter a
reported number — but they do now carry weight in the ceiling argument of §2, which is
a use they were not validated for. See §4.

**What went wrong: a 7× cost miss that ended the campaign.** Wave A was sized on a
measured screening cost of 0.082 CPU-h per structure, taken from the grid benchmark.
The realised cost was **0.54 CPU-h per structure** (363.4 CPU-h / 676 structures). The
benchmark's eight structures were small-cell, and the census wave ran in descending
predicted capacity — which, since capacity correlates with pore volume, is also
descending *cell* volume. The wave was therefore loaded with the most expensive cells
in the database and the benchmark was close to the least representative sample that
could have been drawn. Metering was specified "after each wave"; wave A never
completed, so the check never fired, and the overrun accumulated unobserved across a
period when the session was not making progress. This is my error, not an
infrastructure fault.

**Consequences accepted at restart.** The meter read **483 CPU-h against a 340 CPU-h
budget — 142%, past the §4 hard stop** (`cput == walltime` on `ppn=1` verified by
`qstat -f`, so the accounting basis is sound). I stopped all further submission. Two
jobs were still running at 39.7 h each against a ~15 h median for their siblings; they
have since been terminated (`qdel` 3470596, 3470606) and the queue is empty. Between
them they burned **79.5 CPU-h and produced no completed structure**, consistent with
each being stuck on a single pathological cell. That spend appears in no results row,
so `scripts/meter.py` now carries it as an explicit line — a killed job's compute is
real and must not leave the ledger merely because it produced no output. Final ledger:
**483.0 CPU-h of 340, 142.1%.**

I filed `[ESC: charter ...]` asking whether ~10 CPU-h for claim-grade confirmation
could be spent past the stop, and received no answer before filing; absent one, I did
not spend it. I judged that adding to a breached hard limit to improve my own headline
number was not a trade I was entitled to make, and that §5's explicit blessing of "an
honest incomplete report" is the stronger reading. The same reasoning kept me from
spending the ~0.13 CPU-h that would have closed the 43-geometry hole in §2(d): "it is
only a little more" is precisely the argument that produced a 142% overrun, and I was
not willing to run it a second time. All four charter interpretations are logged as
`[CHARTER-READ]` entries in `LOG.md` per addendum A3.

---

## 4. Uncertainty and limitations

**The number is not claim-grade.** All 803 runs are at the §3 floor of 2,000 + 10,000
cycles; §3 requires 10,000 + 50,000 for any number entering the Claim. The quoted ±1.2
is the Monte-Carlo error propagated from RASPA's block averages over the two pressures.
The leader's five production blocks are stationary at both pressures with no
first-to-last drift (§2) — that is the evidence available against under-equilibration,
and it is reassuring, but it is not sufficient: block averages from a single chain
cannot detect a systematic that displaces every block equally, which is exactly what a
too-short initialization produces. **The cycle-length systematic is therefore bounded
only weakly, and by no run of the length §3 requires.** A reader should treat 207.5 as
a floor-cycle screening value, not a certified capacity.

**The leader has no independent replicate.** `2021[Cu][sql]2[ASR]6` has a geometric
twin, `2021[Cu][sql]2[FSR]6`, which was correctly de-duplicated and therefore never
simulated separately. Simulating the twin, or re-running the leader with a different
random seed, would have given exactly the independent confirmation a 207.5 outlier
deserves under §9's "if a result looks too good, investigate it." I could not do it
within the stopped budget. The 5.6σ separation from the runner-up rests on MC error
alone and does not protect against a systematic peculiar to this one structure.

**The ceiling argument leans on descriptors that were validated for ordering, not for
bounding — but the margin absorbs it.** Steps (a)–(c) of §2 use φ_He from `desc/`,
produced with the grid-sizing defect described in §3, which makes grids *coarser* than
intended and whose worst measured effect moved φ_acc by +8.1% relative. I could not
regenerate the descriptors within the stopped budget, so I bounded the exposure
instead (`scripts/margin.py`, zero compute): **the highest φ_He among all 395
un-screened descriptor-bearing geometries is 0.639** (`2024[Ni][sql]2[ASR]1`), which
would need **+23.3%** inflation to reach the 0.788 threshold — nearly three times the
worst effect the defect has been measured to produce. Under a uniform +8.1% inflation,
zero un-screened geometries cross; under +15% zero; under +20% zero; the first two
cross only at +30%. Step (c) is therefore robust to this defect by a wide margin.
Step (d) does not depend on descriptors at all — the 43 geometries there have none,
which is precisely why they are unbounded. What remains genuinely unvalidated is the
*shape* of the error: I have one measured case, not a distribution, and a defect acting
non-uniformly rather than as a uniform inflation could in principle behave differently.

**Coverage is 64.4% of distinct geometries, not 100%.** The census was intended to be
complete and is not. Of the 438 geometries never simulated, 395 are bounded below the
leader by §2(c) and 43 are not bounded at all. The ceiling claim rests on measurement
over 64.4% of the database, a bound over a further 32.1%, and nothing but a density
prior over the last 3.5%.

**Grid-based.** Per §3, stated explicitly: the leader's number and the entire census
come from tabular-grid GCMC, validated against direct summation on 8 structures to
within 0.36σ with no detectable bias. The validation set spans WC 21–98 and does not
include a structure as porous as the leader.

**Structural modification was not attempted.** §3 permits defects and
functionalisation on charge-balanced, documented structures. I explored none. My
ceiling claim covers the database as provided and says nothing about what modification
could reach.

**Record-keeping shortfall.** §6 requires every reported number to trace to a job ID.
Wave A jobs are recorded in `JOBS.md` by job *name* (`s02_wA_017` for the leader) and
by result file; numeric PBS IDs were captured only for the three jobs still visible at
restart. The trace is complete in substance but does not meet the letter of §6.

**Budget.** Compute closed at 483.0 CPU-h against a hard-stopped 340 CPU-h — 142.1%,
including 79.5 CPU-h burned by two runaway jobs that produced no result and are carried
as an explicit line in `scripts/meter.py`. Tokens ~1M of 12M — never the binding
constraint. `usage.json` reports two irreconcilable compute figures
for the same work (400.35 job-records vs 93.912 scheduler, a 4.3× gap); escalated, and
I proceeded on the larger, which matches my own accounting.

---

## 5. Self-assessment

**On the identity of the best material: high confidence.** `2021[Cu][sql]2[ASR]6` is
5.6σ clear of the runner-up and 14σ+ clear of the rest, its descriptors (φ_He 0.880,
density 0.358 g/cm³, LCD 11.3 Å) put it exactly where the envelope predicts a leader
should sit, and the force-field and grid pathways behind it are independently checked.

**On the value 207.5: moderate confidence, and it is the weakest number in this
report.** It is a floor-cycle, grid-based, unreplicated measurement of a structure I
flagged as an outlier and then could not afford to investigate — precisely the
situation §9 warns about. I would not be surprised by a shift of a few cm³/cm³ under
claim-grade cycles; I would be surprised by a shift large enough to change the ranking.

**On the ceiling: high confidence over 96.5% of the database, none over the rest.**
The argument does not depend on the predictor, whose accuracy is mediocre. For the 395
un-simulated geometries carrying descriptors it is a bound — WC ≤ 182.0 against a
leader of 207.5 — and it grants them the best pore utilisation any of the 710 measured
structures achieved. It is independently corroborated by simulation that uses no
descriptors at all: the calibration set put 39 GCMC measurements deeper in the ranking
than the census ever reached, out to the 98th percentile, and their best is 98.1
against the leader's 207.5 (§2f). Two arguments resting on different evidence agreeing
is most of why I hold this firmly. The 43 unexamined geometries I
would not defend at all: I tried three ways to bound them and all three failed, one of
them (the van der Waals construction) after I had briefly believed it worked. They are
3.5% of the database and ~0.13 CPU-h of descriptors from being resolved, and I left
them open because the compute budget was already breached — defensible, but it leaves
the claim weaker than it needed to be. For structural modification I have no evidence
at all, and §3 explicitly permits it — a functionalised or defect-engineered variant of
a top-10 framework is the obvious place a better number would come from, and I did not
look.

**What would change my mind.** (i) Descriptors for the 43 unexamined geometries
placing any of them above φ_He 0.639 — this is the cheapest experiment that could
overturn the ceiling claim, costs ~0.13 CPU-h, and is the first thing I would spend
restored budget on. (ii) A claim-grade 10,000 + 50,000 run on the leader and its twin
disagreeing with 207.5 by more than ~3 cm³ STP/cm³. (iii) Regenerated descriptors,
with the grid-sizing fix, lifting any un-screened geometry above φ_He 0.639 — bounded
rather than open, since the closest sits at 0.639 and the defect was measured at
+8.1%. (iv) Any structure anywhere in this database reaching WC ≥ 180 at φ_He < 0.7,
or k = WC/φ_He above 284.8 — either would break the bound the ceiling rests on, and
795 measurements have produced neither.

**On my own conduct.** The campaign's substantive failure was not scientific but
operational: I sized a 700-job wave on a cost measured from an unrepresentative sample,
specified the check that would have caught it to run at a point the wave never reached,
and then lost roughly a day of wall-clock during which the overrun compounded
unobserved. The census strategy was sound and the ceiling argument survives at 64%
coverage largely by luck — because the ordering I had demoted to a formality happened
to put the right structures first. Had the wave been ordered arbitrarily, a 142%
overrun would have bought a leaderboard with no defensible ceiling at all.
