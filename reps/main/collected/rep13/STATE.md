# STATE — rep13 (methane deliverable capacity)

Consolidated 2026-08-31 05:20 KST. **This file supersedes every earlier
version and all appended UPDATE/CORRECTION blocks**; it is written to satisfy
charter Rev 25 — a fresh session re-orients from `CHARTER.md`, this file,
`LOG.md` and git, and must need nothing else. Where this file and an older
LOG entry disagree, **this file is right** and the LOG entry is history.

T0 = 2026-08-29 20:42:22 KST.
**DEADLINE T = 2026-09-06 16:43:21 KST** (`WORKSPACE.json` `deadline_kst`:
168 h + 4.4704 h fleet pause + 15.5461 h restored for the 2026-08-30/31
harness fault). ~155 h remain. Figures 2026-09-05 20:42 and
2026-09-06 01:10:35 are both superseded.

## Mandate in one line
Max working capacity N(65 bar) − N(5.8 bar), 298 K, **absolute** loading,
volumetric (cm³ STP/cm³), over the 12,499-structure db, under RASPA 2.0.37 /
UFF+TraPPE / chargeless / 12.8 Å / tail corrections off / unshifted; plus a
defended claim on whether that number is near the achievable ceiling.

---

# 1. SCIENTIFIC POSITION

## Best measured — CLAIM-GRADE, G6-PASSED, IDENTITY RESOLVED (2026-09-01 03:17)
**`2015_V_srs_3_FSR_1` — WC 197.3 +- 0.4 cm3/cm3** (mean of THREE independent
claim-grade runs: 197.535 c2, 197.210 g6a, 197.302 tb1; SD 0.167, SEM 0.097,
95% CI +-0.42 by t on n=3). N(65) 232.4, N(5.8) 34.9, ratio 0.150.
**G6 PASSED** (0.30 sigma). **G4(a): no caveat, no sensitivity owed** — 4 V
centres buried at every threshold.

### THE IDENTITY CONTEST IS SETTLED — do not reopen it as "one of two"
Three independent samples each:
- V-srs  197.535 / 197.210 / 197.302 -> mean **197.349**, SD 0.167
- Yb-nia 196.323 / 196.174 / 196.298 -> mean **196.265**, SD 0.080

Difference **1.084 +- 0.107**, Welch t = **10.1** on ~2.9 df, **p ~ 0.003**.
The Claim names ONE structure. Every earlier version of REPORT/STATE saying
"one of two" is superseded.

### WHY it resolved — a methodological result worth carrying forward
**RASPA's per-run block-average sigma (0.47-1.12) is 3-7x LARGER than the
observed run-to-run scatter (SD 0.08-0.17).** The block-average error is
conservative as a predictor of how far an independent repeat moves. So:
**to compare two materials, use the empirical scatter across independent runs,
not the internal error estimate of a single run.** That is what let 15 CPU-h
settle what looked like an unresolvable 1.1 sigma tie. It also means the
earlier floor-vs-claim deltas sat "inside sigma" partly because sigma was too
generous.

### Estimator rule — both halves, do not collapse them
- **G6 pass/fail**: the archived run and its reproduction are NOT averaged. G6
  asks whether the number reproduces. It does (0.30 sigma).
- **Claim value**: independent samples ARE pooled, because the question is what
  the number is, and three samples beat one. Quote the 95% t-interval, not the
  SEM, at n=3.

### Supporting, deliberately NOT pooled
`2015_V_srs_3_ASR_1` (same framework, other symmetry reduction, different CIF)
gives 197.09 +- 0.53 claim-grade — within 0.26 of the pooled mean. Independent
corroboration that the *material* scores ~197.3, not the file. Not pooled
because it is a different input rather than a repeat of the same one.

### Floor cycles remain unbiased at n=10
Deltas now include -0.12 (V-srs), -0.02 (Yb-nia), -0.84 (Ni-nia) on top of the
original seven. Mean |delta| ~0.24, max 0.96, no sign bias. 1sd falls by about
sqrt(5) each time, as the cycle ratio predicts.

