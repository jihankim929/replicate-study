
## 2026-08-29 20:30 (launch +0.8h) — energy grids are unavailable in this build

- NEGATIVE `SimulationType MakeGrid` segfaults in the pinned RASPA 2.0.37
  binary. Reproduced on structure 9407 at UnitCells 2 2 2, with and without a
  `Component` block and with and without `NumberOfCycles`: without the
  component block it dumps core after 0.07 s; with it and `NumberOfCycles 0`
  it returns 0 having written nothing; with a component block and cycles >= 1
  it dumps core. No `.grid` file is ever produced under
  `$RASPA_DIR/share/raspa/grids`. Charter §3 permits grids for screening but
  does not require them, so this costs precision of throughput, not validity.
  Abandoned after ~20 minutes; the screen runs without tabular grids.
- Filed `[ESC: infra / ...]` for the record only. Per §8 no answer is promised
  and none is being waited on.
