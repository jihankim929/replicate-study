# LAUNCH GATE — 6-hour rehearsal on replicate #1

**Ruled by the PI, 2026-08-29.** Replicate #1 is **a fleet member, not a throwaway**: it launches
under the sealed arm assignment, its workspace is the real one, and if the gate passes its run
continues into the main campaign rather than restarting. The gate is a *hold*, not a rehearsal in
a sandbox.

**Sequence.** On the PI's seal commit → launch replicate #1 → run the gate **6 h** → report
pass/fail **per assertion**. **On pass:** launch the remaining 19 the same day. **On any fail:**
halt, report, fix, re-gate. No partial launches.

**Why a gate exists at all.** Every serious defect this study has found was invisible until
something real ran: the watchdog that had never been invoked (SI-002), the meter that undercounted
19× (SI-001), the modal that blocked an agent for 39 h while every signal above the TUI reported
health (SI-006), the collector that would have scored a compliant report as missing (SI-010), the
gate whose correct reading deleted 35.8% of the database (SI-015), and the scheduler that never
existed (SI-012). **The dry run found none of them.** Six hours of one real replicate is the
cheapest instrument this study has for the class.

---

## The assertions

Each is pass/fail, each is checked against evidence rather than expectation, and **each names what
it would have caught**. A `SKIP` is a fail.

### A1 — Headless start, with transcript growth ≤ 120 s

`session_loop_headless.sh` starts replicate #1 with `-p`, and the agent's transcript **grows
within 120 s of launch**.

- **Evidence:** transcript file size at t+0 and t+120 s; `liveness.py` reports `alive` on the
  transcript-growth basis (SI-003), not on a heartbeat.
- **Catches:** a start that produces a process but no work. `-p` has **never run a full
  replicate** (SI-011) — this is its first real use, and the smoke's launch produced three
  separate defects in its first hour.

### A2 — Billing preflight passed

`preflight_billing.sh` returns clean **before** the agent is started, and the account has headroom
for the phase.

- **Evidence:** preflight exit code and its recorded reading.
- **Catches:** SI-006 exactly — *"You've hit your monthly spend limit"*, which cost the smoke
  39.16 h of one arm (59.7% of its campaign) while the screen session, the heartbeat wrapper and
  every signal above the TUI reported health.

### A3 — Manifest verified **in-workspace**, 12,499 / 12,499

Inside the provisioned workspace, `sha256sum -c` against the frozen `MANIFEST.sha256` returns
**12,499 of 12,499**, zero mismatches, zero missing.

- **Evidence:** the verification output from inside the workspace, not from the frozen source.
- **Catches:** a provision that copied the wrong world, or copied it incompletely. The manifest
  **is** the published membership definition under the world ruling, so a workspace that does not
  match it is not running the study's benchmark. Also catches the phase-independent
  `db_dir`/`manifest` defect recorded in `seal_notes.md` S8, which would have provisioned the main
  fleet with the smoke's slice **while reporting `N/N verified`**.

### A4 — First job submitted and completed

Replicate #1 submits at least one real job and at least one job **reaches completion** with
output on disk.

- **Evidence:** job id, `JOBS.md` entry, the run directory's output, and the job leaving `qstat`.
- **Catches:** the `qas` interface defect found 2026-08-29 — `qas` is **not on a non-interactive
  PATH** (it is at `/usr/local/mjs/qas`) and **takes the qsub file as its first positional
  argument, accepting no flags**. `harness/dirac.py` had both wrong and had **never been
  executed**; `launch.sh` calls nothing in it, so the first main-run submission would have been
  its first run. Corrected 2026-08-29; this assertion is what proves the correction.

### A5 — Meters nonzero and consistent

After the first completed job, **both** meters read nonzero, and the two compute bases are
present and explicable.

- **Evidence:** `usage.json` carries `cpu_h` (job-records basis), `cpu_h_scheduler`, and `tokens`,
  all > 0; `token_daily.jsonl` has a row for replicate #1.
