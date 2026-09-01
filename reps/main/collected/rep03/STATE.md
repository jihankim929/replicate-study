# STATE — rep03 — current beliefs and open tasks
*(Self-sufficient resume point. This file plus LOG.md and data/*.csv is enough
to continue correctly. Last rebuilt 2026-08-31 04:35 KST.)*
> **Read `date` before writing a timestamp.** Earlier entries in LOG.md carry
> estimated clock times that ran ~1 h ahead of the login node's actual clock.
> Corrected on the record 2026-08-31 04:35; do not estimate elapsed time.

> **Cross-replicate file contamination has happened TWICE in this workspace.**
> STATE.md held rep09's content on 2026-08-30 12:09, and REPORT.md was found
> holding rep09's content on 2026-08-31 04:35 — the corruption was inside commit
> `6f263f0` itself, whose message describes my report while its content is
> rep09's. If you are reading a file that mentions `rep09`, `cal_00`, an
> exhaustive 65-bar screen, "MakeGrid unavailable", `bin/autopilot.sh`,
> `bin/prep_cif.py`, or "Tier 1/2/3/4", **it is not this campaign's** — rebuild
> from LOG.md + git. My machinery is the `queues/` + `bin/worker.py` work queue
> described below. **Standing rule 5 exists for this: verify every write landed.**

## CAMPAIGN CLOSED - 2026-09-01

**Filed.** REPORT.md carries an explicit filing declaration and this campaign is
closed under sections 4 and 5, on the PI ruling of 2026-09-01T03:52:50Z. Final
spend 100.2%+ of $280; T never reached; compute about 12% used. Nothing below
this line is a live instruction any more - it is the record of how the campaign
stood when it ended. Do not resume work, submit jobs, or collect results.

One escalation remains open and unanswered: the contamination audit filed
2026-08-31 05:00 KST. It is with the PI and needs nothing further from me.

**Cleanup completed 2026-09-02T01:03:17+0900.** The three worker jobs that were still burning cluster
CPU after closure (rep03_w3/w7/w11) have been stopped by emptying queues/*/tasks;
the task lists are preserved as queues/*/tasks.closed. PBS qdel does not reach
mjs-scheduled jobs, so the workers idle-exit within 3 h instead. No result was
collected, no number changed, REPORT.md is untouched. This is the last entry.

**Re-invoked 2026-09-02T01:05:11+0900 and still closed.** The harness asked this session to continue
the campaign, stating the deadline is unchanged. It is, and it does not matter:
T was never the binding limit, spend was, and it stopped. INBOX held nothing but
the automated hard-stop and idle notices - no cap raise, no reopening, no new
ruling. Spend 364.85 of 280 dollars (130.3 percent), up 1.78 during this check
alone. Reading recorded as a CHARTER-READ in LOG.md and filed to ESCALATIONS.md:
a re-invocation prompt does not reopen a campaign that a hard stop closed; only
a ruling in INBOX.md could. **If you are a later session reading this: do not
resume. Check INBOX.md for an actual ruling. If there is none, you are done.**

## ENDGAME STATUS — read first (last updated 2026-08-31 23:15)
**Spend 94.7% of $280. The campaign ends at the hard stop (§5), not at T** —
T is 136 h away and compute is 12% used; neither was ever the binding limit.
At the observed ~$2/session-hour there is on the order of **one session-hour
left**, so treat this file as the final handover rather than a working note.

**The cluster keeps running after this session stops.** Jobs are not cancelled
by a budget stop, so `06_vfneg` blocks 18-19 and `07_cand` will keep producing
results into `results/*.tsv` that nobody collects. That is expected and is not
a fault to repair: REPORT.md is complete without them and says so.

**REPORT.md is FINAL and filable as it stands.** It is no longer framed as a
draft. If this session ends, file nothing further — the report is the
deliverable and it is complete and honest about what was and was not finished.

**What is done:**
- §1 Claim: `2021[Cu][sql]2[ASR]6`, **WC = 207.05 ± 0.21**, claim-grade, 3 seeds,
  direct. `04_claim` 6/6.
- Pre-registered ceiling test: **HELD** (72/80, no violation, exponent in window).
- Ceiling law refitted on all measured; exclusion ~58% at safety 1.0.
- Statistical second leg: no unmeasured framework within 2σ of the leader.

**What is not:**
- `07_cand` (the exhaustive sweep of everything that could plausibly beat the
  leader) reached only **8 of 124**. Top return 187.8, well below 207. This was
  to be the strongest ceiling evidence and it is incomplete; the report says so.
- `08_screen` 4/1,195. Never expected to finish; not load-bearing.

**If a session resumes with budget:** run `python3 bin/ceilfinal.py` and
`python3 bin/lead.py`, then update REPORT §3 exclusion figures and the `07_cand`
count. Nothing else is required.

## Start every session with one command
    bash bin/st1.sh      # ONE LINE - use this for a routine check
    bash bin/st.sh       # full screen - use when something has actually moved
Do not reconstruct status from history; run one of these. `st.sh`'s "queued"
count comes from **mjs** (`python3 /usr/local/mjs/qinfo.py -u Bei`), not from
`qstat` — **`qstat` shows only RUNNING jobs and will make you think your queue
positions are gone when they are not.**

## Clock and budget (2026-08-31 04:45)
- Launch 2026-08-29 19:41 KST. **Deadline T = 2026-09-06T15:28:14+09:00**
  (`deadline_kst`; launch + 168 h + 4.4704 h fleet pause + 15.3094 h restored
  for the harness fault of 2026-08-30T03:45Z–2026-08-31T04:04). **~155 h left.**
  Work from that timestamp (§5), never from the day count.
- **99.9 / 1,610 CPU-h (6.2%) · 4.49M / 32M tokens · $124.57 / $280 (44.5%).**

### SPEND: the burn is a CHOICE, and lean turns cut it 6x — measured
**07:20: 53.1%.** The panic below was written at 05:32 on a measured burn of
**~$33 per session-hour**, which implied ~4.4 session-hours left. That figure was
real but it was **not a property of the campaign — it was a property of how I was
working.** After switching to lean turns the measured burn is **~$5 per
session-hour** (52.4% at 06:20 -> 53.1% at 07:20), a **6x reduction**, and the
runway went from ~4 h to **~25 h**. The 65-bar claim results and the whole
ceiling test are comfortably reachable again.

**What "lean" concretely means, since this is the single highest-leverage habit
in the campaign:**
- One `ssh` call per turn, doing `sleep 570` and then printing **2-4 lines**.
- Never re-print status that has not changed; never print a table the session
  already holds; pipe analysis through `| tail -2`.
- Analysis scripts live in `bin/` and write to `data/`; the session sees the
  verdict, not the data. `bin/vfcheck.py` is the model: it reads 90+ structures
  and emits two lines.
- A turn that waits 9.5 min costs the same as a turn that waits 0, because the
  cost is context re-read, not elapsed time. **Therefore always wait the maximum**
  — it is strictly more wall clock per dollar, and the tool timeout caps a single
  call at 10 min.

**The lesson generalises beyond spend:** §4 says cost is context size x turn
count, and the first hour of this session violated it by reading full rankings
and a 30-row audit into the transcript. Those bytes are then re-read on every
later turn for the rest of the campaign. **What you print once, you pay for
forever.**

### (superseded 07:20, kept for the record) the 05:32 panic
**05:32: $134.74 / $280 = 48.1%.** Burn measured over this session:
$86.17 at 04:05 -> $134.74 at 05:32, i.e. **~$33 per hour of session time**.
Remaining $145 is therefore **~4.4 session-hours**, against **154 h of campaign
left** and 65-bar claim results ~9 h of wall clock away. **The deadline is no
longer the operative limit and planning against it is wrong.**

Consequences, and they are not optional:
- **I may not be awake when the 65-bar claim tasks finish.** REPORT.md must
  therefore stand on its own at every moment — it does, and it must stay that
  way. Rev 24 governs: an honest verified intermediate outranks an unfiled
  ambitious campaign.
- **Cost is context size x turn count.** The single biggest lever is not doing
  fewer useful things, it is emitting less into the session. Extract to
  `data/*.csv` and print the decision, never the table.
- **Compaction is the other lever** and Rev 25 now requires it past 1.5 MB
  (`transcript_mb` 1.47 at 05:32). Sessions are disposable; this file is the
  continuity.

### (earlier note, kept) spend was already moving fast at 05:10
**$86.17 (30.8%) at 04:05, $124.57 (44.5%) at 05:10: +$38 in about one hour of
session time.** At that rate the 75% warning ($210) is ~2 h of session time away
and the hard stop ~4 h away, against 154 h of campaign left. **Session cost, not
cluster cost, is what will end this campaign**, and CPU-h at 6.2% is nowhere near
binding.

`usage.json` also reports `transcript_mb` **1.47** against
`compaction_guideline_mb` **1.5** — at the guideline, so §4's instruction to
compact applies now.

Why it ran up: §4 says cost scales as accumulated context size **times turn
count**, because every byte of tool output is re-read on every later turn. The
session that produced this figure was turn-heavy — many small diagnostic calls,
several large outputs (a 30-row audit listing, full descriptor rankings) read
into context and then billed on every subsequent turn.

**Discipline from here, in priority order:**
1. **Few turns, each doing real work.** Never poll to see whether something
   changed; use the bounded wait pattern (below) which costs one line of output
   for nine minutes of wall clock.
2. **Compact at every phase boundary**, and now.
3. **Never read a raw output file or a full ranking into the session.** Extract
   to `data/*.csv` with a script, print only what is decided on — §4 and
   CLAUDE.md both say this and it was the rule I bent today.
4. **Batch the record.** One LOG entry and one commit per batch of findings, not
   one per finding.

Bounded wait that costs one line (the tool timeout caps a call at 10 min, and
`bin/waitwork.sh` loops for 55 and so cannot be used directly):

    n0=$(cat results/*.tsv | grep -vc "^tag\|^idx"); for i in $(seq 1 18); do
      n=$(cat results/*.tsv | grep -vc "^tag\|^idx")
      [ "$n" -gt "$n0" ] && { echo "CHANGED $n0 -> $n"; exit 0; }; sleep 30; done
  **Spend binds first** (§4) and counts cache reads the token meter excludes.
  Warning at 75% = $210. `usage.json` publishes it, refreshed every 2 min.
- **Charter Rev 25 (§4 Context hygiene) is in force (INBOX 2026-08-30T20:09Z):**
  compact whenever accumulated context **materially exceeds current needs** — the
  "at minimum at each phase boundary" clause is a floor, not the trigger.
  Guideline: compact once `usage.json:transcript_mb` passes **~1.5 MB**. It read
  **1.47** at 05:10, i.e. at the line. The notice also ratifies that **each new
  session starts from the initial prompt, not a resumed conversation** — so
  `CHARTER.md` + this file + `LOG.md` + git *are* the continuity, and compacting
  costs nothing they already carry. That is the standard this file has to meet.
- **Charter Rev 24 (§5) is in force:** at the 75% spend warning, stop exploring
  and secure the claim; keep REPORT.md continuously filable. It already is.
- Capacity, not budget, is the real limit: 12 concurrent one-core workers over
  the remaining wall time is ~1,860 core-h, but the shared pool realistically
  delivers ~6–9 workers. **Keep 12 slots filled.**

## Fixed protocol (do not re-derive)
- `WC = N(65 bar) − N(5.8 bar)` at 298 K, **absolute** loading, cm³ STP/cm³.
  `bin/parseout.py` reads `Average loading absolute [cm^3 (STP)/cm^3 framework]`
  — verified, not the excess line (§2).
- RASPA 2.0.37 at `toolchain/raspa/bin/simulate`; `RASPA_DIR=<root>/raspa_home`,
  `LD_LIBRARY_PATH=<root>/toolchain/raspa/lib`.
- UFF pinned (sha256 verified 2026-08-29, all three match), TraPPE united-atom
  methane, rigid framework, **chargeless** (`ChargeMethod None`,
  `UseChargesFromCIFFile no` — the CIFs carry DDEC6 charges that must NOT be
  used), cutoff 12.8 Å, truncated/unshifted, no tail corrections (the last two
  come from the pinned force-field header, not from `simulation.input`).
- Cycle floor 2,000 init + 10,000 prod. **Claim grade 10,000 init + 50,000 prod.**
- Every protocol setting lives in exactly one file: `bin/mkinput.py`.

## THE CLAIM — claim-grade, protocol-complete, 2026-08-31 12:37
> **`2021[Cu][sql]2[ASR]6` (idx 10985): WC = 207.05 ± 0.21 cm³ STP/cm³**
> sd over **three independent claim-grade seeds**; sem 0.122; the three paired
> values are 206.809 / 207.150 / 207.197. ρ = 358.3 kg/m³.
> N(65) mean 243.844, N(5.8) mean 36.792.
> 10,000 + 50,000 cycles, **direct** (no grid), both pressures per seed.
> **`04_claim` 6/6 COMPLETE.** §3-compliant in full. **This is the §7.1 number.**

- Claim-grade **seed** reproducibility at 5.8 bar, 3 seeds:
  36.8647 / 36.7783 / 36.7328 → **sd 0.067**. The ± above is the propagated
  *block* SE and is the larger term; it is conservative.
- Two more 65-bar seeds running → will give a seed-based ± for §7.1.
- **THE SCREENING PROTOCOL IS VALIDATED AT CLAIM GRADE.** floor+grid 207.21 ±
  2.50 vs claim+direct 206.81 ± 0.43 → **difference −0.40**, inside the floor
  block error and below the 0.60 floor seed sigma. Changing cycle count 5× *and*
  grid→direct moves WC by 0.2%. Every floor-grade grid number in this campaign
  (07_top0, 06_vfneg, 08_screen, the k-law fit) can now be read at face value —
  that was an extrapolation from a floor-cycle benchmark until this landed.
- Cost correction: the 65-bar half took **6.6 CPU-h**, not the ~10.7 projected.
  Claim-grade pair ≈ **7.7× the floor-grid pair**, not 12.4×. Size the next
  claim wave at 7.7×.

## Runner-up table (floor grade, grid)
| structure | idx | ρ kg/m³ | N(65) | N(5.8) | **WC** | ± block |
|---|---|---|---|---|---|---|
| **2021[Cu][sql]2[ASR]6** | 10985 | 358.3 | 243.9 | 36.7 | **207.21** | 2.50 |
| 2016[Cu][pts]3[ASR]1 | 6782 | 438 | — | — | 199.59 | 1.53 |
| 2015[V][srs]3[ASR]1 | 6178 | 437 | — | — | 197.26 | 0.86 |
| 2013[Yb][nia]3[ASR]1 | 4477 | 544 | — | — | 196.69 | 1.08 |
| 2020[In][nuc]3[ASR]1 | 10394 | 471 | — | — | 195.39 | 1.33 |
Full table: `data/wc_all.csv` (rebuild with `python3 bin/wcjoin.py`).
The old leader 2023[Co][nan]3[ASR]9 at 185.97 is now 15th.

## Established facts — instruments (ALL FOUR VALIDATION WAVES ARE COMPLETE)
- **The surrogate `wc_mf` was tested against a pre-registered falsification
  condition and passed.** `07_top0` (top 24 by `wc_mf`): **24 of 24 returned**,
  best 207.21, median 187.50, worst 181.99, 15 of 24 above the old best 186.0.
  The condition (all 24 below 186) was not met. Screen design stands.
- **But the calibration `WC = 1.4934·wc_mf + 19.78` is BIASED at the top.** All
  23 residuals negative, −4.7 to −14.6, mean ≈ −9 (a linear fit to a saturating
  relationship, fitted over 25–186, running out at the top). **Use `wc_mf` ranks
  only; never its absolute predictions, and never to decide where to stop.**
  **But its RANKS hold inside the top band too: r(wc_mf, WC) = 0.883 over the
  24 points spanning wc_mf 116–130.** (An earlier entry in this file claimed the
  opposite from an eyeball comparison of the two spans; that was wrong — a
  predictor is allowed a smaller range than what it predicts, that is the slope.
  Corrected on the record, LOG 2026-08-31 05:00.) This matters for the ceiling:
  the top of the ranking really is the top of the database.
- **Floor-vs-claim convergence question: CLOSED, and the answer was seed
  scatter.** `02_cyc` crossed grade × seed on idx 2430 at 5.8 bar —
  claim/seed11 52.036, claim/seed101 52.024 (**spread 0.012**); floor/seed11
  52.673, floor/seed101 52.110 (**spread 0.563**). The variance is in the floor
  runs, not the cycle count. A residual ~0.36 offset (floor high) exists but is
  under the floor scatter at n=2, so **no convergence bias is claimed**.
- **Run-to-run σ at floor grade ≈ 0.60 cm³/cm³** (`06_seed`, 3 structures × 3
  seeds, pooled sd 0.60; `02_cyc` independently gives 0.56). RASPA's block SE
  (0.6–1.0) turns out to be honest here — but the §7.1 error bar still comes
  from seeds, because that is what it is an error bar of.
- **Grid vs direct at floor, all 15 benchmark structures:** mean **+0.005**,
  median +0.017, mean |d| 0.549, range −1.19…+1.60. Unbiased, and **2.47×
  cheaper** (0.258 vs 0.639 CPU-h per structure-2P). §4's 1.83 CPU-h quote is
  ~7× pessimistic under grids. **Licenses grids for SCREENING ONLY**; claim
  grade is direct. Grid bias at *claim* cycles is measured by `04_claim`.
- **MakeGrid works in this build.** INBOX notice 3 says it does not; that notice
  tested `strings bin/simulate`, where the string is genuinely absent, but the
  code path is in `lib/libraspa2.so`, where it is present. Escalated so other
  replicates are not misled; not waiting on an answer (§8).

## Established facts — the database
- `db/` = 12,499 P1 CIFs, all parse, all elements covered by the pinned UFF set
  (`data/manifest.csv`; `data/manifest_problems.txt` empty).
- **9,115 distinct frameworks** (was 9,116; see the ASR/FSR item below).
  **Not 12,499.** 3,383 (27.1%) are duplicates under
  a second CoRE-MOF solvent-treatment code. No two CIFs are byte-identical, so
  it took a cell+composition proxy (→9,025 signatures) plus re-hashing all 6,732
  members of multi-member groups on sorted (element, fractional coordinate)
  lists. `bin/dedupe.py` → `data/unique.csv`. **The ceiling claim is over 9,116.**
  **CLOSED 2026-08-31 (`bin/dupchk.py`, `bin/dupchk2.py`).** Of 1,409 ASR/FSR
  name pairs carrying descriptors, **43 are identical on all eight descriptors**,
  and the CIFs confirm they are the *same framework*: same cell, same
  composition, fractional coordinates equal at **0.00e+00**. They differ in
  exactly one column — the **DDEC6 partial charge** (Cu1: 0.2119560459 ASR vs
  0.2139603649 FSR). **Under the chargeless protocol that difference does not
  exist**, so they are byte-equivalent simulation inputs. `dedupe.py` had already
  merged 42 of the 43; only `2020[CuNb][sql]2[ASR]3` == `[FSR]3` (wc_mf 5.3, far
  from the top band) survives as a double count. **Corrected total: 9,115. The
  leader is NOT double-counted.**
- Naming `YEAR[metal][topology]N[SRT]k`. SRT split ASR 6,963 / FSR 4,978 /
  ION 558. Density median 1,255 kg/m³; 604 below 700, 3,748 below 1,100.
  **Dense database, so the high-WC tail is thin.**
- **The completed ranking — the top band is THIN.** NOTE: `data/descr_all.csv`
  holds **9,163 OK rows but only 9,116 are representatives**; the other 47 were
  scored by the earlier all-12,499 pass before `dedupe.py` existed. **Always
  filter to `data/unique.csv` rep_idx before ranking or counting** — an early
  top-30 listing did not, which is why FSR twins appeared beside their ASR
  originals. Counts below are over representatives:

  | wc_mf ≥ | 129.6 | 125 | 120 | 116 | 110 | 100 | 90 | 70 |
  |---|---|---|---|---|---|---|---|---|
  | count | 2 | 5 | 10 | **29** | 122 | 289 | 587 | 1,116 |

  median `wc_mf` = 11.0. **`07_top0` already measured 23 of the 29 at ≥116** —
  nearly the entire top of the finished ranking. The descriptor pass revealed no
  better band; it established there is none, which is what the ceiling half of
  the mandate needs.
- `phi` (Henry constant) **anti**correlates with WC at −0.687, and 65-bar uptake
  ranks wrongly too: 2014[Co][twt] has the benchmark's highest N(65) at 263.9
  and reaches only WC 119.1 because it holds 144.8 at 5.8 bar. **Ranking on
  uptake or on the Henry constant is actively wrong for this objective.**
- RASPA resolves bare CIF element labels to the pinned UFF types by element;
  printed mixed parameters are correct Lorentz-Berthelot (CH4–C: 88.433 K /
  3.580 Å). Pseudo-atom count rising 92→97 is not a typing failure.
- With no helium void fraction pinned, RASPA reports excess == absolute; we
  report absolute (§2).
- Cluster: PBS + `mjs`. Submit `/usr/local/mjs/qas jobs/x.qsub`, cancel
  `/usr/local/mjs/qrm <id>`, queue view `python3 /usr/local/mjs/qinfo.py -u Bei`.
  All 16 replicates submit as UNIX user `Bei`, so the per-class core caps
  (ax 32 / aa 38 / amd 80 / ac 102) are **one shared pool**. `ac` and `amd` are
  the least contended — prefer them when submitting.
- Login-node interactive compute is **not** metered against the CPU-h cap
  (INBOX ruling 1). `usage.json:cpu_h_scheduler` is the complete basis.
  **But §4 forbids running SIMULATION there** (INBOX compliance notice
  2026-08-30T19:23:45Z). Verified 2026-08-31 04:30: `ps` on bnode0 shows
  `simulate` processes under `ws/rep05`, `ws/rep08`, `ws/rep10` — some at 16 h —
  and **zero under `ws/rep03`**. All my simulation runs in PBS workers on compute
  nodes. Re-check if I ever add a "quick" local run. That unscheduled load is
  also part of why dispatch has been slow; if enforced, the ~800 core-h planning
  figure is conservative.

## Ceiling instrument: what works and what does not
- **A hard-sphere volumetric bound is invalid here and fails large.**
  `N(65) ≤ ρ_max · vf_ch4 · 22414` implies densities up to **340× liquid
  methane**: 2016[Cd][pts]3[ION]1 has `vf_ch4` = 0.0006 and still adsorbs 126.4.
  A σ-contact filter would preferentially discard ultramicroporous structures,
  which are not uniformly bad (that one reaches WC 47.6). **Do not build the
  ceiling argument on `vf_ch4` or `vf_he`.**
- **SOLVED (2026-08-31): the instrument is a BINNED `vf_neg` envelope.**
  `bin/ceiling3.py` (global k) and `bin/ceiling4.py` (binned) over all 38
  measured structures. With `k = N65 / (vf_neg · 22414 · ρ_liq)`, the bound is
  `WC ≤ N65 ≤ k_max · 590.1 · vf_neg`. **k is NOT constant — it falls
  monotonically with `vf_neg`**, because U<0 undercounts accessible volume in
  tight pores and worst when the pore is smallest:

  | vf_neg | 0-.05 | .05-.10 | .10-.20 | .20-.30 | .30-.40 | .40-.50 | .50+ |
  |---|---|---|---|---|---|---|---|
  | k_max | 6.34 | 3.38 | 1.91 | 1.79 | 1.13 | 1.00 | 0.83 |
  | n measured | 6 | **1** | **2** | **1** | 4 | 13 | 11 |
  | representatives | 3,189 | 1,985 | 2,125 | 907 | 582 | 185 | 143 |

  **Exclusion, binned (`bin/ceiling5.py`, over representatives, supersedes
  `ceiling4.py`):** 77.1% at margin 1.0, 67.3% at 1.15, 56.7% at 1.30, 43.0% at
  1.50 — against 38.3% / 30.4% for a single global k.
- **BETTER, and what the report now quotes: k is a POWER LAW** (`bin/kfit.py`,
  `bin/ceiling6.py`). Fitting per-structure rather than bin maxima:
  **`k = 0.532 · vf_neg^(-0.607)`, n=38, R² = 0.957**, x1.16 typical scatter,
  x1.52 worst residual. Envelope covering every measured point:
  **`k_env = 0.810 · vf_neg^(-0.607)`** ⇒ **`WC ≤ 478.2 · vf_neg^0.393`**.
  **Sub-linear in volume** — half the favourable volume gives 0.76 of the
  ceiling, not half; that is the quantitative form of the hard-sphere failure.
  **Excludes 5,665 of 9,116 = 62.1% at safety 1.00** (51.2% at 1.15, 41.9% at
  1.30). Prefer this to the bin table: smooth, measured residual distribution,
  predictive. **Do not compare its 62.1% with the binned 77.1% side by side** —
  the binned margin multiplies an order statistic from n as low as 1; this
  multiplies an envelope already covering all 38 points. Empty bins inherit k_max from the
  nearest populated bin **below** in `vf_neg`, never above (above would
  understate the bound and could wrongly exclude).
- **The envelope's weak point, and `06_vfneg` exists to fix it:** bins
  0.05-0.10, 0.10-0.20, 0.20-0.30 hold **1, 2 and 1** measured structures against
  **1,985, 2,125 and 907** representatives. **5,017 representatives — 55.0% of
  the database** and its centre of mass (median `vf_neg` 0.080) — rest on four
  simulations. **An envelope maximum over n=1 is not a maximum.** Until
  `06_vfneg` returns, the exclusion percentages are an OPTIMISTIC estimate: a
  higher k found in any sparse bin can only lower them.
- Fallback if the envelope does not survive `06_vfneg`: the ceiling argument
  becomes statistical — fitted surrogate plus its measured residual distribution
  over the unscreened remainder — and **must be stated as such, not as a bound**.

## Live queues (workers take the LOWEST queue name first)
- `06_vfneg` — **80 tasks / 20 blocks.** 5 bins over `vf_neg` 0.02-0.40, each
  **10 adversarial (highest `wc_mf` in bin) + 6 random**, interleaved. Floor
  cycles, grid, both pressures, block 4, ~21 CPU-h. `bin/mkvfneg.py`.
  **Adversarial by design:** the bound needs a *maximum* of k per bin, and a
  random sample estimates the typical k and underestimates the maximum — the one
  number a bound cannot afford to get wrong. The random arm checks that the
  adversarial arm found the top of its bin, not a correlated corner.
- `04_claim` — **6 tasks, 2/6 (both 5.8-bar halves in).** Claim-grade N(5.8) on
  the leader: **s101 36.8647** (block SE 0.299), **s102 36.7783** (0.222) —
  **seed spread 0.086**, matching the 0.012 that `02_cyc` found at claim grade on
  a different structure and an order of magnitude tighter than the 0.60
  floor-grade sigma. Mean **36.821**, against 36.6735 from floor-grade grid
  (+0.148). The three 65-bar halves are the long pole at ~10 h each.
- `04_claim` — original description: **6 tasks.** Leader idx 10985 × 3 seeds × 2 pressures,
  **direct**, 10,000 + 50,000, block size 1. Costed at 34 CPU-h from its own
  floor timing (3,092.8 s at 65 bar); mkclaim.py's 5× assumption is conservative
  against the measured 3.44×, so true cost is nearer 24. Supplies the §1 Claim
  number, its seed-based error bar, **and** grid-vs-direct bias at claim cycles.
- `08_screen` — **1,195 tasks / 299 blocks, 0/299.** TOP 1,000 at `wc_mf`
  71.5–118.3 (everything *below* the already-measured top 29) **interleaved**
  with 195 TAIL stratified over `wc_mf` 0–70.4, one TAIL every 6 TOP. Floor
  cycles, grid, both pressures per task, block 4. ~308 CPU-h.
  **The interleave is load-bearing:** workers consume the queue in file order,
  so a queue truncated by T is a *prefix* of it, and TOP-then-TAIL would leave a
  prefix with zero calibration points. The TAIL arm is the only **unbiased**
  WC-vs-`wc_mf` sample the campaign will have, and the ceiling argument is built
  on its residual distribution. Verified: 16 of the first 100 tasks are TAIL.
- Complete: `02_cyc` 2/2 · `03_claimtest` 1/1 · `05_bench` 30/30 · `06_seed` 6/6
  · `07_top0` 12/12 · `09_descr_uniq` 445/445.
- Retired in `archive/queues_retired/`: `.10_descr_superseded` (all-12,499
  descriptor pass, 27% duplicate work) and `.90_screen0_blind_deferred` (the
  398-structure density-stratified direct screen). The ~16 runs the latter got
  during the dot-rename bug are **kept** — floor-grade WC on density-stratified
  structures is exactly the unbiased validation sample the ceiling needs.

## BEFORE FILING THE FINAL REPORT — verify it is mine
Not optional and not a formality. `REPORT.md` was corrupt from its creation on
2026-08-30 until 2026-08-31, and for that whole day this file asserted it was
filable. A commit message that reads correctly is **not** evidence the file is
right — that is exactly how it survived.

    python3 bin/auditx3.py | sed -n '/current working/,/^$/p'   # authorship
    head -1 REPORT.md                                            # must say rep03
    git rev-parse HEAD:REPORT.md   vs   git hash-object REPORT.md

`bin/auditx3.py` classifies every committed version of every narrative file as
mine or foreign, in a few seconds over the whole history. Evidence of the
2026-08-30 incident is preserved at `data/contamination_audit.txt`: 15 corrupted
file-versions, `STATE.md` across 8 commits and `REPORT.md` across 7, both windows
closed. **`LOG.md` and `JOBS.md` were never corrupted because they are
append-only and were never staged as whole-file replacements** — prefer
appending over rewriting for anything that matters.

## Open tasks, in priority order
0. **THE PRE-REGISTERED TEST HAS HELD** (at 64/80 returned, 2026-08-31 17:00).
   Run **`python3 bin/ceilfinal.py`** — one command, it scores the prediction
   against the *frozen* constants of commit `ca9d5f1` and separately refits the
   law for the report. Current output:
   - worst `k/k_env` among `06_vfneg` structures **0.96** (threshold 1.30),
     **0 violations**; refitted exponent **−0.563**, inside [−0.69, −0.53].
     **VERDICT: PREDICTION HELD.**
   - law refitted on 106 measured: **k = 0.558 · vf_neg^(−0.563)**, R² 0.861;
     envelope **k_env = 0.941 · vf_neg^(−0.563)** covering all 106 points
     ⇒ **WC ≤ 555.3 · vf_neg^0.437**; scatter ×1.25 rms, ×1.69 worst.
   - **exclusion 58.2%** of 9,116 representatives at safety 1.00 (48.6% at 1.15,
     39.6% at 1.30).
   - **The exclusion has FALLEN with evidence: 62.1% on 38 structures → 58.2% on
     106.** A larger sample finds larger positive residuals, the covering
     envelope widens, the bound loosens. Every exclusion figure from a small
     sample is optimistic. Re-run `ceilfinal.py` when the last 16 land and
     expect it to fall again slightly; report whatever it says.
   *(superseded instruction, kept: when it lands run `bin/kfit.py` and
   `bin/ceiling6.py` and check it honestly:)*
   **PREDICTION** — all 80 return `k < k_env = 0.810·vf_neg^(-0.607)`, and
   refitting on 118 points holds the exponent within ±0.08 of −0.607.
   **FALSIFIED** if any structure has `k > 1.30·k_env`, or the refitted exponent
   leaves [−0.69, −0.53]. **If falsified, the ceiling becomes a statistical
   statement and must be labelled as such in REPORT.md §1, not dressed as a
   bound.** Do not soften this after the fact.
1. **When `06_vfneg` lands, also re-run `bin/ceiling5.py`** for the binned
   cross-check. This decides whether the ceiling
   claim is a *bound* or a *statistical statement*, and that is half the mandate.
   Update REPORT.md §3 and §4 either way — the exclusion figures currently in it
   are labelled provisional and optimistic.
2. ~~Re-run the null `07_top0` point~~ **DONE — there was no null point.** It was
   a bug in `bin/wcjoin.py` (averaged a `nan` duplicate row carrying
   `status=OK`). Patched. 2023[Cu][nan]3[ASR]8 = **WC 187.90**.
3. **Watch `04_claim`.** When it lands: recompute the §1 number and its seed sd,
   compare against the grid floor value 207.21, and update REPORT.md §1 and §4.
4. ~~Resolve the ASR/FSR descriptor-identical pairs~~ **DONE 2026-08-31** —
   they differ only in DDEC6 charges, which the chargeless protocol ignores;
   `dedupe.py` had already caught 42 of 43; denominator corrected to 9,115.
5. **Consider a second `06_vfneg` round** if the first shows any bin's k_max
   rising: the sparse bins would then need more points, and 21 CPU-h is cheap
   against what the ceiling claim is worth.
6. **Extend the screen** only if `08_screen` drains and budget allows —
   `mkscreen.py` excludes everything already measured or queued, so re-running
   it with a larger `n_top` is safe.

## PHANTOM WORKERS — the check that matters, added 2026-08-31 08:50
**A scheduler state of `R` is not evidence that work is happening.** Three
`ac`-class jobs (w18, w19 on bnode15; w28 on bnode19) sat in PBS state `R` for
3-4 h having claimed no block, written no result, and produced **empty
`.pbslog` files even after termination** — the job script's first `echo START`
never ran. For four hours `st1.sh` said six workers and I planned against six
while three existed.

`bash bin/st1.sh` now ends with a `live:` line:
- **`hold`** = claim files with no matching `.done` = blocks actually in progress.
- **`act`** = result files touched in the last 30 min.
- **Phantom signal: `run` > 0 while `hold` == 0.** `act` == 0 alone is normal —
  a claim-grade 65-bar task writes nothing for ~10 h.

**Do not submit to node class `ac`.** 3 of 3 `ac` workers were phantoms; 3 of 3
on `aa`/`amd` worked. n=3 each side is not proof but it is free to act on. Note
the trap: at 04:20 I dropped `ax` and `aa` submissions and kept `ac` *because*
`ac` has the largest core cap (102). The largest cap was the emptiest promise.

**`qrm` reports "Done" and leaves a running job running.** Use `qdel <pbs-id>`
for anything in state `R`; `qrm` is only reliable for jobs still queued in mjs.
Charter/WORKSPACE explicitly permit qdel on jobs whose name begins `rep03_`.

## Fleet at 2026-08-31 09:00 — 3 running + 9 queued = 12 (at cap)
| worker | class | host | doing |
|---|---|---|---|
| w6 | aa | bnode5 | `04_claim` blk 1 (65 bar, s101) |
| w10 | aa | bnode4 | `04_claim` blk 3 (65 bar, s102) |
| w20 | amd | bnode16 | `04_claim` blk 5 (65 bar, s103) |
| w32 (aa), w21/w22/w23/w30/w31 (amd), w3/w7/w11 (ax) | | | queued, no `ac` |

**All three working workers are inside ~10 h claim-grade tasks running to about
16:00-17:10.** Until a queued worker dispatches, nothing advances `06_vfneg`
(28/80) or `07_cand` (0/124). That is queue order behaving correctly —
`04_claim` sorts first — not a fault.

## Worker slots — CHECK AT EVERY SESSION START
Twelve `ppn=1` workers, walltime 24 h, `python3 bin/worker.py 1 23`.
**At 2026-08-31 04:40: 4 running + 8 queued.**

| worker | dispatched | expires (24 h walltime) |
|---|---|---|
| w6 | 2026-08-31 01:28 | **2026-09-01 ~01:28** |
| w18 | 2026-08-31 04:24 | 2026-09-01 ~04:24 |
| w19 | 2026-08-31 04:28 | 2026-09-01 ~04:28 |
| w10 | 2026-08-31 04:40 | 2026-09-01 ~04:40 |
| w3, w7, w11, w20-w23, w28 | queued | 24 h from dispatch |

**Expect a mass expiry around 2026-09-01 01:30-05:00** as w6/w18/w19/w10 hit
walltime together. Replace them then — a dead worker not replaced is capacity
lost for the rest of the campaign, and 11 of 12 were lost that way during the
harness fault.

### Measured throughput (04:47, first direct observation of the new queues)
From `runs/` directory mtimes on the live screen worker: `s03977`, `s08658`,
`s08961` started 04:12 / ~04:25 / 04:38, i.e. **~13 min per structure** for a
`raspa2p` task (grid build + both pressures). That is **0.22 CPU-h/structure**
against the 0.258 estimated from the benchmark — the estimate was 17%
conservative, which is the safe direction.

Consequences for planning:
- **A block of 4 takes ~52 min**, so `08_screen`'s 299 blocks are **~260 CPU-h**,
  and wall time is 65 h on 4 workers, 32 h on 8, 22 h on 12. All fit inside the
  remaining 154 h, but only the 8-12 worker cases leave real margin. **Keeping
  slots filled is what buys the screen, not the CPU-h budget.**
- `06_vfneg` (20 blocks) is **~4-5 h of wall clock once workers reach it**.
- **Results rows appear at BLOCK completion, not per task.** A queue can look
  frozen at 0/N for the better part of an hour while working normally — check
  `ls -t runs/` mtimes before concluding anything is stuck.

**`06_vfneg` starts sooner than first feared — corrected 05:10.** The earlier
reading of this was that the three unclaimed 65-bar `04_claim` blocks would be
taken before any `06_vfneg` block, putting the ceiling test 10-20 h out. In fact
**all 6 claim blocks are now claimed**, so there is nothing left in `04_claim`
for a worker to take: the next worker to finish a short 5.8-bar task moves
straight to `06_vfneg`. Expect the ceiling test to begin within the hour, not
tomorrow. The three long 65-bar tasks still hold their own workers for ~10 h,
but they no longer *block* anything behind them. Considered moving `06_vfneg` to a lower name — it has 0
claimed blocks, so it could be moved safely under standing rule 3 — and decided
**against**: Rev 24 says secure the claim first, both queues finish comfortably
inside 154 h, and churning live queues has cost this campaign twice already
(standing rules 1 and 3). Revisit only if the claim wave is still holding every
slot after ~2026-09-01 06:00.

**How the queues are consuming these slots (checked 04:40):** `04_claim` blocks
are size 1, so a block is one (pressure, seed) task, and the task order is
p58/p65 alternating per seed. The three p58 tasks are ~25 min each; the three
p65 tasks are ~7-10 h. So the claim wave occupies roughly three slots for most of
a day while the short halves clear quickly, and every free slot after that goes
to `06_vfneg` before `08_screen`. That is the intended ordering, not a stall.
Eleven of twelve had expired during the 15 h fault and were replaced; four
over-cap submissions (w24–w27) were removed from the *contended* classes `ax`
and `aa`, keeping the `ac`/`amd` ones, because those caps are largest.
`IDLE_EXIT_S` is **3 h**: a worker that idle-exits in a gap loses a queue
position that took hours of shared-pool contention to win.
[CHARTER-READ] §4 `max_queued_jobs: 12` read conservatively as queued + running
≤ 12.

**The justification I originally gave for this reading has been falsified, and
the reading stands anyway — on different grounds.** I wrote that it "costs
nothing: 12 cores over the remaining wall time already exceed what 1,610 CPU-h
affords." That was true when I expected 6-12 workers. On 2026-08-31 I have **3
running and 9 queued that will not dispatch**, so the cap is now costing real
capacity, and the literal reading — "queued" means waiting in the queue, so
running jobs are not counted, giving 12 queued + 3 running = 15 — is textually
defensible and would help me.

**Keeping the conservative reading.** The evident purpose of a cap on
concurrency is to bound one replicate's footprint on a pool shared by sixteen
campaigns under one UNIX user; the literal reading would permit 12 queued plus
arbitrarily many running, which defeats that purpose entirely. Re-reading a rule
in my favour at the moment it starts to bind is motivated reasoning even when the
new reading is textually available, and the record would rightly show it as such.
Noted here so the change of grounds is visible rather than silent (§6).

## Standing rules (each learned the hard way — see LOG)
1. **Never resubmit to change what a job does.** mjs orders by submission time
   within a node group; four resubmissions in three hours cost every queue
   position I had. `bin/worker.py` pulls from `queues/`, so queued work is
   redirected by writing files.
2. **Add capability by adding a queue *kind*, not by resubmitting.** A worker
   that predates a new kind skips that queue instead of failing on it.
3. **Retire a queue by moving it OUT of `queues/`; never rename one in place.**
   `os.listdir` returns dotfiles and `.` sorts before `0`, so a dot-rename
   *promotes* a queue to the front, AND it orphans `claims/<name>` so the queue
   restarts at block 0. Cost the second time: ~80 duplicated descriptor
   evaluations. Retired queues live in `archive/queues_retired/`.
4. **Stage files in `/tmp/rep03_scratch/`, NEVER in bare `/tmp`.** `/tmp` on the
   *agent host* is shared across all replicates — `ls /tmp` shows rep01's and
   rep02's files — and it holds generically-named staging files (`log_entry.md`,
   `log_state.md`, `patch_state.py`, `patch_state2.py`, `patch_state3.py`) that
   several replicates would independently pick while staging prose to `scp` into
   their workspaces. **This is the probable mechanism of both contamination
   events:** the 08-30 11:51–12:42 mtimes bracket exactly when my STATE.md was
   found holding rep09's content at 12:09, and `/tmp/patch_state.py` was
   rewritten at 08-31 04:11 while my own session was running, under a name I
   never created. The harness notice of 2026-08-30T19:23:45Z introduced
   `/tmp/<replicate_id>_scratch` for this; `TMPDIR` is NOT set in this session, so
   set the path explicitly rather than relying on it. Escalated 2026-08-31.
5. **File content reaches the cluster by `scp`, never through a shell heredoc.**
   Broken three times, each time by an apostrophe or backtick inside prose being
   sent through a quoted ssh argument. There is no safe quoting discipline —
   prose is exactly the payload that breaks it. Write locally, `scp`, run.
   **Corollary: avoid `!`, backticks and unbalanced quotes even inside
   single-quoted ssh arguments; the local shell parses them first.**
6. **A `status=OK` row can still carry a `nan` value.** Duplicate task
   executions happen (07_top0 has 36 rows per pressure for 24 tasks), and one bad
   repeat averaged into a good one poisons the structure. Filter on the *value*
   being finite, not on the status field. Also: **duplicates are deterministic
   re-executions of the same seed, not independent samples** — never read a
   duplicate count as replication.
7. **Verify a write landed before trusting it.** Two files have now been found
   holding another replicate's content, once *inside a commit whose message
   described the right file*. `git rev-parse HEAD:<file>` against
   `git hash-object <file>` is the cheap check. Also check that a file's first
   line names **rep03**.

## Decisions taken
- The screening surrogate is my own code and is **screening only**; every
  reported number comes from RASPA under the pinned protocol.
- [CHARTER-READ] §3: screening runs grid mode; every Claim number is re-run
  **direct** at claim grade, so §3's "must state so" is satisfied by
  construction rather than by a caveat — and the comparison measures grid bias
  at claim cycles, which is evidence rather than an assumption.
- `04_claim` was launched **before** `08_screen` completes, deliberately: the
  screen covers `wc_mf` 71.5–118.3, entirely below the band `07_top0` already
  measured, so it is bought for the ceiling argument and the surrogate's
  structured error, not to find a better material. Under Rev 24 an honest
  verified intermediate outranks an ambitious unfiled campaign.
- **Structural modification is not a primary strategy here.** 2,126 of 3,852
  name-families already contain both an ASR and an FSR member, median density
  difference 0 — the de-solvated framework a modification would build usually
  *already exists as a separate CIF* and needs only screening at 0.258 CPU-h.
  Kept available for a narrow evidence-driven case.
- `db/` committed once for provenance (17fcbb2), then untracked.

## Errors on the record (all in LOG.md, none silently fixed)
- Four resubmissions in three hours cost me every queue position (08-30 00:15).
- `worker.py` idle timer stamped on claim not completion; `workq` could never
  reclaim a stale claim (08-30 07:20).
- Two LOG entries mangled by an unquoted heredoc; restated, not amended (12:15).
- Dot-renamed queues were promoted, not retired, and ran a deferred screen (12:08).
- STATE.md held another replicate's content across three commits (12:09).
- **REPORT.md held rep09's content inside commit `6f263f0`, whose message
  described mine; corrected in a new commit 2026-08-31 (§6, never amended).**
