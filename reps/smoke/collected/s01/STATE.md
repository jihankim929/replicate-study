# STATE — current tasks and beliefs
_Last updated: 2026-08-26T16:30 KST. Written to be sufficient on its own after any restart._

## How to operate here (mechanics that are easy to get wrong)
- Workspace `/home1/users/Bei/ws/s01`, reached with `ssh dirac-bei`. Deadline
  **2026-08-29 09:00 KST**. Budget 340 CPU-h, 12M tokens, ≤50 jobs in the scheduler.
- Submit: `PATH=$PATH:/usr/local/mjs qas jobs/<x>.pbs`. **The node spec must be the
  three-token form `nodes=1:ppn=1:amd`** — `qas` asserts on `nodes=1:ppn=1`.
- `usage.json` reports `cpu_h: 0.0` and is **not tracking**. Real accounting is
  `bash bin/budget.sh <batches...>`, which sums the `CPUSEC` lines `/usr/bin/time` writes
  into every run's `raspa.stderr`.
- A detached feeder (`bin/feeder.sh <joblist> 46`) keeps the queue topped up under the cap.
  Check it with `pgrep -f feeder.sh` and `tail runs/feeder_s1.log`; its progress cursor is
  `<joblist>.pos`. Restarting it is safe — it resumes from the cursor and skips runs that
  already have a `DONE` file.
- Heredocs over `ssh '...'` break on apostrophes in the payload. Write the file locally and
  `scp` it. This has bitten me three times.

## Tooling (all in bin/, all committed)
`cifutil.py` parse/emit CIFs and cell replication · `descriptors.py` zero-cost CIF
descriptors · `geom.py` G3 legs + porosity/Henry descriptors · `oms.py` G4 exposed-metal
detector · `mkjob.py` build run dirs + PBS scripts (`--mode scout|triage|floor|claim`,
`--reps N`) · `collect.py` runs → per-batch CSV · `merge.py` → `data/master.csv` ·
`gates.py` apply G1–G4/G7 and write AUDIT.jsonl · `audit.py` audit writer ·
`budget.sh` compute accounting · `feeder.sh` queue feeder.

## Established facts (verified, not assumed)
- Toolchain matches §3 exactly: three UFF SHA-256s, `RASPA 2.0.37`, and run headers show
  `CutOff VDW : 12.800000`, `All potentials are unshifted`, `tailcorrection: no`.
- All 1731 CIFs parse; every element is covered by the pinned UFF set; every
  `_atom_site_occupancy` is 1.0; **all densities are inside the G3 window** (0.313–3.963).
- **No helium pseudo-atom exists in the pinned UFF set** → G3's He void fraction is
  geometric (LOG-05), not Widom.
- **Energy grids rejected on measurement** (LOG-04): 189 CPU-s + 85 MB per structure.
- **RASPA seeds from the clock** → repeat runs are independent; G6 reproduction is a real
  test (LOG-10).
- Cycle-cost ladder measured: scout 750 cycles, floor 12,000 (16×), Claim 60,000 (80×);
  one structure gave 60.8 → 1,130 CPU-s, i.e. 18.6×, matching.
- **Cost concentrates in porous structures**: top 5% carry 55%, cheapest 50% carry 15%.
  So exhaustive screening costs ~15% more than a porosity-filtered screen, not 2×.
- **G4 excludes 620 of 1731 (35.8%)**, validated against the ASR/FSR convention: 133
  ASR-only flags vs 6 FSR-only on 657 matched pairs (LOG-07).
- **Screen reproducibility is better than its own error bar**: the exact-duplicate pair
  `2021[Cu][sql]2[ASR]6`/`[FSR]6` gave 206.77 and 207.69 as independent runs (LOG-12).

## Current beliefs
- Working capacity here is governed by *saturation timing*, not raw uptake. Structures that
  are already full at 5.8 bar deliver nothing regardless of N(65).
- The leaderboard is currently led by G4-inadmissible Cu structures. Expect the defensible
  answer to be materially below the raw maximum, and expect that gap to be a real part of
  the ceiling answer rather than a nuisance.

## Plan and budget (340 CPU-h total; ~15 used at last check)
| stage | what | est. CPU-h |
|---|---|---|
| S1 | exhaustive scout screen, all 1731, both pressures | ~150 |
| G7 | every 40th passing structure, reproduction-grade audit | ~6 |
| S2 | floor cycles on ~top 20 admissible **+ ~15 stratified random across the S1 range** | ~55 |
| S3 | Claim cycles on 2–3 finalists + G6 fresh reproductions | ~40 |
| — | contingency | ~40 |

**The stratified random sample in S2 is not optional.** The ceiling claim needs a *measured*
scout→floor error in the range where the screen said "not interesting"; the top-N paired
sample is selection-biased and cannot supply it (LOG-09).

## Open tasks
1. Watch S1 cost. **If S1 projects past ~150 CPU-h, intervene** — the tail of the ordering
   is cheap, so truncating it saves little; the lever is cycles on the porous head.
2. On S1 completion: `collect.py s1` → `merge.py` → `gates.py` (writes AUDIT.jsonl, emits
   the promotion list). Kill G3 overlap failures (4 structures below 0.90 Å heavy-atom
   minimum) and G4 exposures.
3. Build S2 = top admissible + stratified random + G7 selections.
4. Decide the modification experiment. Current candidate: replace neutral terminal
   substituents (−CH3, −Cl, −Br) with −H on a top admissible structure. Charge-balanced by
   construction (neutral-for-neutral on carbon), reproducible from a script, matched
   pristine control is the unmodified structure (G5), and it creates no metal exposure (G4).
   Physical rationale: raises free volume and weakens low-pressure binding, and WC is
   limited by exactly those two things.
