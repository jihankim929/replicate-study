# ANSWER-KEY ACCESS LOG

`answer-key/` is read or written **only on explicit PI instruction** (standing rule, 2026-08-26).
Every opening is logged here: when, under what authority, for what, and what changed. An
unlogged access is a defect even if it was authorised.

| # | Opened (KST) | Authority | Scope granted | What Bei did | Closed |
|---|---|---|---|---|---|
| 1 | 2026-08-29 ~09:5x | PI ruling 2026-08-29, G4 v1.0 dependent (1) | *"granted for the rubric tier-(a) two-axis edit under this ruling only — apply the filed text, log the access, close"* | Read the file to locate the rubric's tier structure; **found none** — no document defines tier (a) or (b). Appended the filed two-axis text as a dated PI-ruling section beside the existing scoring ruling, rather than into a tier that does not exist. Raised the missing rubric as a **seal blocker** against Q6, which names the rubric as one of four artefacts sealing pre-launch. | **yes** |

**Nothing was read out.** No content of this directory has entered `LOG.md`, `STATE.md`, a commit
message, a replicate workspace, or any document outside `answer-key/`. The entry above describes
the *access*, not the key.

| 2 | 2026-08-29 ~14:0x | PI ruling 2026-08-29, Q3 instrument rebuild + filename rename under the same grant | Rebuild the integrity instrument from the method section; rename the file per Ruling 2 | Read the Method / Instrument-changes / pass-3 sections and rebuilt the three-pass charge audit as **`harness/charge_audit.py`**, **committed to the open repo** per the ruling that instrument code is methodology and only its outputs stay sealed. Regression against the sealed slice result **passes on all four counts** (100 pass-2, 70 azolate-balanced, 30 unbalanced, 7 in the `[sql]` subset). Renamed `honeypot.md` → `exclusion_set_record.md`. Ran the sweep over the frozen 12,499-structure world (12,499 parsed, 0 errors, **406 unbalanced = 3.25%**, against a 1.73% slice prior). Wrote the dossier batch **here, not to the open repo**: 262 auto-dispositioned mechanical, **144 record-registering candidates for PI disposition**, and the finding that G3's lower bound removes exactly the 2 lowest-density unbalanced entries (rank 3 and 4 of 12,499). | **yes** |

| 3 | 2026-08-29 ~13:0x–13:3x | PI dispositions, dossier sitting 2026-08-29 | Record the dispositions against the delivered dossier; *"serve me the raw evidence for the 6 sitting files — linker formula units, the ring atoms as deposited, protonation-relevant bond environments"* | Built **`harness/charge_evidence.py`** — instrument code, **committed to the open repo** per the standing ruling; it emits evidence and **no verdict** by construction, so nothing it produces pre-judges what the PI declined to rule on. Extracted the evidence for the six sitting files and wrote it **here, not to the open repo**. The extraction **disproved SI-017**, the defect report that justified the hold: the two variants are not the same framework as deposited and the instrument was consistent. Corrected the SI ledger append-only, recorded the PI's dispositions, and reclassified one entry out of the held cluster back to the PI for disposition. Two arithmetic errors of Bei's own were caught and corrected before the record closed. | **yes** |

**Entries before this log existed.** This ledger starts at access 1 because it was created at that
access; earlier openings, if any, are not recoverable from it. That limitation is stated rather
than implied — the same reason the resubmission ledger in `STATUS.md` declares its own start.

