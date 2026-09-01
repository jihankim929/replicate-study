# LOG — append-only narrative

## 2026-08-29 (T+0h) — Setup, toolchain verification, database characterisation

**Toolchain verified.** `sha256sum` on the three files in `toolchain/raspa/share/raspa/forcefield/UFF/`
reproduces the §3 table exactly. `libraspa2.so` reports `RASPA 2.0.37`. A 300-cycle probe run
confirms from the output header: 4,186 interaction pairs all `tailcorrection: no`, and
`All potentials are unshifted !!!!!!`. Framework density reported by RASPA (2228.36 kg/m³ for
`0000[Ag][nan]3[ASR]1`) agrees with my own parser (2.2285 g/cm³), so the CIF→RASPA path is faithful.

**Atom labelling — the silent-failure path §3/G4 warns about.** The database CIFs label atoms
`Ag1`, `Ag2`, … . RASPA matches `_atom_site_label` against `pseudo_atoms.def` and, per the G4(b)(ii)
note, substitutes its own element table for labels it cannot find rather than erroring. Every CIF
is therefore rewritten (`scripts/cifutil.py`) with `_atom_site_label` set to the exact pinned
pseudo-atom name (`Ag_`, `C_`, …). Verified on the probe run: 92 pseudo atoms loaded, all framework
atoms mapped, no substitution.

**Stage-1 scan of all 12,499 structures** (`tables/scan1.csv`, `scripts/scan1.py`): cell, atom count,
supercell replication at 12.8 Å, density, minimum interatomic distance including images, element roster.
Findings:
- **No structure contains an element absent from the pinned `pseudo_atoms.def`.** G4(b)(ii)(i) —
  the mechanically checkable leg — cannot fire anywhere in this database. Recorded once here rather
  than per structure.
- Density spans 0.164 – 3.963 g/cm³ (median 1.255). **Four structures fall below the G3 lower bound
  of 0.20 g/cm³**; none exceeds 4.50. Note: the charter's note on G3 states "the least dense entry in
  this database is 0.313 g/cm³". My parser gives 0.164 for `0000[Cu][tbo]3[ASR]1`. The discrepancy is
  logged and investigated before any of these four is used; it does not affect the gate, which is
  applied as written.
- Two structures have a minimum interatomic distance below 0.5 Å (G3 overlap kill); 76 structures
  above 1,200 atoms were skipped by the O(N²) overlap check and are checked individually if selected.

**Redundancy.** 12,499 files collapse to **9,111 distinct structures** under a coordinate-and-cell hash
(`tables/dupgroups.csv`). The database carries ASR/FSR pairs of the same material. Screening runs on
group representatives; duplicates inherit their representative's number and are never simulated twice.

**Cost calibration.** A 700-cycle GCMC at 65 bar on `2012[Cu][tbo]3[ASR]1` (2,656 framework atoms in
the 2×2×2 supercell, 144 cm³/cm³) took 5 m 18 s of one core → ≈1.5 CPU-h per pressure at the §3 floor
of 2,000+10,000 cycles, ≈3.0 CPU-h for the two-pressure pair. The charter's quoted 1.83 CPU-h is a
database average; large porous cells cost about double that, which is exactly where the candidates are.

**Energy grids.** §3 permits grids for screening. `SimulationType MakeGrid` in this build returns
success and writes no grid file, under every input ordering tried and with `$RASPA_DIR` pointed at a
writable shadow tree whose forcefield/molecule files are symlinks to the pinned originals (hashes
re-verified through the shadow). Screening therefore proceeds at full explicit-framework cost unless
`UseCellLists` proves to help. Recorded as an infrastructure observation, not a blocker: the charter's
own G7 note sizes the campaign at "~600 passers", which the budget supports without grids.

### Charter interpretations

[CHARTER-READ] §4 / workspace boundary: §4 forbids reading or writing outside the workspace, but the
mandated submission tool `qas` is not on `PATH` and is not in the workspace → I read `/usr/local/mjs/`
and the scheduler's own documentation under `/home/molsim_share/` to learn how to submit at all, and
treat that as operating the provided infrastructure rather than working outside my workspace. I did
not read the RASPA source tree that exists under the supervisor's home, though it would have answered
the MakeGrid question, because that is scientific tooling rather than submission mechanics. All data,
inputs, outputs and records live in the workspace.

[CHARTER-READ] Appendix A G3 / He void fraction: G3 requires a He void fraction for every structure
entering GCMC, but the pinned `pseudo_atoms.def` contains **no helium**, so it cannot be computed
inside the §3 protocol without editing a hash-pinned file → I compute it outside RASPA
(`scripts/scan2.py`, He ε=10.9 K σ=2.64 Å, Lorentz-Berthelot against the pinned UFF table, 12.8 Å,
unshifted, no tail correction) and record it as a pre-simulation descriptor. §2 already establishes
that no reported number depends on the void fraction, since it reports absolute rather than excess
loading for precisely this reason.

[CHARTER-READ] §3 / cycle floor: "Floor for any reported number" → I read *any reported number* as
including the landscape values the report will show, not only the Claim. Every GCMC in this campaign
therefore runs at ≥ 2,000+10,000; nothing is run at a lower fidelity merely to rank.

## 2026-08-29 (T+1h) — Descriptors, G3 pre-screen, cost model surprise

**Descriptors complete** for all 12,499 structures (`tables/scan2.csv`, job 3473240, ~15 CPU-h):
He void fraction, CH4-accessible volume fraction, Henry integral, Boltzmann-average CH4 energy,
deepest sampled site, free-sphere proxy, saturation proxy and a two-parameter Langmuir
working-capacity proxy. Zero failures.

**G3 pre-screen** over the whole database. Six kills, all logged to `AUDIT.jsonl`:
- overlapping atoms: `2007[Ag][nan]3[ION]1` (0.184 Å) and `2008[Bi][dia]3[ION]1` (0.094 Å). These
  are not unusual structures, they are broken ones — a 0.09 Å contact is not a bond — and they are
  not simulated.
- density below 0.20 g/cm³: `0000[Cu][tbo]3[ASR]1` (0.164), `2010[Cu][wbl]3[ASR]3` (0.170),
  `2020[Fe][hcb]2[ASR]2` and `[FSR]2` (0.175).

**Charge balance (G3, third leg).** Every one of the 12,499 CIFs carries a PACMAN/DDEC6
`_atom_site_charge` column that sums to zero to five decimals — for all 12,499. That is a property
of how the charges were generated, not evidence about the structures: the column is normalised to
neutrality by construction and therefore **cannot detect a missing counter-ion**. Recorded here so
that the G3 charge-balance leg is not mistaken for having been tested by it.

**Cost model — the measurement that resizes the campaign.** On `2012[Cu][tbo]3[ASR]1`
(2,656 framework atoms, 599 CH4 at 65 bar) one core takes 5 m 19 s for **zero** cycles,
5 m 24 s for 50, and 5 m 18 s for 700. The MC cycles are nearly free; essentially the whole cost is
fixed per-run setup. This inverts the planning assumption: the §3 floor of 2,000+10,000 and the
Claim grade of 10,000+50,000 cost almost the same, and the number of *structures* — not the number
of cycles — is what the compute budget buys. A 47-structure pilot at floor cycles is running to
measure the real distribution of per-structure cost before the main screen is sized.

### Charter interpretations

[CHARTER-READ] Appendix A / G3 kill vs. the Rev-19 note: G3 says failures are "killed and logged",
while the Rev-19 note says "No gate in this appendix forbids a simulation or suppresses a measured
value" → I kill for *claim* purposes in both cases, and additionally **simulate the four
density-out-of-bounds structures anyway** and report them in the landscape, since they cost about
1 CPU-h and the note's whole point is that removing data removes the evidence for the gate's own
correctness. The two overlapping structures are not simulated: a 0.09 Å contact makes the GCMC
number meaningless rather than merely excluded, which is the case G3's own note describes as
"cannot be real".

[CHARTER-READ] Appendix A / G3 charge balance for unmodified entries: the leg reads "all charged
framework components retain their counter-ions/pillars", which is a test about what has been
*removed* from a structure → for unmodified database entries I verify it as "the entry is used
exactly as deposited, nothing removed by me", and record that the deposited charge column cannot
support a stronger claim. The leg acquires real force only under G5, on structures I modify.

## 2026-08-29 (T+3h) — Pilot measured, screening model built, main screen launched

**Pilot (job 3473259, 47 structures, §3 floor cycles, both pressures).** Working capacities span
0.8 – 182.6 cm³/cm³. Best in the pilot: `2012[Cu][nbo]3[ASR]1` at **182.6** (N(65)=232.7,
N(5.8)=50.1, ρ=0.522 g/cm³). Protocol compliance is verified per run from the output headers:
zero `tailcorrection: yes` pairs anywhere, `All potentials are unshifted` in both pressures of
every run. Cost: 579 s to 4,270 s per structure for the two-pressure pair; median ≈ 2,775 s.

**Cycle-grade check, and a correction to the T+1h entry.** The earlier "cycles are nearly free"
reading came from one structure and does not generalise. On `2007[Cu][tbo]3[ASR]1`:
floor grade (2,000+10,000, seed 1001) gives **147.82** in 579 s; Claim grade (10,000+50,000,
seed 2001, job 3473272) gives **148.69 ± 1.14** in 2,137 s. Claim grade costs ≈3.7× floor, and
the two agree to 0.9 cm³/cm³ — within the Claim-grade error bar. Floor-grade screening is
therefore an unbiased ranker, and promoting a finalist changes the number by less than its own
uncertainty. Budget planning uses 3.7× for Claim-grade runs, not 1×.

**Screening model.** Descriptor→working-capacity ridge fit on the pilot. Descriptor Spearman
correlations against measured WC: void fraction +0.90, CH4-accessible fraction +0.90, Langmuir
proxy +0.91, free-sphere diameter +0.82, density −0.82.

*A model failure worth recording.* The first fit used a rich polynomial basis including
log₁₀(Henry integral) and reached LOO-RMSE 18.7 — and then ranked six **zero-porosity** frameworks
(φ = 0.0000, void fraction 0.03–0.15) at the top of the database, all at the 260 cm³/cm³ clip.
log(k_H) diverges to −∞ on a non-porous structure, and a linear coefficient on a divergent feature
ranks the divergence rather than the material. The basis is now restricted to bounded terms
(void fraction, accessible fraction, free-sphere diameter, density, Langmuir proxy, saturation
proxy, φ·Ū), structures with φ < 0.02 are excluded from the candidate pool as unable to deliver
at all, and the fit's LOO-RMSE improved to **14.5 cm³/cm³**. Had this not been caught, round 1
would have spent ~500 CPU-h measuring non-porous solids.

**Round 1 launched** (jobs `rep01_r1a`/`r1b`/`r1c`, 540 structures): 480 by model rank plus 60
stratified across void fraction among structures with φ > 0.05, so that a model error cannot
silently remove a whole region from consideration. All at §3 floor cycles, both pressures.

**Budget ledger** (`scripts/budget.py`, charging cores × wall-clock, not busy time): 92 core-h of
1,610 used at this point (5.7%).

**Scheduler note (T+3.5h).** `rep01_r1b` was submitted as `nodes=1:ppn=32:aa` and vanished: `aa`
nodes are 12–16 cores each, so a 32-core single-node request on that property can never be
satisfied. `qas` accepted it and PBS dropped it with no output file — a silent failure, not an
error. Resubmitted as two 16-core jobs (`r1b0`, `r1b1`). Node sizes on this cluster: `amd` 32,
`aa` 12–16, `ax` 64, `ac` 40–44. Also noted: `qas` is a shared FIFO across all cluster users, so a
job can sit behind several hundred other people's jobs; `r1c` is queued behind ~176 of them.

**Inbox note.** All three escalations were logged and queued. The acknowledgements carry the old
§8 language ("will be repaired", "answered from this document") that the sealed charter's §8
explicitly says was removed because it was not kept. I am treating the sealed §8 as governing —
no answer is assumed, and each question already has a `[CHARTER-READ]` on the record.

