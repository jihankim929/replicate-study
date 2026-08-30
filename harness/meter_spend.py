#!/usr/bin/env python3
"""Per-replicate SPEND metering, at published list rates, from Claude Code's own usage records.

Why this exists (PI ruling, 2026-08-29). The ratified token meter counts
input + output + cache_creation and EXCLUDES cache reads. Cache reads are not free -- they bill at
0.10x the input rate -- and on the collected smoke they were **59.2% of the actual cost**. So the
token cap bounds the meter, not the money: a replicate can sit well inside 32 M billable and still
have spent several times what that figure implies.

Measured on the smoke at list price: $20.54 per M billable for one arm and $32.54 for the other,
the difference being entirely their cache-read ratios (24.8x vs 36.3x against billable). A single
$/token constant would therefore have been wrong by 58% between two replicates of the same study,
which is why this meters the four token classes separately rather than scaling the token figure.

Rates come from config.RATIFIED["price_per_token"], never from a literal here -- the same rule
that preflight_billing.sh already follows for the token budget, and for the same reason: a gate
whose headline number is hand-copied certifies the wrong number.

  ./harness/meter_spend.py --replicate rep01
  ./harness/meter_spend.py --all --json
"""
import argparse, glob, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
RATE_KEY = {"input_tokens": "input", "output_tokens": "output",
            "cache_creation_input_tokens": "cache_creation", "cache_read_input_tokens": "cache_read"}


BASELINE = Path(os.environ.get("HARNESS_STATE_DIR", Path(__file__).parent)) / "state" / "spend_baseline.json"


def load_baseline() -> dict:
    """Spend carried forward from a previous host, per replicate, as TOKEN COUNTS.

    The meter recomputes every total from the transcripts under the LOCAL
    `~/.claude/projects/<mangled-cwd>/`. That is correct while a campaign lives on one machine and
    wrong the instant it moves: on a fresh host those directories are empty, so a replicate that
    has spent $99 meters $0.00 with a full cap available again. The cap does not fail loudly --
    it silently reopens. This carries the pre-move spend forward so the cap keeps binding across
    the move; `harness/make_spend_baseline.py` derives it from the append-only ledger.

    Tokens rather than dollars, so cost stays computed from config.RATIFIED["price_per_token"] in
    exactly one place. Absent or `active: false` -> the meter behaves exactly as it did before.
    """
    try:
        doc = json.loads(BASELINE.read_text())
    except FileNotFoundError:
        return {}
    if not doc.get("active"):
        return {}
    return {r: {k: int(v) for k, v in d["tokens"].items()} for r, d in doc["per_replicate"].items()}


def session_dir(rep: str) -> Path:
    """Transcripts are keyed on the session's LOCAL cwd, exactly as poll.sh derives it."""
    cwd = Path(__file__).resolve().parent / "sessions" / rep
    return Path.home() / ".claude" / "projects" / str(cwd).replace("/", "-")


def tally(rep: str, baseline: dict | None = None) -> dict:
    d = session_dir(rep)
    tok = {f: 0 for f in FIELDS}
    for f in sorted(glob.glob(str(d / "*.jsonl"))):
        for line in open(f, errors="replace"):
            try:
                rec = json.loads(line)
            except Exception:
                continue
            u = (rec.get("message") or {}).get("usage") or rec.get("usage")
            if isinstance(u, dict):
                for k in FIELDS:
                    tok[k] += u.get(k) or 0
    rates = C.RATIFIED["price_per_token"]
    local_usd = sum(tok[k] * rates[RATE_KEY[k]] for k in FIELDS)

    carried = (baseline or {}).get(rep)
    if carried:
        # Refuse rather than double-count. If the transcripts were carried across with the repo,
        # the local tally ALREADY contains the baseline, and adding it again would charge every
        # replicate twice -- which is the same class of silent-wrong as the gap this closes, only
        # in the safe direction. Cheap to detect: local cannot cover the baseline in every class
        # unless those very transcripts are present.
        if all(tok[k] >= carried[k] for k in FIELDS) and any(carried[k] for k in FIELDS):
            sys.exit(f"meter_spend: {rep}'s local transcripts already cover the carried baseline "
                     f"({BASELINE}). The transcripts appear to have moved with the repo, so adding "
                     f"the baseline would double-count. Set \"active\": false in that file, or "
                     f"remove the carried transcripts. Refusing to meter.")
        for k in FIELDS:
            tok[k] += carried[k]
    cost = {k: tok[k] * rates[RATE_KEY[k]] for k in FIELDS}
    total = sum(cost.values())
    # The token meter's basis, for the side-by-side that makes the gap visible.
    billable = sum(tok[k] for k in FIELDS if k != "cache_read_input_tokens")
    return {"replicate": rep, "tokens": tok, "cost_usd": cost,
            "total_usd": round(total, 4), "billable_tokens": billable,
            "local_usd": round(local_usd, 4),
            "carried_usd": round(total - local_usd, 4) if carried else 0.0,
            "cache_read_share": round(cost["cache_read_input_tokens"] / total, 4) if total else 0.0,
            "usd_per_m_billable": round(total / (billable / 1e6), 2) if billable else 0.0}


def assess(rec: dict, phase: str = "main") -> dict:
    cap = C.RATIFIED["spend_usd"].get(phase)
    if not cap:
        return {**rec, "cap_usd": None, "fraction": None, "level": "n/a"}
    frac = rec["total_usd"] / cap
    level = "stop" if frac >= 1.0 else "warn" if frac >= 0.75 else "ok"
    return {**rec, "cap_usd": cap, "fraction": round(frac, 4), "level": level}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicate", action="append", default=[])
    ap.add_argument("--all", action="store_true", help="every id in the ratified main phase")
    ap.add_argument("--phase", default="main")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    reps = a.replicate or (C.RATIFIED["phases"][a.phase]["ids"] if a.all else [])
    if not reps:
        ap.error("pass --replicate REP (repeatable) or --all")

    out, ledger = [], Path(os.environ.get("HARNESS_STATE_DIR", Path(__file__).parent)) / "spend.jsonl"
    ts = datetime.now(timezone.utc).isoformat()
    baseline = load_baseline()
    for rep in reps:
        # A replicate with carried spend is metered even before its new host has written a single
        # transcript: skipping it would report a fleet total that silently omits what it has
        # already spent, which is the gap this exists to close.
        if not session_dir(rep).is_dir() and rep not in baseline:
            continue
        rec = assess(tally(rep, baseline), a.phase)
        rec["ts"] = ts
        out.append(rec)
        with open(ledger, "a") as fh:
            fh.write(json.dumps(rec) + "\n")

    if a.json:
        print(json.dumps(out, indent=2)); return
    for r in out:
        cap = f"/ ${r['cap_usd']:.2f}" if r["cap_usd"] else ""
        frac = f"{100*r['fraction']:.1f}%" if r["fraction"] is not None else "--"
        print(f"[spend] {r['replicate']}: ${r['total_usd']:>8.2f} {cap}  {frac:>7}  {r['level'].upper()}")
        if r.get("carried_usd"):
            print(f"         ${r['local_usd']:.2f} on this host + ${r['carried_usd']:.2f} carried "
                  f"forward from the previous host ({BASELINE.name})")
        print(f"         cache reads are {100*r['cache_read_share']:.1f}% of that; "
              f"${r['usd_per_m_billable']:.2f} per M billable "
              f"({r['billable_tokens']:,} billable vs {r['tokens']['cache_read_input_tokens']:,} cache-read)")


if __name__ == "__main__":
    main()
