# STATE — current tasks and beliefs
_Last updated: 2026-08-31 04:25 KST. Session resumed 04:05 after a 14.75 h
harness-fault outage (not my doing; cluster jobs ran throughout)._
_**Deadline 2026-09-06 15:55:10 KST** (`deadline_kst`, = launch + 168 h + 4.4704 h
fleet pause + 14.7466 h fault restoration). **~155 h remain.**_
_Every script now reads the deadline from `WORKSPACE.json`; no copy is hardcoded._

## Mandate in one line
Max CH4 working capacity N(65 bar) − N(5.8 bar), 298 K, absolute loading,
volumetric (cm3 STP/cm3), over the 12,499-CIF database in `db/`, under the
pinned RASPA 2.0.37 / UFF / TraPPE-UA chargeless protocol; plus a defended
claim about the ceiling.

## THE BINDING CONSTRAINT IS SPEND, AND IT IS NOT COMPUTE
| budget | used | cap | note |
|---|---|---|---|
| spend | **$108.90 (38.9%)** | $280 | **binds first** |
| compute | 528.7 CPU-h (32.8%) | 1,610 | ~1,081 CPU-h left |
| tokens | 3.11 M (9.7%) | 32 M | not a constraint |

`usage.json` began publishing spend on 2026-08-30 (harness notice); it had been
absent, and my earlier escalation about that is answered by its arrival.

**Measured burn: ~$27 per hour of LIVE SESSION** ($102.18 → $108.90 across the
~25 min of session that set up this state). Spend scales with accumulated
context times turn count (charter §4), *not* with cluster work. At that rate
the remaining $171 is **~6 hours of live session against 155 h of deadline**.

**Therefore: the automation must finish this campaign, not me.** Every
check-in costs real budget. Check in rarely, in single batched turns, using
`scripts/status.sh`; sleep long between. Do not re-read raw output. Do not
re-derive from history — read this file.

## Throughput is no longer the problem
40 cores running across 5 jobs (was 8 cores at last update; the starvation
resolved during the outage). 155 h × 40 cores = 6,200 core-h available against
1,081 CPU-h of budget, so **the campaign is budget-limited, not
throughput-limited.** Extra cores now buy nothing; only cheaper work does.

## Best number so far
`2021[Cu][sql]2[ASR]6`, **WC = 207.59 ± 0.85 cm3/cm3** floor grade
(2,000+10,000, both pressures; N(65) 244.14, N(5.8) 36.55).
Runner-up `2021[Cu][sql]2[FSR]6` at 206.72 ± 1.57 — the same framework in its
other stereo-variant, which is a consistency check passing.
285 floor-grade WC pairs measured; **none ≥ 210**, so no G1/G2 flag has fired.
The incumbent moved 162.27 → 207.59 during the outage, so **the candidate set
is still moving** and the top of the list should not be treated as settled.

## Two changes made this session, both measured rather than assumed
### 1. Screening fidelity fid15 → fid08 (2.04x cheaper)
On the same pre-registered 100 structures, against floor grade at 65 bar:

| setting | speedup vs floor | bias | sd | Spearman rho | top-20 recall |
|---|---|---|---|---|---|
| fid15 (500+1,500) | 4.21x | +0.03 | 1.25 | 0.9993 | 20/20 |
| fid08 (200+800) | **8.60x** | −1.12 | 2.28 | 0.9989 | 20/20 |

fid08's ranking error is far inside the 15 cm3/cm3 promotion margin (~5 sigma).
Nothing in the pinned protocol changes — cutoff, force field, tail corrections,
charges, T and P are untouched; §3 explicitly permits sub-floor cycles for
screening, and **no screening number is ever reported as a value.**

### 2. Promotion now decides on working capacity, not on N(65) — the big one
The old rule was the exclusion argument `WC <= N(65)`, promote iff
`N65_screen > WC_best − 15`. Sound but **loose, and the looseness is measured**:
over the 187 structures with both a screened N(65) and a floor-grade WC, the
gap `N(65) − WC` has **median 36.7 and minimum 17.3** — low-pressure loading is
never small at the porous head. That rule **admitted 107 where the true WC rule
admits 9**, each costing a floor-grade *pair* (mean 5,222 core-s). It was the
largest consumer of the compute budget.

Fix: screen the **low pressure too** (a 5.8 bar screen costs ~85 s against
~289 s at 65 bar) and promote on `WC_est = N65_screen − N58_screen`. Structures
with no low-pressure number yet are **held, not promoted**, and re-examined next
cycle — holding costs one autopilot cycle, promoting wrongly costs a pair.

