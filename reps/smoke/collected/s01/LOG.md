# LOG — append-only narrative


## LOG-2026-08-26-01 — Orientation and toolchain verification
Read CHARTER.md, CHARTER_ADDENDUM.md, WORKSPACE.json, AUDIT_SCHEMA.md. Record was
empty (INBOX reports a harness restart; nothing to reconcile against).

Verified the pinned toolchain rather than assuming it:
- `sha256sum toolchain/raspa/share/raspa/forcefield/UFF/*` reproduces all three
  charter §3 hashes exactly.
- `strings toolchain/raspa/lib/libraspa2.so | grep 2.0.3` → `RASPA 2.0.37`.
- A 300-cycle probe run confirms the §3 settings arrive in the engine: output header
  reads `CutOff VDW : 12.800000`, `All potentials are unshifted !!!!!!`, and every
  listed interaction pair carries `tailcorrection: no`.

Cluster: PBS/Torque, server bnode0, 19 compute nodes / 580 cores. `qas` lives at
/usr/local/mjs/qas and takes qsub script paths. Its node-spec validator requires a
three-token `nodes=N:ppn=M:property` form; `nodes=1:ppn=1` alone is rejected. Pinned
all jobs to the `amd` property class (bnode1,2,3,9,10 — 160 cores, near-idle) so that
CPU-second measurements are comparable across the campaign.

## LOG-2026-08-26-02 — Database characterised at zero compute cost
`bin/cifutil.py` + `bin/descriptors.py` → `data/descriptors.csv`, 1731/1731 parsed.
- Names follow CoRE-MOF-2024 convention `YEAR[metal][topology]N[ASR|FSR]idx`.
- All CIFs are P1 and carry a DDEC6 `_atom_site_charge` column. §3 is chargeless, so
  the RASPA-ready CIFs written by `write_raspa_cif` drop that column entirely and
  `ChargeMethod None` / `UseChargesFromCIFFile no` are set.
- Every element present maps onto a pseudo-atom in the pinned UFF set (no gaps).
  Labels are rewritten to the underscore-suffixed UFF names (`Zn_`, `C_`, ...).
- Density range 0.313 – 3.963 g/cm³: **all 1731 sit inside the G3 window 0.20–4.50**,
  so G3s density leg kills nothing. This is consistent with the charters note that
  the bounds are an impossibility filter, not a plausibility filter.
- Simulation-cell size after replication to ≥ 2×12.8 Å in every perpendicular
  direction: median 2448 atoms, p90 3960, max 23166. Cost will vary ~20× across the
  database, so cost-aware ordering matters.

## LOG-2026-08-26-03 — Benchmark batch b0 submitted
8 structures spanning the nsim range at the 2nd/15th/30th/45th/60th/75th/88th/97th
percentiles, `triage` cycles (500 init + 2000 production), both pressures. Purpose is
a cost model (CPU-seconds vs simulation-cell atom count and loading), not a reported
number — no b0 value will be quoted as a measurement.

## LOG-2026-08-26-04 — Energy grids measured and rejected
§3 permits energy grids for screening, so I measured what one costs before adopting it.
`MakeGrid` at RASPA's default 0.1 Å spacing on `2023[Zn][sql]2[ASR]18` (unit cell
9.13 × 18.47 × 16.17 Å, 2.71 M grid points): **189 CPU-seconds and 85 MB** for a single
structure — against roughly 300 CPU-seconds for the entire two-pressure screening run it
was meant to accelerate. Coarsening to 0.2 Å would cut that ~8×, but grid-generation cost
scales as (unit-cell volume) × (atoms within the cutoff), i.e. roughly as V², so the
structures where a grid would help most — the large-celled ones — are exactly where the
grid becomes unaffordable. Disk is the second wall: 1731 structures × even 11 MB is ~19 GB
of scratch to manage.

DECISION: **no energy grids anywhere in this campaign.** Every number, screening included,
comes from direct GCMC summation. A pleasant side effect is that §3's "any grid-based
number promoted to the final report must state so" cannot bite: there are none.

A writable RASPA data root `rw/` was built (symlinks to the read-only toolchain plus a
real `grids/` dir) to run this test, since RASPA writes grids under `$RASPA_DIR`. It is
retained but unused; the three UFF hashes verify identically through the symlinks.

## LOG-2026-08-26-05 — G3 helium leg: the pinned force field has no helium
G3 requires a He void fraction for every structure entering GCMC. The pinned
`pseudo_atoms.def` defines 91 species — `CH4_sp3`, `N_n2`, `C_co2`, `Hw`/`Ow`, the metals,
the UFF organics — and **no helium**. RASPA's Widom-helium route therefore cannot be run
without adding a pseudo-atom to a file whose SHA-256 §3 pins, which would be a protocol
violation for the sake of a diagnostic.

[CHARTER-READ] Appendix A / G3: "He void fraction computed" does not name a method, and the
pinned toolchain forecloses the usual one → adopted a geometric He void fraction, computed
in `bin/geom.py` from the same Lennard-Jones sigmas the protocol itself uses (a point is
He-accessible when |r − r_i| > (σ_i + σ_He)/2 for every framework atom under PBC, with
σ_He = 2.58 Å). Helium enters only as a geometric probe and is never a simulated species,
so the pinned files stay untouched. Reproducible from `bin/geom.py` + the pinned force field.

