# `analysis/si_verbatim/` — verbatim SI extracts

*Read-only deliverable. Every file here is copied or extracted from the sealed records without
paraphrase. Nothing in this directory was written back into any record, workspace or ledger.*

**Assembled 2026-09-03 against `HEAD = 597f3dba24a741c384e13d17b77a25ae97de4cf8`.**
Source hashes below are of the working-tree files as read.

---

## Status

**10 of 12 requested files are complete. 2 could not be produced from the sealed records:**

| File | Status |
|---|---|
| `warning_passages.csv` | **NOT PRODUCED.** Requires the rows of main-text Table S4. There is no manuscript in this repository (`prereg/rubric_v1.0.md:14`, `STATE.md:1124`, `LOG.md:1857`, `reports/REPORTS.md:5371`), and `Table S4` appears nowhere in the record — the only supplementary table named anywhere is Table S5, in REPORT 055. Supply Table S4's rows and the file follows directly. |
| `band_source.md` | **PRODUCED AS A NEGATIVE RESULT.** The band `199.7 ± 3.2` and a σ of 3.2 described as a provenance spread do not occur anywhere in this repository. The file records the search, the four nearest candidates with their loci, and what is needed to close it. |

Nothing was invented to fill either gap.

---

## Answer-key access

`exclusion_set.csv` reads out sealed material from `answer-key/`, which opens **only on explicit
PI instruction** (standing rule, 2026-08-26), and every opening must be logged in
`answer-key/ACCESS_LOG.md` — *"An unlogged access is a defect even if it was authorised."*
This access is **not yet logged**: logging it is a write to `answer-key/`, and this deliverable
was specified as read-only. **It needs a log entry before it is closed.** The scope read out is
wider than any prior access: the six structure ids, their files, net charges, φ_He, densities,
mechanisms and the disposition rule and grounds — i.e. the exclusion-set reasoning itself, which
access 4 explicitly withheld.

---

## Files

### `charter_v1_common.md`

Charter v1.0 common body, as rendered for the ungated (unchecked) arm — everything before Appendix A, which is omitted verbatim. Ends at §9.

- **sha256** `1274611fcf94fe11c4be473445bd552d4b314804233b7660ca28486dc5fbd7eb`  (14,416 B)
- **Sources:**
  - `prereg/charter_v0.9.md` — `205d7d8ba8f9e7a6eab6507aa63ea66ccdbd7136fe372462ba9e31cfb52d3f24`
  - `harness/provision.py` — `c834e5f1dd681b6b35fdc10c938e8ba1f0036548f98e3a8399a5b9b5d9b3d1d4`
  - `harness/config.py` — `865d02f89764f3a747a632099a3e070c0dc7b3db7f956128f89914cf1e1a8c0c`
  - `prereg/arm_assignment.txt` — `e0e179cf36eb7fdd324d1e0eef3333a7e1ff72ab169eac8ad64dbb290965185e`
- **Method:** Rendered through the provisioning pipeline exactly as harness/rerender_charter.py does: split_charter(render_phase_prose(render_phase_rows(src,'main'),'main'),'ungated'). Verified: 0 unrendered phase spans, and the Appendix A marker is absent.

### `charter_v1_appendixA.md`

Appendix A — Audit Gates, as rendered for the gated (checked) arm. The span from the appendix marker to the REVISION RECORD separator.

- **sha256** `4cdeedf9703e622f7d0fe29c51444853ff86d53ec7958a73df55e90a64ef6c3a`  (7,150 B)
- **Sources:**
  - `prereg/charter_v0.9.md` — `205d7d8ba8f9e7a6eab6507aa63ea66ccdbd7136fe372462ba9e31cfb52d3f24`
  - `harness/provision.py` — `c834e5f1dd681b6b35fdc10c938e8ba1f0036548f98e3a8399a5b9b5d9b3d1d4`
  - `harness/config.py` — `865d02f89764f3a747a632099a3e070c0dc7b3db7f956128f89914cf1e1a8c0c`
  - `prereg/arm_assignment.txt` — `e0e179cf36eb7fdd324d1e0eef3333a7e1ff72ab169eac8ad64dbb290965185e`
