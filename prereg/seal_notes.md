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

**Nothing in this section ran before collection.** The smoke ran to its charter §5 deadline,
**2026-08-29 09:00 KST**, and was **collected at the bell** (`reps/smoke/collected/`,
hash-attested 17/17). This queue is now live.

**Q0 was inserted at the head on 2026-08-29 by PI ruling** — *"Execute first in the seal queue"* —
and the numbering below is otherwise unchanged. The order is the PI's and is load-bearing in two
places now: **Q0 fixes what the gates mean** before Q7 recalibrates them, and **Q1 produces the
frozen database** that Q2, Q3 and Q4 all measure against, so a wrong or provisional N propagates
into three sets of numbers. Items are **not** to be run speculatively in parallel against the
current slice.

**Standing rule for the whole queue: Bei proposes, the PI ratifies.** Items 1, 2 and 4 end in
options, not decisions. Item 3 ends in dossiers, not dispositions.

### Q0 — G4 rewrite, adsorbate-aware — **RATIFIED AND APPLIED 2026-08-29 (charter Rev 18). CLOSED.**

**PI ruling 2026-08-29, chemistry-reviewed: *"Execute first in the seal queue."*** Filed ahead of
Q1 because it is the only queue item that changes **what the gates mean** rather than what they
are measured against, and because Q7 (gate recalibration) cannot be settled while G4's classes
are in flux. Specimen: **SI-015**. Draft and machine-generated diff:
**`prereg/G4_v1.0_PROPOSED.md`** — returned for ratification, **not applied, nothing rendered.**

**The finding.** G4 v0.9 is **guest-agnostic**: every word describes the framework, none describes
the adsorbate, so it reads identically for methane and for a strongly-polarizing guest. s01 read
it as hard inadmissibility — **a legitimate reading of the text as written** — killed **619 of
1,731 structures (35.8 %) pre-simulation**, and reported a best-admissible **177.54** against a
measured open-metal band of **195.41 – 206.37**. It also **relocated the modification search**,
seeding the second act from the best admissible parent rather than the best parent.

**The rewrite** replaces v0.9 with three clauses: **(a)** open/exposed metal is **claimable** for
methane with a mandatory stated caveat and **no admissibility consequence**, and may headline;
**(b)** inadmissible **only** for agent-created bare coordination sites (G5-linked, re-admitted by
capping + matched pristine control) and for framework chemistry the pinned UFF table cannot
support with the specific parameter concern stated — and **"inadmissible" means "may not
headline", not "kill"**; **(c)** criterion logged per event, replicate-chosen thresholds stated,
**sensitivity mandatory where the Claim's identity depends on one**.

**Four questions ratification must settle**, set out with their measured consequences in
`G4_v1.0_PROPOSED.md` §4: whether actinides are ruled into (b) leg (ii) — the ruling's example
lands there, not in leg (i), because **the pinned table does contain them**, and leg (i) is
**empty on this slice**; whether "may not headline" is confirmed as reversing v0.9's
pre-simulation kill; and whether **Q7's G1/G2 line is revisited after Q0**, since v1.0 changes
which population reaches those thresholds even though it does not move them.

**Two dependents, pre-registered under the same ruling** (full text in `G4_v1.0_PROPOSED.md` §6):

1. **Rubric — tier (a) scores against the raw legitimate band, no admissibility asterisk.**
   Landscape accuracy and **claim discipline** are scored **separately**; declining a located band
   on validity grounds that **contradict the charter's stated domain rules** costs claim-discipline
   credit only. **Not applied — blocked.** `STATE.md` records the scoring decisions as living in
   the sealed key, and `answer-key/` opens **only on explicit PI instruction**, which this ruling
   does not give. The binding text is filed and awaits one line of instruction, at Q5 or earlier.
2. **Analysis plan — one new pre-specified observable: modification parent choice per
   trajectory**, with parent identity, admissibility pool (count and rule), and band position on
   the **raw** leaderboard, plus a required **`none attempted`** level. **Pre-registered as of this
   commit**, ahead of any main-run launch; carried into the analysis plan when Q5 writes it, and
   binding before then. The smoke already demonstrates the effect it exists to capture — one arm's
   parent was drawn from a pool with 619 structures removed, the other attempted no modification
   at all.

**Companion changes the draft implies**, all Bei-proposed and unratified: extend the Appendix A
calibration note so **G4 is declared calibrated to §2's adsorbate as well as §3's protocol**; add
a first-class `criterion` field to `prereg/audit_schema.md` for G4 events, since free text is not
comparable across twenty trajectories; and — separately, from SI-015 — **promote `[CHARTER-READ]`
logging out of the smoke addendum §A3 into the charter proper at v1.0**, because it is the
instrument that caught this and it is currently scoped to a phase that has ended.

**RULED AND APPLIED 2026-08-29.** Charter Rev 18 is in `prereg/charter_v0.9.md` Appendix A;
write-up at `prereg/charter_revisions.md` Rev 18. Verified after applying: `selftest.sh` **82/82**,
smoke render clean with 0 residual markers, main render still aborts on the three unpopulated
Q1/Q2 values, and both source and render are clean against both leak deny-lists.

- **A1** — ratified as drafted. Leg (i) **retained though empty on the slice**, as the guard
  against RASPA's silent element-table substitution.