### Prediction (c)'s MECHANISM is contradicted — LOG-2026-08-31-13
Yb-nia has N(65) = 242.3 with ratio **0.1897**, below the 0.20 I predicted for
anything above N(65) 235, measured at Claim fidelity. Ni-nia at N(65) 243.6
sits at 0.2037, above it. Two structures 1.3 apart in uptake fall on opposite
sides, so 0.20 is not a physical boundary. Formally (c) is scoped to wP members
so this is not the test failing, but the mechanism is contradicted and it is
recorded BEFORE wP lands so it cannot look like a retrofit. Re-check (c) on wP
members as written when they land.

## 247 pairs / 231 distinct structures
Waves: cal 64 (pre-committed uniform, seed 13), w1 167, c1 7 (claim-grade),
land 4, g7a 2. Stage A descriptors complete for all 12,499.

## Three results the report leans on

**(a) Floor cycles are unbiased against claim-grade.** Seven structures have
both: mean |Δ| 0.27, max 0.96, four down three up. Claim-grade 1sd falls to
0.34–1.13 from 0.63–2.80 (≈√5, as the cycle ratio predicts). This
retrospectively licenses screening-by-floor-cycles. It does **not** license
separating candidates closer than ~1 cm³/cm³ — hence c2. Measured claim-grade
cost 0.90–2.60 CPU-h/pair vs 0.57 floor. LOG-2026-08-31-01.

**(b) The ceiling is an interior optimum with both failure modes measured.**
Upper envelope of WC vs N(65) over 231 structures (`bin/envelope.py`) peaks at
**N(65) 225–235, max 197.7**, and falls on both sides. Right-hand side now
rests on 35 structures (was 7). Mechanism: stronger binding fills the 5.8-bar
leg faster than the 65-bar leg. The six highest uptakes in the campaign
(N(65) 252–267, twt/dia/unc topologies) have ratio 0.30–0.57 and WC 116–177 —
each beats the leader on uptake by 20–35 and loses on WC by 21–82. Weakest
binders (ratio 0.086–0.097) cap near N(65) 130. **Uptake is not the objective
and this database proves it at both ends.** LOG-2026-08-31-02.

**(c) Every plausible challenger is already queued.** Surrogate refit on 230
structures (`data/s2_*`): CV RMSE 16.7→11.22, R² 0.819→0.964, Spearman
0.880→0.947; importances vf_he 0.323, asa_g 0.228, vf_ch4_energy 0.222. Over
the 12,262 unmeasured G3 passers: **zero** have a point prediction above the
leader (best 188.6); **284** have an optimistic bound (pred + 2sd) above it;
**all 284 are already queued** (verified against `work/{pending,running,done}`,
284/284); **zero** lie below the vf_he 0.30 cut. This **closes the
adversarial-search leg** — the ~160 CPU-h hunt below the cut is cancelled on
evidence, and the 398 demoted `80_f1` tasks stay demoted.
*Two limitations that are load-bearing:* a random forest cannot predict above
its training maximum (197.7), so the point-prediction result is partly a
model-class property — **the argument rests on the bound, not the point**; and
the CV is optimistic because 167 of 230 training points were selected by the
previous model. The uniform 64 is the only unbiased part and is why the refit
is trustworthy outside the selected region at all. LOG-2026-08-31-03.

## PRE-REGISTERED PREDICTIONS (committed b43275a, before wP ran)
- **(a) no wP structure exceeds WC 200 — STANDS**, 2.3 of headroom. This is
  the one that matters: if it fails, a better material exists and the ceiling
  claim is wrong.
- **(b) envelope peak stays in N(65) 210–230 — FAILED.** Peak is at 232.5, and
  it moved on w1 data before wP ran a single task. Reported as failed in
  LOG-2026-08-31-02 and REPORT.md §4.2. What failed is the claim that I knew
  *where* the peak was, not that it is interior.
- **(c) any wP structure with N(65) > 235 has ratio > 0.20 — STRAINED.**
  Yb-nia at N(65) 241.8 gives 0.188 (under); Ni-nia at 244.2 gives 0.202
  (over). Both are w1, not wP, so neither is formally a test.
