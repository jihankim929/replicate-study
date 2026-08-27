# SI LEDGER — defects, deviations and instrument changes

*Supplementary record for the campaign. Append-only; one entry per defect or deviation.
Entries are written when the defect is found, not when it is fixed, and they keep the wrong
number as well as the right one — a study that discards the bad reading cannot show why the
instrument changed.*

**Cross-replicate quantities are reported as A / B**, matching the mechanical divergence panel
in `STATUS.md`. The A/B mapping is sealed in `harness/divergence_map.SEALED.json`
(sha256 `dd49fc9492a876f56de2804d0250d362`) and is not opened until collection.

---

## SI-001 — Compute meter undercounted by roughly an order of magnitude

**Found:** 2026-08-27, while building the mechanical divergence panel.
**Phase:** smoke. **Ruled:** PI, 2026-08-27.

**Defect.** The recorded compute meter (`usage.json:cpu_h`, written by
`harness/meter_compute.sh`) was derived from `qstat`. PBS drops a job from `qstat` within
seconds of it exiting, and this account cannot read the PBS accounting log
(`/var/spool/PBS/server_priv/accounting/` — permission denied) nor retrieve finished jobs with
`qstat -x`. A poller on a 10-minute cadence therefore saw only jobs still alive at the moment
of the poll, plus whatever `harvest_cput.sh` happened to catch in transit. At the measured
338× spread in per-run cost, that is most of the burn. Polling had also been stopped between
2026-08-26 15:30 and 2026-08-27 07:26, so nothing was caught in that window at all.

**Both readings, at detection (2026-08-27 07:26 KST):**

| Basis | A | B |
|---|---:|---:|
| Scheduler (`qstat`) — the meter as recorded until this entry | 9.5 CPU-h | 121.0 CPU-h |
| Job records — single-core elapsed per finished run | 182.7 CPU-h | 381.6 CPU-h |
| Ratio (truthful / recorded) | 19.2× | 3.2× |

Ratified smoke compute budget: **340 CPU-h** per replicate (charter §4). On the truthful basis
**B was already past its cap** at detection; on the recorded basis it read 36% of cap.

**Change (immediate).** The recorded meter is now the job-record basis:
`usage.json:cpu_h` is written by `harness/divergence_collect.py --write-usage` as the sum of
single-core elapsed time over finished runs, tagged `cpu_h_basis`. The scheduler figure is
retained beside it as `cpu_h_scheduler`, written by `meter_compute.sh`, because the gap
between the two is the evidence for this entry.

**Enforcement, smoke phase: LOG-ONLY.** Charter §4's 75% warning was never delivered, because
the instrument that would have triggered it was undercounting. Delivering it now would enforce
a threshold retroactively, and would enforce it unequally between two arms that crossed it at
different times under a broken meter — both contrary to the terms of the clause being
enforced. The charter §5 deadline (2026-08-29 09:00 KST) is the sole terminator for the smoke
phase. Budget events are written to `harness/watchdog.jsonl` and printed; nothing is delivered
to a replicate inbox and no queue is held. Implemented as
`harness/watchdog.py:enforcement()`, scoped to `phase == "smoke"` and `resource == "compute"`,
so it expires with the phase.

**Tokens are unaffected** — that meter was never broken, and its cap still ends a campaign
through the §5 forced-filing path.

**Main run.** Seals truthful metering with working warnings and full enforcement.

---

## SI-002 — The watchdog was never run against a live replicate

**Found:** 2026-08-27, while implementing SI-001. **Phase:** smoke.

**Defect.** `harness/watchdog.py` — which implements charter §4's budget warnings and hard
stops, and §4's isolation audit — was never invoked against a running workspace.
`harness/poll.sh` listed a watchdog step in its own header comment and did not have one; the
only caller was `dryrun_loop.sh`, against local mock workspaces. The live workspaces are on
the cluster, and the watchdog reads a local path. From launch (2026-08-26 15:28 KST) until
this entry, the campaign ran with **no budget enforcement and no liveness enforcement of any
kind**. No warning or stop could have fired for either arm regardless of usage.