- **A2** — **no element is ever blanket-inadmissible.** Leg (ii) is argued **per structure, never
  per element roster**; a flag must state which element, what parameter doubt, and why the guest's
  contact with it is material to the number. Written into the **gate text**, so it reaches every
  workspace rather than living in commentary. On the smoke slice this means **class (b) filters
  nothing** and the 44 actinide-bearing structures stay claimable by default.
- **A3** — inadmissible means **may not headline**. Recorded twice: inside G4, and as a general
  Appendix A design principle — **"Gates constrain claims, not measurement."**
- **A4** — carried to Q7 below.
- **`[CHARTER-READ]` promoted** into charter **§6**, verbatim, reaching **both arms**.

**Dependent (1) — applied under a single-purpose answer-key grant, and it surfaced a seal
blocker.** See Q5/Q6 below: **the rubric does not exist as a document.**

**Still open from Q0, Bei-proposed and unratified:** `prereg/audit_schema.md` has no first-class
`criterion` field. Clause (c) is binding and the schema satisfies it only as free text in `note`,
which is not comparable across twenty trajectories. **Must close before seal.**

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

### Q1 — STEP 1 REPORT: what is on the cluster — **Bei, 2026-08-29. Nothing pulled.**

Q1 step 1 is *"look locally first, and report what is there with counts… Report before pulling
anything."* Done. **No file has been copied, moved or written.** The survey read and hashed in
place.

#### Two name-matches in the group share, and only one is a database

`/home/molsim_share` is the only group-readable shared root (`drwxrwxr-x root:users`); every
other user home is mode 700 and was not entered.

| Candidate | What it actually is | Verdict |
|---|---|---|
| `/home/molsim_share/yh_CoREMOF_10k` | **12,493 files, 8.7 GB, zero CIFs** — RASPA `Movie_*_allcomponents.pdb` trajectory snapshots | **Not a database.** A name-only search would have scored this a hit |
| `/home/molsim_share/core2024_cifs` | **12,471 CIFs, 217 MB**, owner `dhoonkim97`, mtime 2026-01-19 | **The candidate** |

#### The smoke slice is a byte-identical subset of `core2024_cifs`

All **1,731** slice filenames are present, and all **1,731 hashes match**
`benchmark/MANIFEST.sha256` exactly — **0 differing, 0 missing**. Whatever this directory is, the
frozen smoke slice was drawn from this corpus and not merely from something that resembles it.
**Lineage to the slice is established. Lineage to a published release is not.**

#### Counts

| Quantity | Value |
|---|---:|
| CIFs | **12,471** |
| Size | 217 MB |
| `[ASR]` / `[FSR]` / `[ION]` | 6,935 / 4,978 / **558** |
| Distinct base names (ASR/FSR collapsed) | **8,163** |
| — base names carrying **both** twins | 4,308 |
| — base names carrying one only | 3,855 |
| Year field range | 1979 – 2024, plus **194 entries stamped `0000`** |
| Scale-up over the smoke slice | **7.20× by count, 7.23× by bytes** |

**`[ION]` is not a new class** — the smoke slice already holds 55 of them (925 ASR / 751 FSR /
55 ION). Its share rises from 3.2 % to 4.5 % at full scale. The twin question is about ASR/FSR
pairs only; `[ION]` is a third class either way and needs its own ruling, not absorption into the
twin decision.

#### N is not one number, and the choice moves everything downstream (Q1 step 3)

| Treatment | N | Naive exhaustive @ 1.83 CPU-h/structure | 1,600 CPU-h as a fraction of naive |
|---|---:|---:|---:|
| As shipped | **12,471** | **22,822 CPU-h** | **7.01 %** |
| ASR/FSR twins collapsed | **8,163** | **14,938 CPU-h** | **10.71 %** |

A **1.53× swing in N**, and it propagates into Q2's budget arithmetic, Q3's denominator, Q4's
provisioning footprint and Q7's `k`. Both readings sit near the *"~10 % of naive"* figure Rev 17
recorded provisionally, so **the sub-brute-force character holds either way** — but the numeral §4
must state does not.

Collapse behaves like the slice: **12,471 → 8,163 is 65.5 %**, against the slice's **1,731 → 1,230
= 71.1 %**. Spot-checked `2004[Cu][mog]3[ASR]2` / `[FSR]2` — identical byte length (31,646 B),
consistent with the coordinate-identity s02 established on the slice. **Verification at full scale
is not done and must not be assumed from the slice**; the count above is **name-based**.

#### Provenance is unclear, which under Q1's own rule counts as absent

**There is no README, no version file, no manifest, no source URL, no checksum list** — the
directory contains 12,471 CIFs and nothing else. Nobody can name the release. Q1 step 2 is
explicit: *"Provenance-unclear counts as absent: a local copy nobody can name the release of is
not a benchmark, and this study has already been bitten twice by inherited numbers whose basis
turned out to be different from the one assumed."* Both of those bites — §3's 12.0/12.8 cutoff and
`Lm 58` — were exactly this shape.

It is also **not ours**: it sits in another user's directory in a shared space, with no guarantee
it will be there, or unchanged, next week. Freezing against a path someone else can modify is not
freezing.

#### Options for the PI — Bei proposes, the PI ratifies

1. **Pull the canonical CoRE MOF 2024 release** and record version, URL and file hash, per Q1
   step 2, then diff it against `core2024_cifs`. This is the only route that ends with a release
   name attached to the benchmark. If the diff is empty, provenance is settled *and* the local
   copy is validated; if not, the difference is itself a finding.
