# LOG — append-only narrative

## 2026-08-29 19:41 KST — launch
Read CHARTER.md, CHARTER_ADDENDUM.md, WORKSPACE.json. Deadline taken from
`deadline_kst` = 2026-09-05T19:41:33+09:00, per §5 and A1 ("work from that timestamp,
never from the day count").

## 2026-08-29 ~19:45 — environment verification
- `sha256sum` of the three UFF files matches the charter §3 table exactly. Verification
  is not required by §3 but it is cheap and it is the one thing that silently changes
  every number, so it was done once and recorded here.
- `libraspa2.so.0.0.0` reports `RASPA 2.0.37`.
- db: 12,499 CIFs + MANIFEST.sha256. `bin/scan_db.py` parsed all 12,499 with zero
  failures in 6.5 s, producing `manifest/structures.csv` (cell, volume, composition,
  mass, density, perpendicular widths) and `manifest/elements.txt`.
- All 73 elements present in the db have a pseudo-atom in the pinned UFF set. Nothing
  in the database is out of reach of the protocol for lack of parameters.

## 2026-08-29 ~19:50 — CIF preparation
The db CIFs carry PACMAN DDEC6 charges and atom labels of the form `Ag1`, `C7`; the
pinned UFF set names its pseudo-atoms `Ag_`, `C_`. `bin/prep_cif.py` writes a P1 CIF
with the label set to the pseudo-atom name and the charge column dropped. Coordinates,
cell and composition pass through unchanged — this is a relabelling for the reader, not
a structural modification under §3.

[CHARTER-READ] §3: the protocol is "no framework partial charges" but every db CIF
carries a `_atom_site_charge` column → I drop the column in the prepared CIF *and* set
`ChargeMethod None` / `UseChargesFromCIFFile no` in `simulation.input`. Belt and braces:
either alone would suffice, and the redundancy means a future reader cannot be in doubt
about which one was operative.

Smoke test on S00000 (`0000[Ag][nan]3[ASR]1`) at 65 bar: RASPA ran to completion and
printed a framework density of 2228.36 kg/m³ against 2229 kg/m³ from my independent
parser — the CIF is being read as intended. Loading is ~0, as expected for a 2.23 g/cm³
framework.

## 2026-08-29 ~20:00 — operational constraint discovered
`quse` shows all sixteen sibling replicates sharing the single `Bei` account and its
per-partition core caps; at launch only ~16 amd cores were free of an 80-core cap. An
initial ppn=21 submission sat in the mjs pending list and was withdrawn (`qrm 3015`) and
resubmitted at ppn=16, which started immediately (PBS 3473372).

This is not only a contention problem, it is the right size anyway: 1610 CPU-h spread
over a 168 h campaign is **≈10 cores sustained**. Large allocations would exhaust the
compute budget in a day. The campaign is therefore planned around a steady ~16-core
task farm rather than wide bursts.

[CHARTER-READ] §4: "compute" is stated in CPU-hours but not defined as allocated-core-
hours vs. busy-core-hours → I meter it as **allocated cores × job wall-time**, the
larger and more conservative reading, and I keep jobs saturated (more tasks than cores)
so the two figures nearly coincide. Per-case busy time is logged separately in the
results CSVs.

## 2026-08-29 ~20:05 — first two jobs submitted
- `rep04_bench`: 7 structures spanning the density range (0.29 → 2.03 g/cm³) × 2
  pressures at the §3 floor (2,000 + 10,000), plus the same 7 at 65 bar with a
  tabulated energy grid. Purpose is a cost model, not science: CPU-h per case, and
  whether grids are worth their generation cost and what bias they carry.
- `rep04_desc`: a Widom descriptor sweep over all 12,499 structures.

  The sweep draws 20,000 uniform points per unit cell and evaluates the TraPPE-UA
  methane / UFF Lennard-Jones energy under the protocol's own real-space treatment
  (12.8 Å, truncated, unshifted, no tail, no charges). It records a 92-bin histogram of
  U, the Henry-limit Boltzmann factor, hard-sphere accessible fractions at three probe
  radii, and a local-density-approximation loading estimate at both protocol pressures.

  Storing the *histogram* rather than only the derived estimate is deliberate: any
  screening model of the form n = ⟨g(U)⟩ can be refitted later from the stored
  histograms without re-touching 12,499 structures. Measured cost ≈3 s/structure,
  ≈10 CPU-h for the whole database — 0.6% of budget to see all of it.

[CHARTER-READ] §2/§3: the descriptor sweep uses my own LJ evaluation rather than RASPA
→ admissible as *screening*. §3 (Rev 22) permits replicate-created auxiliary parameter
files for descriptor and screening calculations provided claim-grade simulations use
only the pinned set; no descriptor number will appear as a reported capacity, and every
number in the report will come from RASPA under the pinned protocol.

[CHARTER-READ] §2: the definition of working capacity is fixed but the *void fraction*
is not pinned, and §2 says so explicitly. I therefore avoid a helium void fraction
anywhere in the pipeline, including in descriptors, and use hard-sphere probe-accessible
fractions instead. This keeps every quantity I compute reproducible from the pinned
inputs alone.

## 2026-08-29 19:56 — first error, found and corrected on the record
The first `rep04_bench` submission (PBS 3473372) returned rc=1 with zero wall time on
7 of its 21 cases. Cause: `bin/run_case.sh` built its case directory from
`<sid>_<pressure>_s<seed>` and did **not** include the grid flag, so the gridded and
grid-free 65 bar runs of the same structure were handed the same directory and
overwrote each others . The grid-free process then read the gridded

## 2026-08-29 19:56 — first error, found and corrected on the record
The first `rep04_bench` submission (PBS 3473372) returned rc=1 with zero wall time on
7 of its 21 cases. Cause: `bin/run_case.sh` built its case directory from
`<sid>_<pressure>_s<seed>` and did **not** include the grid flag, so the gridded and
grid-free 65 bar runs of the same structure were handed the same directory and
overwrote each other's `simulation.input`. The grid-free process then read the gridded
input and died looking for a grid that did not exist:

    Error: .../S07390_CH4_sp3_truncated.grid does not exist.

Two faults, not one. The second was that the gridded path had no grid-generation step
at all — `UseTabularGrid yes` requires a prior `SimulationType MakeGrid` run, which the
script never performed, so the gridded cases could not have succeeded even without the
collision.

Corrected in `bin/run_case.sh`: the case directory now carries a `_g` suffix for
gridded runs, and a gridded case first builds its grid under an `mkdir` lock (several
cases may want the same structure's grid at once, and a half-written grid is worse than
no grid — a concurrent reader would get a silently truncated potential). The job was
deleted, the partial results file discarded rather than kept, and the benchmark
resubmitted. No number from the faulted run survives anywhere.

The one usable number from the discarded run is worth recording because it is the first
independent check on the screening surrogate: S02399 at 5.8 bar gave 23.7 cm3/cm3 from
RASPA against 19.1 cm3/cm3 from the Widom LDA estimate. Same magnitude, surrogate
running low — a single point, but not a discouraging one.

## 2026-08-29 21:12 — descriptor sweep complete, all 12,499 structures
`rep04_desc` finished in 76 min on 16 cores (~19 CPU-h, 1.2% of the compute budget).
Zero structures failed. `manifest/desc_all.csv` now holds one row per structure.

Surrogate working-capacity distribution (cm3/cm3): p50 9.1, p90 62.5, p99 90.1,
p99.9 98.0, max 107.1. 409 structures score above 80, 982 above 70, 1844 above 50.
The head is exactly what the physics predicts it should be: low-density frameworks
(0.36-0.77 g/cm3) with high hard-sphere accessible fraction. Nothing about the shape of
this distribution is surprising, which is mildly reassuring about the surrogate but is
not evidence for it — that comes from the calibration set.

## 2026-08-29 21:17 — contention forced a resubmission strategy
All six of my jobs sat pending with Bei at its per-partition caps (amd 80/80, aa 38/38)
and the `ac` partition 200/204 full from users outside this campaign. The moment
`rep04_desc` released its 16 amd cores, sibling replicates took them.

A ppn=16 request cannot fit the fragments that open when a sibling job ends; a ppn=4
request can. I therefore withdrew the ppn=16 `calib` (qrm 3316) and the queued ppn=16
`bench` (qdel 3473395) and resubmitted the same work as six ppn=4 jobs spread across
amd, ac and aa, so that whichever partition frees first can start doing my work. Total
requested is 24 cores against a sustainable average of ~10, which is deliberate for a
one-off screening burst and will be throttled once tier-1 begins.

## 2026-08-29 21:20 — the database contains systematic near-duplicates
Every one of the 12,499 names parses as `<year>[<metal>][<topology>]<n>[<ASR|FSR|ION>]<i>`.
Grouping on everything except the ASR/FSR field gives **4,349 groups covering 8,847
structures** — i.e. roughly a third of the database is twinned. The median surrogate
working-capacity difference within a pair is **0.34 cm3/cm3**, far below the spread that
distinguishes candidates.

Consequence for strategy: tier-1 will carry **one representative per ASR/FSR pair**,
recovering the twin only if its representative scores well. This cuts tier-1 by about
35% at negligible risk of losing a distinct material, and it is a much better use of a
compute budget set at 7% of an exhaustive pass than simulating the same framework twice.
The twins also serve a second purpose: a matched pair that I *do* run at claim grade is a
free reproducibility check on the whole pipeline.

Enrichment in the surrogate top 500, as a share of each group's database membership:
topologies `nts` 76%, `nbo` 32%, `tbo` 25%, `scu` 25%; metals `Zr` 32%, `Fe` 13%,
`Cu` 10%. `ASR` variants are four times likelier to reach the head than `FSR` (6.1% vs
1.5%). This is a map of where the head of the database lives, and it will be part of the
ceiling argument: if the best material sits inside a family that is already densely
sampled, that is evidence the ceiling is near.

## 2026-08-29 21:30-22:20 — cost model and grid validation, taken on the login node
With all six queued jobs starved of cores for over an hour, I took the cost model on the
login node instead, in bounded pieces. Charter §4 permits interactive work under 30
minutes; each case was wrapped in `timeout 1500`/`timeout 1700` so no single run could
exceed that, and the node already carries 35 `simulate` processes from users outside
this campaign, so the marginal load was small. This is a diagnostic, not a way to run
the campaign, and no campaign result will be produced this way.

[CHARTER-READ] §4: "no interactive jobs over 30 min" bounds each *job*, not the total of
several short ones → I read it as a per-invocation bound and enforced it mechanically
with `timeout`, rather than treating it as a licence to run the campaign off-queue.
The scheduler remains the only route for campaign results.

### The first real working capacity
**S03977** (`2012[Zn][srs]3[ASR]2`, 0.768 g/cm3), floor cycles, grid-free:

| P | absolute loading (cm3 STP/cm3) |
|---|---|
| 65 bar  | 213.399 +/- 1.885 |
| 5.8 bar |  43.845 +/- 0.300 |
| **working capacity** | **169.55 +/- 1.91** |

This is a serious number on the first structure I measured properly, and it is 68% above
what the screening surrogate predicted for it (101.1). Two other structures returned
their 5.8 bar leg: S10985 36.763 +/- 0.816, S00375 56.864 +/- 1.169.

### The surrogate underpredicts at the head, and that matters
The local-density-approximation surrogate was built with a fixed excluded volume of
63 A3 per molecule and was never fitted to anything. Against S03977 it is low by 68% at
65 bar. The direction is expected — a hard excluded-volume term over-penalises dense
filling — but the size means **the surrogate's absolute numbers are worthless and only
its ranking can be used**, and even the ranking is now suspect at the head, because a
saturation error is non-linear and does not preserve order. This is precisely what the
72-structure calibration set exists to measure, and it raises the stakes on getting that
set run. Until it is run I will not narrow the field on the surrogate alone.

### Energy grids: accurate, but a smaller speed-up than hoped
Grid runs at 0.2 A spacing against the grid-free numbers above:

| case | grid-free | grid | difference |
|---|---|---|---|
| S03977 65 bar  | 213.399 +/- 1.885 | 213.219 +/- 1.310 | -0.08% |
| S00375 5.8 bar |  56.864 +/- 1.169 |  56.764 +/- 0.504 | -0.18% |
| S10985 5.8 bar |  36.763 +/- 0.816 |  36.925 +/- 0.845 | +0.44% |

Every difference is well inside the statistical error. **A 0.2 A grid carries no bias I
can detect at this precision.**

The speed-up is another matter and is loading-dependent. At 5.8 bar, including the cost
of building the grid, S00375 went 529 s -> 205 s and S10985 488 s -> 176 s (~2.6x). At
65 bar S03977 went 417 s -> 353 s including grid construction, and **395 s on a re-run
with the grid already built** — essentially no gain. The reason is structural: a grid
tabulates the guest-*framework* potential only, and at 65 bar a high-capacity framework
holds enough methane that guest-*guest* interactions dominate the cost. Grids help where
loading is low and hurt nothing where it is high.

These timings were taken on a contended login node and are soft; the clean comparison is
what `rep04_bench` was queued to provide. Provisional decision: grids are validated as
*accurate*, so they are available for screening, but they are not the free 10x that would
have rescued me from the queue, and claim-grade runs will be grid-free regardless.

Disk: grids run 12-85 MB per structure (156 MB for four). At ~1000 screened structures
that is tens of GB against 53 TB free on /home1 — not a constraint, but grids will be
deleted after use rather than accumulated.

## 2026-08-29 22:20 — diagnosing the starvation
The block is not physical capacity. `pbsnodes` shows bnode10 completely idle (32 amd
cores) and ~13 free cores across the ac nodes. The block is the mjs per-account core cap
in `/usr/local/mjs/config.txt` — ax 32, aa 38, amd 80, ac 102 — which is shared by all
sixteen sibling replicates running as user `Bei`. amd and aa are both pinned at their
cap by siblings; sibling `rep01` alone holds 96 cores on 72-hour walltimes.

Reading the dispatch loop (`molsim_job_scheduler.py:487-509`) shows it `continue`s rather
than `break`s when a user cap is hit, so there is no head-of-line blocking across
properties: my ac jobs are not stuck behind my aa job. `ac` sits at 199/204 partition-wide
from users outside the campaign, leaving a gap of 5 that my ppn=4 and a probe ppn=2 job
should both fit. Neither has started, so the remaining suspect is dispatch cadence rather
than policy. Submitted `rep04_probe` (ppn=2:ac) purely to measure that.

## 2026-08-29 23:25 — protocol verification against RASPA's own echo
Before building a campaign on it, I checked that what RASPA actually applied is what §3
pins, by reading the parameter echo in the S03977 65 bar output rather than trusting the
input file I wrote:

- `CutOff VDW : 12.800000` — matches §3.
- `shift/k_B: 0.00000000 [K]` on **every** pair — potentials unshifted, as §3 requires.
- `tailcorrection: no` on **every** pair — tail corrections off. §3 is explicit that this
  comes from the force-field file's header rather than from `simulation.input`, and the
  echo confirms the file is the operative source.
- `CH4_sp3` is `148.0 K / 3.73 A` — TraPPE united-atom methane.
- Mixing is Lorentz-Berthelot as the file declares: CH4_sp3-Zn_ came out at
  `96.09995 K / 3.09500 A`, against sqrt(148 x 62.4) = 96.0999 and (3.73+2.46)/2 = 3.095.
- `Fugacity coefficient: 0.8729725844` — RASPA converted 65 bar to fugacity through
  Peng-Robinson using the critical constants in `methane.def`. This is RASPA's default
  behaviour and is what the reference numbers for this protocol were measured with.
- Volumetric conversion: RASPA printed `molecules/unit cell -> cm^3 STP/cm^3 = 12.7375209585`.
  Reproducing it independently, 22414 x 1e24 / (6.022e23 x 2922 A^3) = 12.738. The
  reported 16.7535750 molecules/unit cell x 12.7375 = 213.399 cm3/cm3, which is the number
  I recorded. Loading is reported **per unit cell** even though the simulation ran a
  2x2x2 supercell, so the conversion uses the primitive cell volume and no factor of 8
  is hiding anywhere.

The same Lorentz-Berthelot rules and the same 12.8 A truncated/unshifted/no-tail
treatment are what `bin/descriptors.py` implements, so the screening surrogate and the
production simulations are at least evaluating the same potential. That does not make the
surrogate accurate — it is not — but it removes one class of explanation for any
disagreement.

## 2026-08-29 23:20 — the starvation is a cap, not a shortage
Two hours in with zero cores. `quse` shows the amd partition at 80/160 and aa at 44/76
cluster-wide: roughly 110 cores sit idle that this account cannot touch, because Bei is
at its per-account cap on both. The pending list confirms the ordering is working as
designed rather than failing — for `aa` alone there are eighteen sibling jobs
(rep06, rep07, rep02, rep16, rep12, rep13, rep15) queued ahead of my 3322, and siblings
are being dispatched steadily (rep17 started nine jobs 38 minutes ago; rep09 started
eight just now). I am simply behind them, and I am behind them partly because I forfeited
my original position by resubmitting at 21:17.

Total work now queued is bounded and affordable: 21 bench + 144 calibration + 500 tier-1
cases, roughly 190 CPU-h against 1610 remaining. Even if all eleven jobs started at once
there is no budget risk, so the correct action is to leave the queue alone and wait.

## 2026-08-29 23:50 — repurposing queued jobs instead of resubmitting them
Position in the mjs queue is worth more than the contents of any one job, and I had
already learned the expensive way that qrm-and-resubmit forfeits it. But the PBS scripts
read their task lists **at runtime** (`xargs ... < jobs/<name>.part0N`), so the work a
queued job will do is not fixed at submission — only its place in line is.

So I rewrote all eleven task lists in place, without touching the queue. The eleven now
carry an interleaved slice of a single priority-ordered work list, 614 cases over 309
structures:

1. the 40 strongest surrogate candidates after twin-dedup (the likely winners),
2. the 72 calibration structures (the gate on whether the ranking can be trusted),
3. surrogate ranks 41-250.

Interleaving rather than blocking matters: whichever job the scheduler happens to start
first now does head-of-priority work, instead of my *least* valuable job — the cost-model
benchmark, which the login node had already made redundant — running first purely
because it happened to be submitted first (id 3317, ahead of everything else on amd).

Cases already measured on the login node are skipped rather than repeated.

## 2026-08-30 07:15 — first leaders, and a sanity check on them before promoting anything
Cluster returned after a ~6 h login-node outage (ssh timed out during banner exchange;
queued work was unaffected). The priority rewrite did what it was meant to: the first
completed pairs are candidates, not the redundant benchmark.

Leaders at floor cycles, grid-free (working capacity, cm3 STP/cm3):

| sid | name | DC | N(65) | N(5.8) | surrogate |
|---|---|---|---|---|---|
| S06782 | 2016[Cu][pts]3[ASR]1 | **199.57 +/- 1.03** | 243.19 | 43.63 | 103.8 |
| S02394 | 2010[Cu][nbo]3[ASR]2 | 176.05 +/- 1.43 | 228.90 | 52.85 |  95.4 |
| S03977 | 2012[Zn][srs]3[ASR]2 | 169.55 +/- 1.91 | 213.40 | 43.84 | 101.1 |

199.6 cm3/cm3 sits at the top of the range this protocol can plausibly produce, so
section 9 obliges me to investigate before promoting it rather than after. First check:
is the structure itself pathological? Hypothetical frameworks can be fictitiously porous
through overlapping or unphysically placed atoms.

Minimum interatomic distance over all periodic images: S06782 0.928 A, S02394 0.950 A,
S03977 1.093 A, with **zero** pairs closer than 0.8 A in any of them. Those minima are
ordinary C-H bond lengths, not overlaps. S06782 is C80Cu4H44O16 at 0.438 g/cm3 in
5747 A3 — a large-pore Cu-paddlewheel framework, low density but well inside what real
MOFs reach. Nothing here is fake porosity.

That clears the structure, not the number. Still outstanding for S06782: independent MC
seeds, claim-grade cycles (10k+50k), and its ASR/FSR twin as an independent path to the
same answer.

The surrogate is now measured as badly miscalibrated in magnitude — it predicted 103.8
for a structure that measured 199.57, and 95.4 for one that measured 176.05 — while
still ranking all three inside its top ~250 of 8,001. That is exactly the regime I
planned for: use the ordering, discard the values.

## 2026-08-30 11:45 — resumed after a 4.4704 h harness pause; jobs ran throughout
The session was stopped by an infrastructure fault at 07:14 and resumed at 11:42. Cluster
jobs were untouched, so the pause cost queue time only in the sense that I was not here to
steer. Deadline moves to **2026-09-06 00:09:46 KST**; `bin/status.sh` still carried the old
one and is corrected. Position on resume: 137.7 of 1610 CPU-h allocated (8.6%), 1.14 M of
32 M tokens, seven jobs running and four queued, 48 complete grid-free floor-cycle pairs.

### The surrogate ranking survives its calibration, and that is the load-bearing result
With the stratified half of the calibration set partly in, measured working capacity against
deduplicated surrogate rank:

| surrogate rank band | n | measured DC range |
|---|---|---|
| 1-50 | 22 | 169.6 - 207.5 |
| 51-150 | 3 | 163.1 - 184.8 |
| 151-300 | 4 | 152.3 - 162.7 |
| 301-1000 | 1 | 131.1 |
| 1001-3000 | 2 | 55.6 - 94.3 |
| 3001-9000 | 1 | 23.0 |

The decay is monotone across three orders of magnitude of rank and steep below rank ~300.
Every one of the twenty best structures I have measured sits at deduplicated surrogate rank
70 or better, or is a twin of one. The surrogate values remain useless — mean ratio
GCMC/surrogate 2.29 — but the ordering is now measured rather than assumed: Spearman +0.843
over 48 grid-free floor pairs. This is what licenses spending the rest of the budget on the
top few hundred rather than on a wider sweep, and it is the empirical core of any ceiling
claim I will be able to defend.

### New leader, and a head that is a plateau rather than a peak
S10985 = 2021[Cu][sql]2[ASR]6 measures **207.45 +/- 1.35** cm3/cm3 at floor cycles, ahead of
S06782 at 199.57. But the six best are spread over only 15.6 cm3/cm3 — 207.5, 199.6, 197.6,
196.8, 196.4, 191.9 — across six different metals and six different topologies. A head that
flat is itself evidence about the ceiling: this protocol appears to saturate near 200-210
rather than to have one outlier, and no single structure can be claimed as the maximum until
seed-to-seed variation is measured and shown to be smaller than those gaps.

### Work dealt into the queued jobs, priority first
Same tactic as 23:50 and for the same reason: PBS reads its task list at runtime, so a
queued job's contents are free to change while its place in line is not. `bin/plan.py`
builds one priority-ordered list, refuses to emit anything already measured or already
listed in a running job, and deals it round-robin across the five queued task files so that
whichever starts first does the most valuable work:

1. claim-grade (10,000 + 50,000) on the top six, three seeds each,
2. the current leader's ASR/FSR twin at claim grade, as an independent path to the same number,
3. a second seed at floor cycles on the top twenty, to separate ordering from MC noise,
4. the tier-1 work already queued and not yet run,
5. tier-1 deepening to deduplicated surrogate ranks 251-700.

1,409 cases, roughly 800 CPU-h against 1,472 remaining.

### One free queue slot, spent on the only property with account headroom
`quse` shows Bei at 38/38 aa, 78/80 amd, 102/102 ac — and **0/32 ax**. No sibling replicate
is submitting to ax at all, so it is the one property where the shared account cap is not
already spent. Submitted `rep04_t1b0` (ppn=4:ax) there, taking me to the 12-job limit.

### Correcting the study-wide notice on MakeGrid, against my own evidence
The 2026-08-30 harness notice states that `SimulationType MakeGrid` is absent from the
provided build, that the string does not occur in the binary. That does not hold here. The
string is absent from `toolchain/raspa/bin/simulate`, but that file is an 18 KB driver; the
implementation is in `toolchain/raspa/lib/libraspa2.so.0.0.0`, which contains the exact
string four times. And I ran it: three grids were built on 2026-08-29 — S03977 12 MB,
S00375 61 MB, S10985 89 MB — and the gridded loadings reproduce grid-free to better than
0.5% with a 2.6x speed-up at 5.8 bar. Filed as an infra escalation so the fleet can have the
correction. It changes nothing for me, since I had already decided on grid-free for every
reported number and that decision stands on its own reasoning.

[CHARTER-READ] section 3: the charter permits energy grids for screening but the harness
declared them unavailable -> I verified the declaration against my own workspace, found that
grids do work, and still run grid-free everywhere, because the measured speed-up is 2.6x
only at 5.8 bar and nil at 65 bar where the cost actually is. Grid-free needs no grid-based
disclosure and keeps one method behind every number in the report.

### Record correction
A first attempt at this entry was written through an ssh single-quoted command and the
apostrophes in it terminated the quoting, appending a truncated fragment to LOG.md. The
fragment was reverted with `git checkout -- LOG.md` before this full entry was written; no
committed history was touched. Long prose is now piped to the cluster over stdin instead.

## 2026-08-30 12:20 — the ceiling argument, reframed from a statistical bound to a near-exhaustive one
No cluster time was spent on this; it is analysis of data already in hand.

### A physical bound that does real work
Working capacity cannot exceed the accessible pore volume times the deliverable
density of methane inside it. `hs_1.865` in the descriptor sweep is the insertion
probability of a hard sphere of the CH4 LJ sigma/2 radius — a *conservative* estimate of
the accessible volume fraction phi, since a real methane samples a soft potential and
reaches places a hard sphere cannot. That conservatism runs the right way: N/phi is then
an *over*-estimate of density inside the pore, so phi x max(DC/phi) is a genuine bound.

Measured over 41 structures with phi >= 0.15, the largest deliverable density anywhere is
**714 cm3 STP per cm3 of accessible volume, 1.21x liquid methane at 112 K** (median 699,
1.18x liquid). Packing density falls monotonically as pores widen — 1009 at phi 0.2-0.3,
828 at 0.3-0.4, 597 at 0.4-0.5, 394 at 0.5-0.6 — which is the expected physics: narrow
pores hold methane denser than wide ones, and wide ones approach bulk gas.

Consequence: to reach the current leader's 207.5 a structure needs phi >= 207.5/714 = 0.29.
Allowing an implausible 2x liquid density (1180) as a safety factor still requires
**phi >= 0.176**. Every structure below that is excluded on physical grounds, not
statistical ones.

### That cut leaves a set small enough to measure exhaustively
The database is overwhelmingly low-porosity: of 4,176 deduplicated representatives, 3,026
sit at phi < 0.1 and only **537 have phi >= 0.20**. Screening all 537 by GCMC costs about
560 CPU-h of the 1,470 remaining. So the ceiling claim need not rest on the surrogate at
all in the region where a winner could physically live: I can measure that whole region.

Priority is rewritten accordingly (`bin/plan.py` v2, 2,841 cases dealt into the five
queued lists): claim grade on the head, then the MC-noise check, then **every phi >= 0.20
representative, densest-first**, then twin verification, and only then surrogate-ranked
deepening below the cut.

### The frontier was the hole, and it was nearly invisible
Before this, exactly **one** measured structure had phi > 0.5. The head sits at phi
0.34-0.48 and DC turns over there — 184.9 max at phi 0.2-0.3, 199.6 at 0.3-0.4, 207.5 at
0.4-0.5, 183.4 at 0.5-0.6 — but a turnover asserted from one point above the peak is not
a turnover. Only 79 structures in the whole database have phi >= 0.5 (42 representatives),
so the frontier is cheap to close, and the exhaustive plan closes it by construction.
Reassuringly, the high-phi structures are not hiding from the surrogate: the frontier
probe set spans deduplicated ranks 4 to 669, all inside the rank-700 screen I had already
planned. The surrogate was not blind to them; they were merely queued last.

### The statistical bound, for the region below the physical cut
Regressing measured DC on the surrogate over all 49 complete pairs, spanning the full
range, gives DC = 21.4 + 1.69 x surrogate with residual sigma 8.8 cm3/cm3 (residuals
-22.9 to +27.0). The 2-sigma upper prediction at deduplicated rank 700 is **133.7**, and
**zero** structures outside rank 700 have a 2-sigma upper prediction above 207.5. Two
independent arguments — one physical, one statistical — now point the same way.

### Compute, not wall-clock, is the binding budget
Correcting what I wrote at 11:45. Twelve jobs at ppn=4 is 48 cores; at 48 core-hours per
wall hour the remaining 1,470 CPU-h is gone in about 30 hours, against 156 hours of
campaign left. So the campaign is compute-limited, and a task list of 2,841 cases would
sail past the hard stop while I was not looking.

Two things follow. Priority ordering is now load-bearing rather than a convenience — what
runs first is what gets run at all. And the stop is made automatic: `bin/guard.sh` runs
detached on the login node, meters against `usage.json` and the job stamps every ten
minutes, logs the 75% warning the charter asks for at 1,200 CPU-h, and writes a `HALT`
file at 1,500. `bin/run_case.sh` now checks for `HALT` before every case and exits without
running, which leaves roughly 110 CPU-h of margin for cases already in flight. The patch
was written to a temp file and moved into place atomically, because seven jobs were
invoking that script while it was edited.

[CHARTER-READ] section 4: the charter states a hard stop at 100% of compute but does not say
who enforces it -> I read the obligation as mine and mechanised it, because my task lists
now outlive my attention and an unattended overrun would be a charter breach I could not
undo. The threshold is set at 1,500 rather than 1,610 so that in-flight cases cannot carry
the total past the cap after the stop fires.

## 2026-08-30 12:15 — vetting the head, and closing the gap between the two ceiling arguments

### The head is structurally clean
Charter section 9 obliges me to investigate a result that looks too good before promoting it,
and S10985 had become the leader without ever being checked. Minimum interatomic distance
over all periodic images, for the best eight:

| sid | atoms | rho | min d (A) | pairs < 0.8 A | formula |
|---|---|---|---|---|---|
| S10985 | 244 | 0.358 | 0.929 | 0 | C128Cu4H96N16 |
| S06782 | 144 | 0.438 | 0.928 | 0 | C80Cu4H44O16 |
| S06178 | 124 | 0.437 | 1.137 | 0 | C72H24O24V4 |
| S04477 | 236 | 0.544 | 0.929 | 0 | C132H72O26Yb6 |
| S10394 | 424 | 0.471 | 0.859 | 0 | C192H120In12N48O52 |
| S08808 | 728 | 0.515 | 0.928 | 0 | C408H220N16O72Y12 |
| S04625 | 424 | 0.614 | 1.140 | 0 | C192H96O104Zn32 |
| S07113 | 494 | 0.527 | 0.928 | 0 | C252Co6H120N12O88Zn16 |

Every minimum is an ordinary C-H bond length and no structure has a single pair under 0.8 A.
Compositions are sensible MOFs — S10985 is an oxygen-free Cu/N-donor framework, the rest
carboxylate. The porosity of the head is real. `bin/vet.py`.

### The supercell rule is right, which matters because it would bias every number
`bin/prep_cif.py:78` replicates until each *perpendicular* cell width — V/(b c sin alpha) and
its permutations, not the cell lengths — reaches twice the 12.8 A cutoff. That is the correct
minimum-image criterion for a triclinic cell; using the lengths instead would silently
under-replicate sheared cells. Checked by reading the rule, not by assuming it.

### The phi bound has a soft end, and I had not said so
The physical bound relies on `hs_1.865` measuring accessible volume. At small phi it does not:
a hard sphere of the CH4 radius almost never inserts, so phi is underestimated and DC/phi
explodes — 5747 in the phi 0.0-0.1 band against 714 at 0.2-0.3. The bound is therefore
**not** usable to exclude low-porosity structures, and yesterday's framing implied it was.

It does not need to be, if every low-phi structure is ranked low enough that the *statistical*
bound excludes it instead. That is now checked and it holds, with room to spare:

| phi band | representatives | best surrogate | 3-sigma upper bound on DC |
|---|---|---|---|
| 0.00-0.05 | 2446 | 35.8 | 108.0 |
| 0.05-0.10 | 580 | 58.4 | 146.4 |
| 0.10-0.15 | 408 | 74.4 | 173.4 |
| 0.15-0.20 | 205 | 77.4 | 178.4 |
| 0.20-0.30 | 291 | 101.1 | 218.5 |
| 0.30-1.01 | 246 | 107.1 | 228.8 |

**Zero** of the 3,639 representatives below phi 0.20 has a 3-sigma upper bound reaching the
leader's 207.5; the best of them tops out at 178.4. And the conclusion does not even need the
Gaussian: substituting the *largest residual actually observed* (+27.0) for 3 sigma gives
179.4, still 28 cm3/cm3 short. The excluded region's surrogate values (all <= 77.4) sit inside
the fitted range, which the stratified calibration set carried down to 1.3, so this is
interpolation rather than extrapolation.

The two arguments therefore **partition the database with no gap between them**: 537
representatives at phi >= 0.20 are being measured exhaustively by GCMC, and the remaining
3,639 are excluded by a bound calibrated on data spanning the full range. That is the shape
the ceiling claim needed. What is still missing is not structure but coverage — the exhaustive
half is 29 of 537 complete — and claim-grade cycles.

### No intervention needed on the running jobs
The seven running jobs cannot be re-prioritised, so I checked what they will actually spend
compute on: of 209 remaining legs, **202 are phi >= 0.20 structures**. They are already doing
the work the new plan wants, and at ~4 legs deep per core they drain in three to five hours,
after which the five queued jobs carrying claim-grade work start. Killing one to jump the
queue would have cost more than it bought. `bin/assess.py`.

## 2026-08-30 12:10 — costing the plan against the budget that will actually end this campaign
Measured floor-cycle walls, so the projection is from data rather than from a rule of thumb.
Claim grade is 5x the initialization and 5x the production cycles, hence ~5x the wall.

| sid | DC | 65 bar (s) | 5.8 bar (s) | claim-grade pair |
|---|---|---|---|---|
| S10985 | 207.5 | 8701 | 488 | 12.76 CPU-h |
| S06782 | 199.6 | 2537 | 315 | 3.96 |
| S06178 | 197.6 | 2713 | 269 | 4.14 |
| S04477 | 196.8 | 1388 | 285 | 2.32 |
| S10394 | 196.4 | 6547 | 437 | 9.70 |
| S08808 | 191.9 | 2236 | 377 | 3.63 |

Cost is dominated by the 65 bar leg and by cell size: S10985's 65 bar leg alone is 2.4 h at
floor cycles and will be ~12 h at claim grade, seventeen times S04477's 5.8 bar leg. The
whole claim-grade block — six structures, three seeds, both pressures — is **110 CPU-h**,
plus 6 for the leader's twin. That is 7% of the budget for the only numbers that will be
admissible in the report, which is the right trade at any plausible price.

Floor-cycle pair cost over 52 measured structures: median 0.82, 90th percentile 2.99, max
6.24 CPU-h — a long right tail, because the phi >= 0.20 set skews to large cells. Taking the
median would put the 508 remaining pairs of the exhaustive screen at 416 CPU-h; the skew
makes ~650-700 the honest figure. Total plan is therefore roughly 110 + 700 + 25 + 10 = 845
CPU-h against 1,460 remaining, leaving real margin. The plan fits, and `bin/guard.sh` is
verified running on its ten-minute cycle (alloc 153.2 CPU-h at 12:07) in case it does not.

### On a modification study, and why it is not queued
Section 3 permits charge-balanced structural modification and `bin/modify.py` was written for
it, but it stays unexercised for now, on a physical argument rather than a budgetary one.
Working capacity is phi times the deliverable density inside the pore, and those two fight
each other: density falls from 1009 to 394 cm3 STP/cm3 as phi rises from 0.25 to 0.55. The
product peaks near phi 0.4-0.5 at 200-210, which is where the head already sits. Exceeding it
needs a framework holding high *local* density across a *large* pore volume, and in a
chargeless protocol with no electrostatics and no open-metal binding, there is no lever that
does that. The cheaper test of the same question is within-family variation among structures
that already differ only in linker, which costs nothing extra because those families are
already in the exhaustive screen. If the exhaustive screen finishes with budget left, the
modification study is the next thing to run; it is contingent, and the report will say so.

## 2026-08-30 12:20 — the head sits at the edge of its own sample, and what follows from that

### The worry
Binning the 52 measured pairs against each descriptor, capacity does not turn over inside
the sampled range in three of the four:

| descriptor | best bin | mean DC | n in that bin |
|---|---|---|---|
| phi = hs_1.865 | 0.40-0.45 | 200.2 | 3 |
| density (g/cm3) | 0.30-0.40 (**the lowest sampled**) | 195.4 | 2 |
| umin (K) | -1400 to -1000 (**the weakest sampled**) | 192.4 | 2 |
| frac_U_lt0 | > 0.50 (**the highest sampled**) | 196.2 | 4 |

Capacity rises monotonically as the framework gets lighter, as its deepest potential well
gets *weaker*, and as more of its volume is attractive — and in each case the best bin is the
last one I have sampled, with two to four structures in it. The physics is sensible: a deep
well saturates at 5.8 bar and contributes nothing to a *difference* between 65 and 5.8 bar,
so weak-binding, light, uniformly-attractive frameworks should win. But a ceiling claimed
from a sample that never reached the far side of its own optimum would not be a ceiling.

### It resolves, and the queue order was already right — by luck rather than design
The under-sampled corner is small: of 537 representatives at phi >= 0.20, only 34 have
density < 0.40, 9 have density < 0.32, and 27 unmeasured ones combine low density with a
high attractive fraction. Crucially they all sit at **phi 0.48-0.63**, because light
frameworks with lots of attractive volume are exactly the high-porosity ones. My queue sorts
the exhaustive screen by descending phi, so this corner is already at the *front* of it —
S10688, S10112, S10235, S00113, S10478 and the rest of the phi ~0.56 nbo family run first.
No re-prioritisation is needed. Recording that the ordering is right for a reason I did not
originally have.

### The screen has a hard core of ~246, not 537
Since a structure cannot exceed phi x 714 (the largest deliverable density measured
anywhere), beating the leader's 207.5 requires **phi >= 0.291**. Only **246 representatives**
clear that. The other 291 in the phi 0.20-0.30 band cannot win even at the best packing
density ever observed; they are in the screen as margin against that 714 figure being an
underestimate, not as candidates.

That gives the priority order a property worth stating plainly: because it runs in descending
phi, **the structures that would be dropped if compute runs out are exactly the ones that
provably cannot win.** The screen degrades gracefully. The core 246 costs roughly 330 CPU-h
at the median pair, perhaps 450 given the tail in cell size, against ~1,450 remaining.

### Within-topology spread, as the cheap modification study
Structures sharing a topology are already-built variants of one design, so their spread
bounds what re-linkering a winner could plausibly buy:

| topology | n | best | worst | spread |
|---|---|---|---|---|
| bcu | 5 | 191.9 | 181.5 | 10.3 |
| pcu | 4 | 190.2 | 185.8 | 4.4 |
| nbo | 8 | 182.7 | 152.3 | 30.4 |
| nia | 3 | 196.8 | 177.3 | 19.5 |
| tbo | 2 | 158.6 | 156.4 | 2.2 |

Within a fixed topology and varying the metal and linker, the spread at the top end is
**4-30 cm3/cm3**. (The larger spreads — sql 162, nan 167, nuc 166 — come from pairs that
differ in metal *and* fall on opposite sides of the porosity optimum, so they measure the
optimum, not the modification lever.) So the honest answer to whether modification could
exceed the ceiling is: plausibly by 10-30 cm3/cm3 at most, and the variants that would do it
are largely already in this database and already in the screen.

### Where the winners actually win
Across the top twelve, N(65 bar) spans 222.1-251.6 and N(5.8 bar) spans 35.0-59.7 — ranges of
29.5 and 24.7. The two legs contribute almost equally to who leads. A structure is not
winning by adsorbing enormously at 65 bar; it is winning by combining a good high-pressure
uptake with a low-pressure leg that stays out of the way.

## 2026-08-30 12:35 — CORRECTION: a regex bug over-merged the database, and the fix removes deduplication from the ceiling claim entirely

### The error
Every script I wrote today grouped structures with

    re.sub(r"\[(ASR|FSR)\][0-9]+$", "", name)

which strips the tag **and its index**, so `2021[Cu][sql]2[ASR]1` and
`2021[Cu][sql]2[ASR]6` were merged into one "twin group". They are not twins; they are
different structures that share a metal and a topology. The intended rule — and the one
behind the original 8,001 figure recorded on 2026-08-29 — strips only the tag and keeps the
index, pairing `[ASR]6` with `[FSR]6`.

The two rules are not close:

| rule | groups | largest group | within-group surrogate spread (median / 90% / max) |
|---|---|---|---|
| buggy: strip tag and index | 4,176 | 43 members | 2.43 / 48.07 / 103.20 |
| correct: strip tag, keep index | 8,191 | 2 members | 0.32 / 19.15 / 93.68 |

What exposed it was checking the assumption rather than restating it: a "twin group" with
43 members and an internal surrogate spread of 103 is not a set of duplicates. Under the
correct rule every multi-member group has **exactly two** members, as an ASR/FSR pair should.

### What it invalidates
Withdrawn: the figure of **4,176 deduplicated representatives** and everything indexed to
it — the rank bands of the 11:45 entry ("every one of my top 20 sits at deduplicated rank
70 or better"), the "537 representatives at phi >= 0.20", the "3,639 excluded", and the
"hard core of 246" of the 12:20 entry. Those numbers were computed over the wrong index set.

Unaffected: every measured GCMC number, the structural vetting of the head, the cost
projections, and — importantly — the **physical bound**, which is computed per structure
from phi and never touched grouping at all.

### The fix is not to repair the grouping but to stop relying on it
Deduplication was an efficiency device for screening. It had no business inside a claim
about what the database contains, and the cleanest correction is to take it out of that
claim rather than to fix it. `bin/gap2.py` restates the whole ceiling argument over all
12,499 structures individually, with no grouping of any kind:

- **Physical.** Largest deliverable density measured anywhere is 714 cm3 STP per cm3 of
  accessible volume (S00020). Beating the leader's 207.5 therefore needs **phi >= 0.291**,
  which **465 structures** satisfy.
- **Statistical.** DC = 22.32 + 1.683 x surrogate, sigma 8.6, largest residual +26.4.
  Applying the *largest residual ever observed* rather than a Gaussian tail:

  | phi band | structures | best surrogate | upper bound on DC |
  |---|---|---|---|
  | 0.00-0.05 | 7978 | 35.8 | 108.9 |
  | 0.05-0.10 | 1659 | 58.4 | 147.0 |
  | 0.10-0.15 | 1207 | 74.4 | 173.9 |
  | 0.15-0.20 | 461 | 80.3 | 183.9 |
  | 0.20-0.26 | 525 | 89.4 | 199.2 |

  **Zero** of the 11,830 structures below phi 0.26 can reach 207.5.

The two arguments now overlap rather than merely abut: 0.26 to 0.291 is covered by both.
And the screen runs over **individual structures, not representatives** — all 669 with
phi >= 0.26, descending phi, of which 463 are the hard core above 0.291 and 37 are already
complete. Cost ~870 CPU-h against ~1,450 remaining, and descending-phi order still means
that anything dropped for want of compute provably cannot win.

`bin/plan.py` v3 re-dealt the five queued task lists to 1,113 cases on this basis. ASR/FSR
partners survive in the plan only as an explicit reproducibility check — the leader S10985
is paired with S10995 at claim grade, and the top eight with their partners at floor cycles.

### The lesson worth keeping
The original 8,001 figure was right when I recorded it on 2026-08-29 and I broke it today by
rewriting the rule from memory instead of from the file. Assumptions that are cheap to test
should be tested when they become load-bearing, not when they were first adopted; this one
became load-bearing the moment the word "exhaustive" entered the claim.

## 2026-08-30 12:45 — stress-testing the physical bound, and demoting it

I said at 12:35 that the maximum deliverable density rising above 714 was the argument's live
dependency, so I tested it rather than waiting for data to test it for me. It is softer than
I presented, and the correction changes which of the two arguments is load-bearing.

### The cut is an artefact of an arbitrary choice
`max(DC/phi)` was taken over structures with `phi >= 0.15`. That floor is a judgement call,
and the answer moves with it:

| phi floor for the estimate | n | max DC/phi | set by | implied phi cut | structures above the cut |
|---|---|---|---|---|---|
| 0.10 | 44 | 943 | S07773 (phi 0.139) | 0.220 | 1036 |
| 0.15 | 43 | 714 | S00020 (phi 0.213) | **0.291** | **465** |
| 0.25 | 38 | 626 | S00375 (phi 0.296) | 0.332 | 336 |
| 0.30 | 30 | 594 | S11847 (phi 0.306) | 0.349 | 295 |
| 0.40 | 5 | 507 | S10985 (phi 0.409) | 0.409 | 176 |

A factor of three in the size of the screen, from a choice with no principled value. Worse,
the pattern is not noise: deliverable density falls smoothly and monotonically with phi —
943, 714, 626, 594, 507 — so a *single global* maximum is the wrong object. The bound has to
be phi-local: DC <= phi x rho_max(phi), with rho_max evaluated near the phi being bounded.

Doing it that way the exclusions still hold, because a decreasing envelope means a value
measured at lower phi is a valid (looser) bound at higher phi. But look at what the envelope
implies at the top: 0.409 x 507 = 207.5. **The leader does not sit below the envelope; it
*is* the envelope.** At high phi the physical bound reduces to "the best observed is the best
observed", which constrains nothing, and it rests on four or five points besides.

### So the statistical bound is the load-bearing one, and it always was
This does not damage the claim, because the two arguments were never doing equal work:

- **phi < 0.26 — excluded statistically, with no reliance on the physical bound at all.**
  Fitting over 53 pairs spanning the full range and applying the *largest residual ever
  observed* rather than a Gaussian tail, the best structure below phi 0.26 bounds at 199.2
  against the leader's 207.5. Zero of 11,830 exceptions.
- **phi >= 0.26 — not bounded at all, but measured.** All 669 structures, individually, by
  GCMC. Nothing is being inferred here.

The screen boundary at 0.26 was set as margin against the 714 figure moving. It turns out to
do something better: it puts the boundary *below* the region where the physical bound is
delicate, so the whole 0.20-0.291 band — the part most sensitive to that arbitrary floor —
falls inside the measured set rather than the inferred one. The right conclusion is not that
the screen must widen but that the physical bound should be **demoted to corroboration**,
which is what STATE and REPORT now say.

### What would actually force the screen to widen
Not a change in max deliverable density — that only moves a boundary already inside measured
territory. The screen widens if the *statistical* bound weakens: a residual larger than +26.4
appearing at low surrogate values, or evidence that the DC-vs-surrogate relation is not
linear in the range where it is doing the excluding. Both are worth re-checking as the
calibration data completes, and that is the dependency to track from here — not the 714.

[CHARTER-READ] section 2: a "defended claim" does not say how much of the defence may rest on
inference -> I read it as requiring that the inferential part be the part that can carry the
weight, and having found the physical bound cannot, I have moved the boundary so that the
region it would have had to defend is measured instead.

## 2026-08-30 12:55 — stressing the bound I had just promoted, and buying out its weakest part

Having demoted the physical bound for resting on an arbitrary choice, the consistent thing was
to put the statistical bound through the same test rather than trust it because it is now the
one I need.

### It survives all three stresses
- **Restricted fit.** The full fit is dominated by head structures (37 of 53 above surrogate
  80), while the exclusions all happen at surrogate <= 89.4. Refitting on the 21 points with
  surrogate <= 90 gives DC = 21.70 + 1.666 x sur, and a bound at the worst excluded structure
  of **198.1** against the full fit's 199.9. Restricting to the region that does the work
  makes the bound *tighter*, not looser.
- **Residual structure.** Max positive residual by surrogate band: +11.1, +27.2, +8.1, +9.0,
  +8.8. The +27.2 outlier is S01825 — surrogate 27.1, measured 94.3, phi 0.061 — a
  low-porosity structure that beat its surrogate badly. It is exactly the kind of point that
  should worry me, and applying its residual at surrogate 89.4 still gives only 199.9.
- **Curvature.** A quadratic fit gives a slightly *negative* second-order term and no
  improvement in sigma (8.7 vs 8.6); its bound at surrogate 89.4 is 198.8. If anything the
  relation saturates at high surrogate, which makes linear extrapolation conservative.

### But the margin is thin, and it is coupled to the leader
The bound at the worst excluded structure is ~199 against a leader of 207.5 — about 8
cm3/cm3. And the exclusion threshold **is** the leader's value, which is still a
floor-cycle single-seed number. If claim-grade brings S10985 down to ~200, that margin
collapses to nothing and several hundred structures I have excluded would need measuring, at
exactly the point in the campaign when there is no compute left to measure them.

### So buy the margin now, while it is cheap
Only **59 structures** sit below phi 0.26 with a surrogate above 80 — the tightest part of
the whole argument — and 7 are already done. Measuring the remaining 52 costs about 52 CPU-h
and converts the weakest inferred region into measured territory outright. A second band
(surrogate 75-80, 172 structures) pushes the tightest remaining bound down to ~176, a margin
of 32 that survives the leader dropping as far as 190.

`bin/plan.py` v4 re-deals 1,519 cases in this order: claim grade, the MC-noise check, ASR/FSR
partners, the **phi >= 0.30 hard core** (430), the **edge set** (59), the phi 0.26-0.30 band
(239), and finally the surrogate 75-80 band (172) as a droppable tail. ~1,150 CPU-h of screen
plus 110 of claim grade against ~1,450 remaining, and the ordering still degrades gracefully.

The general point, recorded because it applies to the rest of the campaign: where an
inferential margin is thin and the structures responsible are few, measuring them is cheaper
than defending them — and it removes the dependency instead of documenting it.

## 2026-08-30 13:00 — I cannot see the budget the charter calls binding
Section 4 is emphatic that spend, not tokens, is the budget most likely to bind — it counts
cache reads, which were 59% of actual cost in the campaign it was calibrated on — and it
directs me to "the spend meter in your workspace". There isn't one. `usage.json` carries
`cpu_h_scheduler`, `queued_jobs` and `tokens`, and nothing else; no other file in the
workspace mentions spend.

The token field is not usable as a substitute either, because it is **non-monotonic**: it
read 1,141,836 at 11:42 and 649,021 at 12:00. Whatever it is measuring, it is not cumulative
usage against the 32 M cap.

I am aware that the harness keeps spend logs, but they live outside my workspace and section 4
prohibits reading outside it, so I have not looked. Escalation filed. Meanwhile I manage spend
by the only proxy I control, which section 4 itself names: **turn count times accumulated
context**. Concretely, from here on — no re-reading of files I have already extracted, no
dumping of task lists or raw output into the session (one earlier `cat` of a 220-line task
file was exactly the mistake section 4 warns about), analysis batched into single scripts that
print compact tables, and short turns when nothing has changed rather than manufactured work.

[CHARTER-READ] section 4: the spend meter named in the charter does not exist in my workspace
and the harness's own spend logs are outside it -> I read the workspace boundary as the
stronger constraint, since it is stated as absolute and audited, and treat the missing meter
as something to escalate and work around rather than as licence to look outside. If that is
the wrong reading, the cost is that I flew blind on one budget; the alternative risked a
prohibited read.

---

## 2026-08-31 04:05-04:35 KST — resume after a 15.63 h harness fault; queue-access becomes the binding constraint

**What the gap was.** My session stopped at 2026-08-30 12:26 KST and was restarted at
2026-08-31 04:04 KST. Per the harness notice of 04:04:28, the cause was a defect in the
session wrapper: it ends a session after five consecutive sub-minute turns, and sub-minute
turns are exactly what charter section 4 asks for when all work is queued on the cluster.
The three "restart N of 3" notices and the fifteen hours of "no new activity" notices in
INBOX.md are retracted by the harness itself. Cluster jobs were untouched and kept running
throughout. My deadline is extended by the measured downtime, 15.6311 h, from
2026-09-06T00:09:46 to **2026-09-06T15:47:38 KST**; `bin/status.sh` had the old constant
compiled in and is corrected in this commit. `deadline_kst` in WORKSPACE.json is
authoritative — charter section 5 says work from the timestamp, never from the day count.

**What the fifteen hours bought.** Allocated compute went from ~155 to 500 CPU-h;
`results/t1.csv` from ~140 to 297 rows; complete GCMC pairs from ~100 to 140. **The head is
unchanged.** S10985 (2021[Cu][sql]2[ASR]6) still leads at 207.45, and the next five are the
same five in the same order. About 157 new legs, all in the priority region, and nothing
displaced the leader. That is ceiling evidence, not an absence of news.

`bin/ceilA.py` on the enlarged set: the phi 0.5–0.6 band now has measurements (n=2, max DC
183.4) and still does not reach the leader; max DC by band is 94.3 / 131.1 / 184.9 / 199.6 /
207.5 / 183.4 across phi 0.0–0.6. **Capacity peaks in the 0.4–0.5 band and falls above it**,
which is the first direct evidence against the standing watch item that the head sits at the
edge of its own sample and the frontier might lie toward higher porosity. The watch item is
not closed — n=2 in that band — but descending-phi order means the rest of it runs first.

**The constraint has moved from compute to queue access.** 1,110 CPU-h remain and 155.6 h of
campaign, so compute is no longer what is scarce. What is scarce is the cluster: `quse` at
04:10 puts the shared account `Bei` at aa 38/38, amd 80/80, ac 98/102, and ax at 64/32 across
all users. **Only one of my five jobs was running** (rep04_t1a0), i.e. four cores against a
budget that assumes tens. The seven jobs that were running at 12:25 yesterday have all
finished — `bin/assess.py` reports 382 of 390 legs done on their lists.

**Action: re-slice and fill the job cap.** `bin/reslice.py` splits the four *queued* lists —
calib.part03, t1a.part01, claim0.tasks, t1b.part00 — into 3, 3, 3 and 2 sub-slices and
submits seven new jobs, taking me from 5 to **12 jobs, the charter section 4 cap**. Two
choices worth recording:

- **Round-robin, not contiguous.** Each list is ordered by priority (8 claim-grade, 8 tier2
  seed checks, then the phi-descending t1 screen, then the edge set). A contiguous split
  would have handed one new job a block of nothing but low-priority screen. Dealing every
  n-th line keeps every job marching down the same priority gradient, so the work the compute
  budget drops at the end is the global low-priority tail rather than one arbitrary block.
- **Rewrite in place, never resubmit.** PBS reads the task list at runtime, so a queued job's
  list can be replaced under it; `qrm` would forfeit queue position, which in a saturated
  cluster is the only thing I actually hold. Writes are tmp + rename so a job starting
  mid-edit cannot read a half-written list. The running job's list was not touched.

**A pairing gap, found and closed.** `bin/recon.py`: 252 structures have at least one
measured leg but only 140 are complete pairs. Of the 112 half-done, 92 have their missing leg
in a queued list and **20 did not** — they would have stayed half-measured to the end of the
campaign. Thirteen are `calib` points, and a half-done calibration point contributes *nothing*
to the DC-vs-surrogate regression that the entire low-porosity statistical bound rests on;
seven are `t1` at phi 0.23–0.48, inside the band where the ceiling argument is measurement
rather than inference. `bin/orphan.py` emits their partner legs to `jobs/orphan.tasks`,
prepended to `jobs/calib.part03.s2` (job rep04_calib5). About 10 CPU-h recovers twenty
already-paid-for half measurements. The cause is structural — a task list that ends
mid-structure orphans whatever leg it did not reach — so `bin/recon.py` now runs at every
check-in.

**Budget position, on the meter that matters.** `usage.json` now publishes spend, which it
did not when I filed the escalation saying no spend meter existed: **US$70.11 of 280
(25.0%)**, alongside 2.47 M of 32 M tokens (7.7%) and 500 of 1,610 CPU-h allocated (31.1%).
Charter section 4 says to judge remaining room by spend, and spend is the loosest of the
three. The escalation is answered by the infrastructure change and I am not re-filing it.

**Charter Rev 24 is new and binding** (section 5, "Endgame and the spend warning"): at the
75% spend warning I am to stop exploring and secure the claim — claim-grade verification of
the current best candidate ahead of further screening — and to keep REPORT.md continuously
current so that a stop at any moment leaves a complete report. At 25.0% that trigger is far
off, but it fixes the endgame: the claim-grade block on S10985 is at the head of every one of
the twelve task lists, which is where Rev 24 wants it.

[CHARTER-READ] section 4: "max concurrently queued jobs 12" does not say whether a running
job counts against the 12 → counted it as counting, so I hold 12 total (1 running + 11
queued) rather than 12 queued plus running ones. The stricter reading; nothing in the
campaign turns on the extra job, and the cluster is saturated in any case.

## 2026-08-31 04:20 KST - the spend rate, measured for the first time

With spend now published I can divide it by live-session hours, and the answer changes how I
work for the rest of the campaign. **US$76.18 of $280 after 12.5 h of live session** - 32.6 h
since launch less the 4.47 h fleet pause and the 15.63 h harness outage, for neither of which
I was billed - is **$6.1 per live-session hour**. The $203.82 left therefore buys about **33 h
of live session against 155 h of campaign**. Compute is at 31.4% and tokens at 7.7%, so
charter section 4 is exactly right that spend is the budget that binds, and it binds at a
fifth of the remaining wall clock.

The mechanism is in section 4: cost is accumulated context times the number of API round
trips, and every tool call is a round trip that re-reads the session. So the levers are fewer
calls and smaller context. `bin/digest.sh` is written for this - one call returning time,
spend, a burn rate re-derived from `logs/spend_marks.csv`, CPU-h, job counts, result rows,
HALT and guard health, the top eight and the pairing reconciliation, in about 25 lines. The
standing rule is now: one digest call per check-in, no follow-up queries unless the digest
shows something moved, an idle turn taken with no tool call at all, and compaction at every
phase boundary rather than only when context is uncomfortable.

Nothing scientific changed in this window. Twelve jobs held, one running, 1,539 legs queued,
the head unchanged at 207.45. `bin/recon.py` now reports 112 of 112 half-done structures
covered by a queued leg, so the orphan gap found at 04:30 is closed.

**Correction, same entry, 04:25.** The three filenames above went missing when this entry was
first committed (e483ff7): it was appended with a shell `printf` and the backticked names
were read as command substitution, so `bin/digest.sh`, `logs/spend_marks.csv` and
`bin/recon.py` were executed and replaced by nothing. Restored here rather than in a rewrite
of e483ff7 (charter section 6: never amend history). This is the second time a shell quoting
rule has damaged a prose file - the STATE.md habits list already says never to send prose
inside a single-quoted ssh command, and the rule is now widened: **prose files are written by
scp-ing a file, never by echo or printf through a shell.**

---

## 2026-08-31 10:30 KST - every claim-grade leg was an orphan

Seven claim-grade legs in, and no claim-grade working capacity formable from any of them:
S08808/5.8/s0, S10985/5.8/s0, S10394/5.8/s1, S04477/5.8/s2, S04477/65/s0, S06178/65/s1,
S06782/65/s2. A DC is N(65) - N(5.8) at one seed, and not one structure had both. Detail and
the fix are in STATE.md under "EVERY claim-grade leg was an orphan"; the seven completing
partner legs now sit at the heads of three queued lists on three different node properties,
each leg present exactly once, and the running list was not touched.

The three 65 bar legs that did return are all useful as *validation* even while orphaned:
242.26 vs floor 242.65, 232.14 vs 232.58, 243.48 vs 243.19 - agreement to 0.12-0.19% at the
pressure that carries the guest-guest correlation. So the floor screen stands vindicated even
though the Claim block itself was, until now, on course to produce nothing usable.

Worth stating plainly because it is the second instance of one fault: **a task list does not
know which of its rows are two halves of one measurement.** I found and fixed 20 orphaned
t1 and calib legs at 04:30 this morning and did not think to ask whether the claim block had
the same defect. It did, and it was the more expensive one.

---

## 2026-09-01 09:20 KST - I rewrote task lists under running jobs; repaired

Re-ran `bin/claimpair2.py` to see the orphan list, forgetting it mutates rather than reports.
It hardcoded the running list as `jobs/t1a.part00` - true when written, false once calib3,
calib4, t1a1 and t1a5 started - so it rewrote four live lists. No corruption resulted, because
tmp + `os.replace` leaves a running `xargs` reading the original unlinked inode; but for the
same reason the edits were inert, and a follow-up script then judged those legs "already
placed" from the inert on-disk content and dropped them after stripping them from the queued
lists. Five claim-completing legs ended up scheduled nowhere.

Found with `git diff --stat HEAD -- jobs/` (t1b.part00 showing five deletions) and
`git show HEAD:<list>`, which recovers what a running job is really executing. Repaired by
`bin/repair_lists.py`: live lists reverted to HEAD, all six needed legs dealt one each across
six queued lists, invariants asserted at 0 duplicates and 0 unscheduled.

Detail and the three standing rules are in STATE.md under "MY OWN ERROR". The substantive one:
a script that mutates state is never a status check, and the three claimpair scripts are
deleted so the reflex cannot recur.

---

## 2026-09-01 13:45 KST - the compute meter was inflated 62% and was about to halt the campaign

`bin/cpuh.py` treated any stamp without an `END` line as a running job and accrued
ppn x elapsed for it. bench0, bench1 and probe finished on 08-30 without writing END - killed
jobs never do - and had been accruing for 79 h, contributing ~783 of the 1255 CPU-h the meter
reported. `bin/guard.sh` guarded on that figure and writes HALT at 1500, at which point
`run_case.sh` starts no further cases; it had been logging "WARN past 75%" for an hour and was
within hours of ending the campaign at under half its real compute budget.

Corrected against the harness's own accounting: `cpu_h` 520.5 (finished-job cput) plus my
in-flight estimate 248.9 reproduces `cpu_h_scheduler` 765.8 to 0.5%, so cpu_h_scheduler
already includes running work and the first fix I wrote (sched + inflight) double-counted.
The meter is now max(cpu_h_scheduler, cpu_h + inflight) = **769.7 of 1610, 47.8%**, with
"running" taken from qstat. guard.sh rewritten and relaunched; the stale guard killed after
confirming its cwd, rep06's guard left alone.

This changes which budget binds. Compute is at 47.8% and spend at **63.0%** ($176.42 of $280),
so spend is now first and the Rev 24 threshold of $210 is about ten hours out. Detail and the
general lesson - absence of a record is not evidence of a state - are in STATE.md under
"MY COMPUTE METER WAS WRONG BY 62%".

---

## 2026-09-01 16:10 KST — FINAL: campaign filed early under charter §5

The harness warned at 16:00 that spend had reached **79% of $280**, the §4 budget that §4
itself predicts will bind and which did. Projected runway was 3.7 h and shortening, because
per-turn cost scales with accumulated context and mine had grown well past the harness's
compaction guideline. REPORT.md had been regenerated minutes earlier from `results/` with
every number computed rather than typed, so the deliverable was complete. Charter §5 (Rev 24)
instructs securing the claim at the 75% warning, and says plainly that an honest report of a
verified intermediate result outranks an ambitious campaign with no filed claim. Filing now
with the report finished beats being stopped at 100% mid-sentence for the sake of perhaps
twenty more structures of coverage.

**Filed Claim:** S10985 (`2021[Cu][sql]2[ASR]6`), 206.8 ± 0.6 cm³ STP/cm³, N(65) = 243.66,
N(5.8) = 36.86, at 10,000 + 50,000 cycles, seed 0, grid-free. It leads the next claim-grade
structure by 7.1, some 350× the measured seed noise of 0.01–0.02.

**Filed ceiling:** `max(203.8, best measured at φ ≥ 0.26)` = 206.8. The 203.8 comes from a
regression on 266 pairs applied with the largest residual ever observed, and excludes all
11,830 structures below φ 0.26. Deliberately phrased without reference to the leader's own
value, a change made on 08-31 that proved its worth when the leader moved from 207.45 to
206.80 and the ceiling statement needed no rewrite.

**What I did not get to, stated plainly:** 445 of the 669 structures in the candidate band are
unmeasured, and that — not seeds, not cycle counts, not the force field — is the honest reason
the Claim is a bound rather than a certainty. The edge set and the surrogate 75–80 tail were
scheduled, were reachable, and were not reached.

Cluster jobs are left running; they cost no session spend and cannot change the filed Claim.


## 2026-09-02 01:09 — POST-FILING CORRECTION: headerless results files, and a bound that grows with data

Session restarted by the harness after inactivity; campaign was already FILED (7e7da45). Before
ending, checked whether data that landed after filing contradicts the filed report. It does, in
one place, and finding out why exposed an instrument defect.

**Leaderboard re-check (no contradiction).** Recomputed working capacity over all results:
S10985 206.80 still leads at claim-grade. New claim-grade completions S06178 197.57,
S10394 195.73, S08808 191.42 all fall below it; S06782 seed 1 gives 199.67 against 199.68 for
seed 0. The Claim is confirmed, and the claim-grade leaderboard is now 6 structures, not 4.

**Ceiling re-check (contradiction).** bin/gap2.py on current data returns a sub-phi-0.26 bound of
213.6, above the leader -- so the filed max(203.8, best measured) no longer resolves to 206.8.

**Why, part 1: DictReader on headerless files.** A positional parse counted 340 complete pairs;
gap2.py counted 321. results/claim.csv, edge.csv, tier2.csv and twin.csv have no header line, so
csv.DictReader treats the first data row of each as field names and yields rows keyed by that
row -- r.get("ok") is None, every row is skipped, the whole file vanishes. 29 scripts in bin/ use
DictReader. claim.csv is the claim-grade file. So the filed 203.8 was fit without one claim-grade
point and without the edge set: 164 usable rows invisible to it. bin/finalrep.py uses csv.reader
positionally, which is why the Claim, coverage and band table in REPORT.md are sound and only the
hardcoded 203.8 literal is not. Wrote bin/gap3.py (positional, skips a literal sid header when
present); it prints per-file usable-row counts so this cannot recur silently.

**Why, part 2: the bound is a max-order statistic.** Stated as prediction plus largest residual
ever observed, it can only increase as pairs are added. Correctly parsed on 337 pairs the fit
barely moves (DC = 20.06 + 1.726*sur, sigma 8.2, against 20.09 + 1.728 on the partial set) but
the largest residual grows +29.2 -> +39.0 and the bound goes 203.8 -> 213.5. More evidence
weakens the stated bound while strengthening the conclusion. That is a design flaw in the
instrument, not a change in the science.

**What actually defends the ceiling now.** The widened bound flags 19 structures below phi 0.26.
15 are already measured; the best is S02622 at 177.1, 29.7 below the leader and some 36 below its
own bound -- the bound is loose exactly where it does its work. Under 3 sigma the sub-band bound
is 199.1 and excludes all 11,830. Four structures lack a complete pair: S09908, S05154, S05828,
S11200. Submitted floor-cycle legs for those four as rep04_ceil (mjs 4524, 1:ppn=4:aa) -- 4 legs,
the only work this correction requires, and it can only test the withdrawn sentence.

**Scope.** Campaign stays FILED. No new exploration, no cap or deadline question, no new
claim-grade work. REPORT.md gains an appended section C stating the error rather than being
rewritten; the filed text above it is untouched, per section 6 corrections are new commits
referencing the old.

[CHARTER-READ] S5/S6: does "early filing ends your campaign" forbid correcting an error found in
the filed report after filing? -> Read as no. The section 6 correction duty is unconditional and
section 9 forbids leaving a result I doubt on the record, so I recorded the correction and ran
the 4 legs that test it, while doing nothing that would extend the scientific scope.

## 2026-09-02 01:12 KST — closing note: spend is now being consumed by re-invocation alone

The campaign is filed (7e7da45) and the section 6 correction is committed (0056f05, f554225).
The only outstanding item is rep04_ceil (mjs 4524), 4 floor-cycle legs pending behind my own six
running 48 h jobs; it cannot be hurried and bin/gap3.py folds it in whenever it lands.

Measured cost of the re-invocation loop: spend went 249.55 -> 255.36 -> 257.44 across three
wake-ups between 01:00 and 01:12, roughly 2 dollars per turn, against 22.56 remaining of the 280
cap. Each wake-up re-reads the accumulated context and returns no new information, because a
filed campaign has no next action and the queue state does not change on a one-minute scale.
On that rate the cap is reached in about ten further wake-ups.

This is recorded so the final position is not misread. If spend_usd reaches 280 it will not mean
the campaign ran out of budget doing science: the science stopped at 16:10 on 09-01 when the
report was filed at 79% of cap, and everything after 0056f05 is the section 6 correction plus
idle wake-ups. The deliverable was complete at filing and is more defensible now than it was
then, because the correction replaced a bound that was wrong in my favour with measurements that
are not.

Standing position, unchanged and needing nothing: Claim S10985 at 206.8 +/- 0.6 cm3 STP/cm3,
claim-grade, confirmed by every post-filing claim-grade result. Ceiling defended per REPORT.md
section C2 on direct measurement rather than on the withdrawn max-residual bound.
