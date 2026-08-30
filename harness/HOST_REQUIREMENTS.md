# What a supervision host must provide

*Written 2026-08-30 from the bronze4 migration, at PI instruction (REPORT 001 §4(g)), because
the retired laptop's configuration was never part of this repository and therefore did not
travel. Four separate defects found during the move — the reopened spend cap, the absent
scheduler, the failing selftest case, the unresolvable cluster alias — are all the same shape:
**truth that lived on one machine rather than in the record.** This file is the record.*

The supervision host is the machine that runs the replicate **agent sessions**. The cluster runs
their **jobs**. These are different machines and the distinction is load-bearing: an offline
supervision host is an offline fleet, which is why 2026-08-29's pause happened at all.

---

## 1. Hard requirements — the fleet cannot run without these

| # | Requirement | Why, and what fails without it | Verify |
|---|---|---|---|
| 1 | **Node ≥ 18** | Claude Code's floor. This is why the cluster head `bnode0` (CentOS 7.6, glibc 2.17) **cannot** host sessions and there was no cluster-side fallback at the pause. | `node --version` |
| 2 | **`claude` CLI on PATH** | Runs every replicate session. | `command -v claude && claude --version` |
| 3 | **Python 3.10+** | The whole harness. f-strings with `=`, `datetime.fromisoformat` on offset strings. | `python3 --version` |
| 4 | **GNU `screen`** | `launch_sessions.sh` starts every session under `screen -dmS`, and both it and `resume_fleet.sh` **prove liveness** with `screen -ls`. Without it all sixteen report `LAUNCH FAILED`, the resume exits 1, and `PAUSE.json` is correctly left in place. `tmux` is **not** a drop-in: the scripts call `screen` by name. | `command -v screen` |
| 5 | **`ssh dirac-bei` — alias + key, non-interactive, *including the jump host*** | Every cluster read and write goes through this exact alias with `BatchMode=yes`. `resume_fleet.py` pass 1 reads sixteen live deadlines over it and **aborts the whole resume** on the first failure. It must work with **no passphrase prompt, no agent, no TTY** — a key that works interactively but not under `BatchMode` will pass a human's test and fail the harness's. **On bronze4 the alias is not a direct connection: it reaches the cluster through a `ProxyJump` gateway (§5a).** | `ssh -o BatchMode=yes -o ConnectTimeout=10 dirac-bei true` **and** the same against the gateway alias must each exit 0 silently |
| 6 | **Workspace path reachable** | `/home1/users/Bei/ws/<rep>` readable and writable for all sixteen. | `ssh dirac-bei 'ls -d /home1/users/Bei/ws/rep01'` |
| 7 | **A scheduler with missed-interval catch-up** | §2 below. Without it nothing runs `poll.sh` and nothing runs the spend meter. This is SI-012, the largest harness defect the study has found. | `./harness/systemd/install.sh --verify` |
| 8 | **Git remote push** | The record is kept on GitHub; the PI reads it there. | `git push --dry-run` |

**Not required locally:** `qstat` / `qsub` / `qas`. `poll.sh` reaches the scheduler over
`ssh dirac-bei`, never locally. Their absence on the supervision host is expected, not a defect.

---

## 2. The scheduler, stated as a property rather than a product

**The requirement is: a missed interval must fire on resume, not be silently dropped.**

That property — not launchd, not systemd — is what SI-012's fix was actually choosing. The
recorded fix reads *"launchd, not cron"*, which is a macOS sentence; when the study moved to
Ubuntu it had no referent, `launchctl` did not exist, and the fleet was one `go` away from being
resumed with **no scheduler at all**. State the property, then name the local implementation:

| Platform | Implementation | The catch-up property |
|---|---|---|
| **Linux (bronze4, current)** | `harness/systemd/` — `study.spend` 120 s, `study.poll` 10 min | `Persistent=true`, **which systemd honours ONLY on `OnCalendar=` timers.** On a monotonic `OnUnitActiveSec=` timer the line is accepted, ignored, and reads as though the guarantee holds. |
| **macOS (retired laptop)** | `harness/launchd/*.plist` — kept as the historical record, **not portable**: paths hardcoded to `/Users/jihankim/replicate-study` | macOS runs a missed `StartInterval` on wake |
| **any** | **`cron` is the wrong answer on both**, and `poll_wrapper.sh`'s own header says so | cron silently drops missed intervals — on the smoke's host that would have been **111 dropped cycles** |

Two further Linux-specific requirements that have no macOS equivalent:

- **Lingering must be on** (`loginctl enable-linger <user>`). Without it the systemd **user**
  manager stops at logout and both timers die with it — an unattended fleet with no scheduler,
  which is precisely the condition the timers exist to prevent. It does not need root.
- **`AccuracySec`** must be set. systemd's default is **1 minute**, which on the 120 s spend
  cadence is 50 % jitter. The spend bound is computed *from* the interval, so the interval has
  to be the interval.

**The cadences are not free parameters.**

- **`study.spend` = 120 s.** Enforcement is *polled*, so the fleet maximum is
  `N × (cap + peak_rate × interval)`. At a 30-minute cadence the overshoot alone is **$168**
  fleet-wide and the $280 cap does **not** fit under the $4,500 limit; at 2 minutes it does.
  `LAUNCH_GATE.md`'s A2 passes on that arithmetic — **slowing this timer silently invalidates
  the launch gate.**
- **`study.poll` = 10 min**, the ratified interval stated in `poll.sh`'s own header and the
  figure SI-012's arithmetic is built from (2 observed cycles against "an expected 393";
  393 × 10 min = 65.5 h = the smoke campaign).

**A scheduler nobody has observed firing is not a scheduler.** That is the whole of SI-012.
After installing, confirm fires land in `harness/spend_fires.jsonl` and `harness/poll_fires.jsonl`
before trusting either.

---

## 3. The host must not sleep — and "it's a server" is a claim, not a check

A suspended host is a stopped fleet. `Persistent=true` catches a missed fire up on wake, but not
sleeping at all is better, and the smoke's host measured **32.00 h suspended (48.8 % of the
campaign), 154 transitions, 111 stretches longer than the poll interval.**

Verify, do not assume:

```bash
systemctl is-enabled sleep.target suspend.target hibernate.target hybrid-sleep.target
grep -E '^\s*IdleAction=' /etc/systemd/logind.conf     # default is `ignore`
```

**On bronze4, 2026-08-30:** all four targets are `static` and `inactive`, and `IdleAction` is at
its compiled default `ignore` — so nothing initiates a suspend. They are **not `masked`**, which
would need root; the machine is a server with no lid, and the verified absence of any *trigger*
is what makes it safe. Masking them is still the belt-and-braces step, and it is on the
root-required list in §5.

---

## 4. What does NOT travel with the repository — read this before any host move

**Claude Code writes each session's transcripts to `~/.claude/projects/<mangled-local-cwd>/` on
the machine the session ran on.** They are not in git and they do not move. Two binding
instruments read them, and both fail *silently and in the unsafe direction* on a fresh host:

- **Spend.** `meter_spend.py` recomputes each replicate's total from those transcripts. On a new
  host they are empty, so every replicate meters **$0.00 spent with a full $280 available
  again** — against $725.47 actually spent. The cap does not fail loudly; **it silently
  reopens.** Carried across as **token counts** in `harness/state/spend_baseline.json`, derived
  from the append-only ledger by `harness/make_spend_baseline.py`, so cost is recomputed from
  `config.RATIFIED["price_per_token"]` in exactly one place. The meter refuses to meter at all
  if it sees local transcripts that already cover the baseline, because the two available fixes
  must not both be applied.
