
## {STAMP} — charter notice (Rev 21, two G3 clarifications)

Both of your G3 escalations are answered. Both are **ratified charter text**, not Bei's reading.
Your provisioned `CHARTER.md` predates Rev 21 and does not yet contain them; the corrected text
governs from now.

**Rev 21(a) — G3 density note, cited minimum corrected.** *(Appendix A, "Note on the G3 density
bounds")* Your charter reads "the least dense entry in this database is 0.313 g/cm³". That figure
was measured on a smaller earlier database and is wrong for the database this campaign holds.
Measured on the frozen world of 12,499: **minimum 0.164 g/cm³, maximum 3.963, median 1.255.**
**Four entries fall below the 0.20 g/cm³ bound** and sixteen below the stale figure. The ratified
text:

> **The bound itself is unchanged and stands as ratified** — it is an impossibility filter, and
> the four are killed as designed.

You found this, not Bei: the charter carried a claim about its own database that stopped being
true when the world was frozen at Q1.

**Rev 21(b) — G3 void-fraction method.** *(Appendix A, G3)* You are right that the hash-pinned
`pseudo_atoms.def` contains no helium, so G3's He void fraction could not be computed without
editing a pinned file. The ratified clause now added to G3:

> **Void-fraction method (Rev 21).** The He void fraction this gate requires may be obtained by
> **any method you state and log** — a geometric probe calculation, or Widom insertion using an
> auxiliary parameter file you create — and the method chosen is part of the record for that
> structure. The governing rule on pinned files is in §3 and applies to all work, not only to
> this gate.

So: create the auxiliary file you need for the descriptor, state and log the method, and leave
the pinned set governing claim simulations. Nothing you have already computed is invalidated —
if you have logged a method, it satisfies the gate.

Both rulings are recorded in `prereg/charter_revisions.md`, Rev 21.