**Re-check all three explicitly when wP lands and report either way.**

## Landscape (do not re-derive)
vf_he median 0.081, q90 0.304, q99 0.560 over 12,492 G3 passers; 1,283 reach
0.30, 480 reach 0.40, 201 reach 0.50. WC rises steeply with vf_he, peaks
0.50–0.55, falls above 0.65. None of the 59 measured below vf_he 0.30 exceeds
110. Leaders sit at vf 0.49–0.52, ρ 0.46–0.59. Empirical envelope, **not** a
physical bound: N(65)/vf_he reaches 1,162 at vf 0.155 against the 590 cm³
STP/cm³ liquid-methane figure, because vf_he is a hard-sphere geometric volume
for a 1.32 Å probe. LOG-2026-08-30-08.

## Reproducibility denominator
**Twelve structures measured twice; none moved by more than 1 cm³/cm³.**
7 floor-vs-claim-grade, 2 G7 reproductions from archived inputs
(2015_Cu_pcu_3_ASR_2 176.48/176.11; 2014_Ce_nan_3_ASR_4 91.69/92.30), 1
independent repeat (2010_Cu_wbl_3_ASR_3 120.73/120.72), 2 in-family duplicates.
RASPA is **not** deterministically seeded here, so G6 is a real test.

---

# 2. GATES — `AUDIT.jsonl` = 37 lines (G3 7, G4 25, G7 5)

- **G1/G2 clean** over all 244 pairs. Nothing >230, nothing in 210–230.
- **G3** whole database: 12,492 pass, 7 fail (4 density 0.164–0.175, 3 overlap
  d_min 0.094–0.523 Å). All seven logged.
- **G4(b)(ii) leg (i) clean database-wide**: all 73 elements have entries in
  the pinned `pseudo_atoms.def`. Recorded once, not per structure.
- **G4(a) settled for the nine leaders** (`bin/g4_metal.py`, `data/g4_c2.txt`).
  Criterion: probe points on the closest-approach sphere of each metal,
  accessible when clear of every other framework atom; EXPOSED at threshold.
  **The leader `2015_V_srs_3_FSR_1` has max exposure 0.000 — buried at every
  threshold (0.001/0.01/0.05/0.10), so NO caveat attaches and NO sensitivity
  report is owed for it.** Threshold-dependent cases if the claim moves:
  Yb-nia 0.022 (EXPOSED ≤0.01, buried ≥0.05 — **would owe caveat + mandatory
  G4(c) sensitivity**); Ni-nia and Tb-soc 0.005 (EXPOSED at 0.001 only).
  No leg-(ii) argument is made against Yb or Tb, and none is asserted.
- **G7** due on 5 (ranks 40/80/120/160/200 of 234). Non-simulation half
  **passed on all five** (prep byte-identical, ρ 0.428–1.086, d_min
  0.820–0.947, net q 0, headers 12.8/unshifted/tailcorr no). Two complete and
  passed (Δ 0.21%, 0.67%). **Three reproductions queued as wave g7b**,
  disposition `flagged_pending`. `2013_Ni_nia_3_ASR_1` is both the 160th
  passer and the 4th-ranked candidate — coincidental, noted in its audit line,
  and its g7b run serves G7 and G6 at once.
- **Still owed before the Claim is admissible:** (1) c2 must land — the leader
  has no claim-grade pair; (2) **G6 reproduction of the Claim number**, not
  yet queued for the new leader — queue at priority 25 the moment c2 returns;
  (3) as much of wP as fits, to convert the 284 challengers from modelled to
  measured. If spend runs out first, **report what fraction of the 284 were
  measured** — that number is the honest strength of the ceiling claim.

---

# 3. BUDGETS (2026-08-31 05:17)

| budget | used | cap | % |
|---|---|---|---|
| compute (`usage.json cpu_h_scheduler`, authoritative) | 263.0 CPU-h | 1610 | 38.8%* |
| tokens | 5.13 M | 32 M | 16% |
| **spend** | **$114.87** | **$280** | **41.0%** |