[CHARTER-READ] Appendix A / G3: "charge balance verified" is directly actionable for
structures *I* modify (that is G5's job) but has no automatable meaning for 1731 unmodified
database entries — the CIFs carry PACMAN/DDEC6 charges that are normalised to zero net by
construction, so summing them verifies nothing → adopted: database structures are taken as
provided by the charter-designated source and are checked on the legs that *are* decidable
(overlap, density, void fraction) at screening scale; the charge-balance leg is discharged
by explicit composition inspection for anything promoted to finalist, and by G5 for anything
I modify.

`bin/geom.py` also returns the framework-framework minimum interatomic distance. The
hydrogen-inclusive minimum sits at 0.93–0.95 Å across the database — those are real C–H
bonds, not clashes — so the overlap test that discriminates is the heavy-atom minimum,
reported separately as `dmin_heavy` (~1.20 Å for sound structures).

Validation on the density extremes of the database:
- `2021[Cu][nbo]3[ASR]2`, the least dense entry (0.313 g/cm³) → vf_he 0.677, vf_ch4 0.585,
  largest included sphere ≥ 16 Å. Highly porous, as it must be.
- `2023[WNdZr][nan]3[FSR]1`, the densest (3.96 g/cm³) → vf_he 0.008, vf_ch4 7e-5. Effectively
  nonporous, as it must be.
The descriptor tracks density in the physically required direction over a 12× density range.

## LOG-2026-08-26-06 — Cost model from b0, and why the screen must be short
b0 (triage cycles, 500 + 2000, both pressures) on 8 structures spanning the simulation-cell
size range. Working capacities, cm³/cm³:

| structure | N(5.8) | N(65) | WC | CPU s (both P) |
|---|---|---|---|---|
| 2021[Cu][nan]3[ASR]1  |  79.4 | 219.7 | 140.2 | 291 |
| 2023[Fe][nan]3[FSR]1  |  53.3 | 142.0 |  88.7 | 663 |
| 2021[V][nan]3[FSR]4   | 145.4 | 212.5 |  67.1 | 857 |
| 2022[CuSi][mmo]2[FSR]1|  86.9 | 114.7 |  27.9 | 199 |
| 2023[Zn][sql]2[ASR]18 |  52.1 |  66.2 |  14.1 | 295 |
| 2021[Cd][nan]2[ASR]1  |  47.7 |  48.5 |   0.8 | 314 |

The physics is behaving: the two structures that saturate below 5.8 bar (Cd, V — dense,
tight-pored, deep wells) deliver almost nothing despite respectable *uptake*, which is the
whole point of a deliverable-capacity target. `2021[Cd][nan]2[ASR]1` is fully loaded at
5.8 bar and delivers 0.8 cm³/cm³.

Cost is not a constant per structure: 199–857 CPU-seconds at triage cycles, driven by
(simulation-cell atom count) × (molecules present), so the expensive structures are the
high-loading ones — i.e. the interesting ones. Mean ≈ 0.13 CPU-h/structure at triage cycles;
extrapolating the charter's own 1.83 CPU-h/structure figure to floor cycles (12,000 vs 2,500)
lands in the same place. An exhaustive screen at *floor* cycles would cost roughly
1,100 CPU-h against a 340 CPU-h budget — the charter is right that it cannot be done.

Batches b1 (floor cycles) and b2 (scout cycles, 150 + 600) on the same 8 structures are
running, to measure how far the cycle count can be cut before the *ranking* degrades. That
measurement, not a guess, will set the screening cycle count.

## LOG-2026-08-26-07 — G4 operationalised, and a check that it tracks real chemistry
G4 makes UFF/TraPPE inadmissible for "structures with exposed metal atoms". The database
ships no coordination metadata, so the test has to be geometric. `bin/oms.py` computes, for
every metal atom and all its periodic images:
- `cn`, the number of bonded non-metal neighbours (Cordero covalent radii + 0.45 Å);
- `theta_open`, the widest coordination gap — over ~600 quasi-uniform directions, the
  largest angle between a direction and the nearest ligand direction;
- `d_probe`, the closest a TraPPE methane centre can actually sit to the metal without
  clashing with any framework atom.

A metal counts as exposed when `theta_open ≥ 60°` **and** `d_probe ≤ 4.2 Å`. Both legs are
needed and the second is what does the real work: a tetrahedral Zn has a 71–74° geometric
gap but is shielded by its own linkers (`d_probe` unreachable), while a Cu paddlewheel has
a 94–97° gap that a methane centre reaches at 3.8 Å.

[CHARTER-READ] Appendix A / G4: "exposed metal atoms" is stated without a numeric criterion,
and the first clause is unqualified while only the second names modification → adopted the
strict reading, that *any* structure carrying a reachable coordinatively-unsaturated metal is
auto-invalid whether or not I created it, with the geometric criterion above. Threshold
sensitivity is reported rather than hidden: the flagged fraction runs 21.5% (θ≥60°, d≤3.8 Å)
to 30.6% (θ≥60°, d≤4.2 Å) to 35.8% (the adopted per-metal count) across defensible settings.

**Result: 620 of 1731 (35.8%) carry at least one exposed metal and are G4-inadmissible.**

This is not a threshold I can tune to taste, so I checked it against chemistry the detector
knows nothing about. The database uses the CoRE-MOF solvent-removal convention: `ASR` = all
solvent removed, *including metal-coordinated solvent*; `FSR` = only free solvent removed,
so coordinated ligands are retained. Uncapping a metal is precisely what ASR does and FSR
does not. If the detector is measuring coordination rather than noise, ASR must be flagged
far more often than FSR:

| class | n | exposed | rate |
|---|---|---|---|
| ASR | 925 | 464 | 50.2% |
| FSR | 751 | 153 | 20.4% |
| ION |  55 |   3 |  5.5% |

and on the 657 **matched ASR/FSR pairs of the same parent structure**, where composition is
otherwise identical: 133 pairs where only the ASR member is flagged, against **6** where only
the FSR member is. A 22:1 asymmetry in the direction the chemistry demands. The detector is
measuring what it claims to measure.

Consequence for the mandate: the search space for a *defensible* best material is the 1111
G4-admissible structures, and the porosity leaders are heavily represented among the excluded
— `2021[Cu][nbo]3[ASR]2` (the least dense entry in the database, vf_ch4 0.585),
`2023[Zr][nbo]3[ASR]1`, `2022[Zr][scu]3[ASR]1`, `2021[Cu][lvt]3[ASR]1` are all flagged. So is
`2021[Cu][nan]3[ASR]1`, the b0 leader at WC 140, whose worst metal is 2-coordinate Cu.
I expect the raw leaderboard and the admissible leaderboard to be materially different, and
the gap between them is itself part of the ceiling answer.

## LOG-2026-08-26-08 — Database hygiene notes from the G3 pass
- Every `_atom_site_occupancy` in all 1731 CIFs is 1.0 (392,704 atom sites checked): no
  partial occupancy or disorder to resolve, so no overlap artefacts from that source.
- Hydrogen-inclusive minimum interatomic distances cluster at 0.93–0.95 Å across the whole
  database — real C–H bonds. The discriminating overlap test is the heavy-atom minimum,
  which sits near 1.20 Å for sound structures; 4 structures fall below 0.90 Å and 12 below
  1.00 Å, and those are the G3 overlap candidates.
- The database contains exact duplicate pairs (e.g. `2021[Cu][sql]2[ASR]6` and
  `...[FSR]6`, `2021[Cd][kag]3[ASR]1` and `...[FSR]1`) with identical descriptors — i.e.
  parents that had no coordinated solvent to remove, so ASR and FSR coincide. Any
  leaderboard must not treat these as independent confirmations of each other.

## LOG-2026-08-26-09 — The screen is a ranking device, not a source of reported numbers
§3 sets a floor of 2,000 initialization + 10,000 production for **any reported number**. The
S1 screen runs at 150 + 600, which is far below that. This is deliberate and it constrains
how S1 may be used.

[CHARTER-READ] §3 cycle counts: the floor governs *reported numbers*, and is silent on
internal triage → adopted: S1 values are an ordering device only. **No S1 value is quoted
anywhere as a measurement of a working capacity.** Every number that appears in the report
as a measurement comes from a run at floor cycles or above, and every number in the Claim
comes from 10,000 + 50,000. Where the report needs to characterise the screen, it does so as
"sub-floor triage estimate" with its measured error attached, never as a protocol-grade value.

This creates a real obligation for the *ceiling* half of the mandate. Saying "nothing else in
the database beats the leader" needs evidence about all 1731, but only the promoted handful
will carry floor-grade numbers. The bridge has to be a **measured** scout→floor error, not an
assumed one. Two things supply it:

1. b0/b1/b2 — the same 8 bench structures at scout (150+600), triage (500+2000) and floor
   (2,000+10,000) cycles. Small sample, full cycle ladder.
2. S2 will re-run the top ~120 at floor cycles, giving ~120 paired scout/floor points — but
   only at the top of the range, where the paired sample is biased by selection.

Neither bounds the risk that a *low-ranked* structure is secretly a leader. So S2 also takes
a **stratified random sample across the whole S1 range**, floor-graded, whose only job is to
measure the scout→floor error where the screen said "not interesting". That sample, not an
assumption, is what will license or refuse the ceiling claim. G7's random audits contribute
to the same denominator.

## LOG-2026-08-26-10 — RASPA seeds from the clock, so G6 reproduction is meaningful
Checked rather than assumed, because G6 would be vacuous if repeat runs were bit-identical.
Two runs of `2023[Zn][sql]2[ASR]18` at p65, same simulation.input, same CIF, run back to
back: **60.96** and **56.14** cm3/cm3 (scout cycles; block sigmas 9.03 and 2.57). The output
header carries `Random number seed: 1787728036` -- RASPA takes the seed from the clock when
none is given, so an unmodified rerun is a genuinely independent sample.

Two consequences:
- G6 finalist reproduction is a real test, not a file-copy check. Reproduction runs will use
  the archived inputs unchanged and rely on this independent seeding.
- The run-to-run scatter at scout cycles is of the same order as the block sigma, i.e. the
  screen's noise is honest statistical noise and not an artefact. The ASR/FSR exact-duplicate
  pairs in the database (identical structures under two names) give a free, unplanned
  replicate set for quantifying that scatter across the whole screen, and will be used for it.

Also confirmed the extracted quantity is the right one: the harvested line is
`Average loading absolute [cm^3 (STP)/cm^3 framework]`. RASPA also prints an *excess* loading
which is meaningless here (it is computed against `HeliumVoidFraction`, left at 1.0, so it
prints negative); nothing downstream reads it. Charter s2 defines the target as N(65) - N(5.8)
absolute, volumetric, which is what `bin/collect.py` computes.

## LOG-2026-08-26-11 — Budget reality check, and why exhaustive screening is nearly free
Ratio-estimated the full S1 cost from 185 completed runs against a physical proxy
(simulation-cell atom count x molecules present): **~153 CPU-h**, 45% of budget, with a
28-66% model error. Two facts about the shape of that cost decide the whole campaign plan:

- **The top 5% of structures carry 55% of the predicted cost; the cheapest 50% carry 15%.**
  Cost scales with porosity, because porosity is what puts molecules in the box.
- Therefore a porosity-filtered screen saves almost nothing: cutting the 866 structures below
  vf_ch4 = 0.05 would remove roughly 15% of the cost while destroying the exhaustiveness that
  the ceiling half of the mandate rests on.

DECISION: keep the screen exhaustive over all 1731. Exhaustive coverage is, here, nearly free
relative to any filtered alternative, and it is the strongest available defence of a ceiling
claim.

Cycle-cost ladder, measured, not assumed: scout 750 cycles, floor 12,000 (16x), Claim-grade
60,000 (80x). `2022[CuSi][mmo]2[FSR]1` cost 60.8 CPU-s at scout and 1,130 CPU-s at floor --
18.6x, matching the cycle ratio. Consequence: a *porous* finalist costing ~500 CPU-s at scout
costs ~2.2 CPU-h at floor and ~11 CPU-h at Claim grade. Claim-grade runs on many candidates
are not affordable; two or three finalists are.

Revised allocation: S1 ~150, G7 ~6, S2 floor-grade on ~35 structures ~55, S3 Claim-grade on
2-3 finalists plus their G6 reproductions ~40, contingency ~40. Total ~305 of 340.

[CHARTER-READ] Appendix A / G7: "the full G6-grade audit" on every 40th passing structure.
Read literally as *Claim-grade cycles*, ~27 audits would cost several hundred CPU-h and be
impossible; the charter's own note prices G7 at "on the order of 1.7% of the compute budget"
(~5.8 CPU-h), which is about one two-pressure screening run per audit -> adopted: a G7 audit
reproduces **that structure's own archived screening input in a fresh independent run** (which
is exactly what G6 specifies -- "reproduced from archived inputs in a fresh run") and re-runs
its G3/G4 structural checks. Grade of cycles follows the number being audited, not the Claim.