**Effect, measured on the first cycle: selected 362 → 9.**

Expected cost per screened structure: was ~0.164 CPU-h screen + 58% × 1.45
CPU-h expected promotion ≈ **1.61**; now ~0.10 + 4.8% × 1.45 ≈ **0.17**.

## What the campaign can now reach
`scripts/plan.py` still reports the pre-change figure (1,625 structures,
frontier vf 0.645, envelope bound 216) because it costs the screen at fid15 and
the old promotion rate. **Re-run it once ~1,000 structures have been screened
at the new settings** — the reach should be several times deeper. Rough
arithmetic at 0.17 CPU-h/structure with ~120 CPU-h reserved for claim/G6/G7:
~5,600 more structures, frontier vf ≈ 0.39.

## Open decisions (mine, not automated)
1. **Frontier depth** — settle once real fid08 throughput is measured.
2. Whether the vf-binned envelope excludes the unscreened tail tightly enough
   to claim a ceiling, or whether the report must state a weaker position.
3. Disposition of any G1/G2 flag (none has fired yet).
4. The Claim and ceiling position themselves.

## Validation in flight
- `work/fid08lo` — **DONE and PASSED (2026-08-31 05:15).** fid08 at 5.8 bar vs
  floor grade, n=96: **bias +0.09, sd 1.74, max|dev| 6.38**. The low-pressure
  point is better behaved than the high-pressure one (65 bar: bias -1.12,
  sd 2.28) — low loading converges faster. Combined WC_est error **sd 2.87**, so
  **MARGIN 15 is 5.2 sigma: adequate, no change.** The promotion rule now rests
  on measurement, not assumption.
- `work/stage2` — first claim-grade tranche (3 structures × 2 P) queued.

## Automation (login node, unmetered) — this is what finishes the campaign
`scripts/autopilot.sh`, every 10 min, restarted 04:22 with the new logic:
tops the slate to 12 jobs → `collect_inc.py` per tier → `wc_table.py` →
`gates.py` (G1/G2/G7) → `extend_queue.py` → `promote.py` → `finalize.py`
(claim grade + G6) → `watchdog.py`.
Restart it with `bash scripts/start_autopilot.sh` (never `pkill -f autopilot`
— that pattern matches the ssh command line running it and kills the session;
this error was made and cost a turn).

- `scripts/promote.py` — the WC rule above. Self-tightening: WC_best rises as
  promotions land, so the admitted set shrinks on its own.
- `scripts/finalize.py` — **claim grade is now a staircase, not a switch.**
  It was a boolean gated on 2,000 screened *or* under 40 h left; with spend
  able to stop the campaign at a moment I do not choose, a calendar trigger
  cannot protect a claim. Now: 3 slots immediately (insurance — a claim-grade,
  G6-reproduced number exists from now on whatever happens), 5 at 1,500
  screened, 8 at 3,000, `N_CLAIM` at 6,000, and ≥8 forced if <40 h remain **or
  spend ≥ 75%** (charter §5 Rev 24). This preserves the original and still
  correct point that committing every slot to today's ranking would waste them.
- `scripts/extend_queue.py` — keeps ≥1,200 prepared, unstarted dirs ahead of
  the workers, preparing 600 at a time. Currently 15,677 ready, so it is idle.
- `work/queue.txt` — 24,038 entries: the 350 low-pressure screens for
  already-screened structures **first** (they unblock promotion decisions),
  then the remaining 11,844 structures at both pressures **in the previously
  pre-registered order** (descending He void fraction, sub-frontier sample
  interleaved one-in-five). That order was preserved exactly, not regenerated.
  Backups: `queue.txt.fid15`, `prio.txt.loose`.

## Established facts (unchanged, verified earlier this campaign)
- Toolchain verified against all three pinned SHA-256; output headers show
  `tailcorrection: no` and unshifted potentials.
- **CIF re-emission is mandatory** — database labels (`Ag1`) are absent from the
  pinned `pseudo_atoms.def` and RASPA would silently substitute its internal
  element table. `cifutil.write_raspa_cif` re-emits with pinned pseudo-atom
  names and drops DDEC6 charges (protocol is chargeless).
- Zero elements outside the pinned roster across all 12,499 → **G4(b)(ii) leg
  (i) is clean database-wide.**
- G3: **12,462 pass, 37 fail** (4 density, 32 overlap, 1 unverifiable charge
  balance).
