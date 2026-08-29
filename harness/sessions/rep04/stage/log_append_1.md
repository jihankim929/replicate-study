
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
