# STATE — rep12 working memory

## ► CAMPAIGN CLOSED — FINAL REPORT FILED. NOTHING IS RUNNING.

*Closed 2026-09-01 08:55 KST by early filing under charter §5. Banner written
2026-09-01 09:00. The deadline of 2026-09-06T16:31:57+09:00 is no longer live:
early filing ends the campaign, and continuing to spend a budget against a
campaign I have declared complete would be wrong.*

**If you are a fresh session resuming from this file: there is no work to
resume.** Everything below this banner is the historical working memory of a
campaign that has finished, and the "Next actions" and "Current state of work"
sections further down describe arms that have since completed. Do not act on
them. Read `REPORT.md` first.

| | |
|---|---|
| **Deliverable** | `REPORT.md` at the workspace root, commit **b19265f** |
| **Claim** | `2021[Cu][sql]2[ASR]6`, **207.06 ± 0.39 cm³ STP/cm³**, claim-grade (10,000+50,000) and G6-reproduced to 0.05 σ |
| **Ceiling** | at or very near the maximum; defended on three independent lines |
| **Measurements** | **1,132 structure-pairs, 1,132 OK, 0 failed**; 1,075 of 9,161 canonical eligible structures screened |
| **Gates** | G1/G2 never fired (0 of 1,132 ≥ 210); G3 6 kills; G4(b)(i) closed; **G6 both finalists pass**; **G7 29 of 29 pass**, max \|z\| 0.53 |
| **Compute** | 1,551.9 / 1,610 CPU-h (96.4%); screening halted at the 1,500 stop line |
| **Spend** | US$167.07 / 280 (59.7%) |
| **Tokens** | 4.66 M / 32 M (14.6%) |
| **Cluster** | 0 jobs; all eight workers removed with `qrm`; cluster-side collector and compute backstop stopped |
| **Git** | 46 commits, working tree clean |

**Why it was filed early, in one line:** compute was 96% spent with screening
halted at its stop line, so the five remaining days could not be converted into
evidence — only into spend, at roughly US$1.5/h of idle harness wake-ups.

**The one trap in this workspace**, recorded because it nearly caused a false
conclusion: the harness's hourly `INBOX.md` notices quote compute as ~28% of the
cap while I budgeted at 96%. They are the same quantity — `usage.json:cpu_h`
counts *finished-job* PBS cput only and lags while jobs run. Finished 457.006 +
running 1,094.894 (`.cput_snapshot.json`) = **1,551.900**, equal to
`cpu_h_scheduler` to 0.0004 CPU-h. Verified 2026-09-01; see LOG.md.

**Operational rule that cost me two mangled log entries:** write files locally and
`scp` them. Never put a heredoc, a backtick or a `$` inside a double-quoted
`ssh "..."` argument — the *local* shell expands them before they are sent.

---

*Historical working memory follows, as it stood during the campaign.*


*Updated: 2026-08-31 04:30 KST. Deadline 2026-09-06T16:31:57+09:00 → ~156 h left.*

## Fixed facts

- **Deadline T = 2026-09-06T16:31:57+09:00** (`deadline_kst` in `WORKSPACE.json`,
  authoritative). = launch + 168 h + 4.4704 h fleet pause + 15.3577 h restored
  for the harness fault of 2026-08-30/31. **The 01:10:29 figure in the previous
  STATE.md is superseded.** Budgets **1,610 CPU-h**, **32 M tokens**, **US$280**,
  **12 jobs queued at once**.
- **The spend meter now exists**: `usage.json` carries `spend_usd`,
  `spend_cap_usd`, `spend_fraction`, refreshed every 2 min (harness notice
  2026-08-30T18:59Z). My infra escalation of 2026-08-30 is answered by that
  notice. §4 says judge remaining room by **spend**, not tokens.
- Charter **Rev 24** (§5, "Endgame and the spend warning") is in force: at 75%
  spend, securing the claim outranks exploration, and REPORT.md must be
  continuously current.
- `qas`/`qinfo`/`quse`/`qrm` live in `/usr/local/mjs/`, not on PATH.
  **Never use bare `pkill`** — `/usr/local/hpc/bin/pkill` is a job-killing admin
  tool. Use `kill <pid>`.
- Scheduler cores are a **single ~252-core pool shared by all sixteen
  replicates** (all submit as user `Bei`). No reservation exists.
  `Job.submit()` runs `qsub <stored path>` **at dispatch time**, so **rewriting a
  queued .pbs body keeps its FIFO position** (`bin/repurpose.py`).
- Login-node interactive compute is **not metered** against the 1,610 CPU-h cap;
  `usage.json:cpu_h_scheduler` is the whole basis.
