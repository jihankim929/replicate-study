<!-- SEALED — answer-key artefact. Never enters a replicate workspace, LOG.md, STATE.md,
     or a commit message. Produced under the PI's dossier-sitting ruling of 2026-08-29. -->

# CLUSTER D — RAW EVIDENCE FOR HAND-RULING — [Bei, 2026-08-29]

The PI ratified the hold on cluster D and asked for the evidence rather than the verdict:
*"serve me the raw evidence for the 6 sitting files — linker formula units, the ring atoms as
deposited, protonation-relevant bond environments — and I'll rule the azolate chemistry by hand."*

This is that evidence. **It carries no disposition.** The instrument that produced it
(`harness/charge_evidence.py`, open repo) emits no verdict by construction, so nothing here has
been pre-judged by the code whose output the PI declined to rule on.

**Producing it disproved the defect report that justified the hold.** That correction is §1, and it
is stated before the evidence because it changes what the PI is ruling on.

---

## 1. SI-017 is withdrawn — the instrument was consistent

Bei reported that two variants of one framework with **identical atom counts (2,016) and identical
metal counts (96)** returned azolate counts differing by exactly 2×, and called it a fourth
enumeration hole. **Bei checked atom counts and never checked atom composition.**

| | cell contents | linker | 5-rings with ≥2 N |
|---|---|---|---|
| `2020[Cu][she]3[ASR]1` | C896 H576 N448 Cu96 | **C14H9N7** × 64 | 128 × `C3N2`, 64 × `C2N3` |
| `2020[Cu][she]3[FSR]1` | C832 H576 N512 Cu96 | **C13H9N8** × 64 | 64 × `C3N2`, 128 × `C2N3` |

They differ by **one carbon-for-nitrogen swap per linker**. They are not the same framework as
deposited. Pass 3's rule was applied identically to both and its output follows deterministically:
it counted every ring with no exocyclic H (128 in one file, 64 in the other) and rejected every ring
carrying one. **The ring populations are swapped between the files, so the counts are too.** The 2×
is arithmetic on the depositions, not instability in the code. The claim is withdrawn in full; the
SI ledger carries the correction append-only.

**What is real is a different and narrower defect:** pass 3 treats deposited hydrogen as
authoritative evidence of protonation state, and in this family the hydrogen is not evidence. That
is what the PI is actually being asked to rule.

---

## 2. The three findings that decide the chemistry

**(a) Full deprotonation balances both files exactly.** Each linker is a 1,3,5-trisubstituted
benzene carrying three azolyl arms; 64 linkers × 3 arms = **192 rings**, against Cu 96 × (+2) =
**+192**. If every arm is an azolate anion, net charge is **exactly 0** — and the azolate:metal
ratio is **exactly 2.00**, the value on which 70 balanced structures landed in the sealed
validation. This holds for *both* variants, from *different* ring populations. As deposited,
neither balances: `[ASR]` retains one N–H per linker (net **+64**), `[FSR]` retains two (net
**+128**).

**(b) The N–H positions are calculated, not refined.** Every N–H in both files is **1.0221 Å to
four decimal places — one distinct value** across all 64 (`[ASR]`) and 128 (`[FSR]`) instances.
C–H in the same files take three distinct values spanning 0.9986–1.0732 Å. A single exactly-repeated
distance is idealized riding-hydrogen placement. No hydrogen in either file is bonded to more than
one heavy atom, so this is not a connectivity artifact of Bei's bond criterion.

**(c) Neither file is internally consistent.** The core is a benzene ring with heavy substituents
at the **1,3,5 positions** (measured: substitution pattern `(1,0,1,0,1,0)`, 64 cores per cell).
`[ASR]` assigns those three arms as **2 diazolyl + 1 triazolyl**; `[FSR]` as **1 + 2**. Three arms
on a symmetric 1,3,5 core cannot be two different rings. **Each file contradicts itself,
independently of the other.** C and N are near-indistinguishable by X-ray scattering, and the
hydrogen rides on whichever assignment was made.

**The question for the PI, stated plainly:** are these fully deprotonated tris(azolate)benzene
linkers on Cu(II) — in which case both files are charge-balanced and neither is a capacity artifact
— or is the retained N–H real, in which case they are genuinely uncompensated? Bei has no standing
to answer this and does not.

---

## 3. `2009[Cd][nan]3[ASR]1` is not a cluster-D case at all

Its evidence carries **no ambiguity**: one linker type (C6H4N5 × 144), one ring type (144 × `CN4`
tetrazole), every ring identical (2 N metal-bound at degree 3, 2 N free at degree 2), and
**no N–H anywhere in the file** — 576 C–H, zero N–H. There is no protonation judgment to make. Its
azolate count of 144 is not in question, and the residual **+48** against Cd 96 × (+2) = +192 is a
clean missing-anion signature: 144 monoanionic tetrazolates where 192 are needed.

