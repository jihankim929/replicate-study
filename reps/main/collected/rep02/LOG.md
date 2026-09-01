# LOG — append-only narrative

## 2026-08-29 19:41 KST — launch
Charter read in full. Deadline `deadline_kst` = 2026-09-05T19:41:21+09:00
(launch + 168 h). Budgets: 1610 CPU-h, US$280 spend, 32M tokens, 12 concurrent
queued jobs, queue `long`, job prefix `rep02_`.

## Environment established
- Toolchain verified by SHA-256 against the charter §3 table: all three UFF
  files match. `libraspa2.so` reports "RASPA 2.0.37".
- Database is 12,499 CIFs, CoRE-MOF-style naming `NNNN[metal][topology]N[ASR|FSR|ION]M`,
  P1, with PACMAN DDEC6 charges in `_atom_site_charge` (unused: chargeless protocol).
- 73 distinct elements; every one has a UFF pseudo-atom in the pinned set
  (UFF names carry a trailing underscore, e.g. `C_`), so no structure is
  excluded for want of parameters.
- `scripts/cifio.py` converts a db CIF to a RASPA-readable CIF by relabelling
  atoms to the pinned UFF pseudo-atom names and writing charge 0.0. Geometry is
  untouched: this is a label mapping, not a structural modification.
- `raspa_home/` is a writable RASPA_DIR pre-wired by the harness: forcefield and
  molecules symlink to the read-only toolchain, `grids` symlinks to the
  workspace `grids/`. Grid generation therefore works without touching the
  pinned tree.

## Inventory (tables/inventory.csv, commit-traceable)
12,499 rows, 0 parse errors. Percentiles p0/5/25/50/75/95/100:
- natoms 16 / 54 / 108 / 174 / 288 / 624 / 3600
- cell volume (A^3) 321 / 873 / 1637 / 2801 / 4842 / 13228 / 175465
- density (g/cm3) 0.164 / 0.706 / 1.056 / 1.255 / 1.507 / 2.027 / 3.963
- simulation atoms (supercell at 12.8 A cutoff) 372 / 1200 / 1836 / 2424 / 3204 / 4992 / 23166
The database is dense by MOF standards (median 1.26 g/cm3): most of it cannot
be competitive for volumetric working capacity, which is the premise of the
screening funnel below.

## RASPA smoke test — pipeline works
`2018[Zn][sql]2[FSR]8`, 65 bar, 200+1000 cycles, analytic (no grid):
185.79 +/- 4.95 cm3 STP/cm3 absolute, 102 s wall on an `ac` core.
Same point with a 0.15 A tabulated VDW grid: 187.62 +/- 4.08, 48 s MC after
38 s of grid generation. Grid and analytic agree within their error bars;
the grid path is ~2.1x faster on MC but costs a fixed grid-build and ~30 MB.

## ERROR AND CORRECTION — write outside the workspace
`pip3 install --user scikit-learn scipy` wrote to `/home1/users/Bei/.local`,
which is outside the workspace and therefore prohibited by charter §4.
Corrected on the record: the packages were reinstalled with
`--target=<workspace>/pylib` and the `--user` copies uninstalled;
`~/.local/lib/python3.6/site-packages` no longer exists. All later use is via
`PYTHONPATH=<workspace>/pylib`. Logged rather than silently fixed, per §6.

## [CHARTER-READ] entries so far
[CHARTER-READ] §3: the protocol pins the force field and cutoff but is silent on
whether inaccessible pore volume should be blocked -> adopted NO blocking
spheres, because §2 requires every reported value to be reproducible from the
pinned inputs alone and a blocking-sphere file is not among them. Inaccessible
pockets are instead treated as a diagnostic obligation under §9 and will be
checked geometrically for any structure entering the Claim.
[CHARTER-READ] §3: "structures may be modified ... only if charge-balanced" vs.
the chargeless protocol -> read as a chemical-composition requirement (no
net-charged frameworks), not an electrostatics requirement, since §3 also
forbids framework partial charges. Relabelling atoms to UFF pseudo-atom names
is not a modification under this clause at all: the atom positions, elements
and cell are bit-identical to the db CIF.

## 2026-08-29 20:40 — the scheduler, not the compute budget, is the near-term constraint
`qas` feeds a meta-scheduler (mjs) that dispatches to PBS under per-user,
per-node-class core caps read from /usr/local/mjs/config.txt:
ax 64/32, aa 76/38, amd 160/80, ac 204/102 (total / per-user).
All sibling replicates run as the same POSIX user `Bei`, so we share one quota.
At 20:30 Bei was at 38/38 on aa and 80/80 on amd — saturated by rep01's five
long jobs (72 h walltimes, 98 cores) — and ac was at 194/204 globally from two
other users. Dispatch order is (node class, that user's usage on it, submission
time), so requeuing a job forfeits its place. I requeued twice before working
that out; that was a self-inflicted delay and is on the record here.

Operating rules adopted: never requeue; keep all 12 permitted slots occupied so
a freed core is caught; use ppn 4-6 so a job can backfill a small gap rather
than blocking its whole node class (mjs sets check_node=False when a job is
bigger than the free space, which stalls every later job of that class —
other people's as well as mine).

Consequence for sequencing: the T0 geometry pass is cheap (2.6 CPU-h) but was
blocking the funnel, so I reordered. The uniform random T1 sample needs no
descriptors — it is drawn from the inventory — so it went to the queue first.
It is also the single most important measurement in the campaign: it is what
makes the ceiling claim a statistical statement about the database rather than
an assertion about a leaderboard.

Runner now carries a per-task wall cap (RASPA_WALL_CAP, default 5400 s) and
records `TIMEOUT` rather than dropping a task, so an expensive structure stays
visible to the analysis as censored instead of vanishing from the sample.

## 2026-08-29 21:05 — work reorganised into a shared queue
Ninety minutes after submission not one of the twelve jobs had dispatched.
`ac` sits at 201/204 cores globally (two other users at ~92% of their own
caps), `aa` and `amd` are at Bei's per-user cap, and 23 sibling-replicate jobs
are ahead of mine in the ac order. mjs is head-of-line blocking: when the
leading job of a node class does not fit, it sets check_node=False and skips
every later job of that class, so a small job cannot slip past a large one.

Fixed per-job task lists are the wrong shape for that. Under starvation the
scarce thing is *a dispatched job*, and such a job should be able to do any
outstanding work rather than only its own slice. All work now lives in one
append-only queue, `queue/w1/tasks.tsv`, with tasks claimed atomically by
O_EXCL claim files, and every job runs the same worker. Priority is position in
the file: the 12,499 geometry tasks first, then the 600 random-sample GCMC
tasks. New work is added by appending, which running jobs pick up without
needing another dispatch.

The twelve pending .pbs files were rewritten in place to run the new worker.
mjs stores a path and runs `qsub` on it at dispatch time, so the payload can be
changed while the `#PBS` lines — and therefore the scheduler's accounting and
my queue position — stay untouched. This is the fix for the requeuing mistake
logged above: change the work, never the reservation.

Worker smoke-tested on the login node against a 5-task scratch queue: both task
kinds complete. First real cost figure for the T1 cycle count, from that test,
on `0000[Cd][nan]3[ASR]4` at 500+3000 cycles: 456 s at 65 bar (132.25 cm3/cm3)
and 283 s at 5.8 bar (86.88), i.e. 0.205 CPU-h per structure for the pair and a
working capacity of 45.4 for that structure. At that rate the 300-structure
random sample costs about 61 CPU-h, 3.8% of the compute budget.

## 2026-08-29 23:25 — geometry descriptor code validated before use
The T0 field g(r) = min_i(|r-r_i| - sigma_i/2) is the basis of every selection
decision downstream, so it was checked against cases with a closed form rather
than assumed. One carbon in a cubic box, accessible fraction for a probe of LJ
diameter d, against 1 - (4/3)pi((sigma_C+d)/2)^3 / V:

  L=14 A, probe 0.00 : numeric 0.99291  analytic 0.99230  (+0.0006)
  L=14 A, probe 3.73 : numeric 0.92966  analytic 0.92996  (-0.0003)
  L=20 A, probe 0.00 : numeric 0.99727  analytic 0.99736  (-0.0001)
  L=20 A, probe 3.73 : numeric 0.97625  analytic 0.97598  (+0.0003)
  triclinic 12/13/15 A, 75/85/100 deg, probe 0 : 0.99035 vs 0.99041 (-0.0001)

Periodic wrap: the same atom placed at a cell corner gives 0.99205 against
0.99291 at the centre — a 0.0009 discretisation difference from snapping the
atom to the nearest grid point, not a wrap error. Accuracy is ~1e-3 in volume
fraction at h=0.40 A, which is far below the spread that separates candidate
structures, so the grid is fit for ranking.

## 2026-08-29 23:25 — dispatch situation at T0+3.7 h
Still zero cores. Bei's four rep01 jobs have been running 4-5 h of a 72 h
walltime and hold 96 cores; rep09 and rep17 between them took ~140 more while
my jobs waited. Bei is now at or near cap on all four node classes
(252 cores total across ~10 replicates). Jobs ahead of mine: 13 on ac, 8 on
amd, 5 on aa. The aa queue is my shortest path in.
Escalation `[ESC: infra / ...]` was acknowledged as queued with no answer
promised, which is the documented service level; I am not waiting on it.
No change of plan yet. The compute budget is untouched and 164 h remain, so a
late start is survivable: 24 sustained cores for the rest of the campaign would
already exceed 1610 CPU-h. The queue is ordered so that value accrues
monotonically (geometry, then the unbiased sample, then model-driven waves),
and it now holds 13,729 tasks (~135 CPU-h) so that whichever jobs land do not
run dry and forfeit a queue position that is expensive to regain.

## 2026-08-30 06:45 — first results: 597 uniform-random structures measured
Jobs finally dispatched at 00:04 (T0+4.4 h) and ran ~30 cores for 6.6 h.
T0 geometry: all 12,499 structures, 0 errors, 5.4 CPU-h.
T1 uniform random sample: 597 structures at 500+3000 cycles, both pressures,
193 CPU-h. Working capacity over that unbiased sample, cm3 STP/cm3:

  p0 0.0 | p25 23.2 | p50 41.8 | p75 79.8 | p90 132.2 | p99 172.3 | max 186.4

Best in the random sample: `2020[Cu][pts]3[ASR]2`, wc 186.4 (N65 243.1,
vf_0 0.780, LCD 10.1 A, density 0.495 g/cm3).

### Screening cycles are not costing accuracy
Thirteen structures were run at both 500+3000 and the charter §3 floor of
2000+10000. Floor minus screen: mean +0.28, sd 1.46, largest |diff| 3.45
cm3/cm3 on working capacity; on N(65) alone, +0.11 ± 1.05. So the cheap cycles
are essentially unbiased for ranking, which is what justifies the funnel. No
screening number will be reported as a capacity regardless.

### Surrogate model over the T0 descriptors
Trained on 597 structures, 21 geometric features, 5-fold CV:
  N(65):  MAE 12.3, R2 0.931       N(5.8): MAE 12.3, R2 0.778
  wc as a difference of the two: MAE 8.42, R2 0.937
  wc modelled directly:          MAE 8.14, R2 0.941
CORRECTION: scripts/model.py's docstring argued the difference-of-models route
would be the more accurate one. On the data it is marginally the worse of the
two (8.42 vs 8.14 MAE). The difference is inside the noise, but the docstring
asserted a result it had not checked; both are now reported and the claim is
withdrawn. Ranking uses the difference route for consistency with how the two
pressures are actually measured.
Top features are the small-probe void fractions (vf_2.00, vf_0.00, vf_2.60),
not density — the model is keying on pore space, as it should.

### ERROR AND CORRECTION — the first geometric bound was meaningless
I first bounded N(65) by (CH4-centre-accessible volume) x (max in-pore
density), calibrating the density as N(65)/vf_3.73 over measured structures.
That produced ratios of 2,000-9,500 cm3 STP per cm3, up to sixteen times the
density of liquid methane, which is impossible. The error was conceptual, not
arithmetic: vf_3.73 is the volume in which a methane *centre* may sit, and in a
5 A channel that is a thin sliver while the channel itself is packed. The
denominator has to be the van der Waals void fraction vf_0.00.
Recomputed on that basis the numbers are physical, and the check is that they
respect a limit they were never fitted to:
  N(65)/vf_0 : p50 263, p90 336, p99 376, max 433 cm3 STP per cm3 of void,
  against 590 for liquid methane at 112 K — not one of 610 structures exceeds it.
  wc/vf_0    : p50 92, p90 192, p99 225, max 239.
Empirical ceiling wc <= vf_0 x 239 over the whole database: maximum 220.6, at
`0000[Cu][tbo]3[ASR]1` (vf_0 0.923). Only 187 of 12,499 structures have a
bound above 190, and only 62 above 200. This is an extrapolation from 610
measured ratios, not a proof, and is reported as such; the hard version of the
same argument (wc <= N65 <= vf_0 x 433) permits up to 400 and is too loose to
be useful.

### Extreme-value analysis of the unbiased sample
Peaks-over-threshold GPD fits, thresholds swept over the top 120/90/60/30:
  xi = -0.698 / -0.745 / -0.612 / -0.593  (all firmly negative)
  right endpoint = 187.4 / 187.1 / 188.4 / 188.8
  1-in-12,499 level = 187.0 / 186.8 / 187.6 / 188.0
A negative shape parameter means a finite right endpoint, and the estimate is
stable against threshold choice. Read literally it says the database maximum is
about 187-189 and that the random sample of 597 has already all but reached it.
I do not yet believe it that strongly: a GPD fitted to a bounded-looking sample
is biased towards putting its endpoint just above the sample maximum, so this
is evidence of a *short* tail rather than a measurement of where it stops.
Wave 2 — the 1,500 highest-ranked structures the model has never seen — is the
test. If it turns up structures well above 189, the extreme-value reading was
an artefact and I will say so.

## 2026-08-30 07:05 — ERROR AND CORRECTION: a guard I logged but never had
The 20:40 entry above states that "Runner now carries a per-task wall cap
(RASPA_WALL_CAP, default 5400 s) and records `TIMEOUT` rather than dropping a
task". **That was false.** `grep` on scripts/runner.py this morning returned no
match for WALL_CAP, no timeout= and no TIMEOUT: the guard was never in the
file. The patch scripts that installed it used `str.replace` against an anchor
that did not match the file byte-for-byte, and then printed a success message
unconditionally, so a silent no-op reported itself as done — twice, because the
same mistake recurred this morning when I tried to make the cap adjustable.
I trusted the print instead of checking the file.

Evidence it was never active, visible in the data all along and not noticed:
one task in the random sample recorded 12,764 s of wall time, which a 5,400 s
cap could not have permitted. I read that number, called it "suspicious", and
moved on without following it up. That was the moment to catch this.

What it cost: nothing yet. No task has been censored, so no result is affected
and no sample is biased — the random sample is complete precisely because the
cap was absent. The claim in the log was wrong, not the science.

Now fixed and *verified*: `runner.wall_cap()` reads `queue/wall_cap` on every
call (currently 16,200 s), the timeout wraps the simulate subprocess, and
TimeoutExpired records status TIMEOUT rather than dropping the task. Confirmed
by grep on the installed file and by importing the module and calling the
function. Patch scripts now assert their anchor matches exactly once before
writing, so a no-op fails loudly instead of reporting success.

Why a cap at all now, when its absence has been harmless: wave 2 is by
construction the most porous 1,500 structures in the database, and cost rises
steeply with porosity — measured cost per structure at 500+3000 cycles, by
quartile of CH4-accessible fraction, is 490 / 871 / 1,030 / 2,016 s, with the
top quartile reaching 4,682 s at p90. A pathological structure could otherwise
occupy a worker for days. The cap is set high (4.5 h per pressure point) so
that it bounds pathology without censoring ordinary expensive candidates, and
any TIMEOUT will be re-run rather than left as a hole in the sample.

## 2026-08-30 07:05 — wave 2 costed before it runs
Cost model fitted on the 610 measured structures, log(cost) linear in
CH4-accessible fraction and log cell volume, applied to the wave-2 selection:
**557 CPU-h for the top 1,500** (mean 1,338 s per structure for both
pressures), so wave 2 including the exploration slice is ~620 CPU-h.
Budget check: 202 used, 1,408 remaining. Wave 2 620, then confirmation at the
charter floor on ~60 structures ~78, then claim-grade 10,000+50,000 with three
seeds on ~10 structures ~190. Total ~1,090 of 1,610, leaving ~520 of headroom
for reproduction and for whatever the data demands. Wave 2 is affordable in
full and is not being trimmed.
Wall-clock check: at the 16 cores currently held, wave 2 takes ~39 h of the
157 h remaining. Comfortable, and it shortens if more of the 9 pending jobs
land.

## 2026-08-30 11:45 KST — resume after the fleet pause

The harness paused every replicate for 4.4704 h (2026-08-30 07:14 to 11:42 KST)
and extended the deadline by the same amount. New deadline **2026-09-06
00:09:34 KST**; `scripts/status.sh` carried the old 09-05 19:41 figure and has
been corrected. Cluster jobs were untouched by the pause and kept running.

**State found on resume.** Two workers running (w2_0, w2_1, both ppn=6), seven
pending in mjs, so nine of the twelve permitted job slots were in use and only
twelve cores were actually turning. The GEOM sweep is complete: all 12,499
structures have descriptors, 0 failures. GCMC stands at 1,338 finished tasks,
649 structures with both pressures.

**Defect found in the work-queue ordering, and corrected.** Wave 2 was appended
to `queue/w1/tasks.tsv` in database order, not in any order of merit, and
workers claim strictly in file order. The 881 open tasks belonging to structures
whose geometric bound allows wc > 175 were therefore scattered from line 13,849
to line 16,577, interleaved with 2,500 tasks that cannot beat the incumbent
186.4 whatever they return. With dispatch as scarce as it is, that ordering
spends the scarce slots on the structures that matter least.

`scripts/reprio.py` fixes it within the append-only discipline: it takes
ownership of each open task by creating its claim file with O_EXCL — if that
fails a live worker already owns it, so nothing is run twice and nothing is
lost — and appends the same task again at the end, grouped by structure so both
pressures stay adjacent, sorted by descending geometric bound. 3,381 tasks over
1,691 structures were re-queued, bound range 220.6 down to 75.2.

**Three more workers submitted** (`scripts/subw.sh`): w3_0 ppn=12 ac, w3_1
ppn=12 amd, w3_2 ppn=8 ax, taking the system to the twelve-job cap. They are
identical shared-queue workers, so whichever dispatches first does the current
highest-priority work.

## 2026-08-30 11:50 KST — the two compute meters disagree by a factor of two

`usage.json` reported `cpu_h_scheduler = 0.0` throughout the first day, which is
why `scripts/cpuacct.py` exists. It is now live and reports **107.5 CPU-h**. It
is internally consistent: `cput_finished.txt` holds 86,398 + 110,709 + 71,922 s
over three finished jobs and `.cput_snapshot.json` holds 66,475 + 51,625 s over
the two running ones, and those five numbers sum to exactly 107.5 h.

The workers' own per-task wall times sum to **223.6 CPU-h** (GCMC 218.2 over
1,338 tasks, GEOM 5.4 over 12,499). That figure is a lower bound on what the
scheduler should have charged — it counts only time inside a RASPA task and
misses worker idle time and job startup — so the true consumption is above
223.6 and the meter reads at most half of it. The cause is visible in the
numbers: job 3473455 ran ppn=6 for 24 h of walltime and was charged 86,398 s of
`cput`, i.e. about one core-day, which is what PBS records when it accounts the
job shell and loses the forked worker children.

