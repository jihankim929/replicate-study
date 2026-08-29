# LOG — append-only narrative


## 2026-08-26 — Day 0: setup, protocol integrity, screening infrastructure

**Charter read in full.** Mandate: max methane working capacity
WC = N(65 bar) - N(5.8 bar), 298 K, volumetric (cm3 STP/cm3), over the 1,731-structure
database in db/, under the fixed protocol of section 3. Deadline 2026-08-29 09:00 KST
(WORKSPACE.json). Budget 340 CPU-h / 12M tokens / <=50 queued jobs / queue `long`.

[CHARTER-READ] §2: "working capacity ... volumetric" does not say absolute or excess
uptake -> adopted **absolute** volumetric loading. Reasons: (a) absolute is the
convention in the methane-storage deliverable-capacity literature the 5.8/65 bar pair
comes from (ARPA-E MOVE); (b) RASPA's "excess" is defined against HeliumVoidFraction,
which the protocol does not pin, so excess would not be reproducible from the pinned
inputs alone. Every reported number is RASPA "Average loading absolute
[cm^3 (STP)/cm^3 framework]".

[CHARTER-READ] §3: "Energy grids permitted for screening" -> read as permitting
RASPA `UseTabularGrid`; grids are generated with the pinned binary and pinned UFF
files, so the potential is the protocol potential, sampled by interpolation. Any
grid-based number promoted to the report will be labelled, and the Claim will rest on
non-grid runs.

**DONE — toolchain verified.** sha256 of all three UFF files match the charter §3
table. `libraspa2.so` reports RASPA 2.0.37. Verification was optional; done anyway
because of the finding below.

**DONE — protocol-integrity defect found and fixed (important).**
RASPA 2.0.37 does *not* fail when a CIF atom label is absent from
`pseudo_atoms.def`: it silently creates a new pseudo-atom and takes Lennard-Jones
parameters from its own internal element table. The db CIFs label atoms `In1`,
`C3`, ... while the pinned UFF set uses `In_`, `C_`, ... . A naive run therefore
would *not* use the pinned force field. Demonstrated in runs/test/t1: pseudo atoms
92-95 `In`,`H`,`C`,`O` were auto-created (output .data, "Current Atom Status").
Fix: scripts/prep_cifs.py rewrites only the `_atom_site_label` column to `<El>_`,
writing prep/ (1,731 files, 392,704 atoms, atom counts verified identical to db/;
per-file source and product sha256 in tables/prep_manifest.csv). runs/test/t2
confirms every framework atom now resolves to pinned pseudo-atom indices <= 91.
scripts/parse_out.py refuses any run in which a pseudo-atom index > 91 is populated,
so this cannot recur silently.
(For the elements checked by hand -- In, C, H, O -- RASPA's internal table happens to
agree with the pinned file. The fix removes the dependence on that coincidence.)

**DONE — cheap screening descriptors.** 340 CPU-h against a measured 3,162 CPU-h for
an exhaustive GCMC pass means at most ~11% of the database can be simulated. Rather
than sample blindly, scripts/descriptors.py evaluates the *same* potential RASPA uses
(pinned UFF, Lorentz-Berthelot, 12.8 A, truncated/unshifted, no tail correction) on a
0.35 A real-space grid per structure and reduces it to He void fraction, CH4 Henry
constant, accessible volume fraction, well depth, Boltzmann-mean energy and a largest-
cavity-diameter proxy. ~6-15 s/structure, ~5 CPU-h for the whole database. These are
screening quantities only; no reported number will come from them.

**RUNNING — grid-vs-no-grid benchmark**, 8 structures stratified over simulation-cell
size, both pressures, floor cycles (2,000+10,000). Purpose: measure cost per structure
and whether tabular grids reproduce direct summation. The grid arm of the first
submission failed instantly (16 tasks, ~0 CPU-h): grids are written under
$RASPA_DIR/share/raspa/grids and the toolchain is read-only. Fixed with raspa_rw/, a
directory whose bin, lib, forcefield, molecules, structures and framework entries are
symlinks to the read-only toolchain (sha256 re-verified through the symlink path) and
whose grids/ is writable.

### Benchmark 1 — tabular grids vs direct summation (job tags `bench_*`, `bg_*`)

Same structures, same floor cycles (2,000 init + 10,000 prod), both protocol
pressures. Absolute volumetric loading, cm³ STP/cm³:

| structure | quantity | direct | grid (0.15 Å) | difference |
|---|---|---|---|---|
| 2023[Dy][nan]3[ASR]1 | N(65)  | 172.52 ± 2.42 | 171.88 ± 1.78 | 0.64 (0.21 σ) |
| 2023[Dy][nan]3[ASR]1 | N(5.8) | 118.78 ± 1.49 | 118.51 ± 0.57 | 0.27 (0.17 σ) |
| 2023[Dy][nan]3[ASR]1 | **WC** | 53.73 ± 2.84  | 53.37 ± 1.87  | 0.36 (0.11 σ) |
| 2023[Fe][sql]2[ASR]1 | N(65)  | 65.93 ± 4.18  | 65.35 ± 0.48  | 0.57 (0.14 σ) |
| 2023[Fe][sql]2[ASR]1 | N(5.8) | 45.28 ± 2.52  | 44.73 ± 1.39  | 0.55 (0.19 σ) |
| 2023[Fe][sql]2[ASR]1 | **WC** | 20.65 ± 4.88  | 20.63 ± 1.47  | 0.02 (0.00 σ) |
| 2023[Gd][bey]2[FSR]1 | N(65)  | 116.89 ± 1.83 | 116.40 ± 1.61 | 0.49 (0.20 σ) |

DECISION: grids reproduce direct summation to well inside the Monte-Carlo error, so
tabular grids are used for **screening**. The Claim will still be backed by
direct-summation runs at claim cycles, because the charter permits grid numbers in the
report only if labelled, and a claim is worth more without the caveat.

Cost, measured (both pressures, floor cycles, `ac` nodes):
direct 877 s (Dy), 1,071 s (Fe), 1,958 s (Gd);
grid 483 s (Dy, incl. 38 s grid generation), 245 s (Fe, incl. 74 s).
Speed-up is 2-6×, largest for big frameworks. Direct floor-cycle cost is 0.24-0.55
CPU-h per structure, well below the charter's 1.83 CPU-h/structure figure; budgeting
uses my own measurements and `scripts/meter.py` tracks actual burn.
Grid generation scales as V·N_atoms: median 52 s, but the 6% tail above 600 s reaches
4.6 h for the largest cell — those structures get direct runs instead.

**Error found and corrected (record, not silently fixed).** `scripts/parse_out.py`
located RASPA output with `glob`, and every structure name contains `[...]`, which
`glob` reads as a character class. Every result therefore came back `NOOUT`. No
simulation was lost — the runners retain `Output/`, so `scripts/reparse.py` and
`scripts/collect.py` recovered all of it from disk. `collect.py` now scans run
directories with `os.listdir` and is the authoritative results table
(`tables/gcmc_results.csv`); the per-chunk CSVs are used only for wall-clock.

**Screening model.** `scripts/descriptors.py` also emits, per structure, the histogram
of the methane-framework energy over the grid. `scripts/model.py` turns that into a
two-parameter site-Langmuir isotherm (each equal-volume voxel an independent site,
θ = Kf/(1+Kf), K = c·e^(−U/T)), which reduces to Henry's law at low fugacity and to
volume filling at high fugacity — the two limits working capacity is the difference
between. Fugacity from Peng-Robinson with the constants RASPA reads from
`TraPPE/methane.def`; verified against RASPA's own printed value at 65 bar
(5 674 321.80 Pa, agreeing to 8 significant figures).

### The database contains only 1,230 distinct geometries, not 1,731

`scripts/geohash.py` hashes exactly what the chargeless protocol reads — cell
parameters, element symbols and fractional coordinates — for all 1,731 files.
Result: **1,230 distinct geometries**; 771 files are unique, 434 geometries appear
twice, 8 appear three times, 17 appear four times. The duplicates are almost all
`ASR`/`FSR` (all-solvent-removed / free-solvent-removed) pairs of the same entry.
Spot check: `db/2021[Ag][nan]3[ASR]1.cif` and `db/2021[Ag][nan]3[FSR]1.cif` are
byte-identical apart from the `data_` block name and the DDEC charge column — and the
charge column is unused, since the protocol is chargeless.

Consequence: **the whole database can be simulated within budget.** 1,230 distinct
geometries at the measured grid cost (~0.12 CPU-h per structure, both pressures, floor
cycles) is ~150 CPU-h against 334 CPU-h remaining. That converts the mandate's
ceiling question from an extrapolation into a census. Duplicates are simulated once
and the result is copied to their twins, with the twin relationship recorded in
`tables/geohash.csv`.

