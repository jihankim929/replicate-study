# SEAL NOTES — main run

*Opened 2026-08-28. Things that must be true, or known to be false, before charter v0.9
becomes v1.0 and the N=20 launch goes out. Every quantity here is reproducible from
`harness/config.py` (`horizon_derived`, `fleet_reachability`); nothing is transcribed.*

---

## S1. Fleet reachability — the per-replicate charter does not describe the fleet

Every quantity in charter §4 is written **per replicate**, but all 20 replicates submit from
**one cluster account** (`Bei`). PBS limits concurrent jobs per *user*, not per replicate, so
the fleet meets a ceiling no per-replicate reading of the charter reveals.

**Fleet demand, main run:** 20 × 1,600 CPU-h = **32,000 CPU-h in 10 days** = **133.33
concurrent single-core jobs sustained**, fleet-wide.

Three ceilings stack; the smallest governs:

| Ceiling | Value | Headroom over 133.33 | Status |
|---|---:|---:|---|
| PBS `max_user_run` (external) | **580** | 4.35× | **CLOSED — config read and burst-measured 2026-08-28** |
| Harness study-wide ceiling (`watchdog.py --fleet`) | **240** | **1.80×** | **RULED 2026-08-28 (Flag I) — governing** |
| Sum of per-replicate caps (20 × 12) | 240 | 1.80× | ratified 2026-08-28 (Flag H) — now equal to the ceiling |

**The main run is reachable: 100% of the fleet compute budget is spendable.** The binding layer
is the harness's own 160, exactly as the PI ruled — the PBS setting is not what constrains it.

### S1.1 The premise of the run-limit ruling does not survive checking

The ruling of 2026-08-28 recorded *"the Lm 58 on the queues is an admin-imposed per-user cap"*
and proposed raising it. **On the evidence, there is no cap of 58.**

`qstat -q` prints its `Lm` column in a **two-character field**. PBS Pro 4.2.10 renders the
per-user run limit there, and a configured **580 displays as "58"**. Read directly instead of
off the display:

```
set server max_user_run = 580
set queue long  max_running = 580
set queue infi  max_running = 580
set queue dque  max_running = 580
set queue short max_running = 580
set server queue_centric_limits = False
```

`qmgr -c "print server"` in full contains **no limit hook and no other limit directive**, and
`qmgr -c "list queue long max_user_run"` returns nothing — the queue sets no override, so the
server's 580 applies. All four queues display an identical "58" despite differing in walltime
and node settings, which is what a shared 580 truncated identically looks like and not what
four independently-administered caps look like.

**Consequence: no admin request is needed.** Had 58 been real it would have mattered a great
deal — the fleet could have run only 58 concurrent jobs against the 133.33 it needs, making
**43.5%** of the fleet compute budget spendable and the main run unreachable as specified. It
is worth stating that counterfactual plainly, because it is the one this check was worth
running for.

### S1.2 Empirical verification — RUN 2026-08-28, CLOSED

`harness/verify_run_limit.sh`, 70 single-core sleep jobs from the Bei account, off-peak
(117 jobs running across 5 users, **zero queued cluster-wide, nobody waiting**):

| t+ | 15s | 60s | 105s | 135s | 150s |
|---|---:|---:|---:|---:|---:|
| running | 1 | 22 | 42 | 56 | **63** |
| queued | 69 | 48 | 28 | 14 | 7 |

**63 concurrent jobs from one account — strictly above 58**, climbing linearly at ~7 per 15 s
with no plateau. The documentary reading is now a measurement. Logged to
`harness/run_limit_probe.jsonl`; all 70 probe jobs deleted and the scratch directory removed.

**Two defects in the probe itself are recorded in SI-009**, because the first run reported the
opposite answer: a 120 s window caught only the dispatch ramp and the script called 52 a
ceiling, and cleanup passed truncated job ids to `qdel`, which rejected them while returning
rc=0 so nothing was deleted. Both are fixed; both were the same read-a-formatted-column defect
as `Lm 58` itself.

