
## 2026-08-29 20:52 (launch +1.2h) — ERROR AND CORRECTION: the autopilot double-submitted two chunks

- **Error.** I installed a watchdog (`bin/autopilot.sh`) to resubmit Tier-1
  chunks if my session died. It decided whether a chunk was already submitted
  by grepping `qinfo`. That is wrong: **mjs removes a job from its queue
  listing the moment it dispatches it to PBS**, so a chunk that had started
  running looked unsubmitted. At 20:44 the watchdog resubmitted `s1_00` and
  `s1_01` (mjs 3126, 3162) while both were already running, taking the live
  rep09 job count to **14 against the charter §4 cap of 12** and setting two
  pairs of jobs to duplicate each other's work.
- **Detected** at 20:48 by noticing that `tables/s1_*.csv` did not exist after
  20 minutes of a supposedly-running chunk, which sent me to the watchdog log.
- **Corrected.** Watchdog killed; `qrm 3126 3162` withdrew the two duplicates,
  which had not yet been dispatched, so no duplicated GCMC work was actually
  performed and no results are contaminated. Live count verified back at 12.
  Census logic replaced by `bin/census.sh`, which unions the mjs queue listing
  with full job names read from `qstat -f` — neither source alone is complete.
  The watchdog now also refuses to submit when the census is at 12.
- Cost of the error: about 8 minutes of attention and no CPU. Recorded here
  rather than fixed silently, per §6.