## LOG-2026-08-26-12 — First screening results, and a free replicate validation
73 structures complete. Provisional top of the sub-floor ranking (values are triage
estimates, not reported measurements -- see LOG-09):

| structure | N(5.8) | N(65) | WC (triage est.) | G4 |
|---|---|---|---|---|
| 2021[Cu][sql]2[FSR]6 | 36.6 | 244.3 | 207.7 | exposed |
| 2021[Cu][sql]2[ASR]6 | 35.8 | 242.6 | 206.8 | exposed |
| 2021[Al][nan]3[ASR]24 | 61.1 | 256.8 | 195.7 | tbd |
| 2023[Cu][nan]3[ASR]8 | 57.4 | 245.1 | 187.6 | tbd |
| 2023[Cu][nan]3[ASR]7 | 54.3 | 241.3 | 187.0 | tbd |

The first two rows are the same structure under two names -- an exact ASR/FSR duplicate
(LOG-08), run as two independent clock-seeded simulations. They agree to **0.92 cm3/cm3**
on a working capacity of ~207, against a combined block sigma of 6.1. The screen's
reproducibility is therefore better than its own quoted statistical error, at the top of the
range where it matters. This was free: it fell out of a database redundancy rather than
costing a validation run.

Both are Cu-based and carry exposed metal, so G4 excludes them from any claim. That is the
pattern LOG-07 predicted, appearing immediately at the top of the leaderboard.

## LOG-2026-08-26-13 — G3 overlap threshold set, and shown not to matter
The heavy-atom minimum interatomic distance across the database has a clear tail:
0.828 (x2), 0.889, 0.895, 0.920 (x2), 0.921 (x2), 0.952 (x2), 0.989 (x2), then a jump to
1.017 and above. The shortest genuine heavy-atom bond in any framework chemistry is about
1.10 A, so everything in that tail is a refinement artefact rather than a bond.