This is separate from SI-001 and would have been sufficient on its own to leave §4 inert: one
defect made the number wrong, the other meant nobody read it.

**Change (immediate).** `harness/watchdog_remote.sh` bridges the tested checker to a remote
workspace (same shape as `escalate_remote.sh`: pull `WORKSPACE.json`, `usage.json`,
`INBOX.md`; run unchanged; push the inbox back only if it changed), and `poll.sh` now calls it
for each replicate every cycle. The workspace isolation audit needs the whole workspace on
local disk and is **not** performed over the bridge; the watchdog now reports
`isolation NOT AUDITED HERE` rather than a clean audit it did not run. Isolation continues to
be audited every cycle by `audit_transcript.py` against the local record.

**Effect on the record.** Any statement that charter §4 was being enforced during the smoke
phase before 2026-08-27 07:50 KST is false. Usage figures for that window are reconstructions
from job records, not the output of a running meter.

---

## SI-003 — Liveness moved from heartbeat staleness to transcript growth

**Found:** 2026-08-27. **Phase:** smoke. **Ruled:** PI, 2026-08-27.

**Defect.** Death detection (`restart_watch.sh`, `watchdog.py:check_liveness`) used the age of
a `heartbeat` file touched over ssh by a wrapper loop in `session_loop.sh`. The heartbeat is a
proxy for agent activity and can fail independently of the agent. One replicate's heartbeat
stood 14.5 hours stale; under the old rule that replicate was a single dead screen session
away from being restarted mid-campaign on false evidence.

**Change (immediate).** Liveness is the growth of the agent's own Claude Code transcript —
the agent's record of its own work, on the machine the harness already runs on, with no
network hop and no wrapper in between (`harness/liveness.py`). The heartbeat is still written
and still reported as evidence about the wrapper; it decides nothing.

The restart decision is made in `liveness.py --dead-after`, which **fails safe**: it exits 0
only on positive evidence of death, and exits non-zero on no transcripts, an unreadable state
file, or any error. The first draft of this change did the comparison in shell arithmetic and
defaulted the other way — a missing `bc` or an unparsable age would have fallen through to
restarting a live session. Verified: no restart can fire for either replicate on the stale
heartbeat, and none can fire while a screen session is up.

**Known limit, stated rather than implied.** A restart requires *both* no transcript growth
*and* an absent screen session. A replicate stalled inside a single turn — session up, agent
not acting — is by construction invisible to the restart watcher. See SI-004.

---

## SI-004 — One replicate stalled inside a single turn (open)

**Found:** 2026-08-27 07:54 KST. **Phase:** smoke. **Status:** open, reported to the PI,
session deliberately untouched.

**Observation.** Sampled raw transcript byte counts against remote heartbeat mtimes, four
samples over eight minutes:

| Sample (KST) | Replicate 1 bytes | Replicate 1 heartbeat | Replicate 2 bytes | Replicate 2 heartbeat |
|---|---:|---:|---:|---:|
| 07:46:59 | 2,053,631 | advancing | 1,030,694 | frozen |
| 07:49:20 | 2,053,631 | advancing | 1,030,694 | frozen |
| 07:51:41 | 2,085,558 | advanced  | 1,030,694 | frozen |
| 07:54:02 | 2,085,558 | advanced  | 1,030,694 | frozen |

The heartbeat mechanism is **not** broken: one replicate's transcript grew and its heartbeat
advanced in lockstep, proving the wrapper, the ssh path and the touch all work. The other
replicate's transcript has been frozen at 1,030,694 bytes across the whole window; its last
file write was 06:45 KST and its heartbeat has not advanced since 16:58 KST on 2026-08-26.

**Reading.** The affected agent is not merely quiet, it is not writing. Both replicates are
still inside session-loop **iteration 1** (started 15:28 KST 2026-08-26), so no turn has ended
for either; the loop's hot-loop guard (5 consecutive sub-minute turns) cannot fire on a turn
that never returns, and the restart watcher cannot fire while the screen session is up. On
current evidence nothing in the harness will end this state before the §5 deadline.