It is **removed from cluster D** and is ruleable on the ordinary uncompensated rule. Note for the
PI: an earlier draft of this evidence showed a heterogeneous fragment inventory for this entry
(bare `N` atoms, `N3` fragments, eight different formulas). **That was Bei's own artifact** —
components were being truncated at the edge of the replicated block and reported as chemistry.
Fixed before this document was written; the entry is chemically homogeneous.

**Cluster D is therefore 5 files, all `[she]`, reducing to two distinct chemical descriptions**
(`[ASR]`-type × 2, `[FSR]`-type × 3).

---

## 4. Raw evidence, as extracted

Linker formula units are per unit cell, metals stripped, components found on the replicated cell
with edge-truncated components discarded. Ring counts are per unit cell. Bond environments are
reported per ring nitrogen rather than summarised, because the triple *(metal-bound, exocyclic H,
exocyclic C)* is the entire basis on which azolate separates from azole.

### `2020[Cu][she]3[ASR]1`

- **Cell contents as deposited:** C896H576N448Cu96 — 2016 atoms
- **Metal census:** Cu × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C14H9N7` | discrete | 64 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `C3N2` | 128 |
| `C2N3` | 64 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `C3N2` | 3 | yes | no | no | 256 |
| `C2N3` | 3 | yes | no | no | 128 |
| `C2N3` | 3 | no | **yes** | no | 64 |

### `2020[Cu][she]3[ASR]2`

- **Cell contents as deposited:** C896H576N448Cu96 — 2016 atoms
- **Metal census:** Cu × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C14H9N7` | discrete | 64 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `C3N2` | 128 |
| `C2N3` | 64 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `C3N2` | 3 | yes | no | no | 256 |
| `C2N3` | 3 | yes | no | no | 128 |
| `C2N3` | 3 | no | **yes** | no | 64 |

### `2020[Cu][she]3[FSR]1`

- **Cell contents as deposited:** C832H576N512Cu96 — 2016 atoms
- **Metal census:** Cu × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C13H9N8` | discrete | 64 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `C2N3` | 128 |
| `C3N2` | 64 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `C2N3` | 3 | yes | no | no | 256 |
| `C2N3` | 3 | no | **yes** | no | 128 |
| `C3N2` | 3 | yes | no | no | 128 |

### `2020[Cu][she]3[FSR]2`

- **Cell contents as deposited:** C832H576N512Cu96 — 2016 atoms
- **Metal census:** Cu × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C13H9N8` | discrete | 64 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `C2N3` | 128 |
| `C3N2` | 64 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `C2N3` | 3 | yes | no | no | 256 |
| `C2N3` | 3 | no | **yes** | no | 128 |
| `C3N2` | 3 | yes | no | no | 128 |

### `2019[Cu][she]3[FSR]1`

- **Cell contents as deposited:** C832H576N512Cu96 — 2016 atoms
- **Metal census:** Cu × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C13H9N8` | discrete | 64 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `C2N3` | 128 |
| `C3N2` | 64 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `C2N3` | 3 | yes | no | no | 256 |
| `C2N3` | 3 | no | **yes** | no | 128 |
| `C3N2` | 3 | yes | no | no | 128 |

### `2009[Cd][nan]3[ASR]1`

- **Cell contents as deposited:** C864H576N720Cd96 — 2256 atoms
- **Metal census:** Cd × 96 (assumed +2)
- **Total formal metal charge, standard states:** **+192**

**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)

| formula unit | connectivity | count |
|---|---|---:|
| `C6H4N5` | discrete | 84 |

**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N

| ring composition | rings |
|---|---:|
| `CN4` | 144 |

**3. Protonation-relevant bond environments, per ring nitrogen**

| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |
|---|---:|---|---|---|---:|
| `CN4` | 3 | yes | no | no | 288 |
| `CN4` | 2 | no | no | no | 288 |


---

## 5. What happens after the PI rules

Per the ruling: the hand-rulings become SI-017's calibration set — the chemistry-known answer that
did not exist when the defect was filed. Then, in order:

1. Repair pass 3 against the calibration set. The repair is **not** to the ring finder, which is
   sound; it is to the treatment of deposited hydrogen as evidence of protonation.
2. Re-run the sweep over the frozen 12,499 and confirm the 406 headline and the 128-file mechanical
   disposition are unchanged, since neither depends on ring enumeration.
3. Re-sweep cluster D's remaining non-sitting files under the repaired rule and close their
   dispositions mechanically.
4. Seal the exclusion set complete.

**The ruling's arithmetic survives the reclassification.** Cluster D was 12 files, 6 of them in
today's sitting set. Moving `2009[Cd][nan]3[ASR]1` out leaves **11 files: 5 sitting + 6
non-sitting** — so the ruling's "cluster D's remaining 6 non-sitting files" is exactly right, and
only the sitting count changes, 6 → 5. (A first draft of this section claimed the remainder became
7. It does not; the file removed was a sitting file, not a remainder file.)
