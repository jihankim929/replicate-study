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
import argparse, glob, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
RATE_KEY = {"input_tokens": "input", "output_tokens": "output",
            "cache_creation_input_tokens": "cache_creation", "cache_read_input_tokens": "cache_read"}


BASELINE = Path(os.environ.get("HARNESS_STATE_DIR", Path(__file__).parent)) / "state" / "spend_baseline.json"


class CarriedTranscriptsPresent(RuntimeError):
    """The carried transcripts are on THIS host, so the baseline is already in the local tally.

    Raised, not `sys.exit`-ed. `main()` turns it into an exit; watchdog.py's `except Exception`
    can then degrade one replicate's spend row to `unknown` instead of taking the whole watchdog
    down with it. `sys.exit` raises SystemExit, which derives from BaseException and is NOT
    caught by that clause -- so the refusal used to be a fleet-wide outage by construction.
    REPORT 006 section 4; ruled 2026-08-31.
    """


def load_baseline_doc() -> dict:
    try:
        return json.loads(BASELINE.read_text())
    except FileNotFoundError:
        return {}


def carried_cutoff() -> datetime | None:
    """The instant the previous host's fleet was CONFIRMED DOWN.

    Any local transcript record older than this was written on the retired host and therefore
    travelled with the repository. That is the only thing that makes the baseline a double-count,
    and it is what the guard in `tally()` now tests. See its comment.
    """
    ts = load_baseline_doc().get("fleet_confirmed_down_utc")
    if not ts:
        return None
    try:
        d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


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
    doc = load_baseline_doc()
    if not doc or not doc.get("active"):
        return {}
    return {r: {k: int(v) for k, v in d["tokens"].items()} for r, d in doc["per_replicate"].items()}


def session_dir(rep: str) -> Path:
    """Transcripts are keyed on the session's LOCAL cwd, exactly as poll.sh derives it."""
    cwd = Path(__file__).resolve().parent / "sessions" / rep
    return Path.home() / ".claude" / "projects" / str(cwd).replace("/", "-")


def tally(rep: str, baseline: dict | None = None, cutoff: "datetime | None" = None) -> dict:
    d = session_dir(rep)
    tok = {f: 0 for f in FIELDS}
    earliest = None                      # oldest record timestamp seen on THIS host
    for f in sorted(glob.glob(str(d / "*.jsonl"))):
        for line in open(f, errors="replace"):
            try:
                rec = json.loads(line)
            except Exception:
                continue
            ts = rec.get("timestamp")
            if isinstance(ts, str):
                try:
                    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    t = None
                if t is not None:
                    if t.tzinfo is None:
                        t = t.replace(tzinfo=timezone.utc)
                    if earliest is None or t < earliest:
                        earliest = t
            u = (rec.get("message") or {}).get("usage") or rec.get("usage")
            if isinstance(u, dict):
                for k in FIELDS:
                    tok[k] += u.get(k) or 0
    rates = C.RATIFIED["price_per_token"]
    local_usd = sum(tok[k] * rates[RATE_KEY[k]] for k in FIELDS)

    carried = (baseline or {}).get(rep)
    if carried:
        # Refuse rather than double-count -- but only on EVIDENCE that the transcripts moved.
        #
        # This guard used to test `local >= baseline in all four token classes`. That is not
        # evidence of anything: it is what time does to any replicate that keeps running, and it
        # became true for rep01 at 21:36 KST on 2026-08-30 simply because rep01 passed the
        # carried cache-read count on its own. Because the refusal was a `sys.exit` and rep01
        # sorts first, the whole fleet's meter died on it and the $280 cap -- the budget the
        # record calls binding -- went unenforced for six hours with the meter firing every two
        # minutes and writing nothing. REPORT 006 section 4; re-guarded on the PI's ruling
        # 2026-08-31.
        #
        # The actual question is "are the previous host's transcripts sitting in this directory?"
        # and it has a direct answer: those transcripts contain records written BEFORE the old
        # fleet was confirmed down. A record older than that instant cannot have been written
        # here. Nothing a running campaign does can make this true, and copying the directory
        # across cannot make it false -- which is exactly the asymmetry the old test lacked.
        if cutoff and earliest and earliest < cutoff:
            raise CarriedTranscriptsPresent(
                f"meter_spend: {rep} has a local transcript record from {earliest.isoformat()}, "
                f"before the previous fleet was confirmed down ({cutoff.isoformat()}), so the "
                f"carried transcripts are present on this host and the baseline in {BASELINE} is "
                f"already inside the local tally. Adding it would double-count. Set "
                f"\"active\": false in that file, or remove the carried transcripts. "
                f"Refusing to meter.")
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