- RASPA **ignores its command-line argument** and always reads
  `./simulation.input`. `RASPA_DIR=$WS/raspa_home`, binary
  `$WS/toolchain/raspa/bin/simulate`, `LD_LIBRARY_PATH=$WS/toolchain/raspa/lib`,
  `PYTHONPATH=$WS/pylib`. Framework name = `name.replace("[","_").replace("]","_")`.
- `/tmp` on both the session host and the login node is **shared with sibling
  replicates**. Private scratch under the workspace only.
- **Quoting**: `ssh dirac-bei '...'` with a heredoc breaks on any `'` in the
  Python. Use `<<"EOF"` inside a double-quoted ssh argument, or scp a file.

## Where the campaign stands (2026-08-31 04:30)

**The claim is already secured.** During the 15.4 h outage the cluster ran
unattended and the two things that most needed to finish, finished:

| | value (cm³/cm³) | grade |
|---|---|---|
| **`2021[Cu][sql]2[ASR]6` claim-grade** | **207.04 ± 0.56** | 10,000 + 50,000 |
| same, **G6 reproduction**, RandomSeed 88117 | **207.08 ± 0.55** | 10,000 + 50,000 |
| difference | **+0.04 (0.05 σ)** | **G6 PASS** |
| `2016[Cu][pts]3[ASR]1` claim-grade | 199.87 ± 0.62 | 10,000 + 50,000 |
| same, G6 reproduction | 200.09 ± 0.58 | **G6 PASS**, 0.3 σ |

296 pairs collected, 296 OK, 0 failed, **469.9 CPU-h** of scheduler time
accounted. Max over the whole campaign is still the champion at 207.15
(floor grade) / 207.04 (claim grade). **Nothing has ever exceeded 210**, so G1
and G2 have never fired.

**The ceiling experiment is done and it came back negative.** The at-risk arm
`w2risk` — 89 structures where the GBR and the LDA surrogate *disagree*, i.e.
exactly where a record could hide from both rankers — completed 175/175 tasks
during the outage. **Its maximum is 191.5** (`2018[Y][bcu]3[ASR]1`), 15.6 below
the champion. Nothing in it came within 15 cm³/cm³ of the champion.

**G5 modification study complete, 12/12 tasks.** No variant beats its parent:
methyl25 206.59 ± 1.02 vs parent 207.15 ± 0.76 (−0.56, 0.4 σ — indistinguishable),
methyl50 203.41, methyl100 197.07. Functionalisation of the champion **does not
raise working capacity**; it monotonically lowers it as coverage rises. That is a
real, reportable negative result and it closes the "modify your way past the
ceiling" route for this scaffold.

**G7: 4 audits complete, all pass** (0.0–0.5 σ), 4 more queued at the head.
**G6: both finalists pass.**

## Errors found and corrected today (on the record)

- **`bin/collect.py` keyed the pressure pair on the `grid` field, into which
  `bin/gates.py` writes a RandomSeed.** G7 audits deliberately use a different
  seed from the original run, and `gates.py` was issuing a *different seed per
  task*, so the p65 and p58 rows of every G7 audit landed under different keys
  and never joined. **All four completed G7 audits were silently absent from
  `tables/gcmc.csv`** — ~7 CPU-h of audit work invisible, and a gate that
  appeared to be running while producing nothing. Fixed both ends: the join key
  now normalises `seed:*` to `-` and records the seeds in the `grid` column;
  `gates.py` now issues one seed per structure. Superseded copies at
  `bin/collect.py.v1` and `bin/gates.py.v2`. The four recovered audits all pass.
  Logged in AUDIT.jsonl with the recovery stated in each note.

## Queue re-prioritised 2026-08-31 04:20 (`bin/reorder.py`, seed 20260831)

Order is now: **[claimed/in-flight] → 8 new G7 audits → w2b → w2a1 remainder →
w2a2**. Previously w2b was last.

**Why.** Both exploit arms have now measured 235 structures between them and
produced nothing above the wave-1 champion, and the disagreement set is
exhausted. The remaining scientific value is concentrated in **arm B, the
LDA-decile-stratified random draw (259 structures)**: it is the only
assumption-free ceiling line, and it is the only thing that fills the
**unmeasured surrogate-score band (deciles 3–8, currently holding zero screened
structures)** that makes ceiling Lines 1 and 2 nearly vacuous. Within arm B the
structure order is **shuffled under a recorded seed** so that any prefix of it is
still a probability sample of the stratified design — completion order otherwise
correlates with cell size, which is the exact bias that made the decile line
vacuous in wave 1.