\* `bin/status.sh` shows 624 CPU-h from `bin/acct.py`, which is conservative
(charges walltime × ppn, i.e. idle worker slots, plus non-chargeable head-node
work). **Plan against acct.py, report against usage.json.**

**Per-turn cost, measured by turn type — never quote a blended hourly rate**
(doing so produced two wrong estimates in opposite directions on 2026-08-31):
- minimal status check: **~$0.37**
- analysis + writing + commit: **~$2.70–4.00**

Idle re-invocation cadence is now **45 min** (harness change, Rev 25 notice;
takes effect when the session loop next starts). At $0.37 per idle turn that
is well under $1/h, so **the hard stop is not imminent**. Rev 24 still binds:
at **$210 (75%)** stop exploring, secure the claim, file.

**Compaction (Rev 25):** compact when `transcript_mb` (published in
`usage.json`) materially exceeds need; guideline ~1.5 MB. Now 1.24. Sessions
are disposable and restart from the initial prompt — **compaction costs
nothing this file carries.**

---

# 4. CLUSTER — the binding constraint

**0 running, 12 queued (the §4 cap) since 04:06 KST.**

**The block is the fleet-shared per-user quota, not fragmentation.**
`pbsnodes` at 04:28 showed 38 amd and 16 aa cores physically idle, including
two amd nodes with 16 free each — unreachable because Bei sits at 38/38 aa,
80/80 amd, 98/102 ac, with ax physically full via another user. All ~16
replicates submit as `Bei` and share ~252 cores with no per-replicate
reservation. **No submission strategy wins a core**: not ppn size, not node
type, not FIFO position. Only another replicate's job ending frees one.
**Do not re-plan this.** LOG-2026-08-31-04.

**CORRECTED 2026-08-31 13:00 (LOG-2026-08-31-09): small jobs dispatch, large
ones wait.** STATE previously claimed that mjs `_iter_jobs` sets
`check_node=False` on the first non-fitting job of a node type and thereby
blocks every later job of that type, and concluded that holding the four
oldest aa positions at ppn=8 was the strongest position. **Wrong.** At 12:58
mjs reached *past* all four of my head-of-queue ppn=8 aa jobs to dispatch
`small_aa2` at ppn=2. The working rule is:

> When every node type sits at 100% quota, cores free in ones and twos and a
> small job takes them. A large job at the head waits for a block that never
> comes.

Queue is therefore now **deliberately mixed**: 9 x ppn=8 to capture a large
opening if one comes, 3 x ppn=2 to take the small openings this cluster
actually produces, across all four node types. Do not make it uniform again.

Queued: aa — descA_08/09/10/11 (ppn=8, head of FIFO), poolA_02 (8),
small_aa2 (2). ac — poolB_ac0/1/2 (8). amd — poolB_amd0/1 (8). ax — descA_06 (8).

### >>> THE MISTAKE THAT COST REAL SCIENCE — DO NOT REPEAT <<<
The 2026-08-30/31 outage cost ~12 h at ~27 cores **not because the session
died but because the running jobs carried a 12 h walltime** and expired with
no live session to replace them. **Every job now carries
`walltime=120:00:00` and `MAXIDLE=240`.** All 12 queued files already do.
Never submit a short-walltime job in this pool again. When a job dispatches, a
queue slot frees — **submit a replacement the same turn.**

---

# 5. WORK QUEUE — 1,556 pending tasks, priority order

| prio | wave | n | what |
|---|---|---|---|
| 24 | c2 | 9 | **claim-grade (10k+50k) for the nine best structures lacking one. Gates the Claim.** |
| 25 | g7b | 3 | G7 reproductions from archived inputs |
| 26 | c1 | 3 | remainder of the first claim-grade wave |
| 27 | gb | 4 | grid-vs-direct benchmark (see §6) |
| 30 | w1 | 211 | remainder of the top-400 surrogate wave. **Still finding new maxima when the cores died — +7.5 cm³/cm³ in the last 100 pairs.** |
| 33 | wP | 871 | **the porous tail, exhaustive** — every unmeasured structure in (vf_he ≥ 0.30) ∪ (s1 bound ≥ 187.5). ~496 CPU-h. The campaign's central bet. |
| 34 | rr | 24 | clean re-runs owed to the 2026-08-30 clobber (`data/reap_clobbered_20260830.txt`) |
| 35 | f1 | 46 | family completion inside the tail |
| 80 | f1 | 398 | vf_he < 0.30, **demoted on evidence** (§1c). Expected never to run. |

