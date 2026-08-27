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

## S3. Token budget — 40 M stands, evidentiary note to be revisited

The 40 M figure stands on the basis stated in charter Rev 13. **SI-005 must be re-read at smoke
end**: its caveat was that one arm's burn measurement might be contaminated. It is now known to
be contaminated — SI-006 established that arm was blocked at a spend-limit modal, not working
at a low rate. **The smoke has produced one usable token-burn trajectory, not two.**

If the smoke ends without a second usable trajectory, the seal should record that 40 M rests on
a single replicate's burn, measured over ~1.7 days, one of which was an opening day.

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
campaign's maximum possible burn (**20 × 40 M = 800,000,000 billable tokens** for the main run).
Run 2026-08-28: **legs 1–2 PASS**.

Its third leg **cannot be automated** — Claude Code exposes no machine-readable spend limit —
and the script says so rather than skipping it silently. **Manual confirmation required before
seal:** confirm in the account's billing settings that either no monthly spend limit is set, or
the limit exceeds 800 M tokens' worth of spend with margin, and record the confirmation here.

- [ ] *(unchecked)* Spend limit confirmed to exceed the fleet ceiling with margin — PI, date:

## S6. Main-run launch gaps found while wiring headless mode — not blocking today, blocking at launch

- **`launch_sessions.sh` iterates a hardcoded `for REP in s01 s02`.** It cannot launch the main
  fleet as written. The phase-selected loop, the deadline read, the credential-clean environment
  and the growth-based proof of life are all correct and reusable; only the replicate list is
  wrong. Must be driven from `config.RATIFIED["phases"][phase]["ids"]` before the main launch.
- **`poll.sh`, `restart_watch.sh` and `collect.sh` carry the same hardcoded pair.** Same fix,
  same place to make it.
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