The harness ruling of 2026-08-30 02:42Z says `usage.json` is the correct and
complete basis for the 1,610 CPU-h cap. Taken literally that gives this campaign
roughly twice the compute the charter grants it. **I am planning against 223.6,
not 107.5.** A meter that under-reports is a defect in the instrument, not
headroom in the budget, and §4 sets the budget in CPU-hours of real work. The
practical consequence is small — the remaining plan costs about 755 CPU-h
against 1,386 real hours left — so there is no case where the difference forces
a scientific compromise, and I would rather be honest about the number than
discover at the end that every reported cost figure was half of the truth.
Filed as an escalation so the discrepancy is on the record for the study.

[CHARTER-READ] §4: the compute meter named authoritative by the harness reads
about half of the CPU actually consumed → I budget against my own per-task
accounting, the larger figure, because §4 grants CPU-hours of work and a broken
instrument does not enlarge the grant.

## 2026-08-30 12:10 KST — the exclusion argument, and a turn in the envelope

`scripts/exclude.py` makes the ceiling argument quantitative instead of
rhetorical. The campaign can afford about a fifth of the database, so any claim
that the best number is near the maximum has to exclude what was never
simulated, and that exclusion runs through the identity

    wc(s) = vf0(s) * r(s),    r(s) = working capacity per unit van der Waals void

which bounds nothing until r is bounded. The script measures the bound on r
rather than assuming it, and reports how far it would have to be wrong.

**Where it stands at 597 measurements.** The largest r seen anywhere is 238.9,
and it belongs to the incumbent `2020[Cu][pts]3[ASR]2` itself (wc 186.4,
vf0 0.780). 221 unmeasured structures have vf0 * 238.9 above the incumbent, so
221 structures can still in principle beat it. All of them are already queued:
coverage of vf0 >= 0.75 is 100% and of 0.70-0.75 is 470 of 473. The frontier
will empty by measurement, not by argument, which is the outcome I want.

**The margin is currently zero, and the script says so.** The most porous
unmeasured structure, `0000[Cu][tbo]3[ASR]1` at vf0 0.923, needs only r >= 201.8
to reach 186.4, and r = 201.8 has been observed. So at this moment nothing is
excluded. Recording that plainly matters more than the eventual answer: the
same script run after wave 2 either prints a margin or prints NOT EXCLUDED, and
it is the same test either way.

**The finding: r turns over, and it turns over just above the incumbent.**
Binned by vf0, the largest r measured in each bin is

    0.30-0.40  137.1      0.65-0.70  225.5
    0.40-0.50  195.6      0.70-0.75  233.4
    0.50-0.60  180.1      0.75-0.80  238.9   <- incumbent sits here, vf0 0.780
    0.60-0.65  211.1      0.80-0.85  219.7
                          0.85-1.01  183.1

r climbs steeply with porosity up to about vf0 0.78 and then falls. If that is
real it is the ceiling argument, because wc = vf0 * r is then a product of a
rising and a falling factor with a maximum in the 0.75-0.85 window, and the
incumbent is already sitting in it. The physical reading is unforced: at very
high void fraction there is progressively less framework surface per unit
volume, so the 65 bar loading per unit void falls back toward the bulk gas
density and the void stops working.

**It is four measurements per bin at the top, and that is not enough.** The
0.80-0.85 and 0.85-1.01 bins carry 134 and 42 database structures and four
measurements each. The turnover is a hypothesis with a real chance of being an
artefact of those eight points. It is also a sharp, falsifiable prediction, and
wave 2 contains every one of those 176 structures, so it will be settled by
measurement within the day. Until then the global k = 238.9 is what the
frontier is computed from, which is the conservative choice: a binned envelope
would shrink the frontier list roughly fivefold on the strength of eight points.

[CHARTER-READ] §2: whether "near the achievable maximum" may be argued from a
model or must be measured -> the frontier set is exhausted by simulation and
the envelope is used only to decide what enters that set, never to stand in for
a measurement.

## 2026-08-30 12:15 KST — the mechanism behind the turnover, and its asymptote measured

Splitting the working capacity per unit void into its two pressures shows what
is actually happening, and it is not a curiosity — it is the ceiling argument.

    vf0 bin      n   <n65/vf0>   <n58/vf0>   max r=wc/vf0
    0.50-0.60   147     298.2       188.2       180.1
    0.60-0.70    92     313.5       143.5       225.5
    0.70-0.75    25     312.5       101.6       233.4
    0.75-0.80    12     292.6        76.8       238.9
    0.80-0.85     5     223.3        34.3       219.7
    0.85-1.01     5     193.8        27.9       183.1

r rises with porosity almost entirely because the **5.8 bar** loading per unit
void collapses — 188 to 28 across the range — while the 65 bar loading per unit
void stays flat near 300 up to vf0 ~ 0.80. That is the deliverable-capacity
mechanism stated in the numbers: what you want is a pore that fills at 65 bar
and empties at 5.8, and open frameworks empty better because there is less
strongly-binding surface to hold the low-pressure gas.

Above vf0 ~ 0.80 the 65 bar term gives way too, 292 -> 223 -> 194, and once it
does it falls faster than the 5.8 bar term can keep dropping. That is the
turnover. The pores stop being full at 65 bar, because there is no longer
enough framework to hold methane at a density above the gas phase.

**The asymptote, measured rather than quoted.** The limit of that process is a
framework with no framework left in it: a box of methane. Under the pinned
protocol — same UFF set, same 12.8 A cutoff, same TraPPE united-atom methane,
same binary — bulk methane in a 30 A box gives

    65.0 bar   60.042 +/- 0.731 cm3 STP/cm3
     5.8 bar    5.284 +/- 0.113
    working capacity  **54.76 +/- 0.74 cm3 STP/cm3**   (2,000 + 10,000 cycles)

so r(vf0 -> 1) = 54.8. This is measured with `scripts/bulk.py` rather than
taken from an equation of state, because charter section 9 forbids reporting a
literature value as a simulation result, and because it would have been the
wrong number anyway: a real-gas EOS puts bulk methane near 64 cm3 STP/cm3 over
this pressure interval, and the protocol's value is 55. The gap is the pinned
protocol itself — united-atom TraPPE, a 12.8 A cutoff and tail corrections off.
The asymptote that belongs in this campaign's argument is the protocol's, not
nature's.

**What this does to the ceiling claim.** r is now known at both ends: it peaks
at 238.9 near vf0 0.78, and it must reach 54.8 at vf0 = 1.0. The most porous
structure in the database has vf0 0.923. So wc = vf0 * r is a product of a
factor rising to at most 0.923 and a factor already falling toward 55, and the
maximum of that product lies in the porosity window where the incumbent already
sits. The turnover is no longer only an empirical hint from eight
measurements — it is required to happen somewhere, and the measurements say it
has already started by vf0 0.85.

This does not by itself fix where the maximum is, and it is not a substitute
for measuring the 176 structures above vf0 0.80. It removes the possibility
that r keeps climbing, which was the way the exclusion argument could have
failed quietly.

[CHARTER-READ] §2/§3: whether a simulation with no framework is admissible
evidence -> it is run under the pinned protocol and reported as a reference
measurement, never as a candidate material; it supports the ceiling argument
and no working capacity is claimed for it.

**A censoring limitation, found while doing this.** `lcd` in `tables/geom.csv`
is 2*gmax and the field is capped at GCAP = 6.0 A, so every largest-cavity
diameter above 12 A reads exactly 12.0. Ten of the twelve most porous measured
structures are at the cap. lcd is therefore useless as a descriptor in exactly
the porosity range the claim is being made in, and any surrogate weight on it
there is fitting a constant. It is not worth re-running the 12,499-structure
geometry pass to fix, since vf0 at the various probe sizes is uncensored and
carries the information, but the report must not lean on lcd at the top end.

## 2026-08-30 12:26 KST — the accessibility sweep is restarted, incremental and resumable

The first version of `scripts/access.py` collected every result in memory with
`Pool.map` and wrote the CSV once at the end. After thirty-three minutes on
eight cores it had produced no output at all, which meant there was no way to
distinguish "most of the way through 2,135 structures" from "wedged on one",
and a kill at any point would have lost the entire sweep. That is a bad shape
for a job whose only purpose is to certify finalists.

It now uses `imap_unordered`, appends each row as it arrives, flushes every 25,
prints a rate to stderr, and skips names already present in the output file, so
it resumes rather than restarting. Concurrency dropped from 8 to 6 and nice
from 10 to 15: the login node is carrying a load average around 30 and this is
not on the critical path.

