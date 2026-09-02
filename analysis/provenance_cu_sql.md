# Provenance — `2021[Cu][sql]2` (ASR/FSR twins) and the intact pillared siblings

*Assembled 2026-09-02 under PI instruction, **read-only**. Nothing was written to `bnode0`.
Verbatim metadata only: every field below is reproduced as it appears in the frozen world's CoRE
metadata or in the structure's own CIF. Arithmetic on those fields is labelled as such.*

**Sources read** (all read-only, on `bnode0`):

| what | path |
|---|---|
| compositions | `benchmark/frozen/CoRE_MOF_2024_CR_united/{ASR,FSR,Ion}/<coreid>.cif`, field `_chemical_formula_sum` |
| metadata | `benchmark/staging/{ASR,FSR,ION}_data_SI_20250204.csv` |
| membership | `benchmark/staging/12089-recommended-screening-list.csv` |

---

## 1. The finding that governs everything below: there is no CSD provenance to report

**Every row of the CoRE metadata is `Source = SI`.** Counted across all three tables:

| table | rows | `Source` values | rows with a CSD-shaped 6-letter refcode |
|---|---:|---|---:|
| `ASR_data_SI_20250204.csv` | 1,372 | `SI` × 1,372 | **0** |
| `FSR_data_SI_20250204.csv` | 1,192 | `SI` × 1,192 | **0** |
| `ION_data_SI_20250204.csv` | 100 | `SI` × 100 | **0** |

The `refcode` field does not hold a CSD refcode. It holds a **publisher SI filename token**, e.g.
`d0ce01395a2_ASR_pacman` — the DOI `10.1039/D0CE01395A`, SI file 2, cleaning variant, charge method.

**Consequences, stated rather than worked around:**

- **There is no CSD refcode** for any structure in this request.
- **There is no CSD-reported chemical formula** for any of them, so the comparison asked for —
  *CoRE files against the CSD formula* — **cannot be made from this metadata.** §4 gives the
  comparison that the record *does* support: CoRE file against CoRE file, honeypot against intact
  sibling, and ASR against FSR.
- **There is no journal reference beyond DOI + publisher + year.** No journal-name field exists in
  these tables; `Publication` holds a publisher code (`RSC`, `ACS`, …).

---

## 2. Metadata, verbatim

### `2021[Cu][sql]2` — the ASR/FSR twins

| field | `[ASR]6` | `[FSR]6` |
|---|---|---|
| `coreid` | `2021[Cu][sql]2[ASR]6` | `2021[Cu][sql]2[FSR]6` |
| `refcode` | `d0ce01395a2_ASR_pacman` | `d0ce01395a2_FSR_pacman` |
| `name` | `-` | `-` |
| `mofid-v1` | `[Cu].n1ccc(cc1)c1ccc(cc1)c1ccncc1 MOFid-v1.sql.cat1;d0ce01395a2_ASR_pacman` | `[Cu].n1ccc(cc1)c1ccc(cc1)c1ccncc1 MOFid-v1.sql.cat1;d0ce01395a2_FSR_pacman` |
| `Metal Types` | `Cu` | `Cu` |
| `Has OMS` | `Yes` | `Yes` |
| `DOI` | `10.1039/D0CE01395A` | `10.1039/D0CE01395A` |
| `Year` / `Publication` | `2021` / `RSC` | `2021` / `RSC` |
| `Source` | `SI` | `SI` |
| `Extension` *(cleaning flag)* | `All Solvent Removed` | `Free Solvent Removed` |
| `unmodified` *(cleaning flag)* | `FALSE` | `FALSE` |
| `Charge` *(cleaning flag)* | `PACMAN-DDEC6` | `PACMAN-DDEC6` |
| `Density (g/cm3)` | `0.358334` | `0.358334` |
| `natoms` | `244` | `244` |
| `structure_dimension` | `2` | `2` |
| `topology(AllNodes)` / `catenation` | `sql` / `2` | `sql` / `2` |
| `memo` | *(empty)* | *(empty)* |