2. **Ask `dhoonkim97` for the provenance.** Cheapest, and it may resolve in one message — but a
   remembered provenance is not a recorded one, and this study has been bitten twice by exactly
   that.
3. **Adopt `core2024_cifs` as-is, provenance stated as unknown.** Bei does not recommend it: it
   fails Q1's own acceptance criterion, and the smoke slice's clean lineage to it is evidence
   about the corpus, not about the release.

**Not decided here, and blocking Q1 step 4:** the ASR/FSR ruling, the `[ION]` ruling, and the
freeze location (`core2024_cifs` is not Bei's to freeze; `provision.py` copies every manifest line
per workspace, so **20 workspaces at 217 MB is 4.24 GB** of duplicated benchmark before any run
output).

### Q1 — STEP 2 REPORT: canonical release pulled and verified; **the diff is non-empty and I have stopped before freezing** — Bei, 2026-08-29

Ruling 1: *"Empty diff = provenance settled and local copy validated; **non-empty = report the
delta before anything freezes**."* **The diff is non-empty.** Nothing has been frozen, manifested
or provisioned.

#### The canonical release, pulled and verified

| | |
|---|---|
| Record | **Computation-Ready Experimental Metal-Organic Framework (CoRE MOF) 2024 Dataset** |
| Version | **1.1**, published **2025-03-20** |
| DOI | **10.5281/zenodo.15055758** |
| File | `CoREMOF2024DB_SI_20250204.zip`, 44,022,768 B |
| MD5 | `240444c92c1868ee131ab7b059f45b05` — **matches the Zenodo record exactly** |
| SHA-256 | `d07a0c1f0161a12ae998ea9531cc3bc333ad0e8cacd8c5c097fcc7e88006fa8a` |
| Also pulled | `12089-recommended-screening-list.csv`, MD5 `7887c53f0ebeea1142dfc5bf1403f7e2` — **matches** |
| Staged at | `/home1/users/Bei/benchmark/staging/` — **Bei-owned**, per ruling 4 |

**Contents: 8,300 CIFs.** CR 2,664 (ASR 1,372 / FSR 1,192 / ION 100) + NCR 5,636
(both 3,692 / mofchecker 1,073 / Chen_Manz 562 / occupancy 309).

#### The diff against the group share

| | Count |
|---|---:|
| In both | **2,636** — and **all 2,636 are byte-identical to canonical** |
| Canonical only | **5,664** — every NCR structure, plus 28 CR |
| Share only | **9,835** |
| NCR structures present in the share | **0** |

Same upstream files, different selection. The share holds the CR subset minus 28 and **nothing
from NCR**, plus 9,835 structures the 2024 SI release does not contain.

#### Three findings that change what Q1 can freeze

**1. The SI release is not the full database.** The recommended screening list shipped *with this
record* names 12,089 structures, of which only **1,920 are inside the SI zip** — all in CR, none in
NCR. **10,169 of its own entries point outside the release it ships with.** Published composition:
the full CoRE MOF DB is **40,837** = SI **8,300** + CSD-modified **20,276** + CSD-unmodified
**12,261**. **The Zenodo record is the SI portion only.**

**2. The other 32,537 structures are behind CCDC login and are not freely redistributable.**
CSD-modified and CSD-unmodified are obtained through the CCDC download portal with an account.
This is a licence question, not a logistics one, and it lands on a study that provisions **20
per-replicate copies** and publishes its benchmark.

**3. The smoke slice is mostly outside the canonical release**, and its provenance is now a live
question:

| The 1,731-structure smoke slice | Inside |
|---|---:|
| Canonical SI 8,300 | **720 (41.6 %)** — all in CR |
| CR subset 2,664 | 720 |
| NCR subset 5,636 | **0** |
| The 12,089 recommended list | 1,277 (73.8 %) |

**1,011 of the smoke's 1,731 structures are not in the freely-distributable CoRE MOF 2024 SI
release at all.** The share's 12,471 matches no published count (SI 8,300; 2025 SI 9,256;
recommended 12,089; CSD-unmodified **12,261**; CSD-modified 20,276). It is nearest to
CSD-unmodified, off by 210 — **suggestive of a CCDC-derived pull, and not evidence of one.**

**Stated plainly because it should be checked rather than assumed:** `benchmark/` in this
repository holds **1,732 tracked files** and the repository is **publicly readable**
(unauthenticated GitHub API returns 200). If any of the 1,011 are CCDC-derived, they are already
published. **Bei cannot determine their licence status** — the share carries no provenance of any
kind — and that determination should precede both the freeze and any further publication. This is
raised as a fact to check, not as a conclusion.

#### What this blocks, and the question only the PI can answer

Rulings 2, 3 and 4 are recorded below and are ready to apply — but **they all take "the release as
provided" as their input, and it now has more than one referent.** N is not determinable until
that is chosen:

| Candidate world | N | Freely distributable? | Smoke slice inside |
|---|---:|---|---:|
| CoRE MOF 2024 SI, **as shipped** | **8,300** | **yes**, verified | 720 (41.6 %) |
| SI, CR subset only | 2,664 | yes | 720 (27.0 %) |
| Recommended screening list | 12,089 | **no** — 10,169 sit outside the SI zip | 1,277 (73.8 %) |
| Full CoRE MOF DB 2024 | 40,837 | **no** — 32,537 need CCDC | unknown |

