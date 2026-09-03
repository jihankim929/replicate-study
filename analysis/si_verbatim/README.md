# `analysis/si_verbatim/` — verbatim SI extracts

*Every file here is copied or extracted from the sealed records without paraphrase.*

**Assembled 2026-09-03, completed 2026-09-04. Sources read at `HEAD = 597f3db`; this index regenerated at `7213a879541ffd71d4785bf725ab4f90ada1209f`.**

---

## Status — complete

**Twelve files for the original SI request, plus `behavior_rules.csv` for Supplementary
Table S3 (added 2026-09-04). Thirteen in all.** Three carry a disposition worth reading before use:

| File | Disposition |
|---|---|
| `band_source.md` | **CLOSED, and nothing in it goes to the SI.** The 199.7 ± 3.2 band was searched for exhaustively and is not in this repository; PI disposition 2026-09-04 is that it originated outside the repository and is **withdrawn from the SI**. The file is retained as the record of the question. Its four candidate quantities are not the band and must not be cited as such. |
| `warning_passages.csv` | Produced 2026-09-04 from the Table S4 rows supplied by the PI. Table S4 itself is main-text and is not in this repository; the rows were taken as given and every quotation in them was then **verified back into the agents' filed records — 15 of 15**. |
| `behavior_rules.csv` | Produced 2026-09-04, read-only. Carries a **measured residual arm confound in column `c1`** found while writing it: c1's `reproduc\w+ from ... archived` branch is near-verbatim Appendix A G6, which only the gated arm received. Removing that branch moves c1 from gated 8/8 vs ungated 1/8 to **6/8 vs 1/8**. Nothing was corrected — the flag is in the file's `design_note` and in REPORT 058. |

## Answer-key access — logged

`exclusion_set.csv` reads out sealed material from `answer-key/`. That access is **logged as
access 5** in `answer-key/ACCESS_LOG.md` (2026-09-04, on explicit PI instruction), together with
the scope stated against access 4 — access 5 reads out the exclusion-set **reasoning**, which
access 4 explicitly withheld — and with the fact that the entry was written ~21 h after the read
it records. Nothing else in that directory was read out.

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
- **Method:** Structures, files, net and per-metal from FINAL STATE OF THE EXCLUSION SET - SEALED (exclusion_set_record.md:1089); grounds verbatim from the PI dispositions (:948); phi_He and rho from the anomalous-void candidate table (dossier_sitting:89), the values the disposition rule was applied to. Cross-checked against analysis/descriptors.csv: all eleven files agree and each coordinate-identical twin shares its group's values. Reads out sealed material - LOGGED as access 5 in answer-key/ACCESS_LOG.md on 2026-09-04.

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
- **Method:** Entry text extracted verbatim from the harvest. Each mapping to a v1.0 edit was verified against the charter's own revision record and by git diff of prereg/charter_v0.9.md between db78835 (Rev 17) and HEAD; where no edit followed, the row says 'None' and names the diff that establishes it. Three entries are attributed in the record itself (s01 LOG.md:141 -> Rev 18; s02 LOG.md:11 and :276 -> Rev 19 §2).

### `warning_passages.csv`

Every row of main-text Table S4: the full passage as filed, with its file and line location in the agent's workspace.

- **sha256** `b983ccf95f103926d816a1c585c29109f993b7ce2cdc7cb6069d8e0db4f18095`  (13,434 B)
- **Sources:**
  - `reps/main/collected/rep01/REPORT.md` — `96103b24777a21af926f3dce70f24fd5ead439db01adc13105336c418e0a0d7c`
  - `reps/main/collected/rep02/REPORT.md` — `8e994f58c41db7da0a13595f5d59b2428a72d4ab08a70bfa402c51037e914aec`
  - `reps/main/collected/rep03/REPORT.md` — `2cd6d633074f780bd3eb1b6b35053040d204078b9a0aabd31f09924df00c9f2a`
  - `reps/main/collected/rep05/REPORT.md` — `cd57c86ffa8c09b5be2507a50c7cfe757231ea8765550caacc817cc4cad6679d`
  - `reps/main/collected/rep06/REPORT.md` — `baacd24b9804fb060aeda0285125fa50eba58d93f802dcef35be02e19330526d`
  - `reps/main/collected/rep08/REPORT.md` — `858d0dc5de823f15d39f34e8bec25aaf8ae9d536bab1a2b3aa753cc306d39c2b`
  - `reps/main/collected/rep11/REPORT.md` — `c6854f10e96afa794d4c43852c4169cbf4febd8345e0d4efc85523282f37e65c`
  - `reps/main/collected/rep12/REPORT.md` — `507e834ce442dc65b78f1c8d348cd427ba561f3eea688f39cf3ff35e677238a7`
  - `reps/main/collected/rep16/REPORT.md` — `40a86a0be48455e500c0863d99c5aa2809115a060ad06586229378d3cda2dda9`
  - `reps/main/collected/rep17/REPORT.md` — `61492553a7d4a54c370f2360290de8f112c3ce05902760d6d3fa543cdfaf40b1`
  - `reps/main/collected/rep01/LOG.md` — `8761f7ad3515348d44151949eb25162dc0b41562dce697b5466065bddf3d5617`
  - `reps/main/collected/rep05/LOG.md` — `f52e1bfecb198642cf40c975edec967e36c167e54b04031d9c195b436c92572e`
  - `reps/main/collected/rep08/LOG.md` — `e733f361eb39c4dc841a5bc846d9c102ff0437038c856790a8d23670b7715c8a`
  - `reps/main/collected/rep12/LOG.md` — `9f80f5da74da48077c25f15332ab050cc3c80db1f0a8ed6b99f13455322ead5e`
  - `reps/main/collected/rep17/LOG.md` — `6f25e24195736c50a95666e18862a2d81ce694430ced52714fb2cec7964e6f44`