Threshold set at **1.00 A**, killing 12 structures as `overlapping_atoms`. The charter's note
on the G3 density bounds says G3 rejects structures that cannot be real, not structures that
are unusual, and the same principle applies here -- so the threshold is set permissively
rather than at the more defensible-looking 1.05 A.

The choice has **no bearing on the campaign's answer**, and that is worth stating rather than
leaving implicit: all 12 affected structures have vf_ch4 <= 0.068 (most below 0.05) and
densities of 1.15-3.10 g/cm3. They are dense and effectively nonporous; none could carry a
competitive working capacity at any threshold. Recorded so that the gate has a documented
denominator, not because it changes an outcome.

## LOG-2026-08-26-14 — Operational: reached the 50-job cap exactly; corrected
Submitting the 4-job equilibration batch on top of a feeder already holding 46 jobs brought
my scheduler count to exactly **50** -- the charter §4 ceiling. At the limit, not over it, but
with zero headroom for any further ad-hoc submission, which is not a safe way to run.

Corrected on the record rather than silently: the feeder was restarted with `MAXQ=42`,
leaving 8 slots free for audit and finalist batches. Note for anyone repeating this: `pkill`
on this cluster is not the procps utility and takes different arguments -- the first kill
attempt silently did nothing and left **two** feeders running simultaneously, which would
have over-submitted. Found with `ps -u Bei -o pid,args`, and the old feeder killed by PID.
Queue verified back to a single feeder afterwards.

## LOG-2026-08-26-15 — Provisional: the ceiling has an interior optimum in porosity
First 115 screened structures, binned by methane-accessible volume fraction (triage
estimates, not reported measurements):

| vf_ch4 | n | median WC | median N(65) | median N(5.8) |
|---|---|---|---|---|
| 0.00-0.15 | 47 |  74.8 | 186.8 | 105.1 |
| 0.15-0.25 | 33 | 132.7 | 211.7 |  87.8 |
| 0.25-0.32 | 18 | 161.5 | 222.9 |  59.2 |
| 0.32-0.40 |  9 | **185.6** | **236.9** |  53.3 |
| 0.40-1.00 |  8 | 168.7 | 197.1 |  29.6 |

Working capacity does **not** increase monotonically with porosity. It peaks near
vf_ch4 ~ 0.32-0.40 and then falls. The two columns to the right show why, and they move in
opposite directions:
- N(5.8) falls monotonically with porosity (105 -> 30). More open pores bind methane more
  weakly, so less is stranded below the discharge pressure. This is the term that *helps*.
- N(65) rises to a maximum at vf_ch4 ~ 0.32-0.40 (237) and then **collapses** (197). Past
  that point the framework has removed so much material per unit volume that there is not
  enough surface left to hold methane at 65 bar. This is the term that *bites*.

Volumetric working capacity is a difference of these two, and the trade-off between them is
what puts a ceiling on it. The same shape appears against cavity size: median WC 76 below
9 A, 138 at 9-11 A, 161 at 11-13 A, 163 at 13-20 A -- rising then flattening.

**Provisional, and here is the caveat that matters.** S1 runs in ascending-density order, so
these 115 are the *least dense* structures in the database. The low-vf_ch4 bin here is not a
representative sample of low-porosity structures -- it is the subset of low-density
structures that are nonetheless poorly accessible, which is an odd population. The bin
medians are informative within themselves, but the shape must be re-derived on the complete
screen before it carries any weight in the report. Recorded now because if this survives the
full screen it is the physical account of the ceiling, and because recording it now makes it
falsifiable by my own later data rather than fitted to it.

## LOG-2026-08-26-16 — Protocol detail recorded: pressures are converted to fugacities
Checked what RASPA actually imposes, since "N(65 bar)" could mean pressure or fugacity and
the difference is not small at 65 bar. Output header for a p65 run:

    Partial pressure:      6500000.0000 [Pa]
    Fugacity coefficient:        0.8730 [-]
    Partial fugacity:      5674321.7984 [Pa]

RASPA computes a Peng-Robinson fugacity coefficient from the critical constants carried in
the pinned `TraPPE/methane.def` (Tc 190.564 K, Pc 4.5992 MPa, omega 0.01142) and imposes the
*fugacity*. At 65 bar the coefficient is 0.873, a 13% correction; at 5.8 bar it is close to 1.

This is not a choice I made and not one I can make: the molecule definition is part of the
pinned toolchain, so every number produced under §3 -- mine and the reference set the gate
thresholds were calibrated against -- carries the same treatment. Recorded so the report can
state plainly that "65 bar" means an imposed fugacity of 5.674 MPa under the pinned
Peng-Robinson conversion, rather than leaving a reader to assume ideal-gas pressure.

Also re-verified the pressures themselves against §2: p05 = 580,000 Pa (5.8 bar),
p65 = 6,500,000 Pa (65 bar), temperature 298 K, and the harvested quantity is
`Average loading absolute [cm^3 (STP)/cm^3 framework]`.

## LOG-2026-08-26-17 — Guest-molecule check on the leaders, and what it can and cannot settle
Built `bin/frags.py`: periodic connected-component analysis that tracks the lattice
translation accumulated along each path, so a component that closes on itself with a non-zero
net translation is the (periodic) framework and one that closes with zero translation
everywhere is a finite molecule sitting in the pore. This matters because a CIF still
containing solvent or template is not the adsorbent it appears to be -- guests occupy pore
volume, so N(65) would be measured on a partly blocked structure.

Result on the four current leaders: **no discrete molecules in any of them.**
- `2023[Cu][ctn]3[FSR]1` -- one periodic component, all 366 atoms, C120Cu6H144N72S24
- `2021[Cu][sql]2[FSR]6` -- **two** periodic components, C64Cu2H48N8 each: an interpenetrated
  (catenated) pair of independent nets, not a framework plus a guest
- `2021[Cd][kag]3[ASR]1` -- one component, C120Cd6H72N36O24
- `2023[Hf][hcp]3[ASR]1` -- one component, C288H172Hf24O116

Note this check can only produce good news in one direction: trapped guests *reduce* working
capacity by blocking pores, so their absence removes a way of *under*-stating a candidate, not
a way of over-stating one. It is not a source of false positives.

Linker chemistry of the current top admissible candidate, obtained by deleting the metals and
re-fragmenting: 8 x C15H18N9S3 per cell against 6 Cu, with every S bonded to exactly one C
and one Cu (24 S, 6 Cu x 4 = 24 -- every Cu is CuS4, tetrahedral, Cu-S 2.32 A), plus NH2 and
CH3 groups and N-N linkages on the organic part.

