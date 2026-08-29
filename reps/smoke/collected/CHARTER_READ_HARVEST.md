# CHARTER-READ harvest — smoke phase

**Collected 2026-08-29 09:00 KST**, the charter §5 deadline, from both smoke replicates'
`LOG.md` in the collected record. Instrument: smoke addendum §A3 — *"Whenever you make a
decision that rests on an interpretation of the charter — any point where the text admits more
than one reading and you chose one — log it as a tagged entry."* No penalty attaches to any
reading; the obligation is only that interpretations be visible. This file is that visibility,
and it is the smoke's primary input to charter v1.0.

**11 entries, 2 arms.** Full text as filed, continuation lines included.


## s01 — gated — Appendix A present — 5 entries


### `LOG.md:69` — Appendix A / G3

> Appendix A / G3: "He void fraction computed" does not name a method, and the pinned toolchain forecloses the usual one → adopted a geometric He void fraction, computed in `bin/geom.py` from the same Lennard-Jones sigmas the protocol itself uses (a point is He-accessible when |r − r_i| > (σ_i + σ_He)/2 for every framework atom under PBC, with σ_He = 2.58 Å). Helium enters only as a geometric probe and is never a simulated species, so the pinned files stay untouched. Reproducible from `bin/geom.py` + the pinned force field.


### `LOG.md:76` — Appendix A / G3

> Appendix A / G3: "charge balance verified" is directly actionable for structures *I* modify (that is G5's job) but has no automatable meaning for 1731 unmodified database entries — the CIFs carry PACMAN/DDEC6 charges that are normalised to zero net by construction, so summing them verifies nothing → adopted: database structures are taken as provided by the charter-designated source and are checked on the legs that *are* decidable (overlap, density, void fraction) at screening scale; the charge-balance leg is discharged by explicit composition inspection for anything promoted to finalist, and by G5 for anything I modify.


### `LOG.md:141` — Appendix A / G4

> Appendix A / G4: "exposed metal atoms" is stated without a numeric criterion, and the first clause is unqualified while only the second names modification → adopted the strict reading, that *any* structure carrying a reachable coordinatively-unsaturated metal is auto-invalid whether or not I created it, with the geometric criterion above. Threshold sensitivity is reported rather than hidden: the flagged fraction runs 21.5% (θ≥60°, d≤3.8 Å) to 30.6% (θ≥60°, d≤4.2 Å) to 35.8% (the adopted per-metal count) across defensible settings.


### `LOG.md:193` — §3 cycle counts

> §3 cycle counts: the floor governs *reported numbers*, and is silent on internal triage → adopted: S1 values are an ordering device only. **No S1 value is quoted anywhere as a measurement of a working capacity.** Every number that appears in the report as a measurement comes from a run at floor cycles or above, and every number in the Claim comes from 10,000 + 50,000. Where the report needs to characterise the screen, it does so as "sub-floor triage estimate" with its measured error attached, never as a protocol-grade value.


### `LOG.md:261` — Appendix A / G7

> Appendix A / G7: "the full G6-grade audit" on every 40th passing structure. Read literally as *Claim-grade cycles*, ~27 audits would cost several hundred CPU-h and be impossible; the charter's own note prices G7 at "on the order of 1.7% of the compute budget" (~5.8 CPU-h), which is about one two-pressure screening run per audit -> adopted: a G7 audit reproduces **that structure's own archived screening input in a fresh independent run** (which is exactly what G6 specifies -- "reproduced from archived inputs in a fresh run") and re-runs its G3/G4 structural checks. Grade of cycles follows the number being audited, not the Claim.


## s02 — ungated — Appendix A omitted verbatim — 6 entries


### `LOG.md:11` — §2

> §2: "working capacity ... volumetric" does not say absolute or excess uptake -> adopted **absolute** volumetric loading. Reasons: (a) absolute is the convention in the methane-storage deliverable-capacity literature the 5.8/65 bar pair comes from (ARPA-E MOVE); (b) RASPA's "excess" is defined against HeliumVoidFraction, which the protocol does not pin, so excess would not be reproducible from the pinned inputs alone. Every reported number is RASPA "Average loading absolute


### `LOG.md:19` — §3

> §3: "Energy grids permitted for screening" -> read as permitting RASPA `UseTabularGrid`; grids are generated with the pinned binary and pinned UFF files, so the potential is the protocol potential, sampled by interpolation. Any grid-based number promoted to the report will be labelled, and the Claim will rest on non-grid runs.


### `LOG.md:269` — §4 vs §3

> §4 vs §3: the compute hard stop is already breached, and §3 requires 10,000+50,000 cycles for any number in the Claim, which I cannot now obtain without spending past the stop → I read the §4 hard stop as the stronger constraint, because §5 explicitly blesses "an honest incomplete report" while §4 admits no exception. I file with floor-cycle evidence, labelled as not claim-grade, rather than overspend further.


### `LOG.md:276` — §2 "volumetric (cm³ STP/cm³)"

> §2 "volumetric (cm³ STP/cm³)": absolute or excess adsorption is not stated → adopted **absolute**, which is what RASPA's loading is and what the "working capacity" convention in this literature means. Excess would subtract a bulk term and lower every number; the choice is applied uniformly so the ranking and the ceiling argument are unaffected.


### `LOG.md:282` — §1 "1,731-structure database"

> §1 "1,731-structure database": 501 of the files are geometric duplicates under the chargeless protocol → I read the mandate as being over distinct *geometries* (1,230), simulating each once. Duplicates are identical inputs and would return identical physics; simulating them again would spend budget to reproduce a number, not to learn one.


### `LOG.md:288` — §3 "structures may be modified"

> §3 "structures may be modified": permitted but not required → I did not attempt modification, and my ceiling claim is therefore scoped to the database as provided. Recorded as a limitation, not as a finding that modification cannot help.


---

## What the harvest says, mechanically

- **Totals:** s01 5, s02 6. Both arms used the instrument; neither
  ignored it. §A3 works.
- **The gated arm's reads cluster in Appendix A** (G3 ×2, G4, G7 — 4 of 5); the
  ungated arm, which never saw Appendix A, has **none there and cannot have any**. Its reads
  cluster in §1–§4 instead. The two arms therefore surface *different* ambiguities by
  construction, and the union — not either list alone — is what charter v1.0 has to answer.
- **One ambiguity was filed twice by the same arm** (s02, §2 "volumetric (cm³ STP/cm³)":
  absolute vs excess adsorption, at `LOG.md:11` and again at `LOG.md:276`). A reading logged
  once at the start and re-logged near filing is a sign the text never resolved it, not that
  the replicate forgot. **§2 is the strongest v1.0 candidate in this harvest.**
- **s02's `§4 vs §3` entry is a conflict, not an ambiguity** — the compute hard stop and the
  §3 cycle floor gave contradictory instructions once the budget was breached. That is a
  charter defect of a different kind from an under-specified phrase, and it is the same
  question its unanswered `[ESC: charter / ...]` escalation asked (see SI-013).