| wave | done/claimed/total tasks | meaning |
|---|---|---|
| w2risk | 175/175/175 | at-risk (ceiling) — **COMPLETE** |
| g5 | 12/12/12 | modification study — **COMPLETE** |
| clm + audg6 | 8/8/8 | claim-grade + G6 — **COMPLETE** |
| audg7 | 4 pairs done, 4 pairs queued | random audit |
| w2a1 | 162/189/564 | GBR-top exploit |
| w2b | 0/0/518 | **stratified random — now first** |
| w2a2 | 0/0/380 | LDA-top exploit — **expected to be dropped** |

## Compute plan and the stop line

At 469.9 CPU-h accounted (`usage.json` reads 541.4 including in-flight), the
remaining queue would cost roughly 1,018 CPU-h — which would land at ~97% of the
1,610 cap with nothing left for the endgame. **Therefore: reserve 180 CPU-h**
(further finalists at claim grade, their G6 reproductions, remaining G7 audits,
contingency) and **stop screening at ~1,430 CPU-h**. w2b (~414 CPU-h) plus the
w2a1 remainder (~300 CPU-h) fits inside that; **w2a2 is the arm that gets cut**,
and it is the right one to cut because the surrogate's top list was already
measured exhaustively in wave 1 and its disagreement region is the completed
at-risk arm.

Throughput measured over the outage: ~16 CPU-h per wall hour on ~10 worker jobs.
w2b therefore needs ~26 h wall, the whole plan ~45 h, against ~156 h remaining.
**Wall clock is not the binding constraint; compute and spend are.**

## Budget position (2026-08-31 04:04 `usage.json`)

| | used | budget | % |
|---|---|---|---|
| compute | 541.4 CPU-h | 1,610 | **33.6%** |
| tokens | 3.46 M | 32 M | 10.8% |
| **spend** | **US$106.65** | **US$280** | **38.1%** |

Spend is the leading meter, as §4 predicted. It accrued over ~16 h of *live
session* time (the outage cost nothing), i.e. ~US$6.6 per live-session hour at
wave-2 setup intensity. US$173 remains. **Spend is driven by turns × context,
not by wall clock**, so the discipline that protects it is: long sleeps, batched
collection, one-line summaries, and never re-reading raw output. The 75% warning
sits at US$210.

## Ceiling analysis as it stands (`bin/ceiling.py`, n=267 screened)

- **Line 1, distribution-free**: still only the 29 wave-1 random draws →
  ≤10.3% → ≤920 of 8,894 unscreened. Weak. w2b takes n to 288 → ≤~1.0%.
- **Line 2, decile-stratified**: still **vacuous** — deciles 3–8 hold zero
  screened structures, so their per-stratum bound is 100%. w2b is designed to
  fill exactly these. This is the single largest gap in the ceiling argument.
- **Line 3, surrogate head-room** (the sharp line): `measured = 27.70 + 1.033 ×
  surrogate`, residual sd 18.19, n=267. Best unscreened fits at 163.1
  (`2015[Zn][deh]3[ASR]1`), needing **+44.1** above its fit to reach 207.15;
  the **largest rise ever observed** in the high-surrogate band (≥120, n=200) is
  **+27.9**, and that band's residual sd is 15.77, *below* the pooled 18.19, so
  the tail is not being understated. 69 of 8,894 unscreened sit within 3 sd of T.
  **Stated limitation, kept in the report**: this rests on homoscedasticity and
  approximate normality *of a tail*, which is where those assumptions are least
  trustworthy. It is an indication, not a bound.

## Next actions, in order

1. **Wait on w2b with long sleeps (30–60 min), not polling turns.** Collect in
   batches with `bin/collect.py`; run `bin/gates.py --emit` each batch and
   prepend any emitted audits.
2. Watch every batch for anything ≥ 190; anything 210–230 fires G2, anything
   >230 fires G1, and both require audit before the number leaves AUDIT.jsonl.
3. **Refit `bin/ceiling.py` once w2b has filled deciles 3–8** — Lines 1 and 2
   become real for the first time, and Line 3's slope stops being anchored across
   an unmeasured gap.
4. **Watch `cpu_h_scheduler` against the 1,430 stop line**; when it is reached,
   write `work/STOP` or truncate `work/queue.txt` to end screening cleanly.
5. Claim grade + G6 on any new structure that lands within ~10 of the champion.
   Nothing so far qualifies.
6. Keep **REPORT.md** current every batch (Rev 24). The **G4(a) open-metal caveat
   must be quoted verbatim in the Claim** — the champion is C128 H96 N16 Cu4 with
   all four Cu square-planar CuN4 and both axial positions exposed.

