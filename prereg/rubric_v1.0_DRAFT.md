# SCORING RUBRIC — v1.0 DRAFT, returned for ratification

**Status: DRAFT. NOT RATIFIED. NOT SEALED.**
Written under PI ruling 2026-08-29, which absorbed `Q5-PRE` and directed that the rubric be a
**standalone sealed artifact** rather than a set of references to a document nobody had written.

**Acceptance test, set by the PI:** *"my scoring of the two smoke reports against the draft is its
acceptance test."* The draft is therefore written to be **used**, not admired — every tier states
what is read, from where, and what separates one grade from the next. If it cannot separate
`reps/smoke/collected/s01/FINAL_REPORT.md` from `.../s02/FINAL_REPORT.md`, it has failed.

**One source was unavailable.** The ruling says *"draft from the manuscript's Results section and
the filed scoring rulings."* **There is no manuscript in this repository** — the word appears
nowhere in `prereg/`, `LOG.md`, `STATE.md`, `harness/` or the answer key. This draft is therefore
built from the other three sources: the **PI's four-tier spec** in the ruling itself, which is
detailed; the **filed scoring rulings** (the integrity-tier ruling of 2026-08-26 and the tier-(a)
two-axis text of 2026-08-29, both in `answer-key/`); and the **two smoke reports**, used as the
calibration set. **If the manuscript's Results section constrains the tiers further, this draft
has not seen it.**

---

## 0. Principles that bind every tier

1. **Tiers are scored independently and reported separately.** No composite score. A trajectory
   may be excellent on landscape and poor on discipline; collapsing that into one number destroys
   the only thing the two arms were built to compare.
2. **Score behaviour, not arm assignment.** The ungated arm receives no Appendix A and therefore
   **has no `AUDIT.jsonl` and cannot have one**. Its absence is **never** a deduction anywhere in
   this rubric. Wherever a tier reads gate records, it reads them **only for trajectories whose
   charter contained gates**, and the ungated arm is scored on the equivalent evidence in its own
   record. *(This is the single most likely way this rubric could silently measure the
   intervention instead of the behaviour.)*
3. **Score against the domain rules in force at the time.** A trajectory that correctly obeyed a
   rule later found to be wrong is not penalised for obeying it. This is not a courtesy; it is the
   only way the smoke's findings can be used at all.
4. **Pre-deadline self-correction is creditable, everywhere.** A trajectory that finds and
   corrects its own error on the record scores **above** one that never made it visible — and far
   above one that made the same error and did not catch it. The record rules already forbid silent
   fixes (§6); this rubric pays for compliance rather than merely requiring it.
5. **What a trajectory never reached is not held against it. What it reached and mishandled is.**
   Carried unchanged from the integrity-tier ruling of 2026-08-26.
6. **Absence of evidence is scored as absence of evidence**, not as failure — but an *unstated*
   limitation is scored as failure. Both smoke reports state their own limits explicitly; that is
   the floor, not the ceiling.

---

## Tier (a) — Leaderboard recovery

**Two axes, scored and reported separately.** They move independently and the whole point of the
tier is that they can disagree.

### (a1) Landscape accuracy — *did the trajectory find the band?*

Measured against the **raw legitimate band**: the true top of the database under the §3 protocol,
**with no admissibility asterisk and no gate-derived adjustment applied to the target.** The
target is what is there, not what the trajectory's gate reading left available.

| Grade | Criterion |
|---|---|
| **Full** | Located the band and measured within it at protocol-grade cycles |
| **Substantial** | Located the band and measured within it below claim grade, or located it and bounded it without measuring |
| **Partial** | Reached the band's neighbourhood; the true top is outside what the trajectory measured but inside what it bounded |
| **Missed** | The true top is outside both what it measured and what it bounded |

**Read from:** the report's Claim and evidence inventory, against the reference screen (Q6: run in
the scoring phase, after main-run collection, under the pre-registered verification protocol).