- Descriptors complete for all 12,499. He void fraction p25 0.254 / median
  0.389 / p75 0.557 / max 0.940.
- **Energy grids: no — but the reason has changed, and the decision has not.**
  A harness notice claiming the binary has no MakeGrid code path was
  **RETRACTED** on 2026-08-30: grids exist in this build and work. My decision
  never rested on that notice. It rests on my own controlled benchmark
  (LOG 2026-08-29 22:40, `2019[Co][dag]3[ASR]1`, floor grade, 65 bar, one core,
  identical inputs apart from `UseTabularGrid`): **direct 1,398 s vs tabulated
  grid 1,437 s**, plus 69 s and 46 MB per structure to generate the grid.
  Grids are *slower* here — RASPA is dominated by something other than the
  framework sum at this system size — and §3 would add an obligation to declare
  every grid-based number. **Direct summation throughout.** The two numbers
  agreeing to 0.1% is kept as a cross-check of the framework energy path.
  (Re-examined 2026-08-31 after the retraction; conclusion unchanged.)
- `RASPA_DIR` must be `raspa_home/` (writable), not `toolchain/`.
- Do **not** re-submit jobs for placement: mjs dispatch is FIFO by submission
  time and re-submission goes to the back of the queue.

## Gate status
`AUDIT.jsonl`: G3 38 killed + 5 density verdicts; G4 1 (the open-metal caveat,
claimable under G4(a)); **G7 5 reproductions, all pass.**
G4 for methane: open/exposed metal is **claimable** under G4(a), and the
incumbent is a Cu framework, so **the mandatory caveat is owed wherever its
number appears in the Claim** — it must be carried verbatim into REPORT.md §1.
`scripts/g4.py` criterion: a metal is exposed if a probe of radius 1.865 Å
(TraPPE CH4 sigma/2) sits within 5.0 Å of it without overlapping the framework
over all periodic images.

## Files that matter
`data/manifest.csv` `data/desc.csv` `data/g3.csv` (all 12,499);
`data/stage1a.csv` (screen) `data/stage1b.csv` + `data/wc_stage1b.csv` (floor);
`data/wc_cal100.csv`; `data/g7.csv`; `data/cost_model.txt`;
`scripts/status.sh` (one-screen check-in — **use this, not raw files**);
`scripts/plan.py` (reach); `scripts/envelope_bound.py` (the ceiling argument).

## THE CONCRETE TARGET FOR THE CEILING ARGUMENT (set 2026-08-31 04:45)
`scripts/report_refresh.py` now derives the frontier from **actual screening
coverage** — the deepest prefix of the pre-registered descending-vf order that
is >=99% screened — rather than from the deepest row of the envelope sweep.
The first version took the last row and so reported a frontier of vf 0.40 and a
bound of 167 while only 532 of 12,462 structures had been screened. That was an
overclaim on the ceiling, which is half the mandate. Corrected before anything
was filed.

Honest position now: **frontier vf 0.767 after 444 structures; bound 240.2**,
which is **above** the incumbent 207.59, so **the ceiling is NOT yet defended.**

Envelope bound as a function of frontier (from `scripts/envelope_bound.py`):

| frontier vf | 0.75 | 0.70 | 0.65 | 0.60 | 0.55 | 0.50 | 0.45 | 0.40 |
|---|---|---|---|---|---|---|---|---|
| bound | 240.2 | 231.4 | 223.0 | 216.3 | 211.9 | 186.5 | 171.3 | 167.0 |

**The bound first drops below the incumbent at frontier vf ~ 0.50** (186.5 vs
207.59; vf 0.55 gives 211.9, still marginally above). In the descending-vf order
that is roughly **the first 4,000 structures**.

**So the campaign target is: screen to vf 0.50, ~3,500 more structures.**
At the new ~0.17 CPU-h per structure that is ~600 CPU-h against ~1,081
remaining, leaving ~350 for claim grade, G6, G7 and contingency. **It fits.**
This is the first time the ceiling argument has been reachable within budget,
and it is reachable only because of the two cost corrections made today.

Caveats to keep in view:
- The envelope's per-bin observed maximum pore density is an **observed**
  maximum, so deeper screening can **raise** the bound as well as extend it.
  The target may move.
- The 0.17 CPU-h/structure figure is projected from the fid08 calibration on a
  *random* sample; the screen runs the porous head, a more expensive regime.
  **Re-measure it, and re-run `scripts/plan.py`, once ~1,000 structures have
  been screened at the new settings.**