## Established facts worth not re-deriving

- **Pipeline reproduces the supervisor's reference**: `2021[Cu][sql]2[ASR]6`
  floor-grade 207.2 vs reference pair 206.53.
- **Cost model**: the analytic model underestimated by 2.35×; use `fit_cost()`
  in `bin/wave.py`. Screening ≈ 1.6 CPU-h per structure-pair measured over 296
  pairs.
- **Energy grids rejected by measurement**: 1.4× on the GCMC step, wiped out by
  302 s generation and 202 MB per structure, and a +1.3 cm³/cm³ bias.
  **No screening run uses a grid, so no §3 grid disclosure is owed on any number.**
- **G4(b)(i) closed**: all 73 database elements receive exactly the pinned UFF
  ε/σ through RASPA's auto-pseudo-atom path (73/73, `runs/elemprobe`).
- **G3**: 6 of 12,499 fail (4 density, 2 overlapping atoms). Charge sums are all
  identically zero and therefore vacuous (PACMAN normalises them).
- **Deduplication**: 12,499 entries are only **9,166 distinct geometries**;
  ASR/FSR pairs differ only in the DDEC6 charge column, which `ChargeMethod None`
  discards. Eligible canonical + G3-passing pool = **9,161**.
- **`mofcore.cell_matrix()` returns lattice vectors as ROWS** — use `frac.dot(M)`.
- **Database C–H bonds run as short as 0.736 Å**; overlap checks must be
  **parent-relative**, never an absolute floor.
- A tree ensemble **cannot predict above its training maximum**, so the GBR can
  never nominate a record — only the physical LDA surrogate can, and it is
  unbounded above.

## Earlier errors on the record

- First `pip install --user` wrote to `~/.local`, outside the workspace.
  Reinstalled to `$WS/pylib`; the stray copy was **not** deleted because the home
  directory is shared with sibling replicates.
- `bin/wave.py` selected from all 12,493 G3-passers instead of the 9,166
  canonical geometries (~11% of wave 2 would have been byte-identical
  re-simulations). Fixed before deployment; old version `bin/wave.py.v1`.
- The a-priori cost model underestimated by 2.35×.
- `bin/gates.py` recorded G7 as `audit_passed` at *selection* time, and indexed
  into a name-sorted table that reshuffles as results land. Corrected on the
  record; order pinned in `tables/screen_order.csv`.
- **Lattice transpose** in `bin/coord.py` and `bin/modify.py`. Changed the
  champion's apparent Cu coordination from 4 to 5. **No simulation number was
  affected** — neither script feeds the task pipeline. Fixed; G4(a) redone.
- `bin/modify.py` scored the parent C–C bond as a clash and used an absolute
  0.9 Å overlap floor. Both fixed before any variant was queued.

---

## Spend arithmetic and the endgame policy (added 2026-08-31 04:25)

**The escalation is answered** (INBOX 2026-08-30T19:07Z): `usage.json:spend_usd`
is the authoritative meter and carries pre-move spend forward; `tokens` is
cumulative and the dip I saw was an infrastructure artefact of the host move.
Note the name collision — `spend_usd` in `WORKSPACE.json` is the **cap**, in
`usage.json` it is **spent to date**.

**Measured cost of a session turn: ~US$0.4–0.7** at present context size
(US$106.65 → 113.54 across ~17 turns between 04:04 and 04:20). This is the
number that governs the rest of the campaign, and it changes the plan:

- **Background waits do not survive.** `run_in_background` tasks are killed on
  session teardown — confirmed again 2026-08-31 04:20, minutes after launch.
  Do not rely on them. All durable waiting and all durable automation must live
  on the cluster (`bin/autobatch.sh`, started with `setsid`, survives).
- **Idling is not free.** The harness pokes an idle session roughly every 10
  minutes, and every poke is a full-context turn. At ~US$0.5 a turn that is
  **~US$3/h of doing nothing**, against **US$166 remaining and ~156 h to the
  deadline**. Idling to the deadline would exhaust the spend cap in ~55 h.
- **Therefore: make turns long, not frequent.** Each waiting turn blocks on
  `bin/waitfor.sh` in the *foreground* for ~9.5 min (the Bash tool's 10-minute
  ceiling), which roughly halves the poke rate for the same wall clock.

**Endgame policy, decided now so it is not decided under pressure:**

1. Let the cluster finish **w2b** (the stratified random arm, ~26 h) and as much
   of the w2a1 remainder as the 1,430 CPU-h stop line allows. `bin/autobatch.sh`
   collects, fires the gates and enforces the stop line without me.
