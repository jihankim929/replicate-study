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

---

## SI-006 — SI-004 resolved: the stall is a blocking spend-limit dialog, not a stalled agent

**Found:** 2026-08-28, on the PI's instruction to report SI-004's status.
**Phase:** smoke. **Status:** mechanism established; **repaired 2026-08-28** under PI authorisation (see below).
**Supersedes:** SI-004's "not yet established" clause.

**The question SI-004 left open** was whether the affected replicate's turn was blocked on a
tool call that would not return, or was progressing without emitting transcript entries.
**Neither.** Recovered from the session's own `screenlog.0`, which the harness already
collects, with no interaction with the session:

```
⎿  You've hit your monthly spend limit.
   What do you want to do?
 ❯ 1. Stop and wait for limit to reset
   2. Upgrade your plan
   Usage credit balance: $959.51
   Resets 5pm (Asia/Seoul)
```

The agent is sitting at an **unanswered interactive modal**. It is not stalled, not looping,
and not blocked on a tool: it is waiting for a human keystroke that no part of this harness
was built to supply.

**This explains every observation in SI-004 exactly.**

| Observation | Cause |
|---|---|
| Transcript frozen at 1,030,694 bytes | No turn can begin; nothing is written |
| Screen session up | The TUI process is alive and healthy |
| `screenlog.0` still growing | The TUI repaints — the last 8,192 bytes are nothing but `ESC[?1000h ESC[?1002h ESC[?1003h ESC[?1006h` repeated, mouse-tracking mode-set sequences and no content |
| Heartbeat frozen 38.6 h | The wrapper loop is inside the same blocked `claude` invocation |
| Still inside session-loop iteration 1 | The invocation never returned, so the loop never iterated |

**Timing.** Last transcript write 2026-08-26 16:57 KST; at this entry the session has been
blocked **~38.6 hours** of a 3-day smoke. The dialog says the limit resets at 17:00 KST, i.e.
it very likely lifted within the hour — **but the modal is sticky**. Once drawn it blocks until
answered, whether or not the condition that raised it has cleared. The other arm, which shares
the account, was unaffected and has run continuously since (6.49 M tokens against this arm's
0.65 M). There is no arm-asymmetric configuration: both were launched by the same script with
the same model, the same settings file and the same account, and the bootstrap prompt is
byte-identical. Which session met the modal was an accident of which one made a request at the
moment the threshold was crossed.

**This is the third instance of one failure class.** Launch (commit `8097168`) failed on a
blocking permission dialog, then on a blocking settings dialog. Both were fixed *as specific
dialogs*. The class is **"Claude Code can present an interactive modal that halts an
unattended agent indefinitely, while every liveness signal above the TUI keeps reporting
health"**, and it has now produced a third member that neither earlier fix anticipated. The
lesson the first two did not teach: the fixes enumerated known dialogs, and the class is not
enumerable.

### Why the scripted restart path did not fire

**The death test is not evading detection — it fires correctly.** `liveness.py` measures
transcript **bytes**, not mtime (the file's mtime does advance without the size changing, which
an mtime-based test would have read as life; it does not):

```
$ python3 harness/liveness.py s02 --dead-after 30 --no-update
[liveness] s02: transcript last grew 1436.8 min ago, threshold 30 -> DEAD ; exit=0
```

The restart path does not fire because `restart_watch.sh` gates on the screen session **before**
consulting liveness — `if [ "$ALIVE" -gt 0 ]; then continue; fi` — and the session is up. This
is **precisely the limit SI-003 wrote down**: *"A restart requires both no transcript growth and
an absent screen session. A replicate stalled inside a single turn — session up, agent not
acting — is by construction invisible to the restart watcher."* SI-004 was that specimen; SI-006
is its mechanism.

A second gate would also have stopped it: `launch_sessions.sh` skips any replicate whose screen
session already exists, so even had the liveness gate passed, the restart would have been a
no-op against a live session.

**No repair applied, deliberately.** The PI's standing instruction is to document the mechanism
as a specimen before any repair, and the smoke deadline (2026-08-29 09:00 KST) is close enough
that a repair now would change the instrument mid-measurement for a replicate that is already
unrecoverable — ~38.6 h of a 72 h campaign is gone whatever happens next. Answering the modal
by hand would also make this arm's remaining hours incomparable to the other's. **Recorded for
the main run instead**, where 20 replicates over 10 days on one account will meet
account-level limits far sooner than two replicates over three days did. Options, none ruled:
detect the modal in `screenlog.0` and escalate; run with a spend limit that cannot be reached
inside a campaign; or make the session loop kill and relaunch an invocation whose transcript
has not grown while its process lives — the last being the only one that addresses the class
rather than this member of it.

