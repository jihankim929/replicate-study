
### s01  —  305 tool results, 12.3 active h (span 40.1 h, 27.8 h idle >30 min)

| class | calls | calls/active h | bytes into context | share of re-read | attributed |
|---|---:|---:|---:|---:|---:|
| directory listings | 19 | 1.5 | 30,437 |  29.5% | $24.14 |
| file writes | 167 | 13.6 | 55,401 |  28.2% | $23.09 |
| scheduler polls | 49 | 4.0 | 23,183 |  20.1% | $16.46 |
| other | 53 | 4.3 | 23,714 |  18.9% | $15.49 |
| raw simulation-output reads | 17 | 1.4 | 4,274 |   3.4% | $2.80 |
| **total** | **305** | **24.9** | **137,009** | **100.0%** | **$81.97** |

Cache-read spend **$81.97** (60% of the bill); everything else (fresh input, output, cache writes) **$54.01**. Lifetime total **$135.99**.

### s02  —  201 tool results, 1.4 active h (span 41.2 h, 39.8 h idle >30 min)

| class | calls | calls/active h | bytes into context | share of re-read | attributed |
|---|---:|---:|---:|---:|---:|
| directory listings | 28 | 20.2 | 55,623 |  45.2% | $10.73 |
| other | 40 | 28.9 | 58,352 |  20.8% | $4.92 |
| file writes | 85 | 61.4 | 50,902 |  20.0% | $4.74 |
| scheduler polls | 44 | 31.8 | 25,187 |  13.4% | $3.17 |
| raw simulation-output reads | 4 | 2.9 | 1,039 |   0.7% | $0.16 |
| **total** | **201** | **145.1** | **191,103** | **100.0%** | **$23.72** |

Cache-read spend **$23.72** (56% of the bill); everything else (fresh input, output, cache writes) **$18.78**. Lifetime total **$42.50**.

### rep01  —  171 tool results, 5.2 active h (span 5.2 h, 0.0 h idle >30 min)

| class | calls | calls/active h | bytes into context | share of re-read | attributed |
|---|---:|---:|---:|---:|---:|
| other | 26 | 5.0 | 46,396 |  48.0% | $9.82 |
| file writes | 58 | 11.1 | 23,890 |  16.9% | $3.46 |
| scheduler polls | 44 | 8.4 | 23,328 |  14.9% | $3.04 |
| directory listings | 19 | 3.6 | 13,456 |  11.4% | $2.34 |
| raw simulation-output reads | 24 | 4.6 | 12,096 |   8.8% | $1.81 |
| **total** | **171** | **32.8** | **119,166** | **100.0%** | **$20.46** |

Cache-read spend **$20.46** (68% of the bill); everything else (fresh input, output, cache writes) **$9.53**. Lifetime total **$30.00**.

---

## Verdict on rep01, as ordered

**Predominantly one-time world-exploration weight — but the cost of *carrying* that weight is what
now governs, and carrying is not self-limiting.**

**The accumulation is front-loaded and effectively finished.** 84,721 of rep01's 119,166 bytes —
**71%** — entered in hour 0. The single largest item in the whole session is
`cat CHARTER.md` at **25,429 bytes, 21% of everything**, which is not a habit but an instruction:
the charter's first line orders it read in full before anything else. Hour 0 cost **$14.36**,
**48% of lifetime spend inside the first 20% of elapsed time**.

**The habit term is small and already disciplined.** Scheduler polls are 44 calls at 8.4/active h
and only **14.9%** of re-read share; raw simulation-output reads are 24 calls and **8.8%**. From
15:11 KST onward rep01's turns are spaced at **10.1 minutes, to the tenth of a minute, twenty
consecutive times** — it is waiting with sleeps rather than polling in turns, which is exactly the
discipline the Rev 22 clause mandates. **It adopted the behaviour without being told.**

**What does not self-limit is the re-reading.** Average cache-read tokens per turn climbs steadily
— 97k → 169k → 182k → 206k → 228k → 237k — so every remaining turn costs more than the last, on
context that is already paid for. Cache reads are **68% of rep01's bill**, the highest of the three.
The compounding term is not new dumps; it is the re-reading of what is already there.

**Consequence for the fleet.** The Rev 22 clause will help most by keeping accumulation *smaller*,
not by changing turn behaviour rep01 had already converged on. And because rep01's largest single
item is the charter — which every replicate must read, and which the gated arm's copy is
**26,861 bytes against the ungated arm's 11,487** — the gated arm carries roughly **15 KB more
mandatory context from its first turn, re-read on every subsequent turn, for the whole campaign**.
That is a cost asymmetry created by the treatment itself. It is not a defect and it is not
correctable without changing the treatment, but it should be named before per-arm spend is
compared: **the gated arm is structurally more expensive per turn, by construction.**

## Cross-replicate comparison

| | s01 | s02 | rep01 |
|---|---:|---:|---:|
| tool results | 305 | 201 | 171 |
| bytes into context | 137,009 | 191,103 | 119,166 |
| cache-read share of bill | 60% | 56% | **68%** |
| scheduler polls / active h | 4.0 | 31.8 | 8.4 |
| directory-listing share of re-read | **29.5%** | **45.2%** | 11.4% |
| lifetime bill | $135.99 | $42.50 | $30.00 (running) |

**Directory listings are the largest single re-read class in both smoke replicates** — 29.5% and
45.2% — and the smallest-but-one in rep01. That is the class the new clause names explicitly
(*"never list the full database into the session"*), and it is the one where the smoke's evidence
is strongest that the instruction was needed.