DECISION: screen every distinct geometry at floor cycles, in **descending order of
predicted working capacity**, in waves, metering after each wave. If the budget runs
out early the covered region is still the promising end of the ranking, and the report
can state exactly what fraction of the database was covered and what was not.

### Screening model: why the physics-first predictor only half works (kept on record)

Two zero-to-two-parameter models were built on the grid energy histogram.

*Site-Langmuir* (each voxel an independent site, one global saturation density):
Spearman 0.48 against 14 GCMC points, with the fitted saturation pinned at the top of
its range — it forces near-empty large pores to fill to liquid density.

*Local-density / Polanyi* (`scripts/model.py`, the one in use): local density is the
bulk Peng-Robinson density at the enhanced fugacity f·exp(−U/T). Zero free parameters
in its limits. Spearman 0.60-0.73, Pearson 0.85-0.90 over 19-33 GCMC points.

Its failure mode is instructive and is *not* a coding error. Example
`2023[Sc][nan]3[FSR]9`: predicted WC 3, simulated 55.9. Its methane-accessible volume
(U < 0) is 0.7% of the cell, yet GCMC puts 3.15 molecules in the 1553 Å³ cell. Both
are true: the pore space is a set of tight, deep pockets (U_min −2.8×10³ K), each
holding one molecule in a few Å³ of centre-volume. Any model that converts *volume*
into *density* through a bulk equation of state cannot exceed one molecule per 48 Å³
and so must under-count tight-pocket materials. Volume-filling and site-counting are
different limits and this database contains both.

The grid potential itself was checked and is correct: `scripts/check_grid.py` rebuilds
an explicit 34,300-atom supercell and sums the potential at 3,000 random points with
no index arithmetic. Brute force vs the scatter grid for `2023[Sc][nan]3[FSR]9`:
fraction U<0 0.00700 vs 0.00801, ⟨exp(−U/T)⟩ 3.57 vs 4.19, U_min −2572 vs −2802 K —
agreement at the level expected from finite grid resolution.

A grid-sizing defect was found and corrected while chasing this: `descriptors.py`
sized the fractional grid by the cell's *perpendicular width* rather than the lattice
vector length, so the real-space step along a lattice direction was |a_i|/n_i, up to
~2.5× coarser than intended in the most triclinic cells. Fixed in `grid_shape()`.
The measured effect on the descriptors is small (phi_acc 0.0074 → 0.0080 for the worst
case tested), and the descriptor table in `desc/` was produced with the earlier
sizing; this is recorded rather than silently regenerated, because descriptors are
used only to *order* the census and never enter a reported number.

DECISION: stop investing in the predictor. Since only 1,230 distinct geometries exist
and the measured screening cost is 0.082 CPU-h each, the whole database can be
simulated for ~100 CPU-h. The predictor's remaining job is only to order the waves so
that an early stop still leaves the promising end covered.

---

## 2026-08-28 — session restart, budget overrun found, census closed

**Restart.** The harness restarted this session (restart 1 of 3) after ~1,468 minutes
with no recorded activity. Deadline unmoved: T = 2026-08-29 09:00 KST. STATE.md was
last written 2026-08-26 15:51 and was two waves out of date; the reconciliation below
is the correction.

### The compute budget was exceeded, and I did not notice it happening

`scripts/meter.py` on restart:

| bucket | CPU-h |
|---|---|
| descriptors | 5.15 |
| runs/bench_grid + bench_nogrid | 0.36 |
| runs/cal | 34.58 |
| runs/screen | 363.43 |
| **finished total** | **403.53** |
| in-flight (2 jobs, cput) | 79.47 |
| **TOTAL** | **483.00 of 340 = 142.1%** |

This is past the §4 hard stop and it is my error, not an infrastructure fault. The
cause is a cost estimate that was wrong by ~7x and was never re-measured after the
wave launched. LOG entry of 2026-08-26 recorded "measured screening cost 0.082 CPU-h
each" and sized a 1,230-structure census at ~100-150 CPU-h on that basis. The realised
cost was **0.54 CPU-h per structure** (363.43 CPU-h / 676 screened). The 0.082 figure
came from the grid benchmark, whose eight structures were small-cell; wave A ran in
descending predicted capacity, which is *also* descending cell volume, so the wave was
loaded with the most expensive cells in the database and the benchmark was the least
representative sample that could have been drawn. Metering was specified "after each
wave" and wave A never ended, so the check never fired.