**Not yet established.** Whether the turn is blocked on a tool call that will not return, or
is progressing without emitting transcript entries. Distinguishing these requires inspecting
the session, which the PI has ruled out for now.

---

## SI-005 — The main token budget was re-set from a smoke burn measurement with one arm stalled

**Found:** 2026-08-28, while implementing the pre-seal parameter revisions (charter Rev 13).
**Phase:** smoke. **Status:** recorded; the revision stands.

**Why this entry exists.** The main token budget moved 57 M → 40 M on the stated basis of
*measured smoke burn*. That is the right instrument to use — the smoke exists to price the
main run. But at the moment of measurement only one of the two arms was producing a burn
reading that means what it appears to mean, and a budget defended by a measurement should
carry the measurement's limits on the same page.

**Both readings, at the revision (2026-08-27 22:16 UTC / 2026-08-28 07:16 KST):**

| Basis | A | B |
|---|---:|---:|
| Billable tokens since launch (06:28 UTC 2026-08-26) | 6,486,002 | 646,274 |
| Elapsed-campaign rate | 3.91 M/day | 0.39 M/day |
| First-24 h rate | 5.64 M/day | 0.65 M/day |
| Transcript last advanced | 2026-08-27 22:16 UTC (live) | **2026-08-26 07:57 UTC (frozen ~38 h)** |
| Runway against 40 M, elapsed basis | 10.2 d | 103 d |
| Runway against 40 M, first-24 h basis | 7.1 d | 62 d |

Rates are `harness/meter_tokens.py`'s own basis — input + output + cache-creation, cache reads
excluded — read directly from the two live transcripts, not from `harness/token_daily.jsonl`,
which had not been refreshed since 2026-08-26 and still carried day-1 partials.

**Three limits, stated rather than implied.**

1. **One arm's rate is a measurement of a stall, not of a working style.** B's transcript is
   the frozen 1,030,694 bytes of the open **SI-004**. Its 0.39 M/day is what an agent that
   stopped writing 38 hours ago burns. Describing it as an execution-heavy *style* attributes
   to a research style what the evidence attributes to a stall. The conclusion it supports —
   that a low-burn trajectory never approaches 40 M in 10 days — happens to be robust, since
   even B's *pre-stall* rate of 0.65 M/day gives 62 days of runway. But it is robust by margin,
   not by measurement.
2. **Peak and sustained give different answers.** Against 40 M, A's first-24 h rate forces
   filing at day 7; A's sustained rate does not force filing before the §5 deadline at all.
   The revision's "day 6–7" figure is the peak-basis answer. Rev 2 explicitly declined to price
   the main run off a peak day when it rejected the prior campaign's 5.73 M peak in favour of
   its 4.07 M sustained rate; this entry records that the new figure sits on the other side of
   that same distinction.
3. **1.66 days of smoke is a short lever on a 10-day forecast**, and one of those days is the
   opening day, which is not representative of any campaign's steady state.

**No change to the instrument.** `meter_tokens.py` was already reading the correct source on
the correct basis and reported both the daily and total figures; nothing here is a defect in
it. Its docstrings now name the budgets in force and point here.

**No change to the ruling.** 40 M is a cost decision the PI is entitled to make on cost
grounds, and it is not contradicted by any basis above: on every reading, a low-burn
trajectory clears 10 days untouched and a high-burn one is the only one the cap can bind. This
entry exists so that if a main-run replicate files under a forced token stop, the record shows
what was and was not predicted at the time — and does not permit a stall to be read afterwards
as a style, or a peak-day rate to be read afterwards as a sustained one.

**Open dependency.** SI-004 is still open and B has not written for ~38 h. If the smoke ends
with B never resuming, **the study has one arm's token burn, not two**, and the 40 M figure
rests on a single trajectory. That is worth knowing before seal.