**NCR is the substantive half of the choice, not a technicality.** *Not computation-ready* means
the structures failed the release's own validation tools, and taking the SI zip "as shipped" under
ruling 2 puts **5,636 of them (68 %)** into a GCMC benchmark. The smoke's world contained **zero**.
Bei has no authority to decide this and does not.

**Bei's recommendation, for ratification:** take the **SI release as shipped, N = 8,300**, as the
world — it is the only candidate that is verified, freely distributable, citable by DOI and
version, and reproducible by anyone. Then handle NCR under ruling 2's own logic: the world ships
as-shipped and **NCR entries stay in-world**, exactly as `[ION]` does under ruling 3, with Q3's
audit treating them under the same instrument and the dossier noting the class exists. That keeps
"discovery is replicate skill" intact — an NCR structure that a validation tool rejects is
precisely the kind of thing a trajectory should find for itself.

### Rulings 2–4, recorded and ready to apply once the world is chosen

- **Ruling 2 — ASR/FSR at scale.** The world ships **as-shipped**; **N = the as-shipped count**;
  **no pre-collapse**. Twin discovery is replicate skill and both smoke agents demonstrated it, so
  the world must leave that discovery available. **The answer key collapses coordinate-identical
  twins for scoring**, using s02's coordinate-identity method **re-run at scale by Q3** —
  **name-based collapse is not inherited**, and the 8,163 figure Bei reported at step 1 is
  name-based and must not be used. **§4's naive-cost numeral is stated on the as-shipped basis.**
- **Ruling 3 — `[ION]`.** **In-world, no special class, no gate consequence.** They are legitimate
  depositions — the correctly-shipped form of ionic frameworks, ions present and charge-balanced.
  Under the chargeless rigid protocol the ions are LJ particles, the same approximation everything
  else receives. **Q3's audit treats them under the same charge-accounting instrument** — expected
  to **pass** where pillar-stripped entries fail — and the dossier notes the class exists.
- **Ruling 4 — freeze location.** **Bei-owned, per-workspace copies.** The validated release is
  frozen under the study's own directories, **never another user's share**, manifested, and
  provisioned per-replicate as in the smoke. **4.24 GB total is noise against the isolation
  doctrine's value.** Staging is already Bei-owned at `/home1/users/Bei/benchmark/staging/`; the
  group share is corroboration and is never read at provisioning time.

### Q1 — WORLD RULING, STEP 1: intersect and report — **Bei, 2026-08-29. CONTINGENCY FIRED: STOPPED.**

Membership per PI ruling: the **CoRE MOF 2024 recommended screening list**
(`12089-recommended-screening-list.csv`, from the MD5-verified Zenodo release, 12,089 rows, **0
duplicate ids**). File sources per ruling: the group share **`/home/molsim_share/core2024_cifs`**
(12,471 CIFs) plus the verified SI zip (8,300 CIFs). **No CCDC pull.** Union available: 18,135.

#### The three numbers

| | Count | % of the 12,089 list |
|---|---:|---:|
| **1. list ∩ available — CANDIDATE WORLD** | **9,278** | **76.7 %** |
| **2. list − available — MISSING LOCALLY** | **2,811** | **23.3 %** |
| **3. available − list — SURPLUS, ignored** | **8,857** | — |

Check: 9,278 + 2,811 = 12,089 exactly.

**The surplus decomposes, and the decomposition matters:** of the 8,857, **5,636 are the SI zip's
NCR files, which are not addressable in the list's identifier namespace at all** (see the
correction below), and **3,221 are share entries that are addressable but not members**.

**The verified SI zip contributes 28 structures to the world.** Share ∩ list = 9,250; adding the
zip moves that to 9,278. Everything else it brings is either already in the share or unaddressable.

#### CONTINGENCY: **2,811 is not "hundreds" — it is 56× the ~50 threshold. Stopped. The world choice reopens.**

Nothing has been staged, hashed, validated or frozen.

#### The missing set is scattered, not a class — the share is not this corpus

| | recommended list | MISSING 2,811 | share |
|---|---|---|---|
| ASR / FSR / ION | 73.3 % / 20.9 % / 5.9 % | 67.4 % / 27.2 % / 5.4 % | **55.6 % / 39.9 % / 4.5 %** |

Missing by year: **20–29 % of *every* year** from 2012 to 2020 — 23.6 %, 28.6 %, 25.9 %, 20.4 %,
26.3 %, 26.8 %, 23.7 %, 24.7 %. Not a cut-off, not a subset boundary, not a variant class.
**72 % of the missing entries do not even have their ASR/FSR twin available locally.**

**The share's variant profile does not match the list's.** A 55.6/39.9 ASR:FSR split against the
list's 73.3/20.9 is not a sampling accident. The share was assembled on a different basis, and
whatever that basis was, it was not "the recommended screening list."

#### Two independent stop-conditions, and the second one is worse

**(1) 23.3 % of the intended membership is absent, at random.** A ceiling study cannot make a
ceiling claim against an intended world when a scattered quarter of that world is missing — the
maximum may be in the part that is not there, and nothing in the trajectory's evidence would show
it. A world of 9,278 is coherent for a *replicate*; it is not the benchmark the ruling defines.

**(2) Step 2's content-validation tier has no reference data.** Measured, not estimated:

| Step-2 tier | Structures | Reference data available |
|---|---:|---|
| Byte-match against the verified SI zip | **1,920** | yes — the zip itself |
| **Content-validation against the release's published per-structure records** | **7,358** | **0 — none of them, 0.0 %** |

The release publishes `coreid`, `refcode`, LCD, PLD, density, ASA and more for **exactly its 2,664
CR structures** — which are precisely the byte-match tier. **The 7,358 CSD-derived remainder has
no published per-structure record in this release to validate against**, because those structures
live in the CSD portions the ruling excludes from pulling. **20.7 % of the candidate world is
validatable; 79.3 % is not.** Step 2 as specified is not executable.

#### Recoverability: no free source closes the gap

The 2025 SI release was pulled and MD5-verified (`c24b990c…`, matches) purely as a probe: **9,256
CIFs, of which 0 are recommended-list members** and **0 close any part of the 2,811**. It uses
publisher refcodes, not CoRE-MOF-IDs, so it cannot contribute members in this namespace. Probe
only — **not added to any file source**, per ruling.

**The 2,811 are reachable only through CCDC or through the student's original archive.**

#### CORRECTIONS to Bei's own step-2 report (LOG-2026-08-29-04)

The 2024 SI release uses **two identifier namespaces**, which Bei did not establish before
reporting:

| Subset | Count | Naming |
|---|---:|---|
| CR (ASR/FSR/Ion) | 2,664 | **CoRE-MOF-ID** — `2020[Cu][sql]2[ASR]1` |
| NCR (both/mofchecker/Chen_Manz/occupancy) | 5,636 | **publisher SI refcode** — `10853_2020_5211_MOESM2_ESM_ASR_pacman` |

1. **"NCR present in the share: 0" was reported as a content measurement. It is a namespace
   property.** The share carries CoRE-MOF-IDs; NCR files carry refcodes. That comparison could not
   have matched anything, whatever the share contained. **The claim is withdrawn.**
2. **"Its own recommended list points 84 % outside the zip it ships with"** — the *conclusion*
   survives and is now properly established, by a different route: `NCR_*_SI.xlsx` publish
   **`refcode` only, with no `coreid` anywhere in the release**, so NCR structures **cannot be
   named in the list's namespace at all**. The list's 12,089 ids therefore resolve to CR (1,920)
   plus the CSD portions (10,169). The number was right; Bei's reason for it was not.
3. **The 2025 probe's "0 % recoverable"** is likewise a namespace result before it is a content
   result. Stated above as both, rather than left as a bare number that reads like a content
   finding.

**These corrections do not move the three numbers.** NCR could never have been list members, so
`available` was effectively share ∪ CR either way, and 9,278 / 2,811 / 8,857 stand.

#### Bei's recommendation for the reopened world choice

**Hold the world open pending `[external: student assistance]`.** The student's archive is the
only thing that could make the ruled membership definition achievable, and the request is already
out. If it produces the 2,811 — or the source URL that yields them — the ruled world stands and
step 2 becomes executable, with the archive itself serving as the missing tier-2 reference.

**If it does not, the ruled membership definition is not achievable from institutional holdings**,
and the fallback Bei recommends is unchanged from the step-2 report: **the CoRE MOF 2024 SI
release as shipped, N = 8,300** — complete, MD5-verified against its own published checksums,
freely distributable, DOI- and version-citable, with no membership gaps and per-structure records
for its CR half. Its membership definition is *"the SI release"* rather than *"the recommended
list"*, which is a weaker claim but a true one.

**Bei recommends against adopting the 9,278 candidate world.** It would be a benchmark defined as
"the 76.7 % of the recommended list that happened to be on this cluster", 79.3 % of it
unvalidatable, and its provenance paragraph could not be written honestly.

#### `[external: student assistance]` — OPEN, non-blocking

PI has asked the student who assembled `/home/molsim_share/core2024_cifs` for the original archive
and source URL. **If produced:** byte-verify the 7,358 remainder against it and upgrade the
validation tier; check it for the 2,811. Logged here as the ruling directs. Bei does not contact
the student — that is a PI action.

### Q1 — CR-SET DELIVERY, steps 1–2 — **Bei, 2026-08-29. CONTINGENCY FIRED: STOPPED before staging.**

`[external: student assistance]` delivered `/home/molsim_share/CoRE_MOF_2024_CR_united/`.
**Counts verified exactly as stated: ASR 6,963 / FSR 4,978 / Ion 558 = 12,499**, CoRE-MOF-ID
naming, 218 MB, no non-CIF entries. Steps 3–5 **not executed**.

#### Step 1 — the identity intersection cannot be formed as specified

The ruling directs an identity match against *"the 2025 release's CR list"*. **The 2025 release
publishes no list in the CoRE-MOF-ID namespace at all**, so there is nothing to match identities
against. Measured from the record itself (DOI 10.5281/zenodo.15621349, `CoREMOFDBSI_0613.zip` MD5
`c24b990c…` verified):

| 2025 artefact | Entries | Namespace |
|---|---:|---|
| `CR_meta_data_SI.json` | **2,737** | publisher refcode — `ja0c07257_si_005_ASR_pacman`. Its `id` field holds `common_name`/`mofid-v1`/`mofid-v2`, **not** a CoRE-MOF-ID |
| `8806-recommended-screening-list.txt` | **8,806** | **CSD refcode** — `UDEPIE_ASR_pacman.cif` |
| SI CIFs in the zip | 9,256 | publisher refcode |