**Straggler waste (T+4h).** The pilot job held 32 cores for its last 8 structures for over an hour —
24 cores idle inside an allocation that a CPU-hour budget charges in full. Killed job 3473259 at
39/47 and appended the 8 unfinished structures to the queued `r1c` list, where they run packed
against 180 others. Trade: ~16 core-h of partial work discarded to stop a leak of ~24 core-h per
hour. The lesson is in the job shape, not the structures: batches must be long relative to their
slowest member, and the slowest member is set by supercell size (`nsuper` spans 400–23,166 in this
database). Screening batches are now sized so that no single structure can hold a whole node.

## 2026-08-29 (T+7h) — The surrogate, not the sample, was the limit

Refitting the ridge surrogate on 199 measured structures instead of 28 moved its
leave-one-out error from 14.5 to 14.3 cm³/cm³. That is a model ceiling, not a data ceiling, so
before spending more compute on screening I compared model classes by 8-fold CV on the identical
descriptors (`scripts/model.py`, n=205):

| model | CV-RMSE (cm³/cm³) |
|---|---|
| gradient-boosted stumps, 200×0.08 | **10.56** |
| k-NN, k=5 | 12.92 |
| ridge | 14.86 |

The boosted-tree surrogate is 29% better and has a property the ridge fit conspicuously lacked:
a tree ensemble cannot predict outside the range of measured values, so it cannot rank an
extrapolation artifact first. Ranking switched to it (`scripts/pick2.py`).

**Calibrating the ceiling claim, properly.** The interesting quantity is not the RMSE but the
upper tail of the out-of-fold residual y − ŷ, because a structure the surrogate *under*-rates is
exactly the one that could beat the leader unmeasured. On 205 structures: residual sd 10.2,
95th percentile +14.7, 99th +26.2, and **maximum +43.9** (`2008[Cd][ths]3[ASR]1`). A 3σ rule
would have set the screening threshold at best−31 and would not have covered that structure.
The round-2 rule is therefore **best − (empirical maximum under-prediction)**, not best − 3σ, and
the maximum is re-measured as the sample grows.

**Leader at this point:** `2021[Cu][sql]2[ASR]6`, **207.45 ± 0.83 cm³/cm³** at floor grade
(N(65)=244.17, N(5.8)=36.72, ρ=0.358 g/cm³). Below the G2 band; no gate action due yet. Its own
out-of-fold prediction was 191.8, i.e. the surrogate under-rated the eventual leader by 15.7 —
which is the argument for screening by threshold rather than by rank.

## 2026-08-29 (T+7.5h) — Round 1 re-scoped to what the ceiling claim needs

Round 1 was measuring at ~2.4 CPU-h per structure, and finishing all 540 would have reached
~1,270 core-h — 79% of budget — with 163 of the remaining 343 structures predicted below
best−45 cm³/cm³ and therefore unable to change either half of the mandate.

Rather than kill jobs mid-run and lose the in-flight work, `run_gcmc.sh` gained a **drain guard**:
a task that has not yet started exits immediately when `jobs/STOP_<tag>` exists, so a batch
re-scopes without discarding runs already going. `STOP_r1` was set at 197/540.

**Round 2 (262 structures)** is now the set the claim actually rests on:
- **195 ceiling-critical** — every unmeasured eligible structure the boosted-tree surrogate puts
  above best − 4.3σ (= 207.45 − 45 = 159.7 cm³/cm³), where 4.3σ is the empirical maximum
  under-prediction, not a nominal confidence level. 180 of these were already inside round 1's
  queue; 15 were not, and would have been missed by taking the top of a ranking.
- **60 stratified** across void fraction — the guard against the surrogate being wrong in a region
  it has not seen. These are kept precisely because they are *not* ceiling-critical: dropping them
  would make the coverage argument circular.
- **8 pilot leftovers** discarded when job 3473259 was killed.

The claim-grade cost calibration job was also stopped after its first structure: it had spent
6 h on a second one whose only purpose was a timing point I already had.

**Cost model (T+8.5h).** Regressing 236 completed two-pressure runs:
`log₁₀ secs = −4.195 + 1.384·log(n_super) + 0.434·log(n_CH4@65bar)`, residual factor 1.28.
Median 2,623 s, 90th percentile 6,490 s, maximum 12,758 s. The cost is dominated by the number of
framework atoms in the supercell, and the most porous structures — exactly the ceiling-critical
ones — sit in the expensive tail: several single 65-bar runs have taken over 3 CPU-hours.

Two numbers that matter and differ by 2.5×: the **work** in those 236 runs is 212 core-h, while the
**allocation** charged to the budget is 542 core-h. The gap is cores held while a batch's slowest
members finish, plus work in flight that has not yet produced a row. Batches from here are packed
so that every core has queued tasks behind it, and the ledger charges allocation, not work, so the
gap is visible rather than assumed away.

## 2026-08-29 (T+9h) — Error found in my own work, and corrected on the record

Between 21:08 and 23:30 the screening produced **no** result rows while ~96 tasks ran at 100% CPU
and the ledger charged ~250 core-h. The cause was mine: I edited `scripts/run_gcmc.sh` (adding the
drain guard) **while ~96 tasks were executing that file**. Bash reads a script incrementally from a
byte offset; inserting three lines near the top shifted every later offset, so each running task
resumed at the wrong place and lost the tail of its own script — the extraction call — after its
simulations had already finished.

**Nothing was recomputed.** The RASPA outputs were complete and on disk; only the extraction step
was lost. `scripts/recover.py` re-ran `extract.py` against the archived outputs of every affected
run and recovered **61 result rows**, taking the screening total from 197 to 258. A second defect
surfaced in the recovery itself: the run directory names are `tr -c`-sanitised structure ids and
`echo` had appended a newline that became a trailing `_`, so the recovered rows initially carried
sanitised ids that would not join to the descriptor tables. Corrected in place; 61 ids rewritten.

The lesson is recorded rather than the fix alone: `run_gcmc2.sh` — created earlier for exactly this
reason, to add cross-batch de-duplication without touching the file in use — is now the only script
that changes, and no script is edited while tasks execute it.

