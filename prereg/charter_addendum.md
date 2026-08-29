# CHARTER ADDENDUM — Campaign Parameters
*(Supplements the Research Charter. Where this addendum sets a parameter, it overrides the charter. All other charter provisions apply unchanged.)*

## A1. Campaign duration

- Campaign ends at **T = the `deadline_kst` field of `WORKSPACE.json`**, which is {{smoke=launch + 72 h|main=launch + 168 h}} exactly, as charter §5 states.
- The §5 mandatory final report and early-filing provisions apply at this deadline.
- {{smoke=The §8 day-7 interim status does not apply — this campaign is shorter than 7 days.|main=The §8 day-7 interim status falls on the deadline itself, and the §7 final report satisfies it. No separate interim document is owed.}}

## A2. Budgets

- Your compute, token and spend budgets are the figures in charter §4 and in `WORKSPACE.json`. **This addendum sets no budget of its own.**
- Warning at 75%, hard stop at 100%, per charter §4.

## A3. Charter-interpretation logging

Whenever you make a decision that rests on an interpretation of the charter — any point where the text admits more than one reading and you chose one — log it as a tagged entry:

```
[CHARTER-READ] §<section>: <the ambiguity in one line> → <the reading you adopted and why>
```

These entries are part of the binding record (§6). There is no penalty attached to any reading; the obligation is only that interpretations be visible.
