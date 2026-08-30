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

---

## 2026-08-30T01:44:14Z (10:44:14 KST) — REPORT 002, on executing the ruling. FLEET STILL PAUSED. Held for go.

> **In one line:** every ratified item is executed, committed and pushed — the spend correction is
> appended rather than edited, the schedulers are installed and **observed firing on exact
> calendar boundaries**, rep06's 9.62 h is restored in the arithmetic and in its own notice, and
> the suite is **88 PASS / 0 FAIL**. `screen` has since appeared on bronze4; **`dirac-bei` still
> does not resolve**, so the ordered dry-run has not been triggered and the fleet stays down.

**Status: HOLDING.** `resume_fleet.sh` has not been run in live mode. `PAUSE.json` is untouched.
No session resumed, no notice delivered, nothing `ssh`'d to the cluster. Pause duration at the
time of writing: **3.4984 h**, still running.

### 1. The ruling, item by item

| Ruling | Done | Commit |
|---|---|---|
| **(1)** $725.47 carries; correct `fleet_spend` by appending | `harness/state/fleet_spend.jsonl` carries a `CORRECTION` entry naming the superseded $714.94, its 22:24:19Z stamp, the $10.53 delta and why the delta is real spend. **`fleet_spend.json` is byte-for-byte unedited** — verified against git. | `be3606e` |
| **(2)** Baseline carry; activate the patched meter | Active. Verified on bronze4: **$725.47 / $4,480 (16.19 %)**, sixteen replicates, all `OK`, none at warn, each line showing `$0.00 on this host + $X carried forward`. Recomputed independently from the ledger before letting it bind: **$725.4712**. | (in `a76d851`) |
| **(3)** systemd, `study.spend` 120 s, `study.poll` at cadence, `Persistent=true`, user units, enabled before any resume | Installed, enabled, **and observed firing.** §2 below. | `3b9074d` |
| **(4)** rep06 compensated; standing rule recorded | Rule recorded in `resume_fleet.py` as a cause-keyed table; applied in the deadline arithmetic, in `deadline_basis`, in rep06's own INBOX notice, and surfaced in the dry-run. §3 below. | `3a7c4df` |
| **(5)** Rev 21 to rep01 only; budget/infra fleet-uniform | **Already correct; nothing changed.** Verified `deliver_escalation_answers.py` sends `NOTICE_rep01_rev21.md` to `["rep01"]` alone and `NOTICE_fleet_uniform.md` to all sixteen, and that the uniform notice contains no arm-dependent content. | — |
| **(6)** Reconcile STATE.md in a grooming commit | Done. §4 below. | `1c8ca02` |
| **(7)(e)** selftest death-case fixture | Done; suite **87/1 → 88 PASS / 0 FAIL**. | `cff2a91` |
| **(7)(g)** `HOST_REQUIREMENTS.md` | Written from this migration. | `814cb3c` |
| **(7)(h)** smoke-literal cleanup | Done. | `965fafe` |

All seven commits are pushed; `origin/main` is at `1c8ca02`.

### 2. The schedulers — and one thing I had to decide to make the ratified property real

**`Persistent=true` does not do what it says on a monotonic timer.** systemd honours it **only**
on `OnCalendar=` timers; on an `OnUnitActiveSec=` timer the key is accepted, silently ignored, and
reads in the unit file as though the guarantee is in force. Since `Persistent=true` is exactly the
launchd property the ruling was porting — a missed interval fires on resume rather than being
dropped — writing the obvious interval-based timer would have reproduced **SI-012's shape**: a
scheduling property asserted in a config file with no runtime effect. Both timers are therefore
`OnCalendar`-based (`*:0/2` and `*:0/10`), with `AccuracySec=1s` because systemd's default
accuracy is 1 minute — 50 % jitter on a 120 s cadence, and the spend bound is computed *from* the
interval.

**Observed, not asserted** — the whole of SI-012 is that nobody ever watched:

```
study.spend  fires at 01:36:00Z  01:38:00Z  01:40:00Z     exactly 120 s, zero drift
study.poll   fires at 01:40:00Z, completed rc=0
```

**Lingering is enabled** (`loginctl enable-linger`, no root needed). Without it the user manager
stops at logout and both timers die with it — an unattended fleet with no scheduler, which is the
condition they exist to prevent.

**Suspend, verified as ordered.** All four targets — `sleep`, `suspend`, `hibernate`,
`hybrid-sleep` — are `static` and `inactive`, and `logind`'s `IdleAction` is at its compiled
default `ignore` with no override in `/etc/systemd/logind.conf`. **They are not `masked`**;
masking needs root. So the correct statement for the record is *no trigger to suspend exists*,
which is weaker than *cannot suspend*. Masking is on the root-required list in
`HOST_REQUIREMENTS.md` §5 alongside the `screen` install.

### 3. rep06 — the restoration, and why it is arm-blind

Recorded as a rule keyed on **cause**, not identity, exactly as ruled: *the 168-hour entitlement is
live-session time, and campaign time lost to a verified harness fault is restored to the affected
replicate.* It would be written identically for any replicate the harness failed this way; nothing
in it can be read differently for a gated and an ungated arm; and the arm map stays sealed — I do
not know which arm rep06 is in and did not need to.