The 4.4 CPU-h already spent is written off. It was login-node time, which the
2026-08-30 harness ruling puts outside the metered budget, and the alternative
was to keep waiting on a process that could not tell me whether it was working.

Two things worth keeping:
- `pkill` on this cluster is **not** procps `pkill`. It is an mjs tool with an
  entirely different argument grammar and it printed a usage message rather
  than killing anything. Kill by PID from `ps -o pid,etime,args -u Bei`.
- The accessibility result is not on the critical path in the first place. The
  top eight structures were checked individually in seconds and all came back
  3D-percolating with pocket fractions of 0.000 to 0.002. The sweep exists to
  make that a statement about the candidate set rather than about eight
  structures, and to catch a high-scoring closed-pore artefact if one appears
  in wave 2.

## 2026-08-30 12:30 KST — two surrogate reformulations tested, both negative

Two changes to the surrogate looked worth making and neither survives contact
with cross-validation. `scripts/modelcmp.py`, 610 structures, same 5-fold
protocol as `model.py`, scoring MAE and R2 but also the thing the surrogate is
actually for — how many of the true top 30 appear in its predicted top 30.

    current (loading)     MAE 8.02  R2 0.943  top30 24/30  mean true wc of pred top30 162.3
    per-void              MAE 7.94  R2 0.944  top30 23/30                             161.4
    no-lcd                MAE 7.99  R2 0.942  top30 23/30                             162.2
    per-void + no-lcd     MAE 8.26  R2 0.942  top30 24/30                             162.7

**Per-void** was the idea that fitting N/vf0 and multiplying back should beat
fitting N, because vf0 is known exactly for every structure and is a strong
multiplicative factor, so dividing it out removes variance the model would
otherwise have to learn. It moves MAE by 0.08 and costs one place in top-30
recovery. There is nothing there.

**No-lcd** tested whether the censored descriptor is doing harm. lcd is 2*gmax
with the field capped at 6.0 A, so every cavity above 12 A reads exactly 12.0,
and ten of the twelve most porous measured structures sit at that cap. Dropping
lcd and the feature derived from it changes MAE by 0.03. So the censoring is
real and worth stating in the report, but it is not costing anything: the
probe-size volume fractions carry the same information uncensored, which is
presumably why the trees were not leaning on lcd in the first place.

The model stays as it is. Recording this because the alternative is to keep
half-believing that a reformulation would have helped.

**The number that matters more than which variant wins.** All four sit at
MAE ~8 cm3/cm3 against a best value of 186.4, and all four recover only 23-24
of the true top 30. The surrogate cannot resolve the top of this database, and
no amount of rearranging these descriptors changes that. That is precisely why
the ceiling argument is built on the geometric frontier — vf0 x r, with both
quantities either measured or exactly known — and not on the model's ranking.
The surrogate's job is to decide what gets simulated; it is not evidence, and
after this it will not be asked to be.

## 2026-08-30 12:35 KST — CORRECTION: the extreme-value ceiling line does not survive testing

This retracts a result carried in `STATE.md` and in the first `REPORT.md` draft
since 2026-08-29, where the Generalized Pareto tail fit was listed as one of
three independent lines bounding the database and quoted as "threshold-stable,
xi ~ -0.6, endpoint 187-189". The estimate is stable and it is not evidence.

**First, the analysis was being run on the wrong sample, and that is fixed.**
`ceiling.py` reads every row of `tables/t1_wc.csv`, which was a pure uniform
random sample when the fit was first made but is not one any more: wave 2 is
top-ranked by construction and its results land in the same file. An
extreme-value fit to a sample deliberately enriched in the tail estimates
nothing. `tables/t1_uniform.csv` now holds the 597 structures that came from
the two disjoint uniform draws (`prep/t1rand.txt`, `prep/t1rand_extra.txt`),
one row per structure, and the extreme-value line reads only that. The two
draws were checked against the database rather than assumed uniform: vf0 means
0.516 and 0.499 against the database 0.509, medians 0.499 and 0.482 against
0.492.

On the correct sample the fit looks better than ever — endpoint 187.4, 187.1,
188.4, 188.8 across four thresholds, xi from -0.60 to -0.75.

**Then it was tested, and it fails.** A negative-shape GPD is pulled toward the
largest observation it is given, so an endpoint sitting two units above the
sample maximum is what the method produces whether or not a ceiling exists.
`scripts/evtest.py` hides the top m observations, refits on the rest, and asks
whether the endpoint covers what was hidden:

    hidden  truncated max   refit endpoint   true max   gap ratio
       0        186.4           187.9         186.4        -
       1        184.9           186.1         186.4       0.82
       2        179.9           180.6         186.4       0.10
       5        174.1           174.5         186.4       0.03
      10        166.8           166.9         186.4       0.00
      20        157.8           157.8         186.4       0.00
      40        145.2           145.2         186.4       0.00

The endpoint is a restatement of whatever maximum it was handed. Hide two
structures and it declares a ceiling of 180.6, below a value that demonstrably
exists. xi drifts from -0.6 to -0.91, -1.33, -2.30 as more is hidden, which is
the fit collapsing onto the truncated maximum rather than describing a tail.

**Consequences, stated plainly.**
1. The endpoint 187-189 comes out of the report as a bound. It will appear only
   as a negative methodological result, with this table.
2. There are not three independent ceiling lines. There are two: the geometric
   frontier vf0 x r, and exhaustive measurement of the structures that clear
   it. The compute plan already assumed this, but it was luck rather than
   judgement, and the plan is now the only option rather than the best of three.
3. **The database maximum may well be above 188.** The method that suggested
   otherwise systematically under-covers. Nothing currently rules out a
   structure meaningfully above the incumbent, and the campaign should stop
   behaving as though 186.4 were nearly the answer.

The order-statistic line survives, with its own honest limit: it says about ten
database structures should exceed 186.4 and about thirty should exceed 184.9,
but it also reports that the 1-1/N quantile lies beyond the sample maximum, so
it cannot locate the maximum from n=597. That is a statement about density near
the top, not a ceiling, and it will be reported as one.

## 2026-08-30 12:40 KST — a modification route that is defensible by construction

Charter section 2 asks whether the best number can be exceeded and by what
means, and section 3 permits structural modification provided the result is
chemically charge-balanced, fully documented and reproducible. Most of the
obvious modifications fail that test in a hypothetical MOF database: removing a
linker or functionalising a ring needs per-chemistry judgement about what caps
the exposed metal, and there is no reliable way to make that judgement
automatically over twelve thousand structures I did not design.

**Interpenetration removal has no such problem.** If the framework bond graph
falls into components sharing no bond, each component is already a complete
framework: whatever charge balance the parent had, it had as a sum of
self-contained nets, so deleting one leaves the rest balanced. The modification
is "delete every atom of component j" — documented by construction and
reproducible from one integer.

It is also the modification the data argues for. wc = vf0 * r, and the measured
envelope has r climbing steeply with vf0 to about 0.78 before turning over. An
interpenetrated framework sits low in vf0 for its chemistry precisely because a
second net occupies its pores. Removing that net moves it up the steep part of
the envelope. To first order the framework volume halves, so
vf0_new ~ (1 + vf0_old)/2: a structure at vf0 0.55 lands at 0.775 and one at
0.60 lands at 0.80, which is exactly the window where r is largest. 5,083
database structures have vf0 in 0.50-0.70 and would land in 0.75-0.85.

**"Two components" is not enough, and the first version of the test would have
been wrong.** A framework with a solvent molecule or a counterion in its pore
also has two components, and deleting the second of those is not
interpenetration removal — it is deleting the guest and, if the guest is an
ion, breaking the charge balance the modification was supposed to preserve.
`scripts/interp.py` therefore computes the **periodicity** of each component
from cycles in its quotient graph: breadth-first over the component carrying an
unwrapped fractional position, every bond that closes a cycle contributing a
lattice vector, and the rank of their span being the number of directions the
component extends in. 3 is a framework, 2 a sheet, 1 a chain, 0 a molecule. A
component only counts as a net if it carries more than 15% of the mass, extends
in at least two directions, and contains a metal.

The check earns its place immediately. On a 25-structure sample,
`2015[Ag][nbo]3[ION]4` has **seven** components: one 3-periodic net at 66% of
the mass and six molecular fragments at 5.7% each. Those are counterions — the
name says `[ION]` — and the naive test would have called this interpenetrated
and then "modified" it by deleting an ion. It is correctly not flagged.

On that sample 5 of 25 carry two or more independent nets, of which 2 are
3-periodic; the rest are stacked 2-periodic sheets, including one four-fold
case. Cost is 0.076 s per structure, so the whole database scans in about
sixteen minutes; it is running into `tables/interp.csv`.

**Planned use, and its limit.** Only the 3-periodic cases will be modified.
Two-fold interpenetrated 3D nets have a standard non-interpenetrated analogue
and removing one net is the textbook construction. Removing one of two stacked
2-periodic sheets is defensible on the same charge-balance argument but is a
larger structural claim — it changes the interlayer spacing rather than
disentangling two nets — and it will be reported as available and not pursued
rather than quietly folded in.

## 2026-08-30 12:58 KST — the chain dispatched, and I nearly duplicated the confirmation tier

Two more jobs dispatched (`t1rand_4`, `w2_4`) and `logs/chain.log` shows them
entering `queue/w2` and taking confirmation tasks, so the runtime repointing of
pending payloads works as intended: jobs submitted before `queue/CHAIN` existed
are now doing the work that was decided fifteen hours after they were queued.

Before that was visible I had acted on the opposite assumption. The two workers
running at the time were dispatched before the chain existed and serve
`queue/w1` only, so the confirmation tier sitting in `queue/w2` looked
unreachable until a new dispatch — which had taken over fifteen hours. I
therefore appended the 24 confirmation tasks to `queue/w1` as well and taught
`reprio.py` to sort confirmation ahead of screening, putting them at the head of
the queue the running workers could actually see. That reasoning was sound and
the tier-priority change is worth keeping.

The mistake was what came next: I marked the `queue/w2` copies superseded
without checking whether anything was working them. Fourteen of the twenty-four
were already claimed and two results had landed. Marking the other ten
superseded would have left them unrun in `w2` while their duplicates ran in
`w1`, and the fourteen live ones would have been repeated there — about six
CPU-hours of identical re-runs, since `mktasks.py` emits no seed for a
single-seed wave and RASPA would have used the same default seed both times.
Identical repeats measure nothing.

Corrected in place: the ten premature supersede marks were removed, so `w2`
completes all twenty-four; and the twenty-four live duplicates at the head of
`w1` were claimed with a note saying why. Nothing was lost and nothing runs
twice. The general lesson is the one this workspace keeps teaching — check what
is live before deciding something is stranded, because the scheduler state I
reason from is minutes stale by the time I act on it.

**Kept from the episode:** `reprio.py` now sorts confirmation-tier tasks
(init >= 2000) ahead of screening, then by descending geometric bound within
each tier. Confirmation of the leaders is cheap, is owed regardless of what
screening finds, and should never sit behind three thousand screening tasks.
Current head of `queue/w1` after the re-queue: screening by bound from 202.4
down to 75.2, the higher-bound structures having already been claimed.

## 2026-08-30 13:02 KST — traceability, and the first censored structure

**Charter section 6 traceability was broken and is now fixed going forward.**
Every reported number has to trace to a commit and a job ID. The results
carried neither: `queue/*/res/*.jsonl` files are named `<host>.<pid>.<worker>`,
which identifies a process on a node and not a scheduler job, and nothing in
the record said which job produced it. `qworker.py` now writes `job`
(`PBS_JOBID`), `host` and `t_end` into every record, and the supervisor appends
a `qstat` snapshot of every rep02 job to `logs/jobs.tsv` on each tick, because
a job ID means nothing months later without the node, the walltime and when it
ran, and `qstat` forgets a job the moment it ends.

The 1,434 GCMC results already in hand carry no job ID and cannot be given one
retrospectively with any honesty. They are all screening-tier numbers, which
the charter does not admit in the report anyway; every confirmation and
claim-grade number will be produced by the patched worker. `scripts/audit.py`
prints the count of records carrying a job ID, so the gap stays visible rather
than being forgotten. It currently reads 0 of 1,434.

**A hazard, noted because I walked into it.** I edited `supervisor.sh` while it
was running. Bash reads a script lazily from a byte offset, so editing a
running script can make it execute garbage at the next command boundary. It was
killed and restarted immediately and no damage is visible in `tick.log`, but
the correct order is stop, edit, start.

**The first censored measurement.** `2023[Eu][nan]3[FSR]2` hit the 16,200 s
per-(structure, pressure) wall cap at 65 bar, 3x3x3 replication, and was
recorded TIMEOUT with no loading. This is the failure mode that can make the
whole exclusion argument false while every table still looks healthy: the
collect step never sees a censored structure, so it is indistinguishable from
one that was never queued, and "every structure that could beat the incumbent
was measured" quietly stops being true.

`scripts/audit.py` now separates censored structures into those the geometric
bound excludes anyway and those on the frontier. The policy adopted: a censored
structure whose bound exceeds the best confirmed working capacity is re-run at
a raised cap until it returns a number; one below that bound stays censored and
is excluded by the bound rather than by measurement, and is named as such in
the report. This one has vf0 0.652 and a bound of 155.9 against an incumbent of
186.4, so it is excluded by bound and needs no re-run.

The cap stays at 16,200 s. Raising it globally would tie a core up for longer
on structures that cannot win; the cap file is read fresh per task, so it can
be raised for a targeted re-run when one is actually needed. Expect more of
these as screening works down the bound order into larger cells --
`prep/recensored.txt` is where the ones that matter will collect.

## 2026-08-30 13:06 KST — the modified candidates are ranked and queued

Geometry finished on all 664 non-interpenetrated analogues. The construction
does what the geometric argument said it would: parents at vf0 0.59 come back
at 0.79, parents at 0.52 with three-fold interpenetration come back at 0.84.
The predicted move up the r(vf0) envelope is real as a move in vf0.

`scripts/predmod.py` ranks them two ways, and prints both, because they fail
differently.

- **Surrogate**, the same ensemble as `model.py` trained on measured database
  structures. Its cross-validated MAE of about 8 cm3/cm3 does not transfer:
  every modified structure is out of the training distribution by construction,
  since nothing in the training set has had a net removed. Its top predictions
  run 180-182.
