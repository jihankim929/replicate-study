#!/usr/bin/env python3
"""Context-composition analysis: what kind of tool output entered a replicate's session, and what
that output cost for the rest of the campaign.

The premise, from the PI's cost-mechanics ruling: context is re-read every turn, so a byte that
enters at turn t is billed at cache-read rates on every turn after t. A one-time 200 KB dump early
in a long session is not a one-time cost -- it is 200 KB times the remaining turn count.

ATTRIBUTION MODEL. A first version multiplied bytes by an assumed bytes-per-token and by a
position-derived turn count; it came out ~5x under the measured bill, because tool results are only
part of what is re-read and the token estimate was a guess. This version does not estimate the
total at all -- it MEASURES it and apportions it.

  measured_cache_read_spend = sum(cache_read_input_tokens over every turn) * cache_read_rate
  weight(result)            = bytes * (number of turns that follow it)
  attributed(result)        = measured_cache_read_spend * weight / sum(weights)

So the per-class column sums exactly to the campaign's real cache-read spend, and the only modelled
quantity is the SHARE, not the total. What it still assumes: that re-read cost is proportional to
bytes carried forward, which ignores cache block granularity and any compaction. Non-cache-read
spend (fresh input, output, cache writes) is reported separately and never attributed here.
"""
import json, glob, os, re, sys, datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as C

BYTES_PER_TOKEN = 4.0
RATE = C.RATIFIED["price_per_token"]["cache_read"]
GAP_MIN = 30          # a gap longer than this is not working time


def classify(cmd, out):
    c = (cmd or "").lower()
    if re.search(r"\bqstat\b|\bqas\b|\bpbsnodes\b|\bqselect\b", c):
        return "scheduler polls"
    if re.search(r"\b(cat|head|tail|less|more)\b.*(output|\.data\b|\.out\b|movie|restart)", c):
        return "raw simulation-output reads"
    if re.search(r"\b(ls|find|du|tree)\b", c) and not re.search(r"\bwc -l\b", c):
        return "directory listings"
    if re.search(r">\s*\S|\btee\b|\bcp\b|\bmv\b|\bmkdir\b|<<\s*'?\w+", c):
        return "file writes"
    return "other"


