# REPORTS — Bei to PI

*Append-only. Newest entry at the bottom. One entry per report; entries are never edited after
they are pushed, and a correction is a new entry that names the one it corrects.*

*Established 2026-08-30 by PI addendum: all reporting goes through this file, because the PI reads
this record on GitHub and cannot copy text out of the operator's terminal.*

---

## 2026-08-30T01:14:31Z (10:14:31 KST) — REPORT 001, preliminary. FLEET STILL PAUSED. Held for go.

> **In one line:** the fleet is down and safe, the spend cap would have silently reopened at $0.00
> on this host and now carries $725.47 forward (not the $714.94 of record), and bronze4 cannot yet
> host a resume at all — no `screen`, no `dirac-bei`, and no scheduler to replace macOS launchd.

**Status: HOLDING.** `harness/resume_fleet.sh` has **not** been run, in any form, in either
dry-run or live mode. No session has
been resumed, no daemon has been started or loaded, nothing has been `ssh`'d to the cluster.
`harness/state/PAUSE.json` is in place and untouched, so `restart_watch.sh` and `divergence.py`
remain stood down. This entry is written before the resume, as instructed, and the fleet stays
down until an explicit go.

### 0. What this report is written from, and what it is not written from

This host **is bronze4** — `hostname` bronze4, Ubuntu 24.04.4 LTS, Linux x86_64. It has **no
prior state for this study**: the working copy was cloned from the remote today at commit
`71ecc9c`, and everything below comes from reading that record — `STATE.md`, `LOG.md`, `harness/`,
`harness/state/`, `harness/spend.jsonl` — plus arithmetic and host checks run against it today.
There was no earlier session on this machine, so nothing was "already armed": the resume described
in §2 is armed **by the repository**, in the sense that it is one committed command that will run
end to end when invoked, not by any preparation carried over from before. The spend-meter patch in
§3 was written today and is described exactly as it stands.

**The most important thing in this report is not the spend gap.** bronze4 is not yet able to host
the fleet, and I established that by inspection rather than by trying: `screen` is not installed,
and the cluster alias `dirac-bei` does not resolve. Run today, the resume would abort at its first
cluster read with nothing changed. Details in §2; the readiness gap is §4(c) and §4(g). The hold
is therefore also, at this moment, a technical necessity and not only an instruction.

---

### 1. The study's state as I understand it from the record

**Phase.** Pre-seal, main phase, **N = 16 (8 gated / 8 ungated)**, 7-day horizon, charter Rev 20
applied (Rev 21 pending delivery, see below). Budgets per replicate: 1,610 CPU-h, 32 M tokens,
and a **US$280 spend cap** — spend being the budget the record says actually binds, because the
ratified token basis excludes cache reads and cache reads were 59.2 % of the smoke's real bill.

**The fleet is deliberately paused, not failed.** Sixteen replicates stopped by PI ruling at
2026-08-30 07:14:19 KST (`harness/state/PAUSE.json`), all confirmed down at 2026-08-29T22:35:50Z.
Reason of record: supervision host unavailable. Because the replicate *processes* run on the
supervising machine and only their *workspaces* live on the cluster, an offline host is an offline
fleet; `bnode0` at glibc 2.17 cannot host sessions, so there was no cluster-side fallback. Cluster
jobs were **never touched** — nothing was `qdel`'d, and outputs have been accumulating in the
workspaces for pickup at resume.

**The old host is being retired; the fleet's new home is bronze4 (KAIST)**, bootstrapping from
this repository.

**Three defects were found and corrected while paused**, all in the restart path:
`restart_watch.sh` relaunched with no argument and so defaulted to `PHASE=smoke` and the `s01 s02`
roster — meaning **rep06 died once at 12:36Z on 2026-08-29 and was never restarted**, while three
cap-consuming "restarts" went to two other replicates; `stamp_deadline.py` re-stamped
`now + campaign_hours` unconditionally, silently extending the campaign of anything the restart
path touched (caught live on rep06, +11.3 h, reverted to `2026-09-05T19:41:02.832166+09:00`); and
a **pause guard** now stands the watcher and the divergence panel down while `PAUSE.json` exists,
without which the first poll thirty minutes into the pause would have relaunched all sixteen on
an unattended machine.