- **Envelope**, wc <= vf0 * r_env(vf0) with r_env the largest working capacity
  per unit void measured in that vf0 bin. No shape assumption, an upper bound
  rather than an estimate, so it cannot rank within a bin and cannot be fooled
  by extrapolation either. Its top values run 189-191.

The union of the two top-120 lists is 195 structures, of which 63 have an
envelope bound above the incumbent 186.4. The union is taken on purpose:
agreement between the two would be reassuring, but disagreement is precisely
where one of them is wrong, and a measurement is what settles that.

**Queued: 195 structures, 390 tasks, about 60 CPU-h, into `queue/w2`.** They go
in the priority queue rather than the bulk one so that the two chain workers
take them while the two pre-chain workers continue down the frontier in
`queue/w1`. The two lines of work are of comparable size — 442 frontier tasks
against 390 modified — and splitting the fleet between them finishes both
rather than serialising one behind the other.

**Why this is worth 60 CPU-h beyond the 63 that could win.** The r(vf0)
envelope is the assumption the entire ceiling argument rests on, and so far it
has only ever been measured on structures drawn from one database built by one
generator. The modified set is the same chemistry with a net removed — a family
produced by a different mechanism, sitting in the same porosity window. If they
obey the same envelope, that is independent support for the one assumption the
claim cannot do without. If they break it, the ceiling argument needed to know
before the report was written and not after.

`reprio.py` now reads `tables/geom_mod.csv` alongside `tables/geom.csv`;
without it a modified structure scores bound = -1 and sorts to the very back of
the queue, which is the opposite of what its porosity deserves.

## 2026-08-30 13:12 KST — the accessibility sweep is complete: the artefact is real, and it does not touch the claim

All 2,135 structures with a geometric bound above 150 are analysed, 2,135 OK,
0 failures. `tables/access.csv`.

**The closed-pore artefact exists in this database under this protocol.**
Charter section 3 pins a protocol with no blocking spheres, so RASPA inserts
methane wherever a methane centre fits, sealed cavities included. Of the 2,135
swept structures, **75 have no percolating channel at all** — every accessible
voxel is in a closed pocket, `ndim 0`, `f_pocket 1.000`. A further 624 percolate
in only one direction and 197 in two; 1,239 are 3-periodic. 218 have more than
2% of their accessible volume sealed.

This is not hypothetical. Two structures already measured are entirely sealed:

    2016[Cu][nbo]3[ASR]25   wc 120.7   f_pocket 1.000  ndim 0
    2022[Cu][tbo]3[FSR]10   wc 116.9   f_pocket 1.000  ndim 0

Both returned a substantial working capacity from GCMC. Neither could be loaded
in a real crystal at any pressure, because there is no path from the outside to
the pore. Their numbers are artefacts of the protocol and they are disqualified
as candidates; they are kept on the record rather than deleted, and they are the
evidence that the diagnostic was worth building rather than a precaution against
nothing.

**And it does not touch the claim.** Two checks, both clean.

- The top twelve measured structures all come back `f_pocket` 0.000-0.002 and
  `ndim 3`. The incumbent `2020[Cu][pts]3[ASR]2` is 0.000.
- **All 230 frontier structures** — every structure whose geometric bound
  leaves it able to beat the incumbent — are covered by the sweep, and every
  one of them is 3-periodic. Their pocket fractions have a maximum of 0.084, a
  99th percentile of 0.009 and a 90th of 0.0002. Not one exceeds 10%.

So the exclusion argument is not holed by closed-pore artefacts: there is no
structure sitting on the frontier whose eventual number would have to be thrown
away, and no leader whose number already should be.

The eight measured structures with more than 2% sealed volume are all well below
the top: the highest is `2013[Zn][nts]3[ASR]1` at wc 148.7 with 16% sealed, and
`2019[Cu][hxg]3[ASR]1` at 130.9 with 52%. They will be reported with their
pocket fractions rather than silently kept or silently dropped.

**Reading adopted, and its limit.** The protocol is pinned and is not modified,
so reported numbers stay the protocol's numbers; the diagnostic disqualifies a
candidate whose capacity is an artefact, it does not correct anyone's number.
The limit worth stating: `f_pocket` is computed on a 0.4 A grid with
6-connectivity and a hard-sphere methane radius, so a channel constricted to
near exactly sigma_CH4 could be called sealed when a real methane would squeeze
through with thermal energy, or the reverse. It is a screen for gross artefacts,
which is what it is used for, and it is not a transport calculation.

## 2026-08-30 13:22 KST — unseeded RASPA runs are not reproducible, and mine were unseeded

Two investigations, one of which changes what has to be run.

**First, a comparison of mine was contaminated and is corrected.** I compared
screening against the charter floor by taking each structure's working capacity
from `tables/t1_wc.csv` — but that table is built from `tables/gcmc_raw.csv`
including the floor-tier rows, so for a structure measured at both settings the
"screening" value I was reading was the floor value. Eight of seventeen deltas
came out at exactly 0.0, which is what tipped me off. Recomputed from
`gcmc_raw.csv` keyed on the cycle count, the true comparison over the 17
structures now measured at both settings is

    delta (2000+10000) - (500+3000):  mean +0.200, sd 1.341, max |.| 3.45

which is consistent with the earlier figure of +0.28 +/- 1.46 on 13 structures
and confirms screening is unbiased for ranking. The conclusion survives; the
way I had just recomputed it did not.

**Second, and this one costs compute.** One structure still showed a delta of
0.0004 after the correction, which is a 1-in-1500 coincidence at the measured
spread, so I tested whether the runs were somehow identical. They are not, and
the test found something more useful:

    2016[Cu][nbo]3[ASR]4, 65 bar, 500+3000, four runs
      no seed   175.4125
      seed 1    175.1283
      seed 2    174.8964
      seed 3    173.2047
      (an earlier archived unseeded run of the same point: 174.0498)

Explicit seeds work — the three seeded runs differ as they should, spread 1.9,
which is a better uncertainty estimate than the block standard deviations give.
But the two *unseeded* runs of the identical point returned 175.41 and 174.05.
**RASPA seeds itself from the clock or the pid when no `RandomSeed` is given**,
so an unseeded result cannot be reproduced from the pinned inputs. Charter
section 3 requires exactly that of every reported value: reproducible from the
pinned inputs alone.

`mktasks.py` emitted an empty seed field for any single-seed wave, so the twelve
confirmation runs I queued at the charter floor are unreproducible. They are not
wrong — they are valid GCMC results and their numbers are sound — but they
could not be regenerated by anyone, including me, and that is a charter
requirement rather than a nicety.

Fixed: `mktasks.py` now always writes an explicit seed, defaulting to 1. The
twelve confirmation structures are re-queued at 2,000+10,000 with seed 1, about
10 CPU-h. The unseeded runs already in flight are kept and reported as an
additional independent sample rather than discarded, since a second draw from
the same distribution is worth having even if its seed was not recorded.

The near-zero delta itself is settled: the raw loadings are genuinely different
at both pressures (146.7006 against 147.0978 at 65 bar, 21.5161 against 21.9137
at 5.8 bar) and it is their *difference* that nearly cancels. With seventeen
structures and a selection effect from looking for it, that is a coincidence at
about the one percent level and not an artefact.

[CHARTER-READ] §3: whether "reproducible from the pinned inputs alone" extends
to the Monte Carlo seed -> it does; a value that cannot be regenerated is not
reproducible in any useful sense, so every confirmation and claim-grade run
carries an explicit seed recorded in the task line.

## 2026-08-30 13:26 KST — the leaderboard moved to 200.3, the turnover is confirmed, and the frontier has collapsed to one bin

Wave 2 has landed enough of the high-porosity end to change the answer.

**A new leader, well above the old one.** 727 structures now measured, up from
597. Top of the screening table:

    2016[Cu][pts]3[ASR]1   200.3   N65 244.2  N5.8 43.9  vf0 0.809  r 247.7
    2015[V][srs]3[ASR]1    198.8   N65 233.6  N5.8 34.8  vf0 0.821  r 242.2
    2015[V][srs]3[FSR]1    196.9   N65 232.0  N5.8 35.1  vf0 0.821  r 239.8
    2018[Y][bcu]3[ASR]1    190.7   N65 250.4  N5.8 59.7  vf0 0.770  r 247.8
    2005[Cu][lvt]3[ASR]1   188.7
    2023[Cu][nan]3[ASR]8   188.7
    2010[Cu][nan]3[ASR]1   188.3
    2005[Cu][pts]3[ASR]2   187.0
    2020[Cu][pts]3[ASR]2   186.4   <- the former incumbent, now ninth

All have f_pocket 0.000 and ndim 3. Eighteen structures have no floor-tier
measurement and are queued for one, 36 tasks.

**This vindicates the retraction of the extreme-value line, and it is worth
being blunt about how close that came to being the reported answer.** The
Generalized Pareto fit gave a right endpoint of 187-189, stable across four
thresholds with xi about -0.6, on a correct uniform sample of 597. The database
maximum is now known to be at least 200.3. Had that fit been reported as a
ceiling — as it was drafted to be — the report would have named a ceiling that
the campaign then exceeded by 11 units using its own data. The hide-the-tail
test caught it beforehand for the right reason: the endpoint was tracking the
sample maximum, not bounding a distribution.

**The turnover in r is confirmed, with complete coverage where it matters.**
Every one of the 42 database structures with vf0 >= 0.85 is now measured. The
bin-local maximum of r there is **213.4**, against 247.8 at 0.75-0.80 and 247.7
at 0.80-0.85. r rises with porosity, peaks in the 0.75-0.85 window, and falls
above it, exactly as the bulk-methane asymptote of 54.76 requires it to
eventually. This is no longer a hypothesis resting on eight measurements.

**The frontier has collapsed to a single porosity bin.** With bin-local
envelopes rather than one global k:

    vf0 bin      db   measured        max r  max bound   still live
    0.05-0.75  12104   578/12104   <= 233.7   <= 175.3            0
    0.75-0.80    219      41/219      247.8      198.1            0
    0.80-0.85    134      48/134      247.7      210.3           51
    0.85-1.01     42   42/42 COMPLETE 213.4      197.1            0

Only 51 unmeasured structures in the world can still exceed 200.3, all of them
in vf0 0.80-0.85, all of them already queued, and closing that set costs
**16 CPU-h**. The 0.85+ bin is excluded twice over: by complete measurement and
by a maximum bound of 197.1 that sits below the leader.

The single-global-k version of the same calculation gives 52 rather than 51, so
the binned envelope is barely doing any work at this incumbent — the two agree,
which is the reassuring case. The distinction still matters for the report,
because a bin-local maximum from a complete sample is a fact and one from a
partial sample is an estimate, and the 0.80-0.85 bin is 48 of 134.

**A pipeline gap that hid all of this, found and fixed.** `exclude.py` reads
`tables/t1_wc.csv`, but the supervisor only ran `harvest.py`, which rebuilds
`gcmc_raw.csv` and nothing downstream. So `t1_wc.csv` had been frozen since the
last time I ran `collect.py` by hand, and every frontier calculation for the
past hours was computed against a stale incumbent of 186.4 while the real
leader was 200.3. Nothing was wrong with the data; the analysis was reading a
snapshot. The supervisor now runs `collect.py` after every harvest and prints
the leaderboard summary into `logs/tick.log`, so a stale leader becomes visible
on every tick instead of silently persisting.

## 2026-08-30 13:34 KST — the database contains exact duplicates, and two of them are in the top three

Checking whether the leaderboard is a set of distinct materials or one motif
appearing repeatedly, I compared the top sixteen by composition and cell. Most
are genuinely distinct — Cu, V, Y, Zn and Co centres across pts, srs, bcu, lvt,
nan, nts and pcu topologies, cell volumes from 5,082 to 36,958 A^3. One pair is
not:

    2015[V][srs]3[ASR]1   wc 198.8
    2015[V][srs]3[FSR]1   wc 196.9

Same cell parameters, same 124 atoms, same fractional coordinates to four
decimals. They are **bit-identical structures under two names**, and they were
screened independently.

Two consequences, and a third thing I get for free.

**N is not 12,499 for statistical purposes.** Every order-statistic statement in
this campaign uses the database size as the population — "about ten structures
should exceed 186.4" is N x (k-0.5)/n. If the population of *distinct*
structures is smaller, those counts are smaller in proportion. `scripts/dupes.py`
is now scanning all 12,499 by a signature of the cell parameters plus a hash of
the sorted, wrapped element-and-coordinate list. That catches exact duplicates
and ones differing only by atom ordering or by a lattice translation; it does
not catch duplicates related by a symmetry operation or an origin shift, so its
count is a lower bound on redundancy, which is the safe direction for every use.

**A claim names a material.** If the best structure has duplicates under other
names, the report has to say so rather than present one of several identical
entries as though it were unique. That check now has an answer to point at.

**And an uncertainty estimate that cost nothing.** Two independent GCMC runs on
a bit-identical pair are a replicate measurement. This one gives 198.8 against
196.9, a difference of 1.9 on a top-tier structure. It is consistent with the
across-seed spread of about 1.0 measured directly on a mid-range structure — the
difference of two draws with sd 1.0 has sd 1.4 — and it is a better-placed
estimate than that one, because it sits at the top of the range where the claim
will be made. If the scan finds more such pairs among measured structures, the
set of them is a real uncertainty estimate at screening cycles, obtained without
spending anything.

I also checked two other suspicious pairs and they are *not* duplicates:
`2005[Cu][lvt]3[ASR]1` and `2005[Cu][pts]3[ASR]2` share the formula
C68Cu4H40N4O16 and have cell volumes of 5,082 and 5,091 A^3, but differ in cell
and coordinates; likewise `2016[Cu][pts]3[ASR]1` and `2009[Cu][pts]3[ASR]2`.
Shared composition and near-equal volume are not enough — the test has to be on
the coordinates.

## 2026-08-30 13:36 KST — the database is 9,127 distinct structures, not 12,499