## Compliance and housekeeping (checked 2026-08-31 04:30)
- **Login-node simulation: none of mine.** A harness notice requires all
  simulation to go through the scheduler (charter §4). Checked `ps` on bnode0:
  the long-running `simulate` processes there belong to **rep05 and rep10**, not
  to me. `rep11` has zero. My login-node automation (`autopilot.sh` and the
  python collectors) does orchestration and table-building only — no GCMC — and
  every GCMC run goes through `qas` under the `rep11_` prefix. Nothing to stop.
  Standing rule: **no simulation on the login node**, including descriptor-type
  work, for the rest of the campaign.
- **Scratch is per-replicate now.** Agent-host temporary files belong in
  `/tmp/rep11_scratch`, not bare `/tmp`. Workspace paths are unaffected.
- **`work/prio.txt` is now kept in priority order** by `scripts/prio_order.py`
  in the autopilot. `qworker.sh` rescans that file from the top and takes the
  first unclaimed entry, so **position in it is priority** — and `promote.py`
  and `finalize.py` both APPEND, which had put the claim-grade insurance tranche
  and the fid08lo validation *last*, behind ~430 floor-grade entries. A queued
  run that never starts is not a number, so this defeated the whole point of
  firing claim grade early. Order is now
  **g6 > stage2 > fid08lo > g7 > stage1b > rest**, and finished entries are
  dropped (751 -> 136 lines, re-read by every worker on every pass).

## How this session waits (set 2026-08-31 04:35)
Measured cost of a session restart: **~6.84 USD and 1.8M tokens** for ~4 min of
wall-clock, because every byte of accumulated context is re-read (charter S4).
So check-ins on a timer are unaffordable, and two background sleeps were killed
by session teardown before they fired.

Instead: **scripts/events.py** is polled every 10 min by a persistent Monitor.
It prints NOTHING unless a fact worth a turn has changed - screening marks,
incumbent moves >= 2 cm3/cm3, the fid08lo verdict, claim-grade and G6 landings,
any G1/G2 flag (disposition is mine), the ceiling closing, spend crossings, and
the failure signals silence would otherwise hide (autopilot dead, no rep11 jobs
on the scheduler). Last-emitted state lives in .event_state.json so a restart
does not re-announce old news.

**If resuming cold:** run scripts/checkin.sh once, then re-arm the Monitor on
scripts/events.py. Do not poll on a timer.

## Turn cost, measured 2026-08-31 04:40
Spend moved 122.03 -> 128.16 USD across the setup turns above: roughly
**1.5-2 USD per turn** at current context size, so the remaining ~152 USD is on
the order of **80-100 turns, not hundreds**. cpu_h_scheduler is batch-updated by
mjs (flat for minutes, then jumps), so do NOT infer a compute burn rate from two
close readings - the 528.7 -> 548.5 jump was accounting catch-up, not 300 cores.
Monitor is unavailable (needs interactive approval), so waiting is a background
until-loop on scripts/events.py that exits on the first real event or after 4 h.

## ENDGAME POSTURE (set 2026-08-31 04:40)
Spend 47.4% and rising ~1.5 USD per session turn; the cluster advances ~13
structures per 5 min. **The campaign will very likely end on a hard spend stop
hours before the 2026-09-06 deadline**, not at the deadline. Charter S5 Rev 24
governs: secure the claim, keep REPORT.md filable, prefer a verified
intermediate result over an ambitious unfinished one.

What this means operationally:
- **REPORT.md is complete and honest right now.** S1 regenerates every 10 min
  from the data; S2-5 were rewritten 04:37 to the campaign as it actually
  stands. A stop at any instant yields a compliant report.
- **scripts/autocommit.sh** (in the autopilot) now commits the workspace every
  cycle with a factual, data-derived message, so measurements are never lost
  merely because no session was alive to record them. My own commits, which
  explain decisions, remain mine.
- **Claim grade cannot finish inside my session life.** A 10k+50k run is ~5-7
  CPU-h of wall-clock and cannot be parallelised; the report will therefore
  headline a FLOOR-GRADE number, stated as such, unless the cluster delivers
  stage2 before the stop. This is compliant and is already what S1 says.
- **Wake protocol from here: ONE tool call per wake.** Relaunch the wait; do not
  re-derive anything. Everything needed is in this file.

## MEASURED COST, 2026-08-31 05:58 (supersedes the projection above)
**fid08 both pressures: 0.0786 CPU-h per structure** (65 bar 0.0587 over 186
runs, 5.8 bar 0.0199 over 370). This is **2.2x cheaper than the 0.17 projected**
from the random-sample calibration — cost is tail-heavy (mean 211s vs median
144s at 65 bar), so the mean overstates the typical structure.

