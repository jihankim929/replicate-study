# STATE — rep12 working memory

*Updated: 2026-08-29 23:45 KST (T+3.0 h of 168 h)*

## Fixed facts

- Deadline **T = 2026-09-05T20:42:16+09:00**. Budgets **1,610 CPU-h**,
  **32 M tokens**, **US$280**, **12 queued jobs**.
- `qas`/`qinfo`/`quse`/`qrm` live in `/usr/local/mjs/`, not on PATH.
  **Never use bare `pkill`** — `/usr/local/hpc/bin/pkill` shadows it and is a
  job-killing admin tool. Use `kill <pid>`.
- Scheduler: sorts pending jobs by `(property, user usage, submit time)`; every
  replicate is user `Bei`, so ordering among us is FIFO by submit time against
  shared per-property limits (ax 32, aa 38, amd 80, ac 102 of 64/76/160/204
  physical). `Job.submit()` runs `qsub <stored path>` **at dispatch time**, so
  **rewriting a queued .pbs body keeps its FIFO position** — use
  `bin/repurpose.py`, never `qas` again for an already-queued job.
- RASPA **ignores its command-line argument** and always reads `./simulation.input`.
- `RASPA_DIR=$WS/raspa_home`, binary `$WS/toolchain/raspa/bin/simulate`,
  `LD_LIBRARY_PATH=$WS/toolchain/raspa/lib`, `PYTHONPATH=$WS/pylib` (sklearn).
- Framework name = `name.replace("[","_").replace("]","_")`.

## Measured protocol facts

- **My pipeline reproduces the supervisor's reference**: `2021[Cu][sql]2[ASR]6`
  at 65 bar, 200+1,000 cycles → 243.20 ± 2.10 against their 243.49 ± 0.68 at
  2,000+10,000. Their pair gives **WC = 206.53 cm³/cm³**.
- **Cost**: 0.333 s/cycle for that structure ⇒ floor grade ≈ 1.1 CPU-h at
  65 bar, 0.36 at 5.8 bar. Cost model in `bin/mkqueue.py`:
  `C·ncyc·N_mol·(N_fw+N_mol)`, `C = 2.40e-7`. Most structures are far smaller
  than the reference — modelled median 0.33 CPU-h per structure-pair.
- **Energy grids rejected by measurement**: 1.4× on the GCMC step, wiped out by
  302 s generation and 202 MB per structure; +1.3 cm³/cm³ bias. No screening run
  uses a grid, so no §3 grid disclosure is owed on any number.
- **G4(b)(i) closed**: all 73 database elements receive exactly the pinned UFF
  ε/σ through RASPA's auto-pseudo-atom path (73/73, `runs/elemprobe`).
- **G3**: 6 of 12,499 fail (4 density out of bounds, 2 overlapping atoms);
  charge sums all identically zero (vacuous — PACMAN normalises them).
- **Deduplication**: 12,499 entries are only **9,166 distinct geometries**.
  ASR/FSR pairs differ *only* in the DDEC6 charge column, which
  `ChargeMethod None` discards — so they are bitwise-identical simulations.
  Eligible canonical + G3-passing pool = **9,161**.

## Ranking model (validated)

`bin/rank.py` integrates a **local-density estimate** over the sampled
framework-energy histogram: local fugacity `f·exp(-U/kT)`, local density from
Peng-Robinson at that fugacity. It ranks the reference structure **#1 of
12,499** (predicts WC 176 vs true 206.5 — biased low, but the ordering is what
is used). The earlier Langmuir/liquid-filling surrogate ranked it 196th because
liquid-filling saturation rewards ever-larger pores; the LDA form cannot, since
an empty cavity tends to the bulk working capacity of 61.9 cm³/cm³.

## Current state of work

- **All 11 queued jobs repurposed in place** into pull-based GCMC workers
  (46 cores across ax/aa/amd), reading `work/queue.txt` and claiming lines by
  atomic `mkdir` in `work/claimed/`. Rewriting `work/queue.txt` re-prioritises
  everything instantly, including jobs queued hours ago.
- **`work/queue.txt` holds wave 1**: 620 canonical structures (500 exploit by
  LDA rank + 120 stratified explore), 1,240 tasks at floor cycles, estimated
  478 CPU-h. Plan archived at `tables/w1_plan.csv`.
- **Nothing has dispatched yet** — 3 h queued. Contention, not breakage.
  Watchdog `logs/watch.log` updates every 2 min.

## Next actions, in order

1. When results start landing: `bin/collect.py` → `tables/gcmc.csv`;
   calibrate the cost model against real wall times; check LDA rank vs measured
   WC on the explore arm.
2. Fit the GBR correction (`bin/wave.py`, needs ≥40 pairs), rewrite
   `work/queue.txt` for wave 2 from the corrected ranking.
3. G2 audit for anything in 210–230; G1 audit for anything >230.
4. G7: every 40th structure to pass screening gets a G6-grade audit.
5. Claim grade (10,000+50,000, `bin/claim.py`) on ~12 finalists, then G6
   reproduction with a different `RandomSeed`.
6. `REPORT.md` in the §7 format.

## Errors on the record

- First `pip install --user` wrote to `~/.local`, outside the workspace.
  Reinstalled to `$WS/pylib`; the stray copy was **not** deleted because the
  home directory is shared with sibling replicates. Logged in LOG.md.
