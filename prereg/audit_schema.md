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
| `note` | string (optional) | Free-text detail; required when `audit_outcome` is `other` |

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