`scripts/dupes.py` scanned all 12,499 entries. **6,616 of them lie in 3,244
duplicate groups** — 3,168 pairs, 24 triples, 52 quadruples — so the database
holds **9,127 distinct structures and 27.0% redundancy**. The signature is the
cell parameters plus a hash of the sorted, wrapped element-and-coordinate list,
so this is a lower bound: duplicates related by a symmetry operation or an
origin shift are not caught.

**What changes.**

*N in every order-statistic statement.* "About ten database structures should
exceed 186.4" was N x (k-0.5)/n with N = 12,499. The correct population is
9,127, which scales every such count down by 27%. The uniform sample is itself
redundant in the same proportion — 600 entries, 588 distinct — so the sampling
fraction barely moves, but the population multiplier does. All order-statistic
figures will be restated on N = 9,127 and the report will say why.

*Nothing about the leader.* `2016[Cu][pts]3[ASR]1` is in a group of one, as are
`2018[Y][bcu]3[ASR]1` and `2005[Cu][lvt]3[ASR]1`. The claim, when it is made,
names a structure with no duplicate entry. Second and third place are the same
material: `2015[V][srs]3[ASR]1` and `2015[V][srs]3[FSR]1` are one structure,
and the leaderboard must be presented that way rather than as two runners-up.

*Two frontier structures are already answered.* Of the 52 unmeasured structures
that could still beat 200.3, two are bit-identical to structures already
measured — `2013[Zn][nan]3[FSR]9` (= 125.2) and `2020[Fe][tbo]3[ASR]1`
(= 171.6). Both are far below the leader, so the live frontier is 50, and those
two need no compute.

**And a genuine uncertainty estimate, obtained for nothing.** 22 duplicate
groups have more than one independently measured member. Each is a replicate
measurement of the same structure under the same protocol:

    within-group spread of wc:  mean 0.91, median 0.76, max 2.21, n = 22

with examples across the whole range, including the top:
198.8/196.9, 181.8/181.7, 180.4/179.7, 172.2/173.4, 157.8/157.4, 154.4/155.7.

This is a better basis for screening-tier uncertainty than the four-run seed
test on a single mid-range structure, because it is 22 independent pairs spread
over the range where the claim lives. **Screening-tier reproducibility is
+/- 0.9 cm3/cm3**, which is comfortably smaller than the 1.5-unit gaps
separating the current top three and comparable to the gaps below that — so the
screening ranking is trustworthy at the top to about one place, no better.

The duplicates were not a defect in my work — they are a property of the
provided database — but counting them as distinct materials would have been,
and reporting two names for one material as first and second runners-up
certainly would have been.

## 2026-08-30 13:42 KST — the stored block values were molecule counts, not loadings

Checking the leader's raw output before building anything on it, the per-block
values stored in `tables/gcmc_raw.csv` did not agree with the reported loading:
`2016[Cu][pts]3[ASR]1` at 65 bar has vv = 244.19 with blocks of 339.59, 341.16,
338.98, 339.07, 338.08. Every structure showed the same pattern with a
different constant ratio — 1.390 here, 1.207 and 1.312 for two others — which
is the signature of a units problem rather than a numerical one.

It is. RASPA prints the per-block values under **"Number of molecules"**, as raw
molecule counts in the simulation box, and then the whole family of unit
conversions beneath them:

    Block[ 0] 339.59167 ...
    Average                          339.3740000000 +/- 2.0296
    Average loading absolute [molecules/unit cell]        37.7082
    Average loading absolute [mol/kg framework]           24.8847
    Average loading absolute [cm^3 (STP)/cm^3 framework] 244.1943

My `BLOCK` regex anchored on the `cm^3 (STP)/cm^3` label and took the block
lines that followed it, which are the *next* group — the same molecule counts,
repeated ahead of the excess-loading conversions.

**No reported number is affected.** `vv` is parsed directly from its own
labelled line, never from the blocks, and the conversion checks out
independently: 339.374 molecules over the 3x3x1 replication is 37.708 per unit
cell, matching RASPA's own line, and 339.374 molecules in 9 x 5,747 A^3 is
244.2 cm^3 STP/cm^3 by hand. The blocks were a mislabeled diagnostic column,
not an input to anything.

Fixed: `runner.py` now rescales the blocks by the factor that takes the mean
molecule count to the reported loading, so they are in the reported unit and
mean exactly to it. Verified on the leader's archived output: blocks 244.35,
245.48, 243.91, 243.97, 243.26, mean 244.1943 against a reported 244.1943.
Block values already stored are molecule counts and are left as they are, with
this entry as the record of what they mean; `block_unit` now distinguishes the
two cases per row.

**The diagnostic, now that it works.** The leader at 65 bar has a block spread
of 2.2 on 244.2, about 0.9%, over five blocks of 3,000 production cycles each.
That is well converged for a screening run and consistent with the +/- 0.9
reproducibility measured from the 22 duplicate pairs.

**An incidental confirmation of charter §2.** The same output block shows
`Average loading excess [cm^3 (STP)/cm^3 framework] = 176.5572` against an
absolute 244.1943 — a 28% difference, produced entirely by the
`HeliumVoidFraction 1.0` that the protocol does not pin. §2 requires absolute
loading precisely because the excess number is not reproducible from the pinned
inputs, and the run output demonstrates the size of what that would have cost.

## 2026-08-30 13:46 KST — the exclusion had a 1% margin where it mattered; it now has 10%

The ceiling argument excludes a porosity class by saying a structure at the top
of it would need a working capacity per unit void that has never been observed.
I had been reporting which bins are excluded without reporting **by how much**,
and the answer is uncomfortable in exactly one place:

    vf0 bin      r needed to beat 200.3    vs global max r = 247.8
    0.05-0.30            667.7                    +169.5%
    0.30-0.40            500.8                    +102.1%
    0.40-0.50            400.6                     +61.7%
    0.50-0.60            333.9                     +34.7%
    0.60-0.65            308.2                     +24.4%
    0.65-0.70            286.2                     +15.5%
    0.70-0.75            267.1                      +7.8%
    0.75-0.80            250.4                      +1.1%   <-- this one
    0.80-0.85            235.7                      -4.9%   (on the frontier)
    0.85-1.01            198.3                     -20.0%   (fully measured)

A structure at vf0 0.80 needs r = 250.4 to beat the leader, and the largest r
ever measured is 247.8. **That is a 1.1% margin, and 1.1% is not an
exclusion** — it is a coin flip dressed as an argument, resting on 41
measurements out of 219 in that bin.

The fix is to measure rather than argue. `exclude.py` now carries an explicit
`MARGIN_K`, set to 1.10: a structure is excluded only if beating the leader
would require r more than 10% above the largest ever measured. That criterion
puts every structure with vf0 > 0.735 in the "measure it" set — **370
unmeasured structures, 115 CPU-h**, and all 370 are already in the queue, at
the head of the bound ordering. Against 262 CPU-h consumed of 1,610, buying a
tenfold better margin for 115 hours is not a close call.

What the +10% criterion then says, if it holds: no structure in the database
outside the measured set can beat the leader unless it achieves a working
capacity per unit void more than 10% above anything observed across ~1,100
measurements spanning the whole porosity range. That is a claim with a number
attached, which the previous version was not.

The bins below 0.70 keep margins of 15% to 170% and are excluded comfortably;
their exclusion was never the weak part and is not affected.

[CHARTER-READ] §2: how far "near the achievable maximum" has to be defended ->
by a stated margin rather than a binary exclusion, with the margin chosen so
that closing it costs a fraction of the remaining budget rather than by
whatever the current measurements happen to allow.

## 2026-08-30 13:50 KST — the margin is now calibrated rather than chosen

Having just set MARGIN_K to 1.10, I had no basis for 1.10 beyond it sounding
safer than 1.01. The whole ceiling claim reduces to whether that number is big
enough, so choosing it by taste would make the claim a matter of taste. It can
be measured instead.

One porosity bin has **complete coverage**: every one of the 42 database
structures with vf0 >= 0.85 has been simulated, so its true maximum r is known
rather than estimated. `scripts/margincal.py` subsamples that bin at the
coverage fraction the *incomplete* bins actually have and compares each
subsample's maximum to the known true maximum. That is precisely the error
MARGIN_K has to cover.

    bin          db  measured  frac    p50     p90     p99   worst
    0.85-1.01    42  42 COMPLETE 0.20   7.2%   15.3%   18.1%   24.8%
                                 0.30   2.0%   14.6%   16.0%   18.9%
                                 0.50   1.6%    7.2%   12.9%   16.0%
    0.80-0.85   134        55    0.20   5.2%   12.6%   16.2%   18.6%
    0.75-0.80   219        41    0.20   3.7%    6.5%    7.6%    8.7%
    0.70-0.75   473        23    0.20   3.8%   10.3%   12.8%   15.7%

The incomplete bins are shown as a consistency check but understate the gap,
because their "true" maximum is only their own partial maximum. The complete
bin is the one to trust.

The partially measured bins sit at 19-41% coverage. At 20-30%, the complete
bin's shortfall is **14.6-15.3% at the 90th percentile and 16.0-18.1% at the
99th**. So MARGIN_K = 1.10 was roughly a 90th-percentile margin — a one-in-ten
chance of having excluded a bin that contained a winner — while being written
up as though it were an exclusion.

**MARGIN_K raised to 1.20**, which covers the measured 99th percentile. Every
structure with vf0 > 0.674 is now measured rather than argued away: 1,026
unmeasured structures, 318 CPU-h. 978 were already queued; the remaining 48
were appended and the queue re-sorted, and the screening front now runs from
bound 204.0 downward.

Cost check: 263 CPU-h consumed of 1,610. The +20% frontier at 318 CPU-h, the
confirmation and modification work in `queue/w2` at roughly 230, and a claim
tier of order 70 bring the campaign to about 880 CPU-h — comfortably inside the
budget, and about 25 hours of wall time at the 24 cores currently running
against 155 hours remaining.

**The criterion is self-tightening**, which is worth noting because it means
this is not an arms race. Measuring the +20% set raises the coverage fraction
of exactly the bins whose margin is weak, which lowers the shortfall the margin
must cover, which shrinks the set. At 50% coverage the 99th-percentile gap is
already down to 12.9%.

## 2026-08-30 13:52 KST — de-duplicating the queues; I emptied them first, then did it properly

**The check that started it.** If removing a net from structure A produced
something identical to database structure B, the "modification" would be a
rediscovery rather than a new material. Signing all 664 modified structures and
comparing against `tables/dupes.csv`: **0 are identical to any database entry**,
so every one is genuinely new.

The same signatures showed the modified set carries its own redundancy: **235
duplicate groups covering 486 of the 664**, so there are only 413 distinct
modified structures. That is inherited — duplicate parents give duplicate
children — and it means part of the 195-structure modification screen was
buying the same number twice.

**Then I broke the queues.** The de-duplication pass walked every task line,
collecting the signatures it had already seen and blocking any later task whose
structure matched one. It blocked 4,025 tasks — which was every open task in
both queues. `queue/w1` and `queue/w2` both went to **0 open**.

The bug is `reprio.py`'s own mechanism. Re-prioritising works by claiming an
unclaimed task and appending the same task again at the end, so after any
re-queue **every live task has a claimed twin earlier in the file**. My loop
added the twin's signature to the covered set and then blocked the live copy as
a duplicate of it. A claimed line does not mean the work will be done; it means
the work was moved.

Caught immediately, because the pass prints what it blocked and the queue depth
is one command away. The claim files I had written carried a distinctive
message, so undoing was exact: 4,025 removed, 3,321 open restored in `w1` and
704 in `w2`, against 3,327 and 708 before — the six missing were claimed by
real workers in the interval, which is correct behaviour and not loss.

**No workers were lost.** The queues were empty for about three minutes and the
idle tolerance in `queue/w1/idle_exit` is 1,800 s. All four running jobs
survived. That margin was luck rather than design: had the chain been in a
phase where it writes 60 s into the priority queue's `idle_exit`, three minutes
would have cost the slots, and slots here take hours to regain.

**Done correctly**, the pass considers only *unclaimed* tasks, so a moved task
never covers itself: **1,508 live tasks kept, 2,516 blocked as exact
duplicates, about 390 CPU-h saved.**

**Verified afterwards rather than assumed.** The +20% margin set is 1,020
entries carrying 840 distinct signatures, 824 of them not yet measured. Of
those 824, 812 have a live task and the remaining 12 are claimed by named
worker processes on bnode18 and bnode19 — in flight, not lost. Coverage of the
set the ceiling argument depends on is complete.

The general lesson, and it is the second time this workspace has taught it: a
queue operation that reasons about which tasks are "already handled" has to
know the difference between a task that was *done*, one that is *being done*,
and one that was *moved*. The claim file is the same in all three cases and the
content is the only thing that distinguishes them.

## 2026-08-30 13:55 KST — the modified candidates were never accessibility-checked; now they are

A gap on the critical path: `scripts/access.py` had `db/` hard-coded in its one
call to `read_cif`, so it could only analyse database structures. Every
accessibility statement in this campaign — including "all 230 frontier
structures are 3-periodic" — covered database entries only, while 664 modified
candidates were queued for GCMC with no accessibility check at all. A modified
structure entering the Claim would have carried an unexamined pore-blocking
risk, and removing a net can in principle close a channel as easily as open one.

Patched to `cifio.find_cif`, which resolves `mod/` before `db/`, and run over
all 664:

    664 analysed, 664 OK
    ndim 3: 639    ndim 2: 15    ndim 1: 10    ndim 0: 0
    f_pocket > 2%: 0     fully sealed: 0

Not one modified structure has a closed-pore problem. That is the physically
expected direction — removing an interpenetrating net opens the pore network
rather than sealing it — but "expected" was exactly the reasoning that left
these unchecked, and the database sweep found 75 fully sealed structures among
2,135, so the failure mode is real in this database and was worth ruling out
rather than assuming away.

**Where the modification route stands.** Ten modified structures measured:

    2019[Zn][utp]3[ASR]2__1of2    193.9
    2015[Zn][pcu]3[FSR]8__1of2    192.7
    1999[Ag][ths]3[ASR]1__1of2    192.5
    2015[Zn][pcu]3[ASR]9__1of2    192.4
    1997[Cu][dia]3[ASR]1__1of3    190.9
    1997[Cu][dia]3[FSR]1__1of3    190.3
    2019[Ni][dia]3[FSR]2__1of2    186.8
    2019[Ni][dia]3[ASR]2__1of2    186.8

