# Design rationale — why each run chose its transformation, and why those parents

*Verbatim quotation only. Every passage is reproduced as filed, with its locus. No paraphrase, no
interpretation, and nothing is offered here as a judgement about whether a rationale was good.*

**Source:** each run's own `reps/main/collected/<run>/REPORT.md`. **All eight programs state their
rationale in the report; `LOG.md` was not needed for any of them.** Line numbers are into the
collected `REPORT.md`.

The eight programs are the runs in `analysis/agent_modified_structures.csv`: rep02, rep05, rep06,
rep09, rep10, rep12, rep15, rep17.

---

## rep02 — interpenetration removal · 1,713 files

**Why this transformation** — `REPORT.md` line 258:

> *"**The modification route — §2's "by what means", and the answer is that this means was not
> enough.** §2 asks whether the best number can be exceeded and by what means; this route came
> within 1.4% and did not. Interpenetration removal was chosen because it is charge-balanced *by
> construction*: if the framework bond graph falls into components sharing no bond, each is a
> complete net, so deleting one leaves the rest balanced. 1,817 of 12,499 structures are
> interpenetrated, 1,112 with all nets 3-periodic. *The effect is large and it is measured as a
> paired comparison, parent against its own analogue, so nothing about it depends on the two
> families being comparable populations.*"*

**Why these parents, and the limit rep02 places on its own selection** — line 423:

> *"**The modification space, and the biggest single gap in this report.** Interpenetration removal
> is one modification of many. The porosity-window limitation was removed — all 1,065 analogues of
> every all-3-periodic interpenetrated parent are built, described and either measured or queued.
> **But the route was defined only over 3-periodic nets**, which silently excluded the 1,885
> database entries with maxdim 2 — the family the claimed material itself belongs to."*

---

## rep05 — isotropic lattice scaling · 35 files

**Why this transformation, and what rep05 says it is and is not** — line 28:

> *"**This is the ceiling of this database but not of this protocol**: an exhaustive census of the
> 319 distinct materials occupying the high-capacity region of descriptor space found nothing above
> it, while isotropically compressing this same framework by 4% raises its working capacity to
> **214.35 ± 0.61**, verified at claim fidelity with no grid against a control of 206.62 measured
> the same way, so the limit reflects what was enumerated rather than methane's behaviour between
> 5.8 and 65 bar — but the compressed structures have covalent bonds shortened below chemical
> plausibility and are offered as evidence about the ceiling, not as materials."*

**Why these parents** — line 147, heading and series:

> *"### 2.6 The ceiling can be exceeded — verified at claim fidelity*
> *Isotropic lattice scaling of the winner. Screening curve first, floor fidelity with the grid,
> thirteen points (`mods/MANIFEST.tsv` carries a SHA-256 each)"*

and the extension to eight frameworks, same section:

> *"The scaling series repeated on the eight highest-capacity distinct frameworks (batches
> `m1`/`m2`/`m4`/`m5`, floor fidelity). Each control is that framework's **own factor-1.000 run
> through the modified path**, so every gain is a within-batch difference"*

---

## rep06 — de-interpenetration · 4 files

**Why this transformation** — line 236:

> *"**Attempted, and the honest status is incomplete: structural modification.** De-interpenetration
> was chosen as the modification most likely to raise working capacity, with matched pristine
> controls in the same batch (G5)."*

**The same passage continues, and it is quoted because it is part of the same statement** — line 238:

> *"The three pristine controls completed; **all modified runs failed silently and produced no
> output**, and the recovery path could not repair it because the recovery path was itself the
> defect — `gcmc_sweep.py` validated structure names against the read-only database only, so it
> rejected every modified structure and requeued nothing while reporting the round complete (LOG,
> Defect 13). Fixed and requeued 2026-08-31. **If those runs do not land before the deadline, the
> modification arm reports as untested, not as negative.**"*

*Both passages are in the filed report. The results table at line 116 carries four completed
matched pairs, so the requeued runs landed. The two are quoted together, in file order, without
being reconciled here.*

---

## rep09 — defunctionalisation · 209 files

**Why this transformation, and why these parents — one sentence carries both** — line 166:

> *"**The modification arm** (§3 permits structural modification; charge balance holds by
> construction because every substitution is monovalent-for-monovalent, substituent → H). 209
> products were built from the 1,054 structures above N65 = 200 that carry a removable terminal
> group; 208 completed at both pressures. Defunctionalisation raises screening working capacity by
> **+11.18 ± 11.31 cm³/cm³, 185 of 208 improving, best single gain +54.12**, and the entire effect
> is in the low-pressure leg — N65 moves by +1.08 on average while N5.8 falls by 10.10. That is the
> mechanism written into `modify.py` before any of it was measured, and it confirms the physics
> above."*

**Why the selection could not reach the leaders** — line 176:

> *"**But the arm does not reach the ceiling**: the best product is 191.99, below the unmodified
> leaders, for two measured reasons — none of the top six candidates carries a removable terminal
> group at all, so the arm cannot touch them by construction; and the gain shrinks as the source
> improves (Pearson −0.463; sources already above 170 gain only 1.67). Defunctionalisation moves
> functionalised structures *toward* the ceiling the unfunctionalised ones already occupy and stops
> there."*

---

## rep10 — methylation · 24 files

**Why this transformation, why these parents, and the mechanism stated in the same passage** —
line 73:

> *"**Structural modification (charter section 3 arm).** Methylation of framework C-H,
> charge-balanced by construction and reproducible from (parent, fraction, seed) via
> `bin/methylate.py`. Across 20 variants of the six best frameworks at substitution fractions
> 0.25-1.0, every variant screened below its parent and monotonically worse with more methylation.
> These frameworks already sit at void fraction 0.87-0.93; methylation removes pore volume (lowering
> 65 bar loading) and deepens binding (raising 5.8 bar loading), and working capacity is the
> difference, so both effects push the same way. The four variants the model liked best were sent to
> GCMC to test the negative result rather than assume it."*

*(Same line, continuing)*:

> *"Read against the void-fraction trend above, this is not evidence that modification cannot help
> but that methylation is the wrong DIRECTION: below the peak capacity rises with void fraction, and
> methylation lowers it. The uphill direction is the opposite one -- linker-vacancy defects raising
> void fraction toward the peak -- and whether headroom exists there is decided by the void-fraction
> screen above."*

---

## rep12 — methylation and fluorination · 7 files

**Why this transformation and why these parents** — line 145:

> *"**The modification route, tested and closed for these scaffolds.** Charter §3 permits structural
> modification. **Seven** charge-balanced variants of the two best structures were built
> (`bin/modify.py`: aromatic C–H → C–CH₃ and C–H → C–F, both charge-neutral by construction, which
> is what makes "charge-balanced" meaningful under a chargeless protocol; no metal touched, so
> G4(b)(1) is not engaged; rotamers scanned over 36 torsions with a **parent-relative** clash test),
> each against its pristine parent at identical settings, which is what G5 requires."*

**The scope rep12 places on its own conclusion**, same section:

> *"**That it cannot be exceeded by decorating these scaffolds: high confidence, for these scaffolds
> only.** Seven variants across two parents, monotone decline with coverage, no exception. I tested
> decoration — methylation and fluorination — not defect creation, linker substitution or topology
> change, and I do not claim beyond what I measured."*

---

## rep15 — terminal-aqua removal (`+DEAQ`) · 251 files

**Why these parents, first application** — line 220:

> *"206 structures built from the 670 FSR-only parents the database never offers desolvated.
> Measured 206/206; best **174.0**; none above the leader."*

**Why a second application was needed, and why those parents** — line 223:

> *"*Second application, and this is the one that answers §1.2.* The first arm tested the
> modification only on structures that were poor to begin with, which does not answer whether the
> **best** number can be exceeded. So `bin/mod_gain.py` measured the effect on 42 paired
> parent/child runs of my own: **mean +18.6, median +13.7, max +74.8, and 41 of 42 children beat
> their parent.** The modification is large and real. Then `bin/mktopmods.py` applied it to the top
> of the measured leaderboard — and found removable terminal aqua in **1 of the top 400
> structures**, and in 48 of the top 1,500, all 48 already built. The gains are large *because* they
> unblock a pore that was blocked (the best case is 23.3 → 98.1), which can only happen where
> capacity was near zero. The leader's pores are already open."*

---

## rep17 — methylation and fluorination · 10 files

**Why this transformation, and why no other axis was available** — line 147:

> *"§3 permits modifying a database structure if it is chemically charge-balanced and reproducibly
> prepared. The available axis is **decoration of the pore wall** — rewiring the topology would make
> it a new structure, which §1 puts out of scope. Aromatic C–H → C–CH₃ and C–H → C–F both preserve
> every valence exactly, so charge balance is structural rather than argued. `scripts/methylate.py`
> and `scripts/fluorinate.py` are deterministic: farthest-point site selection, methyl torsion
> optimised against contacts, pair-dependent clash criteria."*

**Why this parent, and the series design** — line 153:

> *"Seven methyl counts at floor cycles, parent 207.60 ± 0.93: … An inverse-variance-weighted
> quadratic gives **WC(k) = 207.672 + 0.0014k − 0.00777k²**, every residual inside its own error
> bar, **vertex at k = 0.09 methyls, 0.000 cm³/cm³ above WC(0)**. The methylation optimum is the
> unmodified parent. Fluorine is linear and worse: −0.385 and −0.396 per site at 24 and 44
> substitutions."*