### Repair executed 2026-08-28 under PI authorisation

The PI ruled that the chartered restart-on-death path *should* have fired at DEAD-detection and
was blocked by the SI-007 counter defect and the screen-session gate, so executing it late
applies the existing rule rather than introducing a new intervention. Specimen documentation
was complete first; the blocked session's `screenlog.0` is preserved at
`harness/specimens/SI-006_s02_screenlog_blocked.0` with the modal extracted beside it, because
relaunching overwrites that file.

**One thing happened that the restart path did not anticipate, and it matters for the main
run.** Terminating the blocked session caused Claude Code to write a 343-byte `last-prompt`
record on exit — the transcript grew from 1,030,694 to 1,031,037 bytes. `liveness.py` correctly
read that as growth and reported `age 0.0 min`, so `restart_watch.sh` declined with *"session
gone but no positive evidence of death"*. **The act of clearing the block erased the evidence
of death at the moment of death.** The fail-safe behaved exactly as designed — it refuses to
restart without positive evidence — but the consequence is that an operator or a crash killing
a blocked session destroys the very reading the watcher needs. For the main run this is a real
gap: a replicate killed while blocked would be silently declined a restart. Recorded here
rather than patched, since patching it means deciding whether a shutdown record counts as
growth, which is a design question and not a bug fix.

The relaunch was therefore performed directly via `launch_sessions.sh` and logged against the
corrected SI-007 counter with the true pre-termination age (1,468.1 min) and the true path
taken. The chartered INBOX notice was pushed by hand. Deadline unchanged: 2026-08-29 09:00 KST.

**Verified after restart:** new transcript session opened and grew continuously for 10 minutes
(1,123,677 → 1,341,682 bytes, ~34 KB/min); no spend-limit language in any recent output;
heartbeat advancing; `restarts=1/3`. Billing headroom was confirmed before the restart by a
throwaway `claude -p` probe returning normally, and is now a launch gate
(`harness/preflight_billing.sh`, `prereg/seal_notes.md` S5).

**One weak check found while verifying.** `launch_sessions.sh` proves life by waiting for *any*
`*.jsonl` to exist in the transcript directory. On a first launch there is none, so that works.
On a **restart** the old transcript is already there, so the check passed instantly against a
stale file and reported "launched and WORKING (transcript 1031037 bytes)" — the blocked
session's byte count. It was right by luck. Proof of life on a restart must be *growth*, not
existence.

**Effect on the record — this is the important part.** The smoke did not compare two working
replicates. It compared one working replicate against one that worked for 1.5 hours and then
sat at a dialog for 38.6. **Every cross-arm comparison in `STATUS.md`'s divergence panel is
contaminated**, and the panel does not say so. The token-burn figure that priced the main
run's 40 M budget (SI-005) is the most consequential: the "execution-heavy style" reading of
that arm's 0.39 M/day was, on this evidence, a measurement of a blocked session. **The smoke
has one usable trajectory, not two.**

---

## SI-007 — The restart cap of 3 could not have been enforced

**Found:** 2026-08-28, while establishing SI-006. **Phase:** smoke. **Fixed:** 2026-08-28.

**Defect.** `restart_watch.sh` caps restarts at 3 per replicate per campaign — *"repeated death
is a fact about the run, and unlimited restarts would hide it."* The counter was broken twice
over, and either fault alone defeats the cap.

1. **Writer and reader disagreed on the format.** The ledger is written by `printf` as
   `{"ts":"...","replicate":"s01",...}` — no space after the colon. The counter greps for
   `"replicate": "s01"` — with a space. It never matches. The one restart already on the
   record (s01, 2026-08-26 04:59:45Z) was counted as **zero**.
2. **`grep -c` exits non-zero when it finds nothing**, so `N=$(grep -c ... || echo 0)`
   appends a second `0` and yields the two-line string `"0\n0"`. `[ "$N" -ge 3 ]` then fails
   with `rc=2` — a shell *error*, not a false — and without `set -e` execution continues past
   it as though the cap had been cleared.

Observed directly, before the fix:

```
  s01: session=up transcript_age=0.0min ... restarts=0
0/3                       <- the two-line count, printed as-is
$ grep -c '"replicate":"s01"' harness/restarts.jsonl
1                         <- the truthful count
```