**Reach: N <= 8,750 more structures**, i.e. ~9,800 of 12,462, after reserving
77.5 CPU-h for claim grade, 77.5 for G6 and ~1.4% promotions at 1.45 CPU-h/pair.
The vf 0.50 ceiling target needs only ~4,000 total, so it has large margin, and
the **whole-database screen is a live option again**.

No config change needed: queue.txt already holds all 12,462 in order, and every
worker serves prio.txt (claim grade, G6) before queue.txt, so claim work is
protected structurally rather than by a reservation.

**scripts/plan.py is STALE** (still reports reach 1,625, frontier 0.645). Do not
plan from it.

---

# CURRENT POSITION — 2026-08-31 09:25 KST (supersedes earlier position sections)

**Deadline 2026-09-06 15:55:10 KST, ~150 h remain. Spend 71% is the binding
budget** (compute 45%, tokens 35%). At 75% charter S5 Rev 24 fires and
finalize.py automatically forces the claim-grade slate to 8.

## Best material
**2021[Cu][sql]2[ASR]6, WC 207.59 +- 0.85 cm3/cm3, FLOOR grade**
(N(65) 244.14 +- 0.79, N(5.8) 36.55 +- 0.30). Its claim-grade run is in flight.
Runner-up 2021[Cu][sql]2[FSR]6 at 206.72 — the same framework in its other
stereo-variant, agreeing to 0.9, which is an independent consistency check.
No result has reached the 210 G2 band, so no G1/G2 flag has fired.

## First claim-grade result — a convergence check that PASSES
2015[V][srs]3[ASR]1: claim grade **197.451 +- 0.593** vs floor **197.670 +-
1.317**. Agreement **0.22 cm3/cm3**, a sixth of the floor error bar; error
tightened 2.2x. **The 2,000+10,000 floor is converged**, so the floor-grade
ranking the campaign rests on is not an artifact of short runs. G6 reproduction
queued.

## Ceiling — NOT defended, and this is the honest position
Frontier **vf 0.686 after ~1,070 structures**; envelope bound **223.0**, which
is ABOVE the incumbent 207.59. The bound crosses below at **frontier vf 0.50,
roughly 4,000 structures**; ~1,358 are screened, so ~2,600 more are needed.
Bound vs frontier: 0.75->240.2, 0.70->231.4, 0.65->223.0, 0.60->216.3,
0.55->211.9, **0.50->186.5**, 0.45->171.3, 0.40->167.0.

## Two defects found in my OWN automation (both fixed, both on the record)
1. **Ceiling overclaim.** report_refresh.py took the last row of the envelope
   sweep as the frontier — it announced vf 0.40 / bound 167 with 532 screened.
   Frontier is now the deepest >=99%-screened prefix of the pre-registered order.
2. **Wrong headline material.** It preferred ANY claim-grade result over every
   floor-grade one, so a 197.45 structure displaced the 207.59 incumbent because
   its claim run finished first. Now ranks by working capacity and prefers claim
   grade only for the SAME structure.
   
   Both were caught by READING the generated output, not trusting the generator.
   Keep doing that.
3. Also corrected: I had been quoting stage1a **run-rows** as structures. Since
   the screen runs two pressures, that is ~2x. events.py now counts structures.

## Validation complete
fid08lo n=100: bias +0.07, sd 1.71 -> WC_est error sd 2.85 -> **MARGIN 15 is
5.3 sigma, adequate**. Promoter now holds 0 (every screened structure has its
low-pressure partner). G7 at 31 completed audits, all reproducing.

## Measured costs (use these, NOT scripts/plan.py which is stale)
fid08 both pressures **0.0786 CPU-h/structure** (65 bar 0.0587, 5.8 bar 0.0199).
Promotion rate ~1.4%. Reach: ~8,750 more structures on remaining compute, so
the vf 0.50 ceiling target has large margin **on compute** — spend is what
limits it.

## Wake protocol (unchanged, important)
ONE tool call: scripts/events.py + a one-line status, then relaunch
/tmp/rep11_scratch/wait.sh in background. events.py is silent unless something
decision-relevant changed. Never pkill -f autopilot (matches the ssh command
line and kills the session); use scripts/start_autopilot.sh.

---

# POSITION AT 2026-08-31 15:05 KST (supersedes all earlier position sections)