**Measurement re-verified from the ledger before applying:** rep06's last row whose token totals
moved is `2026-08-29T12:37:21.500736Z`; the pause stamp is `2026-08-29T22:14:19.952793Z`;
difference **9.6162 h**, ratified at **9.62 h**. (180 ledger rows for rep06, flat after 12:37:21.)

**One thing this forced.** The INBOX notice told every replicate its deadline had moved by
*"exactly the pause duration"*. For rep06 that would have been false in the notice it was most
important to be honest in, so the notice now states the pause extension and the restoration
separately, and rep06's carries the cause and the measurement. Nothing in that paragraph
references arms, gates or Appendix A.

### 4. The grooming — what a cold reader would have inherited

The stale paragraph was worse than one paragraph. **Items 14, 15 and 16 together described a study
still choosing its benchmark** — world stopped on a fired contingency, Q2 blocked behind it — when
the world froze at **N = 12,499 with zero validation exceptions** on 2026-08-29 and Q2 landed
inside the envelope (2,300 CPU-h = 10.06 % of naive; G7's `k` invariant as algebra). Alongside
them: the phase line read **PRE-SEAL** after the seal commit `c67fff5`; four seal blockers
(11(a), 12's SI-012/013/014, 13's missing rubric, 10's `criterion` residual) read **open** when
all had closed; item 18 read **84 PASS**; and the top banner said *"do not resume here"* in a
working copy that now lives on the host it was pointing at.

**Nothing was deleted.** Every finding is kept and every superseded status line names what closed
it and when. What had gone stale was the status, not the findings.

### 5. Findings from doing the work — four of them, one a correction to my own REPORT 001

**(a) The poll cadence in the record contradicts itself, and I had to choose. Please rule.**
`poll.sh`'s header says *"Run every 10 minutes (ratified interval)"*, and SI-012's arithmetic is
built from it — *"2 cycles of an expected 393"*, and 393 × 10 min = 65.5 h, which is exactly the
smoke campaign. But the retired `study.poll.plist` carried `StartInterval 1800`, and both
`config.py` and `spend_wrapper.sh` refer in prose to *"the 30-min cluster cadence"*. **So the
scheduler that finally did exist was running at three times the ratified interval.** I wrote the
timer at the ratified **10 minutes** and flagged it rather than copying the plist forward. This is
in the fleet's favour — it tightens the polled compute-overshoot bound by 3× — and it does not
disturb the spend argument, which holds a fortiori. But the ratified overshoot bound depends on
this number, so it should be a ruling and not my reading.

**(b) Correction to REPORT 001 §1 and to STATE.md: the divergence panel does not stand down on
`PAUSE.json`.** I wrote that `restart_watch.sh` *and* `divergence.py` both stand down while the
pause record exists. `restart_watch.sh` does. `divergence.py` stands down on
`SMOKE_ARCHIVED.json`, permanently, because its subject is the two archived smoke arms. **The
safety conclusion is unchanged and in fact stronger** — I verified separately that
`restart_watch.sh` is the only component in `poll.sh` with authority to relaunch anything, and it
exits before reaching that authority — but the mechanism I stated was wrong, and a reader would
have relied on the mechanism. Corrected in STATE.md in the grooming commit.

**(c) The spend meter appends 5.8 MiB/day to the ledger against a fleet that is not moving.**
At 120 s × 16 replicates that is **11,520 rows/day**, every one an identical re-tally, for as long
as the hold lasts. They are not spurious — this is the same idempotency I argued in REPORT 001
§4(b) — but they are not informative either, and the ledger is a record the study reads. **Your
call:** I can stop `study.spend.timer` for the duration of the hold and restart it as part of the
resume, or leave it running as continuous evidence that the scheduler works. I have left it
**running**, because the ruling was that the fleet is not resumed into an unscheduled state and
because an unobserved scheduler is what SI-012 was.

**(d) `charter_revisions.md` stops at Rev 21; the charter's own revision table carries Rev 22 and
Rev 23.** Both revisions are properly recorded as rows in `prereg/charter_v0.9.md` — and Rev 22 is
substantive, since it is what split the pinned-file rule out of G3 so it reaches both arms,
resolving the asymmetry LOG-2026-08-29-12 filed for a ruling. But the file that carries the
narrative write-ups has no Rev 22 or Rev 23 section. I have not touched `prereg/`. Flagged only.

**Smaller, not acted on:** `selftest.sh`'s *"live replicate is not restartable"* passes for the
wrong reason. Both of its `liveness.py` calls use `--no-update`, so no baseline is ever recorded
and the second call exits 1 via *"no positive evidence of death (baseline only)"* — never
exercising the growth path its name describes, and duplicating the check on the line below it. I
verified this by reproducing the case. It is a **passing** test outside the fixture fix you
authorised, so I have not changed it.

### 6. What happens next, and what I will not do without a go

`screen` **is now installed** (4.09.01) — the provisioning is landing. **`dirac-bei` still does not
resolve** and there is no `~/.ssh/config`, so the trigger in your item (8) has not fired and the
dry-run has not been run against the cluster. I did run the dry-run **path** locally to verify my
change to it; it touches no cluster, changes nothing, and its output is in §3's arithmetic.

On `ssh dirac-bei true` passing I will: run `./harness/resume_fleet.sh --dry-run`, report the
measured pause duration and the projected per-replicate deadlines here, and **hold for the one
word**.

Until then I will not resume, deliver any notice, touch a credential, or clear the pause record.

— Bei (harness)

---

## 2026-08-30T02:24:59Z (11:24:59 KST) — REPORT 003, on the dry-run. FLEET STILL PAUSED. Held for go.

> **In one line:** `ssh dirac-bei true` now passes and I verified it myself rather than taking the
> handoff's word for it; all three ratification items were already complete and are re-verified
> here rather than re-done; the dry-run is clean and the measured pause stands at **4.1776 h**,
> which every replicate gains, with rep06 gaining that **plus its ratified 9.62 h**. The one thing
> worth your attention is that **`--dry-run` never exercises the check that would actually abort a
> resume** — so I ran that check read-only and report it below.

**Status: HOLDING.** `resume_fleet.sh` has not been run in live mode. `PAUSE.json` is untouched.
No session resumed, no notice delivered, no deadline extended, nothing written to any workspace.
Every cluster contact in this report is a read.

### 1. The trigger condition, verified by me

Provisioning was done externally and reported clean. I did not take that as the verification — the
handoff is a claim about the host, and item (5) of `HOST_REQUIREMENTS.md` is specifically the case
where a human's test passes and the harness's fails. Re-run here, in the exact forms the record
specifies:

| Requirement | Check | Result |
|---|---|---|
| 5 — alias + key, non-interactive | `ssh -o BatchMode=yes -o ConnectTimeout=10 dirac-bei true` | **exit 0, silent** |
| 5 — the gateway it now jumps through | `ssh -o BatchMode=yes dirac-bei-gw true` | **exit 0, silent** |
| 6 — workspace path reachable *and writable* | `/home1/users/Bei/ws/<rep>` for all sixteen | **16/16 `rw`** |
| 1 — `screen` | `screen --version` | **4.09.01 (GNU)** |

`~/.ssh/config` resolves `dirac-bei` to `143.248.125.145` via `ProxyJump dirac-bei-gw`
(`143.248.130.178`). **The gateway hop is new** — no earlier report or requirement mentions one,
and the retired laptop reached the cluster directly. It works and `BatchMode` is clean through it,
so nothing is blocked; I note it because the record now understates the path, and a future host
rebuild that follows `HOST_REQUIREMENTS.md` §5 literally would not know to configure a jump host.

### 2. The ratification list — all three already complete; verified, not re-done

Each of the three was executed and pushed under REPORT 002. I checked state rather than re-running
anything, since re-running (2) or (3) would have been a write against a fleet under hold.

**(a) systemd timers enabled.** `study.poll.timer` and `study.spend.timer` are both
`enabled` and firing. `install.sh --verify` reports `linger: ENABLED`, all four suspend targets
`static (inactive)`, `IdleAction` at the compiled default. Cadence observed in the fire logs, not
asserted:

```
study.poll   02:00:00Z fire -> 02:00:02Z done rc=0
             02:10:00Z fire -> 02:10:02Z done rc=0
             02:20:00Z fire -> 02:20:02Z done rc=0      exactly 600 s, rc=0 each
study.spend  02:18:00Z  02:20:00Z  02:22:00Z            exactly 120 s, zero drift
```

Both units are `OnCalendar=` (`*:0/10`, `*:0/2`) so `Persistent=true` is really in force, which
was the judgement call REPORT 002 §2 flagged. **The 10-minute poll interval is still the reading I
made and not a ruling you have given** — REPORT 002 §5(a) is open and this report does not close
it.

**(b) Meter active on the $725.47 baseline.** `spend_baseline.json` is `active: true` carrying
token counts, and the meter binds it. Run across all sixteen just now:

**$725.4712 / $4,480 = 16.19 %**, sixteen replicates, **all `OK`, none at warn**, every line
reading `$0.00 on this host + $X carried forward`. Local tally is **$0.00 for all sixteen**, which
is the expected shape on a host whose `~/.claude/projects` is empty and confirms the meter is
carrying rather than double-counting — the failure mode `spend_baseline.json`'s own refusal clause
exists to catch. The figure matches the ledger-derived total to the fourth decimal.

**(c) `fleet_spend` correction appended.** `harness/state/fleet_spend.jsonl` carries the
`fleet_spend/correction/1` entry: superseded `714.94` at its `2026-08-29T22:24:19Z` stamp, delta
`$10.5312`, corrected `725.4712`, with `left_unedited: true`. **`fleet_spend.json` is byte-for-byte
unchanged** — verified against git, it is not in the working tree's modified set.

### 3. The dry-run — measured pause and per-replicate arithmetic

```
paused at:    2026-08-29T22:14:19.952793+00:00
now:          2026-08-30T02:24:59.381189+00:00
pause so far: 4.1776 h  -- gained by all sixteen, uniformly
rep06:        +9.6200 h -- additionally, keyed on cause [PI ruling 2026-08-30, REPORT 001 §4(f)]
```

The pause is **still running** and the figure is measured at execution, not stored, so the number
in the live run will be larger than the one above by however long the hold lasts. That is the
design — nothing here is a round number or a judgement.

| Replicate | Deadline at pause (KST) | Projected (KST) | Gain |
|---|---|---|---|
| rep01 | 2026-09-05T14:12:32 | 2026-09-05T18:23:12 | +4.1776 h |
| rep02 | 2026-09-05T19:41:21 | 2026-09-05T23:52:00 | +4.1776 h |
| rep03 | 2026-09-05T19:41:27 | 2026-09-05T23:52:06 | +4.1776 h |
| rep04 | 2026-09-05T19:41:33 | 2026-09-05T23:52:12 | +4.1776 h |
| rep05 | 2026-09-05T19:40:56 | 2026-09-05T23:51:36 | +4.1776 h |
| **rep06** | 2026-09-05T19:41:02 | **2026-09-06T09:28:54** | **+4.1776 h +9.62 h** |
| rep07 | 2026-09-05T19:41:08 | 2026-09-05T23:51:48 | +4.1776 h |
| rep08 | 2026-09-05T19:41:15 | 2026-09-05T23:51:54 | +4.1776 h |
| rep09 | 2026-09-05T19:41:39 | 2026-09-05T23:52:18 | +4.1776 h |
| rep10 | 2026-09-05T20:42:28 | 2026-09-06T00:53:07 | +4.1776 h |
| rep11 | 2026-09-05T20:42:09 | 2026-09-06T00:52:48 | +4.1776 h |
| rep12 | 2026-09-05T20:42:16 | 2026-09-06T00:52:55 | +4.1776 h |
| rep13 | 2026-09-05T20:42:22 | 2026-09-06T00:53:01 | +4.1776 h |
| rep15 | 2026-09-05T20:42:34 | 2026-09-06T00:53:14 | +4.1776 h |
| rep16 | 2026-09-05T20:42:41 | 2026-09-06T00:53:20 | +4.1776 h |
| rep17 | 2026-09-05T20:42:48 | 2026-09-06T00:53:27 | +4.1776 h |

I recomputed two rows by hand against the stored microsecond stamps rather than trusting the
printer: rep02 `19:41:21.212177 + 4h10m39.4s = 23:52:00` ✓; rep06 `19:41:02.832166 + 4h10m39.4s =
23:51:42`, `+ 9h37m12s = 09:28:54` ✓. The restoration is applied to the **pause-record** deadline,
not to the extended one, so the two additions do not compound.

**A consequence of §4(f) worth stating plainly, because it is visible and someone will ask.**
The restoration moves rep06 from mid-pack to **the latest deadline in the fleet** — about 9.6 h
behind the wave-A cohort and 8.6 h behind wave B. That is the ruling working correctly, not a
side-effect: rep06 is being given back live-session time it lost to a harness defect, so it
finishes later in wall-clock while holding the *same* 168 h of worked time as everyone else. The
asymmetry is in the clock, not in the entitlement. It is also **arm-blind** — the rule keys on
cause, the arm map stays sealed, and I do not know which arm rep06 is in.

### 4. What the dry-run does **not** cover — and the check I ran read-only instead

**This is the finding of this report.** `resume_fleet.sh --dry-run` returns at the end of its
dry-run branch, *before* it ever calls `resume_fleet.py`. So the dry-run exercises the deadline
**arithmetic** and nothing else. In particular it never runs **PASS 1** — the sixteen live
`WORKSPACE.json` reads that compare each live deadline against the pause record and **abort the
whole resume** on the first mismatch. That check is the single most consequential thing in the
resume path, it is the only part that touches the cluster before anything is written, and it is
the part a dry-run exists to rehearse. A clean `--dry-run` is therefore *not* evidence that the
resume will proceed; it is evidence that the arithmetic is right if it does.

So I ran PASS 1's logic myself, read-only — the same sixteen `grep deadline_kst` reads over the
same alias, with the comparison and without the write:

```
match = 16    moved = 0    unreadable = 0        PASS 1 would: PASS
```

All sixteen live deadlines equal the pause record exactly, to the microsecond. **rep06's live
value is `2026-09-05T19:41:02.832166+09:00`** — the pre-defect value that was restored by hand
after `stamp_deadline.py` moved it +11.3 h, so that revert is confirmed still in place on the
cluster and PASS 1 will not trip on it.

**Two smaller gaps in the same shape.** `--dry-run` also does not exercise (i)
`deliver_escalation_answers.py`, or (ii) the per-replicate relaunch. I ran the first's own
`--dry-run` separately: **2,981 bytes of the fleet-uniform notice to all sixteen, 1,994 bytes of
the Rev 21 notice to `rep01` alone**, escalation rows unmodified — the scoping REPORT 002 §1(5)
verified, still correct. For the second I confirmed `config.phase_of` resolves **`main` for all
sixteen**, which is what stops step 5 from repeating the smoke-roster defect.

**I have not changed `resume_fleet.sh` to close this gap.** Extending the dry-run to perform PASS 1
would be the right fix and it is a read-only change, but it edits the resume path itself while the
fleet is held for a go on that exact path, and the coverage is provided above by other means. It
is yours to rule on.

### 5. Other state, verified

- **The fleet is down.** No `rep-*` screen sessions on bronze4 (one socket, my own shell). All
  **16 stop files present** under `harness/sessions/`. `PAUSE.json` in place, so
  `restart_watch.sh` remains stood down.
- **Suite: 88 PASS / 0 FAIL**, re-run on bronze4 just now, including SI-014's regression case
  ("production state files unchanged by this run").
- **`study.pollprobe` has no systemd counterpart, deliberately.** The retired host had three
  plists; `install.sh` renders two. The third was a 60-second heartbeat that existed only to prove
  launchd was firing, and its function is served better by `poll_fires.jsonl` and
  `spend_fires.jsonl`, which record real fires with return codes — which is what §2 quotes. Noted
  so the 3→2 drop is not later read as something lost in the migration.
- **Host keys were accepted trust-on-first-use during external provisioning**, and the record
  holds no fingerprint to check them against (`known_hosts` gained the gateway's entry; the
  cluster's is unchanged from `known_hosts.old`). Nothing suggests a problem and the cluster key
  is consistent across both files. But "the alias resolves and authenticates" is not the same
  claim as "it authenticates *the right host*", and I cannot close that second one from here.
  Flagged, not blocking.
- **REPORT 002 §5(c) is still open and the ledger is still growing.** `harness/spend.jsonl` has
  gained **384 rows since REPORT 002** and stands at 3,294 rows / 1.75 MiB, all of them identical
  re-tallies of a fleet that is not moving. I have left the timer running for the reason given
  there. The working tree is correspondingly dirty in five scheduler-written files
  (`spend.jsonl`, `spend_fires.jsonl`, `poll_fires.jsonl`, and the two daily logs) — expected, and
  no tracked state file is modified.

### 6. What I will do on the word, and what I will not do without it

On your go: `./harness/resume_fleet.sh` live — deadlines extended by the pause measured **at that
moment**, notices delivered before the agents wake, counters reset, stops cleared, sixteen
relaunched each in its own phase, and `PAUSE.json` retired **only** on a clean sixteen-for-sixteen.
Then I will verify all sixteen up, meter once against the carried baseline, and report again.

Until then: no resume, no notice, no workspace write, no credential touched, no pause record
cleared, and no edit to the resume path.

**Open for ruling, carried forward:** §5(a) the 10-minute poll cadence (REPORT 002) · §5(c) the
paused-fleet ledger growth (REPORT 002) · §5(d) `charter_revisions.md` missing Rev 22/23
(REPORT 002) · §4 above, whether `--dry-run` should perform PASS 1.

— Bei (harness)

---

## 2026-08-30T02:37:00Z (11:37:00 KST) — REPORT 004, on the REPORT 002 rulings. FLEET STILL PAUSED. Held for go.

> **In one line:** ssh re-verified and passing, and **REPORT 003 above already contains the
> dry-run you ordered** — it was run and filed before this message arrived. (d) is executed and
> (c) needs nothing. **I have not executed (a), because (a) was ruled on a premise I gave you in
> REPORT 002 §5(a) and that premise is wrong.** Ten minutes is the ratified interval for the
> **smoke** phase; **thirty is the ratified interval for main**, and the plist was keeping it. I am
> not filing a correct number as a deviation or overwriting a correct bound with a wrong one on my
> own error. Details below; this needs one more word from you.

### 0. Your provisioning check — already satisfied

`ssh -o BatchMode=yes -o ConnectTimeout=10 dirac-bei true` → **exit 0, silent**; the gateway hop
likewise. Nothing needs relaying: `/home/Bei/.ssh/` has `config`, `id_ed25519` (0600),
`id_ed25519.pub`, `known_hosts`, all owned by `Bei`, and all sixteen workspaces read/write over the
alias. **The dry-run was run on that pass and reported in REPORT 003**, which also carries the
measured pause, the per-replicate deadline table, rep06's `+9.62 h` arithmetic, and one finding
about what `--dry-run` does not cover. It is directly above this entry.

Fleet still down: 0 `rep-*` sessions, 16 stop files, `PAUSE.json` in place.

### 1. (a) — NOT EXECUTED. The record does not contradict itself; my report did.

I reported that `poll.sh`'s *"Run every 10 minutes (ratified interval)"* contradicted the plist's
`StartInterval 1800`. **It does not, and I should have caught this before filing it.** The two
numbers are scoped to different phases and both are ratified:

```
config.py  "watchdog_poll_minutes": {"smoke": 10, "main": 30}
```

`poll.sh`'s header opens *"One operational poll of the whole **smoke** fleet"* — the 10-minute
figure in it is **smoke-scoped**, and I quoted the second half of that sentence without the first.
SI-012's own arithmetic says the same thing in both directions:

| SI-012 says | Phase | Poll | Bound |
|---|---|---|---|
| "Cycles expected at the ratified 10-minute interval — 393" (65.5 h = the smoke campaign) | smoke | 10 min | 8.33 CPU-h, 2.45 % |
| "Main-run parameters **as ratified**: … **30-minute poll**" | main | **30 min** | **6.00 CPU-h, 0.375 %** |

So the retired plist at 1800 s was **running the main phase at its ratified main cadence.** It was
not a deviation and it was not three times anything. The deviation is the timer **I installed**,
which is running main at 10 minutes — 3× tighter than ratified — and it is running that way right
now, and would apply to all sixteen the moment the fleet resumes.

**Why I did not just carry out the ruling.** Executed literally it would (i) file a correct,
ratified figure into the record as a deviation, and (ii) restate the main compute-overshoot bound
from **6.00 CPU-h (0.375 %)** to **2.00 CPU-h (0.124 %)**. That second number is the problem: it is
not merely tighter, it is **a bound the harness cannot honour**, and writing it would be exactly
what SI-012's own Proposed §3 warns against — *"a bound derived from an assumption is not a bound;
it is the assumption wearing a number."* Reproducing that inside the fix for SI-012 is the shape I
flagged in REPORT 002 and I am not going to author it.

**Measured, not argued — 28 recorded poll cycles from `poll_fires.jsonl`:**

```
while the fleet was LIVE (N=16):   126 s, 139 s, 152 s, 158 s, 236 s, 248 s, 262 s ...
                          max:     842 s  (14.0 min)
current cycles (fleet paused):     2 s     <- cheap, not representative
```

A 600 s interval **is already exceeded by the observed worst case of 842 s.** At 1800 s it is not
close. SI-012 documented the mechanism before I measured it: `poll.sh` is serial and O(N), and
`divergence.collect()` retries 3× at a 300 s timeout, so **one unreachable workspace can consume up
to 900 s** — "1.5× the smoke interval, half the main interval", and every replicate after it in the
loop is skipped **silently**. SI-012 called N=20 at 30 minutes *"it fits, but not comfortably."*
At 10 minutes it does not fit.

So the tighter cadence does not buy a tighter bound. It buys overlapping cycles, silently skipped
replicates, and a *worse* effective interval than 30 minutes — while the record would claim 2.00.

**What I recommend, and what I need from you.** Revert `study.poll.timer` to `OnCalendar=*:0/30`
for the main phase, keep the ratified **6.00 CPU-h / 0.375 %** bound exactly as it stands, and file
the deviation against **my timer**, not against the plist. Then (a)'s remaining substance still
holds and is worth doing: **`poll.sh`'s header is smoke-scoped in a main-phase harness** and should
say so, and SI-012 Proposed §3 — compute the bound from the *measured* interval since the last
`watchdog.jsonl` entry rather than from the configured constant — is the durable fix, since it
would have made this self-correcting.

I have changed **nothing** for (a): the 10-minute timer is still installed and still firing, so the
state is exactly as REPORT 003 described it and is yours to rule on. If you read the phase scoping
differently and still want 10 minutes for main, say so and I will restate the bound at 2.00 CPU-h
— but the cycle-time measurement above should be on the record first.

### 2. (d) — EXECUTED. Rev 22 and Rev 23 narrative sections written.

`prereg/charter_revisions.md` gains two sections, written from the charter's own revision rows
(`prereg/charter_v0.9.md` lines 46, 241–243) and the rendered §3/§4 text. **`charter_v0.9.md` is
untouched** — verified, empty diff. Documentation of ratified history, exactly as authorized.

- **Rev 22** — (a) the pinned-file rule split out of the G3 gate into §3 common core, with the
  reason it mattered: Appendix A *is* the treatment, so a general protocol statement left sitting
  inside the gate reached the gated arm only, giving eight replicates a pinned file set with no
  statement of what it governed. (b) "Cost mechanics and discipline" into §4 common core,
  byte-identical in both arms, because it is a statement about billing rather than about science
  and a one-arm version would have confounded the pre-registered per-arm cost decomposition.
- **Rev 23** — "Context hygiene" into §4 common core. Written as the other half of Rev 22(b)'s
  mechanism: 22(b) governs what enters context, 23 governs what is carried forward. Carries the
  measured basis (cache-read tokens climbing 97k → 237k per turn; rep01 71 % front-loaded) and the
  reason it had to be common core — the gated charter is 28,929 bytes against 13,109, so that arm
  is structurally more expensive per turn before anyone does anything, and a one-arm hygiene rule
  would have made that structural difference inseparable from a behavioural one.

Both sections state that they were written up on 2026-08-30 under your authorization, so no future
reader mistakes the write-up date for the ruling date.

### 3. (c) and (b) — no action needed

**(c)** Ratified as-is; `study.spend.timer` stays running through the hold and I have not touched
it. For the record it has now added **384 rows since REPORT 002** (3,294 rows / 1.75 MiB).
**(b)** Noted, already corrected in STATE.md at the grooming commit.

**The selftest wrong-reason pass** is filed as post-resume, low priority, and I have not touched it.

### 4. Status

Nothing committed — the working tree carries `prereg/charter_revisions.md`, this file, and five
scheduler-written logs. No workspace write, no notice, no resume, no pause record cleared.

**Blocking on you:** (a) — 30 minutes restored for main (my recommendation), or 10 minutes
confirmed with the bound restated. **Ready on your word:** the live resume, per REPORT 003 §6.

— Bei (harness)

---

## 2026-08-30T03:05:00Z (12:05:00 KST) — REPORT 005, on the go. **FLEET RESUMED AND RUNNING.**

> **In one line:** the ruling is executed — `study.poll.timer` is back at `OnCalendar=*:0/30`
> with the **6.00 CPU-h / 0.375 %** bound untouched, the deviation is filed against my timer as
> **SI-023** with the measurement attached, and **the fleet resumed cleanly at 11:42:33 KST**:
> PASS 1 matched 16/16 before anything was written, 16/16 relaunched, 16/16 live deadlines
> re-read afterwards and correct. All four post-resume items are done and the suite is
> **98 PASS / 0 FAIL**. One judgement call inside the revert is flagged for you in §6, and §7
> lists what I have *not* been able to verify yet.

### 1. The cadence — reverted first, before the resume, because it binds the moment the fleet is live

`harness/systemd/study.poll.timer` → `OnCalendar=*:0/30`, re-rendered through
`install.sh`. Verified as **effective runtime state**, not as file contents:

```
systemctl --user show study.poll.timer
    TimersCalendar={ OnCalendar=*-*-* *:00/30:00 ; next_elapse=Sun 2026-08-30 12:00:00 KST }
    Persistent=yes      AccuracyUSec=1s
```

**And it fired on the new cadence, observed:** `02:40:00Z` (last 10-minute fire) → **`03:00:00Z`
fire → `03:01:54Z` done, rc=0** — 114 s for a live sixteen-replicate cycle. All sixteen report
`liveness=alive` in that cycle. The ratified bound is unchanged everywhere it appears:
`config.overshoot_bound("main")` returns **6.0 CPU-h / 0.37 %**, and the watchdog prints it.

### 2. The resume — executed on your go, 2026-08-30 11:42:33 KST

```
measured pause: 4.4704 h (16,094 s) -- applied to all 16 identically
verified: all 16 live deadlines match the pause record      <- PASS 1, before any write
...
16/16 up      pause record retired; restart watcher re-armed
=== RESUMED CLEANLY ===
```

- **PASS 1 passed 16/16** to the microsecond, rep06's hand-restored value included.
- **Deadlines, live, re-read by me afterwards over the alias: 16/16 equal to the extended
  values.** rep01 → `2026-09-05T18:40:46`, the wave-A cohort → `2026-09-06T00:09:xx`, wave B →
  `01:10:xx`, **rep06 → `2026-09-06T09:46:28`** (uniform 4.4704 h **plus** its ratified 9.62 h).
- **Notices:** fleet-uniform to 16/16, Rev 21 to rep01 alone, **22 escalation rows closed**,
  delivered *before* the agents woke.
- **Sixteen `screen` sessions up**, `rep-rep01 … rep-rep17`, all detached and writing
  transcripts (rep01 560 KiB, rep06 472 KiB, rep17 380 KiB and growing).
- **Meter, once, against the carried baseline: `$746.06 / $4,480 = 16.65 %`, all sixteen `OK`,
  none at warn.** That is `$725.47` carried + `$20.59` spent on this host since the sessions
  woke — the boot turns. The baseline is carrying, not double-counting.
- `PAUSE.json` retired to `PAUSE.resumed.20260830T024428Z.json`; `LAST_RESUME.json` written.

### 3. The deviation — filed as SI-023, against my timer

`SI_LEDGER.md` gains **SI-023**, which keeps the wrong number beside the right one as the ledger
requires: both cadences ratified, phase-scoped, the half-sentence I quoted, the retired plist
exonerated, and the 30 recorded cycles as the measurement (`126–262 s` live, **worst 842 s**,
`66–78 s` paused-with-cluster-reachable, `2 s` paused-and-unreachable). It records that the
10-minute timer ran **02:42Z back to its 01:34Z install — 68 minutes, entirely inside the pause,
against zero live sessions**, so no replicate was ever polled at the wrong cadence. Class:
same as SI-018/SI-019, a phase-scoped value read out of phase.

### 4. The four authorized post-resume items — all four done

**(a) `poll.sh`'s header is phase-scoped.** It now says the file is phase-*agnostic* — it polls
whatever is in `active_replicates` — that the cadence is `{"smoke": 10, "main": 30}` and lives in
the scheduler, and it quotes its own old sentence as the thing that caused SI-023.

**(b) SI-012 Proposed §3 — the bound is computed from the measured interval.**
`config.overshoot_bound(phase, poll_minutes=None)` takes a measured override;
`watchdog.py` measures the gap since **its own last `watchdog.jsonl` entry for that replicate**
and reports *both* bounds plus a verdict (`as-ratified` / `bound-understated` /
`tighter-than-ratified`). The ratified key is untouched, so nothing downstream changes meaning.
Against SI-012's own 49 h outage the measured bound reads **588 CPU-h / 36.5 %** — SI-012's
table says 588.6 / 36.8 — instead of the 8.33 the harness printed throughout. **Live, in the
03:00 cycle:**

```
[watchdog] rep01  T-150.7h  liveness=alive  poll=30min bound=+6.0CPU-h (0.37%)
    poll interval measured 20.48min vs ratified 30min (0.68x): bound +4.1CPU-h (0.25%)
                                                <-- POLL INTERVAL TIGHTER THAN RATIFIED
```

That flag is **correct and transitional**: this cycle's predecessor was a 10-minute-era fire at
02:40Z, so the first measured gap after the revert is 20.5 min. See §7 — I have not yet seen the
cycle that should clear it.

**(c) `--dry-run` now performs PASS 1, read-only.** PASS 1 is factored out of
`resume_fleet.py:main()` into `pass1(reps, at_pause, abort=)`; `--check-only` runs it and nothing
else; `resume_fleet.sh --dry-run` calls it and adopts its exit code. Live behaviour is byte-for-
byte the same path with `abort=True`. Tested **against the live cluster, read-only, both ways**:
a fixture matching the real deadlines gave `match=16 problems=0 → PASS 1 would: PASS` (exit 0),
and a fixture with one moved deadline and one unreadable replicate gave
`match=1 problems=2 → PASS 1 would: ABORT` (exit 1), naming both problems rather than stopping
at the first — which is what a dry-run is for.

**(d) The selftest's wrong-reason case.** Its baseline call dropped `--no-update`, so a baseline
is actually recorded (under `HARNESS_STATE_DIR`, so nothing about a fake replicate reaches the
live growth record) and the second call now exercises the **growth** path it is named after. Two
assertions added on the *reason*: the output must say `alive` and must **not** say `baseline
only`.

**Suite: 98 PASS / 0 FAIL** (was 88), including the SI-014 regression case. The ten new cases
cover the ratified bound staying at 6.00, the measured basis moving it, the divergence verdict,
an unmeasured interval reporting `none` rather than a number, the dry-run's PASS 1 wiring, and
the two reason-assertions above.

### 5. The gateway hop and the host keys — `HOST_REQUIREMENTS.md` §5 and new §5a

Requirement 5 now names the jump host and requires **both** aliases to pass `BatchMode`;
checklist step 3 does the same. New **§5a** records the `ProxyJump` topology, that two hosts must
authenticate rather than one (a gateway failure looks exactly like a cluster outage), and that
the hop is inside the latency budget the 30-minute cadence absorbs. The **trust-on-first-use**
host keys are recorded there as the record's own gap, non-blocking, with your note that you will
verify the fingerprints against the Mac's `known_hosts` on your return, and the rule for the next
move: **carry the expected fingerprints in the record, or a rebuild has nothing to verify
against.**

### 6. One judgement call inside the revert — please rule when convenient

`study.poll.service` carried `TimeoutStartSec=9min`, which **I** sized to fit inside the
10-minute interval. Left at 9 minutes under a 30-minute cadence it is no longer a pile-up guard —
it is a **kill on a poll that is merely slow**, and the measurement says that is not hypothetical:
the worst observed live cycle is **842 s (14.0 min)** and SI-012 shows one unreachable workspace
alone can reach **900 s**. systemd would have terminated a working poll mid-loop and recorded a
failure for it, which is SI-012's shape again — the scheduler fires, the work does not finish,
and the record does not say so. **I set it to 25 min**, still strictly inside the 30-minute
interval. It is in SI-023 and it is the line to change if you want the guard tighter than the
measurement.

**Also mine, smaller, done:** `deliver_escalation_answers.py` writes a timestamped
`escalation_queue.jsonl.pre-answer.<stamp>` backup, and the `.gitignore` rule that keeps the
escalation ledgers out of git did not match it — so this resume's backup was sitting untracked
and the next `git add` would have committed the ledger under another name. Pattern added.

### 7. What I have NOT verified, stated as such

- **The next poll cycle.** At `03:30:00Z` the measured interval should read ~30 min and the
  verdict should flip to `as-ratified`. I have seen `03:00` (20.48 min, transitional) and **not**
  `03:30`. If it does not clear, the measurement is wrong and not the timer.
- **The 25-minute `TimeoutStartSec` has not been exercised** — no poll since the change has run
  long. Its correctness rests on the recorded cycle times, not on an observation.
- **Compute meters read `UNACCOUNTED`, not a number**, for all sixteen: no job has finished since
  the resume, so `harvest_cput.sh` has nothing to populate `cpu_h` with. That is **SI-021 working
  as fixed** — a meter with no data says so instead of saying `0.0 OK` — and it will resolve
  itself as jobs land. Flagged so the panel is not misread.
- **Host-key fingerprints** remain unverifiable from here, per §5.
- **Nothing has been observed of the resumed agents' *work*** beyond transcript growth and
  liveness. The first real read of what sixteen woken replicates did with their notices comes at
  the next collection point, not from me.

### 8. State

Committed and pushed. Fleet **RUNNING**: 16 sessions up, restart watcher re-armed,
`study.poll.timer` at 30 min and `study.spend.timer` at 2 min, both `Persistent=true` and both
observed firing. `STATE.md`'s banner, pause section and SI-012 item are reconciled to a resumed
fleet — the findings kept, the status lines updated, as in the last grooming.

**Open for you, none blocking:** §6 the 25-minute service timeout · the host-key fingerprints on
your return · SI-021's `UNACCOUNTED` compute basis, still filed and unruled from 2026-08-29.

— Bei (harness)
