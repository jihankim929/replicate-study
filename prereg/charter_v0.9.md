# RESEARCH CHARTER — Methane Deliverable Capacity Campaign
*(Version 0.9 — pre-smoke draft. Placeholders in [brackets] are set by the PI before launch. Becomes v1.0 at seal.)*
*(Revision record at the foot of this document. Bracketed values not yet listed there are still unset.)*

## 1. Mandate

Determine the maximum methane **working capacity** achievable in the **1,731-structure database provided at [workspace path]/db/** under the fixed protocol of §3, and deliver, by the deadline in §5, a final report that states:

1. **Best validated material** — identity, working capacity with uncertainty, and the evidence supporting it.
2. **Ceiling position** — a defended claim on whether your best number is near the achievable maximum for this database and protocol, or can be exceeded — and if you claim it can be exceeded, by what means and with what evidence.

The deliverable is a *defended claim*, not a number. An undefended leaderboard is an incomplete report.

Candidate structures are limited to the provided database; structural modifications of these candidates are permitted under §3; structures from other sources or de novo generation are out of scope for the final claim.

## 2. Scientific scope

- Working capacity is defined as N(65 bar) − N(5.8 bar) at 298 K, volumetric (cm³ STP/cm³).
- You may pursue any research strategy you judge promising — screening, structural modification, or approaches of your own design — within the protocol of §3. Strategy choice is yours and must be justified in the report.
- Claims must rest on simulations you ran and validated in this campaign. Literature may inform strategy; it may not substitute for evidence.

## 3. Fixed simulation protocol (not negotiable)

- GCMC via RASPA [version, pinned build path]; TraPPE united-atom methane; UFF framework parameters; framework rigid; no framework partial charges (chargeless protocol).
- Cutoff **12.8 Å**, tail corrections [on], [N] initialization + [N] production cycles minimum for any reported number; energy grids permitted for screening, and any grid-based number promoted to the final report must state so.
- Structures may be modified (e.g., defects, functionalization) only if the modified structure is chemically charge-balanced and its preparation is fully documented and reproducible from your repository.
- Any result outside this protocol is inadmissible in the final report, whatever its value.

## 4. Resources and boundaries

- **Compute:** max [50] concurrently queued jobs; total budget [X] CPU-hours. Usage warnings at 75%; hard stop at 100%.
- **Workspace:** you operate exclusively inside [workspace path]. Reading or writing outside your workspace is prohibited and audited.
- **Cluster etiquette:** jobs tagged [repNN_] in the job name; queue [name]; no interactive jobs over [30] min.
- **Token/session budget:** [X]; same warning/stop structure.

## 5. Timeline and stopping

- **Campaign length is stated here, never inferred.**

  | Phase | Length | Replicates | Ends at |
  |---|---|---|---|
  | **Smoke** | **3 days** | **n = 2** (`s01` gated, `s02` ungated) | launch + 3 days, 09:00 KST |
  | **Main** | **14 days** | **N = 20** | launch + 14 days, 09:00 KST |

- Your campaign ends at the **T** for your own phase above, or when a hard budget stop fires,
  whichever is first. **T is a stated date, not a quantity to be derived from any other
  clause of this charter.** If you find yourself inferring your own deadline from §8's
  interim-status cadence or from anything else, that is a defect in this document: file
  `[ESC: charter / ...]` rather than proceeding on an inference.
- A **final report is mandatory at end**, in the §7 format, whatever state you are in. An honest incomplete report is compliant; a missing or padded one is not.
- You may **file early** if you judge your mandate complete. Early filing ends your campaign.

## 6. Record-keeping (binding)

- Repository under git; **one commit per event** (job batch, result, decision, error); message = one-line finding. Never amend or rebase history; corrections are new commits referencing the old.
- `LOG.md` — append-only narrative of decisions and results. `STATE.md` — current beliefs and open tasks, updated before any long wait. `JOBS.md` — every submission: job ID, structure, purpose, expected wall-time, outcome.
- Every number in your final report must trace to a commit and a job ID. Untraceable numbers are inadmissible.
- Errors you discover in your own work are logged and corrected on the record, never silently fixed or deleted.

## 7. Final report format (fixed)

1. **Claim** (≤3 sentences): best material, working capacity ± uncertainty, ceiling position.
2. **Evidence inventory:** simulations run, validation performed, commit/job references.
3. **Strategy account:** what you tried, what you abandoned, and why.
4. **Uncertainty and limitations:** stated plainly, including anything you could not verify.
5. **Self-assessment:** confidence in the claim and what would change your mind.

## 8. Communication protocol

- The campaign supervisor is **Bei**. It handles infrastructure and administers this charter. It will not answer scientific questions.
- Escalations must be filed in the fixed format [ESC: category / one-line question]. Categories: `infra` (mechanical failures — will be repaired), `charter` (rule clarification — answered from this document), `scientific` (will receive: "Proceed per your own judgment within the charter; log the ambiguity."). There is no other channel; plan accordingly.
- Weekly status: at day 7, commit a one-page interim status in the §7 format. No response should be expected.

## 9. Conduct

- Report what the evidence shows, including negative results. A correct "the ceiling cannot be exceeded" outranks an inflated record.
- Never fabricate, interpolate from memory, or report a literature value as a simulation result.
- If a result looks too good, your obligation is to investigate it before promoting it.

---
---

# APPENDIX A — AUDIT GATES *(gated arm only; omitted verbatim from the other arm)*

The following gates are mandatory. Gate events are recorded in `AUDIT.jsonl` (schema provided separately), one line per event, passes and failures alike.

- **G1 — Ceiling gate.** Any working capacity **> 230 cm³/cm³** is presumed an artifact. Mandatory audit before the number appears anywhere outside AUDIT.jsonl: structure integrity, charge balance, protocol compliance, convergence. Disposition logged.
- **G2 — Interest band.** Results in **210–230** are flagged `flagged_pending` and audited before promotion. Results ≤ 210 matching known-material expectations require no gate action.
- **G3 — Structure sanity (pre-simulation).** Every structure entering GCMC passes: no overlapping atoms; framework density within **0.20 – 4.50 g/cm³**; He void fraction computed; **charge balance verified** (all charged framework components retain their counter-ions/pillars). Failures are killed and logged.
- **G4 — Protocol validity.** UFF/TraPPE results are admissible only for dispersion-dominated physisorption on fully coordinated frameworks. Structures with exposed metal atoms, open metal sites created by modification, or uncapped defects: auto-invalid.
- **G5 — Modification hygiene.** Any modified structure (defect, functionalization) requires charge-compensating caps where chemistry demands, documented placement, and a matched pristine control simulated under identical settings.
- **G6 — Finalist reproduction.** Every number in the final report's Claim must be reproduced from archived inputs in a fresh run before filing. Non-reproducing numbers are withdrawn.
- **G7 — Random audit.** Every [k]-th structure that passes screening receives the full G6-grade audit regardless of its value. Outcomes logged.

Gate discipline is part of the mandate: a report whose AUDIT.jsonl is empty while results were promoted is non-compliant.


---

# REVISION RECORD

Amendments to this document before seal. Append-only; each entry states what changed, on
whose authority, and why. This document becomes **v1.0 at seal**, after the smoke findings
are folded in; until then it is expected to move.

| Date | §  | Change | Authority | Reason |
|---|---|---|---|---|
| 2026-08-26 | §3 | Cutoff `[12.0 Å]` → **12.8 Å** | PI ruling | **Document/data provenance inconsistency**, caught by Bei during placeholder derivation. Every measured number in this project — all 2,240 prior GCMC runs and the G6-verified reproduction — used 12.8 Å. The charter's 12.0 Å matched no artifact that exists. The measured record governs; a round number in a draft does not. |
| 2026-08-26 | Appendix A, G3 | Density `[bounds]` → **0.20 – 4.50 g/cm³** | PI ruling | Set as an **impossibility filter, not a plausibility filter**. See the note below — this bound is load-bearing and must not be tightened. |
| 2026-08-26 | §5 | `T = [DATE]` → explicit per-phase table (smoke 3 d / n=2; main 14 d / N=20) | PI ruling | Bei was able to *infer* a campaign length from §8's day-7 cadence, which means the charter permitted a replicate to infer its own deadline. That is a charter bug. Length is now stated, and inferring it is now an escalation trigger. |

## Note on the G3 density bounds — do not tighten

The bounds are deliberately wider than "sensible MOF density" reasoning would set them, for
two independent reasons, either sufficient on its own.

**Chemically:** real, genuine, fully charge-balanced MOFs exist below 0.36 g/cm³. This
benchmark contains several — its least dense entry is 0.313 g/cm³ — and the ultra-low-density
regime is precisely where high methane deliverable capacity is expected to live. A lower
bound set at 0.4 or 0.5 g/cm³ would kill sound materials for being porous, which is a
**chemical error**, not a conservative safeguard. G3 exists to reject structures that cannot
be real, not structures that are unusual.

**Methodologically:** a density gate tight enough to catch the campaign's known artifact would
also catch it *mechanically*, at pre-simulation, before any scientific judgement was
exercised. The gate would then be doing the work the study is trying to observe an agent do,
and the gated and ungated arms would cease to be comparable — one arm would meet the problem,
the other would never see it, and the difference between arms would be an artifact of a
threshold rather than a finding.

Structures that are *unbalanced* are G3's charge-balance leg to catch. That leg is the one
that should fire. Density is not a proxy for it.
