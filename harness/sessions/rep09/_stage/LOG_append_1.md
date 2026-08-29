
## 2026-08-29 (launch +0h) — setup and toolchain verification

- Read CHARTER.md, CHARTER_ADDENDUM.md, WORKSPACE.json. Deadline
  T = 2026-09-05T19:41:39+09:00 (launch + 168 h), taken from `deadline_kst`.
- Budgets: 1610 CPU-h, US$280 spend, 32M tokens, 12 concurrently queued jobs,
  queue `long`, job prefix `rep09_`.
- DONE Toolchain verified although §3 does not require it: the three UFF files
  under `toolchain/raspa/share/raspa/forcefield/UFF/` reproduce all three
  charter SHA-256 values exactly, and `libraspa2.so` carries the string
  "RASPA 2.0.37". `force_field_mixing_rules.def` header declares `truncated`
  and `tailcorrections no`, i.e. the §3 truncation/tail settings are properties
  of the pinned file as the charter states, not of `simulation.input`.
- DONE Manifest built for all 12,499 CIFs (`manifests/structures.csv`): cell
  parameters, cell volume, atom count, and the unit-cell replication required
  for a 12.8 Å cutoff (each perpendicular cell width >= 2 x 12.8 A). 0 parse
  failures. 73 distinct elements appear; all 73 have UFF Lennard-Jones
  parameters in the pinned mixing-rules file, so no structure is excluded for
  want of parameters.
- Database shape: cell volume median 2801 A^3 (p5 873, p95 13228); atoms per
  cell median 174; volume/atom median 15.6 A^3 (p95 29.7, max 103). The bulk
  of the database is dense; porosity lives in the upper tail.
- DECISION Simulation cells are addressed by an integer id `m%05d` mapped in
  the manifest, not by the bracketed CIF filenames, which are hostile to
  shells and to RASPA's parser.

### Charter interpretations logged at setup

[CHARTER-READ] §3: the db CIFs label atoms `Ag1`, `C3`, ... and carry a DDEC6
`_atom_site_charge` column, but the pinned UFF pseudo-atom names are `Ag_`,
`C_`, ... -> I rewrite each CIF into a RASPA-ready copy (`bin/prep_cif.py`)
in which only the data name and `_atom_site_label` change (label := element
symbol + "_") and the charge column is dropped. Cell parameters, fractional
coordinates and atom count are copied through unchanged. Reading: this is a
format adaptation required to run the pinned force field at all, not a
"structural modification" under §3, since no atom, position or cell parameter
is altered; dropping charges is required by the chargeless protocol of §3.

[CHARTER-READ] §3: the cycle floor "2,000 initialization + 10,000 production"
is stated as the floor "for any reported number" -> I read "reported" as
"entering the final report", so internal screening runs used only to rank
candidates may use fewer cycles. Every number that appears in REPORT.md will
meet the floor, and every number in the report's Claim will meet
10,000 + 50,000. Screening cycle counts are recorded in the results tables so
the distinction is auditable.

[CHARTER-READ] §2/§3: working capacity is N(65 bar) - N(5.8 bar) at 298 K in
cm^3 STP/cm^3, absolute loading -> I take RASPA's
"Average loading absolute [cm^3 (STP)/cm^3 framework]" verbatim from each of
two independent GCMC runs (one per pressure) and subtract. No helium void
fraction is computed or used anywhere, consistent with §2's reason for
requiring absolute rather than excess loading.