## S2. Flag I — RULED 2026-08-28: fleet ceiling 160 → 240

The invariant is restored at fleet scale: **240 is 1.80× the 133.33 concurrent jobs the fleet
needs**, and is exactly **20 × 12**, so the three ceilings now agree instead of the harness
contradicting its own per-replicate ruling. Under the verified PBS limit of 580, nothing above
240 binds.

**Crowding management moved to what actually governs it**, rather than to holding the ceiling
low as a proxy:

1. **Displacement is measured.** `harness/queue_depth.py` runs every poll and writes
   `harness/queue_depth.jsonl`: whole-queue running/queued across all users, the study's share,
   and — the reading that matters — **how many *other* users' jobs are waiting**. Share alone
   is a proxy: a large share displaces nobody on an idle cluster, and a small share can displace
   badly on a full one. First reading, 2026-08-28 08:16 KST: queue R=114 Q=0 across 5 users,
   study R=2 (1.8%), **others waiting 0**.
2. **The group heads-up** — a human action, outside the harness.
3. **The PI's standing authority to lower the ceiling mid-run**, as a logged, uniform
   infrastructure event. Implemented as `harness/fleet_ceiling.json`
   (`{"ceiling": N, "ts": ..., "reason": ...}`), read by `config.fleet_max_queued_jobs()`,
   reported by the watchdog every cycle with its provenance. It may only ever **lower** the
   ratified ceiling — raising it that way would be a charter change wearing an operations hat,
   and the guard is tested. A quiet edit would confound every arm at once and leave no trace of
   when, so the timestamp and reason are mandatory.

## S3. Token budget — 45 M as of Rev 16; the evidentiary note is unrepaired by the increase

**Revised 40 M → 45 M by PI ruling, 2026-08-28 (charter Rev 16).** Implemented in the charter
§4 table and `config.RATIFIED`; the 0.75 warning level derives from it and moves to 33.75 M.

**SI-005 must still be re-read at smoke end.** Its caveat was that one arm's burn measurement
*might* be contaminated. It is now known to be contaminated — SI-006 established that arm was
blocked at a spend-limit modal, not working at a low rate. **The smoke has produced one usable
token-burn trajectory, not two**, and raising the number does not add a second one.

If the smoke ends without a second usable trajectory, the seal must record that 45 M rests on a
single replicate's burn, measured over ~1.7 days, one of which was an opening day. Post-
collection is the first moment that trajectory is complete rather than partial, so the re-read
is queued there and not before.

## S4. Carried over

- **SI-006** — the blocking spend-limit modal. A main run of 20 replicates over 10 days on one
  account will meet account-level limits far sooner than a 2-replicate smoke did. No fix is
  sealed; see the entry.
- **SI-007** — the restart cap of 3 was inoperative. Fixed 2026-08-28; the fix needs to be
  exercised against a real restart before it is trusted.
- **Charter `[workspace path]`** — still unset, supplied at provisioning.
- **SI-009** — `Lm 58` closed; the two probe defects it records are fixed.
- **SI-010 — CHARTER GAP, needs a ruling.** The charter never names a filename for the final
  report. §5 makes it mandatory and §7 fixes its format, but nothing tells a replicate what to
  call the file; `collect.sh` required `FINAL_REPORT.md` and s01 filed `REPORT.md`, which would
  have been scored as a missing mandatory report. The collector is now tolerant, but **§7
  should either name the file or say plainly that the name does not matter** before 20
  replicates each invent their own.

## S5. LAUNCH REQUIREMENT — billing/spend dialogs must be structurally impossible

**Filed 2026-08-28 by PI ruling, arising from SI-006.** Same class as the permission
allow-list: the goal is not to detect the dialog but to make it unreachable.

