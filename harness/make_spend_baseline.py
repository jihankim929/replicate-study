#!/usr/bin/env python3
"""Derive the carried-forward spend baseline from the append-only ledger.

Why this exists. `meter_spend.py` recomputes each replicate's total from the transcripts under
`~/.claude/projects/<mangled-local-cwd>/` on the machine it runs on. That is correct on one host
for the life of a campaign and wrong the moment the campaign changes hosts: on a fresh host those
directories are empty, every replicate meters $0.00 with a full $280 available again, and the one
budget STATE calls binding silently unbinds.

The baseline is taken from `harness/spend.jsonl` -- the append-only ledger -- and NOT from
`harness/state/fleet_spend.json`, which is a summary stamped at 2026-08-29T22:24:19Z, 11.5 minutes
before the fleet was confirmed fully down at 22:35:50Z. Sixteen sessions were still winding down
across that window, so the summary undercounts the ledger by $10.53.

It carries TOKEN COUNTS, not dollars, and the cost is recomputed from them at
`config.RATIFIED["price_per_token"]`. A baseline that hard-codes a dollar figure would freeze
today's list price into every future total; carrying tokens keeps the same single source of truth
the meter already uses. The recomputed cost is asserted against the ledger row it came from, so a
baseline that does not reproduce its own source refuses to be written.

  ./harness/make_spend_baseline.py            # write harness/state/spend_baseline.json
  ./harness/make_spend_baseline.py --dry-run  # print it, write nothing
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "harness" / "spend.jsonl"
PAUSE = REPO / "harness" / "state" / "PAUSE.json"
SUMMARY = REPO / "harness" / "state" / "fleet_spend.json"
OUT = REPO / "harness" / "state" / "spend_baseline.json"

FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
RATE_KEY = {"input_tokens": "input", "output_tokens": "output",
            "cache_creation_input_tokens": "cache_creation", "cache_read_input_tokens": "cache_read"}


def cost_of(tok: dict) -> float:
    rates = C.RATIFIED["price_per_token"]
    return sum(tok[k] * rates[RATE_KEY[k]] for k in FIELDS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    reps = json.load(open(PAUSE))["replicates"]          # the paused roster, smoke excluded
    last = {}
    for line in open(LEDGER):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r["replicate"] in reps:
            last[r["replicate"]] = r

    missing = [r for r in reps if r not in last]
    if missing:
        sys.exit(f"baseline: no ledger row for {missing} -- refusing to write a partial baseline.")

    per, total = {}, 0.0
    for r in reps:
        row = last[r]
        tok = {k: int(row["tokens"][k]) for k in FIELDS}
        usd = cost_of(tok)
        # A baseline that cannot reproduce the row it was derived from is not a baseline.
        if abs(usd - row["total_usd"]) > 0.01:
            sys.exit(f"baseline: {r} recomputes to ${usd:.4f} against a ledger row of "
                     f"${row['total_usd']:.4f} -- refusing.")
        per[r] = {"tokens": tok, "usd_at_current_rates": round(usd, 4), "ledger_ts": row["ts"]}
        total += usd

    summary = json.load(open(SUMMARY))
    doc = {
        "schema": "spend_baseline/1",
        "active": True,
        "_active_note": ("Set false ONLY if the transcript directories were carried across with "
                         "the repo, in which case the local tally already contains this spend and "
                         "adding it would double-count. meter_spend.py also refuses on its own if "
                         "it sees local transcripts that already cover the baseline."),
        "measured_on_host": "the retired supervision laptop (macOS, /Users/jihankim/replicate-study)",
        "basis": "latest harness/spend.jsonl row per paused replicate; token counts, cost recomputed",
        "ledger_last_ts": max(last[r]["ts"] for r in reps),
        "fleet_confirmed_down_utc": "2026-08-29T22:35:50Z",
        "n": len(reps),
        "cap_usd_each": C.RATIFIED["spend_usd"]["main"],
        "denominator_usd": len(reps) * C.RATIFIED["spend_usd"]["main"],
        "carried_usd_total": round(total, 4),
        "carried_fraction": round(total / (len(reps) * C.RATIFIED["spend_usd"]["main"]), 6),
        "supersedes_summary": {
            "file": "harness/state/fleet_spend.json",
            "fleet_spend_usd": summary["fleet_spend_usd"],
            "stamped": summary["ts"],
            "delta_usd": round(total - summary["fleet_spend_usd"], 4),
            "why": ("the summary was stamped 11.5 min before the last session stopped; the ledger "
                    "kept rising until 2026-08-29T22:35:14Z and was flat from there to the final "
                    "row, so the delta is real spend, not the meter re-tallying stopped sessions"),
        },
        "per_replicate": per,
    }
    text = json.dumps(doc, indent=2) + "\n"
    if a.dry_run:
        print(text, end="")
        return
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(REPO)}: {len(reps)} replicates, "
          f"${total:.2f} carried of ${doc['denominator_usd']:.2f} "
          f"({100*doc['carried_fraction']:.1f}%)")


if __name__ == "__main__":
    main()
