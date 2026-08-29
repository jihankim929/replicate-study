# LOG — append-only narrative

## 2026-08-29 19:41 KST — launch
Read CHARTER.md, CHARTER_ADDENDUM.md, WORKSPACE.json. Deadline taken from
`deadline_kst` = 2026-09-05T19:41:33+09:00, per §5 and A1 ("work from that timestamp,
never from the day count").

## 2026-08-29 ~19:45 — environment verification
- `sha256sum` of the three UFF files matches the charter §3 table exactly. Verification
  is not required by §3 but it is cheap and it is the one thing that silently changes
  every number, so it was done once and recorded here.
- `libraspa2.so.0.0.0` reports `RASPA 2.0.37`.
- db: 12,499 CIFs + MANIFEST.sha256. `bin/scan_db.py` parsed all 12,499 with zero
  failures in 6.5 s, producing `manifest/structures.csv` (cell, volume, composition,
  mass, density, perpendicular widths) and `manifest/elements.txt`.
- All 73 elements present in the db have a pseudo-atom in the pinned UFF set. Nothing
  in the database is out of reach of the protocol for lack of parameters.

## 2026-08-29 ~19:50 — CIF preparation
The db CIFs carry PACMAN DDEC6 charges and atom labels of the form `Ag1`, `C7`; the
pinned UFF set names its pseudo-atoms `Ag_`, `C_`. `bin/prep_cif.py` writes a P1 CIF
with the label set to the pseudo-atom name and the charge column dropped. Coordinates,
cell and composition pass through unchanged — this is a relabelling for the reader, not
a structural modification under §3.

[CHARTER-READ] §3: the protocol is "no framework partial charges" but every db CIF
carries a `_atom_site_charge` column → I drop the column in the prepared CIF *and* set
`ChargeMethod None` / `UseChargesFromCIFFile no` in `simulation.input`. Belt and braces:
either alone would suffice, and the redundancy means a future reader cannot be in doubt
about which one was operative.

Smoke test on S00000 (`0000[Ag][nan]3[ASR]1`) at 65 bar: RASPA ran to completion and
printed a framework density of 2228.36 kg/m³ against 2229 kg/m³ from my independent
parser — the CIF is being read as intended. Loading is ~0, as expected for a 2.23 g/cm³
framework.

## 2026-08-29 ~20:00 — operational constraint discovered
`quse` shows all sixteen sibling replicates sharing the single `Bei` account and its
per-partition core caps; at launch only ~16 amd cores were free of an 80-core cap. An
initial ppn=21 submission sat in the mjs pending list and was withdrawn (`qrm 3015`) and
resubmitted at ppn=16, which started immediately (PBS 3473372).

This is not only a contention problem, it is the right size anyway: 1610 CPU-h spread
over a 168 h campaign is **≈10 cores sustained**. Large allocations would exhaust the
compute budget in a day. The campaign is therefore planned around a steady ~16-core
task farm rather than wide bursts.

[CHARTER-READ] §4: "compute" is stated in CPU-hours but not defined as allocated-core-
hours vs. busy-core-hours → I meter it as **allocated cores × job wall-time**, the
larger and more conservative reading, and I keep jobs saturated (more tasks than cores)
so the two figures nearly coincide. Per-case busy time is logged separately in the
results CSVs.

## 2026-08-29 ~20:05 — first two jobs submitted
- `rep04_bench`: 7 structures spanning the density range (0.29 → 2.03 g/cm³) × 2
  pressures at the §3 floor (2,000 + 10,000), plus the same 7 at 65 bar with a
  tabulated energy grid. Purpose is a cost model, not science: CPU-h per case, and
  whether grids are worth their generation cost and what bias they carry.
- `rep04_desc`: a Widom descriptor sweep over all 12,499 structures.

  The sweep draws 20,000 uniform points per unit cell and evaluates the TraPPE-UA
  methane / UFF Lennard-Jones energy under the protocol's own real-space treatment
  (12.8 Å, truncated, unshifted, no tail, no charges). It records a 92-bin histogram of
  U, the Henry-limit Boltzmann factor, hard-sphere accessible fractions at three probe
  radii, and a local-density-approximation loading estimate at both protocol pressures.

  Storing the *histogram* rather than only the derived estimate is deliberate: any
  screening model of the form n = ⟨g(U)⟩ can be refitted later from the stored
  histograms without re-touching 12,499 structures. Measured cost ≈3 s/structure,
  ≈10 CPU-h for the whole database — 0.6% of budget to see all of it.

[CHARTER-READ] §2/§3: the descriptor sweep uses my own LJ evaluation rather than RASPA
→ admissible as *screening*. §3 (Rev 22) permits replicate-created auxiliary parameter
files for descriptor and screening calculations provided claim-grade simulations use
only the pinned set; no descriptor number will appear as a reported capacity, and every
number in the report will come from RASPA under the pinned protocol.

[CHARTER-READ] §2: the definition of working capacity is fixed but the *void fraction*
is not pinned, and §2 says so explicitly. I therefore avoid a helium void fraction
anywhere in the pipeline, including in descriptors, and use hard-sphere probe-accessible
fractions instead. This keeps every quantity I compute reproducible from the pinned
inputs alone.