**Registry.** s01/s02 are **archived, not down**; roster 18 → 16; the A/B divergence panel is
retired in `STATUS.md` and the sealed arm map in `harness/divergence_map.SEALED.json` is
**unopened and stays sealed**. `prereg/` and the phase rosters are deliberately not edited.

**Rev 21 is not fleet-uniform.** Measured: **rep01 is the only replicate holding a pre-Rev-21
Appendix A** (still carrying the stale `0.313 g/cm³`); the other seven gated replicates got Rev 21
as provisioned text; all eight ungated charters contain zero Appendix A, and that omission *is*
the treatment. So the Rev 21 answer goes to **rep01 alone** — delivering it fleet-uniform would
push Appendix A material into the arm defined by its absence, which is the SI-016 leak shape and
unrecoverable. The budget ruling and the infrastructure facts **are** fleet-uniform, all sixteen.

**Not moving while paused, and blocking the seal, not the resume:** the Q1 world choice is stopped
on a fired contingency (2,811 list members missing locally, 56× the threshold; the "student
assistance" delivery turned out to be the old share ∪ SI-zip CR, byte-identical, gap closed = 0),
Q2 is blocked behind it, and the open seal blockers SI-012/013/014 and the rubric work stand as
recorded. None of that is touched by a resume; I flag it only so the report is not read as saying
the study is otherwise clear.

---

### 2. What the armed resume will do when it is executed

`./harness/resume_fleet.sh` is one command and it enforces its own order. In sequence:

1. **Refuses if there is no pause record.** No `harness/state/PAUSE.json` → exit 1, nothing done.
2. **`resume_fleet.py`, in two passes, aborting as a whole.** Pass 1 reads each replicate's live
   `deadline_kst` off the cluster (`ssh dirac-bei`, `/home1/users/Bei/ws/<rep>/WORKSPACE.json`) and
   compares it to the value recorded in `PAUSE.json`. **Any mismatch aborts before a single write**
   — an unexplained edit is not ratified by extending it. Pass 2 then extends **all sixteen by the
   same measured wall-clock interval**, `new = deadline_at_pause + (resumed_at − paused_at)`.
   Nothing re-derives a deadline from `now + campaign_hours`. As of this report the pause stands at
   **~3.0 h** and still running; the actual figure is whatever is measured at the moment of go.
3. **One identical INBOX note per replicate** — infrastructure event, not a judgement, uniform
   across arms, no arm-dependent content, stating the exact extension and the new deadline, and
   telling each replicate its cluster jobs were never cancelled and results may be waiting.
4. **Restart counters reset** by appending a `COUNTER_RESET` marker to `harness/restarts.jsonl`.
   Append-only; nothing is deleted. This is what clears rep06's `3/3`, a cap it reached entirely
   through restarts that never touched it.
5. **Stop files cleared** (`harness/sessions/<rep>.stop`) — until this happens a relaunched loop
   exits immediately.
6. **Prepared escalation answers delivered *before* relaunch**, so the notices are already in
   `INBOX.md` when each agent boots and reads it rather than arriving mid-turn:
   `harness/escalation_answers/NOTICE_fleet_uniform.md` to all sixteen, and
   `NOTICE_rep01_rev21.md` to **rep01 only**.
7. **Relaunch, per replicate, through the corrected path** — each replicate's own id and its own
   phase resolved via `config.phase_of()`, with `stamp_deadline.py` now idempotent so the launch
   **preserves** the extended deadline instead of overwriting it.
8. **The pause record is retired LAST, and only on full success.** Any replicate that fails to
   come up leaves `PAUSE.json` in place, which leaves the restart watcher stood down rather than
   half-armed against a half-up fleet, and exits non-zero.

`./harness/resume_fleet.sh --dry-run` prints the roster and the pause duration and changes nothing.
I have not run either form.

**What it would actually do on bronze4 today: abort at step 2, having changed nothing.** The two
preconditions the script assumes and does not check are both properties of the host, and both are
currently unmet here:

- **`dirac-bei` does not resolve** on this host (`Could not resolve hostname dirac-bei`; there is
  no `~/.ssh/config` entry). Pass 1 reads sixteen live deadlines over that alias, so the first
  read fails and `resume_fleet.py` exits with *"cannot read deadline for rep01 — aborting before
  any change."* **This is the design working**: no deadline is extended, no notice is delivered,
  no counter is reset, `PAUSE.json` stays in place and the restart watcher stays stood down.
- **`screen` is not installed** (`apt` offers 4.9.1-1ubuntu1; installing needs root). Even past a
  working ssh alias, `launch_sessions.sh` starts every session under `screen -dmS` and both it and
  `resume_fleet.sh` prove liveness with `screen -ls`. All sixteen would report `LAUNCH FAILED`,
  the resume would exit 1, and — again by design — `PAUSE.json` would be **left in place** rather
  than retired against a fleet that is not up.

What *is* present and correct here: `node v18.19.1` (clears the Node 18 floor that ruled out
`bnode0`), the `claude` CLI at `/usr/local/bin/claude`, and `python3`. `qstat`/`qsub`/`qas` are
absent locally, which is expected and not a defect — `poll.sh` reaches the scheduler over `ssh
dirac-bei`, not locally.

---

### 3. Closing the spend-baseline gap — with the verified totals

**The gap.** `harness/meter_spend.py` derives every replicate's spend from transcripts under
`~/.claude/projects/<mangled-local-cwd>/` on the machine it runs on, and `tally()` **recomputes**
the total from those files rather than reading the accumulated `harness/spend.jsonl`. On a new
host those directories are empty. Unpatched, the first meter tick on bronze4 reports **$0.00 spent
and a full $280 available for every replicate**, against spend already incurred. The cap does not
fail loudly; it silently reopens. Nothing in the resume path touches spend, so this is not covered
by the standing resume orders.

**The verified baseline.** The record's preserved figure is **$714.94** (`fleet_spend.json`,
`STATE.md`, `LOG.md`). Recomputed today from the append-only ledger, the correct carried figure is