- **Catches:** SI-001 (the scheduler basis undercounted 19×, and is retained only as evidence)
  and the staleness found at collection — `usage.json`'s token figure was **−36.5%** for one smoke
  arm and **−50.5%** for the other, because the meter only ran inside a poll and polling had
  stopped.

### A6 — launchd watchdog fired **every cycle, on schedule**

Across the full 6 h, `harness/poll_fires.jsonl` shows a fire for **every** scheduled interval,
including any interval that spans a host sleep.

- **Evidence:** fire timestamps vs the `StartInterval`; the count of intervals with **no** fire
  must be **0**; cross-referenced against `pmset -g log` sleep transitions in the same window.
- **Catches:** SI-012, the largest harness defect the study has found. The watchdog ran **2 cycles
  of an expected 393** across the whole smoke and was silent for the final **49.05 h**, because
  **nothing ever scheduled `poll.sh`** — no crontab, no agent, no loop. The consequence was
  arithmetic: the ratified overshoot bound of 8.33 CPU-h became **2,452 CPU-h**, a **294×**
  understatement, and one arm finished **456.75 CPU-h past its cap**.
- **Why launchd and not cron:** macOS runs a missed `StartInterval` on wake; cron drops it. On this
  host during the smoke: **154 sleep transitions, 32.00 h suspended (48.8% of the campaign), and
  111 stretches longer than the poll interval.** cron would have dropped 111 cycles. **This
  assertion is the one that must be observed across a real sleep, not argued.**

### A7 — Escalation file writable

`ESCALATIONS.md` exists in the workspace and the agent can append to it; a test line written by
the harness is picked up by `escalate_remote.sh` on the next poll and acknowledged in `INBOX.md`.

- **Evidence:** the round trip, end to end, with timestamps.
- **Catches:** SI-013 — three escalations aged **24.84 h unanswered to the deadline** with **zero**
  acknowledgements and **zero** records in either harness ledger, because the router only runs
  inside a poll. Note that under the rewritten §8 the channel no longer promises an answer; it
  still promises to **log and read**, and this assertion is what makes that promise true.

### A8 — Zero dialogs possible

No interactive modal can be drawn for replicate #1.

- **Evidence:** `-p` confirmed in the running process's arguments; the settings allow-list in
  force; a deliberate limit-triggering condition **exits non-zero and is logged by name** rather
  than blocking.
- **Catches:** the SI-011 class — *"an interactive modal halts an unattended agent while
  everything above the TUI reports health"*. Three instances so far (a permission dialog, a
  settings dialog, the spend-limit modal), each previously fixed **as a specific dialog**. The
  class is not enumerable, so this assertion tests **unreachability**, not detection.

### A9 — The record is being kept

By t+6 h replicate #1 has committed at least once, and `LOG.md`, `STATE.md` and `JOBS.md` exist
and are non-empty.

- **Evidence:** `git log` in the workspace; the three files.
- **Catches:** a replicate that works but does not record, which §6 forbids and which no other
  assertion here would notice.

---

## Reporting

One line per assertion: **PASS / FAIL**, the evidence, and the measured value where there is one.
**Partial passes are fails.** The report goes to the PI before any further launch.

**On any fail: halt.** Do not launch the remaining 19, do not "fix forward" during the gate, and
do not re-run the gate on a replicate that has already consumed budget under a broken
configuration — re-provision, then re-gate.

## What this gate does not cover, stated rather than implied

- **It does not test the 10-day horizon.** Six hours cannot surface a defect whose period is
  longer than six hours. The token cap, the compute cap and the §5 deadline are all outside it.
- **It does not test the fleet.** Replicate #1 alone cannot exercise the fleet ceiling, queue
  crowding, or the account-level limits that SI-006 arose from — and account limits are
  **precisely** the thing that scales with N. The 20-replicate launch is the first test of that,
  and it has no gate.
- **It does not test scoring.** Nothing here exercises the rubric, the reference screen, or the
  verification protocol.