- **Method:** 15 rows for 13 Table S4 rows: row 13 names three agents and is emitted as 13a/13b/13c so each passage carries its own locus. full_passage is the complete paragraph containing the quotation, extracted verbatim by line range; quoted_line is the line carrying the Table S4 text and passage_lines the paragraph's bounds. EVERY Table S4 quotation was checked back into its extracted passage after whitespace normalisation: 15 of 15 verified, 0 failed, and the seven numeric assertions (358, 1,255, 0.876, 27,000, 1,132, 1,376, +8) all present. Each row's checked/unchecked group was asserted against harness/config.arm_of: 15 of 15 agree, which independently confirms checked=gated and unchecked=ungated. All ten agents filed as REPORT.md (REPORT_FILENAME_AS_FILED); collected copies are byte-identical to the workspace files at the bell per reps/main/collected/BELL_FINGERPRINT.log.

### `behavior_rules.csv`

The mechanical rule behind each of the nine behavior columns of `reports/behavioral_counts.csv`, as implemented in `harness/behavioral_extract.py`, with the per-agent y/n values. One row per behavior.

- **sha256** `604e2f1dfc8d02dfe0337c2604a59d1dacacf904e75d7673a108b795c2460bdd`  (9,435 B)
- **Sources:**
  - `harness/behavioral_extract.py` — `8fa1f0e2468da5652a96aec5d6fb8b2f65995e6955e12f97fab5059ea50bf2b4`
  - `reports/behavioral_counts.csv` — `ec037d3f0a95d7b4e208bb87e832a60923ef60e94daca16845da23c6304bbad0`
  - `prereg/rubric_v1.0.md` — `0d66608d24792e55666f446ad786799f18579fa231d11d5b3cf1cba0009ba5ec`
- **Method:** 9 rows, 30 columns. Per behavior: the rubric criterion it enumerates, the record read (each agent's whole filed `REPORT.md`), the preprocessing (`normalize()` + `flat()`), the **regex verbatim as implemented**, the match rule, every manual override with its locus verbatim, and the sixteen per-agent values. Read-only: the instrument's `extract()` was imported and called, never `main()`, so neither `reports/behavioral_counts.csv` nor `analysis/claim_table.csv` was rewritten. **All 144 committed cells were re-derived from the instrument and reproduce exactly (0 mismatches)**, and all 144 were then cross-checked between this file and `behavioral_counts.csv` (0 mismatches). Overrides are separated into those that **change** a regex result (5) and those that are **no-ops** confirming it (5). A tenth candidate criterion, "matched control" (G5), is not a column — see the `design_note` on `c1`.

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

- **sha256** `d64a7f0ff4a424a0f0777f33c36a5572436ac484462606f11f1d28d3690d8ab3`  (11,619 B)
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
- **Method:** Quotation only; every block carries its file and line, and all thirty-two citations were checked line by line against source. No forced filing occurred under §5 - the deadline was the terminator. The one filing that was forced was s02 forcing it on itself against a cap the harness was not enforcing.

### `amendments.csv`

Date and commit hash of the two pre-analysis amendments and of the Figure 4 amendments.

- **sha256** `2cc986019dd5c8af96b1770f3aaca1c2c5c8d2e395a3f572c74971339990dcac`  (13,557 B)
- **Sources:**
  - `reports/REPORTS.md` — `97b4fc42901a08aa7edbd62f831e43e2e6b5df4e0765a5e0cbad1caeb5c53227`
  - `prereg/fig4_order_amendment_2026-09-03.md` — `0c755ef5872945fe9c9e86110400e48e61c1207b037c3d199ea964277838f85e`
- **Method:** Commit hashes and timestamps read from git; subjects are the commit subjects verbatim. Four rows: the 2026-09-02 pre-analysis amendment (REPORT 021), the 2026-09-03 Figure 4 interim plan filed as a pre-analysis amendment (REPORT 043), and the two Figure-4 amendments of 2026-09-03 (queue order, REPORT 051; milestone posts on request).

### `band_source.md`

Origin of the 199.7 ± 3.2 cm³ cm⁻³ band and the σ = 3.2 provenance spread. CLOSED - the band originated outside this repository and is withdrawn from the SI.

- **sha256** `983a7001f40721c36989d8dc81d4ec3ca1c33e12aa331e2002b31b838d75285c`  (6,245 B)
- **Sources:**
  - (searched: whole repository)
- **Method:** NEGATIVE RESULT, closed by PI disposition 2026-09-04: the band originated outside this repository and is withdrawn from the SI. The file stands as filed with the disposition appended, not rewritten. Its four candidate quantities are NOT the band's origin and must not be cited as such; they are retained only as evidence that the search was exhaustive. No quantity in this file is carried into the SI.