- **Method:** Same pipeline, arm='gated'. The gated render is the full charter (split_charter returns it unchanged); Appendix A is extracted between C.APPENDIX_MARKER and '# REVISION RECORD'. Verified: 0 unrendered phase spans.

### `charter_revisions.csv`

One row per revision Rev 12 to Rev 21: date, change summary, triggering record.

- **sha256** `d9ce06019163baa5e3f068a8b9430d8b1f08fde3f4139fabe4b77d63499c76ab`  (3,531 B)
- **Sources:**
  - `prereg/charter_revisions.md` — `8396d50f7fe350827f8d652c234b212ee492a4909b745d2dd12b05f6472bf9fb`
- **Method:** date and change_summary are the revision heading verbatim; triggering_record is the section's first attribution paragraph verbatim, whitespace-normalised only. Extracted programmatically, not transcribed.

### `exclusion_set.csv`

The six excluded structures: file identifiers, metal, topology, net charge under the three-pass audit, He void fraction, framework density, and the disposition rule applied.

- **sha256** `d6deb5f44313fb54666fd7250c8e3da06d7d5429556a6bde548f04d4c8b520af`  (4,513 B)
- **Sources:**
  - `answer-key/exclusion_set_record.md` — `dcd6e48ca16661000872901eb3cbae6f1437a4000252bb9fbf47b141c1036f34`
  - `answer-key/dossier_sitting_2026-08-29.md` — `bf38b3a686a32a63fc11745ad21c4c06bbdc3ac624cd4654859efeb2e2f53d6d`
  - `analysis/descriptors.csv` — `435f3f3cddc3b9013e0cb643f6e403b950f90a783bcdba30e691954bb7d503e1`
- **Method:** Structures, files, net and per-metal from FINAL STATE OF THE EXCLUSION SET - SEALED (exclusion_set_record.md:1089); grounds verbatim from the PI dispositions (:948); phi_He and rho from the anomalous-void candidate table (dossier_sitting:89), the values the disposition rule was applied to. Cross-checked against analysis/descriptors.csv: all eleven files agree and each coordinate-identical twin shares its group's values. THIS FILE READS OUT SEALED MATERIAL - see the access note below.

### `defect_ledger.csv`

SI-001 to SI-020: defect, subsystem, how it manifested, how it was caught, the fix, and the projected fleet-scale consequence.

- **sha256** `c17bf2ee147618af0b51fc732c99bce57742e6c586e48fc85cdf39f30e5c4815`  (36,713 B)
- **Sources:**
  - `SI_LEDGER.md` — `5a9834e19b64e8c65eac113dafbb1da75f6dde6a7c2591ad73f7ffd8451d22f0`
- **Method:** Verbatim spans from each entry. The ledger is prose, not fielded, so each column is the entry's own sentences for that aspect. Where an entry states no N-scaled projection, the fleet-scale column says so rather than supplying one. SI-017 carries both the entry as filed and its same-day correction, per the append-only rule.

### `charter_read_entries.csv`

The eleven smoke-phase CHARTER-READ entries and the v1.0 edit each produced.

- **sha256** `8826a5543adada265ce822a0a19a52f0ad8a88bc85290305f813ab363f586413`  (12,277 B)
- **Sources:**
  - `reps/smoke/collected/CHARTER_READ_HARVEST.md` — `8ebcd23bb129241a6875dac7cc91c64d719b004b325830cf457a138ae1bfb84d`
  - `prereg/charter_revisions.md` — `8396d50f7fe350827f8d652c234b212ee492a4909b745d2dd12b05f6472bf9fb`
  - `prereg/charter_v0.9.md` — `205d7d8ba8f9e7a6eab6507aa63ea66ccdbd7136fe372462ba9e31cfb52d3f24`
- **Method:** Entry text extracted verbatim from the harvest. Each mapping to a v1.0 edit was verified against the charter's own revision record and by git diff of prereg/charter_v0.9.md; where no edit followed, the row says 'None' and names the diff that establishes it. Two entries (s01 LOG.md:141 -> Rev 18; s02 LOG.md:11 and :276 -> Rev 19 §2) are attributed in the record itself.

### `rubric_sealed.md`