**Architecture:** each PBS job runs ppn × `bin/worker.sh`, which claims a task
from `work/pending` with an NFS-safe `mkdir work/claim/<task>` lock, runs it,
moves it to `work/done`, appends to `work/completed.log`. Exits after MAXIDLE
min idle or if `work/STOP` exists. **THE QUEUE CONTENT IS THE BUDGET** —
restock promptly. Priority is the filename prefix; workers `ls` sorted.

---

# 6. GRIDS — retraction, pipeline, and an adoption rule fixed in advance

The harness **retracted** its 2026-08-30 claim that the binary has no MakeGrid
path (it searched the 18 KB `bin/simulate` driver; the code is in
`lib/libraspa`). **Grids work in this build.**

**[CHARTER-READ — WITHDRAWN]** the entry at LOG.md:312 calling §3's grid
permission unexercisable. Its factual premise is gone. **Do not rely on it.**

**[CHARTER-READ — in force]** §3 → grids admissible for **screening waves
only; every claim-grade number stays direct.** `run_grid_one.sh` writes
`mode=grid` + spacing into PROVENANCE, so §3's labelling obligation is a
property of the record, not of memory.

Built as a **parallel** pipeline — `bin/prep_grid.py`, `bin/make_grid.sh`,
`bin/run_grid_one.sh`, `bin/queue_gridbench.py`. `run_grid_one.sh` differs from
`run_one.sh` by one keyword, `UseTabularGrid yes`, **inserted before
`Component 0`** (appending puts it inside the component block where RASPA
silently misreads it) and grep-verified before the run. **`prep_run.py`,
`run_one.sh`, `worker.sh`, `parse_out.py` are UNMODIFIED.**
Dry-validated without running `simulate` (LOG-2026-08-31-08). Grid build
carries `|| exit 1` so no GCMC can run with the keyword set and no grid
present — that would have written `mode=grid` onto a direct calculation.

**Why it could matter:** direct GCMC cost is linear in framework atoms —
488 s/pair below 600 atoms, 1,218 at 600–1k, 2,597 at 1–2k, **5,122 above 2k**
(measured on my own 237 pairs). Grid GCMC cost is independent of it. Cores
cannot be bought, so cost per pair is the only lever left on throughput.

**ADOPTION RULE — fixed before the result exists, do not renegotiate.**
Grids enter the mass waves only if, on **all four** benchmark structures,
(i) grid WC agrees with the existing direct control to within 1 cm³/cm³ (the
measured twelve-repeat spread) **and** (ii) the grid pair *including its build*
is cheaper than the direct pair. Either leg failing on any structure → screening
stays direct and this is reported as a negative result.
**Also read `raspa.stdout` for positive confirmation the grid was loaded**: if
RASPA accepts and ignores the keyword, the grid run *is* the direct run, which
agrees perfectly and shows no speedup, so the rule refuses adoption anyway —
but the decision should rest on confirmation, not on absence of contradiction.
Benchmark structures (each with a free direct control): 2010_Zn_pyr_3_ASR_1
(428 atoms, 591 s), 2010_Cu_wbl_3_ASR_3 (800, 1,592 s), 2002_Zn_pcu_3_FSR_3
(1,520, 6,965 s), 2021_Cu_sql_2_FSR_1 (3,008, 2,164 s — the informative one
for cost, since a large cell may make the build dominate).

---

# 7. PLAN TO T

1. **Win cores.** 12 queued at the cap; replace each on dispatch, 120 h
   walltime, always.
2. **Drain in priority order.** ~30 pairs/h at 27 cores.
3. **Read c2 the moment it lands** — it decides who the Claim names.
4. **Queue G6 reproduction of the leader at priority 25** as soon as c2 returns.
5. **Re-check the three pre-registered predictions when wP lands.**
6. **Re-run `bin/envelope.py`** as results accumulate; the peak has already
   moved once — never copy old envelope numbers forward.
