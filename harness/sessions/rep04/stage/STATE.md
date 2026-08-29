# STATE — current tasks and beliefs
*(working memory; sufficient on its own to resume the campaign)*

## Campaign frame
- rep04. Launch 2026-08-29 19:41:33 KST. **Deadline T = 2026-09-05 19:41:33 KST** (168 h).
- Mandate: max methane working capacity N(65 bar) − N(5.8 bar) at 298 K, **absolute**
  loading, volumetric (cm³ STP/cm³), over the 12,499-structure db. Deliverable is a
  *defended claim* + a ceiling position.
- Budgets: 1610 CPU-h, 32 M tokens, US$280 spend, ≤12 queued jobs, queue `long`.

## Established facts (verified this campaign)
- db holds exactly 12,499 CIFs; all parse; **73 elements, every one covered by the
  pinned UFF set** — no structure is excluded for want of a parameter.
- Pinned UFF sha256 triple verified on the cluster and matches charter §3 exactly.
  `force_field_mixing_rules.def` header declares `truncated` / `tailcorrections no`,
  so cutoff/truncation/tail behaviour comes from the file as §3 says.
- RASPA 2.0.37 at `toolchain/raspa/bin/simulate` runs; `RASPA_DIR=<ws>/raspa_home`
  (its `grids` symlink points at the writable `<ws>/grids`).
- db CIFs label atoms `Ag1`, `C7`; the UFF pseudo-atoms are `Ag_`, `C_`. `bin/prep_cif.py`
  relabels (coordinates, cell and composition untouched) and drops the CIF charge
  column — the protocol is chargeless. Framework density from my own parser agrees
  with RASPA's printed value to 4 significant figures on the smoke test.
- Structure sizes: cell volume p50 2.8e3 Å³ (max 1.75e5); atoms/cell p50 174 (max 3600);
  density p50 1.26 g/cm³. Supercell at 2×12.8 Å: p50 12 images, p50 2416 atoms.
- **Cluster contention is the binding operational limit.** All 16 sibling replicates share
  one account (`Bei`) with per-partition caps (~80 amd / 38 aa / 32 ax / 102 ac cores).
  At launch only ~16 amd cores were free. My own 1610 CPU-h over 168 h averages
  **≈10 cores sustained**, so sizing jobs at ppn=16 is both what I can get and what I
  can afford. Do not try to grab large allocations.
- `qas` is not on PATH; it lives at `/usr/local/mjs/qas`. mjs holds jobs in its own
  pending list (`qinfo`) before they reach PBS (`qstat`). `qrm <mjs-id>` cancels a
  pending one.

## Current beliefs (to be tested)
- Volumetric working capacity should track methane-accessible pore volume fraction,
  penalised by strong adsorption sites (which load up already at 5.8 bar and so do not
  contribute to the 65→5.8 difference). The screening surrogate encodes exactly this.

## In flight
- `rep04_bench` (PBS 3473372, ppn=16 amd): 7 structures spanning density × {65 bar,
  5.8 bar} at floor cycles, plus 7 grid-based 65 bar runs. Purpose: measure real
  CPU-h per case and the grid speed-up/bias. → results/bench.csv
- `rep04_desc` (mjs pending): Widom descriptor sweep over all 12,499, 20 k samples
  each, 16 chunks. ~3 s/structure ⇒ ~10 CPU-h. → results/desc/c*.csv

## Next
1. Read bench.csv → cost model; decide grid vs grid-free for tier-1 screening.
2. Fit the screening surrogate against a GCMC calibration sample; measure rank
   correlation before trusting any ranking.
3. Tier-1 GCMC on the top candidates, then claim-grade (10 k + 50 k) on the finalists.
4. Ceiling argument: modification study on the best material + evidence on where the
   descriptor-space frontier sits.