> **$725.47 of $4,480 (16.2 %), 16 replicates** — not $714.94 / 16.0 %.

`fleet_spend.json` was stamped **2026-08-29T22:24:19Z**, and the fleet was not confirmed fully down
until **22:35:50Z**. Sixteen sessions were still winding down across those 11.5 minutes.
Reconstructing the ledger by timestamp: $704.18 at the pause stamp (22:14:19Z) → **$714.94 at the
summary stamp** (which is exactly the recorded figure, so the summary is a correct reading of the
wrong moment) → **$725.47 by 22:35:14Z**, and then **flat** through every later row to the final
one at 00:46:19Z. Per-replicate verified totals:

| rep | carried $ | rep | carried $ | rep | carried $ | rep | carried $ |
|---|---|---|---|---|---|---|---|
| rep01 | 65.14 | rep05 | 32.93 | rep09 | 37.28 | rep13 | 35.86 |
| rep02 | 40.13 | rep06 | 99.03 | rep10 | 75.59 | rep15 | 49.07 |
| rep03 | 23.79 | rep07 | 50.55 | rep11 | 38.74 | rep16 | 49.34 |
| rep04 | 30.57 | rep08 | 40.08 | rep12 | 36.91 | rep17 | 20.45 |

**Prepared, not yet ratified, and not yet committed to the fleet's behaviour:**

- **`harness/make_spend_baseline.py`** (new) derives `harness/state/spend_baseline.json` from
  `harness/spend.jsonl` — the append-only ledger — restricted to the paused roster, so the smoke's
  $178.48 is excluded by construction. It carries **token counts, not dollars**, so cost keeps
  being computed from `config.RATIFIED["price_per_token"]` in exactly one place and a future rate
  change does not have yesterday's prices frozen into it. It **refuses to write** a baseline that
  does not reproduce the ledger row it came from (±$0.01) or that is missing any replicate.
- **`harness/meter_spend.py`** (patched) loads that file when `"active": true`, adds the carried
  tokens to the local tally before costing, and meters a replicate **even when its local transcript
  directory does not exist yet** — otherwise the first fleet total on bronze4 would silently omit
  every replicate that had not yet written a line. Output now shows the split
  (`$0.00 on this host + $65.14 carried forward`), and `local_usd` / `carried_usd` are recorded in
  every ledger row.
- **A double-count guard, because the record offers two fixes and they must not both be applied.**
  If the transcript directories are carried across with the repo, the local tally already contains
  the baseline and adding it would charge every replicate twice. So if a replicate's local tally
  already covers the baseline in **all four** token classes, the meter **exits with an error**
  rather than metering. Deactivating is one field: `"active": false`.

