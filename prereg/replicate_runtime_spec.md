# Replicate runtime specification — smoke phase

**Status: PROPOSED where marked. One item needs a PI ruling before launch** (§1, host
placement), because it changes what "workspace" denotes in charter §1 and §4.

Filed by Bei, 2026-08-26. Every environment fact below was measured, not assumed.

---

## 1. Host placement — **PI ruling needed**

### The constraint that forces the question

Claude Code requires Node 18+. Node 18+ requires **glibc ≥ 2.28**.

| Host | OS / glibc | Node | tmux/screen | Workspace visible | Scheduler | Outbound HTTPS |
|---|---|---|---|---|---|---|
| **`bnode0`** (cluster head) | CentOS 7.6, **glibc 2.17** | none — `/usr/local/hpc/bin/node` is an HPC Korea *node-selector* utility, not Node.js | tmux + screen | ✅ `/home1/users/Bei/ws/` | ✅ PBS + `qas` | ✅ (HTTP 405 from the API endpoint) |
| **`bronze3`** (gateway) | Ubuntu 20.04, glibc 2.31 | none installed | screen only | ❌ `/home1` and `/home/users` **not mounted** | ❌ none | ✅ |
| **This Mac** | macOS 14.5 | **v24.19.0**, Claude Code **2.1.233** | screen only (**no tmux**) | via `ssh dirac-bei` | via `ssh dirac-bei` | ✅ |

**`bnode0` cannot host the sessions.** glibc 2.17 is two major versions below Node 18's floor,
and Node 16 — the last release supporting 2.17 — is below Claude Code's floor. There is no
version of Node that satisfies both. `bronze3` could run Node but cannot see the workspace or
the scheduler, and is 93 % full.

**So the sessions must run on this Mac**, reaching the cluster through the `dirac-bei` alias.

### What that costs, and the ruling required

The replicate's *process* is local while its *workspace* is remote. Two readings, and they
differ in what charter §1 and §4 denote:

- **(A) Workspace is the cluster directory.** `workspace_root = /home1/users/Bei/ws/<id>`, and
  every replicate action is an `ssh dirac-bei` call. Faithful to the charter as written; the
  database, toolchain and record all sit together where the compute is. Cost: every file
  operation crosses the link, and a dropped connection interrupts work mid-action.
- **(B) Workspace is local, cluster directory is compute scratch.** The governed record and
  the database live on the Mac; jobs and their outputs live on the cluster. Cost: **the record
  is split across two machines**, and charter §6's "every number traces to a commit and a job
  ID" spans a boundary — which is exactly the seam where provenance goes missing.

**Bei recommends (A)**, on the grounds that §6 traceability is the charter's load-bearing
property and (B) puts a machine boundary through the middle of it. But this is a
charter-denotation decision, not an infrastructure default, so it is the PI's.

*(All provisioning to date assumes (A): `workspace_root` in both `WORKSPACE.json` files
already reads `/home1/users/Bei/ws/<id>`.)*

## 2. Session persistence

**`tmux` is not installed on this Mac; `screen` is.** Both are present on `bnode0`, but
`bnode0` cannot host the session, so that does not help.

- **Proposed:** one detached `screen` session per replicate, named `rep-s01` and `rep-s02`.
  `screen -dmS rep-s01 …`, reattach with `screen -r rep-s01`.
- Installing `tmux` (e.g. `brew install tmux`) is a one-line alternative if the PI prefers it;
  Bei has not installed software on the PI's machine unasked.
- Each session's scrollback is logged to `harness/sessions/<id>.log` via `screen -L`, so the
  session transcript survives detachment and death.

## 3. Restart-on-death policy — **PROPOSED**

A replicate's campaign is 3 days; a session that dies at hour 4 and is not restarted produces a
finding about the harness, not about the replicate.

- The watchdog already tracks liveness via `<ws>/heartbeat` with a 30-minute staleness
  threshold. Proposed: **restart automatically when the heartbeat is stale AND the `screen`
  session is gone.**
- **Restarts are capped at 3 per replicate per campaign.** On the 4th death the replicate is
  left down and the PI is notified — repeated death is a fact about the run, and papering over
  it with unlimited restarts would hide it.
- **Every restart is an event on the record**: appended to `harness/restarts.jsonl` with
  timestamp, replicate, death detection reason, and elapsed downtime, and mirrored into the
  replicate's `INBOX.md` so the replicate knows it was restarted and can reason about the gap.
- **The workspace is never reset on restart.** The git record, `usage.json` and any running
  jobs survive; the replicate resumes from its own `STATE.md`. Budget counters continue — a
  restart is not a fresh allowance.
- **Deadline does not extend.** Charter §5's `T` is wall-clock; downtime is the replicate's
  loss and is visible in the record. Extending it would make the two arms incomparable if they
  crashed different numbers of times.

## 4. Pinned model string — **PROPOSED**

- **`claude-opus-5`**, Claude Code **2.1.233** — the same model family and CLI version the
  prior campaign ran throughout, per its `SESSIONS.md`.
- Recorded per session, and **pinned for the campaign's duration**: the prior campaign's own
  standing note is the reason — *"a change in it is a change in the instrument, and a result
  that moves across a model change should not be attributed to the science until that is
  excluded."* Both arms must run the same string, or the arm comparison measures the model
  rather than the gates.

## 5. Token metering into the ratified 12 M budget — **PROPOSED**

**Basis (already ratified):** `input + output + cache_creation`. **Cache reads excluded.**

- **Source:** Claude Code writes per-message `usage` records to
  `~/.claude/projects/<project-path>/*.jsonl`. This is the same source Bei used to measure the
  prior campaign's burn (31.0 M over 11 days, 5.73 M peak day), so the budget and the meter are
  derived from the same instrument — the number the budget was set from is the number the
  meter will report.
- **Mechanism:** a metering pass sums `input_tokens + output_tokens +
  cache_creation_input_tokens` across each replicate's transcripts and writes `tokens` into
  `<ws>/usage.json`, which the watchdog already reads and thresholds at 75 % / 100 %.
- **Cadence:** every watchdog poll — **10 minutes** for the smoke (§ ratified). Worst-case
  overshoot between polls is bounded the same way compute is.
- **Compute metering is separate and authoritative from PBS**: `tracejob`
  `resources_used.cput` per job, not self-reported. Currently `usage.json` trusts the
  replicate's own ledger; wiring `tracejob` closes `harness/README.md` limit 2 and should be
  done before launch.

## 6. Isolation limit — stated, not solved

**Both replicates run as the same Unix user `Bei`**, so each can read the other's workspace and
Bei's home, and can `chmod u+w` the read-only toolchain it owns. Charter §4's *"reading or
writing outside your workspace is prohibited and audited"* is, on this cluster, **enforced as a
rule and audited for traces — not prevented.** Genuinely preventing it requires separate cluster
accounts or containers, neither of which exists today.

This is not necessarily a smoke blocker: whether a replicate respects a boundary it could cross
is itself observable, and arguably worth observing. But it must not be described as isolation.