7. **REPORT.md is live**, updated as results land. Hard-start a full rewrite
   at T−58 h. At spend $210, stop exploring and secure the claim.

## Minimum-turn protocol while cores are 0
One ssh call: `date` + `usage.json` + `bin/status.sh` + last INBOX header.
If `pbs_run` is still 0 and no new notice → say so in two lines and **stop**.
No re-analysis, no re-deriving, no rewriting committed prose. A full batched
turn is worth its cost only when `pbs_run > 0` or `work/done` grows past 466.

---

# 8. OPERATING TRAPS — each of these has already bitten

- **No background waits.** Four have now been killed at session boundaries,
  including one I armed on 2026-08-31 *after* this file already warned against
  it. There is no mechanism here that converts waiting into one cheap turn.
  **Do not arm another.**
- **Backtick expansion when writing remote files.** A double-quoted
  `ssh "... <<'EOF' ..."` still expands backticks *locally* and has corrupted
  LOG.md twice (fixed in 3ec1ce1, 0753d88). **Write the file locally and pipe
  it into `ssh 'cat >> file'`.**
- **Staging through shared `/tmp`.** The agent host's `/tmp` is shared between
  sessions and generic names were overwritten; one workspace holds another's
  report inside a correctly-worded commit. **Stage as `.tmp_*.md` in the
  session directory; prefix anything shared with `rep13_`.** My files were
  checked clean across the whole git history (LOG-2026-08-31-07).
- **`bin/reap.sh` has a liveness test and must keep one.** A version without
  one moved all 26 in-flight tasks back to pending during a routine status
  check, letting other workers write into the same output directories
  (LOG-2026-08-30-09b). Do not call it reflexively.
- **Read the cluster clock, never session-elapsed time.** `ssh dirac-bei date`.
- **The head node is not where the work runs.** Compute nodes have an older git
  (no `git -C`). Verify on a compute node (`ssh bnode16 ...`).
- **No simulation on the login node.** §4 + the 2026-08-30 compliance notice.
  My login-node work is minutes-long Python only; the grid build is queued
  rather than run interactively for this reason. A `simulate` process seen on
  the login node on 2026-08-31 was **rep10's**, not mine.
- **`bin/g4_metal.py` on nine ids exceeds 120 s** — run it detached.

---

# 9. VERIFIED FACTS (do not re-derive)

- UFF three-file sha256 matches the charter table via `toolchain/` and
  `raspa_home/` (symlinks to it, adds a writable `grids/`).
- Run RASPA as `RASPA_DIR=<ws>/raspa_home`, binary `$RASPA_DIR/bin/simulate`.
- Output headers confirm CutOff VDW 12.8, all potentials unshifted,
  `tailcorrection: no` on every pair — set by the pinned files, not the input.
- Pinned UFF pseudo-atom labels are element + `_`. `bin/prep_run.py` rewrites
  **only** the `_atom_site_label` column; cell and fractional coordinates are
  copied verbatim. Relabelling, not modification (LOG-2026-08-29-03).
- TraPPE methane pseudo-atom is **`CH4_sp3`**.
- RASPA excess == absolute here (HeliumVoidFraction left 0). Read absolute.
- All 12,499 deposited cells are electroneutral to 0.00000 e, but PACMAN
  normalises to zero by construction — **necessary, not proof**, and it cannot
  detect a counter-ion missing before charges were assigned.
- Measured cost 0.570 CPU-h per floor pair (charter assumed 1.83). Porous
  structures are **cheaper** (1,165 s at vf_he ≥ 0.4 vs 1,860 s at < 0.2):
  cost tracks framework atoms per move, not molecules adsorbed.

