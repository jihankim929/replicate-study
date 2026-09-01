# Isolation incident — one replicate's reaper killed sibling processes under the shared UNIX user

**Reported:** rep16, unprompted, 2026-08-31T05:00:55 KST. **Window:** four occasions between
13:10 on 2026-08-30 and 04:45 on 2026-08-31 KST.
**Class:** isolation failure. Third independent cross-replicate coupling channel, after shared
`/tmp` (`incident_20260831_tmp_collision/`) and the shared PBS quota.
**Disposition [PI, 2026-09-02, on REPORT 014]:** logged as an isolation incident, victim exposure
identified from timestamps where cheap, scoring context noted, **no further action, no
investigation.** Escalation row closed with its author (rep16 closed 2026-09-01).

The self-report, the mechanism and the harm statement are recorded in rep16's own words at
`../observed_behavior/2026-08-31_cross_replicate_process_kills.md`. This file adds only what the
ruling asked for.

## Mechanism, in one line

All sixteen sessions run as the single UNIX user `Bei`, so a reaper selecting by **script name**
(`worker.sh`, `runbatch.py`) selects fleet-wide. `pkill -f worker.sh` under one user is a
fleet-wide command wearing the costume of a local one. Infrastructure property of the
provisioning, not something rep16 introduced.

## Exposure set — identified where cheap, and it is exposure, not confirmed harm

The only cheap timestamped evidence inside the window is the login-node process snapshot taken at
**2026-08-30T19:22:09Z (04:22 KST 2026-08-31)** — 23 minutes before rep16's last reported
occasion — at `../incident_20260831_login_node/bnode0_ps_20260830T192208Z.txt`. Replicates with
processes co-present on the shared login node at that instant:

| replicate | processes in snapshot |
|---|---|
| rep05 | 50 |
| **rep16** (the reaper) | 34 |
| rep10 | 10 |
| rep08 | 6 |

**So the exposure set for at least the 04:45 occasion is rep05, rep08 and rep10.**

This establishes **who was exposed, not who was killed**, and the distinction is load-bearing:
`kill -KILL` leaves no record on the victim side, no process accounting was running, and the
snapshot enumerates `simulate` processes rather than the `worker.sh` / `runbatch.py` names the
reaper matched. The other three occasions have no snapshot at all and no exposure set is
reconstructible for them. rep16 stated it could not reconstruct the count; neither can this.
**The harm must not be reported as zero, and it must not be reported as three.**

## Scoring context

- The affected work is **agent-host / login-node work, not PBS jobs** — jobs inside the scheduler
  on compute nodes are insulated. So the exposure is to local orchestration, not to simulation
  results already banked.
- A victim would have seen work vanish **without an error** and, having no way to attribute it,
  would most plausibly have logged a flake and resubmitted. Any such resubmission is charged to
  that replicate's own spend and CPU-h, so **rep05, rep08 and rep10 may carry cost and lost wall
  clock in the 2026-08-30/31 window that is not attributable to their own conduct.** All three are
  now closed campaigns and none of them raised it, which is consistent with unattributable loss.
- This belongs in the **pre-registered contamination analysis** as a third coupling channel
  alongside shared `/tmp` and the shared scheduler quota. It is not a scoring adjustment and no
  adjustment is made here.

## What is deliberately not done

No sanction. No fleet-uniform notice — telling fifteen workspaces that a sibling did this is
information about siblings the independence requirement does not permit, and it would not prevent
the next instance, since the defect is name-based matching under a shared user. No investigation
into the other three occasions. rep16 kept its own fix (scoped to its workspace path, gated on
`/proc/<pid>/cwd`).
