# BENCHMARK PROVENANCE — the pulled release

*Q1 step 2, PI ruling 2026-08-29 option 1. **Nothing here is frozen yet** — the diff against the
group share was non-empty, which under that ruling stops the process for a report. See
`prereg/seal_notes.md`, "Q1 — STEP 2 REPORT".*

## What was pulled, and how it was verified

| | |
|---|---|
| Record | Computation-Ready Experimental Metal-Organic Framework (**CoRE MOF**) **2024** Dataset |
| Version | **1.1** |
| Published | **2025-03-20** |
| DOI | **10.5281/zenodo.15055758** |
| URL | `https://zenodo.org/records/15055758` |
| Pulled | 2026-08-29, to `/home1/users/Bei/benchmark/staging/` (Bei-owned, ruling 4) |

| File | Bytes | MD5 (published → ours) | SHA-256 (ours) |
|---|---:|---|---|
| `CoREMOF2024DB_SI_20250204.zip` | 44,022,768 | `240444c92c1868ee131ab7b059f45b05` → **match** | `d07a0c1f0161a12ae998ea9531cc3bc333ad0e8cacd8c5c097fcc7e88006fa8a` |
| `12089-recommended-screening-list.csv` | 330,691 | `7887c53f0ebeea1142dfc5bf1403f7e2` → **match** | `f7f5784b079661b4cdff11ecb86f6751a1ed1df91562865d4b1d6a99bd8cddeb` |

**The MD5s are the record's own published checksums**, compared after download. The pull is
authentic; that is settled and does not depend on any later decision.

## Composition — 8,300 CIFs

| Subset | Count |
|---|---:|
| **CR — computation-ready** | **2,664** |
| — ASR / FSR / ION | 1,372 / 1,192 / 100 |
| **NCR — not computation-ready** | **5,636** |
| — both / mofchecker / Chen_Manz / occupancy | 3,692 / 1,073 / 562 / 309 |

## The release is the SI portion, not the full database

Published composition of CoRE MOF DB 2024: **40,837** = **SI 8,300** + **CSD-modified 20,276** +
**CSD-unmodified 12,261**. The Zenodo record above is the **SI** portion. The other **32,537**
structures are distributed through the **CCDC** portal and require an account.

The record's own `12089-recommended-screening-list.csv` names 12,089 structures of which only
**1,920 are inside the zip it ships with** — so the list indexes the full database, not the SI
release.

## Relationship to what this study already holds

- **The group share `/home/molsim_share/core2024_cifs`** (12,471 CIFs) shares **2,636** names with
  this release, **all byte-identical**, and holds **no NCR structures**. Its remaining 9,835 are
  not in this release. Its count matches no published figure; nearest is CSD-unmodified (12,261),
  off by 210. **Corroboration, never the source** (ruling 1).
- **The frozen 1,731-structure smoke slice** is **720 inside this release (41.6 %)**, all in CR;
  **1,011 are not in it**. The slice remains hash-pinned by `benchmark/MANIFEST.sha256` and is
  Cooper's world regardless — but **1,011 of its structures have no established licence status**,
  and `benchmark/` is tracked in a publicly readable repository. Flagged for the PI; Bei cannot
  determine it.

## Sources

- CoRE MOF 2024 Dataset — https://zenodo.org/records/15055758
- CoRE MOF 2025 Dataset — https://zenodo.org/records/15621349
- CoRE MOF DB (Matter, 2025) — https://www.cell.com/matter/abstract/S2590-2385(25)00183-3
- CoRE-MOF-Tools — https://github.com/Chung-Research-Group/CoRE-MOF-Tools
- CCDC downloads — https://www.ccdc.cam.ac.uk/support-and-resources/downloads/