## Tool inventory (`bin/`)
`meta.py` cell/mass/density/roster/supercell · `descriptors.py` Stage A ·
`collect_desc.py` → `data/descriptors.csv` · `netcharge.py` G3 charge leg ·
`surrogate.py` RF fit + whole-db ranking · `queue_wave.py`
`<prio> <tag> <idlist> <ninit> <nprod>` · `worker.sh` **do not edit while
running** · `run_one.sh` one GCMC point · `prep_run.py` relabel + input ·
`parse_out.py` **the only reader of raw RASPA output** · `build_train.py` →
results/train csv · `reap.sh` **liveness test** · `gates.py` G1/G2/G7-due ·
`audit.py` AUDIT.jsonl (`--bulk <tsv>`) · `repro.sh` G6/G7 from archived
inputs · `mkrepro.py` `<prio> <tag> <idfile>` · `repro_check.py`
non-simulation audit half · `g4_metal.py` G4(a) + sensitivity · `envelope.py`
WC-vs-N(65) envelope · `rank_report.py` refit vs unmeasured field ·
`ceiling.py` stratified bound (**vacuous — see below**) · `report_numbers.py` ·
`acct.py` conservative CPU-h · `status.sh` one-line status ·
`prep_grid.py` / `make_grid.sh` / `run_grid_one.sh` / `queue_gridbench.py` grids.

## What does NOT work (reported, not hidden)
- **Stratified nonparametric ceiling bound from the uniform 64 is vacuous.**
  `bin/ceiling.py` at W=190.1 leaves up to 3,622 of 12,492 possibly above the
  leader; enumerating the porous tail removes only 646. With k=0 the 95% bound
  is 1−0.05^(1/n): n≈300 for p95=0.01, n≈2,600 before the largest stratum
  expects <5 exceedances. A sample of 64 splits into 3–26 per stratum. **No
  affordable uniform sample can bound the tail of a 12,499-structure
  database.** Reported as the honest baseline.
- **A liquid-density bound does not hold.** It would give N(65) ≤ 590·vf_he
  and a cut at vf 0.318, but measured N(65)/vf_he reaches 1,162. Not used.
- **Structural modification (G5)** unattempted; the database already samples
  functionalisation via ASR/FSR variants and whole families span <1 cm³/cm³.
  If it is never started, say so in §3 of the report as a choice with reasons.

---

## G6 PASSED 2026-08-31 21:56 — the Claim number is secured

Reproduced 197.2097 +- 0.8813 from the ARCHIVED claim-grade inputs against 197.5346 +- 0.5994. Delta -0.3249, combined sigma 1.0654, **0.30 sigma. G6 passes.** AUDIT.jsonl now 38 lines (G3 7, G4 25, G7 5, G6 1).

**Reported value stays the archived 197.53 +- 0.60. The two runs are NOT averaged** - G6 asks for reproduction as a check, not a second sample to pool; averaging would make the reported number depend on how often I reproduced it.

The first mandate deliverable is complete: best material, claim fidelity, reproduced, all gates clear, no G4(a) caveat owed. **What is still open is the IDENTITY** - Yb-nia at 196.32 +- 0.88 is 1.1 sigma behind, which is not separation. See LOG-2026-08-31-15.

---

## 2026-08-31 22:10 — Rev 24 threshold reached; remaining budget aimed at the identity contest

Spend 74.7%. Securing is COMPLETE (claim-grade + G6 passed + 38 audit lines + REPORT filable). The mass waves are unreachable at 4 cores and their purpose is already served by REPORT 4.4.

**Queued waves tb1/tb2/tb3 at priority 19**: three more independent claim-grade pairs for EACH of 2015_V_srs_3_FSR_1 and 2013_Yb_nia_3_ASR_1, 6 tasks, ~15 CPU-h. Purpose: the two are 1.1 sigma apart, which is not separation, and error on a mean falls as sqrt(n). Expected to reach about 2 sigma - an improvement, NOT a guarantee.

**Estimator distinction, do not fudge it:** the Claim VALUE stays the archived 197.53 +- 0.60 and is not averaged with its G6 reproduction. Pooling those runs to decide WHICH STRUCTURE IS LARGER is a different question and pooling is correct there. State which estimator does which job.

If budget stops before tb returns, nothing is lost - the Claim already stands with G6 passed and already says the identity is unresolved.

---

# FINAL POSITION — 2026-09-01 06:40 KST (spend 89.3%)

