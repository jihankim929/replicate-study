
## 2026-08-29 23:00 (launch +3.3h) — modification machinery built and tested

- DONE `bin/modify.py`: charge-balanced defunctionalisation. Bonds are
  perceived geometrically over periodic images (d < r_cov,i + r_cov,j + 0.40 Å,
  metals given a 1.45 Å covalent radius so coordination spheres are never cut),
  terminal monovalent substituents are identified, deleted, and replaced by a
  hydrogen on the same bond vector at the standard bond length for the anchor
  element. Recognised groups: -F, -Cl, -Br, -I, -CH3, -NH2, -OH, -NO2. Every
  substitution is monovalent-for-monovalent, so the framework stays neutral by
  construction, which is what §3 requires of a modified candidate.
- Verified on four structures: `2013[SiCu][pcu]3[ASR]1` yields 4 fluorine
  replacements at constant atom count; `2023[ZnTi][nan]3[ION]4` yields 12
  methyl replacements, 812 atoms to 776; two structures correctly yield no
  groups. Runtime 0.0–0.8 s per structure.
- Rationale for this family and no other. Working capacity is hurt from two
  directions at once by pendant groups: they occupy pore volume, and they
  raise the binding energy, which fills the material at 5.8 bar where uptake
  is subtracted rather than added. Defunctionalisation relieves both. The
  screen already shows N(65 bar) peaking at an interior density optimum near
  ρ = 0.5–0.6, so the intended targets are high-N65 structures that sit
  *denser* than that optimum, where removing substituents moves them toward it
  rather than past it.
- NOT YET RUN. Candidates come from Tier 2; no modified structure has been
  simulated yet.