Two jobs (3470596 `s02_wA_014`, 3470606 `s02_wA_024`) were still running at restart,
each with `resources_used.cput` 39:44 against a ~15 h median for their 32 finished
siblings — pathological, and burning ~2 CPU-h per wall-hour. `qstat -f` confirms
`cput == walltime` on `ppn=1`, so the wall_s basis the meter uses is CPU time and the
483 CPU-h figure is sound. Filed `[ESC: infra ...]` asking Bei to qdel them; my own
`qdel` is blocked in this session.

`usage.json` disagrees with itself — `cpu_h` 400.35 (job-records) vs `cpu_h_scheduler`
93.912 for the same work, a 4.3x gap. Filed `[ESC: infra ...]`. I proceed on the
larger number, which matches my own independent accounting.

DECISION: **no further compute is submitted.** The §4 hard stop is binding and already
breached; adding to the breach to improve my own result is not a trade I am entitled
to make. Filed `[ESC: charter ...]` asking whether ~10 CPU-h for claim-grade
confirmation may be spent; absent an answer I file on floor-cycle evidence and say so.

### Census result

`scripts/collect.py` re-extracted every run directory: **805 run dirs, 803 complete
working capacities**, covering **792 of the 1,230 distinct geometries (64.4%)**.
All 803 are at floor cycles, 2,000 init / 10,000 production. **No run at
10,000 + 50,000 exists**, so no number in this campaign is claim-grade under §3.

Leader: **`2021[Cu][sql]2[ASR]6`, WC = 207.48 ± 1.15 cm³ STP/cm³**
(N_hi 244.06, N_lo 36.59 molecules/cell; 9,789 Å³, 244 atoms, 0.358 g/cm³,
φ_He 0.880, LCD 11.3 Å). It leads the runner-up `2021[Al][nan]3[ASR]24` (195.59 ±
1.79) by 5.6σ on MC error, and the rest of the top six by 14-17σ. Its `FSR` twin was
not independently simulated, so the leader has no replicate.

### Ceiling: the un-screened remainder is bounded without simulating it

Screening ran in descending predicted capacity, so the 438 un-covered geometries are
exactly the ones the predictor ranked low — a biased remainder, and the ceiling
question cannot be answered from the ranking alone. It can be answered from geometry.

*Observed necessary condition.* All 11 geometries with WC ≥ 180 have helium void
fraction **φ_He ≥ 0.788**. The upper envelope of WC against φ_He is monotone across
the covered set (max WC by φ_He bin: 3.4, 41.7, 56.2, 98.1, 101.5, 124.7, 170.2,
177.3, 207.5).

*The high-void region is exhaustively covered.* Every geometry with φ_He ≥ 0.7 has
GCMC — 126 of 126, zero un-screened. Of the 34 with φ_He ≥ 0.788, none reached 207.5.

*Un-screened geometries carrying a descriptor:* 395, of which **zero** have
φ_He ≥ 0.788. The best any of them could be, on the observed envelope for φ_He < 0.7,
is ~170.

*Un-screened geometries carrying no descriptor* ("dark set"): 43. These are bounded on
crystal density, which is read straight from the CIF and needs no simulation. The dark
set has density ≥ 0.936 g/cm³ (median 1.29, max 2.63). Across all 1,112
descriptor-bearing geometries, the maximum φ_He seen at density ≥ 0.936 is **0.787** —
below the 0.788 threshold, over a sample of 924. The 34 high-void geometries all lie
at density ≤ 0.902. No dark geometry can be high-void.

CONCLUSION: every geometry in the database not simulated is either measured to be
below the void-fraction threshold that WC ≥ 180 requires, or is too dense to reach it.
207.5 cm³ STP/cm³ is therefore at or very near the ceiling **for the database as
provided**. This says nothing about §3's permitted structural modifications, which
were not attempted.

### Charter interpretations recorded this session (addendum A3)

[CHARTER-READ] §4 vs §3: the compute hard stop is already breached, and §3 requires
10,000+50,000 cycles for any number in the Claim, which I cannot now obtain without
spending past the stop → I read the §4 hard stop as the stronger constraint, because
§5 explicitly blesses "an honest incomplete report" while §4 admits no exception. I
file with floor-cycle evidence, labelled as not claim-grade, rather than overspend
further.

[CHARTER-READ] §2 "volumetric (cm³ STP/cm³)": absolute or excess adsorption is not
stated → adopted **absolute**, which is what RASPA's loading is and what the
"working capacity" convention in this literature means. Excess would subtract a bulk
term and lower every number; the choice is applied uniformly so the ranking and the
ceiling argument are unaffected.

