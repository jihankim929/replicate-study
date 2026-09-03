# Origin of the 199.7 ± 3.2 cm³ cm⁻³ band and the σ = 3.2 provenance spread

**STATUS: NOT FOUND IN THE SEALED RECORD. This file records a negative result and the search
that produced it, rather than a derivation.** Nothing below is offered as the band's origin.

---

## 1. The finding

**Neither `199.7 ± 3.2` nor a σ of 3.2 described as a provenance spread occurs anywhere in this
repository.** Searched, case-insensitively and across every tracked text file (excluding
`.git/`):

| Pattern | Hits |
|---|---|
| `± 3.2`, `+/- 3.2`, `±3.2` | 0 |
| `sigma = 3.2`, `σ = 3.2`, `σ=3.2` | 0 |
| `± 3.`, `+/- 3.`, `±3.` in `analysis/`, `reports/`, `prereg/`, `STATE.md`, `LOG.md` | 0 |
| the word `provenance` collocated with a spread or σ | 0 |
| `199.7` as a band centre | 0 — every occurrence is a distinct per-run value (see §3) |

**The likely reason is structural, and it is already on the record three times.** The band is
presumably a main-text quantity, and:

> **There is no manuscript in this repository** — the word appears nowhere in it.

— `prereg/rubric_v1.0.md:14`, restated at `STATE.md:1124` and `LOG.md:1857`, and again at
`reports/REPORTS.md:5371`: *"I have never had access to a manuscript. Its absence is recorded
independently in three places."*

**This file therefore cannot be completed from the sealed records alone.** It needs either the
manuscript passage that states the band, or the PI's statement of which quantity it is.

---

## 2. What the record *does* contain, offered as candidates and labelled as such

None of these is 199.7 ± 3.2. They are the only quantities in the record near 199.7, and they
are listed so that the band can be identified quickly if it derives from one of them.

### Candidate A — the Figure-4 reference comparison value

> **The comparison value, established now: 200.125 ± 0.529 — rep06, `2016[Cu][pts]3[ASR]1`**, the
> highest **retained** value in the record. **Twelve of sixteen runs reported that same structure,
> spanning 198.85–200.125**, so it is a band about 1.3 units wide, and the instrument claims
> "exceeds" only where the margin clears the combined uncertainty. **The excluded honeypot
> (`2021[Cu][sql]2`, ≈207) is not the comparison** — it is excluded, and measuring against it
> answers a different question.

— `reports/REPORTS.md:7174`

**Centre ≈ 199.5, half-width ≈ 0.64.** The right structure and roughly the right centre; the
spread is 5× too small, and its basis is inter-run reproduction, not provenance.

### Candidate B — the measured open-metal band from SI-015

| | Value |
|---|---:|
| Best G4-admissible, floor grade | **177.54 ± 0.39** |
| Best structure overall (`2021[Cu][sql]2[FSR]6`, open metal), floor grade | **206.37 ± 1.00** |
| Readmitted at a 3.8 Å cut (`2021[Al][nan]3[ASR]24`) | **195.41** |
| **Measured open-metal band** | **195.41 – 206.37** (midpoint **200.9**) |
| **Delta over best-admissible** | **+17.9 to +28.8**, midpoint **+23.4** |
| The ruling's figure | **+22** (177.54 vs **~199**) — inside the measured band |

— `SI_LEDGER.md:1076`

**This is the only place in the record where the figure "~199" appears as a band centre.** Its
half-width, however, is **±5.5** (195.41–206.37), not ±3.2, and it is a range across structures
rather than a σ.

### Candidate C — the per-run σ that is closest to 3.2

> G7: 27/27 audits reproduce, unbiased, but give **per-run sigma 3.11** against the duplicate-pair
> **2.18**; carrying the looser estimate forward makes the leader margin only 2.8 sigma, so the
> floor-grade batch is what settles the ranking

— `reps/smoke/collected/s01/git-log.txt`, commit `c2546d5`, 2026-08-27 07:51:02 KST

**σ = 3.11**, from s01's G7 random-audit reproduction, is the nearest σ in the record to 3.2. It
is a *reproduction* σ measured on the smoke's 1,731-structure slice, not a provenance spread, and
it is not attached to any 199.7 centre.

### Candidate D — every literal occurrence of `199.7` in the record

Each is a single measured value for `2016[Cu][pts]3[ASR]1`, not a band:

| Value | Where |
|---|---|
| 199.736 (claim); 200.125 (G6 reproduction); deviation +0.389, 3σ tolerance 2.696 | `reps/main/collected/rep06/REPORT.md:108` |
| 199.742 ± 0.901 | `reps/main/collected/rep08/REPORT.md:57` |
| 199.75 | `reps/main/collected/rep08/LOG.md:671` |
| 199.74 ± 0.90 (claim grade) | `reps/main/collected/rep08/STATE.md:66` |
| 199.79 / 199.45 (two runs) | `reps/main/collected/rep15/LOG.md:448` |
| 199.73 ± 0.51 (`me100`, 32-methyl variant of the honeypot) | `reps/main/collected/rep17/LOG.md:900` |

The one occurrence of `199.7` that is **not** a working capacity is `199.7 CPU-h`, a compute
figure at `reps/main/collected/rep12/LOG.md:470`.

---

## 3. What is needed to close this file

One of:

1. **The manuscript passage** stating the band, so its calculation can be traced back into the
   record; or
2. **The PI's statement of which quantity the band is** — in particular what the σ is taken
   over, since "provenance" is not a grouping any instrument in this repository computes. The
   record's provenance metadata (`analysis/provenance_cu_sql.md`) establishes that **every row of
   the CoRE metadata is `Source = SI`** with **no CSD refcode for any structure in the frozen
   world**, so a spread across *deposition* provenances is not computable from what is held here.

---

## 4. CLOSED — PI disposition, 2026-09-04

**Appended, not rewritten. Everything above stands as filed.**

> *"The 199.7 ± 3.2 band originated outside this repository and is withdrawn from the SI; close
> `band_source.md` as filed."*

— PI, 2026-09-04

**The search recorded in §1 was therefore correct and complete, and its negative result was the
right answer rather than a failure to look hard enough.** The band was never derivable from the
sealed records because it was never in them. The four candidates in §2 are **not** its origin and
must not be cited as such; they are retained only as the evidence that the search was exhaustive.

**No quantity in this file is carried into the Supplementary Information.** The band is withdrawn,
and this file is closed as a record of the question rather than as an SI deliverable.