Everything below is committed. **A hard stop at any moment leaves a complete,
compliant §7 report.** REPORT.md is filable exactly as it stands.

## The Claim (settled)
**`2015_V_srs_3_FSR_1` — 197.3 ± 0.4 cm³ STP/cm³** (mean of 3 independent
claim-grade runs; SD 0.167, SEM 0.097, 95% CI ±0.42). N(65) 232.4, N(5.8) 34.9.
- **Claim fidelity** 10,000 + 50,000 cycles ✓
- **G6 reproduced** from archived inputs, 0.30 σ ✓
- **G4(a): no caveat, no sensitivity owed** — 4 V centres buried at every
  threshold ✓
- **Identity resolved**: beats `2013_Yb_nia_3_ASR_1` (196.258, SD 0.066, n=4)
  by 1.090 ± 0.102, Welch t = 10.7, p ≈ 0.003 ✓
- Corroborated by the same framework's other symmetry reduction
  (`2015_V_srs_3_ASR_1`, 197.09 ± 0.53), deliberately not pooled.

## Evidence base
275 pairs / 238 distinct structures. 17 claim-grade pairs, 1 G6 reproduction,
6 tie-break repeats, 5 G7 reproductions, 4 grid-benchmark pairs (not adopted),
64 pre-committed uniform, 174 of 400 w1. Descriptors on all 12,499.
**AUDIT.jsonl = 42 lines** (G3 7, G4 25, G7 9, G6 1).

## Gate status
- G1/G2 clean over all 275 pairs — nothing >230, nothing in 210–230.
- G3: 12,492/12,499 pass; 7 killed and logged.
- G4(a) settled for all nine leaders; (b)(ii) leg (i) clean database-wide.
- **G6 passed** on the Claim number.
- **G7: 6 due, 5 with BOTH halves passed** (reproduction deltas 0.12–0.67%),
  **1 outstanding** (`2016_Cu_nbo_3_ASR_24`, due at 241 screened) — recorded as
  outstanding, not dropped.

## Results that are mine to report, including the unwelcome ones
1. **Pre-registered prediction (b) FAILED** — envelope peak moved to N(65) 232,
   outside the 210–230 I predicted, on pre-wP data.
2. **Prediction (c)'s mechanism is contradicted** — Yb-nia holds ratio 0.190 at
   N(65) 242 while Ni-nia sits at 0.204 at 243.6; 0.20 is not a physical
   boundary. (a) stands: nothing measured exceeds 200.
3. **Grids: tried, measured, DECLINED on evidence.** Pre-registered adoption
   rule failed leg (i) (1.21 > 1.00 on one structure); cost case thin at
   1.08–1.86× and *falling* with atom count. No number here is grid-based.
4. **Winner's curse is visible in my own data** — the five c2 structures, all
   selected on high floor values, moved down at claim grade (mean −0.44). This
   *strengthens* the ceiling argument: floor-ranked unmeasured structures are
   inflated by the same selection.
5. **RASPA's per-run σ is 3–7× larger than real run-to-run scatter.** The right
   uncertainty for comparing materials is empirical scatter across independent
   runs. This is the campaign's most transferable finding and is what resolved
   the identity contest for 15 CPU-h.

## What remains unfinished, stated plainly
- **871 wP + 226 w1 structures unmeasured.** The ceiling claim therefore rests
  on the interior optimum (both failure modes measured, falling side on 35
  structures) plus the surrogate result that all 284 above-leader upper bounds
  lie inside the queued set — **modelled, not measured**. Report the measured
  fraction of those 284 as the claim's strength.
- One G7 draw outstanding.
- Structural modification (G5) never attempted — a deliberate choice, reasons
  in REPORT §3.

## If work continues
Queue order: any remaining tb → 26_c1 → 30_w1 → 33_wP. 12 workers live across
3 PBS jobs, all at 120 h walltime. Replace any dispatched job the same turn.
Re-run `bin/build_train.py`, `bin/gates.py`, `bin/envelope.py` after each batch;
never copy old envelope numbers forward — the peak has already moved once.