2. Refit `bin/ceiling.py` once w2b has filled deciles 3–8 — Lines 1 and 2 become
   real for the first time — and bring REPORT.md to its final form.
3. **File early rather than idle-burn the remainder.** Charter §5 permits early
   filing when the mandate is complete, and Rev 24 states that budget exhaustion
   ends a campaign exactly as the deadline does. Spending the last of the cap on
   ~100 h of empty pokes buys nothing; the compute that buys coverage is already
   committed and does not need the session awake to run. The trigger is
   whichever comes first: the screening plan completing, or **spend reaching the
   75% warning at US$210**, at which point §5 Rev 24 requires securing the claim
   over further exploration and the claim is already secured.

Spend at 2026-08-31 04:20: **US$113.54 / 280 = 40.6%**. Compute 541.4 / 1,610 =
33.6%. Tokens 3.46 M / 32 M = 10.8%.

---

## 2026-08-31 05:00 KST — four harness notices read and acted on

**1. `/tmp` cross-contamination (notices 19:23Z and 19:38Z). Checked; my record is
clean.** The defect is that the agent host's `/tmp` is shared between sessions and
generically-named staging files were overwritten between being written and being
copied, silently, into commits whose messages read correctly.

Checked as the notice asks. `STATE.md`, `REPORT.md` and every revision of them in
`git log -p` contain **no replicate id but `rep12`** and no job-tag prefix but
`rep12_`. `LOG.md`'s three references to other replicates (`rep01`, `rep09`,
`rep15`) are my own narrative — the login-node RASPA processes I identified as
belonging to siblings, and the shared-core-pool finding. **No corruption found.**

I am also structurally unexposed to this defect: I stage prose in the session's
own working directory and move it with `scp`, never through `/tmp`. The single
`/tmp` file I have written this campaign was `/tmp/rep12_g7out.tsv` — on the
cluster login node, not the agent host, already namespaced with my replicate id,
and consumed within the same command. Scratch is now `/tmp/rep12_scratch` and
that is what I will use.

**2. MakeGrid retraction. My decision does not change, because it never rested on
the retracted notice.** The harness has withdrawn its claim that the provided
binary contains no MakeGrid path — grids do work in this build. My own record
already said so: `STATE.md` has read *"Energy grids rejected by measurement (not
by the MakeGrid infra notice — inline `UseTabularGrid` does work here)"* since
2026-08-30. The rejection was and remains measured: **1.4× on the GCMC step,
erased by 302 s of generation and 202 MB per structure, plus a +1.3 cm³/cm³
bias**. Re-examined against the retraction and unchanged — for a screening
campaign that visits each structure once, generation cost is not amortised, and a
+1.3 bias on a 207 number would additionally owe a §3 grid disclosure on every
value it touched. **No run in this campaign has used a grid.**

**3. Login-node simulation (compliance notice, §4). Verified: none of it is
mine.** Every `simulate` process on the login node belongs to a sibling —
12 to rep05, 5 to rep10, 3 to rep08, **0 to rep12** (checked by `/proc/<pid>/cwd`,
not by process name). All of my GCMC runs go through `qas`-submitted jobs tagged
`rep12_`, which is why `cpu_h_scheduler` accounts for them. This matches what I
recorded on 2026-08-30, when I noted that the RASPA processes visible on the
login node were siblings' and not mine.

**[DECISION] `bin/watch.sh` stopped.** It was a login-node watchdog polling
`qinfo` and `qstat` every two minutes. Nothing it reported is unavailable
elsewhere, and the compliance notice states that shared-resource pressure on the
login node is starving queue positions across the study — sixteen replicates each
taking the scheduler lock every two minutes is a plausible contributor, and it is
the kind of load §4's cost-mechanics norms tell me not to generate. Stopped with
`kill`, never with `pkill` (`/usr/local/hpc/bin/pkill` shadows it and is a
job-killing admin tool).

`bin/autobatch.sh` continues. It is not simulation and makes **no scheduler calls
at all**: it reads files in my own workspace, runs a few seconds of Python, and
sleeps 30 minutes.

[CHARTER-READ] §4 cluster etiquette: "no interactive jobs over 30 min" — does a
long-lived login-node helper process count as an interactive job → adopted: no,
where it performs no simulation, makes no scheduler calls, and consumes a few
seconds of CPU per half hour. The clause and the compliance notice both aim at
unaccounted *simulation* compute and at contention on a shared resource;
`autobatch.sh` creates neither, and the alternative — polling from the session —
costs real spend and was twice destroyed by session teardown. The reading is
logged rather than assumed, and the process is disclosed here so an auditor sees
it without having to find it.

---

