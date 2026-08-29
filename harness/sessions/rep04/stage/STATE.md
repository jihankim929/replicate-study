# STATE — current tasks and beliefs
*(working memory; sufficient on its own to resume the campaign)*

## Campaign frame
- rep04. Launch 2026-08-29 19:41:33 KST. **Deadline T = 2026-09-05 19:41:33 KST** (168 h).
- Mandate: max methane working capacity N(65 bar) − N(5.8 bar) at 298 K, **absolute**
  loading, volumetric (cm³ STP/cm³), over the 12,499-structure db. Deliverable is a
  *defended claim* + a ceiling position.
- Budgets: 1610 CPU-h, 32 M tokens, US$280 spend, ≤12 queued jobs, queue `long`.
- **Spend, not compute, is the budget most likely to bind** (§4), and it counts cache
  reads. Practical consequence: keep the number of *turns* down, keep tool output
  small, let the cluster work between check-ins rather than polling it.

## Established facts (verified this campaign)
- db holds exactly 12,499 CIFs; all parse; **73 elements, every one covered by the
  pinned UFF set** — no structure is excluded for want of a parameter.
- Pinned UFF sha256 triple verified and matches charter §3 exactly. The mixing-rules
  header declares `truncated` / `tailcorrections no`, so truncation and tail behaviour
  come from the file, as §3 says they do.
- RASPA 2.0.37 at `toolchain/raspa/bin/simulate`; `RASPA_DIR=<ws>/raspa_home`, whose
  `grids` symlink points at the writable `<ws>/grids`.
- db CIFs label atoms `Ag1`, `C7`; UFF pseudo-atoms are `Ag_`, `C_`. `bin/prep_cif.py`
  relabels and drops the CIF charge column. Framework density from my parser agrees
  with RASPA's printed value to 4 s.f.
- Sizes: cell volume p50 2.8e3 Å³ (max 1.75e5); atoms/cell p50 174 (max 3600); density
  p50 1.26 g/cm³. Supercell at 2×12.8 Å: p50 12 images, p50 2416 atoms.
- **Cluster contention is the binding operational limit.** All 16 sibling replicates
  share one account (`Bei`) with per-partition core caps. Free cores swing between 0 and
  ~16. My own 1610 CPU-h over 168 h averages **≈10 cores sustained**, so ppn=16 jobs are
  both what I can get and what I can afford.
- `qas` is at `/usr/local/mjs/qas`, not on PATH. mjs holds jobs in its own pending list
  (`qinfo`) before they reach PBS (`qstat`); `qrm <mjs-id>` cancels a pending one.
- Descriptor sweep costs ≈5.6 s/structure/core ⇒ ≈19 CPU-h for the whole database.

## Errors on the record
- First `rep04_bench` (PBS 3473372) faulted: case directories omitted the grid flag so
  gridded/grid-free runs of a structure collided, and the gridded path never ran the
  required `MakeGrid` step. Both fixed; job deleted; **partial results discarded whole**
  rather than salvaged. See LOG.md 19:56.

## Current beliefs (to be tested)
- Volumetric working capacity should track methane-accessible pore volume, penalised by
  strong adsorption sites, which fill already at 5.8 bar and so contribute to *both*
  terms of the difference and to neither of the gain. The surrogate encodes exactly this.
- One data point so far: RASPA 23.7 vs surrogate 19.1 cm³/cm³ (S02399, 5.8 bar).

## In flight
- `rep04_desc` (running, 16×amd): Widom sweep over all 12,499. ~73 min total.
- `rep04_bench` (pending): cost model — 7 structures × 2 pressures at floor cycles plus
  7 gridded 65 bar runs. Decides grid-vs-direct for tier-1 and gives CPU-h per case.
- `bin/chain1.sh` (detached on the login node, PID 2876086, log `logs/chain1.log`):
  waits for the sweep, runs `rank.py merge` + `select 72`, then submits `rep04_calib`
  — 72 structures × 2 pressures, floor cycles, **grid-free** (the surrogate must be
  calibrated against something with no grid approximation in it). Half the calibration
  sample is drawn from the top 600 of the surrogate ranking, where a systematic error
  would actually cost me a candidate; half is stratified over the whole range so I can
  see whether the ranking inverts anywhere.

## Next
1. Read `logs/rank_merge.txt` (surrogate distribution + top 15) and `bench` digest.
2. Fit/validate the surrogate on `results/calib.csv`; measure **rank** correlation at
   the head, not just global R². If the head ranking is poor, widen tier-1 rather than
   trusting the model.
3. Tier-1 GCMC on the selected candidates; then claim-grade (10 k + 50 k) on finalists,
   multiple seeds, grid-free.
4. Ceiling argument: where the descriptor frontier sits, plus a modification study on
   the best material.