- **Liveness.** `liveness.py` decides death by transcript growth. On a fresh host it correctly
  answers *"no positive evidence of death"* — fail-safe, and right — but any test asserting the
  opposite against a real replicate breaks. `selftest.sh` had exactly one such case and it is
  now a self-built fixture.

**Rule for the next move: anything keyed to `~/.claude/projects` is host-local. Carry it forward
as data in the repository, or it reopens as zero.**

---

## 5. Provisioning checklist for a new host

Root needed (1–2), no root needed (3–7):

1. `apt install screen`
2. *(optional, belt-and-braces)* `systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`
3. `~/.ssh/config` alias `dirac-bei` + key, **and the `dirac-bei-gw` jump host it goes
   through** (§5a); verify `ssh -o BatchMode=yes dirac-bei true` **and**
   `ssh -o BatchMode=yes dirac-bei-gw true` each exit 0
4. `git clone` this repository
5. `loginctl enable-linger $USER`
6. `./harness/systemd/install.sh` — then **watch `*_fires.jsonl` for a real fire**
7. `python3 harness/make_spend_baseline.py` if the fleet has spend on a previous host; confirm
   `./harness/meter_spend.py --all` reports the carried total, not `$0.00`

Then, and only then, `./harness/selftest.sh` (expect **88 PASS / 0 FAIL**) and
`./harness/resume_fleet.sh --dry-run`.

**Credentials never enter this repository** (PI standing rule 2026-08-26; enforced by
`.gitignore`). The ssh key and the git push credential are configured on the host and are named
here only as requirements.

---

## 5a. The gateway hop — the cluster is not reached directly [added 2026-08-30, PI-authorized]

**Found by verifying §5 rather than accepting the handoff's word for it (REPORT 003 §1).**
The retired laptop reached the cluster directly, so no earlier report, requirement or plist
mentions a jump host. On bronze4 `~/.ssh/config` resolves:

```
Host dirac-bei-gw          # the gateway
    HostName 143.248.130.178
Host dirac-bei             # the cluster login node, REACHED THROUGH THE GATEWAY
    HostName 143.248.125.145
    ProxyJump dirac-bei-gw
```

Everything works and `BatchMode` is clean through the hop — this blocks nothing and never did.
It is recorded because **the record understated the path**, and a future host rebuilt by
following §5 literally would configure one alias, watch it fail, and have nothing in this file
to tell it a second one is needed. That is the same shape as the four defects this document was
written from: truth that lived on a machine rather than in the record.

Two consequences worth stating, both of which the harness now depends on:

- **Two hosts must authenticate, not one.** A gateway that stops accepting the key fails
  `dirac-bei` entirely, and the failure looks exactly like a cluster outage. Check the gateway
  alias separately — `ssh -o BatchMode=yes dirac-bei-gw true` — before concluding the cluster
  is down.
- **The hop is in the latency budget.** `poll.sh` is serial and costs ~8 round trips per
  replicate (SI-012), and every one of them now traverses two hops. The measured effect is in
  SI-023's cycle table: 66–78 s for a paused sixteen-replicate fleet, 126–262 s live, worst
  observed 842 s. The 30-minute main cadence absorbs this; a tighter one does not.

**Host keys were accepted trust-on-first-use during provisioning, and that is not closed.**
`known_hosts` gained the gateway's entry at first connection and the cluster's entry is
unchanged from `known_hosts.old`, which is consistent and suggests nothing is wrong. But *"the
alias resolves and authenticates"* is not the same claim as *"it authenticates the right host"*,
and the record holds no fingerprint to check either key against. **Non-blocking, and noted here
as the record's own gap** (REPORT 003 §5; PI 2026-08-30: fingerprints to be verified against
the retired Mac's `known_hosts` on the PI's return). The rule for the next host move: **carry
the expected host-key fingerprints in the record, or a rebuild has nothing to verify against
and TOFU is the only option available to it.**
