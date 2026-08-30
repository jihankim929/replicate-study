
## 2026-08-29 22:40 (launch +3.0h) — screen at 5.5%, resubmission made idempotent

- RUNNING Tier 1 at 692 of 12,499 points, ~700 points/h with 5 chunks
  (40 cores) dispatched of 11 queued. 43.5 CPU-h spent, 226 s/point over the
  low-density front of the queue. Projected whole-database cost stays ~455
  CPU-h: the expensive band is the porous one, and only 1,654 structures lie
  below ρ = 0.9 while 8,753 lie above ρ = 1.1, where points cost ~140 s and
  falling.
- Structure of the result so far, 485 structures screened spanning
  ρ = 0.164–0.953: N(65 bar) rises from a mean of 180.9 below ρ = 0.4 to
  226.4 at ρ = 0.5–0.6, then falls back to 187.5 by ρ = 0.9–1.1. Best single
  value **268.0**. The optimum is an interior maximum in density, as it must
  be — too little framework and there is nothing to adsorb onto, too much and
  there is nowhere to put the methane.
- DEFECT FIXED `run_batch.py` re-ran a chunk's whole task list on
  resubmission; only the chunk *generator* filtered completed points. A chunk
  killed by a node failure and resubmitted by the watchdog would therefore
  have redone everything already on disk. It now skips points already recorded
  `ok` in its own output file. No compute was lost to this — no chunk has yet
  been resubmitted after starting — but the watchdog exists precisely to do
  that, so the hole was on the critical path.
- INBOX The `infra` escalation about the `MakeGrid` segfault is logged and
  queued, with no answer promised. Not waited on.
