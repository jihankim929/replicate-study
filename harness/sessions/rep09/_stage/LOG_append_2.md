
## 2026-08-29 (launch +1.5h) — the screening proxy failed its own validation; screening moves to real GCMC

- DONE Cost probe. 42 structures drawn 4-per-duodecile of volume/atom, GCMC at
  65 bar with 200 initialization + 1000 production cycles, one core each:
  mean 123 s, median 73 s, max 553 s (`tables/timing_probe.csv`). Because the
  sample is uniform over quantiles it is unbiased for the database, so an
  exhaustive 65-bar screen at these cycle counts costs ≈ 430 CPU-h, 27% of
  budget. The charter's 1.83 CPU-h/structure is the floor protocol at two
  pressures; it does not forbid an exhaustive screen at screening cycles.
- DONE Parser cross-validation. For all 42 probe structures the framework
  density I compute from the parsed CIF matches RASPA's `Framework Density`
  to four figures (ratio 0.0010 exactly, g/cm³ vs kg/m³). The CIF reader,
  the cell-volume calculation and the unit-cell replication are therefore
  reading the same structures RASPA is.
- DONE, THEN ABANDONED Geometric screening descriptor (`bin/geom.py`):
  clearance field c(r) = min_i(|r−r_i| − σ_i/2) on a 0.3 Å grid, accessible
  fractions for six probe radii, σ from the pinned UFF mixing rules. It runs
  in 0.05–1.4 s per structure, i.e. the whole database for ~1 CPU-h, and an
  independent brute-force calculation over an explicit 5×5×5 supercell
  reproduces it (structure 2778: 0.00045 brute vs 0.00031 gridded;
  structure 9407: 0.0765 vs 0.0765).
- **Negative result that changed the strategy.** The descriptor is correct and
  useless. Structure 2778 (`2011[Co][nan]3[FSR]9`, ρ = 2.20 g/cm³, cell
  327.8 Å³) has methane-accessible fraction 0.0003 by the σ-contact criterion
  — 0.1 Å³ per unit cell — and RASPA nonetheless equilibrates it to
  1.157 molecules/unit cell, 131.3 cm³ STP/cm³ at 65 bar, with a host–adsorbate
  energy of −2585 K per molecule (−21.5 kJ/mol). The hard-sphere criterion
  places the boundary at the pair separation where U = 0; in an ultramicropore
  a methane centre sitting slightly inside σ of several atoms at once still has
  a deeply negative *total* energy. A σ-contact screen would therefore have
  discarded the tight-pore materials preferentially — the opposite of a
  conservative filter.
- DECISION No proxy screen. The database is screened with the pinned RASPA
  protocol itself at reduced cycle counts. This costs ~27% of compute and buys
  something no descriptor can: because N(5.8 bar) ≥ 0, N(65 bar) is a rigorous
  upper bound on working capacity, so a 65-bar screen *excludes* candidates
  rather than merely deprioritising them.
- RUNNING Tier 1: all 12,499 structures at 65 bar, 200+1000 cycles, seed 1.
  12 jobs `rep09_s1_00..11`, ppn=8, 8 on `ac` and 4 on `amd`, mjs ids 3046+.
  Chunks are interleaved so every chunk carries the same cost distribution,
  and `mkjobs.py` skips points already recorded `ok`, so a dead job can be
  resubmitted without repeating work.

[CHARTER-READ] §4: "the compute budget is deliberately set below the cost of
screening the whole database", quoted against 1.83 CPU-h per structure at two
pressures → I read this as a statement of measured cost under the floor
protocol, not as a prohibition on exhaustive screening. At 200+1000 cycles and
one pressure the whole database costs ~430 CPU-h, which the budget covers, so
I screen it whole. The clause's operative content — that I cannot afford to
run the *reportable* protocol on everything — still holds and still governs
tiers 3 and 4.