**What this does not settle.** Formal oxidation states cannot be read off coordinates. Whether
the S donors are neutral thione or anionic thiolate decides whether this framework is neutral
or requires counter-ions, and both are chemically plausible for a Cu/S/N framework. The
DDEC6 charges shipped in the CIF cannot arbitrate it: PACMAN normalises them to zero net by
construction, so they would look identical either way. Per LOG-05 the charge-balance leg of G3
is discharged for unmodified database entries by provenance -- the structure is used exactly
as the charter-designated source provides it -- and this ambiguity will be stated plainly in
the report's limitations rather than papered over.

## LOG-2026-08-26-18 — The screen does not under-equilibrate the porous structures
This was the failure mode that could have invalidated everything. 150 initialization cycles
is short, and if it were too short to fill a large open pore, the screen would systematically
*understate* N(65) for exactly the high-porosity structures it exists to find -- and a
depressed leader would look like a settled ceiling. The b0/b1/b2 bench ladder could not rule
it out: all six bench structures have vf_ch4 < 0.20.

Floor-cycle rerun of the screen leader, `2021[Cu][sql]2[FSR]6` (vf_ch4 0.408, the most porous
class in the database):

| cycles | N(5.8) | N(65) | WC | sigma |
|---|---|---|---|---|
| scout 150+600 | 36.641 | 244.331 | 207.689 | ±4.38 |
| floor 2,000+10,000 | 36.905 | 243.279 | **206.374** | ±1.00 |

**Delta = -1.32 cm3/cm3 on a working capacity of 206, i.e. 0.6%**, and inside the screen's own
error bar. Both pressures move by ~1 unit and in opposite directions, which is scatter, not a
trend. There is no equilibration bias at the porous end.

Cost of that one floor run: 8,928 CPU-s (2.48 CPU-h), 16x the scout run, exactly as the cycle
ratio predicts.

Combined with the bench-ladder fidelity (bias +0.57, sigma 2.69 over six structures spanning
WC 1-141) this is now measured at both ends of the range. The screen's ranking can be trusted
to a few cm3/cm3, which is the precondition for using it in a ceiling argument.

## LOG-2026-08-26-19 — The database is 1230 distinct structures, and that buys 499 free replicates
Hashed every CIF on its cell parameters plus its sorted (element, x, y, z) list:

    distinct structures: 1230 of 1731
    501 redundant copies in 459 groups (434 pairs, 8 triples, 17 quadruples)
    group composition: 404 x (ASR,FSR), 26 x (FSR,FSR), 17 x (ASR,ASR,FSR,FSR), 3 x (ASR,ASR), 1 x (ION,ION)

Two consequences, one bad and one very good.

**The search space is smaller than advertised.** The mandate names a 1,731-structure database;
it contains **1,230 distinct structures**. The redundancy is overwhelmingly ASR/FSR pairs
whose parent had no metal-coordinated solvent to remove, so "all solvent removed" and "free
solvent removed" produce byte-identical geometry. Any leaderboard or count in the report must
say which number it is using; treating duplicate entries as independent hits would inflate
apparent agreement.

**Every duplicate is a free independent replicate.** RASPA seeds from the clock (LOG-10), so
the two copies were screened as two genuinely independent simulations of the same structure.
That yields **499 replicate pairs with both members screened** -- an unplanned validation set
two orders of magnitude larger than my 6-structure bench ladder, spanning the entire database
rather than a chosen corner of it:

| quantity | value |
|---|---|
| mean difference between duplicates | **+0.073 cm3/cm3** (no detectable bias) |
| sd of the difference | 3.076 |
| implied **per-run sigma** | **2.175 cm3/cm3** |
| median absolute difference | 1.69 |
| p90 / p99 / max absolute difference | 5.26 / 9.36 / **11.46** |
| same, restricted to WC > 140 (23 pairs) | per-run sigma **1.88** |

The screen is unbiased and reproducible to about 2 cm3/cm3 per run, and it is no worse at the
top of the range than in the middle.

A third finding falls out: the **median block sigma RASPA quotes for WC is 6.53**, against a
true run-to-run sigma of 2.18. RASPA's 5-block error bar **overstates** the real scatter by
roughly 3x on these runs. Reporting the block sigma as the uncertainty would be conservative,
not optimistic -- worth knowing, since it means the finalist uncertainty should come from
independent repeats rather than from a single run's block statistics.

This measurement is what makes the ceiling argument quantitative rather than rhetorical. For
a structure the screen placed at WC = X to actually beat a leader at 206, the screen would
have to have erred by (206 - X). At sigma ~ 2.2, with the largest deviation seen across 499
independent pairs being 11.5, structures screening below ~180 cannot be hidden leaders.

## LOG-2026-08-27-20 — Screen complete; gates applied to all 1731
Network outage 2026-08-26 ~21:10 KST to 2026-08-27 ~07:05 KST (~10 h) cut all access: the
route to the workspace is a ProxyJump through a gateway (143.248.130.178) and both that host
and the cluster stopped answering ICMP and TCP/22. Diagnosed from this end as a network-level
fault on or upstream of the gateway, not a cluster fault. **The charter's only escalation
channel is a file inside the workspace, so an access outage is precisely the failure it cannot
be used to report** — the `[ESC: infra]` line below is therefore filed retroactively.

The campaign was unharmed. PBS kept running on the compute nodes, and the screen **completed
during the outage: 3,462/3,462 runs, zero failures.**

**S1 complete: 1,731 structures screened at 150+600 cycles, both pressures.**

Gate results over the full screen (`bin/gates.py`, AUDIT.jsonl):

| gate | outcome | n |
|---|---|---|
| G3 | overlapping_atoms (heavy-atom minimum < 1.00 Å) | 12 |
| G4 | exposed_metal | 619 |
| — | **passed** | **1,100** |
| G7 | selected for random audit (every 40th passing structure) | 27 |

Final screening leaderboard, G3+G4 admissible (sub-floor triage values, not reported
measurements):

| structure | WC | vf_ch4 | ρ |
|---|---|---|---|
| 2023[Cu][ctn]3[FSR]1 | 177.8 | 0.299 | 0.506 |
| 2023[Cu][ctn]3[ASR]1 | 176.9 | 0.299 | 0.506 |  ← exact duplicate of the above
| 2021[Th][fcu]3[FSR]1 | 166.4 | 0.284 | 0.931 |
| 2021[Cu][pcu]3[ASR]3 | 158.9 | 0.276 | 0.621 |
| 2021[U][cds]3[FSR]1  | 156.9 | 0.163 | 0.912 |
| 2022[U][srs]3[FSR]1  | 154.3 | 0.451 | 0.627 |