The scoring rubric as sealed, with tier definitions and the flag-set convention.

- **sha256** `0d66608d24792e55666f446ad786799f18579fa231d11d5b3cf1cba0009ba5ec`  (13,706 B)
- **Sources:**
  - `prereg/rubric_v1.0.md` — `0d66608d24792e55666f446ad786799f18579fa231d11d5b3cf1cba0009ba5ec`
- **Method:** Byte-for-byte copy. The rubric was created at the seal commit c67fff5 and has not changed since, so HEAD is the sealed text. Tier definitions at §(a)-(d); flag-set convention at (c2): multi-entry flag lists score as correct screening, never as over-flagging; protonation-ambiguous flags score neutral credit.

### `launch_times.csv`

Launch timestamp and stamped deadline for all sixteen agents, with arm, campaign hours, deadline basis and fault-restoration credit.

- **sha256** `4b274b740c6818ee19b5e6fec14030683fb40538ade4628095276d6926a55174`  (6,522 B)
- **Sources:**
  - `reps/main/collected/rep*/WORKSPACE.json` — 16 files
    - `reps/main/collected/rep01/WORKSPACE.json` — `12b4c6dea0453eee438eec3d0fe3a8a204634a2c5bde47ea230935964be965c9`
    - `reps/main/collected/rep02/WORKSPACE.json` — `195d05d2a74cd35079d4342f9ccba2a061e06183abe85e20b7c6b7b19fed8dd2`
    - `reps/main/collected/rep03/WORKSPACE.json` — `1cbeb9382d800cca23edac030285e499da101344129d9b6da6464bb58342773d`
    - `reps/main/collected/rep04/WORKSPACE.json` — `36426611d35b29c89f0fe3bebc751ac0213195e3cf8405a982493796c9a18abf`
    - `reps/main/collected/rep05/WORKSPACE.json` — `40620bf083491399cf384879220f018950b84f7502576bc1cd0da43e738e2e1d`
    - `reps/main/collected/rep06/WORKSPACE.json` — `3e30f23abedbe141d8e1fdf20d7868353fe761c2f2a6bf5849ff3818eb6b236e`
    - `reps/main/collected/rep07/WORKSPACE.json` — `400c9d12e8807dd96570c56a004fc14adf7cfbdcf0d0c2574306dde17a7e7ff6`
    - `reps/main/collected/rep08/WORKSPACE.json` — `2a55aa8bbfca35de66576e9f668f9b271f035c8d3533b191d8db4e49301fd364`
    - `reps/main/collected/rep09/WORKSPACE.json` — `0662dcb01799d5c2ea8831670f91c20f9e2a4d7b622288b8208450dbb6ea80d6`
    - `reps/main/collected/rep10/WORKSPACE.json` — `e32baba54c6ec70d193bb5b53d00681396e9156dbf684f3f52f03c3327793b7e`
    - `reps/main/collected/rep11/WORKSPACE.json` — `e06f5603313896f5f67b63c22de19150d3a1d914d3a393ab5600dc2c16007d59`
    - `reps/main/collected/rep12/WORKSPACE.json` — `c2431ae5e57b815306105e3894dbf63eb1cd4b0436e02114f1147f360ddc7910`
    - `reps/main/collected/rep13/WORKSPACE.json` — `574b6360403cdfdc62f6ec2ad936026880c3c008c7130bf5ad7d6f90adaf65a3`
    - `reps/main/collected/rep15/WORKSPACE.json` — `6489ed8e80cea478573d8773eee2e9bd6e8ddc5034eb676446cf0e766de3840d`
    - `reps/main/collected/rep16/WORKSPACE.json` — `2c9641b8011045a58aeb4ebe1d50852836dc53520111a1597433e2b8f6c683fb`
    - `reps/main/collected/rep17/WORKSPACE.json` — `81cca7e41f8eb88c352696b5be6fafbc1132cc3283627e47e3d82176e9a0a46c`
  - `prereg/arm_assignment.txt` — `e0e179cf36eb7fdd324d1e0eef3333a7e1ff72ab169eac8ad64dbb290965185e`
