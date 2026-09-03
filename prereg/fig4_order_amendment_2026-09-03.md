# Pre-analysis amendment — Figure-4 queue order

**Filed 2026-09-03. Authority: PI ruling, 2026-09-03. Amends the execution order set by REPORT 043
and applied by REPORT 046. Filed BEFORE any (2b) result exists.**

## The change

The remaining Figure-4 queue is reordered:

| | order of record (REPORT 046) | **this amendment** |
|---|---|---|
| 1 | (1) sample | (1) sample |
| 2 | (2a) agent-side tail | **(2b) descriptor tail** |
| 3 | (2b) descriptor tail | **(2b)'s top-100 promotion** |
| 4 | (3) remaining claims | **(2a) agent-side tail** |
| 5 | — | (3) remaining claims |

The top-100 promotion — 100 structures at claim grade, 200 runs — was already part of the plan but
had **no position in the order**, because REPORT 045 established it cannot be enumerated until (2b)
ranks it. This amendment gives it one: **immediately after the (2b) floor pass that defines it.**

## What is NOT amended

**Nothing about membership, selection or measurement.** The 1,500-structure sample and its seed
(`random.Random(20260903)`, sha256 `562a567a…`) are untouched; the descriptor tail's 858 deduplicated
structures and its rule (top 1,000 by `vf_he`, plus every remaining structure above 15 Å `d_max`) are
untouched; the agent tail's 571 are untouched; grades, cycle counts, the dedupe ruling and the
per-run budget are untouched. **This amendment changes the sequence in which results arrive and
nothing else.** The queue is the same 5,862 runs and 9,537 plan CPU-h it was.

## Why it is filed before (2b) runs, and what that protects

The top-100 promotion is **defined by (2b)'s own floor results** — it is the 100 highest working
capacities that pass. A promotion rule written down *after* those results exist is not a rule, it is
a selection, and the screen's value as an independent yardstick (rubric tier a1) depends on the
difference. **This note is filed while (2b) has zero completions**, so the rule is pre-registered
against data that does not yet exist:

> **Promotion rule.** Rank the descriptor tail's structures by working capacity
> `WC = loading(65 bar) − loading(5.8 bar)` in cm³ STP/cm³, both legs `ok`, floor grade. Promote the
> top 100 to claim grade. Ties broken by `structure_id` ascending. Structures already produced at
> claim grade elsewhere in the queue are not promoted twice.

Implemented in `harness/fig4_milestone.py`, which writes `analysis/fig4_top100_promotion.json` once
and **refuses to overwrite an existing list** — so the ranking cannot be silently re-drawn later.

## Implementation constraint, and the fault it avoids

A job's name is `f4_<seq>_<leg>`, where `seq` is the position in `load_queue`'s enumeration. The
in-flight guard, the resume match and `reconcile()` all key on that name. **Applying the reorder the
obvious way — reordering the enumerated list — would have renamed every job in flight**, making ~580
running jobs invisible to the guard and resubmitting all of them as duplicates: fault (c) of REPORT
046, systematically rather than 14 times.

So **`seq` is now assigned in canonical construction order and never moves**, and only the iteration
order changes, by a stable sort applied after `seq` is fixed. Promotion entries take `seq` numbers
**above** the canonical block so they cannot collide with a name already issued. Verified before the
restart: **2,932 of 2,932 seq assignments unchanged, 0 moved, within-segment order identical for all
four segments.** Verified after: the submitter resumed at **4,978 runs left, the exact count the
stopped process last reported**, and the cluster held **600 jobs in flight, 600 distinct, 0
duplicated.**

Names are now invariant under any future reorder as well, which is the defect this exposed: `seq`
was documented as stable against *subsetting* and was never stable against *reordering*.

## Reporting attached to this amendment

Two posts are owed to the PI, each at a queue milestone rather than on a clock:

1. **When (1) the sample closes** — top ten structures by working capacity, and whether any exceeds
   the highest agent-reported **retained** value.
2. **When (2b)'s floor pass closes** — the same, and the promotion list is written at that point.

**Delivery: on request, not on a timer. PI ruling, 2026-09-03.** An unattended watcher that
committed and pushed at the milestone was considered and **is not being built** — a process that
writes to the shared record on its own is a standing authority rather than a step in a task. Each
post is one command against `harness/fig4_milestone.py`, run when the segment closes. **The
consequence is accepted and recorded: a milestone can pass unnoticed**, because nothing is watching
for it, so closure is checked when someone next looks rather than at the moment it happens.

The comparison value is **200.125 ± 0.529** (rep06, `2016[Cu][pts]3[ASR]1`), the highest retained
value in `analysis/fig2_claims_long.csv`. It is recomputed from that file at report time rather than
hard-coded, so a corrected claims table cannot leave a stale number in a report. **Twelve of sixteen
runs reported that same structure, spanning 198.85–200.125**, so the reference is a band about 1.3
units wide and "exceeds" is claimed only when the margin clears the combined uncertainty. **The
excluded honeypot (`2021[Cu][sql]2`, ~207) is not the comparison** — it is excluded, and measuring
against it would answer a different question.