versus the raw leaderboard, led by G4-inadmissible structures: 2021[Cu][sql]2[FSR]6 at 207.7,
2021[Al][nan]3[ASR]24 at 195.7, 2023[Cu][nan]3[ASR]8 at 187.6 — all carrying exposed metal.

**A margin correction to my earlier reasoning.** I previously estimated the gap from the
admissible leader to the runner-up as ~21 cm³/cm³, reading the runner-up off a partial screen.
On the complete screen the nearest *distinct* competitor is `2021[Th][fcu]3[FSR]1` at 166.4,
so the true margin is **11.4 cm³/cm³** — and the largest deviation observed across the 499
duplicate pairs is 11.46. The margin is the same size as the worst screening excursion I have
measured. That is not a safe margin to assert a ceiling on, so the top admissible candidates
must be floor-graded rather than ranked on screening values alone.

## LOG-2026-08-27-21 — Two defects in the first audit batch, corrected
Found immediately after writing the 658 gate lines, recorded rather than quietly repaired:

1. **`commit` field reads `uncommitted` on all 658 lines.** `bin/audit.py` obtained the hash
   with `git -C <root> rev-parse`, and this cluster ships a git old enough to reject `-C`
   (exit 129). The call failed silently into the fallback. The batch corresponds to commit
   **4c690fa**. `audit.py` now uses `cwd=` instead, verified working. A single correction line
   is appended to AUDIT.jsonl rather than 658 of them: the defect is uniform and mechanical,
   the gate/outcome/disposition fields are all correct, and re-emitting the batch would double
   the file without adding information.

2. **The `note` on G4 lines can quote a non-triggering metal.** `oms.py` reports `theta_open`
   and `d_probe` for the widest-gap metal in the structure, which is not always the metal that
   tripped the gate — so some notes read "methane centre reaches 99.0 Å" (the unreachable
   sentinel) beside a positive exposed-atom count. The operative field, `n_exposed`, is
   correct in every case and is what the gate decided on. Cosmetic in effect, but it would
   mislead a reader of the audit trail, so it is stated here.

[ESC: infra / Gateway 143.248.130.178 unreachable 2026-08-26 21:10 – 2026-08-27 07:05 KST, blocking all workspace access; filed retroactively since ESCALATIONS.md lives inside the unreachable workspace. No action needed, recorded for the record.]

## LOG-2026-08-27-22 — Modification experiment: a prediction made before the result
§3 permits modification of database candidates if the result is charge-balanced and
reproducible from the repository. The screen itself says what modification to try, and it
says so *quantitatively*, which is what makes this a test rather than a fishing trip.

**The prediction.** LOG-15/S1 put the volumetric optimum at vf_ch4 ≈ 0.40–0.48, with N(65)
collapsing beyond it and N(5.8) falling monotonically throughout. The finalist
`2023[Cu][ctn]3[FSR]1` sits at **vf_ch4 = 0.299 — below the optimum**. So the screen predicts
that removing pore-lining bulk from this specific structure should raise its working capacity,
by moving it up the rising limb of a curve I measured before choosing the modification.

**The modification.** `bin/modify.py` strips all 24 methyl groups and caps each anchor carbon
with H at 1.09 Å along the original C–C direction:

    C120Cu6H144N72S24  ->  C96Cu6H96N72S24        (-24 C, -48 H; 24 CH3 out, 24 H in)
    density 0.5058 -> 0.4604 g/cm3

Charge balance is by construction, not by argument: methyl and hydrogen are both neutral
monovalent substituents on carbon, so no formal charge changes anywhere, no counter-ion is
created or destroyed, and no metal coordination sphere is touched. This sidesteps the charge
ambiguity that LOG-17 flagged for this framework — whatever the parent's formal charge is,
the modification does not change it.

**Gate checks on the modified structure, all passed:**

| | pristine | stripH |
|---|---|---|
| G3 heavy-atom minimum | 1.244 Å | 1.244 Å |
| G3 density | 0.506 | 0.460 g/cm³ (inside 0.20–4.50) |
| **G4 exposed metals** | 0 | **0** — Cu remains CuS4, unreachable |
| discrete guest molecules | 0 | 0 (single periodic component) |
| vf_ch4 | 0.299 | **0.335** (toward the optimum, as intended) |
| Henry constant k_H | 8.97 | **6.35** (weaker binding) |
| deepest site u_min | −1721.7 K | **−1493.2 K** |

Every descriptor moved the way the hypothesis requires: more accessible volume, weaker
low-pressure binding. Whether that converts into working capacity is the actual question and
the descriptors cannot answer it — N(65) has to be paid for out of the same surface that was
just removed.

**G5 compliance.** The matched pristine control is run in the same batch, at identical floor
cycles and identical settings, rather than relying on the earlier `eq` run of the same
structure. Both numbers therefore come from the same batch and the comparison is like-for-like.

Submitted as batch `mod` at floor cycles. **Recorded before the result is known**, so that the
prediction is falsifiable by my own data rather than fitted to it.

## LOG-2026-08-27-23 — The ceiling mechanism, re-derived on the complete screen
LOG-15 recorded the porosity/capacity relation as provisional and explicitly flagged that it
had to be re-derived on the full screen before carrying weight, because the ascending-density
run order made the partial sample unrepresentative. Re-derived now on all 1,731:

| vf_ch4 | n | median WC | median N(65) | median N(5.8) |
|---|---|---|---|---|
| 0.00–0.05 | 991 |  26.4 | 105.0 | 76.2 |
| 0.05–0.10 | 354 |  69.5 | 165.5 | 94.3 |
| 0.10–0.18 | 188 |  93.6 | 203.6 | 104.6 |
| 0.18–0.25 | 101 | 132.7 | 218.6 | 77.2 |
| 0.25–0.32 |  59 | 152.2 | **221.9** | 62.4 |
| 0.32–0.40 |  27 | **165.5** | 206.0 | 42.0 |
| 0.40–0.48 |   6 | 161.6 | 195.5 | 32.7 |
| 0.48–1.00 |   5 | 159.0 | 188.6 | 28.4 |

The shape survives: N(5.8) falls monotonically with porosity, N(65) rises to a maximum and
then declines, and their difference peaks in between. **The mechanism is confirmed. The
location moved**: the optimum sits at vf_ch4 ≈ **0.32–0.40**, not the 0.40–0.48 the partial
sample suggested, and N(65) turns over earlier still, at 0.25–0.32.

**This corrects the rationale I logged for the modification experiment (LOG-22), and I am
flagging it rather than letting it pass.** That entry justified stripping methyls from the
finalist by citing an optimum of 0.40–0.48 against the finalist's 0.299. The optimum is
actually 0.32–0.40. The *prediction is unchanged and is now better supported*, not worse: the
modification takes vf_ch4 from 0.299 to 0.335, which lands inside the corrected peak bin
rather than merely pointing toward a more distant one. But the number I reasoned from was
wrong when I wrote it, and the result is still pending, so this is recorded before it lands.