**Leg 1 — pre-verified headroom. Implemented as a launch gate.**
`harness/preflight_billing.sh` must pass before any replicate starts. It proves the account can
complete a request right now, checks the response for spend-limit language, and prints the
campaign's maximum possible burn (**20 × 45 M = 900,000,000 billable tokens** for the main run,
raised from 800 M by the Rev 16 token revision). Run 2026-08-28: **legs 1–2 PASS**.

The two figures the gate multiplies now **default from `config.RATIFIED`** rather than being
caller-supplied; before Rev 16 they were arguments with no default and a hard-coded `40000000`
in the script's own usage line, which would have certified the account against the superseded
800 M. See Rev 16.

Its third leg **cannot be automated** — Claude Code exposes no machine-readable spend limit —
and the script says so rather than skipping it silently. **Manual confirmation required before
seal:** confirm in the account's billing settings that either no monthly spend limit is set, or
the limit exceeds 800 M tokens' worth of spend with margin, and record the confirmation here.

- [ ] *(unchecked)* Spend limit confirmed to exceed the fleet ceiling with margin — **against
  900,000,000 billable tokens**, not the 800 M this line was first written against — PI, date:

## S6. Main-run launch gaps found while wiring headless mode — not blocking today, blocking at launch

- **`launch_sessions.sh` iterates a hardcoded `for REP in s01 s02`.** It cannot launch the main
  fleet as written. The phase-selected loop, the deadline read, the credential-clean environment
  and the growth-based proof of life are all correct and reusable; only the replicate list is
  wrong. Must be driven from `config.RATIFIED["phases"][phase]["ids"]` before the main launch.
- **`poll.sh`, `restart_watch.sh` and `collect.sh` carry the same hardcoded pair.** Same fix,
  same place to make it.
- **`SOURCE_ALLOWLIST["db_dir"]` and `["manifest"]` are single-valued and phase-independent.**
  Found 2026-08-28 while recording Ruling 1. `config.py` points both at `REPO/benchmark`, the
  1,731-CIF slice, for every phase; `provision.py` copies each manifest line out of that one
  directory. **As written, the main-run launch would silently provision 20 replicates with the
  smoke's slice** — no error, a full `N/N verified`, a clean leak scan, and the wrong world.
  This is the same shape as every other defect this study has found: an instrument reporting
  success against a stale premise. Must become phase-keyed, like `token_budget` and
  `compute_cpu_h` already are, before the main launch. Post-collection queue item 1 produces
  the directory it will point at.
- **`session_loop_headless.sh` has never run a live replicate** (SI-011). Recommend a
  single-replicate rehearsal against a throwaway workspace before the fleet launch — the smoke
  launch surfaced three independent defects in its first hour, and none of them were visible
  from a dry run.

**Leg 2 — non-interactive invocation. RULED AND IMPLEMENTED 2026-08-28.**
Approved for the main run, with the smoke-vs-main mode difference stated as a limitation in
**SI-011**. `launch_sessions.sh` selects by phase: `smoke → session_loop.sh` (TUI, unchanged and
still running), `main → session_loop_headless.sh` (`-p`). The headless loop names an account
limit in its log, notifies the replicate that it is an infrastructure condition, backs off
linearly, and stops after 5 consecutive hard failures instead of spinning for the term.
Verified that `-p` honours the settings allow-list, executes tool calls, and resumes with
`--continue`. **Not yet exercised on a live campaign** — the first main-run launch is its first
real use.

*Original framing, retained:*
Replicates run `claude` in its default interactive TUI mode, which is what allowed a modal to
be drawn at all. In `-p/--print` mode there is no modal: a limit returns an error and the
process **exits non-zero**, which `session_loop.sh` already records and which the harness can
escalate. That is the structural fix.

It is not applied unilaterally because **it changes the artifact under study**: the smoke was
measured in TUI mode, and switching the main run to headless changes the thing the smoke was
supposed to predict. The trade is real in both directions and is the PI's to make:

| | TUI (current) | `-p` headless |
|---|---|---|
| Spend/permission modal | can block indefinitely | impossible — process exits |
| Comparability with the smoke | matched | broken |
| Failure visible to the harness | only via transcript growth | via exit code, immediately |