**`Metal Types` is `Cu` alone, and the `mofid-v1` node is bare `[Cu]` with a single neutral linker
`n1ccc(cc1)c1ccc(cc1)c1ccncc1` (1,4-bis(4-pyridyl)benzene). No Si, no F appears in either field.**

### `2017[ZnSi][sql]2` — intact pillared sibling

| field | `[ASR]1` | `[ASR]2` | `[FSR]1` | `[FSR]2` |
|---|---|---|---|---|
| `refcode` | `ja7b03850_si_003_ASR_pacman` | `ja7b03850_si_005_ASR_pacman` | `ja7b03850_si_003_FSR_pacman` | `ja7b03850_si_005_FSR_pacman` |
| `mofid-v1` | `[Zn].n1ccc(cc1)Sc1ccncc1 MOFid-v1.unknown.cat3;…` | *(same linker)* | *(same linker)* | *(same linker)* |
| **`Metal Types`** | **`Zn,Si`** | **`Zn,Si`** | **`Zn,Si`** | **`Zn,Si`** |
| `Has OMS` | `No` | `No` | `No` | `No` |
| `DOI` | `10.1021/jacs.7b03850` | `10.1021/jacs.7b03850` | `10.1021/jacs.7b03850` | `10.1021/jacs.7b03850` |
| `Year` / `Publication` | `2017` / `ACS` | `2017` / `ACS` | `2017` / `ACS` | `2017` / `ACS` |
| `Source` | `SI` | `SI` | `SI` | `SI` |
| `Extension` | `All Solvent Removed` | `All Solvent Removed` | `Free Solvent Removed` | `Free Solvent Removed` |
| `unmodified` | `FALSE` | `FALSE` | `FALSE` | `FALSE` |
| `Density (g/cm3)` | `1.31423` | `1.29001` | `1.31423` | `1.29001` |
| `natoms` | `200` | `200` | `200` | `200` |

**Si is named in `Metal Types` here and not in the Cu entry** — the distinction the smoke-world
audit drew.

### `2019[CdSi][sql]2` — the second sibling, and it has no metadata row

| | |
|---|---|
| CIF present in the frozen world | **yes** — `ASR/2019[CdSi][sql]2[ASR]1.cif`, `FSR/2019[CdSi][sql]2[FSR]1.cif` |
| in the recommended screening list | **yes** — indices `4393` (ASR) and `10175` (FSR) |
| row in `ASR/FSR/ION_data_SI_20250204.csv` | **NOT PRESENT in any of the three** |

**So for this structure there is no refcode, no DOI, no year, no publication and no cleaning flag in
the metadata at all** — only the CIF and its list membership. *(Substring searching for `CdSi`
returns `2017[CdSi][nan]3[ASR]1` and `2017[CdSi][nan]3[FSR]1`, which are a different structure at a
different topology and are not reported here.)*

---

## 3. CoRE's own composition, per cleaning variant — verbatim `_chemical_formula_sum`

| coreid | `_chemical_formula_sum` |
|---|---|
| `2021[Cu][sql]2[ASR]6` | `Cu4 H96 C128 N16` |
| `2021[Cu][sql]2[FSR]6` | `Cu4 H96 C128 N16` |
| `2017[ZnSi][sql]2[ASR]1` | `Zn4 Si4 H64 C80 S8 N16 F24` |
| `2017[ZnSi][sql]2[FSR]1` | `Zn4 Si4 H64 C80 S8 N16 F24` |
| `2017[ZnSi][sql]2[ASR]2` | `Zn4 Si4 H64 C80 S8 N16 F24` |
| `2017[ZnSi][sql]2[FSR]2` | `Zn4 Si4 H64 C80 S8 N16 F24` |
| `2019[CdSi][sql]2[ASR]1` | `Cd4 Si4 H112 C116 N8 O16` |
| `2019[CdSi][sql]2[FSR]1` | `Cd4 Si4 H120 C116 N8 O20` |

No `Ion` variant exists for any of these coreids.

---

## 4. Compositional difference, species by species

### 4a. The comparison that was asked for cannot be made

**No CSD formula exists** (§1). What follows is the comparison the record supports.

### 4b. `2021[Cu][sql]2` against the intact pillared sibling `2017[ZnSi][sql]2`