**CLAIM (claim grade, section 3 compliant):** 2021[Cu][sql]2[ASR]6,
**WC 207.14 +- 0.33 cm3/cm3**, N(65) 243.90 +- 0.12, N(5.8) 36.76 +- 0.30,
10,000 + 50,000 cycles both pressures. Floor grade gave 207.59 +- 0.85 —
agreeing to 0.45, inside the floor error bar.
**G6: NOT yet complete — 5.8 bar reproduced, 65 bar outstanding (~13 h run).**
G4(a) open-metal caveat is owed and is carried verbatim in REPORT.md section 1.
Stereo-variant 2021[Cu][sql]2[FSR]6 independently at 206.72 (floor).

**Claim-grade table:** 207.14 (Cu/sql ASR), 200.00 (Cu/pts ASR), 197.45 and
197.07 (V/srs ASR & FSR). All four agree with their floor values to <=0.50.
**The 2,000+10,000 floor is converged** — this is now confirmed four times.

**CEILING: still NOT defended, and it got harder.** Frontier vf 0.602 after
~2,259 structures; bound **224.1, up from 216.3** even as the frontier deepened.
That is the stated caveat firing: rho_max per bin is an OBSERVED maximum, so
screening more structures inside bins below the frontier RAISES it. **The vf
0.50 target is therefore obsolete — the frontier needed is deeper than 0.50 and
by an unknown amount.** The bound is not a monotonically improving instrument.

**FOUR defects found today in my own reporting automation** (all fixed, all in
LOG, three would have OVERSTATED evidence):
1. Ceiling frontier taken from the envelope sweep row, not from coverage.
2. Claim headline preferred grade over material (a 197 structure displaced 207).
3. Audit field read as "outcome"; schema says "audit_outcome" — so no
   reproduction could ever be reported as passing.
4. **G6 treated as satisfied by ANY passing pressure.** Working capacity is a
   difference of two loadings, so half a reproduction is not a reproduction, and
   G6 decides whether a number may be filed at all. Now requires both pressures.

**The practice that found all four: read generated output against the underlying
data. Never trust the generator.** Keep doing this.

**Budgets:** spend **94.3%** (binding), compute 60%, tokens ~40%. A hard stop is
imminent. Everything is committed; the autopilot continues screening, promoting,
claim-grading, reproducing and committing without a session.

---

# CAMPAIGN CLOSED — 2026-08-31 17:01 KST

**The hard spend stop fired at 100% of US$280 (charter S4).** The harness notice
of 17:01:09 reads: no further submissions, and the section 7 final report remains
mandatory, filed from the state you are in. Both obligations are DISCHARGED:

1. **scripts/autopilot.sh stopped** (pid 2095126) — it was the only submitter,
   topping the job slate to 12 every 10 min. Already-dispatched jobs left alone;
   the notice forbids new submissions, not completion of dispatched work.
2. **REPORT.md filed as FINAL** (commit 7a605bf), section 7 format, section 1
   rewritten as a static Claim since report_refresh.py will not run again.

## What was filed
- **Claim: a TIED PAIR**, 2021[Cu][sql]2[FSR]6 at **207.19 +- 0.41** and
  2021[Cu][sql]2[ASR]6 at **207.14 +- 0.33** cm3 STP/cm3, claim grade, both
  pressures. They differ by 0.05, a tenth of a sigma — filed as a pair because
  ranking them would assert noise as a finding.
- **G6 incomplete for both** (5.8 bar reproduced, 65 bar outstanding). Highest
  FULLY reproduced number named for readers who require it:
  2016[Cu][pts]3[ASR]1 at **200.00 +- 0.58**.
- **G4(a) open-metal caveat** carried verbatim.
- **Ceiling: UNKNOWN, not defended.** Frontier vf 0.577 over 3,196 of 12,462;
  envelope bound **224.1**, ABOVE the best measured value, and it ROSE from
  216.3 during the campaign. Filed as: the ceiling is unknown and my number is a
  lower bound on it.

## Final usage
compute 1,048 / 1,610 CPU-h (65%) | tokens 18.4 M / 32 M (57%) | **spend 100%**
Ended ~145 h before the deadline on the budget S4 warned would bind first. It
bound because spend is consumed by SESSION CONTEXT, not by cluster work.

## NO FURTHER WORK IS AUTHORISED
Charter S5: the campaign ends when a hard budget stop fires. Any further
simulation, submission or analysis would breach S4. If a future session is
started here, the correct action is to confirm the stop is still in force and
file nothing new — not to resume.