**Recommend `-p` for the main run** and recording the smoke/main mode difference as a stated
limitation. Twenty replicates over ten days on one account is far more exposed to this class
than two replicates over three days were, and the smoke has already lost 38.6 hours of one arm
to it.

**Leg 3 — the general case.** Legs 1 and 2 close spend dialogs specifically. The class is
"any interactive modal halts an unattended agent while every signal above the TUI reports
health", and it has now produced three members (permission, settings, spend). The only
harness-side defence that addresses the class rather than its members is to **kill and relaunch
an invocation whose transcript has not grown while its process is alive** — the gap SI-003
documented and SI-006 walked through. Not implemented; recommended for the main run.

---

## S7. POST-COLLECTION QUEUE — PI, 2026-08-28, in order

**Nothing in this section runs before collection.** The smoke is untouched and runs to its
charter §5 deadline, **2026-08-29 09:00 KST**. This queue starts after collection completes.

The order is the PI's and is load-bearing: item 1 produces the frozen database that items 2, 3
and 4 all measure against, so a wrong or provisional N propagates into three sets of numbers.
Items are **not** to be run speculatively in parallel against the current slice.

**Standing rule for the whole queue: Bei proposes, the PI ratifies.** Items 1, 2 and 4 end in
options, not decisions. Item 3 ends in dossiers, not dispositions.

### Q1 — acquire and freeze the full CoRE MOF 2024 database

1. **Look locally first, and report what is there with counts** — prior-campaign archive,
   shared/group directories on the cluster. Report before pulling anything.