WS_ROOT = "/home1/users/Bei/ws"
SSH_ALIAS = "dirac-bei"


def push_usage(rows: list, timeout: int = 45) -> str:
    """Publish each replicate's spend into its workspace `usage.json`.

    WHY. Charter section 4 tells a replicate to judge its remaining room by spend, and section 4
    calls the spend meter an instrument in its workspace. It was not one: `usage.json` carried
    `cpu_h_scheduler`, `queued_jobs` and `tokens` and no spend figure at all, so the one budget
    the record says actually binds was the one budget an agent could not read. rep07, rep12 and
    rep15 each escalated exactly that, independently. PI ruling 2026-08-31.

    NOTE ON THE KEY NAME. `usage.json` holds what has been USED (`cpu_h_scheduler`, `tokens`) and
    `WORKSPACE.json` holds the CAPS -- where the cap is already called `spend_usd`. The ruled key
    is `spend_usd`, so the same name now means spent-here and cap-there. `spend_cap_usd` and
    `spend_fraction` are written alongside so that no reader has to resolve that collision from
    context; they are additive and cost nothing. Flagged for the PI, trivially reversible.

    ONE ssh for the whole fleet, not one per replicate. The spend meter's 2-minute cadence is
    load-bearing and its wrapper's stated property is "no ssh, no cluster load"; sixteen
    connections every two minutes would be 480 an hour. One is 30, and it carries the same
    payload. The write is atomic (`os.replace`) because poll.sh writes this same file.

    Never raises, never affects exit status, never runs before the ledger. Enforcement is decided
    from local transcripts; this is publication, and an unreachable cluster must not disturb it.
    """
    payload = {r["replicate"]: {"spend_usd": round(r["total_usd"], 2),
                                "spend_cap_usd": r["cap_usd"],
                                "spend_fraction": r["fraction"],
                                "spend_level": r["level"]}
               for r in rows if r.get("cap_usd")}
    if not payload:
        return "[spend-push] nothing to publish"
    script = (
        "import json, os\n"
        "payload = json.loads(" + repr(json.dumps(payload)) + ")\n"
        "ok = 0\n"
        "for rep, vals in payload.items():\n"
        "    p = os.path.join(" + repr(WS_ROOT) + ", rep, 'usage.json')\n"
        "    try:\n"
        "        u = json.load(open(p)) if os.path.exists(p) else {}\n"
        "        u.update(vals)\n"
        "        t = p + '.spend.tmp'\n"
        "        json.dump(u, open(t, 'w'))\n"
        "        os.replace(t, p)\n"
        "        ok += 1\n"
        "    except Exception as e:\n"
        "        print('[spend-push] %s FAILED: %s' % (rep, e))\n"
        "print('[spend-push] %d/%d workspace(s) updated' % (ok, len(payload)))\n")
    try:
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                            SSH_ALIAS, "python3 -"],
                           input=script, text=True, capture_output=True, timeout=timeout)
        out = (r.stdout or "").strip() or (r.stderr or "").strip()
        return out or f"[spend-push] ssh returned {r.returncode} with no output"
    except subprocess.TimeoutExpired:
        return f"[spend-push] ssh timed out after {timeout}s -- spend still metered locally"
    except Exception as exc:                       # unreachable cluster must never break the meter
        return f"[spend-push] not published ({exc.__class__.__name__}: {exc}) -- metering unaffected"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicate", action="append", default=[])
    ap.add_argument("--all", action="store_true", help="every id in the ratified main phase")
    ap.add_argument("--phase", default="main")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-push", action="store_true",
                    help="meter and record, but do not publish spend into the workspaces")
    a = ap.parse_args()

    reps = a.replicate or (C.RATIFIED["phases"][a.phase]["ids"] if a.all else [])
    if not reps:
        ap.error("pass --replicate REP (repeatable) or --all")

    out, ledger = [], Path(os.environ.get("HARNESS_STATE_DIR", Path(__file__).parent)) / "spend.jsonl"
    ts = datetime.now(timezone.utc).isoformat()
    baseline = load_baseline()
    cutoff = carried_cutoff()
    for rep in reps:
        # A replicate with carried spend is metered even before its new host has written a single
        # transcript: skipping it would report a fleet total that silently omits what it has
        # already spent, which is the gap this exists to close.
        if not session_dir(rep).is_dir() and rep not in baseline:
            continue
        try:
            rec = assess(tally(rep, baseline, cutoff), a.phase)
        except CarriedTranscriptsPresent as exc:
            sys.exit(str(exc))
        rec["ts"] = ts
        out.append(rec)
        with open(ledger, "a") as fh:
            fh.write(json.dumps(rec) + "\n")

    if not a.no_push:
        print(push_usage(out))

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