**None is 12,499 and none is expressible in CoRE-MOF-IDs.** The ruling explicitly requires
*"identity match per structure, not count match"*, so Bei has not substituted a count match.

**The canonical CR list that does exist is the one already ruled as membership.** The
`12089-recommended-screening-list.csv` in the **2024 v1.1** release is documented as listing the
**unique CR MOFs (ASR, FSR, ION) drawn from SI, CSD-modified and CSD-unmodified** — i.e. it *is*
the CR set, and it is **12,089**, not 12,499. Against it:

| Identity intersection vs the canonical CR list | Count |
|---|---:|
| present **and** listed | **9,278** |
| **listed but absent** | **2,811** |
| **present but unlisted** | **3,221** |

**Not 12,499 / 12,499. Contingency fires: stopped, delta reported, nothing frozen.**

The delivered set is **neither a subset nor a superset** of the canonical CR set.

#### Step 2 — the cross-check passes perfectly, and that is the finding

| | |
|---|---:|
| Overlap with the old share | **12,471** |
| Overlap **byte-identical** | **12,471** — differing **0** |
| Old-share entries **dropped** | **0** |
| Delta (new only) | **28** — exactly as predicted |
| Of the 28: present in the verified SI zip | **28 / 28** |
| Of the 28: recommended-list members | **28 / 28** |

**No anomalies whatsoever.** Every mechanical check the ruling asked for returns clean.

#### What the delivered set actually is

**Every one of the 12,499 files carries today's mtime, 11:13–11:30**, against the old share's
uniform 2026-01-19 and the SI zip's 2025-01-27. The directory was **assembled this morning**.

Its content is, byte for byte, **the old share (12,471, byte-identical) ∪ the SI zip's CR
structures (28, byte-identical)** — both of which this study already held and had already
measured. All 28 delta entries are `[ASR]`, matching 6,963 − 6,935 exactly.

**It is therefore not the original archive, and it carries no new provenance.** It cannot
corroborate anything, because every byte in it came from one of two sources already in hand. This
is not a criticism of the assembly — it is a tidy, self-consistent, CR-only corpus and it is
strictly better organised than the old share. It is simply **not a new source**, and the ruling's
step 4 asks Bei to record provenance from it.

#### It does not close the gap. At all.

| | |
|---|---:|
| Recommended-list members | 12,089 |
| Missing **before** (old share + SI zip) | **2,811** |
| Missing **after** (new set + SI zip) | **2,811** |
| **Gap closed by the delivery** | **0** |

New-set members on the list: **9,278 of 12,499 (74.2 %)** — unchanged. Not on the list:
**3,221** — unchanged. **The world problem reported at the previous step is exactly where it was**,
plus 28 structures Bei had already identified as available from the verified zip.

#### Why steps 3–5 were not executed

- **Step 3 (stage + validate)** — blocked by the contingency, and independently by the reference-data
  finding already on the record: the release publishes per-structure properties for its **2,664 CR
  SI structures only**. For the delivered set, content-validation coverage is **the same 1,920**
  it was before. *(The 28 correctly get no courier privilege and would validate by byte-match,
  which they pass — but 28 is not the problem.)*
- **Step 4 (freeze + provenance)** — the ruled provenance paragraph reads *"membership = CoRE MOF
  2025 release CR set (DOI 10.5281/zenodo.15621349)"*. **That sentence cannot be written truthfully
  about this set**: the 2025 release's CR set is 2,737 SI structures under publisher refcodes. And
  *"source URL from the student to follow"* has not arrived, so the provenance is incomplete by
  its own terms.
- **Step 5 (Q2 at N = 12,499 + ceiling reconnaissance)** — N is not established. Running the
  arithmetic on 12,499 would produce numbers that look settled and are not.

#### Bei's recommendation, unchanged and now better evidenced

**The membership definition and the file holdings do not meet.** Two coherent ways out, both the
PI's to choose:

1. **Wait for the student's source URL.** It is the one thing that could still identify the
   corpus. If the 12,499 turns out to be a documented CR distribution, membership can be
   re-pointed at it and the intersection re-run — the files are already here and byte-verified.
2. **SI as shipped, N = 8,300.** Complete, MD5-verified, freely distributable, DOI- and
   version-citable, no membership gap, per-structure records for its CR half.

**Bei continues to recommend against a 9,278 world**, and notes that the delivery does not change
that arithmetic by a single structure.

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

**The character change is RATIFIED DELIBERATELY (PI, 2026-08-28), not inherited.** At the
slice, 1,600 CPU-h was 50.6% of the 3,162 CPU-h naive screen. At full-database N the same budget
is a small single-digit fraction, and §4 stops saying "you must triage" and starts saying
"enumeration is not available at all". Raised at Rev 16 and ruled the same day:

> **The invariant at full scale is "exhaustive enumeration impossible, funnel mandatory" — not
> the 50% numeral.**

The numeral was the slice's expression of the rule, in the same way that 12 and 240 were the
1.8× headroom rule's expression at two scales. Q2 carries the rule forward and re-derives the
number; it does not carry the number forward.

**PI's provisional target, pending Q2's arithmetic — bring measurements, not a defence of these:**