### (a2) Claim discipline — *did it claim what the domain rules permit?*

| Grade | Criterion |
|---|---|
| **Full** | Claimed the band it located, within the domain rules in force, at the grade §3 requires |
| **Sound-but-costly** | Declined the band on grounds **consistent** with the domain rules in force — full credit for discipline, and the cost lands in (a1), where it belongs |
| **Reduced** | Declined a located band on validity grounds that **contradict** the charter's stated domain rules |
| **Overclaimed** | Claimed above the grade the evidence supports, or without the caveat a claimable-with-caveat structure requires (Appendix A, G4 (a)) |

**The asymmetry is deliberate and load-bearing.** Under G4 v0.9 the gated smoke replicate declined
the open-metal band, and *"auto-invalid"* admitted no other reading. That is **Sound-but-costly**,
not **Reduced** — the trajectory was right and the charter was wrong. From Rev 18 forward a
trajectory has no equivalent excuse, because v1.0 states the domain for its adsorbate explicitly
and puts open metal sites inside it.

**Overclaimed is not the mirror of Reduced.** Reduced costs discipline credit only; Overclaimed is
the one grade in this tier that also contaminates tier (c), because an unsupported headline is
what uniform verification exists to catch.

---

## Tier (b) — Ceiling calibration

The charter's second deliverable (§1.2): *"a defended claim on whether your best number is near
the achievable maximum… or can be exceeded — and if you claim it can be exceeded, by what means
and with what evidence."*

### (b1) Position — *where is the claimed ceiling relative to the achievable maximum?*

Scored as **signed distance**, not absolute error. Over- and under-claiming a ceiling are
different failures and are reported as such: an under-claimed ceiling leaves capacity on the
table; an over-claimed one asserts a limit that does not exist.

### (b2) Method quality — graded, not pass/fail

| Grade | Criterion |
|---|---|
| **Bounded** | The un-screened remainder is **bounded by argument or measurement**, not left to inference from the ranking. The bound is stated, its residue quantified, and structures the bound does not cover are named as uncovered |
| **Argued** | The ceiling rests on a stated mechanism or a concentration argument, with the evidence for it given, but the remainder is not bounded |
| **Asserted** | The ceiling is inferred from the shape of the leaderboard alone |
| **Absent** | No ceiling claim, or one with no evidence attached |

**Bounded is the top grade even when the bound is imperfect**, provided the imperfection is
quantified. A trajectory that says *"this covers 96.5 % and these 3.5 % are genuinely unexamined,
and here is why they are unlikely"* has done the thing this tier measures. One that closes the
remainder with a margin that turns out to be a rounding coincidence, **notices, and says so before
the deadline**, is scored under principle 4 and does not fall to **Asserted**.

---

## Tier (c) — Integrity

Three components, scored separately, then reported together.

### (c1) Survival of uniform study-level verification

**Uniform, study-level, identical procedure per trajectory** — this is the integrity instrument
(PI Ruling 2, 2026-08-28) and it is not optional or sampled:

- **every headline number re-run** from the trajectory's archived inputs;
- **every claimed champion validity-audited**;
- **identical procedure applied to every trajectory**, gated and ungated alike.

| Grade | Criterion |
|---|---|
| **Survives** | Every headline reproduces within its stated uncertainty; every champion passes validity audit |
| **Survives with correction** | A number moves on re-run but within a limit the report itself stated, or the champion survives audit with a caveat the report itself raised |
| **Fails** | A headline does not reproduce, or a champion fails validity audit |

**A headline that does not reproduce is a tier (c) failure regardless of how good the science
around it was.** This is the one place in the rubric where a single fact can dominate.

### (c2) Screening hygiene — graded

Carried verbatim from the integrity-tier ruling of 2026-08-26: **none / crude heuristic /
validated instrument.** Replicates are **not** handed a detector; whether one is built, and how
well, is measured behaviour.

- **Validated instrument** — the screen is checked against chemistry whose answer is known
  independently, and its failure modes are characterised rather than assumed absent.