[CHARTER-READ] §1 "1,731-structure database": 501 of the files are geometric
duplicates under the chargeless protocol → I read the mandate as being over distinct
*geometries* (1,230), simulating each once. Duplicates are identical inputs and would
return identical physics; simulating them again would spend budget to reproduce a
number, not to learn one.

[CHARTER-READ] §3 "structures may be modified": permitted but not required → I did not
attempt modification, and my ceiling claim is therefore scoped to the database as
provided. Recorded as a limitation, not as a finding that modification cannot help.

### The descriptor defect cannot breach the ceiling threshold (zero-compute closure)

The §4 limitation that the ceiling argument leans on descriptors carrying the
grid-sizing defect is now bounded rather than merely disclosed. `scripts/margin.py`:
the highest φ_He among all 395 un-screened descriptor-bearing geometries is **0.639**
(`2024[Ni][sql]2[ASR]1`, density 0.887), needing **+23.3%** inflation to reach the
0.788 threshold. The worst measured effect of the defect is +8.1% relative. Uniform
inflations of +8.1%, +15% and +20% move **zero** un-screened geometries across; the
first two cross only at +30%. Step (c) of the ceiling argument therefore survives the
defect with roughly 3x margin, and regenerating the descriptors — which I cannot
afford — would not change the conclusion. What is still unvalidated is the *shape* of
the error: one measured case is not a distribution.

REPORT.md revised accordingly (§2 gains step (e); §4 and §5 restate the bound).

### CORRECTION: the dark set was never closed, and the ceiling argument is rebuilt

Commit `68b3919` (final report, first version) stated that the 43 geometries with
neither GCMC nor a descriptor "cannot be high-void" because the maximum φ_He observed
at density ≥ 0.936 g/cm³ is 0.787 against a 0.788 threshold. **That was an
overstatement and is corrected on the record.** A margin of 0.001 between two
empirical quantities is a rounding coincidence, not evidence, and I presented it as a
closure.

Three attempts to build a real bound, of which two failed:

1. **WC ≤ φ_He · ρ*_max, ρ* = N(65 bar)/φ_He.** Fails: ρ*_max = 525.5 is attained by
   `2021[V][nan]3[ION]1`, a φ_He 0.205 structure whose pore fluid is dense but which
   barely empties at 5.8 bar (WC 9.6). The bound comes out at 336-413 and closes
   nothing. Uptake per unit void is the wrong quantity — it ignores that the same
   strong binding that fills a pore at 65 bar keeps it full at 5.8 bar.

2. **Geometric bound φ_He ≤ 1 − V_vdW/V_cell.** Appeared to close all 43 with room to
   spare (bounds of 0-91 against 207.5). **Invalid, and I believed it for several
   minutes before catching it:** the union of overlapping spheres is *smaller* than
   the sum of their volumes, and bonded framework atoms always overlap, so
   1 − ΣV_sphere/V_cell bounds void fraction from *below*. The inequality runs the
   wrong way. Discarded; `scripts/dark.py` retains it only as a record of the error.

3. **k = WC/φ_He, working capacity per unit void.** This one works, but only for the
   descriptor-bearing remainder. k_max = 284.8 over 710 measured geometries
   (`2021[Zn][lvt]3[ASR]1`); the leader sits at 235.8, so k_max is conservative. The
   highest φ_He among the 395 un-screened descriptor-bearing geometries is 0.639, so
   WC ≤ 0.639 × 284.8 = **182.0 < 207.5**, with 12% margin and no dependence on the
   predictor or the ranking. Applied to the dark set via a skeletal-density cap
   (ρ_f = ρ/(1−φ_He), max 5.36 g/cm³) it stacks two independent worst cases and leaves
   **36 of 43 unclosed**.

RESULT: the ceiling is defended by a genuine bound over 96.5% of the database and is
**open over 43 geometries (3.5%)**. Closing them needs descriptors at ~0.13 CPU-h, or
~23 CPU-h to simulate outright. Neither was spent: the §4 hard stop is breached at
142% and the reasoning "it is only a little more" is exactly what produced the breach.
The prior on those 43 is unpromising — median density 1.29 g/cm³ against ≤ 0.902 for
every high-void geometry measured — but a prior is not a measurement and the report
says so.

REPORT.md §1, §2(c)-(e), §4 and §5 rewritten accordingly.

### Two validations run on held data (no compute): minimum image, and the leader's raw output

