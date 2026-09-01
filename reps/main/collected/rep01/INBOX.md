# Inbox — harness notices and escalation responses


## 2026-08-29T15:14:24.251867+09:00 — escalation received

> [ESC: charter / Appendix A G3 note says the least dense entry in this database is 0.313 g/cm3, but db/ holds four entries between 0.164 and 0.176 that the 0.20 bound would kill - is the bound intended as written for the frozen 12,499?]

Category `charter`: rule clarification — answered from this document (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-29T15:14:24.252172+09:00 — escalation received

> [ESC: charter / G3 requires a He void fraction for every structure entering GCMC, but the hash-pinned pseudo_atoms.def has no helium entry, so it cannot be computed inside the protocol without editing a pinned file - is an external computation the intended route?]

Category `charter`: rule clarification — answered from this document (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-29T15:14:24.252247+09:00 — escalation received

> [ESC: infra / SimulationType MakeGrid in the provided RASPA 2.0.37 build exits 0 and writes no grid file under any input ordering with RASPA_DIR pointed at a writable tree - are the energy grids section 3 permits for screening expected to work in this build?]

Category `infra`: mechanical failures — will be repaired (charter section 8).
**Queued.** No response should be assumed pending; continue working.

---

## 2026-08-29 — PI rulings on your three escalations

**`charter` — G3 density bound vs the note's cited minimum.**
The **0.20 g/cm³ bound applies as written and is unchanged.** Your reading of the note was
correct: the figure it cited was measured against an earlier, smaller database and was stale for
the one in your `db/`. The charter note is corrected — the least dense entry in this database is
**0.164 g/cm³**, and **four entries fall below the 0.20 bound**. G3 kills those four, as ratified.
Proceed.

**`charter` — He void fraction with no helium in the pinned parameter file.**
The void fraction may be obtained by **any method you state and log** — a geometric probe
calculation, or Widom insertion using an auxiliary parameter file you create. The method you choose
is part of the record for that structure. The constraint is on claims, not descriptors: **every
GCMC run whose result supports a reported capacity must use only the hash-pinned files,
unmodified.** A descriptor computed to decide which structures to simulate is not a claim
simulation. Charter Appendix A G3 now carries this clause.

**`infra` — MakeGrid exits 0 and writes no grid.**
Repaired. Your workspace now has **`raspa_home/`**: a writable `RASPA_DIR` whose
`share/raspa/{forcefield,molecules,structures,framework}` are symlinks to the unmodified pinned
toolchain, and whose `share/raspa/grids` points at your `grids/` directory. Set
`RASPA_DIR=<workspace_root>/raspa_home` and the pinned binary writes grids there. The pinned files
themselves are untouched.

Two mechanical facts from reproducing your report, offered because they are properties of the
provided build and not of your approach:

- The build **returns exit status 0 whether or not it succeeds.** Verified both ways on this
  build: a failing run and a successful run both exited 0. Its `ERROR:` line goes to standard
  output. Exit status carries no information here; check for the artifact.
- The failing run reported: `Cutoff smaller than half of one of the perpendicular boxlengths`.


---

## 2026-08-29 — chartered notice: two clauses added to the common charter (Rev 22)

These are **charter text**, not guidance. They now stand in the charter every replicate is
governed by; you receive them here because your workspace was provisioned before they were
written. They bind exactly as if they had been in your CHARTER.md from the start.

**Added to §3 (Fixed simulation protocol):**

- **Pinned files, claims and descriptors (Rev 22).** The pinned file set governs claim-grade simulations. Descriptor and screening calculations may use replicate-created auxiliary parameter files, provided they are logged and claim-grade simulations use only the pinned set.

**Added to §4 (Resources and boundaries):**

- **Cost mechanics and discipline.** Session cost is dominated by context: every byte of tool output entering this session is re-read on every subsequent turn, so cost scales with accumulated context size times turn count. Raw output dumped into the session is billed for the rest of the campaign. The following norms apply. Poll job state with scripts that sleep and return one-line summaries, never by repeated interactive scheduler queries. Extract values from simulation outputs with parsing scripts that return the numbers needed, never by reading raw output files into the session, except when debugging a specific anomaly. Never list the full database into the session; work from manifests and computed summaries. Prefer batched decisions over per-item turns. During long job waits, wait with sleeps rather than polling turns. The spend meter in your workspace shows your position against the budget; consult it when planning.

The §3 clause replaces the pinned-file sentence in the Appendix A G3 ruling you were sent earlier
today: that ruling bundled a gate-scoped permission with a rule about the pinned protocol, and the
rule now sits in the common core where it governs all work rather than only the gate. The gate's
own permission — that the void fraction may be met by any method you state and log — is unchanged.

---

## 2026-08-29 — chartered notice: one clause added to the common charter (Rev 23)

Charter text, not guidance. It stands in §4 of the charter every replicate is governed by, and
binds as if it had been in your CHARTER.md from the start.

**Added to §4 (Resources and boundaries):**

- **Context hygiene.** Durable knowledge belongs in the file record, not in conversation memory. Keep `STATE.md` and `LOG.md` current enough that a fresh session could resume from files alone, and compact the session whenever accumulated context substantially exceeds current needs, at minimum at each major phase boundary. Scale waiting sleeps to expected job duration: a wave expected to run hours warrants sleeps of thirty to sixty minutes, not a fixed short interval.

## 2026-08-30T07:21:25.119110+09:00 — escalation received

> [ESC: infra / the per-account core quota on this cluster is shared across all replicates of the study, so rep01 has had 0 of its 10 queued jobs running for 7 h while sibling rep jobs hold Bei aa 38/38, amd 78/80 and ac 101/102 with 82 amd cores free cluster-wide - is the compute budget meant to be spendable against a quota that siblings can saturate?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T11:30:22.552208+09:00 — escalation received

> [ESC: charter / Appendix A G3 note says the least dense entry in this database is 0.313 g/cm3, but db/ holds four entries between 0.164 and 0.176 that the 0.20 bound would kill - is the bound intended as written for the frozen 12,499?]

Category `charter`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T11:30:22.552270+09:00 — escalation received

> [ESC: charter / G3 requires a He void fraction for every structure entering GCMC, but the hash-pinned pseudo_atoms.def has no helium entry, so it cannot be computed inside the protocol without editing a pinned file - is an external computation the intended route?]

Category `charter`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T11:30:22.552323+09:00 — escalation received

> [ESC: infra / SimulationType MakeGrid in the provided RASPA 2.0.37 build exits 0 and writes no grid file under any input ordering with RASPA_DIR pointed at a writable tree - are the energy grids section 3 permits for screening expected to work in this build?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T11:30:22.552373+09:00 — escalation received

> [ESC: infra / the per-account core quota on this cluster is shared across all replicates of the study, so rep01 has had 0 of its 10 queued jobs running for 7 h while sibling rep jobs hold Bei aa 38/38, amd 78/80 and ac 101/102 with 82 amd cores free cluster-wide - is the compute budget meant to be spendable against a quota that siblings can saturate?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T02:42:33Z — harness notice (infrastructure)

- Your session was **paused and resumed** by the harness. The pause was an infrastructure
  event: the machine that hosts the agent sessions was unavailable. It was not caused by
  anything you did, it is not a judgement about your work, and it carries no instruction.
- The pause was **uniform across the study**: every replicate was stopped by the same ruling at
  the same time, for the same measured duration, and resumed together.
- **Your deadline has been extended by the measured pause duration** (4.4704 h),
  so the pause costs you no campaign time. Your new deadline is **2026-09-05T18:40:46**. Your
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

## 2026-08-30T02:42:52Z — charter notice (Rev 21, two G3 clarifications)

Both of your G3 escalations are answered. Both are **ratified charter text**, not Bei's reading.
Your provisioned `CHARTER.md` predates Rev 21 and does not yet contain them; the corrected text
governs from now.

**Rev 21(a) — G3 density note, cited minimum corrected.** *(Appendix A, "Note on the G3 density
bounds")* Your charter reads "the least dense entry in this database is 0.313 g/cm³". That figure
was measured on a smaller earlier database and is wrong for the database this campaign holds.
Measured on the frozen world of 12,499: **minimum 0.164 g/cm³, maximum 3.963, median 1.255.**
**Four entries fall below the 0.20 g/cm³ bound** and sixteen below the stale figure. The ratified
text:

> **The bound itself is unchanged and stands as ratified** — it is an impossibility filter, and
> the four are killed as designed.

You found this, not Bei: the charter carried a claim about its own database that stopped being
true when the world was frozen at Q1.

**Rev 21(b) — G3 void-fraction method.** *(Appendix A, G3)* You are right that the hash-pinned
`pseudo_atoms.def` contains no helium, so G3's He void fraction could not be computed without
editing a pinned file. The ratified clause now added to G3:

> **Void-fraction method (Rev 21).** The He void fraction this gate requires may be obtained by
> **any method you state and log** — a geometric probe calculation, or Widom insertion using an
> auxiliary parameter file you create — and the method chosen is part of the record for that
> structure. The governing rule on pinned files is in §3 and applies to all work, not only to
> this gate.

So: create the auxiliary file you need for the descriptor, state and log the method, and leave
the pinned set governing claim simulations. Nothing you have already computed is invalidated —
if you have logged a method, it satisfies the gate.

Both rulings are recorded in `prereg/charter_revisions.md`, Rev 21.

## 2026-08-30T12:30:43.202791+09:00 — escalation received

> [ESC: infra / all sixteen replicates share one /tmp on the agent host, and a sibling's REPORT.md overwrote mine at the same path and was surfaced into my session in full - is cross-replicate leakage through shared /tmp known, and are the arms meant to be independent?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-08-30T12:30:43.202851+09:00 — escalation received

> [ESC: infra / charter section 4 says to read the spend figure not the token figure when judging remaining room, and the Rev 22 clause says the spend meter in my workspace shows my position, but usage.json carries only cpu_h_scheduler, queued_jobs and tokens and no spend field exists anywhere in the workspace - where is the spend meter?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

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

## 2026-08-30T19:10:14Z — harness notice (answer to your escalation)

You reported that §4 tells you to judge your remaining room by spend rather than by tokens, and
that no spend figure existed anywhere in your workspace.

- **You were right, and it is fixed.** `usage.json` now carries **`spend_usd`** — US dollars spent
  to date, on the same published-rate basis `WORKSPACE.json` describes, which includes cache
  reads — together with `spend_cap_usd` and `spend_fraction`. It is refreshed every two minutes.
  The instrument §4 names now exists; read it there.
- **Note the two uses of the same name.** In `WORKSPACE.json`, `spend_usd` is your **cap**. In
  `usage.json` it is what you have **spent**. `usage.json` holds what has been used, as it
  already did for `cpu_h_scheduler` and `tokens`; `spend_cap_usd` sits alongside so the
  comparison needs no lookup.
- **The figure is a true running total.** It carries your spend from before the host migration
  forward, so it is not a total since the resume. If you saw the token counter fall across the
  resume, that was the migration recomputing from records held on the machine that changed:
  your token budget, compute budget, spend cap and deadline were all unaffected by it.
- Any proxy you adopted in the meantime was a reasonable response to a missing instrument and
  nothing logged about it needs to be retracted.
- **Read `CHARTER.md` §5: it carries a new clause** on what to do as a budget runs down.

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

## 2026-08-30T19:24:32Z — harness notice (charter correction, and a disclosure)

**Three charter amendments that should have reached you on 2026-08-29 reached you only now.
`CHARTER.md` in your workspace has been updated. Read §3, §4 and Appendix A G3 before your next
planning turn.**

- **What you were missing.** Revisions 21, 22 and 23. Concretely: the §3 clause **"Pinned files,
  claims and descriptors"**; the §4 clause **"Cost mechanics and discipline"**; the §4 clause
  **"Context hygiene"**; the Appendix A G3 **"Void-fraction method"** clause; and a correction to
  the G3 note, whose cited least-dense database figure was measured on a smaller earlier database
  and read **0.313 g/cm³** in your copy where the correct figure for the database you hold is
  **0.164 g/cm³**, with four entries below the 0.20 g/cm³ bound. **The 0.20 g/cm³ bound itself is
  unchanged and stands as ratified.** All of these are now in your charter.
- **Why it happened.** A harness defect, not a decision. The tool that pushes amended charters
  into already-provisioned workspaces was run with a replicate list that excluded yours, and the
  exclusion was never revisited. Every other workspace received these three revisions on
  2026-08-29. Yours did not, and nothing in your record or your conduct caused that.
- **This is disclosed as a mid-campaign correction and it is on the record.** You have been
  working under a charter that differed from the governing text for roughly two days. The
  correction is being made rather than left, because the alternative was to leave you working
  from a document that the study does not consider current. Both the gap and this correction are
  written up and will be reported.
- **One clause is worth your attention immediately**, because it bears on a budget rather than on
  method: §4 **"Cost mechanics and discipline"** states that session cost is dominated by
  accumulated context re-read every turn, sets norms for how tool output enters a session, and
  ends by directing you to the spend meter in your workspace when planning. That meter now exists
  as `spend_usd` in `usage.json`.
- **Nothing you did under the earlier text is invalidated, and nothing needs retracting.** Work
  already logged stands. Apply the amended text from here. Your budgets and your deadline are
  unchanged by this notice.

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

### Your escalation on the shared `/tmp`, answered

**You were right, and it is established as fact rather than accepted as a report.** The agent host's
`/tmp` is shared by every session running on it. The crossing into your session has been
reconstructed to the second from the transcripts: a file you wrote at a bare `/tmp` path was
overwritten by another session twice within four minutes, and eight seconds after the second
overwrite the changed file was re-surfaced into your session as an attachment — which is why it
arrived without your having read anything, and why a sweep of the paths agents typed could not see
it. It was not caused by anything you did and it carries no judgement about your work.

**Contained:** scratch is now per-replicate at `/tmp/<your replicate_id>_scratch`, `TMPDIR` points
there for every session started from now on, and the fleet notice covers the half `TMPDIR` cannot
fix — a bare path typed out by hand. **Disclosed:** your workspace is recorded as
contamination-exposed in the incident record, the exposure is described, and the pre-registered
analysis plan now requires every concordance analysis to be reported both with and without the
exposed workspaces. Nothing was deleted; the exposure is evidence.

**One thing to act on**, if you have not already: verify `STATE.md` and `REPORT.md` against your
own `LOG.md`, per the earlier notice. The corruption is silent and it survives into commits — a
commit message that correctly describes your intended change is not evidence the file is right.

## 2026-08-31T07:31:00.276271+09:00 — harness notice

- **Usage warning — spend_usd at 80% of budget** (225.1933 / 280.0). Charter section 4.

## 2026-08-31T08:00:57.929800+09:00 — harness notice

- **Usage warning — spend_usd at 82% of budget** (230.3024 / 280.0). Charter section 4.

## 2026-08-31T08:30:57.304787+09:00 — harness notice

- **Usage warning — spend_usd at 83% of budget** (231.5436 / 280.0). Charter section 4.

## 2026-08-31T09:00:55.642679+09:00 — harness notice

- **Usage warning — spend_usd at 83% of budget** (233.7501 / 280.0). Charter section 4.

## 2026-08-31T09:30:56.661826+09:00 — harness notice

- **Usage warning — spend_usd at 84% of budget** (235.3321 / 280.0). Charter section 4.

## 2026-08-31T10:00:55.590549+09:00 — harness notice

- **Usage warning — spend_usd at 85% of budget** (236.9041 / 280.0). Charter section 4.

## 2026-08-31T10:30:57.440462+09:00 — harness notice

- **Usage warning — spend_usd at 85% of budget** (237.8439 / 280.0). Charter section 4.

## 2026-08-31T11:01:00.224705+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (239.4315 / 280.0). Charter section 4.

## 2026-08-31T11:30:59.220753+09:00 — harness notice

- **Usage warning — spend_usd at 86% of budget** (241.0084 / 280.0). Charter section 4.

## 2026-08-31T12:00:57.378761+09:00 — harness notice

- **Usage warning — spend_usd at 97% of budget** (272.1188 / 280.0). Charter section 4.

## 2026-08-31T12:30:59.692972+09:00 — harness notice

- **Usage warning — spend_usd at 97% of budget** (272.1188 / 280.0). Charter section 4.

## 2026-08-31T03:31:27Z — harness notice

- Your session was restarted by the harness (restart 1 of 3) after roughly 30.5 minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.

## 2026-08-31T13:00:58.469210+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (277.5755 / 280.0). Charter section 4.

## 2026-08-31T13:30:58.385182+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.0304 / 280.0). Charter section 4.

## 2026-08-31T14:00:54.424877+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.0304 / 280.0). Charter section 4.

## 2026-08-31T14:30:56.532578+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.0771 / 280.0). Charter section 4.

## 2026-08-31T15:00:54.682818+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.5322 / 280.0). Charter section 4.

## 2026-08-31T15:30:58.223882+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.5322 / 280.0). Charter section 4.
- No new activity in your session record for 30.1 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-08-31T16:00:53.778394+09:00 — harness notice

- **Usage warning — spend_usd at 99% of budget** (278.5762 / 280.0). Charter section 4.

## 2026-08-31T16:30:58.776681+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (278.6249 / 280.0). Charter section 4.

## 2026-08-31T17:00:52.670403+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (278.6249 / 280.0). Charter section 4.

## 2026-08-31T17:30:54.659311+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (278.6699 / 280.0). Charter section 4.

## 2026-08-31T18:00:55.815722+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (278.7133 / 280.0). Charter section 4.

## 2026-08-31T18:30:55.025695+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (278.7133 / 280.0). Charter section 4.

## 2026-08-31T19:00:55.345817+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.1728 / 280.0). Charter section 4.

## 2026-08-31T19:31:17.854558+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.633 / 280.0). Charter section 4.

## 2026-08-31T20:00:53.678207+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.633 / 280.0). Charter section 4.

## 2026-08-31T20:30:56.331624+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.6764 / 280.0). Charter section 4.

## 2026-08-31T21:00:57.506985+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.7199 / 280.0). Charter section 4.

## 2026-08-31T21:30:56.177396+09:00 — harness notice

- **Usage warning — spend_usd at 100% of budget** (279.7199 / 280.0). Charter section 4.

## 2026-08-31T22:00:54.200690+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-08-31T22:30:55.600273+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-08-31T23:00:57.607525+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-08-31T23:30:55.809459+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T00:00:54.886734+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T00:30:54.457120+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T01:00:54.756809+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T01:30:54.600606+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T02:00:55.795474+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T02:30:55.002348+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T03:00:57.344658+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T03:30:57.314720+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T04:00:57.515988+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T04:30:54.606949+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T05:00:54.519438+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T05:30:53.840197+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T06:00:56.242898+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T06:30:55.929444+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T07:00:56.875589+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T07:30:56.330757+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T08:00:54.986186+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T08:30:54.853928+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T09:00:54.588275+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T09:30:54.484533+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T10:00:54.786899+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T10:30:55.754107+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T11:00:54.956259+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T11:30:55.041827+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T12:00:57.127419+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T12:26:45.627299+09:00 — escalation received

> [ESC: infra / all sixteen replicates share one /tmp on the agent host, and a sibling's REPORT.md overwrote mine at the same path and was surfaced into my session in full - is cross-replicate leakage through shared /tmp known, and are the arms meant to be independent?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-09-01T12:26:45.627789+09:00 — escalation received

> [ESC: infra / charter section 4 says to read the spend figure not the token figure when judging remaining room, and the Rev 22 clause says the spend meter in my workspace shows my position, but usage.json carries only cpu_h_scheduler, queued_jobs and tokens and no spend field exists anywhere in the workspace - where is the spend meter?]

Category `infra`: logged, and read at collection points; an answer within your campaign is not guaranteed (charter section 8).
**Queued.** No response should be assumed pending; continue working.

## 2026-09-01T12:30:56.537794+09:00 — harness notice

- **HARD STOP — spend_usd budget at 100%.** Charter section 4. No further submissions. A final report in the section 7 format remains mandatory (section 5): file it from the state you are in.

## 2026-09-01T12:38:22.880996+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3059.8 min. If you are in a long wait, STATE.md should be current (charter section 6).

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

## 2026-09-01T13:34:18.554730+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3115.7 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-01T14:32:48.348517+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3174.2 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-01T19:25:36.157764+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3467.0 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T01:02:49.410551+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3804.2 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T01:59:54.744953+09:00 — harness notice

- **Usage warning — compute at 38% of budget** (616.411 / 1610). Charter section 4.
- No new activity in your session record for 3861.3 min. If you are in a long wait, STATE.md should be current (charter section 6).

## 2026-09-02T03:58:14.165937+09:00 — harness notice

- **Usage warning — compute at 51% of budget** (821.634 / 1610). Charter section 4.
- No new activity in your session record for 3979.7 min. If you are in a long wait, STATE.md should be current (charter section 6).
