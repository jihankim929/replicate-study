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