all with f_pocket 0.000 and ndim 3, all below the database leader of 200.3, and
**none exceeding the r(vf0) envelope measured on database structures**. The
envelope continues to hold on a family built by a different mechanism, which is
the independent support the ceiling argument could not otherwise get.

**Three more free replicates fall out of this.** The pairs above are duplicate
modified structures inherited from duplicate parents, measured independently:
192.7 against 192.4, 190.9 against 190.3, and 186.8 against 186.8 — spreads of
0.3, 0.6 and 0.0. Together with the 22 database pairs (mean 0.91) they put
screening-tier reproducibility firmly at about +/- 1, now confirmed at the top
of the range on a second family.

Still missing, and it is the number that matters for charter §2: not one parent
has been measured yet, so there is still no paired before-and-after. The 146
parent runs sit behind the floor-tier confirmations in `queue/w2`.

## 2026-08-30 13:58 KST — the de-duplication was tier-blind and had blocked the confirmation tier

Checking whether the leaders had picked up their floor-tier numbers yet, the
answer was no, and the reason was mine. Of the floor-tier tasks in `queue/w2`,
**56 carried a `dedup:` claim** — my own duplicate suppression had blocked them.

The key I de-duplicated on was the structure signature alone. A structure with a
live screening task therefore "covered" its own floor-tier task, and the
floor-tier run was blocked as a duplicate of it. **A run at 2,000+10,000 cycles
is not a duplicate of a run at 500+3,000 — it is the measurement the charter
admits and the other one is not.** The suppression was quietly cancelling
exactly the tier the Claim depends on, while the leaderboard kept moving and
nothing looked wrong.

Fixed by keying on the measurement rather than the structure: signature,
initialization cycles, production cycles, seed, and pressure. Two runs of one
structure at different cycle counts are different measurements; only the same
structure at the same cycles, seed and pressure is redundant. All 2,516 previous
dedup blocks were removed and the pass redone: **3,064 live tasks kept, 946
blocked**, against 2,516 blocked under the tier-blind key. The saving is
smaller and it is the real one.

Queue depth after the fix: 2,563 open in `w1`, 501 in `w2`, and the database
leaders now have live floor-tier tasks again.

**A second gap the check exposed.** The confirmation list `t2_wave2.txt` was
built when the top of the table was all database structures. Modified
candidates have since climbed into it — ten of the current top eighteen are
modified — and none of them had a floor-tier task queued at all. A modified
structure cannot enter the Claim on a screening number any more than a database
one can.

Nine structures now queued for the floor tier, de-duplicated by signature so
that identical modified twins are not measured twice:
`2015[Cd][bto]3[ASR]1__1of2`, `2019[Zn][utp]3[ASR]2__1of2`,
`2015[Zn][pcu]3[FSR]8__1of2`, `1999[Ag][ths]3[ASR]1__1of2`,
`2018[In][dia]3[FSR]2__1of3`, `1997[Cu][dia]3[ASR]1__1of3`,
`2002[Cu][dia]3[ASR]1__1of2`, `2019[Ni][dia]3[FSR]2__1of2`,
`2020[Fe][nuc]3[ASR]1`. `queue/w2` re-sorted with 35 confirmation-tier
structures at its head.

The pattern in both of today's queue mistakes is the same: an optimisation that
reasons about which work is redundant needs to know precisely what makes two
tasks the same, and "same structure" is not it. The first version treated a
moved task as a done one; the second treated a different measurement as a
repeat. Both were caught by asking what the queue actually contained rather
than trusting the count the pass printed.


## 2026-08-31 04:05-04:50 KST — resumption after the 13.98 h harness outage