**Verified today, on bronze4 itself** — so this is the real condition, not a simulation of it
(`~/.claude/projects/` holds nothing for this study): with the baseline active the meter reports the sixteen replicates at **$725.47 / $4,480,
all `OK`, none at warn**; with it inactive it reports nothing at all, i.e. byte-for-byte the
pre-patch behaviour. The guard fires on a covered local tally and stays quiet on a half-covered or
empty one. `./harness/selftest.sh` gives **87 PASS / 1 FAIL** — and gives the **same 87/1 on a
pristine tree with the patch reverted**, so the failure predates the patch and the patch is
neutral to the suite. That one failure is itself a finding; see §4(e).

**PI decisions this needs before it binds:**

1. **Which number carries — $725.47 (ledger, verified) or $714.94 (summary, of record)?** I
   recommend **$725.47**: it is the one supported by the append-only ledger, and the difference
   is $10.53 of headroom that would otherwise be silently granted back to the fleet. Nothing has
   been changed in `fleet_spend.json`; correcting a summary is a PI call, not mine.
2. **Baseline carry vs. transcript carry.** I recommend the baseline, because it travels in git
   and is auditable; the transcript directories are 16 sessions of raw records that have never
   been part of this repository. Whichever is chosen, the other must be off.
3. **Ratification.** The patch is written and tested; it is not merged into the resume path and
   the meter will not be scheduled by me. It changes what sixteen replicates are told about their
   remaining budget, so it is a change to a binding instrument.

---

### 4. What in the record I would question

**(a) The preserved baseline is stale by $10.53, and two documents repeat it.** As above.
`fleet_spend.json` reads the ledger at 22:24:19Z and `STATE.md` and `LOG.md` both carry $714.94
forward as *the* preserved figure. It is not wrong arithmetic; it is a correct reading taken
11.5 minutes early. Flagged rather than fixed.

**(b) The last commit message overstates what the meter did, and that may be why (a) stands.**
`71ecc9c` records the spend meter as "metering sixteen stopped sessions and dirtying the record".
The meter did keep firing on its 120 s interval until 00:46:19Z — but the **totals stopped moving
at 22:35:14Z**, before the fleet was confirmed down at 22:35:50Z, and every later row is an
identical re-tally. So those rows are idempotent, not spurious: nothing was dirtied, and the $10.53
above them is **real spend by live sessions**, not phantom charge. The distinction matters because
the "dirty" framing is a reason to discount the ledger's later rows, and the ledger's later rows
are the correct baseline.

**(c) The scheduling layer does not travel, and on bronze4 it is now measured, not conjectured.
I would rank this above the spend-baseline gap.** `harness/launchd/*.plist` are macOS launchd jobs
with paths hardcoded to `/Users/jihankim/replicate-study`. bronze4 is Ubuntu: **`launchctl` does
not exist here** (`systemctl` and `crontab` do), and the string `bronze4` appears **nowhere in the
repository except prose in `STATE.md` and `LOG.md`** — no host config, no path variable, no
equivalent unit. So on a resumed fleet, **nothing would schedule the spend meter and nothing would
schedule `poll.sh`**. That is SI-012 recurring exactly: the defect that let the watchdog run 2
cycles of an expected 393 and cost 2,452 CPU-h past a stop nobody read, and whose recorded fix —
"launchd, not cron" — is a macOS sentence that no longer has a referent.

It also removes the premise of the launch gate. `LAUNCH_GATE.md` passes $280 under the $4,500
limit **only because spend polls locally every 2 minutes** (fleet maximum $4,491, $9 spare); at a
30-minute cadence the overshoot alone is $168 and $280 does not fit, and with no scheduler at all
the polled bound does not exist. **The §3 patch makes the meter tell the truth; it does nothing to
make the meter run.** A carried baseline that is never re-read is a correct number nobody checks.

**Recommendation, for ratification, not applied:** two `systemd` timers replacing the three plists
— `study.spend` at 120 s and `study.poll` at its 10-minute cadence — each with **`Persistent=true`**,
which is the Linux equivalent of the property the record chose launchd *for*: a missed interval
fires on resume instead of being silently dropped. **`cron` remains the wrong answer here for the
same reason it was on macOS**, and the poll wrapper's own comment says so. I have written no unit
file and loaded nothing; whether the harness runs as a user or system service on bronze4, and
whether this host suspends the way the laptop did, are decisions about a machine the study has not
yet described anywhere in its record.

