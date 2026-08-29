# N = 20 → 16 (8v8) — mechanical derivation

**PI ruling, pre-launch. Reason logged: PI budget ceiling.** No re-draw, no new randomness: the
launch set is derived from the **already-sealed** `prereg/arm_assignment.txt` by the stated rule —
**first 8 per arm in sealed order** — so the derivation is reproducible from the sealed file alone
and the arm balance is exact (8 gated / 8 ungated).

**Sealed order is the file's order**, which is ascending replicate id. The seal is untouched.

| Arm | Sealed order | Launch set (first 8) | Deferred |
|---|---|---|---|
| **gated** | rep01 rep05 rep06 rep07 rep08 rep11 rep12 rep13 **rep14 rep20** | rep01 rep05 rep06 rep07 rep08 rep11 rep12 rep13 | rep14, rep20 |
| **ungated** | rep02 rep03 rep04 rep09 rep10 rep15 rep16 rep17 **rep18 rep19** | rep02 rep03 rep04 rep09 rep10 rep15 rep16 rep17 | rep18, rep19 |

**Launch set, ascending:** rep01 rep02 rep03 rep04 rep05 rep06 rep07 rep08 rep09 rep10 rep11
rep12 rep13 rep15 rep16 rep17

**rep01 is gated**, and it is the launch-gate replicate — so the 6-hour gate exercises the
Appendix A path, `AUDIT.jsonl`, and the G4 v1.0 clauses, not just the ungated skeleton.

## Fleet arithmetic at N = 16

| Quantity | Value |
|---|---:|
| Replicates | **16** |
| Concurrency cap / replicate | 12 |
| **Fleet ceiling** | **192** (= 16 × 12) |
| Cluster capacity (`pbsnodes`) | **580 ncpus / 19 nodes** |
| **Headroom, capacity ÷ ceiling** | **3.02×** |
| Fleet compute budget | 16 × 2,300 = **36,800 CPU-h** |
| Fleet sustained demand over 240 h | **153.3 concurrent** |
| Ceiling ÷ sustained | 1.25× |
| Fleet ceiling as % of cluster | 33.1% |

The three ceilings still agree: 16 × 12 = 192 is the fleet ceiling, and 580 ÷ 192 = **3.02×**
headroom against measured capacity — up from 2.42× at N = 20, because the ceiling fell and the
cluster did not.

## The conditional second wave needs 4 ids the seal does not contain

The ruling says the conditional second wave **becomes +8, same trigger**. The sealed assignment
holds **20** replicates, of which 16 launch — so **only 4 are deferred** (gated rep14, rep20;
ungated rep18, rep19). A +8 second wave therefore needs **4 ids beyond the sealed 20**, and Bei
will not invent pre-registered assignments.

Three ways to close it, all the PI's to choose; Bei does not pick:

1. **Second wave = +4** — the deferred remainder, restoring the sealed 20. Requires no new draw and
   keeps arm balance (2 gated + 2 ungated).
2. **Extend the sealed draw to 24** by re-running the recorded procedure over `rep01…rep24` under
   the same seed, and record the extension as its own pre-registration entry. **This changes the
   arm labels of the original 20**, because the shuffle is over the whole id list — so it is a
   new draw, not an extension, and the old assignment would have to be superseded explicitly.
3. **Draw 4 new ids (rep21…rep24) under a fresh, recorded seed**, leaving the sealed 20 untouched.
   Cleanest if the second wave is genuinely additive.

**Bei recommends (3)** if +8 is intended, and (1) if the "+8" was written against the pre-ruling
N = 20 baseline. The trigger is unchanged either way.
