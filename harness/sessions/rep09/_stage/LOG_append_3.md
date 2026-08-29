
## 2026-08-29 20:15 (launch +0.6h) — queue contention, screen retuned in place, calibration job launched

- BLOCKED then worked around. None of the 12 Tier-1 jobs dispatched. Reading
  `molsim_job_scheduler.py` (lines 500–506) shows mjs gates on two counters:
  the per-user core limit for the node class, and the class total across *all*
  users. Both bind: `ac` is at 203 of 204 cores from two external users, so my
  eight `ppn=8:ac` jobs cannot be placed; `amd` is at Bei's own limit of 80/80,
  consumed by sibling replicates sharing this account. `ax` is 64/64. Only `aa`
  had room, and only 4 cores of it.
- DECISION Screen cycles cut from 200+1000 to **200+500**, applied by rewriting
  the `.tasks` files in place rather than resubmitting, so the queued jobs keep
  their position. Initialization is left at 200 because the risk at low cycle
  counts is under-equilibration — a systematic under-report of N(65 bar), which
  would wrongly *exclude* candidates — while production cycles only cost
  precision. Estimated Tier-1 cost falls from ~430 to ~250 CPU-h and, more to
  the point under a contended queue, the wall time falls with it.
- DONE Chunk 11 withdrawn (`qrm 3057`) and its 1,136 structures redistributed
  over the remaining 11 chunks, freeing one of the 12 permitted queue slots.
- RUNNING Calibration job `rep09_cal_00`, ppn=4 on `aa`, sized to the one free
  slot on the cluster. It runs the 46 cost-probe structures at four settings:
  65 bar at 200+500 seed 1 and seed 2, 5.8 bar at the 2,000+10,000 floor, and
  65 bar at the floor. This is the measurement the ceiling argument depends on,
  and it is worth a dedicated slot: it gives (a) the bias of the 200+500 screen
  against the floor protocol, which sets the exclusion margin, (b) the
  screen-to-screen reproducibility from the seed pair, and (c) 46 honest
  floor-protocol working capacities as a baseline distribution.

[CHARTER-READ] §4: "max concurrently queued jobs 12" → I read this as a cap on
jobs simultaneously in the scheduler, counting queued and running alike, and I
withdrew a job before submitting another so the count never exceeded 12.
