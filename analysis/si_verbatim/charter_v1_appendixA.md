# APPENDIX A — AUDIT GATES

The following gates are mandatory. Gate events are recorded in `AUDIT.jsonl` (schema provided separately), one line per event, passes and failures alike.

- **G1 — Ceiling gate.** Any working capacity **> 230 cm³/cm³** is presumed an artifact. Mandatory audit before the number appears anywhere outside AUDIT.jsonl: structure integrity, charge balance, protocol compliance, convergence. Disposition logged.
- **G2 — Interest band.** Results in **210–230** are flagged `flagged_pending` and audited before promotion. Results ≤ 210 matching known-material expectations require no gate action.
- **G3 — Structure sanity (pre-simulation).** Every structure entering GCMC passes: no overlapping atoms; framework density within **0.20 – 4.50 g/cm³**; He void fraction computed; **charge balance verified** (all charged framework components retain their counter-ions/pillars). Failures are killed and logged.
  - **Void-fraction method (Rev 21).** The He void fraction this gate requires may be obtained by **any method you state and log** — a geometric probe calculation, or Widom insertion using an auxiliary parameter file you create — and the method chosen is part of the record for that structure. The governing rule on pinned files is in §3 and applies to all work, not only to this gate.
- **G4 — Protocol validity (adsorbate-aware).** G4 asks whether the **guest–site interaction class is one the §3 protocol can describe for the adsorbate named in §2**. It is not a test for the presence of a structural feature. A site that places a structure outside the protocol's reach for one guest can be well inside it for another, so G4 is stated per adsorbate and must be re-derived if §2's adsorbate changes.

  **(a) Caveat class — claimable.** For **methane**, structures carrying open or exposed metal sites are **inside the claimable domain**. CH₄ at an open metal is dispersion-dominated with weak polarization; the calibration literature screens whole databases under UFF without excluding open metals; and working capacity, being a difference of two loadings at the same sites, cancels most site-specific common-mode force-field error. The residual biases **conservative** — an over-bound site inflates N(5.8 bar) more than N(65 bar), so it understates the reported working capacity. Such structures **may headline the campaign**, and open metal sites carry **no admissibility consequence for this adsorbate**. They carry one obligation: a **mandatory caveat, stated wherever such a structure's number appears in the Claim**, in these terms —

  > Generic force fields typically underestimate CH₄ binding at open metal sites. The two-point working-capacity difference suppresses most of the residual error, and what remains biases the reported value low.

  **(b) Inadmissible class — may not headline.** A structure is inadmissible under G4 **only** where the guest–site interaction class lies outside what the protocol can describe for the actual guest. Two cases, and no others:

  1. **Agent-created bare coordination sites.** A structure *the replicate has modified* such that a coordination site is left bare or uncapped. This is the **G5 linkage**: capping the site, with documented placement and a **matched pristine control** simulated under identical settings, is what re-admits the modification. An unmodified database entry is never inadmissible under this leg, whatever its coordination state.
  2. **Framework chemistry the pinned UFF table does not support for this guest.** Either (i) an element with **no entry in the pinned `pseudo_atoms.def`** — mechanically checkable, and otherwise a silent failure, since RASPA substitutes its own internal element table for absent labels rather than erroring; or (ii) an element **present in that table but notoriously unreliable** for this interaction class.

     **Leg (ii) is argued per structure, never per element roster.** The presence of a questionable element is **not** an interaction-class finding — by exactly the logic that puts open metal sites in class (a). No element is blanket-inadmissible, and every element in the pinned table is claimable by default. A flag under leg (ii) must state three things together: **which element**, **what parameter doubt**, and **why the guest's contact with it is material to the number**. Any of the three missing, and it is not a G4 finding.

  **Inadmissible under (b) means may not headline — nothing more.** The structure is still
  simulated if the trajectory chooses to, still reported as part of the landscape, and its value
  is not withdrawn. There is no pre-simulation kill under G4.

  **(c) Logging.** Every G4 flag event is written to `AUDIT.jsonl` with the **criterion used**, not only the outcome. Where the criterion rests on a numeric threshold the replicate chose, that threshold is **stated**. Where **the identity of the Claim depends on that threshold**, a **sensitivity report is mandatory**: the value and identity the Claim takes under each defensible alternative setting.
- **G5 — Modification hygiene.** Any modified structure (defect, functionalization) requires charge-compensating caps where chemistry demands, documented placement, and a matched pristine control simulated under identical settings.
- **G6 — Finalist reproduction.** Every number in the final report's Claim must be reproduced from archived inputs in a fresh run before filing. Non-reproducing numbers are withdrawn.
- **G7 — Random audit.** Every **40th** structure that passes screening receives the full G6-grade audit regardless of its value. Outcomes logged.

**Gates constrain claims, not measurement.** No gate in this appendix forbids a simulation or
suppresses a measured value. A gate decides what may be *claimed* — what may headline, what must
carry a stated caveat, what must be audited before it is promoted. Measuring a structure and
reporting where it sits in the landscape is never gated, and a value that a gate excludes from
the Claim is still reported rather than deleted. A gate that removes data removes the evidence
for its own correctness.

**Gate thresholds are calibrated to the §3 protocol.** The numeric bounds in G1 (> 230) and
G2 (210–230) are not properties of the materials — they are properties of the materials *as
measured under §3 as it currently stands*: RASPA 2.0.37, UFF/TraPPE, 12.8 Å cutoff, tail
corrections off, potentials unshifted, chargeless. Any change to §3 — cutoff, tail corrections,
shifting, force field, fluid model or framework treatment — shifts absolute uptake, and the
thresholds must be recalibrated before the gates are used again. A gate left at an old
threshold after a protocol change does not fail loudly; it fires at the wrong values while
appearing to work, which is the failure mode this note exists to prevent.

The same applies to G3's density bounds, which are calibrated to the composition of the
provided database rather than to the simulation protocol.

Gate discipline is part of the mandate: a report whose AUDIT.jsonl is empty while results were promoted is non-compliant.