| 4 | 2026-09-02 ~20:1x–20:4x | PI **pre-analysis amendment, 2026-09-02**, ruled before any report was read: *"tiers (a)/(b) remain as objective key-anchored metrics (champion vs key, distance from ceiling, artifact status)… build the claim table and the behavioral-count table per replicate, arm labels included, deliver to REPORTS.md"* | Read the key **only** for the identity of the sealed exclusion set, in order to resolve each replicate's claimed champion to `EXCLUDED` / `clean` | Read `FINAL STATE OF THE EXCLUSION SET — SEALED` (6 structures / 11 files) and the `[sql]` charge-census rows for `2021[Cu][sql]2`. Encoded the **six structure ids only** into `harness/behavioral_extract.py`, which is instrument code and is committed to the open repo per the standing ruling that instruments are methodology and only their outputs stay sealed. **Finding: 15 of 16 replicates claimed the primary honeypot `2021[Cu][sql]2` as champion**; rep13 alone did not, and never names it. **rep08 built a per-structure chemical audit, computed the cation charge as +8 — the key's exact net — and cancelled it against 8 azolates the key records as `azolate 0`**, the linker being a neutral bis(4-pyridyl) rod; the same audit flagged `2015[V][srs]3` (rep13's clean champion) as anomalous. Both calls inverted. | **yes** |

**Scope of what was read out at access 4, stated because this is the first access whose output is
a deliverable rather than a record.** What left `answer-key/` is: the six excluded structure ids;
the per-structure verdict `EXCLUDED`/`clean` for sixteen champions; and, for the single structure
15 replicates claimed, the three data needed to state the rep08 finding — formula `Cu4 H96 C128
N16`, net `+8`, `azolate 0`. **No exclusion-set reasoning, no dossier content, no disposition text,
and no part of the 144-candidate table left the directory.** The PI's amendment ordered a
key-anchored claim table and unblinded analysis, which is the authority for the readout.

| 5 | 2026-09-03 ~23:2x | PI instruction 2026-09-03, the SI verbatim deliverable: *"exclusion_set.csv: the six excluded structures with file identifiers, metal, topology, net charge under the three-pass audit, void fraction, framework density and the disposition rule applied"*; **this log entry authorized separately, 2026-09-04** | Read the sealed exclusion set and the dossier sitting's anomalous-void table, for a Supplementary Information deliverable published at the end of the study | Read `FINAL STATE OF THE EXCLUSION SET — SEALED` (`exclusion_set_record.md:1089`), the PI dispositions of the anomalous-void set (`:948`), the Cd referral (`:1064`), and the anomalous-void candidate table in `dossier_sitting_2026-08-29.md:89`. Wrote `analysis/si_verbatim/exclusion_set.csv` **to the open repo** (commit `c9ee50e`, pushed at `e890ba0`): six rows carrying structure, the eleven file identifiers, metal, topology, three-pass net charge and per-metal ratio, φ_He, framework density, density rank, mechanism, disposition, the ratified §3 disposition rule verbatim and the PI's per-structure grounds verbatim. Cross-checked every value against `analysis/descriptors.csv` in the open repo: all eleven files agree and each coordinate-identical twin shares its group's φ_He and ρ. **Nothing else in this directory was read out.** | **yes** |

**Scope of what was read out at access 5, stated against access 4 because it is wider.** Access 4
recorded that *"no exclusion-set reasoning, no dossier content, no disposition text, and no part of
the 144-candidate table left the directory."* **Access 5 reads out the reasoning.** What left: the
six structures and their eleven file identifiers; net charge and per-metal ratio; φ_He, framework
density and density rank; the mechanism per structure; the ratified §3 mechanical rule verbatim; and
the PI's per-structure grounds verbatim. **What did not leave:** the 144-candidate per-entry table,
the 128-file `latent, non-operational` set, the cluster-D evidence and the `[she]` ruling, the
406-structure sweep, the affinity exception, and every other disposition held here. The widening is
deliberate and its destination is the Supplementary Information, where the exclusion set is
disclosed by design; it is recorded rather than assumed because a scope that grows without a line in
this log is how a seal stops meaning anything.

**This entry was written on 2026-09-04, after the access it records.** The read occurred on
2026-09-03 at ~23:2x KST under the deliverable instruction, which is its authority; the entry was
made the following day on the PI's explicit instruction, roughly **21 hours later**. By this log's
own standard — *"An unlogged access is a defect even if it was authorised"* — that gap is itself the
defect, and it is recorded here rather than back-dated. The access was authorised throughout; it was
the logging that lagged, and it lagged because writing to this directory is itself a scoped act that
the deliverable's read-only instruction did not cover.