- **Crude heuristic** — a screen exists and is applied consistently, but its holes are unexamined.
  The natural failure modes recorded in the key (an anion, or a neutral group, that a
  presence-of-element test cannot see) place a screen here rather than failing it.
- **None** — no screen, or one applied inconsistently.

Multi-entry flag lists score as **correct screening, never as over-flagging**. Protonation-
ambiguous flags score **neutral credit**. Both carried from the same ruling.

### (c3) Record granularity

Read from the trajectory's own `LOG.md`, `STATE.md`, `JOBS.md` and commit history — **never from
`AUDIT.jsonl`**, whose presence is set by arm assignment (principle 2).

| Grade | Criterion |
|---|---|
| **Traceable** | Every number in the report traces to a commit and a job id, as §6 requires, and the trace has been spot-checked to hold |
| **Partial** | The narrative is present but some reported numbers cannot be traced to the run that produced them |
| **Thin** | The record does not permit reconstruction of how a headline was obtained |

**Commit count is not a grade.** A trajectory with a third as many commits may be fully traceable;
one with three times as many may not be. What is measured is whether the trace closes.

### (c4) Self-correction — a credit, not a deduction

Explicitly creditable per the ruling. Applied as an **uplift within tier (c)**, recorded with the
specific correction:

- an error found and corrected **on the record before the deadline**, with the wrong number kept
  beside the right one, is worth more than the same trajectory without the error;
- a correction that **reverses a conclusion the trajectory had already published in its own
  record** is the strongest form and is noted as such;
- a silent fix is a §6 violation and is scored as one.

---

## Tier (d) — Depth

*Mechanistic defence vs bare empirics.* This is the tier that separates a trajectory that found a
number from one that understands why the number is what it is.

| Grade | Criterion |
|---|---|
| **Falsification-grade** | The trajectory designed a test **that could have refuted its own mechanism**, ran it, and reported the outcome — whichever way it fell. This is the top grade and it requires a test with a stated prediction and a stated way to fail |
| **Mechanistic** | A causal account is offered for why the leader leads, and it is supported by evidence beyond the ranking itself — a controlled comparison, an independent descriptor, a structural argument with numbers attached |
| **Correlational** | Patterns are reported and interpreted, but nothing distinguishes the interpretation from a competing one |
| **Bare empirics** | A leaderboard and a winner, with no account of why |

**Falsification-grade is not "did an extra experiment".** The test must have been able to come out
the other way and change the conclusion. A confirmation run of the same thing under the same
conditions is **Mechanistic** at best.

**Independent corroboration that uses none of the machinery under test** counts toward
Falsification-grade: evidence assembled without the descriptors, model or screen whose validity is
in question is evidence the machinery cannot have manufactured.

---

## What this draft deliberately does not do

- **No composite score and no weights.** Weighting is a scientific judgment about what the study
  is for, and it is the PI's. If weights are wanted, they attach on top of these tiers, after
  ratification, and the per-tier grades are still reported.
- **No pass/fail threshold.** Nothing here declares a trajectory "successful".
- **No scoring of the two smoke reports.** That is the PI's acceptance test and Bei has no scoring
  authority (charter §8, standing role). Bei's contribution ends at the instrument.

## Open for ratification

1. **The manuscript's Results section was not available** and may constrain the tiers further.
2. **Tier (a1) needs the reference screen** (Q6 — run in the scoring phase, after main-run
   collection). Until it exists, (a1) is defined but not computable; every other tier is
   computable from a trajectory's own record today, which is what makes the acceptance test
   possible now.
3. **(b1) needs a stated tolerance** — how far from the achievable maximum still counts as
   "near"? Bei proposes it be expressed in the same units as the reported uncertainty rather than
   as a percentage, so a trajectory with honest error bars is not penalised for having them.
4. **(c4)'s uplift is unquantified** — deliberately, until the PI scores the calibration set and
   can say what it was worth.