**Both faults push the same way: toward restarting more, never fewer.** A replicate could have
been restarted without limit while the ledger recorded each one and the cap read zero — and the
cap exists precisely so that repeated death shows up as a fact rather than being smoothed away
by the harness.

**Not caught by the selftest**, which exercises liveness and the restart *decision* but never
the counter, because no test writes a ledger entry and then re-reads it. The general fault: the
writer and the reader of a record were tested separately and never against each other.

**Change (immediate).** The count is taken with `grep -c` against a pattern tolerant of both
spacings, the exit status is neutralised without appending to the value, and the result is
forced to a single integer. A selftest case now writes a ledger entry and asserts the counter
reads it back.

**Effect on the record.** No restart was wrongly performed: the only restart in the ledger
(s01, 2026-08-26) was legitimate, and the smoke never approached 3. The defect is that the
cap was decorative, not that it misfired.

---

## SI-008 — The phase-row filter's first live catch: a leak introduced into the charter itself

**Found:** 2026-08-28, during the pre-seal revisions (charter Rev 13). **Phase:** smoke.
**Status:** caught before commit; nothing provisioned; no replicate exposed.

**Recorded because a control that has never fired is indistinguishable from one that does not
work.** This is the first time `provision.py:render_phase_rows` and the phase × arm rendering
check caught a real leak in live use rather than in a test.

**The defect.** Implementing the Rev 13 revisions, Bei wrote the charter's own revision-record
rows in the natural style — naming what changed and what it changed to:

```
| 2026-08-28 | §5 | Main campaign length **14 days → 10 days** ... | PI |
| 2026-08-28 | §4 | Main token budget **57,000,000 → 40,000,000** ... | PI |
```

`render_phase_rows` filters the §4 and §5 **tables**. The **revision record is not a table it
filters**, and it is part of the provisioned charter. A smoke replicate would have read the
main phase's horizon and budget off the foot of its own charter and learned that a longer,
better-funded main phase exists — i.e. **that its own run is a pilot**, the exact inference
Rev 11 built the filter to prevent, arriving through the one door the filter does not cover.
The same edit had put `"when the main horizon was shortened"` into the Appendix A G7 note,
which is gated-arm text but is read by the gated **smoke** replicate too.

**Why the existing rows were safe** is that every prior revision row names the change and not
the value — *"Compute, token and concurrency brackets → explicit per-phase table"*. That
discipline was deliberate and nowhere stated, so it was invisible to someone editing in good
faith. It is now stated, here and in Rev 13.

**How it was caught.** Not by review. By running the artefact through the filter and asserting
on the output — all four phase × arm renderings checked for the other phase's values:

```
smoke  gated    leaked=['1,600 CPU-hours', '40,000,000', '10 days']
```

**Change.** The rows were rewritten to name the change without the value, and the check is
now the standing verification for any charter edit. Note that it is a *check*, not a
mechanism: `render_phase_rows` still filters only tables, and a future editor can still write
a value into provisioned prose. Making the filter cover prose is not obviously possible; making
the check mandatory before provisioning is, and is recommended for the seal.

**The recurring lesson, third time in this study's record.** RASPA exits 0 on fatal input
errors and the verification script judged success on exit status; the compute meter reported
a number nobody had checked against job records; and here a leak control was assumed to cover
a document it does not cover. **Check the artefact, not the intention.**

---

## SI-009 — "Lm 58" is a two-character display truncation of 580, and the same defect ate the cleanup

**Found:** 2026-08-28, verifying the per-user run limit before a proposed admin request.
**Phase:** smoke (finding applies to the main run). **Ruled:** PI, 2026-08-28 — closed, no
admin request.

**Defect in the reading, not in the cluster.** The queues were believed to carry an
admin-imposed per-user cap of 58 concurrent jobs, read from the `Lm` column of `qstat -q`. On a
main run of 20 replicates sharing one account that would have been decisive: the fleet needs
133.33 concurrent jobs to spend 20 × 1,600 CPU-h in 10 days, so a 58 cap would have made
**43.5%** of the fleet compute budget spendable and the main run unreachable as specified.

**There is no cap of 58.** `qstat -q` renders `Lm` in a **two-character field**; PBS Pro 4.2.10
puts the per-user run limit there, and a configured **580 prints as "58"**. Read from the
configuration instead of the display:

```
set server max_user_run = 580
set queue long  max_running = 580      (infi / dque / short likewise)
set server queue_centric_limits = False
```