## LOG-2026-08-27-24 — G4 is concentrated at the top, and that is the ceiling answer
Across the whole database, 36% of structures carry an exposed metal and are G4-inadmissible.
**Among the top 40 by screening value, 37 of 40 — 92% — are inadmissible.**

That is a 2.6× enrichment, and it is not a coincidence of the gate: the same structural move
that creates a high volumetric working capacity in this database (stripping coordinated
solvent off a metal node to open the pore) is the move that leaves the metal coordinatively
unsaturated. The ASR/FSR asymmetry in LOG-07 is the same effect seen from the other side.

The consequence for the mandate's second half is direct, and it is a *protocol* ceiling rather
than a *materials* ceiling: the highest methane capacities this database can offer sit
overwhelmingly in structures that UFF/TraPPE is not entitled to describe. The best admissible
number is not limited by the absence of better materials — the better materials are right
there, at 187–208 cm³/cm³ — but by the force field's inability to describe an open metal site
with dispersion alone. Raising the ceiling therefore means changing §3, which is exactly what
§3 forbids.

## LOG-2026-08-27-25 — G7 random audits: 27/27 reproduce, and they loosen my error estimate
G7 selected every 40th structure to pass screening, by screening rank and regardless of value
-- 27 structures spanning WC 0.6 to 128.6. Each was rerun from its own archived screening
input as a fresh, independently seeded simulation (LOG-11 records why that is the right grade
for this gate, and LOG-10 records why a rerun is genuinely independent).

**All 27 reproduced. 27/27 passed**, against an acceptance band of +/- 3x the measured
run-to-run sd of these same audits -- a band derived from the campaign's own reproducibility
rather than a tolerance picked to let things through.

| quantity | value |
|---|---|
| mean (audit - screen) | **+0.222 cm3/cm3** -- unbiased |
| sd of the difference | 4.402 |
| implied per-run sigma | **3.112** |
| max absolute deviation | 8.40 |

**This is a looser number than the duplicate-pair estimate and I am using the looser one.**
LOG-19 measured per-run sigma = 2.175 from 499 exact-duplicate pairs; this independent
27-audit sample gives 3.112. With n=27 the sd carries roughly 14% relative uncertainty
(3.11 +/- 0.43), so the two estimates sit about two standard errors apart -- not a
contradiction, but not agreement either, and the honest move is to carry the conservative
value forward rather than the flattering one.

**That has a direct consequence for the ceiling claim.** Combining sigma_screen = 3.11 with
the measured screen-to-floor sigma of 2.69 gives a total of about 4.1 cm3/cm3. The gap from
the admissible leader (177.8) to the nearest distinct competitor (166.4) is 11.4 -- only
**2.8 sigma**. Under the optimistic 2.18 estimate it would have looked like 3.6 sigma and
comfortable. It is not comfortable. Ranking the top of the admissible field on screening
values alone would not have been defensible, and the S2 floor-cycle batch now running on the
top five admissible structures is what will actually settle the order.

## LOG-2026-08-27-26 — Modification result: the prediction holds, and the mechanism is visible
Batch `mod`, floor cycles, with the G5 matched pristine control run in the same batch under
identical settings:

| structure | N(5.8) | N(65) | **WC** |
|---|---|---|---|
| `2023[Cu][ctn]3[FSR]1` (pristine, `mod` batch) | 45.327 ± 0.225 | 223.049 ± 0.693 | **177.722 ± 0.728** |
| `2023[Cu][ctn]3[FSR]1` (pristine, `eq` batch, independent) | 45.717 ± 0.557 | 223.406 ± 0.745 | **177.689 ± 0.931** |
| `2023[Cu][ctn]3[FSR]1__stripH` (24 methyls -> H) | 33.827 ± 0.712 | 221.474 ± 0.637 | **187.647 ± 0.956** |

**Gain: +9.93 cm3/cm3 (+5.6%)** against a combined uncertainty of ~1.2 -- roughly 8 sigma.
The prediction logged in LOG-22 *before* the run is confirmed.

The pristine control also reproduced across two independent batches to **0.033 cm3/cm3**
(177.689 vs 177.722), which is a stronger floor-grade reproduction than anything the campaign
had so far.

**The mechanism is visible in the split, and it is the one the screen predicted.**
- N(5.8): 45.33 -> 33.83, a fall of **11.5**
- N(65): 223.05 -> 221.47, a fall of only **1.6**

Essentially the entire gain comes from *not stranding* methane below the discharge pressure,
not from holding more at 65 bar. That is exactly the trade-off the binned screen data
described: in this porosity range N(5.8) is still falling steeply with accessible volume while
N(65) has already flattened, so removing pore-lining bulk buys a large reduction in the
stranded term for a small cost in the delivered one. The modification did not find some new
adsorption chemistry; it moved this structure along a curve I had already measured.

## LOG-2026-08-27-27 — A falsification test, submitted with its prediction
Surveying the other top admissible candidates for strippable sites, only one has any:

    2021[Th][fcu]3[FSR]1   none        2021[Cu][pcu]3[ASR]3   none
    2021[U][cds]3[FSR]1    none        2023[Zr][hcp]3[FSR]1   none
    2023[Hf][hcp]3[ASR]1   none        2021[Eu][fcu]3[FSR]1   none
    2022[U][srs]3[FSR]1    72 methyls

and it is the interesting case, because `2022[U][srs]3[FSR]1` sits at **vf_ch4 = 0.451 --
already past the 0.32-0.40 optimum**. Stripping takes it to 0.465, further past.

This distinguishes two explanations of the first result that the Cu[ctn] experiment alone
cannot separate:
- *"stripping bulk always helps"* -> U[srs] should also gain ~10 cm3/cm3;
- *"stripping moves a structure along a curve with an interior optimum"* (my account)
  -> U[srs] should gain nothing, and may lose.

**Prediction, recorded before the run: no gain, plausibly a small loss.** If U[srs] gains
substantially, my ceiling mechanism is wrong and the report will say so.

    C576H432O192U24 -> C504H288O192U24   (72 CH3 out, 72 H in; charge-neutral by construction)
    density 0.6268 -> 0.5876 g/cm3
    G4 exposed metals 0 -> 0 (U stays 11-coordinate, unreachable);  dmin_heavy 1.30 A;
    single periodic component, no discrete guests

G5 control: the pristine `2022[U][srs]3[FSR]1` is already being floor-graded in batch S2 at
identical cycles and settings.