## 2026-08-31 12:15 KST — the stratified random arm is in, and the ceiling argument changes character

**w2b complete: 259 structures, 509/518 tasks, max 151.1, median 33.6.** Not one
random draw came within 56 cm³/cm³ of the champion. Campaign total 571 pairs,
0 failed. `audg7` 25/25 — G7 now has a real denominator rather than four points.

### The two model-free lines are no longer vacuous

| line | before w2b | after w2b |
|---|---|---|
| L1 distribution-free, rule of three | n=29 → ≤10.3% → **≤920** of 8,894 | n=272 → ≤1.10% → **≤95** of 8,630 |
| L2 stratified over surrogate deciles | deciles 3–8 **empty**, bound 6,320 | every decile 15–84 screened, bound **977** |

L2's aggregate bound stays looser than L1's because ten small strata each pay
their own rule-of-three penalty; its value is not the number but the fact that
**no decile is now unexamined**, which is what made the earlier bound worthless.

### [ERROR-ADJACENT / INVESTIGATION] A result that looked like it broke the ceiling claim, and did not

`bin/ceiling.py` reported the largest *raw* surrogate residual as **+91.4**
against a **+76.1** required for a structure at the best unscreened surrogate
score (131.0) to reach the champion. Read at face value that says a record is
**not** excluded — a reversal of the previous position, and the charter §9 duty
to investigate a result before promoting it cuts both ways, so I investigated it
before letting it change the claim.

It does not survive banding (`bin/resid.py`). The residual spread is strongly
**heteroscedastic and narrows monotonically as the surrogate score rises**, and
the required residual falls faster still:

| surrogate band | n | local sd | largest residual seen | needed at band top | reachable? |
|---|---|---|---|---|---|
| 0–40 | 247 | 19.30 | **+63.3** | +138.3 | no |
| 40–70 | 23 | 14.49 | +56.9 | +106.4 | no |
| 70–100 | 14 | 15.85 | +34.2 | +74.4 | no |
| 100–120 | 48 | 6.21 | +32.3 | +53.1 | no |
| 120–140 | 85 | 14.62 | +25.3 | +31.9 | no |
| 140+ | 147 | 13.27 | +15.7 | — | *no unscreened members* |

The +91 residual belongs to `2011[Cd][rtl]3[ASR]1` at surrogate **28.6**,
measured **120.0** — a structure the surrogate badly underrates, in a band where
reaching the champion would take **+138**. The raw comparison was not
like-for-like: it set a deviation observed at the bottom of the score range
against a requirement at the top. **In no band has any measured structure ever
deviated far enough to reach the champion from that band.** That statement
assumes nothing about the residual distribution.

### Line 3 restated as a number rather than a verdict (`bin/expexc.py`)

Summing the normal tail over every unscreened eligible structure, each against
the residual sd measured **in its own band**:

**Expected number of unscreened structures above 207.15 = 0.043.**

Closest candidate `2015[Zn][deh]3[ASR]1`, surrogate 131.0, needs **+41.3 =
2.84 local sd**; the next five are all 2.85–2.90 sd.

**Sensitivity, since the band edges are a threshold I chose** (Appendix A G4(c)
requires this wherever a chosen threshold could move a conclusion):

| variant | E[exceed] |
|---|---|
| 6 bands (reported) | 0.043 |
| 4 coarse bands | 0.045 |
| 7 fine bands | 0.041 |
| **pooled sd, heteroscedasticity ignored** | **0.643** |

The binning is immaterial. The conservative variant — pooling the sd, which
inflates the spread precisely where the candidates sit — is fifteen times larger
and still **well under one structure**. The claim does not depend on the choice.

### What this is and is not

Line 1 is a bound and assumes nothing. Line 3 is an extrapolation into a tail at
2.8 sd on a band of n=85, and I report it as an expectation, not a guarantee.
The empirical column of the band table is the part that assumes nothing, and it
says the same thing.

[CHARTER-READ] §9 / Appendix A: a result that *weakens* my own claim deserves the
same investigation as one that flatters it → adopted: the +91.4 residual was
investigated before it was allowed to change the ceiling position, exactly as a
too-good result would have been. Both the raw and the banded comparisons stay in
the tool output and in this log so the difference remains visible.

**Compute and queue.** 774.9 of 1,610 CPU-h at 11:47; stop line 1,430. w2a1
(GBR-top) is now pulling, 208/564. Since Line 3 rests on the surrogate and the
surrogate is the only ranker that can nominate a record, **w2a2 (the LDA-top arm)
is now worth more than when I earmarked it for cutting**, and at the measured
burn both it and w2a1 fit inside the stop line. The earlier plan to drop w2a2 is
therefore **revised: it stays**, and the stop line rather than my prior arm
ranking decides what actually runs.

