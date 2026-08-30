#!/usr/bin/env python3
"""Registry purge: take the smoke arms out of every LIVE surface (PI ruling, 2026-08-30).

s01/s02 are ARCHIVED, not down. The distinction is the whole point of this script. A "down"
replicate is a live member of the fleet that is failing, and every live surface -- the roster,
the watchdog, the spend denominator, the divergence panel -- is right to keep counting it and
right to keep flagging it. An ARCHIVED replicate is not a fleet member at all: its campaign is
over, its material is off-cluster, and a surface that keeps counting it reports a fleet that
does not exist. Before this purge the panel carried two dead arms as the study's headline
comparison, the roster had the watchdog restarting them, and the spend denominator was 18 x $280
against a fleet of 16.

WHAT IS NOT TOUCHED, DELIBERATELY:
  * prereg/ and config.py's phase rosters. The smoke HAPPENED and was pre-registered; the
    pre-registration is a historical record, not a live surface, and editing it to match today
    would be falsifying the record rather than purging a roster.
  * harness/restarts.jsonl and the smoke's own spend rows. Append-only ledgers keep their
    history; the fleet TOTAL is recomputed to exclude them, which is a different thing from
    deleting them.
  * archive/ and reps/smoke/. That is where the material correctly lives.
"""
import json, re, shutil, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
SMOKE = ["s01", "s02"]
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
REPO = Path(".")
CAP = 280.0
report = []


def backup(p):
    b = Path(str(p) + f".pre-purge.{NOW.strftime('%Y%m%dT%H%M%SZ')}")
    if Path(p).exists():
        shutil.copy2(p, b)
    return b


# --- 1. roster ---------------------------------------------------------------------------
p = REPO / "harness/state/active_replicates"
backup(p)
rows = [l.strip() for l in open(p) if l.strip()]
kept = [r for r in rows if r not in SMOKE]
open(p, "w").write("\n".join(kept) + "\n")
report.append(f"roster: {len(rows)} -> {len(kept)} (removed {', '.join(r for r in rows if r in SMOKE)})")

# --- 2. archived marker: the guard every live surface can read ----------------------------
marker = REPO / "harness/state/SMOKE_ARCHIVED.json"
json.dump({"event": "SMOKE_ARCHIVED", "ts": STAMP, "replicates": SMOKE,
           "status": "archived, not down",
           "material": "archive/smoke/ and reps/smoke/ (verified copies); workspaces removed from cluster",
           "effect": ["out of harness/state/active_replicates",
                      "excluded from the fleet spend denominator",
                      "A/B divergence panel retired",
                      "smoke-era escalation rows closed as resolved-by-archive"],
           "fleet_after": {"n": 16, "cap_usd_each": CAP, "denominator_usd": 16 * CAP}},
          open(marker, "w"), indent=2)
report.append(f"marker: {marker} written (archived, not down)")

# --- 3. escalation rows: close smoke-era rows as resolved-by-archive ----------------------
q = REPO / "harness/escalation_queue.jsonl"
backup(q)
out, closed = [], 0
for line in open(q):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        out.append(line); continue
    if d.get("replicate") in SMOKE and not d.get("answered_at"):
        d["answered_at"] = STAMP
        d["disposition"] = "closed_resolved_by_archive"
        d["reply"] = ("Closed without a substantive answer. The smoke campaign this escalation "
                      "belongs to has ended and its workspaces are archived; there is no live "
                      "campaign for an answer to affect. Recorded, not repaired.")
        closed += 1
    out.append(json.dumps(d))
open(q, "w").write("\n".join(out) + "\n")
report.append(f"escalations: {closed} smoke-era row(s) closed as resolved-by-archive")

# --- 4. retire the A/B divergence panel ---------------------------------------------------
s = REPO / "STATUS.md"
backup(s)
txt = open(s).read()
BEGIN, END = "<!-- DIVERGENCE-PANEL:BEGIN -->", "<!-- DIVERGENCE-PANEL:END -->"
retire = f"""{BEGIN}
## Mechanical divergence panel — **RETIRED {STAMP}**

The A/B panel compared the two **smoke** arms. Those arms are finished and archived
(`harness/state/SMOKE_ARCHIVED.json`), so the panel had no live subject: it was carrying figures
forward from a last successful collection and correctly refusing its own comparison, which is a
dashboard reporting on a fleet that no longer exists.

It is retired rather than repaired. The main phase is N = 16 and its comparison is not this
panel's two-arm shape; a main-phase divergence view is a separate instrument and is not
pre-registered yet. The sealed arm mapping in `harness/divergence_map.SEALED.json` is
**unopened and stays sealed** — retiring the display does not unseal anything.

Historical panels remain in git history. The smoke's own record is in `reps/smoke/` and
`archive/smoke/`.
{END}"""
if BEGIN in txt and END in txt:
    txt = txt[:txt.index(BEGIN)] + retire + txt[txt.index(END) + len(END):]
    open(s, "w").write(txt)
    report.append("STATUS.md: A/B divergence panel retired in place")
else:
    report.append("STATUS.md: panel markers not found -- NOT modified")

# --- 5. fleet spend, recomputed on the 16 that exist --------------------------------------
latest = {}
for line in open(REPO / "harness/spend.jsonl"):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    latest[d["replicate"]] = d
live = {k: v for k, v in latest.items() if k not in SMOKE}
smoke_tot = sum(v["total_usd"] for k, v in latest.items() if k in SMOKE)
tot = sum(v["total_usd"] for v in live.values())
denom = len(live) * CAP
summary = {
    "ts": STAMP, "basis": "latest metered row per replicate, smoke excluded",
    "n_live": len(live), "cap_usd_each": CAP, "denominator_usd": denom,
    "fleet_spend_usd": round(tot, 2), "fleet_fraction": round(tot / denom, 4),
    "excluded_smoke_usd": round(smoke_tot, 2),
    "superseded": {"denominator_usd": 18 * CAP, "note": "18 x $280 counted two archived arms"},
    "per_replicate": {k: round(v["total_usd"], 2) for k, v in sorted(live.items())},
}
json.dump(summary, open(REPO / "harness/state/fleet_spend.json", "w"), indent=2)
report.append(f"fleet spend: ${tot:,.2f} / ${denom:,.0f} ({tot/denom*100:.1f}%) over {len(live)} replicates; "
              f"${smoke_tot:,.2f} of smoke excluded (was ${18*CAP:,.0f} denominator)")

print(f"=== REGISTRY PURGE {STAMP} ===")
for r in report:
    print("  " + r)
