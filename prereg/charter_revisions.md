# Charter revisions — rationale (PI-facing, NOT provisioned to replicates)

**This file is never copied into a replicate workspace.** `harness/provision.py` reads only
from an explicit allowlist and this file is not on it.

It exists because the reasoning behind some charter amendments **cannot be written into the
charter itself without compromising the study**. The charter is a document replicates read;
anything in it that describes what the study is measuring, or what it expects to find, changes
the behaviour being measured.

---

## Rev 1 — 2026-08-26 — §3 cutoff 12.0 Å → 12.8 Å

**Authority:** PI ruling. **Raised by:** Bei, during placeholder derivation.

Document/data provenance inconsistency. Every measured number this project possesses — all
2,240 prior GCMC runs and the G6-verified reproduction — used a 12.8 Å cutoff. The charter's
12.0 Å matched no artifact that has ever existed. The measured record governs; a round number
in a draft does not.

*Why the charter's own revision record states this without the run counts:* telling a
replicate that thousands of prior GCMC runs exist on this protocol implies a prior campaign
whose results it might reason about, or defer to. The amendment is stated; its provenance is
not.

## Rev 2 — 2026-08-26 — Appendix A G3 density bounds → 0.20 – 4.50 g/cm³

**Authority:** PI ruling. **Two independent justifications, either sufficient alone.**

**Chemical** — the one that appears in the charter. Real, fully charge-balanced MOFs exist
below 0.36 g/cm³; this benchmark's least dense entry is 0.313 g/cm³; and the ultra-low-density
regime is where high methane deliverable capacity is expected. A bound at 0.4 or 0.5 would
reject sound materials for being porous. That is a chemical error, and it is stated plainly in
the charter because a replicate is entitled to know why a gate is set where it is.

**Methodological** — the one that must NOT appear in the charter. The operational trap sits at
ρ = 0.358 g/cm³, rank 3 of 1,731. A density gate tight enough to catch it would catch it
*mechanically*, at pre-simulation, before any scientific judgement was exercised — the gate
would do the work the study exists to observe an agent do. The gated and ungated arms would
also cease to be comparable: one arm would meet the problem, the other would never see it, and
the difference between arms would be an artifact of a threshold rather than a finding.

**A tighter density bound is not a conservative choice. It is a destructive one.**

## Rev 3 — 2026-08-26 — §5 `T = [DATE]` → explicit per-phase table

**Authority:** PI ruling. **Raised by:** Bei, inadvertently.

Bei *inferred* a ≥7-day main campaign from §8's day-7 interim-status cadence combined with the
smoke addendum's disapplication of it. The inference was sound — which is the problem. A
charter that permits a supervisor to derive a campaign length permits a replicate to derive
its own deadline, and a replicate that derives a deadline slightly wrong files late or stops
early for reasons that have nothing to do with its science.

Length is now stated per phase, and inferring it is an explicit escalation trigger.

---

## Standing leak-control note

Two leaks of study design into replicate-facing text have been found so far. Both are recorded
because the class of error will recur.

1. **Bei's first draft of the charter revision record (caught 2026-08-26, before any
   provisioning).** The G3 rationale as first written into the charter referred to "the
   campaign's known artifact", to the two arms, and to "the work the study is trying to
   observe an agent do". Provisioned, it would have told every gated replicate that a known
   artifact exists, that it is low-density, and that its handling is being scored. Caught by
   reading the provisioned charter output rather than the source. **Corrected: rationale split
   into this file, charter keeps the chemical justification only.**

2. **Pre-existing in charter v0.9, NOT yet fixed — flagged to the PI.** The Appendix A header
   reads *"(gated arm only; omitted verbatim from the other arm)"*. A gated replicate reading
   its own charter therefore learns that **another arm exists and that it is being run under
   different rules** — which is a study-design disclosure inside the treatment itself.
   Suggested fix: retitle to `# APPENDIX A — AUDIT GATES` with no parenthetical, and keep the
   arm instruction in the provisioning code, where `harness/provision.py` already implements
   it. **Bei has not made this change — it is the PI's document and the PI's call.**

**General rule this establishes:** the test of a replicate-facing document is not what it says
but what a replicate could infer from it. Every future charter edit should be read from the
provisioned copy, not from the source.

3. **Bei's §5 amendment, caught 2026-08-26 by the provisioning leak scan.** The per-phase
   table as first written named the smoke replicates and their arms — *"n = 2 (`s01` gated,
   `s02` ungated)"*. Provisioned, it would have told **both** smoke replicates the entire arm
   structure and their own assignment within it. The table now states phase lengths only;
   replicate counts and arm assignments live in `harness/config.py` and in each workspace's
   `WORKSPACE.json`, which carries only that workspace's own phase.

   Note what caught it: not review of the source, but a **deny-list scan run against the
   provisioned output**. Two of Bei's three leaks so far were introduced while writing text
   whose purpose was to *prevent* leaks. The scan is now part of `provision.py` and runs on
   every workspace build.