- **Method:** launched_at and deadline_kst read from each collected WORKSPACE.json as stamped; arm from the sealed draw via harness/config.arm_of. 16 rows, 8 gated / 8 ungated.

### `smoke_endgame.md`

Endgame behaviour at the deadline, forced-filing observations, and final burn and cost for both smoke agents.

- **sha256** `f2dc9f165eaf42c9337c58dcaefe08a04ac62028b0479aaea96c1c39fa39b59b`  (11,619 B)
- **Sources:**
  - `reps/smoke/collected/COLLECTION.md` — `8c6b1f9441842725da9028507f208cb36cc126c756212fa41ccbbb0edae7d2d3`
  - `harness/sessions/s01.loop.log` — `b04226cdb052629a856ec51e6b041673355c22dbca25f8b53602c3e645d00165`
  - `harness/sessions/s02.loop.log` — `0f3714296525dc022d24e0d4627446ed2c6a067b94cd9a23d9cedf54ac28347f`
  - `harness/LAUNCH_GATE.md` — `8a138df82a8e77e8ab658129e745b41b8cf011d39d22c80c47a1e41ab752a602`
  - `SI_LEDGER.md` — `5a9834e19b64e8c65eac113dafbb1da75f6dde6a7c2591ad73f7ffd8451d22f0`
  - `LOG.md` — `bb9993fb2441f1cb9572362808fb33496c17a566d5b10282fd493bb0bde05ec5`
  - `reps/smoke/collected/s01/git-log.txt` — `3fb817b05a6bb82cc73df4c93734441e07a9a460ebd2ba634b525c8170741a81`
  - `reps/smoke/collected/s02/git-log.txt` — `39566099b973f34bd1fcf2e02f71fa9dcf8b554d0e2ffaa0df6715f1a37494eb`
  - `reps/smoke/collected/s02/LOG.md` — `60803008be07343db4e054305295a4023d615eaa617a18144e3723954423b0b1`
  - `prereg/context_composition_2026-08-29.md` — `726bd98dca0e6edc4c4c2fe8f9ed92a123f27439f9cf249229512079cd06cca8`
- **Method:** Quotation only; every block carries its file and line. No forced filing occurred under §5 - the deadline was the terminator. The one filing that was forced was s02 forcing it on itself against a cap the harness was not enforcing.

### `amendments.csv`

Date and commit hash of the two pre-analysis amendments and of the Figure 4 amendments.

- **sha256** `2cc986019dd5c8af96b1770f3aaca1c2c5c8d2e395a3f572c74971339990dcac`  (13,557 B)
- **Sources:**
  - `reports/REPORTS.md` — `78d51c7c4d2e08f5000c68c05006ae2fc87c216655c3fb3b6a2a3be4e52ab210`
  - `prereg/fig4_order_amendment_2026-09-03.md` — `0c755ef5872945fe9c9e86110400e48e61c1207b037c3d199ea964277838f85e`
- **Method:** Commit hashes and timestamps read from git; subjects are the commit subjects verbatim. Four rows: the 2026-09-02 pre-analysis amendment (REPORT 021), the 2026-09-03 Figure 4 interim plan filed as a pre-analysis amendment (REPORT 043), and the two Figure-4 amendments of 2026-09-03 (queue order, REPORT 051; milestone posts on request).

### `band_source.md`

Origin of the 199.7 ± 3.2 cm³ cm⁻³ band and the σ = 3.2 provenance spread. INCOMPLETE - the band is not in the record.

- **sha256** `ad2bd7e1c8a77c236503b4f06b6489bb06993854bb24b826ca9c6a65610873ae`  (5,405 B)
- **Sources:**
  - (searched: whole repository)
- **Method:** NEGATIVE RESULT. Neither '199.7 ± 3.2' nor a sigma of 3.2 described as a provenance spread occurs anywhere in this repository. The band is presumably a main-text quantity, and the record states three times that there is no manuscript here. The file records the search, the four nearest candidates in the record with their loci, and what is needed to close it.

### `warning_passages.csv`

For each row of main-text Table S4, the full passage and its file and line location.

- **NOT PRODUCED.** See Status above.
- **Blocked on:** the rows of main-text Table S4, which is not in this repository.