**(d) The resume tells sixteen replicates something the unpatched meter would contradict.**
`resume_fleet.py`'s INBOX note says, verbatim, *"Your compute, token and spend budgets are
unchanged."* Delivered from an unpatched host, that sentence is false at the moment it is written:
the spend counter would read $0.00 of $280. The patch in §3 makes it true again. Sequencing point:
the notice is delivered in step 3, before any meter tick, so the ordering cannot rescue it.

**(e) `selftest.sh` asserts against machine-local state that does not travel.** The case
*"positive evidence does authorise"* (`selftest.sh:196`) runs `liveness.py s01 --dead-after 0` and
expects exit 0. On any host without the retired laptop's transcript directories, `liveness.py`
correctly answers *"no positive evidence of death (no transcripts)"* and exits 1 — so the suite
reports **87 PASS / 1 FAIL** here and will do the same on bronze4. This is the same root cause as
the spend gap: harness truth keyed to `~/.claude/projects` on one machine. The comment directly
above that line records this exact lesson being learned for the *live* case, which was moved to a
`selftest_live` fixture; the *death* case was left pointing at the real s01. Same fix available.
Related and smaller: `STATE.md` item 18 records the suite at **84 PASS**; this tree runs 88 checks.

**(f) rep06 lost 9.6 hours that the uniform pause extension does not restore, and I do not think
that should be settled by default.** rep06 died at 12:36Z on 2026-08-29 and was never restarted —
its spend total is flat from 12:37:21Z, which corroborates the record from a third direction. From
its death to the pause stamp is **9.62 h** of campaign time lost to a harness defect, not to
anything rep06 did. The pause extension is uniform by design, and rightly so: it protects arm
balance. But it compensates the pause, not the outage, so on resume rep06 restarts with the same
deadline arithmetic as fifteen replicates that were up. Compensating rep06 individually would
break the uniformity the design exists to preserve; not compensating it leaves one replicate with
~9.6 h less worked time than its arm-mates, from a cause internal to the harness. **Either way it
should be a recorded ruling rather than a silent default**, and it is a PI call, not mine. I raise
it now because after the resume the moment to decide it cleanly has passed.

**(g) Host provisioning for bronze4 is not written down anywhere.** The resume needs the
`dirac-bei` ssh alias, key-based `BatchMode` access to `/home1/users/Bei/ws/<rep>`, and `screen`;
none is present (§2), and nothing in `harness/` or `prereg/` states what a supervision host must
provide. The retired laptop's configuration was never part of the repository, so it did not
travel. This is the same shape as (a), (c) and (e): **truth that lived on one machine rather than
in the record.** Worth one short document, `harness/HOST_REQUIREMENTS.md`, written once from this
migration while the gaps are visible.

**(h) Smaller.** `launch_sessions.sh:127` closes with `grep -E 'rep-s0'` — a smoke-era session-name
filter. Launch sixteen main replicates successfully and the summary line still prints `(none)`.
Cosmetic, but it is the third instance of the family the record already fixed twice (`collect.sh`'s
two-workspace glob, `restart_watch.sh`'s defaulted smoke roster): **a smoke-era literal left in a
main-phase path, reporting success against the wrong subject.**

Roster consistency I did check and it is clean: `config.RATIFIED["phases"]["main"]`,
`PAUSE.json` and `harness/state/active_replicates` are the same sixteen ids in the same order, and
rep14 is correctly absent as reserved second-wave.

---

**Holding for go.** A go alone is not currently sufficient — the resume would abort safely on the
missing ssh alias — so the order I would follow is:

1. **Make bronze4 a host**: `screen` installed, the `dirac-bei` alias and key configured for
   non-interactive use, `ssh dirac-bei true` verified. Root is needed for the first; the second is
   credential work I should not do unattended.
2. **Ratify or reject §3** (which baseline number carries; baseline vs. transcript carry).
3. **Rule on §4(c)** — the fleet should not be resumed into a state with no scheduler, since that
   is the SI-012 condition by construction. Timers first, or an explicit ruling that the first
   interval runs unwatched.
4. **`resume_fleet.sh --dry-run`**, and report the measured pause duration here.
5. **Resume**, verify all sixteen up, meter once against the carried baseline, and report again.

I will not run the resume, deliver any notice, install anything, touch a credential, or load any
scheduler until told. **§4(f) — rep06's uncompensated 9.62 h — wants a ruling before step 5, not
after.**

— Bei (harness)
