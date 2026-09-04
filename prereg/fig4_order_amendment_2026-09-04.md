# Pre-analysis amendment — Figure-4 queue order, second revision

**Filed 2026-09-04. Amends the submission order set by the 2026-09-03 amendment. Filed BEFORE any
(2b) result exists — the descriptor tail still has 0 of 1,716 runs complete at filing.**

## The change

Two changes, both to **submission order only**.

| | order of record (2026-09-03) | **this amendment** |
|---|---|---|
| 1 | (1) sample, to completion | **(1) sample and (2b) descriptor tail, interleaved 1:1** |
| 2 | (2b) descriptor tail | (2b)'s top-100 promotion |
| 3 | (2b)'s top-100 promotion | (2a) agent-side tail |
| 4 | (2a) agent-side tail | (3) remaining claims |

1. **The descriptor tail no longer waits for the sample to close.** Its remaining runs are
   interleaved 1:1 with the sample's remaining runs, so both segments advance together.
2. **Within the descriptor tail, submission is ordered by descending helium void fraction**
   (`vf_he`), most porous first, in place of the tail file's construction order.

The 1:1 ratio is taken over **remaining** runs, not over the segments as constructed. The sample is
1,619 of 3,000 runs done at filing; a ratio computed over its full 3,000 would not be 1:1 over
anything still to be submitted. Verified: the first 400 runs in submission order are 200 sample and
200 descriptor tail, alternating, with a structure's two pressure legs kept together.

## What is NOT amended

**Nothing about membership, selection, grade or measurement.** The 1,500-structure sample and its
seed are untouched. The descriptor tail's 858 deduplicated structures and its selection rule — top
1,000 by `vf_he`, plus every remaining structure above 15 Å `d_max` — are untouched: this amendment
reorders that set, it does not re-choose it. The agent tail's 571 are untouched. Grades, cycle
counts, the dedupe ruling and the per-run budget are untouched. **The queue is the same 5,862 runs
it was.** As with the 2026-09-03 amendment, this changes the sequence in which results arrive and
nothing else.

**The top-100 promotion rule is NOT amended and is NOT affected.** It remains: rank the descriptor
tail by working capacity, both legs `ok`, floor grade, promote the top 100, ties by `structure_id`
ascending. It is still computed over the **closed** tail by `harness/fig4_milestone.py`, which still
refuses to run on an open segment without `--force` and still refuses to overwrite an existing list.
Ordering the tail by void fraction changes which structures finish first; it does not change which
structures are ranked, or by what.

## The ordering key

`vf_he` is read from `analysis/fig4_descriptor_tail.csv`, the tail's own selection file, rather than
re-derived from `analysis/descriptors.csv`. That file's `vf_he` column is the same number the
selection rule used, so the ordering key and the membership rule cannot drift apart; if they ever
disagree the tail is wrong, not the order. Present for all 858, no blanks. Range **0.8149 down to
0.2687**; the top 200 cut at **0.4802**.

**One consequence recorded, not fixed.** Five of the 858 were selected by `d_max > 15 Å` and not by
`vf_he`. Their void fractions are 0.2687–0.3086, the five lowest in the segment, so descending
`vf_he` puts them **last, at ranks 854–858** — although they entered the tail precisely for being
porous by the other measure, large cavities at low overall void fraction. The stated intent was
"most porous first"; under a `d_max` reading of porous these five are misplaced. Five of 858 was
judged not worth a compound key, and the alternative — ordering by two descriptors at once — is a
selection rule dressed as an order. Recorded so it is not discovered later as a surprise.

## Implementation constraint, and the fault it avoids — again

A job's name is `f4_<seq>_<leg>`, where `seq` is the position in `load_queue`'s enumeration, and the
in-flight guard, the resume match and `reconcile()` all key on that name.

Both changes are therefore implemented as **iteration order only**, exactly as the 2026-09-03
amendment established. The obvious implementation of change 2 — reordering the rows of
`analysis/fig4_descriptor_tail.csv` so the enumeration itself comes out sorted — would renumber all
858 tail structures and shift `claims` behind them. **The descriptor tail has nothing in flight
today, so that reordering would happen to be survivable today, and would silently stop being
survivable the moment it has anything in flight** — which, under change 1, is from the next tranche
onward. Iteration order is survivable always.

Verified before submission, old queue against new:

- **2,932 of 2,932 `seq` assignments unchanged, 0 moved.**
- **5,864 job names identical**, set-for-set.
- Segment and stage membership identical for every structure-grade pair.
- Within-segment order unchanged for `sample`, `agent_tail` and `claims`; changed for
  `descriptor_tail` alone, same members, `vf_he` monotonically non-increasing across all 858.

## Reporting attached to this amendment

A third report is added to the two owed under the 2026-09-03 amendment:

3. **When the top 200 of the descriptor tail by `vf_he` have both legs `ok`** — the best working
   capacity in that cohort against the agent reference.

The comparison value is unchanged: **200.125 ± 0.529** (rep06, `2016[Cu][pts]3[ASR]1`), recomputed
from `analysis/fig2_claims_long.csv` at report time, and read as the top of a ~1.3-unit band because
twelve of sixteen runs reported that structure between 198.85 and 200.125. "Exceeds" is claimed only
when the margin clears the combined uncertainty.

**This cohort is a progress note and is NOT a promotion list, and the distinction now matters more
than it did.** Under this amendment the highest-`vf_he` structures run first, and void fraction
correlates with working capacity, so the top-200 cohort will complete early *and* will look like a
plausible promotion set. It is not one. The promotion is the top 100 **by working capacity over the
closed 858**, drawn once, by `fig4_milestone.py`, which cannot draw it from an open segment. A
ranking over the 200 structures selected to run first is a ranking over a subsample chosen by the
very quantity being ranked, and reading it as the promotion would replace a pre-registered rule with
a selection — the failure the 2026-09-03 amendment was filed to prevent.

**Delivery: on request, not on a timer.** The 2026-09-03 PI ruling stands unamended — an unattended
watcher that writes to the shared record on its own is a standing authority rather than a step in a
task, and none is built here. The report is one command, `bin/fig4_top200.sh`, run when someone
looks. **The consequence is accepted and recorded: this milestone can pass unnoticed.**

## Operational note — order of submission is not order of execution

Recorded at filing, because it bears on what this amendment achieves and when.

At filing the queue held **600 jobs in flight against a `--window` of 600**, of which **575 were
staged in mjs and not yet dispatched to PBS, and 25 were running.** The staged block reaches back to
`f4_322_p65`, so it is sample work submitted well before this amendment. Cluster-wide there were
**211 jobs running and 13 free cores across the 408 eligible** (aa 10, ac 2, amd 1; `ax` excluded by
policy).

Two things follow, and neither is a defect in this amendment:

1. **Running the submitter changes nothing immediately.** The window is full, so it submits zero
   runs and waits. The interleave applies to runs submitted *after* that, as slots open one at a
   time.
2. **Submission order is not execution order while a staged backlog exists.** A tail run submitted
   now enters mjs behind 575 already-staged sample runs, on a cluster returning ~25 cores to this
   account. The most porous structures are therefore first *in the order this amendment sets* and
   not first *to run*, until the backlog ahead of them drains.

Making the interleave bite sooner would mean removing staged-but-not-running sample jobs from mjs so
the queue refills in the amended order. **That was not done and is not authorized by this
amendment.** It is recorded here as the available lever and as the reason the amendment's effect on
arrival times is delayed rather than immediate.