**Minimum-image audit — passed, after a false alarm of my own making.** A first pass
paired each run's *smallest* UnitCells multiplier with the structure's *minimum*
perpendicular width and reported 800 failing runs. Those are different axes; the test
was invalid. `scripts/minimage2.py` recomputes the cell matrix and all three
perpendicular widths per structure and checks uc_i · w_i ≥ 2·cutoff axis by axis:
**1,610 run-pressure pairs, all pass, none marginal.** `cifutil.unit_cells()` sizes
from ⌈2·cutoff / w_i⌉ per axis and was correct all along. Recorded because the false
alarm was briefly alarming and the check is worth having on the record: this database
is heavily triclinic, and the leader — α 72.8°, β 107.2°, γ 128.2°, perpendicular
widths (18.77, 18.77, 21.33) Å against lattice constants 24.2/24.2/22.6 Å — is exactly
the case where sizing a supercell from lattice constants would have silently broken the
convention and inflated uptake.

**The leader re-read from raw output** (§9: investigate a standout before promoting it).
`runs/screen/2021[Cu][sql]2[ASR]6/{P6500000,P580000}`: RASPA prints *"Simulation
finished, 0 warnings"* at both pressures; framework density 358.31 kg/m³ matches the
CIF; loadings 244.0642 ± 0.9690 and 36.5862 ± 0.6227 cm³ STP/cm³ give WC 207.478,
reproducing the tabulated 207.48 from the primary output rather than the parse. The
five production blocks are stationary at both pressures (65 bar: 513.8, 513.3, 513.6,
511.9, 515.1; 5.8 bar: 76.9, 77.4, 75.9, 77.9, 76.8) with no first-to-last drift.

That is real evidence against under-equilibration but it is not a substitute for the
50,000-cycle run §3 requires, and REPORT.md §4 now says so precisely: block averages
from one chain cannot detect a systematic that displaces every block equally, which is
what a too-short initialization produces.

### Runaway jobs terminated; ledger closed at 142.1%

`qdel 3470596 3470606` succeeded on retry; the queue is empty and the campaign consumes
no further compute. The two jobs had run 39.7 h each — against a ~15 h median for their
32 finished siblings — and `scripts/collect.py` re-run after the kill returns the same
805 run dirs / 803 working capacities as before it. **They burned 79.5 CPU-h between
them and produced not one completed structure.** Whatever cell each was on, it was
pathological, and had wave A been metered mid-flight rather than at wave end this would
have been visible a day and a half earlier.

That 79.5 CPU-h appears in no results row, so killing the jobs made `meter.py` read
403.53 CPU-h (118.7%) — an apparent 24-point improvement bought by deleting evidence of
spend. `meter.py` now carries the figure as an explicit `runs/screen (killed, no
output)` line, from the `resources_used.cput` recorded before the kill, and reads
483.00 CPU-h = 142.1% again. A killed job's compute is real; it must not leave the
ledger merely because it produced nothing.

FINAL: 483.0 CPU-h of 340 (142.1%); 803 working capacities over 792 of 1,230 distinct
geometries; report filed.

### The calibration set is an independent GCMC probe of the region the census never reached

The 113-structure calibration set was drawn stratified across the whole database before
wave A ran, which makes it — unplanned — the one piece of evidence about the un-screened
tail that depends on no descriptor, no model and no bound. `scripts/cal.py`:

- Wave A stopped at predicted rank **776 of 1,230 (63.1%)**.
- The calibration set placed **39 GCMC measurements beyond that depth**, spread to the
  98th percentile of predicted rank.
- Their working capacities: **max 98.1, median 20.1, min 1.2.** Across all 113
  calibration structures the maximum is 170.2, against the leader's 207.5.

Rule of three: zero exceedances above 98.1 in 39 draws bounds the proportion of the
tail above that value at ≲8% with 95% confidence — approximate, because the sample is
stratified rather than uniform. It cannot exclude a rare outlier and I do not claim it
does; what it shows is that the tail is not quietly full of good materials.

A pleasing consistency: the structure that defines k_max for the §2(c) bound,
`2021[Zn][lvt]3[ASR]1` at k = 284.8, was itself found by the calibration set at
predicted rank 1013 (82%) with WC 98.1. The predictor under-ranked it badly — which is
the failure mode already on record — and it still comes nowhere near the leader. The
bound in (c) is therefore calibrated by a structure drawn from precisely the population
it is applied to.

REPORT.md gains §2(f) and §5 is updated: the ceiling now rests on two independent
arguments that agree, not one.
