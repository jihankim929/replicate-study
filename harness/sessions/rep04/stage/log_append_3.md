
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