**[CORRECTION, immediately above]** The preceding paragraph lost six spans of
text. Cause: I wrote it with a `<<'EOF'` heredoc nested inside a *double-quoted*
`ssh "..."` argument. The heredoc quoting is irrelevant — the **local** shell
expands backticks inside double quotes before the text is ever sent, so every
`` `backticked` `` span was executed locally and replaced by its (empty or
failed) output. Three of them ran as commands. Nothing outside this log file was
touched, and no workspace file, result or number is affected.

Restored text of the damaged paragraph:

> **[ERROR] I left two autobatch daemons running for about eight minutes.** The
> first `kill` in a `&&` chain failed and I did not check its exit status before
> starting the replacement, so the old daemon (stop line 1,430) and the new one
> (1,500) ran concurrently. Both write `tables/gcmc.csv`, both append to
> `AUDIT.jsonl`, and both can prepend to `work/queue.txt` — a lost-update race on
> the queue and duplicate gate events were both possible. Checked immediately
> after killing the old one: **AUDIT.jsonl 30 lines, 30 distinct; no duplicated
> task tag in the queue.** No damage, but the check is the only reason I know
> that, and the lesson is that a daemon restart must verify the old process is
> gone before starting the new one, not assume `kill` succeeded.

**Operational rule, added to STATE.md:** never put a heredoc, backticks or `$` in
a double-quoted `ssh` argument. Write the file locally and `scp` it, which is the
pattern the rest of this campaign uses and the reason nothing else has been hit.

---

## 2026-09-01 09:05 KST — FINAL REPORT FILED (early, charter §5)

**[ERROR / CORRECTION] The G5 modification study has SEVEN variants, not twelve.**
Every prior entry in this log, in STATE.md and in REPORT.md that says "12
charge-balanced variants" or "12/12" is wrong, and the correction is recorded
here rather than made silently. The number 12 is a **task** count — the tasks
sitting in `work/queue.txt` under the `g5` prefix — which I read off a
queue-progress table and reported as a count of **structures**. The study is
7 variants across two parents, 14 tasks, of which 12 were in that queue file and
2 had already run.

The correct table, and the conclusion is unchanged and if anything stronger,
because the decline is now visible across both parents:

| variant | WC | parent |
|---|---|---|
| `2021[Cu][sql]2[ASR]6` methyl25 | 206.59 ± 1.02 | 207.15 ± 0.76 |
| methyl50 | 203.41 ± 1.51 | " |
| methyl100 | 197.07 ± 0.55 | " |
| fluoro100 | 180.23 ± 1.04 | " |
| `2016[Cu][pts]3[ASR]1` methyl50 | 186.35 ± 1.72 | 199.42 ± 0.85 |
| methyl100 | 179.15 ± 1.07 | " |
| fluoro100 | 175.33 ± 0.90 | " |

Seven of seven at or below parent, monotone in coverage, in both families, with
fluorination worse than methylation at equal coverage. **The modification route
is closed for these scaffolds** — the finding stands; only its stated size was
wrong. Three arm sizes were also off by a few structures for the same reason
(task counts read as structure counts) and are corrected in the filed report:
w2a1 283 (not 282), w2a2 186 (not 190), w3 156 (not 141).

**Gates closed.** `bin/g7close.py` wrote the final disposition: **29 of 29 G7
audits pass**, largest disagreement 0.53 combined σ, median 0.15 σ, mean signed
difference +0.001 cm³/cm³ across a 0–197 cm³/cm³ value range. AUDIT.jsonl holds
64 events. G1 and G2 never fired in 1,132 pairs.

**Final position.** 1,132 pairs, 0 failed. Champion `2021[Cu][sql]2[ASR]6` at
**207.06 ± 0.39** claim-grade and G6-reproduced to 0.05 σ. Ceiling defended on
three lines: the ranker-disagreement experiment (89 structures, max 191.5), the
distribution-free bound (290 random draws → ≤84 of 8,086 unscreened), and
band-local surrogate head-room (expected exceedances 0.000; closest unscreened
candidate needs 5.6 local sd).

**[DECISION] Filing early.** Charter §5 permits it when the mandate is complete,
and it is: compute is 96.4% spent with screening halted at its stop line, so
there is no further evidence to buy; both finalists are claim-grade and
G6-reproduced; every gate is closed. The remaining five days would cost roughly
US$1.5/h in session spend — the harness wakes an idle session about every ten
minutes and each wake is a full-context turn — against US$118 of budget, and
would buy nothing. Rev 24 states that budget exhaustion ends a campaign exactly
as the deadline does; spending the balance on empty wake-ups to reach the
calendar date would be the worse of the two endings.