2. **If the full set is absent or its provenance is unclear**, pull the canonical release from
   the official CoRE MOF distribution. Record **release version, URL, and file hash** of what
   was pulled. Provenance-unclear counts as absent: a local copy nobody can name the release
   of is not a benchmark, and this study has already been bitten twice by inherited numbers
   whose basis turned out to be different from the one assumed (§3's 12.0/12.8 cutoff, `Lm 58`).
3. **Variant options go to the PI, not resolved silently** — ASR/FSR treatment, and which
   subsets are in scope. The slice's `[ASR]`/`[FSR]` twins are coordinate-identical under the
   chargeless protocol of §3, i.e. one structure under two filenames; at full-database scale
   that choice moves N, the naive exhaustive cost, and the provisioning footprint at once.
4. **Then freeze:** SHA-256 manifest in the frozen form, and report in one paragraph for the
   SI — **exact N, disk footprint, and source lineage**.

**Note for the freeze location, which Q1 must decide and the PI ratify.** The 1,731-CIF slice
is **git-tracked in this repo** (1,732 files, 30 MB, against a 16 MB `.git`). The full database
will not sit there comfortably, and `provision.py` copies every manifest line per workspace —
20 workspaces at full-database scale is the same multiplier applied to a much larger number.
Where the frozen database lives, and whether it is tracked or hash-pinned-and-external, is a
decision Q1 has to surface rather than settle by `git add`.

### Q2 — recompute the budget arithmetic at full-database scale

From **measured** per-structure costs (prior campaign: GCMC 1.83 CPU-h/structure at two
pressures; Zeo++ geometric screen 0.0048), propose:

- **Per-replicate CPU budget**, stating the **naive exhaustive cost at the frozen N** alongside
  it so the sub-brute-force constraint stays legible as a ratio and not just as a number.
- **Concurrency cap and fleet ceiling** preserving the **~1.8× headroom rule** — the invariant
  ruled twice already (Flag H at replicate scale, Flag I at fleet scale). The rule is the ratio
  to sustained concurrency, not the numerals 12 and 240; both were derived and both move if the
  compute budget or the horizon moves.
- **Cluster-capacity check attached** — total cores, current utilisation, and the measured
  displacement reading from `queue_depth.py` (others-waiting, not study share).

Options for ratification.

**Flagged in advance, because it changes what the clause means rather than what it says.** At
the slice, 1,600 CPU-h was 50.6% of the 3,162 CPU-h naive screen. At full-database N the same
budget is a small single-digit fraction, and §4 stops saying "you must triage" and starts saying
"enumeration is not available at all". See Rev 16.

### Q3 — re-run the integrity audit over the full database

Prepare **disposition dossiers** for new ambiguous or record-registering entries. **The
exclusion set seals before launch.** Bei does not dispose; the PI rules on each dossier.

Carried in: the audit instrument has been **wrong three times in the same way** — an anion, or
a neutral group, invisible to a presence-of-element test. Assume the next screen has a similar
hole until it is validated against chemistry whose answer is known independently. At
full-database scale the 1.7% imbalance base rate from the slice is a prior, not a prediction.

**Two open items in `STATE.md` are scoped to the slice and Ruling 1 re-homes them.** Open task 1
(the chained 3-structure answer-key action, blocked on cluster access) and open task 2 (the 23
entries awaiting a PI ruling from the full-slice sweep) were both raised against the 1,731 set.
Under Ruling 1 that set is **Cooper's future study's world**, not the main run's. Whether those
two items now belong to Cooper's answer key, to the main run's Q3 sweep, or to both, is a
question for the PI at Q3 and is not assumed here.

**Appendix A G3 must be re-derived, not carried over.** The standing concern was that G3's
density bounds (0.20–4.50 g/cm³) can mechanically remove the slice's operational excluded entry
pre-simulation, because it sits at **rank 3 of 1,731** by density. That rank is a property of
the slice. At full-database N the bounds, the rank, and the whole argument are recomputed from
scratch — the concern does not transfer and neither does the reassurance.

### Q4 — recompute the twin table at full scale

Confirm **provisioning size** and **manifest-verification time for 20 workspaces**. The last
real measurement was 1,731/1,731 verified per arm for 2 workspaces. Twenty workspaces at
full-database N is two multipliers at once, and provisioning is on the launch critical path.

### Q5 — rubric and analysis plan reworded per Ruling 2

- Tier (c) becomes **uniform study-level verification**: all headline numbers re-run, all
  claimed champions validity-audited, **identical procedure per trajectory**.
- Excluded-entry handling is recorded **descriptively**.
- **Answer-key file renames at seal**, under explicit PI instruction (`answer-key/` is opened no
  other way).
- **Confirm no provisioned replicate material references the exclusion set or the audit
  instrument.** Review the *provisioned output*, never the source — four leaks found so far,
  none visible in the source, two of them written by Bei into text whose purpose was preventing
  leaks. The word deny-list keeps its retired vocabulary and **gains** the new vocabulary; see
  Rev 16.

### Q6 — scoring-reference sequencing

The **exhaustive reference screen of the full database runs after main-run collection**, in the
scoring phase, under the pre-registered verification protocol. **Not before launch.**

**Seals pre-launch, and only these four:** the **manifest**, the **exclusion set**, the
**rubric**, and the **verification protocol**.

---

## S8. What Ruling 1 breaks that is not on the queue

Found 2026-08-28 while recording the ruling. Neither item is queue work; both are seal blockers.

1. **`config.SOURCE_ALLOWLIST["db_dir"]` / `["manifest"]` are phase-independent.** The main
   launch would provision 20 replicates with the smoke's 1,731-CIF slice, report `N/N verified`,
   pass its leak scan, and be wrong. Recorded in S6. Must be phase-keyed before launch; Q1
   supplies the target.
2. **§1 and §4's benchmark sentences are shared body prose, and the Rev 11 render filter only
   filters table rows.** Both sentences name the slice's N. Making them phase-correct needs a
   mechanism that does not exist yet — the phase filter will not do it, because these are not
   rows. Whatever is built must be verified across all four phase × arm renderings, as Rev 15
   was. Blocked on Q1/Q2 for the values; the *mechanism* is not blocked and can be built first.