def analyse(rep, path_glob):
    files = sorted(glob.glob(path_glob))
    if not files:
        return None
    turns, results = [], []
    for f in files:
        for line in open(f, errors="ignore"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            ts = r.get("timestamp")
            t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None
            if t:
                turns.append(t)
            # tool RESULTS are what enter context
            msg = r.get("message") or {}
            content = msg.get("content")
            if isinstance(content, list):
                for blk in content:
                    if isinstance(blk, dict) and blk.get("type") == "tool_result":
                        body = blk.get("content")
                        if isinstance(body, list):
                            body = "".join(x.get("text", "") for x in body if isinstance(x, dict))
                        results.append({"t": t, "bytes": len(body or ""), "id": blk.get("tool_use_id")})
            # the matching tool_use carries the command
            if isinstance(content, list):
                for blk in content:
                    if isinstance(blk, dict) and blk.get("type") == "tool_use":
                        inp = blk.get("input") or {}
                        cmd = inp.get("command") or inp.get("file_path") or json.dumps(inp)[:400]
                        results.append({"cmd": cmd, "id": blk.get("id"), "bytes": 0, "t": t})
    # pair tool_use -> tool_result by id
    cmds = {r["id"]: r.get("cmd") for r in results if r.get("cmd")}
    real = [r for r in results if r["bytes"] > 0 or (r.get("cmd") is None and r["bytes"] == 0)]
    real = [r for r in results if not r.get("cmd")]
    turns = sorted(t for t in turns if t)
    if not turns:
        return None
    # active hours: elapsed span minus gaps longer than GAP_MIN
    span = (turns[-1] - turns[0]).total_seconds()
    dead = sum((turns[i+1]-turns[i]).total_seconds()
               for i in range(len(turns)-1)
               if (turns[i+1]-turns[i]).total_seconds() > GAP_MIN*60)
    active_h = max((span - dead) / 3600.0, 1e-6)

    n_turns = len(turns)
    ordered = sorted([r for r in real if r["t"]], key=lambda r: r["t"])
    # exact turns-after: count turn timestamps strictly later than this result
    import bisect
    weights = []
    for r in ordered:
        after = n_turns - bisect.bisect_right(turns, r["t"])
        weights.append(r["bytes"] * max(after, 0))
    total_w = sum(weights) or 1
    by = defaultdict(lambda: {"n": 0, "bytes": 0, "w": 0})
    for r, w in zip(ordered, weights):
        cls = classify(cmds.get(r["id"], ""), None)
        g = by[cls]; g["n"] += 1; g["bytes"] += r["bytes"]; g["w"] += w
    return {"rep": rep, "turns": n_turns, "active_h": active_h,
            "span_h": span/3600.0, "dead_h": dead/3600.0, "by": dict(by),
            "total_w": total_w, "n_results": len(ordered)}


def cache_read_spend(rep):
    """Measured cache-read spend and the rest of the bill, from the transcript's own usage rows."""
    base = os.path.expanduser("~/.claude/projects")
    g = f"{base}/-Users-jihankim-replicate-study-harness-sessions-{rep}/*.jsonl"
    cr = other = 0.0
    R = C.RATIFIED["price_per_token"]
    for f in glob.glob(g):
        for line in open(f, errors="ignore"):
            try: r = json.loads(line)
            except Exception: continue
            u = (r.get("message") or {}).get("usage") or r.get("usage")
            if not u: continue
            cr += u.get("cache_read_input_tokens", 0) * R["cache_read"]
            other += (u.get("input_tokens", 0) * R["input"]
                      + u.get("output_tokens", 0) * R["output"]
                      + u.get("cache_creation_input_tokens", 0) * R["cache_creation"])
    return cr, other


def render(a, measured=None, cr=0.0, rest=0.0):
    out = [f"\n### {a['rep']}  —  {a['n_results']} tool results, "
           f"{a['active_h']:.1f} active h (span {a['span_h']:.1f} h, "
           f"{a['dead_h']:.1f} h idle >30 min)"]
    out.append("")
    out.append("| class | calls | calls/active h | bytes into context | share of re-read | attributed |")
    out.append("|---|---:|---:|---:|---:|---:|")
    tot_n = tot_b = 0; tot_c = 0.0
    for cls, g in sorted(a["by"].items(), key=lambda kv: -kv[1]["w"]):
        share = g["w"] / a["total_w"]
        cost = cr * share
        out.append(f"| {cls} | {g['n']:,} | {g['n']/a['active_h']:.1f} | "
                   f"{g['bytes']:,} | {share:6.1%} | ${cost:,.2f} |")
        tot_n += g["n"]; tot_b += g["bytes"]; tot_c += cost
    out.append(f"| **total** | **{tot_n:,}** | **{tot_n/a['active_h']:.1f}** | "
               f"**{tot_b:,}** | **100.0%** | **${tot_c:,.2f}** |")
    out.append(f"\nCache-read spend **${cr:,.2f}** ({cr/(cr+rest):.0%} of the bill); "
               f"everything else (fresh input, output, cache writes) **${rest:,.2f}**. "
               f"Lifetime total **${measured:,.2f}**.")
    return "\n".join(out)


if __name__ == "__main__":
    base = os.path.expanduser("~/.claude/projects")
    reps = [("s01", f"{base}/-Users-jihankim-replicate-study-harness-sessions-s01/*.jsonl"),
            ("s02", f"{base}/-Users-jihankim-replicate-study-harness-sessions-s02/*.jsonl"),
            ("rep01", f"{base}/-Users-jihankim-replicate-study-harness-sessions-rep01/*.jsonl")]
    import meter_spend
    for rep, g in reps:
        a = analyse(rep, g)
        if not a:
            print(f"\n### {rep} — no transcript found"); continue
        try:
            m = meter_spend.tally(rep)["total_usd"]
        except Exception:
            m = None
        cr, rest = cache_read_spend(rep)
        print(render(a, m if m is not None else cr + rest, cr, rest))
