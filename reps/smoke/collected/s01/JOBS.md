# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-26 | 3470391 | long | b0 cost-model benchmark (triage 500+2000, 2 P) | 2 struct × 2 P | ~10 min | submitted |
| 2026-08-26 | b0_001..003 | long | b0 cost-model benchmark, remaining 6 structures | 6 struct × 2 P | ~10 min | submitted |
| 2026-08-26 | s01_b1_000..007 | long | triage-vs-floor fidelity, floor cycles | 8 bench structures x 2 P | ~40 min | submitted |
| 2026-08-26 | s01_b2_000..003 | long | triage-vs-floor fidelity, scout cycles | 8 bench structures x 2 P | ~5 min | submitted |
| 2026-08-26 | s01_geom_00..19 | long | G3 pre-sim screen + descriptors, all 1731 | all | ~10 min each | submitted |
| 2026-08-26 | s01_oms_0..3 | long | G4 exposed-metal screen, all 1731 | all | ~5 min | done: 620/1731 flagged |
| 2026-08-26 | s01_s1_000..088 | long | S1 exhaustive scout screen (150+600, 2 P) | all 1731 | ~47 min each | fed by bin/feeder.sh |
| 2026-08-26 | s01_eq_000..003 | long | scout-vs-floor bias test on porous structures; doubles as S2 work | 2 struct x 2 P | ~60 min | submitted |
| 2026-08-27 | s01_s3_000..003 | long | Claim-grade finalist + G6 reproduction (2 clock-seeded reps) | 2023[Cu][ctn]3[FSR]1 x 2 P x 2 reps | ~14 h each | submitted |
| 2026-08-27 | s01_g7_000..003 | long | G7 random audits, fresh reproduction of screening runs | 27 structures x 2 P | ~1 h | submitted |
| 2026-08-27 | s01_s2_000..037 | long | S2 floor grade: promotion + ceiling gap + stratified fidelity | 19 struct x 2 P | ~2-4 h | submitted |
| 2026-08-27 | s01_mod_000..003 | long | modification test: methyl-stripped finalist + G5 matched pristine control | 2 struct x 2 P | ~2 h | submitted |
| 2026-08-27 | s01_s4_000..003 | long | Claim-grade modified finalist + G6 reproduction | 2023[Cu][ctn]3[FSR]1__stripH x 2 P x 2 reps | ~15 h | submitted |
| 2026-08-27 | s01_mod2_000..001 | long | falsification test: strip methyls from a structure already past the optimum | 2022[U][srs]3[FSR]1__stripH x 2 P | ~4 h | submitted |
