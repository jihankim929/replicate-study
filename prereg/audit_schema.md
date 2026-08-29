# AUDIT.jsonl — Schema
*(Referenced by Charter Appendix A. One JSON object per line; append-only; corrections are new lines with `audit_outcome: "correction"` referencing the original's `ts` and `structure_id`. Passes are recorded as well as failures — the denominator matters.)*

## Fields

| Field | Type | Meaning |
|---|---|---|
| `ts` | string | ISO 8601 timestamp with timezone |
| `structure_id` | string | Canonical identifier of the structure (database filename stem, or modified-structure ID) |
| `gate` | string | Which rule fired: `G1`–`G7` |
| `stage` | string | `pre-sim`, `post-sim`, or `finalist` |
| `apparent_value` | number \| null | Working capacity (cm³/cm³) that triggered the event; `null` for pre-simulation events |
| `audit_outcome` | string | Controlled vocabulary (below) |
| `disposition` | string | `killed`, `flagged_pending`, `passed`, `promoted_to_finalist` |
| `log_ref` | string | Pointer to the LOG.md entry or work file with full reasoning |
| `commit` | string | Git commit hash of the event |
| `criterion` | object (optional) | **Required on every `G4` event** (charter Appendix A, G4 clause (c), Rev 18). Structured, not prose — see below |
| `note` | string (optional) | Free-text detail; required when `audit_outcome` is `other` |

## `criterion` — G4 clause (c), first-class from v1.0

Added by PI ruling 2026-08-29: *"add a first-class `criterion` field at v1.0 so G4(c) is
satisfiable as structure, not free text."*

Clause (c) requires the criterion, the chosen thresholds, and — where the Claim's identity turns
on a threshold — a sensitivity report. In the smoke this was written into `note` as prose. That
was good practice and it is **not comparable across twenty trajectories**: comparison across arms
is the study, and prose does not aggregate.

| Key | Type | Required when |
|---|---|---|
| `rule` | string | always — a short stable name for the test applied, e.g. `open_metal_reachability` |
| `class` | string | always — which G4 clause fired: `a` (caveat class, claimable), `b1` (agent-created bare coordination site), `b2i` (element absent from the pinned `pseudo_atoms.def`), `b2ii` (element present but unreliable) |
| `thresholds` | object | whenever the rule uses any replicate-chosen number. Keys name the quantity and its unit, e.g. `{"theta_open_deg": 60, "ch4_centre_max_A": 4.2}` |
| `element` | string | `b2i`, `b2ii` — which element |
| `parameter_concern` | string | `b2ii` — what about its parameterisation is in doubt |
| `materiality` | string | `b2ii` — why the guest's contact with it is material to the number |
| `sensitivity_ref` | string | whenever **the identity of the Claim depends on a threshold above** — pointer to the sensitivity report |

**`b2ii` requires `element`, `parameter_concern` and `materiality` together.** That is not schema
tidiness, it is the ruling: leg (ii) is argued **per structure, never per element roster**, and a
flag missing any of the three **is not a G4 finding**. The schema is where that becomes checkable
instead of merely stated.

### Example — a class (a) event, claimable with the mandatory caveat

```json
{"ts": "2026-09-02T14:31:00+09:00", "structure_id": "<id>", "gate": "G4", "stage": "pre-sim",
 "apparent_value": null, "audit_outcome": "exposed_metal", "disposition": "passed",
 "criterion": {"rule": "open_metal_reachability", "class": "a",
               "thresholds": {"theta_open_deg": 60, "ch4_centre_max_A": 4.2},
               "sensitivity_ref": "LOG-2026-09-02-11"},
 "log_ref": "LOG-2026-09-02-04", "commit": "a1b2c3d"}
```

### Bei-proposed, UNRATIFIED — the disposition vocabulary is now inconsistent with G4 v1.0

Flagged, not applied. `disposition` still offers **`killed`**, and for a `G4` event that value is
**forbidden by the charter as of Rev 18**: A3 ratified that *"inadmissible means may not headline
— nothing more… There is no pre-simulation kill under G4."* A schema that still accepts
`{"gate": "G4", "disposition": "killed"}` will accept a line the charter forbids, silently.

Two additions would close it, and both need ratification because this document seals pre-launch:

- **`excluded_from_claim`** — the disposition for class (b). Measured, reported in the landscape,
  not eligible to headline. Distinct from `killed`, which no longer has a G4 meaning.
- **`caveat_attached`** — or keep `passed` and let `criterion.class == "a"` carry it. Bei prefers
  the latter: one fact, one place, and the class is already required.

Bei proposes rejecting `disposition: "killed"` on `gate: "G4"` outright at v1.0.

## Controlled vocabulary for `audit_outcome`

- `overlapping_atoms`
- `density_out_of_bounds`
- `charge_unbalanced_structure` — deposited or modified structure missing counter-ions, pillars, or other charge-compensating components
- `charge_artifact`
- `unconverged_gcmc`
- `exposed_metal`
- `uncapped_defect`
- `protocol_violation`
- `reproduction_failed`
- `reproduction_passed`
- `audit_passed`
- `correction` — supersedes an earlier line; `note` must reference it
- `other` — `note` field mandatory

## Example line

```json
{"ts": "2026-09-02T14:31:00+09:00", "structure_id": "2023[Zn][pcu]1[ASR]2", "gate": "G3", "stage": "pre-sim", "apparent_value": null, "audit_outcome": "overlapping_atoms", "disposition": "killed", "log_ref": "LOG-2026-09-02-04", "commit": "a1b2c3d"}
```