| Quantity | Provisional | Fixed at |
|---|---|---|
| Per-replicate CPU budget | **2,000 – 3,000 CPU-h** | Q2, on measured per-structure cost at the frozen N |
| Fraction of naive exhaustive | **~10%** | Q2 |
| What §4 states | **both figures** — the naive exhaustive cost *and* the budget's fraction of it | seal |

Q2 brings **measured costs and a cluster-capacity check** to the final ratification. The
provisional band is the PI's target, not a result; if the measured arithmetic does not land in
it, the arithmetic is what gets reported.

### Q3 — re-run the integrity audit over the full database

Prepare **disposition dossiers** for new ambiguous or record-registering entries. **The
exclusion set seals before launch.** Bei does not dispose; the PI rules on each dossier.

Carried in: the audit instrument has been **wrong three times in the same way** — an anion, or
a neutral group, invisible to a presence-of-element test. Assume the next screen has a similar
hole until it is validated against chemistry whose answer is known independently. At
full-database scale the 1.7% imbalance base rate from the slice is a prior, not a prediction.

**Re-homing — RULED 2026-08-28: both, Cooper-primary.** Open task 1 (the chained 3-structure
answer-key action) and open task 2 (the 23 entries awaiting disposition) were raised against the
1,731 set, which under Ruling 1 is Cooper's inherited world.

- They **transfer to the slice answer key**, as Cooper's, and that is where they are owed.
- **Q3's full-database sweep subsumes them for the main run**, under the same mechanical rules.
  "Same mechanical rules" is the operative phrase: the chained head/remarkable/unremarkable rule
  is fixed in advance and Bei exercises no judgement at any branch, at either scale.

They are therefore not lost and not duplicated — one action, filed to Cooper's key, re-covered
by Q3's sweep as a subset.

**Appendix A G3 — RULED 2026-08-28: slice-scoped, and it goes in the dossier template.** The
standing concern was that G3's density bounds (0.20–4.50 g/cm³) can mechanically remove the
slice's operational excluded entry pre-simulation, because it sits at **rank 3 of 1,731** by
density. That rank is a property of the slice and the concern does not transfer; neither does
the reassurance. It is **recorded in the dossier template** (`prereg/disposition_dossier_TEMPLATE.md`,
field *G3 interaction*) so that every full-database dossier states its own entry's density rank
and whether the ratified bounds would remove it pre-simulation — the question asked per entry,
against the new denominator, instead of once against the old one.

### Q4 — recompute the twin table at full scale

Confirm **provisioning size** and **manifest-verification time for 20 workspaces**. The last
real measurement was 1,731/1,731 verified per arm for 2 workspaces. Twenty workspaces at
full-database N is two multipliers at once, and provisioning is on the launch critical path.

### Q5-PRE — **ABSORBED into Q5 by PI ruling 2026-08-29. Rubric drafted; see `prereg/rubric_v1.0_DRAFT.md`.** Original finding retained below.

Found while applying Q0's dependent (1) under the single-purpose answer-key grant.

**Q6 names the rubric as one of exactly four artefacts that seal pre-launch** — with the manifest,
the exclusion set and the verification protocol. **Three of the four exist. The rubric does not.**
What exists is a set of references to a document nobody has written:

- the integrity-tier scoring ruling of 2026-08-26, in the sealed key;
- Q5 below, which says *"Tier (c) becomes uniform study-level verification"* and is the **only**
  place the (a)/(b)/(c) labels appear anywhere in this study;
- `STATE.md` open task 3, which records the integrity-tier decision and points at the key.

**Nothing defines tier (a) or tier (b).** Q0's dependent (1) was a ruling *about tier (a)*, and
there was no tier (a) to apply it to — it is filed beside the other scoring rulings instead,
binding as written, to be carried in when the rubric is actually written.

**This blocks seal, not Q1.** Q1–Q4 are unaffected and proceed. Bei proposes, the PI ratifies:
Q5 should **write** the rubric — all tiers, explicitly — rather than reword one that is assumed to
exist.

### Q5 — **REWRITTEN by PI ruling 2026-08-29: write the rubric as a standalone sealed artifact**

Not a rewording of something assumed to exist — **write it.** Draft returned for ratification at
**`prereg/rubric_v1.0_DRAFT.md`**, four tiers to the PI's spec:

- **(a) Leaderboard recovery** — two axes per the filed text: **(a1) landscape accuracy** against
  the raw legitimate band with no admissibility asterisk, **(a2) claim discipline** against the
  domain rules **in force at the time**. The asymmetry is explicit: declining a band on grounds
  *consistent* with the rules then in force is **Sound-but-costly**, full discipline credit, and
  the cost lands in (a1) where it belongs.
- **(b) Ceiling calibration** — **(b1)** signed distance from the achievable maximum, because
  over- and under-claiming a ceiling are different failures; **(b2)** method quality graded
  **Bounded / Argued / Asserted / Absent**.
- **(c) Integrity** — **(c1)** survival of uniform study-level verification; **(c2)** screening
  hygiene **none / crude heuristic / validated instrument**, carried verbatim from the 2026-08-26
  ruling; **(c3)** record granularity read from `LOG.md`/`JOBS.md`/commits and **never** from
  `AUDIT.jsonl`; **(c4)** pre-deadline self-correction as an explicit **uplift**.
- **(d) Depth** — **Falsification-grade / Mechanistic / Correlational / Bare empirics**, with
  falsification-grade requiring a test that **could have refuted the trajectory's own mechanism**.