Aggregate at this point: **298 result rows, 297 distinct structures screened, 0 protocol
violations** (every run's header re-checked for `tailcorrection: no` and unshifted potentials),
**7 G7 audits due**.

## 2026-08-30 (T+16.5h) — Queue contention, and a cost cap stated rather than hidden

**Six and a half hours with zero jobs running.** After the round-1 cut, every one of my jobs sat in
the `qas` FIFO. The account I run under (`Bei`) is shared with the other replicates of this study,
and its per-property caps were saturated by them: `aa` 38/38, `amd` 77/80, `ac` 102/102, while the
cluster as a whole had 83 free `amd` cores. The constraint is the account quota, not the machine.

Response: stop asking for large contiguous allocations. The two 32-core round-2 jobs were withdrawn
and resubmitted as **six 8-core jobs**, which fit into fragments as sibling jobs finish. Job size is
now a scheduling variable, not just a throughput one.

**A cost cap, and what it excludes.** Two structures in the round-2 list dominate its predicted
cost: `2023[Eu][nan]3[FSR]2` at **126 CPU-h** (23,166 framework atoms in the 12.8 Å supercell) and
`2018[Dy][nan]3[ASR]1` at **34 CPU-h**. Between them they are 160 of the batch's 345 predicted
core-h. Both are from the stratified guard set, not the ceiling-critical set: the surrogate puts
them at ~101–103 cm³/cm³, some 60 below the 164.8 screening threshold and 105 below the leader.
They are excluded on cost. The remaining 101 structures cost 185 core-h — the batch got 3.5× cheaper
by dropping 2% of it.

This is stated here, in `AUDIT.jsonl` and in the report because a silent cap reads as coverage that
was never achieved. **Correction on the record:** I first filed the two exclusions in `AUDIT.jsonl`
under gate G7. That was wrong — declining to simulate on predicted cost is a resource decision and
no gate in Appendix A authorises it — and two `audit_outcome: correction` lines now supersede them.
The exclusion stands; its classification as a gate event does not.

## 2026-08-30 (T+21.6h) — Resume after the fleet pause: nothing was running, and the job counter that should have said so read zero by construction

The harness paused every replicate for 4.4704 h (workspace was down, cluster jobs untouched) and
extended the deadline by the same amount. **T is now 2026-09-05T18:40:46+09:00**, from
`deadline_kst`; STATE.md still carried the pre-pause 14:12:32 and is corrected. No result landed
during the pause, because nothing was running.

**The real finding is why I could not see that.** `qas` and PBS are two queues, not one. A job
accepted by `qas` enters the **mjs FIFO** and is invisible to `qstat` until mjs dispatches it into
PBS. `scripts/monitor.sh` counted my jobs with `qstat -u Bei | grep -c rep01_`, and `qstat -u Bei`
returns **nothing at all** on this cluster — so `jobs=0` was printed on every line of
`tables/monitor.log` for the whole campaign whether I held twelve jobs or none. A counter that
cannot report a non-zero value is worse than no counter: it reads as evidence.

The authorities, established here and used from now on:

| question | command |
|---|---|
| what am I *running*? | `myqstat \| grep rep01_` |
| what am I *waiting with*? | `qinfo \| grep rep01_` — the mjs FIFO, ordered by mjs id within each node property |
| what is free? | `quse` — per-**user** caps per property, and `Bei` is one pool shared by all sixteen replicates |

`scripts/monitor2.sh` replaces `monitor.sh` and reports running and waiting separately. It is a new
file rather than an edit, for the byte-offset reason logged at T+9h: the old monitor was executing.

**Consequence of looking properly: I was never idle-by-mistake, and I nearly made it worse.**
`qinfo` shows ten rep01 jobs already in the FIFO — `r2s0`–`r2s5` (mjs 3411–3416, submitted 06:44
before the pause), `r2c`/`r2d` (3339/3340) and `cg7` (3389) on `aa`, and `scan3` (3161) on `amd`.
The T+16.5h entry says r2c/r2d were withdrawn: they were not — the replacement jobs were
submitted, the originals were never removed, and both sets sat waiting. Believing `qstat`'s
silence I resubmitted all six r2s jobs; the duplicates (3444–3449) were spotted in `qinfo` and
`qrm`'d within the minute. Nothing ran twice.

The two sets are **disjoint, not duplicates**, which is why r2c/r2d are kept: r2s covers 101
round-2 structures (97 unmeasured) and r202/r203 covers the other 62 (60 unmeasured), zero
overlap. Neither contains the two cost-excluded structures. Round 2 outstanding: **157 structures**.

**Queue position is now the scarce resource, not compute.** Scheduler-metered use is 554 CPU-h of
1,610 (34%; my own allocation ledger says 739.5, and the ruling of 2026-08-30 makes `usage.json`'s
`cpu_h_scheduler` the basis for the cap — both are recorded, the smaller one governs). The `Bei`
account sits at `aa` 38/38, `amd` 78/80, `ac` 102/102 with sixteen replicates drawing on it, so
what limits me is where I stand in four FIFOs, and §4 caps me at **12 queued jobs**.

I spent the two free slots on the **critical path, hedged across properties**. `cg7` (12-way, `aa`,
mjs 3389) carries the five claim-grade finalists and seven G7 audits, and it is behind ~118 `aa`
cores of other replicates' work; if it does not dispatch, the campaign has no Claim-grade number at
all and no compliant Claim. So `cgz1` (3-way, `ax`) and `cgz2` (3-way, `ac`) run the same five
finalists at claim grade under **distinct tags and distinct seeds** — `claimb`/5011 and
`claimc`/5021 — with the leader in both. Distinct tags because same-tag concurrency would put two
jobs in one run directory; distinct seeds because if all three land, the leader has three
independent claim-grade measurements and the spread is evidence for §7.4 rather than a duplicate.
Cost if every task runs: ~54 core-h, against ~1,050 remaining. Small jobs (3 cores) are also the
ones that fit the fragments a saturated account leaves behind.

### Charter interpretations

[CHARTER-READ] §4 / 12 queued jobs: the cap could mean twelve PBS jobs or twelve submissions
outstanding → I count **everything `qinfo` shows me holding**, dispatched or not, because a job
waiting in the mjs FIFO is holding a place in a shared queue exactly as a PBS-queued one does, and
the stricter reading is the one that cannot overdraw a resource the other fifteen replicates share.
I hold twelve and submit nothing further until one clears.

## 2026-08-30 (T+22h) — The ceiling argument, counted; and a 15-structure hole in round 2 closed without a new job

With nothing dispatched there is analysis to do, so I costed the mandate's second half against the
tables rather than waiting on the queue.

**Where the ceiling sits, on present evidence.** Of 12,499 files, **7,766 are eligible** —
deduplicated to group representatives (9,111 distinct), G3-passing, and φ ≥ 0.02. 302 of them are
measured. Ranking the other 7,464 with the boosted-tree surrogate:

| unmeasured structures predicted above | count |
|---|---|
| best − 43.9 (= 163.6; 43.9 is the **empirical maximum out-of-fold under-prediction**, not 4.3 sd) | **107** |
| best − 20 | 2 |
| best (207.45) | **0** |

The highest prediction anywhere in the unmeasured set is **189.4** (`2013[Tb][soc]3[ASR]1`), 18
below the leader. And the measured top is tightly packed — 207.5, 199.9, 197.6, 196.3, 195.8,
195.6 — against a median of 162.0 and a 90th percentile of 185.4. A leader that clears the field
by 7.6 while the next five sit inside 4 of each other is the saturation signature, not a
runaway. **Nothing measured has entered the G2 band (210–230) or the G1 band (>230); zero gate
events on value so far, and zero protocol violations across all 309 rows.**

That makes the ceiling claim a finite piece of work rather than a rhetorical one: measure the 107,
and no unmeasured structure in the database is predicted to beat the leader **even at the
surrogate's worst observed error**.

**The hole.** Checking the 107 against what is actually queued: 92 are in the round-2 lists and
**15 are not.** The lists were built before the last surrogate refit and the critical set moved
under them — precisely the failure the threshold rule exists to prevent, reappearing as a
bookkeeping gap. All 15 are small cells (nsuper 1,120–4,800), so ~0.7 CPU-h each, ~11 CPU-h total.

I am at the §4 cap of 12 queued jobs, so a new job was not available. Instead the 15 were
**prepended to the eight waiting round-2 lists**, two apiece — legal and safe because `xargs -a`
opens its list at dispatch, so a list belonging to a job that has not yet started can be re-scoped
without touching the job or losing its FIFO position. Prepended rather than appended: they are
ceiling-critical and cheap, so they run in the first wave, and breaking LPT order by fifteen short
tasks costs almost nothing. Round 2 now covers **all 107** plus the stratified guard, 172
unmeasured structures in total.

**A correction to my own cost model.** The formula STATE.md carries,
`log secs = −4.195 + 1.384 log n_super + 0.434 log n_CH4`, does not reproduce measured times in
any consistent base — read as log10 it predicts 0.02 CPU-h for a structure like the ones that
actually take ~0.7, and read as natural log it overshoots by an order of magnitude. The
transcription of the base is wrong somewhere between `fit.py` and the note. It is not worth
chasing now and nothing has been decided on it: the two cost exclusions at T+16.5h rest on
n_super = 23,166 and 12,000-odd against a database median near 2,000, which is a ratio argument
that survives the base error. Until it is refit, **n_super is the ordering key and the formula is
not used for absolute cost.** Flagged here so no later decision leans on it unknowingly.

## 2026-08-30 (T+22.3h) — Another replicate's report arrived in my session through a shared /tmp, and is not used

**What happened.** I stage files locally and `scp` them to the workspace, because writing a
heredoc over `ssh` mangles any content containing backticks — the outer double-quoted string is
expanded by the local shell first, and it cost me one botched `REPORT.md` write earlier today
(caught immediately, restored with `git checkout`, no commit polluted). The staging path I used
was `/tmp/REPORT.md`.

All sixteen replicates of this study run on the host as the same UNIX user, and `/tmp` is shared
between them. A sibling replicate wrote its own `REPORT.md` to the same obvious path, and the
harness surfaced the change to me as a diff — so **the full interim report of replicate rep09
entered my session context**: its provisional number and structure id, its screening strategy, a
proxy screen it abandoned, its exclusion-margin argument, and a chemical-family analysis it
offers as ceiling evidence.

**What I did about it, and why.**

1. **None of it is used.** Not the strategy, not the numbers, not the family analysis — and
   particularly not the family analysis, which is the piece most directly relevant to the half of
   my mandate I am least confident about. §2 requires that claims rest on simulations I ran and
   validated in this campaign, and §4 confines me to my own workspace. A second replicate's
   conclusions are neither. Beyond compliance: sixteen replicates are presumably run to see what
   independent campaigns conclude, and a replicate that quietly absorbs a sibling's reasoning
   destroys the thing being measured while leaving no trace in its own record. Hence this entry —
   the record has to show the exposure, or the independence of everything after it is unverifiable.
2. **My workspace is clean, verified rather than assumed.** `REPORT.md` on the cluster is 230
   lines and mine, `git status` is empty, and a grep for rep09's identifiers returns zero. The
   only file that actually collided was `REPORT.md`; `scripts/mkg6.py` md5-matches my local copy,
   so the cluster copy is mine.
3. **Staging moved to `/tmp/rep01_stage/`.** Generic filenames in a shared `/tmp` are the whole
   mechanism. Nothing is staged at a bare `/tmp/<generic>.md` path again.
4. **Escalated as `infra`**, because the exposure is not specific to me: any replicate staging at
   an obvious path is both a victim and a source, and unlike a scheduler quota this one is silent
   in both directions. It is Bei's to know about, not mine to fix for the fleet.

**No scientific decision in this campaign changed as a result of this entry.** The plan in
STATE.md is the one committed at fb4f39b, before the exposure.

### Charter interpretations

[CHARTER-READ] §4 / workspace boundary, receiving rather than reading: §4 forbids reading outside
my workspace, and says nothing about material that arrives unbidden — I did not read another
workspace, the harness handed me a diff of a file at a path I had written to → I treat the
boundary as governing **use**, not merely access, since a rule that only forbade the act of
looking would be satisfied by a replicate that used everything it was accidentally shown. So the
content is recorded as received, quarantined from every downstream decision, and disclosed here
and in the report's limitations rather than left silent.

## 2026-08-30 (T+22.5h) — The threshold rule was being set by a structure that could never hold the record

With the queue stalled there was no measurement to do, so I refit the surrogate on all 308
measured structures instead of the 205 it was last fitted on (`scripts/refit.py`). The refit
improved the model — 8-fold CV-RMSE **10.56 → 9.81** for gbm(200, 0.08), with gbm(500, 0.05)
marginally better at 9.58 — and made the screening rule worse.

**The problem.** My round-2 rule is *threshold = best − (empirical maximum out-of-fold
under-prediction)*. That maximum moved **43.9 → 64.5** on the larger sample. The threshold
therefore fell to 143.0 and the number of unmeasured structures above it went from 107 to
**533** — more than round 2 can measure. Worse, this is a property of the rule and not of the
data: a running maximum can only grow, so every additional measurement widens the threshold and
demands more measurement. A stopping rule that recedes as you approach it is not a stopping rule.

**The diagnosis** (`scripts/tail.py`). The tail is not heavy; it is one point.

| | residual |
|---|---|
| maximum | **64.5** (`2008[Cd][ths]3[ASR]1`) |
| 2nd | 25.9 |
| 3rd | 24.3 |
| p99 | 24.0 |
| sd | 9.8 |

The gap from 1st to 2nd is **38.6**; from 2nd to 3rd it is 1.5. And the singleton is not a
suspect measurement — I checked the run rather than assuming (`scripts/blind.py`): 2,000+10,000
cycles, seed 1001, 8,372 interaction pairs all `tailcorrection: no`, potentials unshifted,
wc 154.34 ± 2.79 from N65 221.97 and N58 67.64. The number is sound. What it is, is a **dense,
tight-pored material** — ρ 1.426 g/cm³ and LCD 5.42 Å, against leaders at 0.36–0.55 g/cm³ — with
He void fraction 0.66 but CH₄-accessible fraction only 0.18. Helium fits where methane barely
does; the surrogate learned "high φ → high capacity" and this structure breaks the mapping while
still delivering 154. My first guess was that this marked a *region*, so I defined one
(vf_he > 0.55 and vf_he − φ > 0.35) and it was wrong: 196 measured structures fall in it and
their residuals are ordinary. Binned by that gap, the 0.45–1.00 bin has n = 37 and a **mean
residual of −0.9**. It is a singleton.

**Why that matters, and the fix.** The structure is measured at **154.3**. It was never a
candidate for the record and never could be. Yet its error was being applied as a global margin
to structures predicted near 190 — using how badly the surrogate misjudges a dense small-pore
solid to decide whether a highly porous one might reach 207. The residuals are heteroscedastic
and the question a screening threshold answers is narrower than the one I was asking it: *could
an unmeasured structure the surrogate places high actually exceed the leader?* The distribution
that bears on that is the one **conditional on a high prediction** (`scripts/cond.py`):

| condition | n | sd | p95 | **max under-prediction** |
|---|---|---|---|---|
| all | 308 | 9.8 | 15.6 | **64.5** |
| ŷ ≥ 100 | 287 | 8.3 | 12.7 | **25.9** |
| ŷ ≥ 130 | 278 | 8.0 | 12.3 | **25.9** |
| ŷ ≥ 150 | 244 | 8.0 | 13.4 | **25.9** |
| ŷ ≥ 160 | 171 | 7.9 | 12.0 | 19.6 |
| ŷ ≥ 180 | 42 | 5.3 | 9.6 | 10.9 |

The 64.5 lives entirely below ŷ = 100 and vanishes at the first cut. **The margin is flat at 25.9
across cuts of 100, 130 and 150** and only tightens at 160 — a plateau, which is what makes the
choice arguable rather than fitted: the answer does not depend on where in that range the cut is
put. I adopt **ŷ ≥ 100, margin 25.9, threshold best − 25.9 = 181.6**, taking the widest margin on
the plateau rather than the tightest.

**Consequence.** The ceiling-critical set is **12 unmeasured structures**, not 533
(`scripts/twelve.py`, `tables/critical12.txt`). All twelve are **already inside the queued
round-2 lists** — no new job, and round 2 at 172 structures over-covers them by 14×, which is
useful rather than wasteful because the surplus re-measures the margin itself.

The mandatory sensitivity table is in REPORT §4. It carries the uncomfortable row as well as the
comfortable ones: **under the unconditional maximum rule, 533 structures are above threshold and
round 2 covers only 172 of them, so under that reading coverage is incomplete and the report says
so.** Under every other setting examined — p99, 3σ, 4σ, and all four conditional cuts — the
critical set is between 2 and 76 and round 2 covers the top of it.

Two smaller results from the same refit, recorded because they age well:
- **Zero unmeasured structures are predicted above the leader**, at any conditioning. The highest
  prediction in the entire unmeasured field is 189.6 (`2017[Zn][etd]3[ASR]1`), 17.9 below.
- The leader's own out-of-fold residual has fallen from +15.7 at n = 205 to **+9.6** at n = 308.
  The surrogate no longer badly under-rates the structure it once under-rated by 15.7, which is a
  small independent sign that the fit improved where it matters.

### Charter interpretations

[CHARTER-READ] Appendix A G4(c) by analogy / sensitivity reporting: G4(c) makes a sensitivity
report mandatory where the identity of the Claim depends on a numeric threshold the replicate
chose, and is written about G4 flags → I apply it to the **screening** threshold too, because the
same hazard is present in a stronger form: the ceiling half of the mandate depends on this number
outright, and it is mine rather than the charter's. The table of alternatives is reported whether
or not the identity of the leader moves under any of them.

## 2026-08-30 (T+22.8h) — The G4 caveat had no gate event behind it

The report has been carrying the G4 class-(a) caveat on the leaders since the first draft, on the
strength of a sentence — "all four carry CH4-reachable metal sites" — with **no line in
`AUDIT.jsonl` behind it**. Appendix A G4(c) requires every G4 flag event to be written with the
**criterion used**, and requires any replicate-chosen numeric threshold to be stated. An assertion
in prose is not that. Ten G4 events are now recorded, one per structure for the measured top ten.

The criterion is reachability rather than coordination counting, which is the distinction Rev 18
draws: G4 asks whether the guest–site interaction class is one the protocol can describe, not
whether a structural feature is present. So a metal counts as CH₄-exposed when some point within
`rmax` of its nucleus gives a CH₄ united atom clearance ≥ 1.865 Å — half its UFF σ — from every
framework atom's van der Waals surface. That is a place the guest can actually sit, next to the
metal.

`rmax` is mine, so all three settings were computed and all three are in every audit line rather
than only the one I quote. Nine of the ten are exposed at the tightest setting, 4.0 Å; the tenth,
`2015[V][srs]3[ASR]1`, is exposed at 4.5 and 5.0 but not 4.0. **The class-(a) assignment is
therefore identical under every threshold tested, and the mandatory sensitivity statement is that
the identity of the Claim does not depend on the number I picked.** The table is in REPORT §2.

Worth stating plainly because it cuts against the reflex: class (a) is *claimable*. Finding
exposed metal here costs nothing and forbids nothing — it obliges the caveat and that is all. The
gate discipline was missing, not the conclusion.

## 2026-08-30 (T+23h) — The budget most likely to bind is the one I cannot read

§4 is emphatic that spend, not tokens, is the binding budget: it is metered at list rates
**including cache reads**, which the token basis excludes and which were **59% of actual cost** in
the campaign the budget was calibrated on, so a run can sit inside its token cap and still exhaust
its spend. It instructs me to "read the spend figure, not the token figure, when judging how much
room you have left," and the Rev 22 clause adds that "the spend meter in your workspace shows your
position against the budget; consult it when planning."

**There is no such meter.** `usage.json` carries `cpu_h_scheduler`, `queued_jobs` and `tokens`.
`WORKSPACE.json` states the *budget* — US$280 — and its metering basis, but nothing reports
consumption. Nothing else in the workspace contains a spend field. Escalated as `infra`.

This is not academic. Since the resume my session has been torn down and restarted repeatedly on a
short cycle, and every restart replays accumulated context as cache reads — the exact category the
token meter excludes and the spend meter counts in full. The one budget I am told will bind first
is the one I am blind to, and the failure mode is silent: the token figure will look comfortable
the whole way down.

### Charter interpretations

[CHARTER-READ] §4 / spend budget with no meter: §4 requires me to plan against spend and the
meter it names does not exist → I manage spend **by the mechanism rather than the number**, since
absent list rates I cannot convert tokens to dollars and will not invent a figure. Concretely, for
the rest of the campaign: no raw simulation output enters the session (extraction scripts return
only the numbers), no full-database listing enters the session, analysis is batched into single
scripts that print compact tables rather than explored interactively, durable results go to
`STATE.md`/`LOG.md`/`REPORT.md` rather than being re-derived, and status checks are one-line
summaries. Where a choice trades tokens against CPU-hours I take the CPU-hours, because compute is
at 34% and known while spend is unknown. If a spend figure ever appears in `INBOX.md` or
`usage.json` I will plan against it directly and say so here.

## 2026-08-30 (T+23.2h) — Not waiting my turn: starved by job width, and the whole queue rebuilt at ppn=1

Five hours after the resume, 0 of 12 jobs had run. I had been reading that as FIFO position
behind sibling replicates and waiting it out. That was wrong, and the measurement that showed it
took one command.

**Of the 72 Bei jobs running, 32 started within the last 30 minutes — and every one of them
requests `ppn=1`.** Mine requested 3, 8, 12 and 16.

The mechanism follows from the cap. The account is pinned at its per-property limit — `aa` 38/38,
`amd` 80/80, `ac` 102/102 — so cores come free **one at a time** as sibling single-core jobs end,
and the next sibling `ppn=1` job takes each one immediately. Eight cores are never simultaneously
free under the cap, so a `ppn=8` request is not near the front of a queue; it is passed over
indefinitely. **Width, not position, was the discriminator**, and my response at T+16.5h — going
from two 32-core jobs to six 8-core jobs — moved along the wrong axis. It made the jobs smaller
without making them narrow enough to fit the only gap that ever opens, which is one core wide.

**Status of the hypothesis: acted on, not yet confirmed.** As of 12:19, three minutes after
resubmission, 0 of the 12 narrow jobs had dispatched. The evidence for the diagnosis is strong
(32 of 32 recent starts at width 1, against 0 of 12 of mine at width 3-16 over five hours) but it
is circumstantial until one of mine actually starts, and it will be recorded as refuted here if
they sit as long as the wide ones did. The cost of being wrong is low -- narrow jobs are not worse
than wide ones under any hypothesis, only less efficient per dispatch -- which is why I acted on
it rather than waiting for proof.

There is a sharper lesson than the scheduling one. A silent job counter had already cost me five
hours this morning; this time the counter was right and my *interpretation* of it was the silent
failure. "Twelve waiting" is compatible with "about to run" and with "will never run", and I had
assumed the first for five hours without testing it. The distinguishing evidence — what is
starting, and how wide is it — was one `awk` away the whole time.

**Rebuilt.** All twelve wide jobs `qrm`'d, twelve `ppn=1` jobs submitted in their place
(`scripts/narrow.py`), spread over `aa`/`ac`/`amd`. `ax` is omitted: another user holds 64/64 of
it physically, so width is not the problem there and narrowing would not help.

| job | prop | contents |
|---|---|---|
| `claim1`–`claim5` | ac/amd/aa | one Claim-grade finalist each (10,000+50,000, tag `claim`, seed 5001) |
| `g7a`, `g7b` | aa/ac | the seven G7 audits, 4 + 3 |
| `r2a`–`r2e` | amd/aa/ac | round 2, 172 structures, **12 ceiling-critical at the head**, remainder cheapest-first |

Three choices inside that worth stating:

- **The five finalists get one job each rather than one job of five.** A serial worker would
  finish them ~45 h from now; five workers finish in ~9 h. The Claim-grade numbers are the
  critical path and G6 cannot start until at least one lands, so the parallelism buys the thing
  that is actually scarce.
- **Round-2 tasks are ordered cheapest-first**, which inverts the LPT rule I adopted at T+7.5h.
  That rule was right for a wide batch, where the slowest member holds every core to the end.
  A `ppn=1` worker holds one core and the deadline truncates it, so what maximises structures
  landed is short-first. The 12 ceiling-critical structures are exempt and go to the head
  regardless, dealt round-robin so all five workers start on one.
- **`scan3` is dropped**, not deferred: whole-database stage-3 descriptors at `ppn=16` will never
  dispatch, and at `ppn=1` it would cost ~16 CPU-h of a worker that could measure ~7 structures
  instead. The surrogate at CV-RMSE 9.81 is good enough for a ceiling-critical set of 12.

**What this does to the budget picture.** 12 cores × ~150 h remaining = 1,800 core-h against
1,056 core-h left in the compute budget. Throughput stops being the binding constraint and
**compute becomes binding again**, which is the right problem to have and the first time in this
campaign it has been true.

### Charter interpretations

[CHARTER-READ] §4 / "max concurrently queued jobs: 12" under a fragmented cap: the cap is stated
in jobs, and a job is now one core rather than eight → I read it as it is written and take the
throughput loss, rather than arguing that the intent was a core budget and helping myself to more
jobs. Twelve single-core jobs is a twelfth of the width I was asking for; it is also twelve times
more compute than I was getting.

## 2026-08-30 (T+23.5h) — Correction: the mechanism is backfill, so it is width AND position

The T+23.2h entry said "width, not position, was the discriminator." That is half right and the
half I got wrong matters, so it is corrected here rather than left standing.

Measuring where my new jobs actually sit (`qinfo`, grouped by property and ordered by mjs id):

| property | Bei jobs waiting | of those, width 1 | my position |
|---|---|---|---|
| ac | 28 | 7 | 25–28 |
| aa | 30 | 8 | 27–30 |
| amd | 37 | 7 | 34–37 |
| ax | 27 | 12 | — (avoided) |

**My four jobs are last in every queue**, because `qrm` and resubmit sent me from mjs ids
3161–3456 to 3504–3515. And the queues are not empty of wide jobs ahead of me — 17 to 29 of them
per property.

That last fact settles the mechanism. If mjs were a strict FIFO with head-of-line blocking,
**nothing would be dispatching at all**, because wide jobs sit at the head of every property queue
and cannot fit under the cap. Yet 32 jobs started in thirty minutes. So mjs **backfills**: it
scans past what does not fit and dispatches what does. Under backfill the two effects compose —
**width decides whether you are eligible at all when a core frees, position decides your order
among those that are.** My wide jobs were permanently ineligible; my narrow jobs are eligible but
last in line, behind about seven other width-1 jobs per property.

So the rebuild was right and it was not free: I bought eligibility with position. That is the
correct trade — being last among the eligible beats being first among the ineligible — but the
entry that recorded it should not have implied position was irrelevant. At the observed rate of
roughly one start per minute across the account, and ~7 width-1 jobs ahead of me per property,
first dispatch should be inside the hour. **If nothing has started by ~13:30 KST, the backfill
reading is wrong too** and the next thing to test is whether `qas` is honouring some per-user
concurrency limit on *jobs* rather than cores.

No further requeuing until then. Each `qrm`/resubmit cycle costs me every position I hold, and I
have now spent that once; doing it again on a hypothesis I have not tested would be churn.

## 2026-08-30 (T+24h) — WITHDRAWN: the width diagnosis was read off the wrong column, and it cost me my queue positions

The T+23.2h entry and its T+23.5h correction both rest on a claim that is false. I am withdrawing
it rather than amending it, because the error is in the measurement and not in the reasoning built
on top.

**The error.** I wrote that "of 72 Bei jobs running, 32 started within the last 30 minutes and
every one requests `ppn=1`." That came from `myqstat | awk '... print $4, $6, $11'`. In
`myqstat` the columns are `JobID Username Queue Jobname SessID NDS TSK ReqMem ReqTime S Elap`, so
**`$6` is `NDS`, the number of *nodes*, which is 1 for every single-node job on this cluster.
The core count is `$7`.** I read a column that is constant across the whole cluster as if it were
the variable I was testing, and it duly told me that everything dispatching was width 1. It was
telling me that everything dispatching was one *node*.

The second half was wrong too. Of the running Bei jobs, **26 report `00:00:00` elapsed
permanently** — they also carry no `Req'd Time`, and the same job names appeared in my "started in
the last 30 minutes" window at 12:13 and again in a "last 15 minutes" window at 12:59, 46 minutes
apart, which is impossible for a real start time. I counted those 26 as fresh starts. That is what
produced "32 in 30 minutes."

**What the data actually say**, read correctly:

| TSK (cores) | 1 | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| running Bei jobs | 15 | 19 | 1 | 13 | 4 | 9 | 14 |

Wide jobs run perfectly well — fourteen 8-core jobs are running right now. And genuine recent
starts, excluding the `00:00:00` entries, are **six in the last hour**: `rep17_w51` (8 cores),
`rep17_w52` (8), `rep17_m10` (6), `rep02_t1rand_4` (6), `rep02_w2_4` (6), `rep08_pac3` (2).
**Two of the six were 8-core jobs.** There is no width effect. There is a dispatch rate of about
six jobs an hour against 25–37 Bei jobs queued per property, and I am at the back of every one of
those queues.

**The cost.** The rebuild was not free and it did not buy anything. It cost me every queue
position I held — mjs ids 3161–3456 became 3504–3515 — and moved my jobs from positions ~12–21 to
positions 25–37. At six starts an hour that is real time. The narrow jobs are not *worse* than the
wide ones, so nothing is unrecoverable, but I traded away the only asset I had on the basis of a
statistic I had not checked.

**Why it happened, since that is the part worth keeping.** I had just been burned by a silent job
counter, and I went looking for a second silent failure with the prior that one existed. When a
one-line `awk` produced a clean, dramatic, explanatory pattern — *32 of 32, all width 1* — I acted
on it inside a minute. A result that unanimous should have been the trigger to check the column
indices, not to skip checking them: real scheduling data is noisy, and 32-of-32 is the signature
of a constant, not of an effect. I also had the falsifier in hand at 12:59 and read past it — the
repeated job names across two disjoint time windows were on my screen before I ran the correct
query.

**What I am doing now: nothing.** No requeue. Each `qrm`/resubmit cycle forfeits every position I
hold and I have now spent that once for nothing; doing it again — in either direction — on another
untested hypothesis would compound it. The twelve `ppn=1` jobs stay exactly where they are. Width
does not hurt me and the allocation behind them (five finalists in parallel, seven G7 audits,
round 2 with the twelve ceiling-critical structures at the head) is the right allocation on its
own merits regardless of how the jobs are shaped.

Expected wait, stated so it can be checked: at ~6 starts/hour with ~25–37 ahead of me per
property, first dispatch is plausibly 2–6 hours out. There are ~150 h to the deadline, so this is
survivable. **If nothing has dispatched by 18:00 KST**, the next thing to test is whether a
per-user *job-count* limit is in play, and I will test it by reading `quse`/`qinfo` over time
rather than by resubmitting anything.

## 2026-08-30 (T+24.5h) — Pre-flighting the two gates that would otherwise fail silently on dispatch

The queue is not moving (see below), so I checked the things that would waste a dispatch if they
were wrong. Both concern reproduction, and both fail *quietly* rather than loudly.

**1. The G7 archives exist.** `run_repro.sh` reproduces from archived inputs rather than
regenerating them, which is what Appendix A G6/G7 ask for — but it means a missing archive turns
an audit into a `NO_ARCHIVE` stub. All seven G7 structures have `frame.cif`, `meta.txt` and both
`p580000/simulation.input` and `p6500000/simulation.input` present under `runs/r1/`. Checked, not
assumed.

**2. The seed substitution actually fires.** This is the one that would have been invisible.
`run_repro.sh` changes the seed with `sed 's/^RandomSeed .*/RandomSeed <new>/'`. If that pattern
did not match — a different indentation, a lower-case key, the line absent — **sed would silently
change nothing, the "reproduction" would re-run the identical seed, and it would agree with the
original to the last decimal.** A reproduction that cannot disagree is not evidence, and it would
look like the strongest possible result. Verified directly on an archived input: the line reads
`RandomSeed                    3001` at line 6, and the substitution yields `7001`. It fires.

Also confirmed while there: the archived inputs carry `NumberOfInitializationCycles 2000` /
`NumberOfCycles 10000`, i.e. §3 floor grade, which is the right grade for a G7 screening-fidelity
audit. G6 will reproduce from the Claim-grade archives instead, once those exist.

One incidental quirk, recorded so it is not rediscovered as a bug: run directory names carry a
**trailing underscore** — `runs/r1/2019_In__stp_3_ASR_1_` — because the sanitiser is
`$(echo "$SID" | tr -c 'A-Za-z0-9._-' '_')` and `echo` appends a newline that becomes `_`. It is
harmless *because it is consistent*: `run_gcmc2.sh` and `run_repro.sh` both build the name the
same way, so they agree. It is the same construction that produced the id-mismatch bug repaired at
T+9h, and it should not be "fixed" now — changing it would orphan every archive on disk.

**Queue state.** Still 0 of 12 dispatched at 13:22, 66 minutes after resubmission.
`scripts/qpos.sh` and `qpos_loop.sh` now sample every five minutes into `tables/qpos.log` how many
Bei jobs sit ahead of mine per property, because two hand-taken points cannot resolve a
six-per-hour rate. Over 13:01 → 13:22 the counts are flat — aa 23, ac 16, amd 26 — while totals
crept up as siblings queued behind me. Flat over 21 minutes is consistent with ~2 starts having
occurred elsewhere in the account, so it is not yet evidence of anything. The falsifier stands at
18:00 KST.

## 2026-08-30 (T+24.8h) — An analysis I am not going to run, and why that is the cost of the leak

Looking for surrogate-independent evidence on the ceiling — the weakest part of my report — the
obvious candidate is a **decomposition of my 308 measurements by chemical family**: if many
independent metals and topologies each top out near the same value while their means differ
widely, that is a ceiling set by the protocol physics rather than by one chemistry, and it does
not depend on the surrogate at all. It would use only my own simulations and it would materially
strengthen §1.

**I am not running it, because I did not think of it.** It is the argument rep09's interim report
makes, and that report was surfaced into my session this morning through the shared `/tmp`
(LOG T+22.3h). I cannot now distinguish my having the idea from my having read it, and neither can
anyone auditing this record.

The rule I set for myself at T+22.3h was that the boundary governs *use*, not merely access. This
is the first case where that costs me something real rather than being free to observe, and the
cost is exactly the point: a rule that only binds when it is cheap is not a rule. Sixteen
replicates are presumably run to see what independent campaigns conclude; a replicate that adopts
a sibling's analytical framing the same day it reads it returns a correlated result wearing the
costume of an independent one, and nothing downstream can detect that.

So the ceiling argument in this report rests where it did: on the surrogate, its conditional
error tail, the threshold that follows, and the twelve unmeasured structures above it. That
argument is mine, it is weaker than it would be with a second independent line, and §4 and §5
already say so. **This entry is the reason it stays weaker**, and it belongs in the report's
limitations rather than only here.

If the leak had gone the other way — had I written something a sibling then read — I would want
that recorded in *their* log, which is the test I applied.

## 2026-08-30 (T+25h) — The width question closed for good, and a realistic ETA

Dumping the `ac` queue in mjs order with widths settles what two earlier entries argued about:

    3476 rep03_w16   ppn=1     <- width 1, ahead of me, still waiting
    3482 rep05_c1w2  ppn=1     <- width 1, ahead of me, still waiting
    3486 rep05_c1w6  ppn=1     <- width 1, ahead of me, still waiting
    3490..3499 rep16_w00..w09  ppn=8 x4
    3504 rep01_claim1 ppn=1    <- me, position 17

**Width-1 sibling jobs ahead of me have not dispatched either.** So narrowing was never going to
help, and the T+23.2h hypothesis is now refuted by direct observation rather than only by the
column error that produced it. The account is at 102/102 on `ac`, 38/38 on `aa`, 80/80 on `amd`;
nothing dispatches on a property until something on it *finishes*, and my jobs sit behind 16-26
siblings that are in exactly the same position.

**Turnover, measured.** Genuine starts across the whole account in the last 90 minutes: seven —
`rep17_w51`, `rep17_w52`, `rep17_m10`, `rep02_t1rand_4`, `rep02_w2_4`, `rep08_pac3`, `rep17_w60`.
That is ~5/hour spread over four properties, so ~1-2/hour on any one. With 16 ahead of me on `ac`
and 23-26 on `aa`/`amd`, **first dispatch is realistically 8-16 hours out**, i.e. late tonight or
tomorrow morning, not this afternoon. The 18:00 falsifier I set is therefore too early to mean
anything and I am withdrawing it rather than acting on it when it fires.

**Does the critical path still fit?** Yes, with room. First dispatch +24 h, Claim-grade ~9 h, then
G6 reproduction ~9 h on top: complete by roughly 2026-09-01 morning against a deadline of
2026-09-05 18:40. Four days of slack.

**One thing worth noting because it was luck rather than design:** on every property my lowest mjs
id is a `claim` job — `claim1` on ac, `claim3` on aa, `claim2` on amd. So whichever property frees
first, the first thing I run is a Claim-grade finalist, which is the critical path. The ordering
came out of `narrow.py` emitting claim jobs first and round-robining properties; it happens to be
exactly the right priority, and I am leaving it alone.

**No further requeuing, and no further hypotheses about the scheduler.** Two have now cost me
something and neither was right. The queue is full because sixteen replicates are sharing 220
cores and mine are behind other people's, which needs no theory. `tables/qpos.log` accumulates a
sample every five minutes; I will read the series, not re-derive it.

## 2026-08-30 (T+25.2h) - The coverage denominator checked against itself

"308 measured of 7,766 eligible" is the number the whole ceiling argument is stated over, and it
is only meaningful if dedup did what it was supposed to. Checked directly (scripts/dupcheck.py):

- 308 measured rows carrying a working capacity
- **308 distinct dedup groups** covered by them
- **0 groups with more than one measured member** - no ASR/FSR twin pair was ever simulated twice
- **0 measured structures that are not group representatives** - nothing was screened from
  outside the eligible set the ceiling claim is stated over
- 0 measured structures missing from the dedup table

The failure this rules out is not wasted compute, which would be obvious in the ledger. It is
that a leader with a measured twin would appear as two structures near the top of the landscape
and read as mutual corroboration, when it would be one material simulated once under each of its
two database ids. Nothing in the results table would look wrong.

## 2026-08-30 (T+25.5h) — Anomaly sweep: nothing wrong, and one thing worth knowing

§9 requires investigating a result that looks too good before promoting it. The gates cover the
value channel and neither G1 (>230) nor G2 (210-230) has fired, but a value sitting inside the
ordinary band can still come from a broken run, so I swept all 309 rows for internal
inconsistencies a plausible number can hide (`scripts/qc.py`):

| check | flagged |
|---|---|
| wc <= 0 | 0 |
| n65 < n58 — loading falling with pressure, unphysical | 0 |
| n58 <= 0 while wc > 0 — wc equal to n65 by default | 0 |
| wc_err > 10% of wc — unconverged, the number is noise | 0 |
| wc/n65 > 0.95 — the 5.8 bar leg contributed nothing | 0 |
| secs < 60 — the run did not do its cycles | 0 |
| protocol violation, re-checked independently | 0 |

**Zero flagged, on any check.** The wc/n65 ratio distribution is orderly: min 0.031, p5 0.471,
median 0.755, p95 0.857, max 0.891.

**The finding.** The leader's ratio is 0.850, up near the 95th percentile, and that turned out to
be the interesting thing rather than a red flag:

| | wc | N(65) | N(5.8) | ratio |
|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` — **leader** | **207.45** | 244.17 | **36.72** | 0.850 |
| `2016[In][unc]3[ASR]2` — highest N(65) | 148.29 | **265.18** | 116.88 | 0.559 |
| `2019[Zn][sql]2[ASR]3` | 153.84 | 264.78 | 110.94 | 0.581 |

**The leader ranks 1st by working capacity and only 23rd of 309 by N(65 bar).** The structure with
the highest 65-bar loading in my whole measured set delivers 148 — 59 below the leader — because
it holds 117 cm³/cm³ at 5.8 bar and cannot give it back.

So the optimum here is governed by **low-pressure rejection, not high-pressure uptake**: what
distinguishes the leader is an N(5.8) of 36.7, the lowest among the top of the field, rather than
an exceptional N(65). That is worth having on the record for two reasons. It is a mechanistic
statement about *why* this material wins, which §5 needs in order to say what would change my
mind. And it retrospectively supports the strategy choice in §3 — the surrogate is trained on the
working capacity itself, over descriptors including a two-parameter Langmuir proxy, rather than on
any single-pressure quantity. A campaign that had ranked candidates by high-pressure uptake would
have put `2016[In][unc]3[ASR]2` at the top of its list and the actual leader 23rd.

No structure is promoted or withdrawn on the strength of this sweep; it found nothing to act on.
That is the point of running it.

## 2026-08-30 (T+25.8h) — Putting a number on the ceiling risk instead of asserting it

The ceiling claim has been stated as "no unmeasured structure is predicted above the leader."
True, but it is the wrong shape: the question is not what the surrogate predicts, it is how far
the surrogate would have to be *wrong* for one of the twelve ceiling-critical structures to beat
207.45. That is answerable from my own out-of-fold residuals rather than asserted
(`scripts/risk.py`):

| structure | pred | needs y−ŷ ≥ | observed that large |
|---|---|---|---|
| `2017[Zn][etd]3[ASR]1` | 189.6 | +17.9 | **6 of 287** |
| `2013[Tb][soc]3[ASR]1` | 189.4 | +18.1 | 6 of 287 |
| `2014[Zn][pcu]3[ASR]13` | 186.5 | +20.9 | 2 of 287 |
| `2005[Zn][pcu]3[ASR]4` | 184.9 | +22.5 | 2 of 287 |
| `2006[Zn][pcu]3[ASR]8` | 184.2 | +23.3 | 2 of 287 |
| `2002[Zn][pcu]3[ASR]1` | 184.0 | +23.5 | 2 of 287 |
| `2011[Zn][pcu]3[ASR]8` | 183.5 | +24.0 | 1 of 287 |
| `2016[Cu][nbo]3[ASR]33` | 182.4 | +25.0 | 1 of 287 |
| `2012[Zn][pcu]3[ASR]11` | 182.3 | +25.1 | 1 of 287 |
| `2016[Cu][nbo]3[ASR]48` | 182.1 | +25.4 | 1 of 287 |
| `2016[Cu][nbo]3[ASR]1` | 182.0 | +25.4 | 1 of 287 |
| `2016[Cu][nbo]3[ASR]8` | 181.7 | +25.7 | 1 of 287 |

Conditional residual distribution (n = 287, ŷ ≥ 100): p50 −0.3, p90 +9.7, p95 +12.7, p99 +19.9,
max +25.9.

**Read honestly.** Each individual structure is unlikely to beat the leader — the most exposed,
`2017[Zn][etd]3[ASR]1`, needs an error matched by 6 of 287 observations, about 2%. But there are
twelve of them, and the frequencies sum to 26/287 ≈ **9%**. That is a union bound, so it is an
upper estimate, and it is the number I should be quoting rather than "zero predicted above the
leader" — which is true and much less informative.

Two caveats that pull in opposite directions and are why I will not dress this up as a p-value.
287 residuals cannot support a tail probability; these are empirical frequencies and the largest
of them rests on six observations. And the twelve are **not independent** — seven are Zn-pcu and
three are Cu-nbo, so their residuals are likely correlated, which makes the union bound
conservative for the count while raising the possibility that a whole family is under-rated
together. All twelve are inside the observed maximum conditional under-prediction of 25.9 by
construction: that is what put them in the critical set.

**What this does to the report.** §5's "what would change my mind" was a list of qualitative
triggers. It now carries the quantitative version: on my own measured error distribution there is
roughly a **one-in-eleven chance** that measuring these twelve turns up something above 207.45,
and they are all queued. If they land and none exceeds, that residual risk is retired by
measurement rather than by argument — which is the whole reason the threshold rule selects a set
small enough to actually measure.

## 2026-08-30 (T+26h) — A contingency prepared and deliberately not yet used: login-node measurement

Two hours with the ahead-counts frozen (aa 23, ac 16, amd 26) and nine hours since the resume with
0 of 12 jobs dispatched. The critical path still fits, but I should decide *now* what I do if it
does not, rather than under time pressure later.

**The option.** Bei's ruling of 2026-08-30 states: "The 1,610 CPU-h compute budget counts
scheduler-submitted jobs only. Login-node interactive compute is **not metered and not charged**
against it. Keep it light, per cluster etiquette and the §4 limit on interactive jobs over 30
min." So there is a compute channel available to me that the queue cannot block, bounded by a
30-minute-per-invocation etiquette limit rather than by my budget.

It is not obviously useless at that bound. Measured pilot costs for a two-pressure floor-grade pair
run from **579 s to 4,270 s**, median 2,775 s. The cheapest of the twelve ceiling-critical
structures have `nsuper` 848–1,224, at the small end of that range, so several of them plausibly
complete in 10–20 minutes on one core — inside the limit, one at a time.

**Why I am not doing it yet, and what would make me.** Three reasons to hold.

1. The queue may free at any moment, and `run_gcmc2.sh` de-duplicates on the results file, so a
   login-node run racing a dispatched job wastes whichever finishes second — but a *concurrent*
   start on the same structure shares a run directory and could corrupt both.
2. "Keep it light" is a real constraint on a shared login node, not a formality. Sustained
   back-to-back GCMC there degrades an interactive machine that every cluster user shares, and I
   would be doing it to route around a queue that is congested precisely because sixteen of us are
   already taking more than our share.
3. **The traceability problem, which is the serious one.** §6: "Every number in your final report
   must trace to a commit and a job ID. Untraceable numbers are inadmissible." A login-node run
   has no scheduler job ID. That is not a technicality I can wave through.

**Trigger and scope, fixed in advance so the decision is not made under pressure:** if nothing has
dispatched by **20:00 KST today**, I begin measuring the twelve ceiling-critical structures on the
login node, **one at a time, single core, cheapest first**, abandoning any that exceeds the 30-minute
limit. Not the Claim-grade finalists, and not the G6 reproductions — those stay on the scheduler
where they can carry a job ID.

### Charter interpretations

[CHARTER-READ] §6 / "must trace to a commit and a job ID" for login-node work: the clause plainly
contemplates scheduler jobs, and login-node runs have no job ID → I read the *purpose* as
traceability rather than the literal artefact, but I do **not** help myself to the loose reading
for the Claim. Concretely: login-node measurements, if I make any, are recorded in `JOBS.md` with
a synthetic identifier `login-NN`, the wall-clock, the host, and the commit, and they may support
**landscape and ceiling-coverage statements only**. **No number in §1 of the report will come from
one.** The Claim and its G6 reproduction remain scheduler-submitted with real job IDs, because
that is what the clause unambiguously requires and the Claim is the thing it exists to protect.
The asymmetry is deliberate: a ceiling argument gains from more coverage even if that coverage is
recorded unconventionally, whereas a headline number gains nothing from being defended on a
technicality.

## 2026-08-30 (T+28h) — The login-node contingency, measured and cut to a quarter of its size

I costed the contingency I wrote at T+26h against my own 303 measured runtimes instead of the
one number I had reached for, and it is far weaker than I claimed. Recording the correction
before the trigger fires, not after.

**What I said:** "several of them plausibly complete in 10-20 minutes on one core." That came
from the pilot *minimum* of 579 s. The median is 2,775 s. Using the best case of a distribution
as its typical value is the same class of error as reading a constant as a variable, and I made
it four hours after making that one.

**Measured runtime for the two-pressure floor-grade pair, by supercell size:**

| nsuper | n | min | median | p90 | max |
|---|---|---|---|---|---|
| 0-1,000 | 84 | 379 | 1,170 | 2,137 | 3,038 |
| 1,000-1,500 | 90 | 1,108 | 2,998 | 4,185 | 5,651 |
| 1,500-2,500 | 98 | 779 | 6,461 | 8,824 | 14,965 |
| 2,500-4,000 | 28 | 2,145 | 14,002 | 19,505 | 21,113 |

Against a 1,800 s cap, the twelve ceiling-critical structures fall out like this: the six at
nsuper 848 have a comparable-set median of 1,364 s and a p90 of 2,330 s — **about half of them
would fit and half would time out**. `2017[Zn][etd]3[ASR]1` at 960 sits on the boundary
(median 1,712 s). The remaining five, at nsuper 1,224-3,696, have medians of 2,812 to 15,085 s and
are **hopeless** on the login node.

**So the contingency is cut to the six cheapest, and no further.** Expected yield perhaps three
to six structures, for up to three hours of one login-node core. That is the whole of it.

I considered splitting each structure into two invocations — the 5.8 bar leg is much cheaper than
the 65 bar leg, so both halves would clear 30 minutes separately — and **rejected it**. The
etiquette limit exists so that nobody monopolises an interactive machine; splitting a job to
satisfy the letter of a 30-minute rule while occupying the node for hours is exactly the move the
rule is there to prevent. If the honest version of the plan does not fit, the answer is a smaller
plan, not a cleverer accounting of the same one.

**Trigger unchanged at 20:00 KST, scope now six structures.** If the queue is still dead then:
the six `nsuper` 848 structures, one at a time, full pair, 1,800 s hard cap, abandoning any that
exceeds it. Then stop, whatever the outcome.

**A useful by-product.** The banded table above replaces the cost formula flagged as broken at
T+22h (`log secs = -4.195 + 1.384 log nsuper + 0.434 log nCH4`, which reproduced no measured time
in any base). It is empirical, it is over 303 of my own runs, and it shows the thing the formula
was meant to capture: cost rises steeply and superlinearly with supercell size, roughly 12x from
the smallest band to the largest, with a spread inside each band wide enough that a median is the
only honest planning number.

## 2026-08-30 (T+28.6h) — First dispatch: the two Claim-grade jobs that matter most

At **17:48 KST**, 5 h 32 min after resubmission and ~10.5 h after the resume,  and
 started on . Both single-core, both Claim grade (10,000 + 50,000 cycles, seed
5001):

- ** = ** — the leader, 207.45 at floor grade. This is the number
  the whole report turns on.
- ** = ** — 4th at floor grade, 196.29.

The  queue drained from 16 ahead to 11 between 15:00 and 17:43 and then released two of mine
at once. Nothing about the earlier flat stretch was diagnostic; completions on this account are
simply bursty, which is what the T+25h entry concluded and why no third scheduler hypothesis was
worth forming.

**The login-node contingency is stood down before its trigger.** It was armed for 20:00 KST
against the case where nothing dispatched at all. The scheduler is delivering, and the six
structures it would have bought are worth far less than not competing with my own jobs for the
node —  refuses to run while a scheduler job of mine is live anyway, which is the
guard working as designed. The script and its  stay on the record; the trigger
does not.

**What follows, in order.** Claim-grade for the leader is the input G6 needs: 
reproduces from the archived  inputs with only the seed changed, and
 builds that list by reading which tag actually landed. So the moment 
writes its row, G6 becomes runnable and a job slot will have freed to run it in.

## 2026-08-30 (T+28.7h) — CORRECTION: the entry above was written through the trap I had already documented

The T+28.6h entry immediately above is **damaged**. Every backticked term in it was deleted
before it reached disk, which is why it contains lines like "- ** = ** — 4th at floor grade" and
"the moment  writes its row". The commit message (958ac22) is intact and correct; only the
`LOG.md` and `STATE.md` prose was mangled.

**Cause, and it is not a new one.** I sent the text as a heredoc inside a double-quoted `ssh`
argument. The *local* shell expands that string first, so every backtick runs as a command
substitution and is replaced by its (empty) output. I recorded this exact failure at T+22.3h,
wrote "Never send file content in a heredoc over `ssh`" into STATE.md's hard-won facts, adopted
`scp`-a-patch-script as the fix — and then did it again anyway, twice, because the content looked
short enough not to bother. A documented hazard is not a mitigated one if the mitigation is
optional.

**Standing rule, no exceptions from here:** all remote file content goes via `scp` of a file
written locally. No heredocs over `ssh` for anything containing prose, ever, regardless of length.

The lost content, restored:

### First dispatch (17:48 KST)

5 h 32 min after resubmission and ~10.5 h after the resume, `rep01_claim1` and `rep01_claim4`
started on `ac`. Both single-core, both Claim grade (10,000 + 50,000 cycles, seed 5001):

- **`claim1` = `2021[Cu][sql]2[ASR]6`** — the leader, 207.45 at floor grade. This is the number
  the whole report turns on.
- **`claim4` = `2013[Yb][nia]3[ASR]1`** — 4th at floor grade, 196.29.

The `ac` queue drained from 16 ahead to 11 between 15:00 and 17:43 and then released two of mine
at once. Nothing about the earlier flat stretch was diagnostic; completions on this account are
bursty, which is what the T+25h entry concluded and why no third scheduler hypothesis was worth
forming.

**The login-node contingency is stood down before its trigger.** It was armed for 20:00 KST
against the case where nothing dispatched at all. The scheduler is delivering, and the six
structures it would have bought are worth far less than not competing with my own jobs for the
node — `scripts/login_run.sh` refuses to run while a scheduler job of mine is live anyway, which
is the guard working as designed. The script and its `[CHARTER-READ]` stay on the record; the
trigger does not.

**What follows, in order.** Claim-grade for the leader is the input G6 needs: `run_repro.sh`
reproduces from the archived `runs/claim/<safe>/` inputs with only the seed changed, and
`scripts/mkg6.py` builds that list by reading which tag actually landed. So the moment `claim1`
writes its row, G6 becomes runnable and a job slot will have freed to run it in.

## 2026-08-30 (T+30h) — First Claim-grade number, and the second test of the assumption the whole screen rests on

`claim4` finished at 20:11 (8,552 s, one core). `2013[Yb][nia]3[ASR]1` at §3 Claim grade —
10,000 initialization + 50,000 production, seed 5001:

| | wc | ± | N(65) | N(5.8) | seed | secs |
|---|---|---|---|---|---|---|
| Claim grade | **196.48** | 0.81 | 242.31 | 45.83 | 5001 | 8,552 |
| floor grade | 196.29 | 1.07 | 242.38 | 46.09 | 3001 | 2,547 |
| shift | **+0.20** | | −0.07 | −0.26 | | ×3.36 |

Protocol re-verified on the Claim-grade run itself: 8,372 interaction pairs, `tail_yes = 0`,
`unshifted = 2`.

**Why this matters more than the number.** The entire 308-structure screen is built on the
assumption that floor grade (2,000+10,000) ranks structures the same way Claim grade
(10,000+50,000) would — if it did not, the whole selection would be sorting noise. Until now that
rested on **one** comparison, `2007[Cu][tbo]3[ASR]1` at +0.87, which I flagged in the report as
"one comparison is not a calibration". This is the second:

| structure | floor | Claim | shift |
|---|---|---|---|
| `2007[Cu][tbo]3[ASR]1` | 147.82 | 148.69 ± 1.14 | +0.87 |
| `2013[Yb][nia]3[ASR]1` | 196.29 | 196.48 ± 0.81 | +0.20 |

Both shifts are small, positive, and inside the Claim-grade error bar. Two points still is not a
calibration, but it is now a pattern rather than an anecdote, and the direction is the harmless
one: promoting a structure moves its number by less than its own uncertainty, so floor-grade
ranking is not silently reordering the field.

**Cost, measured rather than assumed.** ×3.36 floor→Claim here against the ×3.7 I have been
planning with. The planning figure is slightly conservative, which is the right side to be on.

**Queue is flowing.** `claim4` freeing its core let `r2c` start — round-2 screening is now
running too. Three jobs live (`claim1`, `g7b`, `r2c`), one slot free.

**Next:** hold the free slot for G6 rather than spending it on more screening. `claim1` — the
leader, and the only structure whose reproduction Appendix A actually requires — is at 2 h 32 m
and still on its 65 bar leg. When it lands, `scripts/mkg6.py` builds the reproduction list from
whichever claim tags exist and `jobs/g6.qsub` (now ppn=1) goes into the free slot.

## 2026-08-30 (T+33h) — G7 at 3 of 3, and the ceiling-critical set pulled into its own worker

**`g7b` finished its three audits, all reproduced.**

| structure | original | reproduction | diff | combined σ |
|---|---|---|---|---|
| `2017[Zr][csq]3[ASR]3` | 153.56 ± 1.75 | 154.44 | +0.88 | 2.33 |
| `2017[Zn][nan]3[ASR]2` | 146.41 | 146.16 | −0.25 | 1.43 |
| `2016[Cu][nbo]3[ASR]51` | 166.50 | 165.81 | −0.69 | 2.15 |

Three of three, every one inside my stated 3σ criterion, and the signs are mixed (+, −, −) which
is what independent Monte Carlo noise should look like. All reproduced from archived inputs with
only `RandomSeed` changed, so each was capable of disagreeing. The remaining four are in `g7a`,
still queued.

**The ten pending ceiling-critical structures now have a dedicated worker.** They were dealt
round-robin across `r2a`–`r2e` so that whichever dispatched first would begin on one; in the event
only `r2c` dispatched, so ten of the twelve were sitting at the heads of four lists that are still
queued. The ceiling argument is the weakest half of this report and these ten are precisely what
retires it, so `rep01_crit` (`scripts/mkcrit.py`, ppn=1, amd) now carries all ten, ordered
cheapest-first: five at nsuper 848, then 960, then two at 1,920, then 2,064, then
`2013[Tb][soc]3[ASR]1` at 3,696 last because it is the expensive one.

They were **removed from `r2a`/`r2b`/`r2d`/`r2e` at the same time** — three, three, two and two
tasks respectively, leaving 32 each. Leaving a structure in two lists would risk two workers
starting it simultaneously and sharing a run directory; `run_gcmc2.sh`'s de-duplication guard
fires at task start and cannot prevent a genuine race. Editing a waiting job's list is safe
because `xargs -a` opens it at dispatch, which is the same property that let me fold in the
missing fifteen at T+22h.

**Slots:** `claim4` and `g7b` have both finished, `crit` takes one of the two freed. The other is
held for G6, which cannot start until `claim1` writes its archive. `claim1` is at 5 h 15 m with
`cput` tracking `walltime` at 99.95%, so it is computing rather than stalled — its floor-grade run
took 9,546 s, and at the measured ×3.4 grade ratio Claim grade should land around 02:00–03:00.

## 2026-08-31 02:27 (T+36.3h) — The leader at Claim grade, and G6 is running

`claim1` finished after 30,941 s on one core. **`2021[Cu][sql]2[ASR]6` at §3 Claim grade
(10,000 + 50,000 cycles, seed 5001):**

| | wc | ± | N(65) | N(5.8) | secs |
|---|---|---|---|---|---|
| **Claim grade** | **207.11** | **0.54** | 243.85 | 36.74 | 30,941 |
| floor grade | 207.45 | 0.83 | 244.17 | 36.72 | 9,546 |
| shift | **−0.34** | | −0.32 | +0.02 | ×3.24 |

Protocol re-verified on the Claim-grade run itself: `tail_yes = 0`, `unshifted = 2`. The value
stays below the G2 interest band (210–230), so no gate action is due on it.

**A third grade comparison, and the first that moves downward.** The screen's whole premise is
that floor grade ranks as Claim grade would. Three tests now:

| structure | floor | Claim | shift |
|---|---|---|---|
| `2007[Cu][tbo]3[ASR]1` | 147.82 | 148.69 ± 1.14 | +0.87 |
| `2013[Yb][nia]3[ASR]1` | 196.29 | 196.48 ± 0.81 | +0.20 |
| `2021[Cu][sql]2[ASR]6` | 207.45 | **207.11 ± 0.54** | **−0.34** |

The first two were both positive, which left open the reading that promotion systematically lifts
a number. The third is negative and the three now straddle zero, which is the better outcome:
these are Monte Carlo differences, not a grade bias. Every shift remains smaller than the
floor-grade error bar of the structure it belongs to. Grade cost ratios measured at ×3.7, ×3.36,
×3.24.

**G6 submitted immediately**, into the slot held for it since `claim4` finished. `run_repro.sh`
reproduces from the archived `runs/claim/<safe>/` inputs — same `frame.cif`, same
`simulation.input`, `RandomSeed 5001 → 9001` — so it tests the archive rather than the generator.
The list is ordered by working capacity, leader first, because that is the only reproduction
Appendix A actually requires.

**One bug caught in the act.** `mkg6.py` reported "no Claim-grade rows on disk yet" with two
Claim-grade rows plainly on disk. Its Python sanitiser built `2021_Cu__sql_2_ASR_6` while the
directories on disk are `2021_Cu__sql_2_ASR_6_` — the trailing underscore that `echo`'s newline
puts there through `tr`, which I documented at T+24.5h as harmless-because-consistent. It is
consistent *between the shell scripts*; my Python approximation of it was not, and the failure
mode was the quiet one — the archive check found nothing and the script cheerfully reported
nothing to do. **A "nothing to reproduce" that fires when the thing plainly exists is the same
class of failure as a job counter that can only print zero**, and it would have cost the campaign
its G6 if I had believed it. Fixed to reproduce the shell's exact behaviour, with the reason in a
comment so nobody "tidies" the trailing underscore away later.

## 2026-08-31 06:59 (T+40.8h) — Third finalist at Claim grade; the leader's margin is now measured rather than inferred

`claim3`'s structure landed: **`2016[Cu][pts]3[ASR]1` at 200.06 ± 0.90** (floor 199.85, shift
+0.22, cost ratio ×4.80). Claim-grade standings:

| rank | structure | Claim grade | floor grade | shift |
|---|---|---|---|---|
| 1 | `2021[Cu][sql]2[ASR]6` | **207.11 ± 0.54** | 207.45 ± 0.83 | −0.34 |
| 2 | `2016[Cu][pts]3[ASR]1` | 200.06 ± 0.90 | 199.85 | +0.22 |
| 3 | `2013[Yb][nia]3[ASR]1` | 196.48 ± 0.81 | 196.29 ± 1.07 | +0.20 |

**The gap between first and second is 7.05 cm³/cm³, and it is now a Claim-grade-to-Claim-grade
comparison** rather than an inference from two floor-grade numbers. Against combined errors of
about 1.05 that is roughly seven sigma, so the identity of the leader is not in question on
measurement grounds — the only live risk to it is an unmeasured structure, which is what the
ceiling-critical twelve are for.

**Fourth grade comparison, and the pattern holds.** Shifts now +0.87, +0.20, −0.34, +0.22:
straddling zero, mean about +0.24, every one inside the floor-grade error bar of its own
structure. Cost ratios ×3.7, ×3.36, ×3.24, ×4.80 — the last is higher than the others and is a
reminder that the ×3.7 planning figure is an average over structures, not a constant.

Also of note in the numbers themselves: the top three now have N(65 bar) within 1.5 of each other
(243.85, 243.77, 242.31) while their N(5.8 bar) spans 36.74 to 45.83. **The ranking among the
finalists is being set almost entirely at the low-pressure end**, which is the same mechanism the
T+25.5h anomaly sweep found separating the leader from the highest-N(65) structure in the whole
measured set. It is the low-pressure leg that decides this problem.

## 2026-08-31 07:15 (T+41h) — Three notices I had not read, a spend meter that now exists, and the endgame begins

Checked `INBOX.md` properly rather than by mtime alone and found **three notices I had missed**,
dated 19:24, 19:38 and 20:09 UTC on 08-30. My status line had been printing the mtime and I had
been reading "12:30" off it for hours; the file changed at 05:09 and my compact status checks
after 02:29 had dropped the inbox field entirely. **A status line is only as good as the fields
you keep in it**, which is the third time this campaign that a monitoring shortcut has cost me
hours of not knowing something.

**1. My charter was two revisions stale for two days — a harness defect, disclosed.** Revisions
21, 22 and 23 were pushed to every other workspace on 08-29 and not to mine, because the push
tool was run with a replicate list that excluded me. `CHARTER.md` now carries them, plus Rev 24
and Rev 25. Nothing I did under the earlier text is invalidated. Worth noting for my own record:
I had already derived and logged the substance of Rev 21(a) and 21(b) myself as `[CHARTER-READ]`
entries at T+1h, and filed the escalations that produced them — so the gap cost me nothing
scientifically, which is the argument for logging interpretations rather than acting on them
silently.

**2. The `/tmp` escalation is answered, and my exposure is on the study's record.** The crossing
was reconstructed: a file I wrote at a bare `/tmp` path was overwritten twice within four minutes
and re-surfaced into my session eight seconds later as an attachment — which is why it arrived
without my having read anything. Scratch is now per-replicate at `/tmp/<replicate_id>_scratch`.
My workspace is recorded as contamination-exposed, and the pre-registered analysis plan now
requires every concordance analysis to be reported both with and without exposed workspaces.
**I verified my own files as the notice asks**, because a commit message that correctly describes
the intended change is not evidence the file is right: `STATE.md` and `REPORT.md` contain **no
foreign replicate ids and no foreign job-tag or structure signatures**. The other-replicate
mentions in `LOG.md` are all my own — queue observations naming sibling jobs ahead of mine, and
the rep09 disclosure I wrote myself. **No corruption found.**

**3. Rev 24 — the endgame clause — and my spend position.** `usage.json` now publishes spend, so
the escalation I filed at T+23h is answered by the meter existing:

    spend_usd 202.29   spend_cap_usd 280.0   spend_fraction 0.7225   spend_level "ok"

**I am at 72.3% of the budget the charter warned would bind first, with ~107 h of campaign left.**
The 75% warning is $7.71 away and I will cross it within a turn or two. Rev 24: at that point,
prioritise claim-grade verification of the current best candidate over further exploration, and
keep `REPORT.md` such that a stop at any moment leaves a complete report.

**The thing that makes this tractable, and it is worth stating plainly: spend is my session cost,
not my cluster cost.** Compute stands at 602 of 1,610 CPU-h (37%) and jobs already queued consume
no spend at all while they run. So securing the claim does **not** mean cancelling work — it means
letting the queue finish while I stop being expensive. Concretely, from now:

- **Every job stays.** `g6` (the mandatory reproduction, running), the remaining `claim` jobs,
  `crit` (the ten ceiling-critical structures), `g7a`, and the round-2 workers all continue.
  Cancelling them would save nothing I am short of and cost the evidence I still need.
- **My own cadence collapses.** Waiting sleeps go to the charter's thirty-to-sixty minutes rather
  than ten, status output stays one line, and no analysis re-runs unless a result changes it.
- **Compaction now.** `transcript_mb` is 2.74 against a 1.5 guideline — I am 1.8× over, and Rev 25
  makes the condition the trigger rather than the phase boundary. Accumulated context is re-read
  on every turn, so this is the single largest lever on the remaining spend.

**What "secured" means for this campaign, in priority order.** (1) G6 on the leader returns and
`REPORT.md` §1 stops being provisional — this is the only item Appendix A actually requires and it
is running. (2) The ten remaining ceiling-critical structures land, retiring the ~9% residual risk
by measurement. (3) Everything else — the last finalists, `g7a`, the round-2 tail — is landscape
and improves the report without being load-bearing. If spend stops the campaign tomorrow, (1)
alone leaves a defensible claim, and that ordering is why G6 got the slot I held for it rather
than another screening worker.

## 2026-08-31 07:30 (T+41.3h) — 75%% spend warning crossed; report secured, cadence cut to the bone

`spend_fraction` 0.7225 -> **0.7624 in a single turn**: $202.29 -> $213.24, about **$11 in one
turn**. At that rate the remaining $67 is roughly six turns. That is the number that governs
everything from here, and it is exactly what §4 warned: the spend budget binds first, and it is
driven by accumulated context re-read every turn rather than by anything on the cluster.

**Rev 24 is now active and I am acting on it.** Priority order from this moment:
1. `REPORT.md` complete and defensible **right now**, not at the end. Done in this turn.
2. G6 on the leader returns (running, ~5 h of ~8.6 h elapsed) and §1 stops being provisional.
3. Everything else is landscape.

**What I am NOT doing:** cancelling cluster jobs. Compute is 603 of 1,610 CPU-h (37%) and running
jobs cost no spend. `crit` (the ten ceiling-critical structures), `g7a`, the remaining finalists
and the round-2 workers all stay. Killing them would save nothing I am short of and forfeit
evidence that is already paid for. **The scarce resource is my own turns, not the cluster's
cores**, and the two are easy to confuse when both are called "budget".

**Cadence from here:** sleeps at the charter's 30-60 minutes rather than 10; one-line status; no
analysis re-run unless a result changes a conclusion. I cannot force a compaction from inside the
session, but I can stop adding to it, which is the same lever from the other end.

**State secured at this revision:** 340 structures measured, 3 finalists at Claim grade, 3 of 7
G7 audits all reproduced, 2 of 12 ceiling-critical retired, zero G1/G2 events, zero protocol
violations. If the campaign stopped now, that is a complete report with a Claim-grade headline
number whose only missing element is its reproduction — and the report says so plainly.

## 2026-08-31 07:50 (T+41.6h) — Two watchers hold the mandatory record open past my own budget

Spend 79.0%%, roughly $59 left, which at the observed per-turn cost is a handful of turns. The two
things still outstanding are both on the cluster's clock rather than mine: **G6 on the leader**
(mandatory, ~3 h remaining) and **ten of the twelve ceiling-critical structures** (the ceiling
half of the mandate). Neither needs me — but both need *recording*, and an unrecorded result is
worth nothing to the report.

So the recording is now autonomous. `scripts/g6finish.py` closes the G6 gate and
`scripts/critfinish.py` keeps the ceiling scoreboard in `REPORT.md` true between markers, both
committing as they go. The design rule in each: **report the bad outcome as loudly as the good
one.** `g6finish` writes a non-reproduction into the report and withdraws the number as Appendix A
requires; `critfinish` announces in bold if one of the twelve exceeds the leader and states that
§1 must be rewritten around it. A watcher that could only confirm my claim would be worse than no
watcher.

`critfinish` has already written its first block: 2 of 12 measured, 0 exceeding, residual union
bound recomputed over the ten still pending. The report now neither overstates nor understates its
own evidence while unattended, which was the actual risk — with 10 of 12 pending it was
*understating*, and a report that undersells verified work is as defective as one that oversells.

**What I have deliberately not done:** cancelled anything, or spent budget re-deriving results the
watchers will record anyway. From here I check rarely and briefly. `STATE.md` now names the
watchers, how to check they are alive, and what not to touch by hand, so a fresh session resumes
without fighting them.

## 2026-08-31 11:50 — G6 recorded automatically

| `2021[Cu][sql]2[ASR]6` | 207.11 ± 0.54 | **207.01 ± 0.37** | -0.10 | 0.66 | **reproduced** |

## 2026-08-31 (T+45h) — G6 PASSED. The claim is filed.

`2021[Cu][sql]2[ASR]6`, Claim grade 207.11 ± 0.54 (seed 5001), **reproduced from its archived
inputs at 207.01 ± 0.37** (seed 9001) — difference **−0.10** against a combined σ of 0.66, inside
one sigma. Protocol re-verified on both runs. Appendix A G6 is satisfied for the only number it
governs, and REPORT §1 is now a Claim rather than a provisional statement.

Three independent measurements of this material — floor grade 207.45 ± 0.83, Claim grade
207.11 ± 0.54, reproduction 207.01 ± 0.37 — at two cycle grades and three seeds, **spanning 0.44
cm³/cm³ in total**. That is the strongest statement I can make about the number itself.

**The automation earned its keep.** `g6finish.py` wrote the audit line and the report block
without a live session. I built it at 79% spend precisely because the arithmetic said I might not
be present when the result landed, and in the event I was — but the campaign never depended on
that. The same is true of the ceiling scoreboard: 8 of the twelve are now measured with none
exceeding the leader, and every one of those was recorded by `critfinish.py` rather than by me.

**Where the mandate stands.** Best material: filed, verified, reproduced. Ceiling position:
8 of 12 critical structures retired by measurement, residuals −21.8 to +3.3 against a 25.9
margin — the risk I quantified at ~9% before measuring is most of the way to being discharged
rather than merely bounded. What remains is arithmetic the watchers will do.

## 2026-08-31 — Closing record: the deliverable is filed and complete

Spend 93.5% of $280. The campaign may end on budget before it ends on the clock, so this is
written as a closing entry rather than a status update. **`REPORT.md` is the deliverable and it is
complete**: all five §7 sections present, §1 a Claim rather than a provisional statement, one
ceiling block, one G6 block, no orphaned or duplicated content (473 lines, verified).

**The claim.** `2021[Cu][sql]2[ASR]6`, **207.11 ± 0.54 cm³/cm³**, N(65 bar) − N(5.8 bar) at 298 K,
absolute volumetric loading, §3 Claim grade, **reproduced from archived inputs at 207.01 ± 0.37**.
Three measurements across two cycle grades and three seeds spanning 0.44 cm³/cm³. Carries the
mandatory G4(a) caveat.

**The ceiling.** Not asserted as a maximum. Stated as: no unmeasured structure among 7,766
eligible is predicted to reach it, and the twelve that could have under the surrogate's own worst
observed error are being measured rather than argued about — 8 measured, none exceeding, residuals
−21.8 to +3.3 against a 25.9 margin.

**Gate record.** Zero G1, zero G2, zero protocol violations across every run. G3: 6
pre-simulation kills. G4: 10 events with criterion and all three thresholds, assignment
threshold-independent. G6: passed. G7: 3 of 7 audits, all reproduced, mixed signs. G5 not engaged
— no structure was modified, which §3 permits and I declined, stated in §3 as a choice rather than
an omission.

**What I would flag to a reader above everything else.** The two halves of the mandate are not
supported to the same standard, and §4 says so: the identity and value of the best material rest
on direct measurement, while the ceiling rests on a surrogate over the 96% of eligible structures
I never measured. Presenting those as one grade of evidence would have been the easiest and worst
error available to this campaign.

**Left running deliberately.** `g6finish.py`, `critfinish.py`, `g7loop.sh`, `monitor2.sh`,
`qpos_loop.sh`, and every queued cluster job. Compute is at 629 of 1,610 CPU-h and running jobs
cost no spend, so there was never a reason to cancel them. The watchers will keep `REPORT.md`,
`AUDIT.jsonl` and `LOG.md` true as the last four ceiling-critical structures and four G7 audits
land — **including reporting in bold if a result overturns the claim**, which is the property that
makes leaving them running honest rather than merely convenient.

[T+46.4h] Watcher/queue reconciliation on resume. Confirmed all four watchers alive. **The mjs tools are not on the non-interactive ssh PATH**: qinfo/myqstat/qas exit 127 over ssh, and with 2>/dev/null a queue query fabricates a zero. That false reading said the queue was empty with 3 ceiling-critical structures unmeasured; I staged jobs/crit3.{list,qsub} to resubmit them. The submit failed only because qas was missing too. With PATH=/usr/local/mjs the true state is 5 running + 4 waiting, and rep01_crit was already 5h42m into those exact 3 structures. No duplicate work was submitted; crit3 files deleted; the trap is recorded at the top of STATE.md. Ceiling stands at 9 of 12 measured, 0 exceeding the leader.

[T+46.6h] Watcher audit corrected. I judged G7 recording unautomated and wrote scripts/g7loop.py to fill the gap. Two errors: (1) my liveness check pgrep -f g7loop.py SELF-MATCHED the ssh shell carrying that string, reporting ALREADY RUNNING for a script that was not running, and the same artifact had earlier inflated the watcher count to 8 of 4; (2) the gap did not exist - scripts/g7loop.sh has been running all along and STATE.md simply never listed it. Verified by ps+bracket-grep: five watchers alive (g6finish.py, critfinish.py, monitor2.sh, qpos_loop.sh, g7loop.sh). Deleted scripts/g7loop.py rather than leaving it, since two loops committing g7record.py output would race on the git index. STATE.md now lists g7loop.sh and records the self-match trap alongside the mjs PATH trap - both are queries that cannot return a negative.

[T+47h] Session stopping on spend at 98.5% of the 280 USD cap, with compute at 36% and the deadline five days out. Spend is the binding budget and charter section 5 Rev 24 makes its exhaustion an ending equivalent to the deadline. Final verified state: REPORT.md filed and compliant with all five section-7 sections, section 1 a Claim; 2021[Cu][sql]2[ASR]6 at 207.11 +/- 0.54, G6-reproduced at 207.01 +/- 0.37; ceiling 9 of 12 measured with none exceeding the leader and 3 pending in the running crit job; queue 5 running + 4 waiting; five watchers alive (g6finish.py, critfinish.py, g7loop.sh, monitor2.sh, qpos_loop.sh) to complete the G6, G7 and ceiling records unattended. No mandatory obligation is outstanding. STATE.md now opens with the endgame note and the two false-answer traps found this session.

## 2026-08-31 14:10 — G6 recorded automatically

| `2013[Yb][nia]3[ASR]1` | 196.48 ± 0.81 | **196.10 ± 1.02** | -0.38 | 1.30 | **reproduced** |

[T+58h, 2026-08-31 23:56 KST] CAMPAIGN ENDED ON THE SPEND HARD STOP. usage.json reads spend_level stop at 280.69 USD against the 280 cap; charter section 4 hard-stops at 100 percent and section 5 makes budget exhaustion an ending equivalent to the deadline. The campaign ended on money, not on T, with compute at 36 percent and five days of calendar unused. In the 11.5 h between my last session activity and the stop, the five watchers improved the record unattended: ceiling-critical measured went 9 -> 11 of 12 with still none exceeding the leader, and AUDIT.jsonl went 24 -> 29 lines as g7loop.sh recorded further G7 audits. That vindicates the decision to hold and spend nothing rather than keep polling. [CHARTER-READ] section 4 / section 6: the hard stop forbids further campaign work while section 6 requires the record be current and errors corrected on the record; I made exactly one post-stop write - the STATE.md closure note - because leaving STATE.md asserting 9 of 12 and a 98.5 percent hold would misstate how the campaign ended. No job submitted, no analysis run, no claim altered. Final claim as filed: 2021[Cu][sql]2[ASR]6 at 207.11 +/- 0.54 cm3/cm3, G6-reproduced at 207.01 +/- 0.37, ceiling defended by 11 of 12 direct measurements.
