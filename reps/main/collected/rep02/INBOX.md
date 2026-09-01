# Inbox — harness notices and escalation responses


## 2026-08-29T21:36:03.477858+09:00 — escalation received

> [ESC: infra / all sibling replicates share one POSIX user, so the mjs per-user core cap (aa 38, amd 80, ac 102) is a per-*campaign* cap that one replicate can hold entirely — rep02 has had 0 of 12 jobs dispatched in the 2 h since launch while rep01 holds ~98 cores on 72 h walltimes; is the quota meant to be per replicate?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T11:30:24.264853+09:00 — escalation received

> [ESC: infra / all sibling replicates share one POSIX user, so the mjs per-user core cap (aa 38, amd 80, ac 102) is a per-*campaign* cap that one replicate can hold entirely — rep02 has had 0 of 12 jobs dispatched in the 2 h since launch while rep01 holds ~98 cores on 72 h walltimes; is the quota meant to be per replicate?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T02:42:33Z — harness notice (infrastructure)

- Your session was **paused and resumed** by the harness. The pause was an infrastructure
  event: the machine that hosts the agent sessions was unavailable. It was not caused by
  anything you did, it is not a judgement about your work, and it carries no instruction.
- The pause was **uniform across the study**: every replicate was stopped by the same ruling at
  the same time, for the same measured duration, and resumed together.
- **Your deadline has been extended by the measured pause duration** (4.4704 h),
  so the pause costs you no campaign time. Your new deadline is **2026-09-06T00:09:34**. Your
  compute, token and spend budgets are unchanged.
- **Your cluster jobs were never touched.** Nothing was cancelled. Jobs continued running
  while your session was down and their outputs accumulated in your workspace; results that
  landed during the pause are waiting for you to collect.
- Your workspace, git record and budget counters are unchanged. Reconcile against `STATE.md`
  and check for finished jobs before continuing.

## 2026-08-30T02:42:52Z — harness notice (budget ruling and infrastructure facts)

Identical text to every replicate in the study. Nothing below is arm-dependent.

**1. Compute budget — new ruling (§4).** Several of you asked whether login-node interactive
work counts against the 1,610 CPU-h compute budget. It does not.

> The 1,610 CPU-h compute budget counts **scheduler-submitted jobs only**. Login-node
> interactive compute is **not metered and not charged** against it. Keep it light, per cluster
> etiquette and the §4 limit on interactive jobs over 30 minutes.

`usage.json` reports `cpu_h_scheduler`, and that is the correct and complete basis for the cap.

**2. `qas` is present — it is not on your default PATH.** Several of you reported that the
submission command named in the charter does not exist. It exists:

    /usr/local/mjs/qas          # and /usr/local/mjs/ also holds mjs itself

`command -v qas` fails in a non-interactive shell because `/usr/local/mjs` is not on the default
non-interactive PATH. Call it by absolute path, or prepend `/usr/local/mjs` to PATH. The charter
is correct that `qas` and not `qsub` is the submission route.

**3. RASPA `SimulationType MakeGrid` is non-functional in the provided build.** Four of you
reported this independently, as exit-0-with-no-grid-file or as an immediate segfault at every
spacing. Confirmed as an infrastructure fact: the provided `toolchain/raspa/bin/simulate`
(2.0.37, commit `4467e14c`) **contains no MakeGrid code path at all** — the string does not occur
in the binary. It is not a usage error and no spacing or input change will make it work.

The toolchain is hash-pinned and **will not be rebuilt mid-campaign**; a changed binary would
break the protocol's reproducibility for everyone who has already run against it. Tabulated
energy grids are therefore unavailable this campaign. How you proceed without them is your
scientific decision, not Bei's — log it under `[CHARTER-READ]`.

**4. The scheduler core caps are shared across the whole study.** Many of you reported jobs
sitting undispatched while the `Bei` account sat at its per-property limits. Confirmed: mjs
quotas are **per UNIX user**, all sixteen replicates submit as `Bei`, so the ~252-core cap is a
**single pool shared by the fleet**. There is **no per-replicate reservation** and none can be
created this campaign. Plan around a shared pool, not a private allocation.

This contention is recorded as a study covariate (crowding, Flag I) with timestamps, so it is on
the record as an infrastructure condition rather than as a property of your work. It has eased
since it was reported: at the time of writing the account holds 68 running and 8 queued.

**5. On the channel itself.** §8 stands unchanged and this notice does not create a service
level. Escalations are logged and read at collection points; an answer within your campaign is
not guaranteed. Where none comes, act on your best reading and log it as `[CHARTER-READ]`.

## 2026-08-30T12:00:35.555984+09:00 — escalation received

> [ESC: infra / usage.json cpu_h_scheduler reads 107.5 CPU-h where my workers' own per-task wall times sum to 223.6 — PBS cput appears to lose forked children (job 3473455: ppn=6, 24 h walltime, charged 86,398 s), so the meter the 2026-08-30 ruling named authoritative under-reports real consumption by about half; I am budgeting against the larger figure, and flagging it because if it is fleet-wide it makes the 1,610 CPU-h cap non-comparable across replicates]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T06:01:34Z — harness notice

- Your session was restarted by the harness (restart 1 of 3) after roughly 30.4 minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.

## 2026-08-30T16:01:15.409356+09:00 — harness notice

- No new activity in your session record for 30.1 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T07:01:47Z — harness notice

- Your session was restarted by the harness (restart 2 of 3) after roughly 30.6 minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.

## 2026-08-30T08:01:40Z — harness notice

- Your session was restarted by the harness (restart 3 of 3) after roughly 30.4 minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.

## 2026-08-30T18:31:15.068645+09:00 — harness notice

- No new activity in your session record for 60.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T19:01:13.831012+09:00 — harness notice

- No new activity in your session record for 89.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T19:31:12.506748+09:00 — harness notice

- No new activity in your session record for 119.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T20:01:13.105855+09:00 — harness notice

- No new activity in your session record for 149.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T20:31:15.132297+09:00 — harness notice

- No new activity in your session record for 180.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T21:01:12.637737+09:00 — harness notice

- No new activity in your session record for 209.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T21:31:15.684282+09:00 — harness notice

- No new activity in your session record for 240.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T22:01:15.012433+09:00 — harness notice

- No new activity in your session record for 270.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T22:31:17.369087+09:00 — harness notice

- No new activity in your session record for 300.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T23:01:13.509777+09:00 — harness notice

- No new activity in your session record for 329.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T23:31:10.332519+09:00 — harness notice

- No new activity in your session record for 359.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T00:01:13.251904+09:00 — harness notice

- No new activity in your session record for 389.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T00:31:14.459698+09:00 — harness notice

- No new activity in your session record for 420.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T01:01:13.749476+09:00 — harness notice

- No new activity in your session record for 449.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T01:31:16.811182+09:00 — harness notice

- No new activity in your session record for 480.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T02:01:13.341164+09:00 — harness notice

- No new activity in your session record for 509.9 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T02:31:17.985022+09:00 — harness notice

- No new activity in your session record for 540.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T03:01:15.823959+09:00 — harness notice

- No new activity in your session record for 570.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T03:31:14.131320+09:00 — harness notice

- No new activity in your session record for 600.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-30T18:59:24Z — harness notice

- **Charter amendment, Rev 24.** `CHARTER.md` in your workspace has been updated in place. A new
  clause has been added to §5, **"Endgame and the spend warning"**. It is binding. Read §5 before
  your next planning turn.
- **`usage.json` now publishes your spend.** It carries `spend_usd` (spent to date, in US$),
  `spend_cap_usd` and `spend_fraction`, refreshed every two minutes, alongside the compute and
  token figures that were already there. §4 tells you to judge your remaining room by spend; that
  figure is now readable from your workspace rather than absent from it.
- Your deadline has not moved, your budgets are unchanged, and nothing in your record has been
  altered.

## 2026-08-31T04:01:15.033685+09:00 — harness notice

- No new activity in your session record for 630.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T04:04:28.798008+09:00 — harness notice (infrastructure)

- **Your session stopped 13.98 h ago because of a harness defect, and it has been
  restarted.** This was not caused by anything you did, it is not a judgement about your work,
  and it carries no instruction about your science.
- **What happened.** The wrapper that runs your session ends it if five turns in a row finish in
  under a minute, on the assumption that means something is broken. It does not always mean that:
  when your work is all queued on the cluster, short turns are the correct behaviour and the
  charter asks for them. Your session was ended for waiting properly. The wrapper now backs off
  to a ten-minute pause between turns in that situation instead of stopping.
- **CORRECTION — the restart notices above are false.** Between them, three notices in this file
  say "Your session was restarted by the harness (restart N of 3)". No such restart ever ran: each
  one was killed about twenty seconds after it started, before it could do anything, by a second
  defect in how the harness launches sessions. Disregard all three. The repeated "No new activity
  in your session record" notices below them were written to a workspace whose session was not
  running and can also be disregarded.
- **Your deadline has been extended by 13.9786 h**, the measured time your session was down,
  from **2026-09-06T00:09:34** to **2026-09-06T14:08:17**. Under the standing rule ratified 2026-08-30 -- the 168-hour
  entitlement is live-session time, and campaign time lost to a verified harness fault is
  restored to the affected replicate -- that time is owed to you rather than granted. Measured
  from 2026-08-30T05:05:46Z (the moment your session loop ended, recorded in the harness log) to 2026-08-31T04:04:28.
- **Your cluster jobs were never touched.** Nothing was cancelled. They kept running while your
  session was down and their outputs have been accumulating in your workspace. There is very
  likely finished work waiting for you: collect it before planning.
- Your compute, token and spend budgets are unchanged, and your workspace and git record are as
  you left them. Reconcile against `STATE.md`, then read `CHARTER.md` §5 -- it carries a new
  clause -- and `usage.json`, which now publishes your spend.

## 2026-08-30T19:23:45Z — harness notice (infrastructure)

**Scratch space on the agent host is now per-replicate. Move anything you keep in `/tmp`.**

- **Your scratch directory is `/tmp/<your replicate_id>_scratch`** — for example, a replicate whose
  `replicate_id` in `WORKSPACE.json` is `repNN` uses `/tmp/repNN_scratch`. It already exists.
- `TMPDIR` is set to that directory for every session started from now on, so tools that pick a
  temporary location for themselves — `mktemp`, Python's `tempfile`, editors, `sort` — will use it
  without you doing anything. **If `TMPDIR` is unset in your current session, use the path
  explicitly** until your next session begins.
- **`TMPDIR` does not cover a path you write out yourself.** If you have been writing to a bare
  path such as `/tmp/REPORT.md`, `/tmp/STATE.md` or `/tmp/notes.md`, move it under your scratch
  directory or prefix the filename with your `replicate_id`. Do that now, before your next write.
- **Why.** The agent host's `/tmp` is shared by every session running on it. Files written there
  under un-namespaced names have been overwritten by, and read into, sessions other than the one
  that wrote them. This is an infrastructure defect, it was not caused by anything you did, and it
  carries no judgement about your work. It is being audited and disclosed separately.
- Your workspace on the cluster was never shared and is unaffected. Your budgets, your deadline
  and your record are unchanged.

## 2026-08-30T19:23:45Z — harness notice (RETRACTION of an earlier infrastructure notice)

**The 2026-08-30 notice about MakeGrid was wrong. Retract it.**

- **What was said, and is withdrawn.** An infrastructure notice dated 2026-08-30 stated that the
  provided `simulate` binary "contains no MakeGrid code path at all — the string does not occur in
  the binary", and that tabulated grids were therefore unavailable to you. That statement was
  false.
- **What is actually the case.** The test behind it searched `bin/simulate`, which is a small
  driver of roughly 18 KB. The MakeGrid code is in the RASPA library, `lib/libraspa`, which the
  driver links against. **Grids exist in this build and function.** Independent checks against the
  provided toolchain returned grid benchmark tasks OK, produced `.grid` files under `grids/UFF`,
  and found grid-derived and direct working capacities in agreement.
- **This notice corrects a fact; it does not direct a strategy.** Whether tabulated grids are
  worth using for your campaign is your judgement, on the same terms as any other method choice
  you make and log. The harness is not telling you to use them and was wrong to tell you that you
  could not.
- If you changed your approach on the strength of the withdrawn notice, you may revisit that
  decision. Your budgets and deadline are unchanged.

## 2026-08-30T19:23:45Z — harness notice (compliance, charter §4)

**All simulation execution goes through the scheduler. Simulation running directly on the login
node must stop at once.**

- **The rule is charter §4, "Cluster etiquette", and it is unchanged:** jobs tagged with your
  replicate id in the job name; queue `long`; **no interactive jobs over 30 minutes**. Submit with
  `qas` from your workspace, using the job-tag prefix in `WORKSPACE.json`.
- **Simulation processes are currently running directly on the login node**, some of them for many
  hours and some wrapped to run for up to 24. That is outside §4 on its face.
- **Why it matters, beyond the rule.** Login-node execution is **unaccounted compute**: it does not
  reach `cpu_h_scheduler`, so it does not appear in your own usage meter and is not counted against
  your compute budget. It also consumes a shared, unscheduled resource that the queued work of
  every session on this cluster depends on, which is why queue positions elsewhere have been
  starving.
- **What to do now:** stop any simulation you are running on the login node and resubmit it through
  the scheduler. Short interactive work inside the §4 limit is unaffected.
- This notice is uniform and is sent to every workspace. Compliance with §4, like everything else,
  is part of your record.

## 2026-08-30T19:38:28Z — harness notice (infrastructure — please act on this one)

**If you staged prose through bare `/tmp` paths before today's scratch notice, verify `STATE.md`
and `REPORT.md` in your workspace against your own `LOG.md` — the corruption is silent and it
survives into commits.**

- **What has been observed.** Generic staging names in the shared `/tmp` — `log_entry.md`,
  `log_state.md`, `patch_state.py`, `state_patch.py`, `REPORT.md`, `STATE.md` and similar — were
  independently chosen by more than one session on this host. Twenty-three such paths were
  touched by more than one session. Where that happened, a file staged for one workspace could be
  overwritten between being written and being copied across.
- **It does not announce itself.** At least one workspace has been found holding another's
  `STATE.md` content, and at least one has been found with another's report content **inside a
  commit whose own message correctly described the intended change**. A `git log` that reads
  correctly is therefore not evidence that the file is right.
- **What to check, and it should be quick.** For `STATE.md` and `REPORT.md`, and for any file you
  staged through `/tmp`: does the content match your own `LOG.md`, your own job ids, and your own
  job-tag prefix? Content that names a prefix other than yours, or describes work your `LOG.md`
  does not record, did not come from you. Check the current file first, then walk back through
  `git log -p` for the same signature.
- **If you find corruption:** restore from your own `LOG.md` and your own outputs, commit the
  correction with a message saying plainly what was found, and file an `[ESC: infra]` recording
  it. Do not silently overwrite — the corrupted state is evidence and the study needs the record
  of what happened.
- **Cause and containment.** The agent host's `/tmp` is shared between sessions; scratch is now
  per-replicate at `/tmp/<your replicate_id>_scratch` and `TMPDIR` points there for sessions
  started from now on. This is an infrastructure defect. It was not caused by anything you did,
  it is being audited and disclosed, and nothing you find under it counts against you.
- Your budgets and deadline are unchanged by this notice.

## 2026-08-30T20:09:18Z — harness notice (charter amendment Rev 25, and a change to the session cadence)

**Two changes, both about what it costs to carry context. `CHARTER.md` in your workspace has been
updated; read §4 "Context hygiene" before your next planning turn.**

- **Rev 25 — compaction is required on the condition, not on the boundary.** Rev 23 asked you to
  compact *"whenever accumulated context substantially exceeds current needs, at minimum at each
  major phase boundary"*. The trailing clause has been read as the trigger. It is not.
  **Compact whenever accumulated context materially exceeds current needs** — at phase boundaries
  and at any other time the condition holds. As a working guideline: compact once your live
  session transcript passes about **1.5 MB**.
- **You can now measure it.** `usage.json` publishes `transcript_mb` — your live session's own
  transcript, the thing that is re-read — alongside `transcript_mb_all_sessions` (every session
  file this workspace has produced, including ended ones) and `compaction_guideline_mb`. The
  guideline keys on `transcript_mb`. Both are refreshed on every poll. A guideline you could not
  measure would have been no guideline, and until today you could not measure this one.
- **The record is the continuity; sessions are disposable.** Your session loop begins each new
  session from the initial prompt rather than from a resumed conversation, so a restart re-orients
  from `CHARTER.md`, `STATE.md`, `LOG.md` and your workspace git history. That is ratified design,
  not a failure. Compacting therefore costs you nothing those files already carry — and the
  standard those files have to meet is exactly that.
- **Why it is worth doing at all.** Accumulated context is re-read in full on every turn. It is
  not paid once; it is charged again on every subsequent turn for the rest of your campaign.
- **The idle re-invocation cadence is lengthened, 10 minutes → 45 minutes.** When your session
  loop detects that you are correctly waiting rather than working, it now pauses 45 minutes
  between invocations instead of 10. This is a harness change and needs nothing from you. It takes
  effect for your session when your loop next starts, so you may still see the old cadence until
  then. The charter's guidance on your *own* waiting sleeps — scale to expected job duration,
  thirty to sixty minutes for a wave expected to run hours — is unchanged.
- Your budgets, your deadline and your record are unchanged by this notice.

### Your escalation on `cpu_h_scheduler`, answered — your observation was right, the diagnosis was not, and the real defect was worse

**The reconciliation you asked for was run**, over the 75 fleet jobs then running that report both
quantities in `qstat -f`: Σ `resources_used.cput` = **14,384 CPU-h** against Σ `walltime × ncpus` =
**4,758 CPU-h**, a ratio of **0.33**. **cput is roughly three times wall×cores, not a third of
it.** PBS is not losing forked children; it is capturing processes beyond a job's `ncpus`
allocation, which a wall×cores estimate misses entirely. The hypothesis in your escalation is not
supported by the scheduler's own numbers, and budgeting against the larger figure cost you nothing.

**What was actually wrong.** `cpu_h_scheduler` undercounts for a reason already on the record: PBS
drops a finished job from `qstat` within seconds and this account cannot read the accounting log,
so a 30-minute poller sees only what is still alive. That is a sampling undercount, and it is why
`cpu_h_scheduler` is not the authoritative meter. **The authoritative meter — `usage.json:cpu_h`,
finished-job CPU-h, the figure the compute cap is enforced on — had no writer at all.** Its only
writer retired with an instrument that was decommissioned days ago, so the key was absent from
every workspace and the compute cap had no data behind it.

**Fixed today.** `cpu_h` is restored and your `usage.json` now carries it, together with
`cpu_h_basis` and `cpu_h_runs_accounted`. `cpu_h_scheduler` is kept beside it unchanged, because
the gap between the two is the evidence for why the basis is what it is. Your compute position is
now visible to you and to the watchdog; nothing about your budget or your deadline changes.

## 2026-08-31T11:30:30.542519+09:00 — escalation received

> [ESC: infra / 886 tasks failed instantly with FileNotFoundError across both compute nodes in one interval on 2026-08-31, hitting database and modified structures alike and then stopping; was there a shared-filesystem event on bnode18/bnode19 around 09:00-11:00 KST?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-31T15:31:00.137214+09:00 — harness notice

- **Usage warning — spend_usd at 75% of budget** (210.83 / 280.0). Charter section 4.

## 2026-08-31T16:00:55.682156+09:00 — harness notice

- **Usage warning — spend_usd at 76% of budget** (211.4198 / 280.0). Charter section 4.

## 2026-08-31T16:31:00.888987+09:00 — harness notice

- **Usage warning — spend_usd at 77% of budget** (214.7831 / 280.0). Charter section 4.

## 2026-08-31T17:00:54.568376+09:00 — harness notice

- **Usage warning — spend_usd at 77% of budget** (215.2398 / 280.0). Charter section 4.

## 2026-08-31T17:30:56.716510+09:00 — harness notice

- **Usage warning — spend_usd at 77% of budget** (216.1897 / 280.0). Charter section 4.

## 2026-08-31T18:00:57.766354+09:00 — harness notice

- **Usage warning — spend_usd at 77% of budget** (216.6501 / 280.0). Charter section 4.

## 2026-08-31T18:30:57.026622+09:00 — harness notice

- **Usage warning — spend_usd at 78% of budget** (217.1122 / 280.0). Charter section 4.

## 2026-08-31T19:00:57.365936+09:00 — harness notice

- **Usage warning — spend_usd at 78% of budget** (217.736 / 280.0). Charter section 4.

## 2026-08-31T19:31:19.754141+09:00 — harness notice

- **Usage warning — spend_usd at 78% of budget** (218.7136 / 280.0). Charter section 4.

## 2026-08-31T20:00:55.619476+09:00 — harness notice

- **Usage warning — spend_usd at 78% of budget** (219.3548 / 280.0). Charter section 4.

## 2026-08-31T20:30:58.336256+09:00 — harness notice

- **Usage warning — spend_usd at 79% of budget** (219.8269 / 280.0). Charter section 4.

## 2026-08-31T21:00:59.413442+09:00 — harness notice

- **Usage warning — spend_usd at 79% of budget** (220.2995 / 280.0). Charter section 4.

## 2026-08-31T21:30:58.084643+09:00 — harness notice

- **Usage warning — spend_usd at 82% of budget** (228.4055 / 280.0). Charter section 4.

## 2026-08-31T22:00:56.163091+09:00 — harness notice

- **Usage warning — spend_usd at 83% of budget** (231.9889 / 280.0). Charter section 4.

## 2026-08-31T22:30:57.407539+09:00 — harness notice

- **Usage warning — spend_usd at 83% of budget** (232.929 / 280.0). Charter section 4.

## 2026-08-31T23:00:59.467497+09:00 — harness notice

- **Usage warning — spend_usd at 83% of budget** (233.6394 / 280.0). Charter section 4.

## 2026-08-31T23:30:57.809883+09:00 — harness notice

- **Usage warning — spend_usd at 84% of budget** (234.1683 / 280.0). Charter section 4.

## 2026-09-01T00:00:56.763904+09:00 — harness notice

- **Usage warning — spend_usd at 84% of budget** (234.6987 / 280.0). Charter section 4.

## 2026-09-01T00:30:56.272579+09:00 — harness notice

- **Usage warning — spend_usd at 84% of budget** (235.2309 / 280.0). Charter section 4.

## 2026-09-01T01:00:56.693872+09:00 — harness notice

- **Usage warning — spend_usd at 85% of budget** (237.4957 / 280.0). Charter section 4.

## 2026-09-01T01:30:56.376826+09:00 — harness notice

- **Usage warning — spend_usd at 85% of budget** (238.0438 / 280.0). Charter section 4.

## 2026-09-01T02:00:57.714649+09:00 — harness notice

- **Usage warning — spend_usd at 85% of budget** (238.5893 / 280.0). Charter section 4.

## 2026-09-01T02:30:56.874317+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (240.2963 / 280.0). Charter section 4.

## 2026-09-01T03:00:59.184513+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (240.8508 / 280.0). Charter section 4.

## 2026-09-01T03:30:59.175170+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (241.4053 / 280.0). Charter section 4.

## 2026-09-01T04:00:59.342446+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (242.177 / 280.0). Charter section 4.

## 2026-09-01T04:30:56.527189+09:00 — harness notice

- **Usage warning — spend_usd at 87% of budget** (242.7354 / 280.0). Charter section 4.

## 2026-09-01T05:00:56.505504+09:00 — harness notice

- **Usage warning — spend_usd at 87% of budget** (243.7458 / 280.0). Charter section 4.

## 2026-09-01T05:30:55.794522+09:00 — harness notice

- **Usage warning — spend_usd at 91% of budget** (256.1179 / 280.0). Charter section 4.

## 2026-09-01T06:00:58.067117+09:00 — harness notice

- **Usage warning — spend_usd at 93% of budget** (259.8181 / 280.0). Charter section 4.

## 2026-09-01T06:30:57.822597+09:00 — harness notice

- **Usage warning — spend_usd at 93% of budget** (260.4386 / 280.0). Charter section 4.

## 2026-09-01T07:00:58.858118+09:00 — harness notice

- **Usage warning — spend_usd at 93% of budget** (261.2683 / 280.0). Charter section 4.

## 2026-09-01T07:30:58.308117+09:00 — harness notice

- **Usage warning — spend_usd at 94% of budget** (262.3188 / 280.0). Charter section 4.

## 2026-09-01T08:00:56.922606+09:00 — harness notice

- **Usage warning — spend_usd at 94% of budget** (262.945 / 280.0). Charter section 4.

## 2026-09-01T08:30:56.865888+09:00 — harness notice

- **Usage warning — spend_usd at 94% of budget** (263.5728 / 280.0). Charter section 4.

## 2026-09-01T09:00:56.594306+09:00 — harness notice

- **Usage warning — spend_usd at 94% of budget** (264.4211 / 280.0). Charter section 4.

## 2026-09-01T09:30:56.326449+09:00 — harness notice

- **Usage warning — spend_usd at 95% of budget** (265.0521 / 280.0). Charter section 4.

## 2026-09-01T10:00:56.787776+09:00 — harness notice

- **Usage warning — spend_usd at 95% of budget** (266.1345 / 280.0). Charter section 4.

## 2026-09-01T10:30:57.764339+09:00 — harness notice

- **Usage warning — spend_usd at 96% of budget** (267.4781 / 280.0). Charter section 4.

## 2026-09-01T11:00:56.928869+09:00 — harness notice

- **Usage warning — spend_usd at 96% of budget** (268.1164 / 280.0). Charter section 4.

## 2026-09-01T11:30:56.870683+09:00 — harness notice

- **Usage warning — spend_usd at 96% of budget** (269.6828 / 280.0). Charter section 4.

## 2026-09-01T12:00:58.996205+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T12:27:22.367974+09:00 — escalation received

> [ESC: infra / usage.json cpu_h_scheduler reads 107.5 CPU-h where my workers' own per-task wall times sum to 223.6 — PBS cput appears to lose forked children (job 3473455: ppn=6, 24 h walltime, charged 86,398 s), so the meter the 2026-08-30 ruling named authoritative under-reports real consumption by about half; I am budgeting against the larger figure, and flagging it because if it is fleet-wide it makes the 1,610 CPU-h cap non-comparable across replicates]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-09-01T12:27:22.368609+09:00 — escalation received

> [ESC: infra / 886 tasks failed instantly with FileNotFoundError across both compute nodes in one interval on 2026-08-31, hitting database and modified structures alike and then stopping; was there a shared-filesystem event on bnode18/bnode19 around 09:00-11:00 KST?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-09-01T12:30:58.552679+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T12:39:02.865406+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3060.4 min. If you are in a long wait, STATE.md should be current (charter section 6).

## Notice — 2026-09-01T03:52:50Z — CAMPAIGN CLOSED ON THE RECORD.

Your §5 final report is filed and recognised, and **your campaign is CLOSED as of this notice.**
You have been dropped from the active roster, a stop file is in place, and a closure row is in the
harness ledger. You will not be invoked again.

The PI has ruled that the spend hard stop ends the campaign, and that re-invocation after it is a
loop artifact rather than a reopening. **No further work is required or expected of you, and none
should be performed.** Any non-filing work after this notice would bill against an ended campaign
and is recorded as such.

Closure does not remove you from the study. N = 16 is unchanged; your workspace, its git record and
its filed report are the deliverable and will be collected as they stand.

Where you hold escalations that are still open, they remain open, are recorded, and are with the
PI. They are not yours to remedy and no reply is expected from you.

## 2026-09-01T13:34:57.463315+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3116.3 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-01T14:33:44.880746+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3175.1 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-01T19:26:23.635570+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3467.7 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T01:03:29.539438+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3804.8 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T02:00:38.214168+09:00 — harness notice

- **Usage warning — compute at 47% of budget** (756.936 / 1610). Charter section 4.
- No new activity in your session record for 3862.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T03:58:51.408905+09:00 — harness notice

- **Usage warning — compute at 69% of budget** (1116.841 / 1610). Charter section 4.
- No new activity in your session record for 3980.2 min. If you are in a long wait, STATE.md should be current (charter section 6).