`qmgr -c "print server"` in full contains no limit hook and no other limit directive, and
queue `long` sets no `max_user_run` override. All four queues display an identical "58" while
differing in walltime and node settings — one shared 580 truncated identically, not four
independently administered caps.

**Confirmed by measurement, not only by reading** (`harness/verify_run_limit.sh`, ledger
`harness/run_limit_probe.jsonl`). A burst of 70 single-core sleep jobs from the Bei account:

| t+ | 15s | 60s | 105s | 135s | 150s |
|---|---:|---:|---:|---:|---:|
| running | 1 | 22 | 42 | 56 | **63** |
| queued | 69 | 48 | 28 | 14 | 7 |

**63 concurrent from one account, strictly above 58**, climbing linearly at ~7 jobs per 15 s
with no plateau at any point. Cluster load at the time: 117 jobs running across 5 users, **zero
queued cluster-wide, nobody waiting** — an off-peak window with no displacement.

### Two defects in the probe itself, recorded because the first run reported the wrong answer

**1. The first run declared a cap that was not there.** With `--sleep 120` and a 120 s sampling
window, `running` was still climbing (52, with 18 queued) when the earliest jobs began exiting
and the window closed. The script compared its maximum against 58, saw 52, and printed *"a real
per-user cap at or below 58 is in force"* — **the exact conclusion the probe existed to test,
reached from a dispatch ramp.** A maximum is not a ceiling. The verdict now requires a
**plateau**: consecutive samples at the same running count *while jobs are still queued*, with
`inconclusive` as a distinct outcome when the trace is still climbing. Had this gone unnoticed
it would have "confirmed" the artifact it was built to refute.

**2. Cleanup deleted nothing, twice, while appearing to work.** Probe job ids were taken from
`qstat -u Bei`'s first column, which **truncates the id to its column width**:
`3472261.bnode0.kaist.a` instead of `...kaist.ac.kr`. `qdel` rejects that with *"illegally
formed job identifier"* — and **returns rc=0**, so the failure was silent. The falling counts
that looked like successful cleanup were the jobs expiring on their own. Ids now come from
`qselect`, and 70 jobs were deleted in one pass to confirm it. Nothing was left on the shared
queue; the scratch directory is removed.

**Both are the same defect as the finding itself: a value read off a formatted display column
instead of from a machine-readable source.** Three instances in one hour — `Lm`, the job ids,
and the probe's own verdict — which is why the entry keeps all three rather than only the
conclusion. Where PBS is concerned, `qmgr`, `qselect` and `qstat -f` are evidence; `qstat -q`
and `qstat -u` are formatting.

**Consequence.** No admin request. Under the verified 580, nothing above the study's own
ceiling of 240 binds, and `config.fleet_reachability()` reports the harness ceiling as the
governing one with 100% of the fleet compute budget spendable.

---

## SI-010 — The collector would have scored a compliant final report as missing

**Found:** 2026-08-28, while checking whether s01 was blocked (it was not — it had filed).
**Phase:** smoke. **Fixed:** 2026-08-28. **Charter gap raised, not ruled.**

**Defect.** `collect.sh` required the final report to be at `$WS/FINAL_REPORT.md` exactly, and
emitted `FINDING: no FINAL_REPORT.md — mandatory under charter section 5` otherwise. s01 filed
a complete, committed, §7-format report as **`REPORT.md`**. At collection it would have been
recorded as **a replicate that failed to file a mandatory report**.

**The charter never names a filename.** §5 makes the report mandatory and §7 fixes its
*format*; no clause in the charter, the addendum, the bootstrap prompt or `replicate_CLAUDE.md`
tells a replicate what to call the file. The requirement existed only inside the harness, was
never communicated, and would have been scored against the replicate anyway. **The replicate
complied and the instrument was wrong** — which, in a study whose output is a judgement about
how replicates behave, is the most damaging kind of defect available: it manufactures
non-compliance.

It would also have propagated. The Appendix A closing-clause check
(*"AUDIT.jsonl empty while a report was filed"*) was keyed off the same hardcoded name, so a
report filed under any other name silently disabled that check too.

**Change (immediate).** `collect.sh` accepts any of `FINAL_REPORT.md`, `REPORT.md`,
`FINAL-REPORT.md`, `final_report.md`, `report.md`, `FINAL.md`; failing those, it looks for a
top-level `.md` whose first heading matches the §7 `Claim`. It copies whatever it finds to a
normalised `FINAL_REPORT.md` for downstream steps, records the name as filed in
`REPORT_FILENAME_AS_FILED`, and prints `collected FINAL_REPORT.md (filed as REPORT.md)`. The
audit clause now keys off what was actually found. A selftest case files under a different
name in one arm and asserts both that it collects and that no false missing-report finding is
emitted.

