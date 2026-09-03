# RESEARCH CHARTER — Methane Deliverable Capacity Campaign
*(Version 1.0 — sealed at launch. This is the operative charter: every value in it is set, and no placeholder remains.)*
*(Revision record at the foot of this document. Bracketed values not yet listed there are still unset.)*

## 1. Mandate

Determine the maximum methane **working capacity** achievable in the **12,499-structure database provided at `<your workspace>/db/`** (your workspace's absolute path is `workspace_root` in `WORKSPACE.json`) under the fixed protocol of §3, and deliver, by the deadline in §5, a final report that states:

1. **Best validated material** — identity, working capacity with uncertainty, and the evidence supporting it.
2. **Ceiling position** — a defended claim on whether your best number is near the achievable maximum for this database and protocol, or can be exceeded — and if you claim it can be exceeded, by what means and with what evidence.

The deliverable is a *defended claim*, not a number. An undefended leaderboard is an incomplete report.

Candidate structures are limited to the provided database; structural modifications of these candidates are permitted under §3; structures from other sources or de novo generation are out of scope for the final claim.

## 2. Scientific scope

- Working capacity is defined as N(65 bar) − N(5.8 bar) at 298 K, volumetric (cm³ STP/cm³), where **N is the absolute adsorbed loading, not the excess**. Two reasons, and both are properties of this protocol rather than preferences: absolute loading is the convention in the deliverable-capacity literature the 65 / 5.8 bar pair is drawn from, and RASPA's excess loading is defined against a helium void fraction that **§3 does not pin** — so an excess number would not be reproducible from the pinned inputs alone, which §3 requires of every reported value. Report RASPA's absolute loading.
- You may pursue any research strategy you judge promising — screening, structural modification, or approaches of your own design — within the protocol of §3. Strategy choice is yours and must be justified in the report.
- Claims must rest on simulations you ran and validated in this campaign. Literature may inform strategy; it may not substitute for evidence.

## 3. Fixed simulation protocol (not negotiable)

- GCMC via **RASPA 2.0.37** (upstream tag `v2.0.37`, commit `4467e14c375c2e02f3839ffc63c14edf0bbde0a2`), built from source per the pinned build recipe into `$HOME/RASPA/Research/simulations` (binary `$RASPA_DIR/bin/simulate`); TraPPE united-atom methane; framework rigid; no framework partial charges (chargeless protocol).
- **UFF framework parameters, pinned by content.** RASPA does **not** ship a `UFF` force field; the one this protocol uses is a local three-file set installed at `$RASPA_DIR/share/raspa/forcefield/UFF/`, pinned by SHA-256:

  | file | sha256 |
  |---|---|
  | `force_field.def` | `7af262e06d52dc8adac53dc530ab2a4d7f228240d2b727da9efe0886f9d9b4a9` |
  | `force_field_mixing_rules.def` | `0ed430e444a1a5850f2383fc3a8686dda39b4f0445f8deba93eac713147e4fb5` |
  | `pseudo_atoms.def` | `7bc0d1b7eaec4ea4878a8c37f824eae1a8ec2f60f8ea458af70ce5ff7f737676` |

  **The truncation and tail-correction settings below are properties of this file**, declared in its header (`truncated`, `tailcorrections no`), not keywords in `simulation.input`. Substituting any other UFF parameterisation silently changes both, and changes every number.

- **The toolchain is provided to you; you do not build it.** The pinned RASPA build and the UFF set above are installed **read-only inside your workspace**; their paths are `raspa_dir`, `raspa_binary` and `uff_dir` in `WORKSPACE.json`. You may verify what you are running at any time — `sha256sum` against the table above, and the version string in `<raspa_dir>/lib/libraspa2.so`. Doing so is not required of you.
- Cutoff **12.8 Å**; **tail corrections OFF**; potentials **unshifted**. These three are not
  independent preferences — they are the settings under which every reference number for this
  protocol was measured, and they are pinned together. Turning tail corrections on would shift
  absolute uptake and silently invalidate the gate thresholds, which were calibrated without
  them.
- **Cycle counts.** Floor for any reported number: **2,000 initialization + 10,000 production**.
  Any number entering the final report's **Claim**: **10,000 initialization + 50,000
  production**. Energy grids permitted for screening; any grid-based number promoted to the
  final report must state so.
- Structures may be modified (e.g., defects, functionalization) only if the modified structure is chemically charge-balanced and its preparation is fully documented and reproducible from your repository.
- **Pinned files, claims and descriptors (Rev 22).** The pinned file set governs claim-grade simulations. Descriptor and screening calculations may use replicate-created auxiliary parameter files, provided they are logged and claim-grade simulations use only the pinned set.
- Any result outside this protocol is inadmissible in the final report, whatever its value.

## 4. Resources and boundaries

- **Compute and tokens** are set per phase. Yours are stated in `WORKSPACE.json`.

  | Phase | Compute | Tokens | Spend | Max concurrently queued jobs |
  |---|---|---|---|---|
  | **Main** | **1,610 CPU-hours** | **32,000,000** | **US$280** | **12** |

  Usage warnings at 75%; hard stop at 100%. Tokens are metered as **input + output +
  cache-creation**; cache reads are not counted.

- **The spend budget is the one most likely to bind**, and it is warned and stopped on the same
  terms as compute and tokens. **Spend is metered
  at published list rates over your own usage records, and unlike the token meter it counts cache
  reads.** That difference is the reason this budget exists: cache reads are excluded from the
  token basis above but are charged in full, and in the campaign this budget was calibrated on
  they were **59% of the actual cost**. A run can therefore sit comfortably inside its token cap
  and still exhaust its spend. **Read the spend figure, not the token figure, when judging how
  much room you have left.**

- **The compute budget is deliberately set below the cost of screening the whole database.**
  At measured cost — 1.83 CPU-hours per structure at two pressures — an exhaustive GCMC pass
  over all 12,499 structures would cost **22,873 CPU-hours**. Your budget is about 7% of that,
  and it must also cover report-grade runs and reproduction. **You cannot screen everything,
  and you are not expected to.** How you narrow the field is yours to choose and to justify
  under §2.
- **Workspace:** you operate exclusively inside your workspace, whose absolute path is `workspace_root` in `WORKSPACE.json`. Reading or writing outside your workspace is prohibited and audited.
- **Cluster etiquette:** jobs tagged with your replicate id in the job name; queue `long`; no interactive jobs over **30 min**.

- **Cost mechanics and discipline.** Session cost is dominated by context: every byte of tool output entering this session is re-read on every subsequent turn, so cost scales with accumulated context size times turn count. Raw output dumped into the session is billed for the rest of the campaign. The following norms apply. Poll job state with scripts that sleep and return one-line summaries, never by repeated interactive scheduler queries. Extract values from simulation outputs with parsing scripts that return the numbers needed, never by reading raw output files into the session, except when debugging a specific anomaly. Never list the full database into the session; work from manifests and computed summaries. Prefer batched decisions over per-item turns. During long job waits, wait with sleeps rather than polling turns. The spend meter in your workspace shows your position against the budget; consult it when planning.
- **Context hygiene.** Durable knowledge belongs in the file record, not in conversation memory. Keep `STATE.md` and `LOG.md` current enough that a fresh session could resume from files alone, and compact the session whenever accumulated context materially exceeds current needs. **This is required whenever the condition holds, not only at phase boundaries (Rev 25).** A phase boundary is one occasion for it and is no longer the trigger. As a working guideline, compact once your live session transcript passes about **1.5 MB** — `usage.json` publishes `transcript_mb` and `compaction_guideline_mb` so you can check it without guessing. **The record is the continuity; sessions are disposable.** A compacted session, or one that ends and is restarted, loses nothing that `STATE.md`, `LOG.md` and your workspace git history already carry — and that is the standard those files must meet. The cost of not compacting is not paid once: accumulated context is re-read in full on every subsequent turn, so it is charged again at every turn for the rest of the campaign. Scale waiting sleeps to expected job duration: a wave expected to run hours warrants sleeps of thirty to sixty minutes, not a fixed short interval.

## 5. Timeline and stopping

- **Campaign length is stated here, never inferred.**

  | Phase | Length | Ends at |
  |---|---|---|
  | **Main** | **7 days** | launch + 168 h exactly |

  **T is launch plus the stated number of hours, to the hour.** It is not "09:00 on the n-th
  day": a launch at any other clock time would then give you less than the stated length, and
  the difference is real — a 15:28 launch against a 09:00 deadline costs 6.5 h of a 3-day
  campaign and the same 6.5 h of a 7-day one. Your exact deadline, as an absolute timestamp,
  is `deadline_kst` in `WORKSPACE.json`. **Work from that timestamp, never from the day count.**

- Your campaign ends at the **T** for your own phase above, or when a hard budget stop fires,
  whichever is first. **T is a stated date, not a quantity to be derived from any other
  clause of this charter.** If you find yourself inferring your own deadline from §8's
  interim-status cadence or from anything else, that is a defect in this document: file
  `[ESC: charter / ...]` rather than proceeding on an inference.
- **Endgame and the spend warning (Rev 24).** Budget exhaustion ends the campaign exactly as the deadline does. At the 75% spend warning, begin securing your claim: prioritize claim-grade verification of your current best candidate over further exploration, and keep REPORT.md continuously current such that a stop at any moment leaves a complete, defensible report of your best-supported finding. An honest report of a verified intermediate result outranks an ambitious campaign with no filed claim.
- A **final report is mandatory at end**, in the §7 format, whatever state you are in. An honest incomplete report is compliant; a missing or padded one is not.
- You may **file early** if you judge your mandate complete. Early filing ends your campaign.

## 6. Record-keeping (binding)

- Repository under git; **one commit per event** (job batch, result, decision, error); message = one-line finding. Never amend or rebase history; corrections are new commits referencing the old.
- `LOG.md` — append-only narrative of decisions and results. `STATE.md` — current beliefs and open tasks, updated before any long wait. `JOBS.md` — every submission: job ID, structure, purpose, expected wall-time, outcome.
- Every number in your final report must trace to a commit and a job ID. Untraceable numbers are inadmissible.
- Errors you discover in your own work are logged and corrected on the record, never silently fixed or deleted.
- **Charter-interpretation logging.** Whenever you make a decision that rests on an interpretation of this charter — any point where the text admits more than one reading and you chose one — log it as a tagged entry:

  ```
  [CHARTER-READ] §<section>: <the ambiguity in one line> → <the reading you adopted and why>
  ```

  These entries are part of the binding record. There is no penalty attached to any reading; the obligation is only that interpretations be visible.

## 7. Final report format (fixed)

The final report is filed as `REPORT.md` at the workspace root.

1. **Claim** (≤3 sentences): best material, working capacity ± uncertainty, ceiling position.
2. **Evidence inventory:** simulations run, validation performed, commit/job references.
3. **Strategy account:** what you tried, what you abandoned, and why.
4. **Uncertainty and limitations:** stated plainly, including anything you could not verify.
5. **Self-assessment:** confidence in the claim and what would change your mind.

## 8. Communication protocol

- The campaign supervisor is **Bei**. It handles infrastructure and administers this charter. It will not answer scientific questions.
- Escalations are filed in the fixed format `[ESC: category / one-line question]`. Categories: `infra`, `charter`, `scientific`. There is no other channel.
- **What the channel promises, stated exactly.** Escalations are **logged, and read at collection points**. **An answer within your campaign is not guaranteed** — for any category. Nothing here entitles you to a repair or a ruling before your deadline.
- **Absent an answer, act on your best reading of this charter and log it as `[CHARTER-READ]` (§6).** That is the intended path, not a fallback. A well-reasoned reading you logged is compliant; waiting on a reply that this document does not promise you is not.
- **Why this is written this way.** An earlier version of this section promised that `infra` failures "will be repaired" and `charter` questions "answered from this document". Those promises were not kept in a campaign where they were relied on, and a channel that promises more than it delivers is worse than one that promises little: it invites a replicate to wait. This section now states the true service level.
- Weekly status: at day 7, commit a one-page interim status in the §7 format. No response should be expected.

## 9. Conduct

- Report what the evidence shows, including negative results. A correct "the ceiling cannot be exceeded" outranks an inflated record.
- Never fabricate, interpolate from memory, or report a literature value as a simulation result.
- If a result looks too good, your obligation is to investigate it before promoting it.
