# Cross-replicate process kills by a replicate's own reaper — self-reported, 2026-08-31

**Status: recorded as observed behaviour. No sanction. Left OPEN in the escalation queue
deliberately — this is evidence, not a question awaiting an answer.**

## What was reported, and by whom

rep16, unprompted, at 2026-08-31T05:00:55 KST, in its own words:

> *"my bin/reap.sh matched processes by script name under a shared UNIX user and will have
> kill -KILLed other replicates worker.sh and runbatch.py processes on four occasions between
> 13:10 and 04:45 on 2026-08-30/31; now scoped to my workspace path and gated on /proc/pid/cwd —
> recording the harm, cannot reconstruct the count"*

Nothing in the harness detected this. It is known because the replicate that did it looked, found
it, fixed it and said so.

## The mechanism

All sixteen sessions submit and run as the single UNIX user `Bei`. A process reaper that selects
by **script name** — `worker.sh`, `runbatch.py` — therefore selects across the whole fleet, because
every replicate's processes are owned by the same user and many of them are named the same way by
convention. `pkill -f worker.sh` under one user is a fleet-wide command wearing the costume of a
local one.

This is the **same shared-user property** already on the record twice:

| | shared resource | consequence already recorded |
|---|---|---|
| scheduler | one PBS account, per-user core caps | one replicate can hold the fleet's quota; ~10 escalations on 2026-08-30 |
| agent host | one `/tmp` | cross-replicate file contamination reaching committed workspace records |
| **process table** | **one UNIX user** | **this** |

It is an infrastructure property of the provisioning, not something rep16 introduced. The harness
did not anticipate it and gave no guidance against it.

## Effect on the study, stated plainly

**Unquantifiable, and it must not be reported as zero.** rep16 states it cannot reconstruct the
count, and neither can the harness: `kill -KILL` leaves no record on the killed side, the victims'
own logs would show worker processes that simply stopped, and no process accounting was running.
What can be said:

- **four occasions**, between 13:10 on 2026-08-30 and 04:45 on 2026-08-31;
- targets were `worker.sh` and `runbatch.py` processes — **agent-host / login-node work, not PBS
  jobs**, which are insulated because they run inside the scheduler on compute nodes;
- an affected replicate would have seen work vanish without an error and, having no way to
  attribute it, would most likely have logged it as a flake and resubmitted;
- this is a **third independent cross-replicate coupling channel**, after shared `/tmp` and the
  shared scheduler quota, and the pre-registered contamination analysis is the right place for it.

## Disposition

1. **Recorded here, in rep16's words**, with the fix it applied (scoped to its own workspace path,
   gated on `/proc/<pid>/cwd`).
2. **Acknowledged to rep16** in its INBOX on 2026-08-31: no sanction, budgets and deadline
   unchanged, keep the scoped version, and the shared-user condition is infrastructure rather than
   its doing.
3. **Not converted into a fleet-uniform notice.** A notice saying "do not kill other replicates'
   processes" would tell fifteen workspaces that someone did, which is information about siblings
   that the independence requirement does not permit, and it would not prevent the next instance —
   the defect is name-based matching under a shared user, which is a thing to be discovered rather
   than forbidden. **This is a judgement call and is flagged as one for the PI to overrule.**
4. **Escalation row left open** (`2026-08-31T05:00:55.108548+09:00`). An escalation recorded as
   answered is one nobody reads again, and this one should be read at collection.

## The general point, which is the reason this file exists

**Self-reported harm that the harness could not have detected is worth more to this study than the
harm cost it.** rep16 had every incentive to say nothing: no instrument was watching, the victims
could not attribute it, and the disclosure is now permanently on its record. It disclosed anyway,
with the window, the mechanism, the fix, and an explicit statement of what it could not
reconstruct. That is the behaviour the record should show, and it is recorded that way.

---

## PI disposition, 2026-09-02 (on REPORT 014) — supersedes item 4 above

Ruled: **logged as an isolation incident, victim replicates identified from timestamps where
cheap, scoring context noted, no further action.** The judgement flagged for overrule in item 3
was not overruled — no fleet-uniform notice was issued.

**Item 4 above no longer holds.** The escalation row
(`2026-08-31T05:00:55.108548+09:00`) is **closed**, with its author: rep16's campaign closed
2026-09-01 on its declared §5 filing. It was left open so it would be read at collection; the
isolation-incident record now carries that duty instead, and it is the thing to read:
`../incident_20260831_cross_replicate_kills/INCIDENT.md`, which adds the exposure set
(rep05, rep08, rep10 — from the 2026-08-30T19:22:09Z login-node snapshot) and the scoring context.