**DONE** Reconciled against the cluster, which never stopped. 1,835 structures
now have both pressures (1,700 at the last session's end). The leaderboard moved
substantially: `2021[Cu][sql]2[ASR]6` at 208.0 replaced `2016[Cu][pts]3[ASR]1`
at 200.3, and seventeen of the top twenty-five are interpenetration-removal
analogues built by this campaign.

**DONE** Claim tier submitted. `scripts/claim_tier.py --go` selected the four
structures within 8.0 of the leader — all with f_pocket ≤ 0.0005 and ndim 3 —
and emitted 24 tasks at 10,000+50,000 with three explicit seeds, ~62 CPU-h.

**DECISION** The claim tasks were moved out of the fresh `queue/w3` and appended
to `queue/w2`, and `queue/w3` retired to `queue/w3_retired`. Reason: the chain
in `scripts/worker_chain.sh` is re-read only *between* qworker invocations, and
a qworker given a non-last queue runs until that queue is empty. The workers
already dispatched were inside `queue/w2` with ~180 open tasks, so a new
top-priority queue would not have been looked at for something like sixteen
hours of wall. `scripts/reprio.py queue/w2` then put the 24 claim tasks at the
head of the unclaimed tail. Verified by listing the unclaimed lines directly,
not by reading the head of `tasks.tsv` — after any re-queue the head of that
file is all claimed twins.

**DONE / correction to the harness** `scripts/qworker.py` had a real defect:
its two wall-time guards tested `elapsed > MAX_WALL` before claiming the next
task, with no reserve for how long that task would take. A worker with ten
minutes left would therefore claim a twelve-hour claim-grade task and be killed
by PBS mid-run, losing the work *and* leaving a claim file that looks exactly
like coverage. It now reserves `<qdir>/wall_cap` seconds. Reserve is zero where
the file is absent, so screening behaviour is untouched; `queue/w2/wall_cap` =
28800 and `queue/w4/wall_cap` = 16200.

**DONE** Floor tier queued for the 27 structures in the top 40 that had neither
a floor measurement nor a floor task anywhere (54 tasks).

**DECISION — the modification family is closed by construction.** The 664
first-wave analogues came from the 697 parents whose *predicted* post-removal
vf₀ fell in 0.74–0.88. That is a cost heuristic, and it is also the exact
objection a reader should raise against a ceiling claim resting on it: the route
was applied only where it was expected to pay, so a negative result inside the
window says nothing about outside it. `scripts/mod2.sh` built the remaining 401
all-3-periodic interpenetrated parents and measured their true geometry into
`tables/geom_mod.csv`; `scripts/mod2q.py` queued the 315 that the +20% r-margin
cannot exclude into `queue/w4` (~98 CPU-h). Their vf₀ is 0.642–0.913 with median
0.710, so the original window was well placed — but **18 sit on the bare
frontier** and were argued away rather than measured until now.

**RESULT — the modification route works, and by a large margin.**
`scripts/modeval.py` on 250 parent/analogue pairs: mean **+87.1**, median
**+90.5**, maximum +162.6, and removal helped in **241 of 250**. This is the
answer to charter §2's "by what means".

**RESULT — k moved, and a modified structure moved it.** Maximum r = wc/vf₀
over everything measured is now **261.7**, held by
`2020[Zn][pcu]3[ASR]7__1of2`; the database maximum is 254.0. Six analogues
exceed the database r envelope for their own bin by up to +6.0%. The exclusion
argument is consequently restated over the *union* of the two families. Stating
it over the database alone would have been unsound from the moment §3-admissible
modified structures entered the leaderboard, and it is worth recording that this
was not caught by suspicion but by running `modeval.py`'s envelope test, which
exists precisely to falsify the envelope.

**RESULT — the database frontier is empty.** `scripts/exclude.py` against the
new leader: at k = 254.0 there are **zero** unmeasured database structures whose
bound vf₀·k reaches 208.0. Under the adopted +20% margin, 512 remain, all
queued, 159 CPU-h.

**NEXT** Claim-grade runs are the gating item. Do not poll: `logs/tick.log` is
written every ten minutes by the supervisor, and spend — not compute — is the
binding budget, so it is paid per turn rather than per CPU-hour.

**Budget at this point.** Spend $170.17 / $280 (60.8%); compute 638.9 / 1,610
CPU-h by `scripts/cpuacct.py` and 510.6 by the scheduler meter, a 1.25×
discrepancy where it was 2× yesterday; tokens 6.46M / 32M.


## 2026-08-31 04:30 KST — two harness notices, and what they change

**[CHARTER-READ] §3: the MakeGrid retraction.** The harness withdrew its
2026-08-30 notice that the provided binary contains no MakeGrid code path; it
had searched the 18 KB driver rather than `lib/libraspa`, and grids exist and
work here. **This report carried that statement as fact and it is corrected in
place rather than deleted** (REPORT.md §2.1 and §3, STATE.md operational
facts). The ambiguity §3 leaves is only whether to use grids now that they are
available — "energy grids permitted for screening" is permissive, not
directive. Reading adopted: **do not adopt them**, and record it as a judgement
rather than as an impossibility. A screening structure costs ~0.31 CPU-h for
both pressures, against a per-framework tabulation that is a substantial
fraction of that, so the realistic saving is ~2× and not an order of magnitude;
compute is not the binding budget (638.9 of 1,610 used, ~970 left, ~260
committed) whereas spend is (63% of cap); and §3 would require validating
grid-versus-direct agreement before any grid number could enter the report,
which costs turns from the budget that actually binds. This flips if the
frontier reopens and demands thousands more screening runs.

**[CHARTER-READ] §4: login-node execution.** The compliance notice states that
simulation is running directly on the login node and must stop. **Checked: none
of it is mine.** `ps -u Bei` is shared across all sibling replicates on this
account, and the `simulate` processes under `timeout 86400` on bnode0 belong to
rep05 and rep08 workspaces, which §4 forbids me to touch. The only rep02
process on the login node is `scripts/supervisor.sh`, which sleeps ten minutes
between ticks and runs harvest/collect for seconds — orchestration, not
simulation, and it is the mechanism §4's own cost-discipline clause asks for
("poll job state with scripts that sleep and return one-line summaries").
The ambiguity is whether §4's "no interactive jobs over 30 min" covers a
long-lived orchestration loop. Reading adopted: it does not, because the clause
sits under cluster etiquette and the harm it names is unaccounted compute and
starved queue positions, neither of which a sleeping loop causes. **But I am
recording against myself that two *analysis* passes did exceed it** — the
`access.py` accessibility sweep on 2026-08-30 ran for hours on the login node,
and `scripts/mod2.sh` ran ~5.5 min today. The sweep should have gone through
the scheduler. All future analysis passes expected to exceed 30 minutes will.

**RUNNING** Claim tier confirmed turning: `2012[In][dia]3[ASR]4__1of2` seed 1 at
both pressures, 10,000+50,000, on bnode18. 24 claim tasks total, 2 in flight,
no results yet — a claim-grade pressure point on these structures runs 2–4.5 h.


## 2026-08-31 06:20 KST - the floor tier resolves, and it resolves to a tie

**RESULT** With 61 structures now measured at both screening and floor cycles,
the floor-tier top five span 199.9-199.0 against a reproducibility of +/-0.9:
`2016[InCo][pts]3[ASR]1__1of2` 199.9, `2016[Cu][pts]3[ASR]1` 199.6,
`2015[Cd][bto]3[ASR]1__1of2` 199.3, `2018[Zn][pth]3[ASR]2__1of2` 199.3,
`2018[Zn][pth]3[ASR]1__1of2` 199.0. **Four of the five are analogues this
campaign built.** REPORT section 1 now names the tie rather than a winner: a
leaderboard resolved to one material at spacings of 0.3 would be reporting
noise as a result.

**RESULT - the weakness section 6 flagged is closed.** The screening-to-floor
comparison was 17 structures and mostly mid-range, which is the wrong place to
test a device used to rank the top. It is now 61 structures: overall
+0.009 +/- 0.974, above 175 -0.096 +/- 0.853 (n=39), and **above 190
-0.18 +/- 0.93 (n=19, range -1.56 to +1.67)**. Screening is unbiased for
ranking at the top of the range as well as in the middle, and its spread agrees
with the independent +/-0.9 from duplicate groups.

**DECISION** The claim tier is widened from 4 structures to 10. It was selected
against the *screening* leader 208.0 with a margin of 8.0, which excluded
`2016[InCo][pts]3[ASR]1__1of2` by 0.1 - and that structure is now the best
floor-tier number in the campaign. Six floor-tier leaders were added at seed 1,
and `scripts/reseed.py` re-ordered so that every one of the ten gets a
claim-grade number at seed 1 before any structure gets seed 2. Cost is ~25
CPU-h against ~930 remaining; compute is not the binding budget and this buys
the one thing the Claim actually needs, which is claim-grade numbers on the
structures that are actually tied.

**RESULT - claim-tier seed reproducibility, low-pressure leg.** Three seeds of
`2012[In][dia]3[ASR]4__1of2` at 5.8 bar returned 39.449 / 39.525 / 39.483, a
spread of 0.076; two seeds of `2014[Zn][hms]3[ASR]1__1of2` gave 45.904 / 45.838
and of `2021[Mn][dia]3[FSR]1__1of2` 38.56 / 38.42. At 17x the screening cycles
the seed spread is an order of magnitude below the +/-0.9 that governs the
screening tier, as it should be. No 65-bar claim point has finished yet; the
high-pressure leg is several times slower and it is the pole.


## 2026-08-31 07:45 KST — the first claim-grade number, and it is a structure this campaign built

**RESULT** `2014[Zn][hms]3[ASR]1__1of2` at **203.66 ± 0.23 cm³/cm³**, three
independent seeds at 10,000+50,000 (203.40 / 203.81 / 203.76), N65 249.4,
N58 45.9, block sd 0.94, 1.7 CPU-h per seed. This is the first number in the
campaign that satisfies §3 for a Claim, and REPORT §1 is rewritten from it.

**The across-seed spread at claim grade is 0.23**, against ±0.9 at screening
tier and a block sd of 0.94 on the same runs. The ladder behaves as it should:
17× the cycles buys roughly four times the reproducibility, and the block
standard deviations overestimate run-to-run spread, as five blocks inside one
Markov chain will.

**The paired statement for the claimed material specifically.** The parent
`2014[Zn][hms]3[ASR]1` measures 75.4 (screening); deleting one of its two
**identical** nets — exactly half the atoms, 130 to 65, vf₀ 0.591 to 0.795,
density 0.861 to 0.431 — gives 203.66. **+128 cm³/cm³ in one step**, on a
structure whose charge balance follows by construction because the deleted
component is a complete net sharing no bond with the one kept. Pore network
3-periodic, sealed-pocket fraction 0.000.

**Also complete:** `2016[InCo][pts]3[ASR]1__1of2` at 200.21, claim grade, one
seed — the structure the original claim-tier selection had excluded by 0.1 and
which the widened selection recovered. The floor tier and the claim tier now
agree independently that the top of this database sits just under 200 and that
the modification route clears it.

**STILL OPEN** The screening leader `2021[Cu][sql]2[ASR]6` (208.0) has its three
low-pressure claim points done and no high-pressure point yet; so does
`2012[In][dia]3[ASR]4__1of2` (204.2). The 65-bar leg runs several times longer
than the 5.8-bar leg and is the pole for every finalist. If either stands up,
§1 is rewritten again.

**DECISION** 335 structures that sat above the +25% exclusion threshold and in
no queue were queued (104 CPU-h) and `queue/w1` re-ordered by geometric bound,
top bound now 252.7. The intent is to close the whole +25% band by measurement
rather than by the calibrated margin. Compute is at 43.6% with ~900 CPU-h left
and is not the budget that binds; session turns are what cannot be bought, so
the band was queued in one pass rather than by tightening MARGIN_K iteratively.

**NOTE ON A BROKEN COMMAND** The first attempt to write this entry was sent as a
heredoc inside a single-quoted ssh argument and was destroyed by the apostrophe
in "RASPA's" — the known failure mode already recorded in STATE.md, which I
walked into anyway. Nothing was written and no file was corrupted; the fragment
lines were interpreted by the remote shell as commands and failed harmlessly.
Recorded because §6 asks for errors on the record, not only the interesting ones.


## 2026-08-31 11:20 KST — 886 tasks lost to a filesystem burst, and what it cost

**ERROR (infrastructure, not mine, but on the record).** The tick log went from
2 non-OK GCMC rows to 891 in one interval. All 886 new failures are
`FileNotFoundError`, all with `wall 0.0` — they failed before doing any work —
and they are spread across ten worker processes on both compute nodes.

**What it is not.** Not structure-specific: 250 of the affected structures are
modified analogues and **197 are plain database entries**, which rules out the
first hypothesis that `cifio.find_cif` was failing to see newly written files
in `mod/` and falling back to a `db/` path that does not exist for a `__1of`
name. Not code: `mkrun.build` reproduces cleanly on the login node for three of
the failing structures, returning correct replication counts. Not ongoing: the
count has been static at 891 for two ticks and no worker is still producing
them.

**What it most likely is.** A blip on the shared filesystem. Instant failure,
both families hit indiscriminately, self-limiting, on a cluster whose login
node already refuses ssh under load often enough to be recorded in STATE.md.

**What I could not determine, and why.** `runner.py` truncated the exception at
exactly 80 characters, which cut the path off at
`'/home1/users/Bei/ws/rep` — one character before the digits that would have
said whether the missing file was the structure, the binary, or the working
directory. **That is a defect in my own instrumentation**, and it is the reason
this entry says "most likely" rather than names the file. Truncation is now 240
characters in both `runner.py` and `qworker.py`.

**Fixes applied.**
1. `runner.run_one` now retries once, after a 20 s sleep, when and only when the
   failure is `FileNotFoundError` or `OSError`. A structure that genuinely fails
   still fails once and is recorded. The body moved to `_run_one_once`.
2. All 886 lost measurements are re-queued (`scripts/requeue.py`, which queues
   exactly those (structure, pressure, init, prod, seed) keys that have a failed
   row, no OK row, and no live task) and `queue/w1` re-ordered by bound.

**Cost.** No result is wrong because of this and nothing had to be retracted —
the failures are recorded as EXC rows in `tables/gcmc_raw.csv` and were never
mistaken for measurements. What it cost is throughput: 886 screening tasks,
about 137 CPU-h of queue position, at a moment when only three PBS jobs were
running.

[ESC: infra / 886 tasks failed instantly with FileNotFoundError across both compute nodes in one interval on 2026-08-31, hitting database and modified structures alike and then stopping; was there a shared-filesystem event on bnode18/bnode19 around 09:00-11:00 KST?]


## 2026-08-31 12:15 KST — the screening leader's claim run was dead and its claim file hid it

**ERROR (mine, in the sense that I had already identified the mechanism and did
not finish closing it).** `2021[Cu][sql]2[ASR]6` — the 208.0 screening leader,
the one number in the campaign above the Claim — had its three high-pressure
claim-grade legs claimed by a worker on bnode18 whose PBS job then hit its
walltime mid-run. The output file's last write was **06:34, five and a half
hours before I looked**, with three cycles logged out of 50,000. Nothing would
ever have finished it, and the claim file was indistinguishable from a task
being worked on.

**This is the exact failure `qworker`'s missing wall-reserve causes**, which I
found and patched at 04:20 today — but a patch to `qworker.py` only reaches
processes that start afterwards, and the workers holding these tasks had been
running since the previous day. I recorded the fix and did not ask which
already-running workers were still exposed to the bug it fixed.

**Detection.** Directory mtime is useless here: RASPA appends to a file, which
does not touch the directory, and `runner` deletes the whole scratch tree on
success, so a completed task and a dead one look alike from outside.
`scripts/rescue.py` instead walks every file under each scratch subtree, takes
the newest write for each (structure, pressure leg), and calls a claim-tier
measurement stale if nothing has been written for longer than a threshold.

**Recovered.** Four claim measurements re-queued at the head of `queue/w2`: all
three seeds of `2021[Cu][sql]2[ASR]6` at 65 bar and seed 1 of
`2021[Mn][dia]3[FSR]1__1of2`, the latter having no scratch directory at all.
Six others (48–82 min quiet) were left alone as probably live; the threshold was
raised to 150 minutes rather than guess, and they can be rescued later if they
are still missing.

**What it cost, stated plainly.** About 5.5 h of wall on one claim-grade leg,
and — more importantly — it delayed the one measurement that can still change
the Claim. It changed no result: nothing dead was ever mistaken for a
measurement, because a task that never finishes produces no row.

**The general lesson for the record.** A claim file in this queue design carries
three meanings already (done, being done, moved by reprio) and this incident
adds a fourth: *abandoned*. Only the contents of the scratch tree distinguish
the fourth from the second, and only for as long as the tree survives.


## 2026-08-31 14:20 KST — CORRECTION: the ceiling is not exceeded by modification

**RESULT** `2021[Cu][sql]2[ASR]6` returned **207.14 cm³/cm³ at claim grade**
(10,000+50,000, seed 1; N65 243.8, N58 36.7, block sd 0.48). Its screening value
was 208.0, so the screening tier was accurate to 0.9 on the structure it
mattered most for. Seeds 2 and 3 are running.

**CORRECTION on the record, per §6.** From 07:45 to 14:20 today REPORT §1 said
that the database's own ceiling was not the protocol's ceiling and that it could
be exceeded by interpenetration removal. **That is wrong.** The best modified
structure, `2012[In][dia]3[ASR]4__1of2` at 204.17 ± 0.14 over three seeds, is
**3.0 cm³/cm³ below** the best database structure — a gap ten times the largest
across-seed spread measured at this tier (0.23). The claim was made when the
best *admissible* number happened to belong to an analogue, while the one number
above it was screening-tier and therefore not reportable. It was true of the
evidence admissible at the time and false of the evidence now, which is the
weaker of the two ways to be wrong but is still being wrong, and the earlier
text is corrected in place rather than deleted.

**What survives, and it is not nothing.** The paired result is unchanged and
does not depend on the ranking: +87.1 mean over 250 parents and their own
analogues, ahead in 241 of 250, and one case going 75.4 → 203.66 at claim grade.
Eight of the ten claim-grade structures are analogues and they hold places two
through five. The largest working capacity per unit van der Waals void measured
anywhere, 261.7, still belongs to an analogue rather than to a database entry.

**Why it falls short, stated in the terms the ceiling argument uses.** Removing
a net buys *r* and lands the analogue near vf₀ 0.76; the winner sits at vf₀
0.819 and turns a merely-good r of 252.9 into more volume than the analogues can
reach. wc = vf₀ · r needs both, and the modification improves one at the price
of not improving the other. **A modification that raised vf₀ without giving back
r is the thing to try next, and this campaign did not find one.** That is a more
useful sentence for a successor than the one I had written.

**Why the winner wins.** Not by adsorbing more at 65 bar — 243.8 is unremarkable
here, and `2014[Zn][hms]3[ASR]1__1of2` holds 249.5 and loses. It wins on the
bottom of the cycle, N(5.8) = 36.7 against 38–46 for the rest. Working capacity
is a difference and the structure that gives up least at the delivery pressure
takes it.


## 2026-08-31 16:10 KST — the 75% spend warning, and what it changes

**The §5 Rev 24 warning has fired: $209.97 of $280, 75.0%.** The clause asks
for three things at this point, and here is the position against each.

1. *Prioritize claim-grade verification of the current best candidate over
   further exploration.* Already in force. `2021[Cu][sql]2[ASR]6` seeds 2 and 3
   at 65 bar are live and writing, and they sit at the head of `queue/w2`, which
   is first in `queue/CHAIN`. The 2,708 open screening tasks in `queue/w1` —
   the +25% frontier-closure band, which is exploration — are behind them and
   will only be touched by a worker that finds `queue/w2` empty. No further
   exploration has been queued since the warning and none will be.
2. *Keep REPORT.md continuously current.* It is. §1 carries a claim-grade
   number with its tier, its seed count and its missing across-seed spread
   stated rather than implied; §5 carries the ceiling position restated against
   it; §6 lists the framing I got wrong today. A stop at this moment leaves a
   complete and defensible report.
3. *An honest report of a verified intermediate result outranks an ambitious
   campaign with no filed claim.* Taken literally. The Claim is filed on one
   seed rather than held back for three, with the single-seed status printed in
   the Claim itself.

**What the remaining budget is for, in order.** The leader's two outstanding
seeds; then, if they land, one rewrite of §1 to carry an across-seed
uncertainty; nothing else. Waiting turns cost about $0.14 and turns that write
report sections cost $1–2, so roughly $70 buys either a great many hours of
waiting or a handful more rewrites, and the plan spends it on the first.

**What I am deliberately not doing with it.** Not closing the +25% band by
measurement — it is queued and would be finished by the cluster if throughput
returned, but it is insurance against a 25% error in a quantity whose measured
maximum already leaves the frontier empty, and §5 says exploration yields to
securing the claim. Not queueing further modification routes. Not filing early
either: the deadline is five days out, waiting is nearly free, and the leader's
seeds are the one thing that can still change the Claim.

**Throughput, for the record.** One PBS job running and eleven pending and
starving, down from five running this morning; two jobs hit their walltime and
the sibling replicates executing simulations directly on the login node are,
per the 2026-08-31 compliance notice, why queue positions elsewhere starve. Five
claim legs abandoned by those two deaths were detected by `scripts/rescue.py`
and re-queued. This is not something I can fix from inside my workspace.


## 2026-08-31 17:20 KST — the Claim rests on the one seed that escaped the wall cap

**FINDING, and it matters more than it first looks.** The two "stalled" seeds of
`2021[Cu][sql]2[ASR]6` at 65 bar are not stalled. They are recorded **TIMEOUT at
exactly 16,200.0 s** — the *screening* wall cap — while the seed that succeeded
took **30,480 s**. Six tasks in the whole campaign carry TIMEOUT and every one is
at exactly 16,200.0, including three claim-grade legs and one floor-tier leg.

**Why the cap was wrong.** `runner.wall_cap` scales the cap with cycle count and
bounds it by `queue/wall_cap_claim` (43,200 s), which would have given these runs
43,200. It returned 16,200 instead, which is what the function returns when the
scaling branch is absent — i.e. the workers that ran them were **long-lived
processes holding an older `runner.py` in memory**. This is the same class of
fault as the `qworker` wall-reserve bug this morning: a Python worker imports
once and keeps whatever code it started with, and this cluster's workers live for
a day or more.

**Why my earlier "stale run" diagnosis was also wrong, and the correction.**
I inferred abandonment from a scratch tree that had not been written to for
hours. `simulation.input` sets **`PrintEvery 50000`**, so a claim-grade run
writes its header and then is silent for essentially its entire eight hours.
Silence proves nothing here, and `scripts/rescue.py`'s premise — "a live run
cannot be silent that long" — is false for the claim tier. It is still useful for
screening, where prints are frequent; for the claim tier it will re-queue live
work. That over-queues rather than loses work, so it failed safe, but the
threshold is not evidence and this entry says so.

**Fix applied.** `queue/wall_cap` raised 16,200 → 36,000 s, and
`queue/w2/wall_cap` (the qworker claim reserve) 28,800 → 43,200. The cap file is
re-read on **every task**, so this reaches the old-code workers too: they return
`base` unscaled, which is now 36,000 and comfortably above the 30,480 s the
successful run needed. Cost of the looser cap is that a pathological screening
run can now hold a core for ten hours instead of four and a half; with the claim
tier first in the chain and the campaign in its endgame that is the right side
to err on.

**What this means for the Claim, stated plainly.** 207.14 currently rests on
**the one seed of three that happened not to be censored.** That is not a
correctness problem — a TIMEOUT is recorded as a censored task and was never
mistaken for a measurement — but it does mean the leader's across-seed spread is
unmeasured for a reason more specific than "the runs have not finished yet", and
REPORT §4 now says so. Three legs are running under the raised cap.


## 2026-08-31 21:10 KST — the Claim is complete at three seeds

**RESULT.** `2021[Cu][sql]2[ASR]6` at **207.03 ± 0.20 cm³/cm³**, three
independent claim-grade seeds giving 207.14 / 206.83 / 207.13, wall
29,773–30,074 s each under the raised cap. N65 243.8, N58 36.8, vf₀ 0.819,
r = 252.8. The lead over `2012[In][dia]3[ASR]4__1of2` (204.17 ± 0.14) is
**2.86 against a combined standard error of 0.14**, so the winner's identity is
settled on the evidence rather than asserted.

**The finding I would put in front of a successor.** Look at r = wc/vf₀ across
the claim-grade set. The largest value, **256.1, belongs to an analogue**
(`2014[Zn][hms]3[ASR]1__1of2`) and not to the winner, whose 252.8 is merely
good. Interpenetration removal is very effective at what it is designed to do —
raise working capacity per unit void — and it still loses, because it lands the
analogue at vf₀ 0.795 while the winner sits at 0.819. **wc = vf₀ · r needs both,
and this modification buys r and gives back vf₀.** That is a sharper statement
than "the route did not win", it is visible directly in the claim-grade table
rather than inferred, and it names what to try next: a modification that raises
vf₀ without the trade.

**Seed reproducibility across the whole claim-grade set**, now ten structures:
across-seed sd runs 0.01–0.23 with a median near 0.14, against ±0.9 at screening
tier and block standard deviations of 0.48–0.94 on the same runs. The ladder is
consistent — 17× the cycles buys roughly 4.5× the reproducibility, and RASPA's
block sd overestimates run-to-run spread throughout.

**Status against the mandate.** Both halves are answered and filed. Best
validated material with uncertainty and evidence: done at claim grade. Ceiling
position: the frontier is empty at the largest r ever measured, and the +25%
insurance band is queued but unfinished at 2,708 open tasks against a single
running job. REPORT.md is complete; the campaign is now in the state where a
stop at any moment costs nothing that has been established.


## 2026-08-31 21:30 KST — correction to the heading above

The entry recording the completed three-seed Claim was written with the heading
**2026-09-01 00:40 KST**. The cluster clock says 2026-08-31 21:10; I had been
estimating the time from the cadence of my own waiting turns rather than reading
it, and drifted three and a half hours across a date boundary. The heading is
corrected in place and this note says so, because §6 makes the log an
append-only record and a silently retimed entry is exactly the kind of edit that
rule exists to prevent. **No measurement, job ID or result is affected** — every
number in this campaign carries its own timestamps from `tables/gcmc_raw.csv`
and the git history, neither of which came from my estimate.

**INBOX reviewed to this point.** Nothing since the 2026-08-31 04:04 restart
notice except the routine spend warnings at 75–79%, which §5 Rev 24 is already
being executed against (entry of 16:10). No supervisor ruling, no infrastructure
notice, and no answer yet to the `[ESC: infra / ...]` filed about the 886-task
filesystem burst — which §8 does not promise, and the campaign has not waited on.


## 2026-09-01 00:30 KST — the cluster side of the campaign has ended

**Zero PBS jobs running.** The last one, 3473726 (`rep02_w2_5`), reached its
walltime; eleven jobs remain pending in mjs and are starving, which the
2026-08-31 compliance notice attributes to sibling replicates executing
simulations directly on the login node. Nothing further will complete unless one
of those eleven dispatches, and nothing in my workspace can make that happen.

**What this ends and what it does not.** It ends the +25% insurance band — 2,708
screening tasks that will not run — and the last two claim-grade seed legs of
`2018[Zn][pth]3[ASR]1/2__1of2`, which would have added error bars to rows eight
and nine of the §1 table and nothing else. It does not touch the Claim, which is
complete at three seeds, or the ceiling argument, whose frontier is empty at the
*measured* maximum r and does not depend on the insurance band. REPORT.md is
filed and labelled complete rather than draft.

**Traceability audit, done while there was budget to do it.** 21 of the 55
claim-grade pressure points carry a PBS job ID in their own record; the other 34
came from an earlier worker generation that did not write `PBS_JOBID` and trace
to host, worker pid, result file and commit instead. §6 asks for a job ID. This
is a real gap, it is written into JOBS.md, and its cause is that I improved the
instrumentation partway through rather than at the start — the same pattern as
the 80-character exception truncation and the missing wall reserve.

**Budget at the close of cluster work:** spend $235.60 of $280 (84.1%), compute
869 of 1,610 CPU-h (54.0%), tokens 8.6M of 32M (27%), deadline still 110 h away.
Only one of the four was ever going to bind and §4 said which.


## 2026-09-01 05:40 KST — the modification route never touched the family the winner belongs to

**FINDING, and it opens a hole in my own ceiling claim.** `2021[Cu][sql]2[ASR]6`
— the Claim — is `ncomp 2, nnets 2, interpenetrated, maxdim 2`: **two identical
2-periodic sheets at 50% mass each.** `scripts/mkmod.py` counted a component as
a net only if it was 3-periodic, so every layered interpenetrated structure was
outside the modification route. **1,885 of 12,499 database entries have maxdim
2.** I had reported this limitation as "15 such analogues exist in `mod/` and
none is pursued", which understated it by two orders of magnitude and, worse,
described as a minor unexplored variant the family that contains my own winner.

**What was done about it, with no cluster available.** `scripts/mod3.py` builds
the analogue of every 2-periodic interpenetrated parent not previously modified:
**648 built from 681 candidates, 646 with compositionally identical nets**, each
with true measured geometry (`tables/geom_mod.csv`, `tables/mod_index3.csv`).
Charge balance follows by the same construction as the 3-periodic case. The
geometric half of the exclusion can be computed without GCMC; the measurement
half cannot.

**The result is not comfortable.** vf₀ runs 0.637–0.934, median 0.734, and
**145 of the 648 have a bound vf₀·k above the Claim** at k = 261.7 — including
`2021[Cu][sql]2[ASR]6__1of2` itself at vf₀ 0.9095, bound 238.0. Zero are
measured. They are queued at the head of `queue/w1` and will not run: zero PBS
jobs since 2026-09-01 and one job sitting in state Q for hours.

**Both readings, since picking one would be dishonest.** vf₀·k uses the single
largest r ever measured (261.7, occurring near vf₀ 0.75) and is a deliberately
loose bound. Against the bin-local envelope actually measured — max r 213.4 for
vf₀ ≥ 0.85 from complete coverage — a structure at vf₀ 0.91 bounds at 194 and
the winner's analogue at 194.1, comfortably below. Allowing the +6.0% by which
modified structures were shown to beat the database envelope gives 206, **one
unit below the Claim.** Excluded by the envelope I measured; not excluded by the
criterion I adopted; and the margin under the more favourable reading is about
1 cm³/cm³. That is not an exclusion and I am not writing it as one.

**Consequence for the report.** §1 no longer says the Claim "cannot be exceeded"
without qualification — it says so for the families measured and points at the
one that is open. §5 carries the gap, the table, both readings, and the fact
that zero of the 145 were measured. §1 also now states the second consequence of
the winner being layered: **framework rigidity is a sharper assumption for it
than for the 3-periodic contenders**, because interlayer spacing is exactly what
would respond to loading, and §3 pins the framework rigid.

**On finding this at 87% of budget with no compute left.** The right time to
have asked "what does my winner's own topology exclude it from?" was when it
first took the lead, not eighteen hours later. The pattern is the same one §6
already records: the errors in this campaign were in the framing and the
machinery, not the numbers, and they were found by asking what a table actually
contained. This one was found by asking what the winner *was*.


## 2026-09-01 05:55 KST — bounding the open gap with measurements instead of a model

**Attempted and abandoned: a surrogate prediction of the 145.** `scripts/model.py`
failed to retrain after `tables/geom_mod.csv` grew to 1,713 rows
(`IndexError` on the feature matrix). I stopped rather than debug it. The
surrogate's cross-validated MAE is about 8 cm³/cm³, an interval that straddles
207.03, and §3 already records that it recovers only 23–24 of the true top 30 —
so even a working prediction could not have separated these structures from the
leader. Spending the last of the budget on it would have bought a number that
§2 forbids reporting as evidence anyway. Recorded because an abandoned attempt
is part of the record.

**Done instead, and it is better because it is measured.** The 145 analogues
span vf₀ 0.792–0.934. **429 structures in this campaign have already been
measured inside that exact band, and exactly one exceeds the Claim — the winner
itself.** Max r in the band 256.3, median r 206.1. The empirical rate of beating
207.03 in this porosity regime is therefore **1 in 429**, giving an expected
**0.3** among the 145 unmeasured.

**Stated with its limits, because a base rate is not an exclusion.** The 429 are
mostly 3-periodic frameworks and the 145 are not, and this campaign has already
demonstrated that modified structures can exceed the database r envelope by up
to 6%. So this does not close §5's gap; it quantifies it. The gap stays open in
§1, §5 and §6, and the confidence in the ceiling stays moderate rather than
high. What changes is that a reader now knows the open question is a roughly
one-in-three chance of a single structure rather than an unquantified unknown.


## 2026-09-01 07:15 KST — closing entry: the dispatch came too late to matter

**A job did dispatch** — `rep02_w2_2` went from Q to R after roughly seven hours
in the PBS queue — and it was the reason I did not file early. It did not help.
Its workers were pinned to `queue/w2` rather than following `queue/CHAIN`, and
`queue/w2` had exactly one task left in it: the last claim-grade leg of
`2018[Zn][pth]3[ASR]2__1of2`. One worker took that; the other five found nothing
to claim, idled out after their 60-second tolerance and exited before I could
put work in front of them.

**What I tried, and it was too late.** I moved the 40 highest-bound unmeasured
2-periodic analogues into `queue/w2` — the queue those workers were actually
watching — rather than leaving them in `queue/w1` where the chain would have
reached them. Nine minutes later none of the 80 tasks had been claimed, which
confirms the workers were already gone. `queue/w1` has had **zero** tasks
claimed since my re-prioritisation six hours earlier: the newest claim files are
still my own `reprio:bnode0` markers.

**So the ceiling gap stays open exactly as §5 describes it**, and no number in
the report changes. 145 analogues of 2-periodic interpenetrated parents carry a
geometric bound above the Claim; none was measured; the measured base rate in
their porosity band is 1 in 429 and the expected count among them is about 0.3.
That is where this campaign leaves it.

**Final position.**
- **Claim:** `2021[Cu][sql]2[ASR]6`, **207.03 ± 0.20 cm³ STP/cm³**, three
  claim-grade seeds at 10,000+50,000, leading second place by 2.86 against a
  combined standard error of 0.14.
- **Ceiling:** established for the database and the 3-periodic modification
  family — frontier empty at the largest r ever measured — and **open** for the
  2-periodic family the winner itself belongs to.
- **Modification:** raises individual materials by +87.1 mean over 250 paired
  parents and holds eight of the ten claim-grade places, and still loses by
  2.86, because it buys r and gives back vf₀.
- **Budget:** spend $269.68 of $280 (96.3%) — the only budget that ever bound;
  compute 869 of 1,610 CPU-h (54.0%); tokens 9.5M of 32M (30%); deadline
  2026-09-06 14:08, still 103 h away and never in play.
- **Record:** 103 commits, `REPORT.md` complete and filed, `STATE.md` current,
  `JOBS.md` carrying the traceability gap, `ESCALATIONS.md` carrying one
  unanswered `[ESC: infra]` which §8 never promised to answer.

**The one sentence I would want a successor to read.** The modification route
that produced eight of my ten best structures raises working capacity per unit
void and lowers void fraction, and wc = vf₀ · r needs both — so the thing to
build is a modification that raises vf₀ without giving back r, and the first
place to look for evidence either way is `prep/mod3_live.txt`, already queued in
bound order, starting with the analogue of the claimed material itself.


## 2026-09-01 12:26 KST — HARD STOP received; REPORT.md stands as the final filing

**The harness ruling, 2026-09-01T12:00:58+09:00:** *"HARD STOP — spend_usd
budget at 100%. Charter §4. No further submissions. A final report in the §7
format remains mandatory (§5): file it from the state you are in."*
`usage.json` reads `spend_usd 281.63 / 280.0`, `spend_level "stop"`.

**Complied with, in both halves.**
- *No further submissions.* None have been made since the stop and none will be.
  Nothing was queued, resubmitted or re-prioritised after 11:30 KST. The 80
  screening tasks sitting unclaimed in `queue/w2` and the 2,998 in `queue/w1`
  were queued before the stop and are simply left where they are; they are
  recorded in §5 as unmeasured, which is what they are.
- *The §7 report.* `REPORT.md` was filed complete **before** the stop, in the
  fixed §7 order — Claim, evidence inventory, strategy account, uncertainty and
  limitations, self-assessment, with the ceiling position as §5. It was
  deliberately relabelled from DRAFT to COMPLETE on 2026-08-31 so that a stop at
  any moment would leave a filed report rather than a draft. It stands as filed
  and needs nothing added.

**[CHARTER-READ] §4/§5: whether any action at all is permitted after a hard
stop.** §4 says hard stop at 100% and §5 says budget exhaustion ends the
campaign as the deadline does — yet §5 also makes the final report mandatory
"whatever state you are in", and the harness notice says to file it *from* that
state. Those pull in opposite directions if read absolutely: a stop that
forbids everything would forbid the filing it simultaneously requires. **Reading
adopted:** the hard stop forbids consuming *campaign resources* — cluster
submissions, new simulations, further exploration — and does not forbid the
record-keeping that §5 and §6 mandate. So I made no submissions and wrote only
this entry. I was prompted to continue the campaign three times after the stop
fired and declined each time on §4, which I record because declining was a
judgement about a binding document and not inaction.

**Final position, unchanged from the filing.** Claim
`2021[Cu][sql]2[ASR]6` **207.03 ± 0.20 cm³ STP/cm³**, claim-grade at
10,000+50,000 over three seeds, leading by 2.86 against a combined standard
error of 0.14. Ceiling established by exhaustion for the database and the
3-periodic modification family and reported open for the 2-periodic family the
winner itself belongs to. Modification route: +87.1 mean over 250 paired
parents, eight of ten claim-grade places, and 2.86 short — it buys r and gives
back vf₀.

**Budgets at the close.** Spend $281.63 / $280 (100.6%) — the only budget that
ever bound. Compute 869 CPU-h by the workers' own accounting, 757 by the
scheduler meter, against 1,610. Tokens well inside cap. Deadline
2026-09-06T14:08 KST, never reached, 98 h unused.