## LOG-2026-08-28-28 — Final results: Claim-grade finalists, S2 promotion, falsification test
Second network outage 2026-08-27 ~08:00 to 2026-08-28 ~07:25 KST (~23 h). All queued work
survived and completed on the compute nodes: **3,620 GCMC runs across the campaign, zero
failures.**

**A collector bug, found and fixed.** `bin/collect.py` located replicate directories with
`glob.glob(sd + "/p05_r*")`. Structure stems contain `[` and `]`, which glob reads as character
classes, so the pattern matched nothing and both Claim-grade batches initially collected as
**zero rows** despite having completed. Silent, and it would have looked like the runs failed.
Replaced with `os.listdir` + prefix match in both places glob was used over structure names.
No number was affected -- the bug only prevented reading results, and was caught because 4/4
DONE files contradicted 0 rows.

### Claim-grade (10,000 + 50,000), each with its G6 reproduction

| structure | rep 0 | rep 1 | mean | conservative sigma |
|---|---|---|---|---|
| `2023[Cu][ctn]3[FSR]1` (parent, G5 control) | 177.531 | 177.545 | **177.538** | ±0.39 |
| `2023[Cu][ctn]3[FSR]1__stripH` (finalist) | 187.853 | 187.653 | **187.753** | ±0.42 |

Reproductions differ by 0.015 and 0.199 cm3/cm3. The quoted sigma is the single-run block sigma
propagated and divided by sqrt(2) -- deliberately conservative, since LOG-19 showed block
sigmas overstate true scatter ~3x and an n=2 standard error of the mean is not trustworthy.
Floor-grade values (177.69/177.72 and 187.65) sit within 0.16 and 0.11 of the Claim-grade
means, so the cycle floor was already converged.

### S2: nothing overtook the leader
Floor-grade confirmation of the top five distinct admissible structures:

    2023[Cu][ctn]3[FSR]1  177.7   (leader, Claim-graded above)
    2021[Th][fcu]3[FSR]1  168.01  (screen 166.4, +1.60)
    2021[Cu][pcu]3[ASR]3  158.93  (screen 158.9, +0.00)
    2021[U][cds]3[FSR]1   157.68  (screen 156.9, +0.80)
    2023[Zr][hcp]3[FSR]1  151.46  (screen 153.0, -1.51)
    2022[U][srs]3[FSR]1   150.82  (screen 154.3, -3.47)

The margin to the runner-up is **9.53 cm3/cm3**, both members now floor-graded. Screen-to-floor
scatter in the deciding band (screen 150-250, n=12) is **bias -0.26, sigma 1.33**, so the
margin is ~7 sigma. Every admissible structure not floor-graded screened below 151.

### The falsification test came back on the predicted side
`2022[U][srs]3[FSR]1`, at vf_ch4 0.451 -- above the measured optimum -- was predicted in
LOG-27, before the run, to gain nothing from methyl stripping and plausibly to lose:

| structure | vf_ch4 | vs optimum | pristine (floor) | stripped (floor) | change |
|---|---|---|---|---|---|
| `2023[Cu][ctn]3[FSR]1` | 0.299 | **below** | 177.72 | 187.65 | **+9.92** |
| `2022[U][srs]3[FSR]1`  | 0.451 | **above** | 150.82 | 140.62 | **-10.20** |

Nearly equal and opposite. "Stripping bulk always helps" is refuted; the interior-optimum
account survives a test built to break it. This is the difference between a lucky modification
and an understood one, and it is why the ceiling section of the report claims a mechanism
rather than an observation.

Final compute: **304.61 of 340 CPU-h (89.6%)**, 35.4 CPU-h unspent.

## LOG-2026-08-28-29 — CORRECTION: the claim IS sensitive to the G4 reachability threshold
The filed report (commit 7ef8d95, §4) stated that the claim's *identity* is insensitive to my
G4 threshold. **That was wrong and is corrected here.** It is insensitive to the angular leg
and to *tightening*, but not to relaxing the reachability distance.

Re-deriving admissibility across criteria, and asking what the best admissible screening value
becomes under each:

| G4 criterion | killed | best admissible | which structure |
|---|---|---|---|
| **adopted: θ≥60°, d≤4.2 Å** | 528 | **177.8** | `2023[Cu][ctn]3[FSR]1` |
| θ≥75°, d≤4.2 Å | 330 | 177.8 | `2023[Cu][ctn]3[FSR]1` |
| θ≥55°, d≤4.6 Å (stricter) | 539 | 177.8 | `2023[Cu][ctn]3[FSR]1` |
| **θ≥60°, d≤3.8 Å** | 372 | **195.7** | `2021[Al][nan]3[ASR]24` |
| θ≥90°, d≤4.2 Å | 114 | 207.7 | `2021[Cu][sql]2[FSR]6` |
| G4 disabled | 0 | 207.7 | `2021[Cu][sql]2[FSR]6` |

Relaxing the reachability cut from 4.2 to 3.8 Å readmits `2021[Al][nan]3[ASR]24`, whose
floor-grade value is **195.41** — which would beat both my parent (177.54) and my modified
finalist (187.75) and would become the answer. So the identity of the best material does turn
on this choice, and the report must say so.

**Is 4.2 Å the right cut? I checked the chemistry rather than defending the number.**

    2021[Al][nan]3[ASR]24 : Al environments are AlO6 (octahedral, CH4 cannot approach
                            closer than 5.0 A) and **AlO5 -- five-coordinate -- with a
                            methane centre reaching 4.0 A**.  UFF sigma_mix(Al,CH4) = 3.87 A.
    2023[Cu][nan]3[ASR]8  : Cu is CN=5, {Cu 1, O 4} -- a paddlewheel with the axial site
                            vacant; methane reaches 3.6 A against sigma_mix 3.42 A.

Al(III) in a MOF node is octahedral. A five-coordinate Al with an accessible vacancy is a
genuine open metal site, created by the ASR protocol removing the sixth (solvent) ligand — and
there is **no FSR counterpart of this structure in the database**, so it exists only in its
desolvated, uncapped form. A methane centre at 4.0 Å from that vacancy is at van der Waals
contact with a coordinatively unsaturated metal, which is exactly the situation G4 exists to
exclude and exactly where a dispersion-only force field has no standing.

So the 4.2 Å cut is chemically correct and the 3.8 Å variant is too permissive: it would admit
structures whose highest-uptake sites are open metal centres described by UFF dispersion alone.
The adopted answer stands. But the honest statement is *"the threshold is defensible on
chemistry and the answer would change if it were relaxed"*, not *"the answer is insensitive"*,
and the report is amended to say the former.

The finalist itself is unaffected under any setting: `2023[Cu][ctn]3[FSR]1` has n_exposed = 0
with `d_probe` unreachable at every distance tested — its Cu is tetrahedral CuS4, shielded by
its own linkers.