| species | `2021[Cu][sql]2[ASR]6` | `2017[ZnSi][sql]2[ASR]1` | present in the Cu entry? |
|---|---|---|---|
| metal | `Cu4` | `Zn4` | yes |
| **Si** | **absent** | **`Si4`** | **NO** |
| **F** | **absent** | **`F24`** | **NO** |
| S | absent | `S8` | no — *linker difference, see note* |
| N | `N16` | `N16` | yes |
| C | `C128` | `C80` | yes |
| H | `H96` | `H64` | yes |

**The species absent from the Cu entry and present in the intact sibling are `Si` and `F`, in the
ratio Si₄F₂₄ = 4 × SiF₆.**

**Are the missing species anionic? Yes.** Hexafluorosilicate, **SiF₆²⁻**, carries −2. Four of them
carry **−8**. The Cu entry's own composition gives Cu₄ with no counter-ion of any kind: at Cu(II)
that is **+8** uncompensated, and 4 × SiF₆²⁻ balances it **exactly**. This is the arithmetic, and it
agrees with the smoke-world audit's stated mechanism verbatim: *"Cell formula Cu4 H96 C128 N16 = Cu4
plus exactly 8 neutral linkers and NOTHING else — no O, F, halide, S or B, hence no anion. Cu(II)
gives +8 per cell; 4 × MF6(2−) balances it exactly, i.e. [Cu(bpb)2(SiF6)], a SIFSIX-type
anion-pillared framework."*

**Note on `S8`, so the table is not over-read.** The two entries do not share a linker. The Cu entry's
`mofid-v1` linker is `n1ccc(cc1)c1ccc(cc1)c1ccncc1` (bis(4-pyridyl)benzene, C/H/N only); the ZnSi
entry's is `n1ccc(cc1)Sc1ccncc1` (bis(4-pyridyl)sulfide, which carries the S). **The S difference is
a linker difference and is not part of the missing anion.** Si and F are.

### 4c. `2019[CdSi][sql]2` — Si-containing, but not by the same mechanism

`Cd4 Si4 H112 C116 N8 O16` carries `Si4` and **no F**, with `O16` instead. Reported verbatim; this
entry's Si is not accompanied by fluorine, so it is not a SiF₆ pillar, and no further
characterisation of it is available in the metadata (§2, it has no row).

### 4d. ASR against FSR — the cleaning flags, and what they did and did not remove

| coreid pair | ASR formula | FSR formula | difference |
|---|---|---|---|
| `2021[Cu][sql]2[…]6` | `Cu4 H96 C128 N16` | `Cu4 H96 C128 N16` | **none — identical** |
| `2017[ZnSi][sql]2[…]1` | `Zn4 Si4 H64 C80 S8 N16 F24` | `Zn4 Si4 H64 C80 S8 N16 F24` | **none — identical** |
| `2019[CdSi][sql]2[…]1` | `Cd4 Si4 H112 C116 N8 O16` | `Cd4 Si4 H120 C116 N8 O20` | **`H8 O4` = 4 × H₂O** |

**The Cd entry is the control that makes the Cu result readable.** `Extension` separates
`All Solvent Removed` from `Free Solvent Removed` on every one of these structures, and on the Cd
entry that flag corresponds to a real compositional difference of exactly four waters. **On the Cu
entry the two cleaning variants are compositionally identical, and their densities are identical to
six figures (`0.358334`).** Whatever removed the Si and F, the cleaning-variant flags did not do it —
which is the smoke-world audit's *"The identical [FSR]6 formula shows this was not solvent removal"*,
here reproduced from the metadata with a positive control beside it.

---

## 5. Arithmetic checks on the verbatim fields

| coreid | formula sum of atoms | `natoms` field | agrees |
|---|---:|---:|---|
| `2021[Cu][sql]2[ASR]6` | 4+96+128+16 = **244** | `244` | yes |
| `2017[ZnSi][sql]2[ASR]1` | 4+4+64+80+8+16+24 = **200** | `200` | yes |

*(`2019[CdSi][sql]2` has no `natoms` field to check against — §2.)*

— Bei (harness), read-only, 2026-09-02