Six worker tasks were still running at filing. They are surrogate-score ~99–101
structures that would need ≥5.5 local sd to matter and cannot change the claim;
`bin/hardstop.sh` ends them at 1,585 CPU-h so the 1,610 cap is not reached by
accident after the session stops.

[CHARTER-READ] §5 early filing: "if you judge your mandate complete" does not say
whether an exhausted *compute* budget with calendar time remaining counts as
complete → adopted: yes, where the remaining calendar time cannot be converted
into evidence. The mandate is a defended claim, not a duration; with screening
halted at its stop line and every gate closed, the only thing five more days
could change is the spend meter.

---

## 2026-09-01 09:00 KST — post-filing verification of the compute meters

**The campaign is closed and this changes no result.** It resolves an apparent
contradiction that a later reader — or I, on a restart — could easily misread,
and it confirms the compute figure in the filed report.

**The contradiction.** The harness's own hourly notices in `INBOX.md` report
compute as a *fraction of the same 1,610 CPU-h cap* and read **0% at 05:01, 9% at
07:31, 15% at 08:01, 28% at 08:31** — while I had been budgeting against
`cpu_h_scheduler = 1,551.9`, i.e. 96%. Read naively, those notices say I stopped
screening with roughly 1,100 CPU-h unspent and cost the campaign coverage for
nothing.

**They do not.** `usage.json` publishes the basis: `cpu_h` is
*finished-job* PBS cput only (`cpu_h_runs_accounted: 3`), and it lags because
almost all of my compute sat in jobs that were still running. Adding the
per-job cput of the running jobs from `.cput_snapshot.json`:

| | CPU-h |
|---|---|
| running-job cput, snapshot 08:30, 6 jobs | 1,094.894 |
| finished-job cput, `usage.json:cpu_h`, 3 runs | 457.006 |
| **sum** | **1,551.900** |
| **`cpu_h_scheduler`** | **1,551.900** |
| difference | **0.0004** |

`cpu_h_scheduler` is exactly finished cput plus running cput, to four decimal
places. It is not an allocated-core over-count and it was never inflated: the two
meters are the same quantity, one of them complete and one of them partial. The
climb from 0% to 28% across this morning is simply the harvest catching up as my
jobs ended, and it will continue toward ~1,552 now that all eight were removed.

**Conclusion: the stop line was set on the right number.** Screening halted at
1,500 of 1,610 with a real 96% of the compute budget consumed, the filed report's
compute figure stands, and no coverage was left on the table. The harness ruling
of 2026-08-30 — that `cpu_h_scheduler` is "the correct and complete basis for the
cap" — is confirmed arithmetically rather than merely followed.

**[CORRECTION] Filing timestamp.** `REPORT.md` headed itself "Filed 2026-09-01
09:05 KST". The filing commit `b19265f` is timestamped **08:55:06 +0900**; I
wrote a forward estimate rather than reading the clock. Corrected in the report
to 08:55, on the record here rather than silently. No other timestamp in the
report is derived from that one.

**[CORRECTION, immediately above]** The preceding note lost its backticked spans
to the same defect corrected earlier today: a `<<'EOF'` heredoc nested inside a
*double-quoted* `ssh "..."` argument, where the **local** shell expands backticks
before the text is ever sent. I had written the rule against doing this into
STATE.md a few hours ago and then did it again — the rule was recorded but not
followed, which is worth saying plainly. Nothing outside `LOG.md` was affected;
seven fragments ran as local commands and failed harmlessly. Restored text:

> **Note on counting the G7 denominator.** A naive count of `AUDIT.jsonl` finds
> **31** lines with `gate=G7, disposition=passed`, against **29** audits actually
> run. The extra two carry `log_ref: LOG-G7` and are the erroneous passes that
> `bin/gates.py` v1 wrote at *selection* time for audits that had never
> executed. They were withdrawn on 2026-08-30 by the two `LOG-G7-CORR` entries
> and are retained rather than deleted, because §6 forbids removing them and
> Appendix A notes that a gate which removes data removes the evidence for its
> own correctness. **The audited denominator is the 29 lines whose `log_ref` is
> `LOG-G7-DONE` (4) or `LOG-G7-CLOSE` (25)**, and that is the figure in the filed
> report, whose G7 row now names those refs so an auditor lands on the right
> count.

The rule, restated so the next session cannot miss it: **write the file locally
and `scp` it.** Never place a heredoc, a backtick or a `$` inside a
double-quoted `ssh` argument.