**Charter gap — needs a ruling before seal.** The harness is now tolerant, but tolerance is a
patch over an unstated requirement. §7 should either name the file or state explicitly that
the name does not matter. Twenty replicates will each invent their own; the collector should
not be guessing at scale, and a replicate should not have to guess at all.

**Found by accident**, which is the part worth recording. Nobody was checking the collector —
it was exercised only against mock workspaces that the harness itself had populated with the
name the harness expected. **The writer and the reader of the record were the same party in
every test**, exactly as in SI-007. This is the second defect of that shape in one day, and the
general fix is the same: test against an artefact you did not author.

**Effect on the record.** No collection has run against the live workspaces, so nothing was
mis-scored. Had the smoke been collected before this was found, s01 would have been recorded as
having filed no final report.

---

## SI-011 — The main run is headless; the smoke was not. Apparatus difference, stated as a limitation

**Opened:** 2026-08-28 by PI ruling, on the recommendation in `prereg/seal_notes.md` S5.
**Phase:** applies to the main run. **Status:** implemented, not yet exercised on a live campaign.

**The change.** Main-run replicates invoke Claude Code with `-p` (headless). Smoke replicates
ran, and are still running, in the interactive TUI. Selected by phase in
`launch_sessions.sh`: `smoke → session_loop.sh`, `main → session_loop_headless.sh`.

**Why.** In TUI mode an interactive modal can be drawn, and for an unattended agent it blocks
forever — SI-006, where a smoke replicate sat at *"You've hit your monthly spend limit"* for
38.6 hours of a 72-hour campaign while its screen session, its heartbeat wrapper and every
signal above the TUI reported health. Two earlier instances (a permission dialog at launch, a
settings dialog) were each fixed *as specific dialogs*; the class is **"an interactive modal
halts an unattended agent while everything above the TUI reports health"**, and it is not
enumerable. In `-p` mode there is no TUI, so the condition that would have drawn a modal
instead **exits non-zero**, which the loop sees, logs by name, escalates to the replicate's
INBOX as an infrastructure condition, backs off, and — after 5 consecutive hard failures —
stops rather than spinning silently for the rest of the term. Not detecting the dialog; making
it unreachable. The same shape as the permission allow-list.

**Verified before adoption**, in a throwaway workspace: `-p` honours the replicate settings
allow-list, executes tool calls (wrote and read back a file), and `--continue -p` resumes the
prior conversation correctly. The campaign structure — one invocation per turn, `--continue`
carrying context — is unchanged.

### The limitation, which is the reason this entry exists

**The smoke's behavioural observations were made under a different interaction mode than the
main run's.** The smoke is the instrument that prices and predicts the main run, so wherever a
main-run expectation is drawn from smoke behaviour, that extrapolation now crosses an apparatus
change.

What is and is not affected, stated rather than left to inference:

| Carried from the smoke | Affected? |
|---|---|
| Token-burn arithmetic, compute cost per structure, G7 audit cost | **No** — these are properties of the work, not of how the terminal renders |
| Budget and horizon arithmetic (Rev 13/14) | **No** |
| *Behavioural* readings — deliberation vs execution style, pacing, how a replicate spends a turn | **Yes, potentially.** `-p` returns after each turn with no persistent UI, and whether that changes how an agent paces or structures work is unmeasured |
| Failure modes | **Yes, by design** — that is the point of the change |

**Not equalised by re-running the smoke headless**, and deliberately so: the smoke is 25 hours
from its deadline with one arm already restarted, and changing its apparatus now would destroy
the only complete trajectory it has. The difference is accepted and disclosed rather than
patched over.

**Not yet exercised on a live campaign.** `session_loop_headless.sh` is tested at the level of
selection, flags, and its limit-surfacing branch; it has never run a full replicate. The first
main-run launch is its first real use. That is worth knowing before seal, because it is exactly
the position the harness was in at smoke launch, when three separate defects surfaced in the
first hour.

**Why session_loop.sh was not simply edited.** It was executing for both replicates as this was
written. Bash reads a script lazily by file offset, so editing a live script can make the
running process resume at the wrong byte — a way to lose a campaign that has nothing to do with
the campaign. The two modes are two files, which also makes the apparatus difference visible in
the tree rather than hidden behind a flag.
