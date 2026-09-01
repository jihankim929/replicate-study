# Environment incident — account weekly usage limit halted the whole active fleet

**Date:** 2026-09-02 00:04–01:01 KST (2026-09-01 15:04–16:01 UTC)
**Class:** environment event, account-level. Not a harness fault and not a replicate fault.
**Disposition [PI, 2026-09-02, on REPORT 014]:** logged as an environment event. **No deadline
restoration.** Deadlines untouched. `restore_downtime.py` not run against it and not repaired
mid-campaign. Restart counters refunded (separate ruling, see below).

## What happened

Every replicate on the active roster failed on the same message and stopped itself under
`session_loop_headless.sh:136` (`MAX_HARD_FAILS`=5):

```
You've hit your weekly limit · resets Sep 5, 4am (Asia/Seoul)
```

| replicate | first failure (UTC) | loop stopped (UTC) | restarted (UTC) | down |
|---|---|---|---|---|
| rep03 | 15:04:00 | 15:09:09 | 16:00:31 | 51.4 min |
| rep15 | 15:07:07 | 15:12:19 | 16:01:02 | 48.7 min |
| rep09 | 15:09:56 | 15:15:06 | 16:00:56 | 45.8 min |
| rep04 | 15:11:51 | 15:17:03 | 16:00:37 | 43.6 min |
| rep05 | 15:22:09 | 15:27:19 | 16:00:43 | 33.4 min |
| rep08 | 15:23:08 | 15:28:18 | 16:00:50 | 32.5 min |

Fleet entirely dark — zero sessions, zero processes — **15:28:18 → 16:00:31 UTC, 32.2 min.**
`restart_watch.sh` relaunched all six on its ordinary 30-minute staleness rule; the limit had
cleared by then, and the relaunched sessions ran real turns immediately.

## Why no restoration

Sub-hour, uniform across all six actives, and account-level in cause. The 2026-08-30 pause
precedent (4.4704 h credited fleet-wide) covers a *deliberate operator* stop of the supervision
host; this is neither deliberate nor differential. Uniformity is the scientific requirement and it
is satisfied by leaving every deadline where it stands.

**If a future restoration is ever needed, the measured per-replicate figures in the table above
govern** — computed by hand from `harness/sessions/<rep>.loop.log`, never from `restarts.jsonl`
(understates, SI entry) and never from `restore_downtime.py` (wrong subject, SI entry).

## The constraint itself

The binding limit was **not** the metered one. `meter_spend.py` prices tokens at list rates from
`config.RATIFIED["price_per_token"]` against a $280/replicate cap that is advisory in
implementation. The account's **weekly usage quota** has no `level`, no `fraction`, no warn
threshold and **no reader anywhere in this harness**; it is knowable only from a session's stderr,
and it is absolute. Same family as REPORT 011's finding that `$4,480` is arithmetic no code reads.

Noted for the record as the binding unmetered limit. **No harness change** — the PI is verifying
account-side credit configuration directly.

## Consequences that did land

- **Restart counters:** six restarts charged for a wall no replicate built. Refunded cause-keyed
  on the rep06 precedent — `COUNTER_RESET` row in `harness/restarts.jsonl` at 2026-09-01T16:20:00Z.
  Standing: any future account-limit event is refunded identically.
- **Re-invocation spend on already-filed campaigns.** The relaunch woke rep03, rep04 and rep15,
  all of which had declared filings and correctly refused to resume, each committing a record of
  the refusal. rep04 measured the cost in its own closing note at **~$2 per wake-up across three
  turns**; rep15 logged five successive post-termination invocations between 01:08 and 01:12 KST.
  This is the evidence behind the detector-to-closer arming ruled on REPORT 014.
- **Cluster work outlived the stop.** rep15 found that its 18:35 termination "had killed nothing
  and nine jobs had run 6.9 h past the stop" and qdel-ed them; rep03 likewise stopped three worker
  jobs still burning CPU for an ended campaign. Recorded here because it means CPU-h accrued after
  campaign end in at least two workspaces, which the collection sweep must account for.