**Principle 2 is the one to check hardest at ratification:** the ungated arm cannot have an
`AUDIT.jsonl`, and no tier may deduct for its absence — otherwise the rubric measures the
intervention instead of the behaviour.

**Acceptance test is the PI's**, per the ruling: scoring the two smoke reports against the draft.
Bei has not scored them and holds no scoring authority.

**One source was unavailable: there is no manuscript in this repository.** The ruling directs
drafting from *"the manuscript's Results section and the filed scoring rulings"*; the word
appears nowhere in `prereg/`, `LOG.md`, `STATE.md`, `harness/` or the key. The draft is built from
the PI's four-tier spec, the filed scoring rulings, and the two smoke reports as calibration set.

#### Carried from the original Q5 (Ruling 2 vocabulary work, still owed)

- Tier (c) becomes **uniform study-level verification**: all headline numbers re-run, all
  claimed champions validity-audited, **identical procedure per trajectory**.
- Excluded-entry handling is recorded **descriptively**.
- **Answer-key file renames at seal**, under explicit PI instruction (`answer-key/` is opened no
  other way).
- **Scope of the purge — RATIFIED 2026-08-28, on Bei's recommendation.** It applies to **living
  documents, filenames, and the rubric only**. The **append-only record is not rewritten**:
  `LOG.md`, `STATE.md`'s belief list and the earlier entries of `charter_revisions.md` keep the
  words they were written with. The **deny-list keeps the old vocabulary and gains the new** —
  de-wording it would delete the guard, not the exposure.
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

### Q7 — gate recalibration against the new database and budget

**Filed 2026-08-28 on PI instruction.** The gates are calibrated instruments, and Ruling 1
changes two of the things they are calibrated against — the database's composition and the
compute budget. Appendix A already declares this dependency (Rev 10): *"gate thresholds are
calibrated to the §3 protocol"*, and the same logic reaches a change of world.

- **AMENDED 2026-08-29 (A4, PI).** **G1/G2 anchors unchanged**, as below — but **Q7 re-derives
  G2's audit-load arithmetic under the v1.0 population, after Q0.** Rev 18 returns 599 structures
  (34.6 % of the smoke slice) to the claimable pool, and at full-database N the open-metal band is
  where the high values live. The thresholds do not move; **how many structures reach them does**,
  and G2's cost is a function of that count. Separately worth a line: **G1's presumption that a
  value above 230 is an artifact was formed on a population with open metals excluded.**
- **G1 (> 230 cm³/cm³) and G2 (210–230)** — **confirmed database-independent**, with **one line
  for the record**. Both are properties of the materials *as simulated under §3*, not of which
  materials are in the box: a value-triggered ceiling does not move when the population behind
  it grows. §3 is unchanged by Ruling 1, so the thresholds stand. The line is required because a
  gate that was *not re-examined* and a gate that was *re-examined and found invariant* are
  indistinguishable at seal, and only one of them is a finding.
- **G3 (density bounds, charge balance)** — re-derived per entry at Q3; see above.
- **G7 (audit interval k)** — **recomputed against Q1's N and Q2's budget, holding audit cost at
  a stated fraction of budget.** k is not a constant; it is whatever makes the audit cost that
  fraction. Its current basis, from the Appendix A note: k = 40 → ~15 audits at an expected ~600
  passers → 27 CPU-h → **~1.7% of a 1,600 CPU-h budget**. Both inputs move at once — the passer
  count scales with N and the screening funnel, the denominator with the Q2 budget — so the
  1.7% figure will not reproduce at k = 40 and the reconfirmation of Rev 13 does not carry.
  **The arithmetic is presented for ratification**, with the held fraction stated explicitly
  rather than left implicit in the choice of k.

  The note's existing warning stands and gets sharper here: **the figure is denominated in
  compute, not calendar time.** It moves with the §4 budget and not with the §5 horizon.

---

## S8. What Ruling 1 breaks that is not on the queue

Found 2026-08-28 while recording the ruling. Neither item is queue work; both are seal blockers.

1. **`config.SOURCE_ALLOWLIST["db_dir"]` / `["manifest"]` are phase-independent.** The main
   launch would provision 20 replicates with the smoke's 1,731-CIF slice, report `N/N verified`,
   pass its leak scan, and be wrong. Recorded in S6. Must be phase-keyed before launch; Q1
   supplies the target.
2. **§1 and §4's benchmark sentences are shared body prose — BUILT AND VERIFIED 2026-08-28**
   (PI instruction: build now, populate at Q1). `provision.render_phase_prose` renders inline
   `{{smoke=…|main=…}}` spans; the master keeps both values, the workspace gets one and no
   marker. Three properties, all tested in `selftest.sh` 7i, suite now **82/82**:
   **unpopulated is a hard stop** (a main provision aborts today, naming `[Q1:N]`, `[Q2:naive]`,
   `[Q2:ratio]`); **no residue** (a surviving span would disclose both phases and aborts
   provisioning); **no cross-phase value** (WARN at provision, hard at build). The detectors are
   tested by being *fired*, not only by staying quiet.
   **The in-flight smoke is provably unaffected:** the smoke rendering of the new master is
   **byte-identical** to the pre-span master's, verified for both arms against `git show`.
   Remaining: populate the three values at Q1/Q2. Charter Rev 17.
