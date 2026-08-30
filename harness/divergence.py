#!/usr/bin/env python3
"""Mechanical divergence panel — renders the quantities-only A/B block into STATUS.md.

Run every watchdog cycle (poll.sh calls it last, after metering has refreshed).

What this is for: watching the two replicates diverge *mechanically*, without watching their
science. Every row is a count, a duration or a rate. No structure names, no arm identity, no
trajectory content ever enters the panel — and the arms are relabelled A/B under a mapping
drawn once and sealed.

Three separate guards keep it that way:
  1. the collector runs ON the cluster and returns only numbers, so structure names never
     cross the wire and cannot leak from a renderer bug;
  2. the A/B mapping lives in a sealed file, and only its hash is published;
  3. the rendered block is scanned for structure identifiers, replicate ids and arm words
     before it is written, and the write is refused if any appear.

The blind is procedural, not cryptographic — see the panel's own footnote.
"""
import argparse, glob, hashlib, json, os, re, secrets, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import liveness            # SI-006: agent liveness belongs in the panel, not only in the watchdog

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
REPS = ("s01", "s02")
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", "dirac-bei"]
RAW = HERE / ".divergence_raw"
MAP = HERE / "divergence_map.SEALED.json"
STATUS = REPO / "STATUS.md"
BEGIN = "<!-- DIVERGENCE-PANEL:BEGIN -->"
END = "<!-- DIVERGENCE-PANEL:END -->"
KST = timezone(timedelta(hours=9))

# ---------------------------------------------------------------- leak guard
STEM_RE = re.compile(r"\d{4}\[[A-Za-z]+\]\[[A-Za-z0-9]+\]\d+\[[A-Z]+\]\d+")
FORBIDDEN = [(re.compile(r"\bs0[12]\b"), "replicate id"),
             (re.compile(r"(?i)\b(?:un)?gated\b"), "arm identity"),
             (re.compile(r"(?i)\bappendix a\b"), "arm identity"),
             (STEM_RE, "structure identifier")]


def leak_check(block: str):
    """Refuse to write a panel that names a structure, a replicate or an arm.

    A deny-list is blind to disclosures built from ordinary words, which is exactly how the
    leaks found in this study so far were built. It is not the whole defence -- the collector
    returning numbers only is -- but it catches the class of mistake a renderer can make.
    """
    hits = []
    for rx, what in FORBIDDEN:
        for m in rx.finditer(block):
            hits.append("%s: %r" % (what, m.group(0)))
    return hits


# ---------------------------------------------------------------- sealed map
def sealed_map():
    """Draw the A/B mapping once, then never again. Publish the hash, not the mapping."""
    if MAP.exists():
        d = json.loads(MAP.read_text())
    else:
        order = list(REPS)
        if secrets.randbelow(2):                 # OS randomness: no seed exists to reveal it
            order.reverse()
        d = {"_WARNING": "SEALED. Do not open until collection. Opening this file unblinds "
                         "the mechanical divergence panel in STATUS.md.",
             "drawn_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "A": order[0], "B": order[1]}
        MAP.write_text(json.dumps(d, indent=2) + "\n")
    payload = json.dumps({"A": d["A"], "B": d["B"]}, sort_keys=True).encode()
    return d, hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------- collection
def collect(rep: str, attempts: int = 3) -> dict:
    """Ship the collector to the cluster and read back its JSON.

    Retried: this login node drops and times out connections often enough that a single
    failed attempt is not evidence of anything. A panel that blanked itself every time ssh
    hiccuped would be worse than no panel.
    """
    src = (HERE / "divergence_collect.py").read_bytes()
    err = None
    for i in range(attempts):
        try:
            r = subprocess.run(SSH + ["python3 - " + rep + " --write-usage"], input=src,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, timeout=300)
            line = r.stdout.decode("utf-8", "replace").strip().splitlines()
            if line:
                d = json.loads(line[-1])
                d["collected_epoch"] = datetime.now(timezone.utc).timestamp()
                return d
            err = (r.stderr.decode("utf-8", "replace").strip().splitlines() or ["no output"])[-1][:200]
        except Exception as e:
            err = type(e).__name__
    return {"replicate": rep, "reachable": False, "error": err}


def last_good(rep: str) -> dict:
    """The most recent snapshot that actually collected. Never overwritten by a failure."""
    p = RAW / ("last_%s.json" % rep)
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text())
        return d if d.get("reachable") else {}
    except Exception:
        return {}


def tokens_for(rep: str) -> int:
    """Billable tokens, read from the same instrument the token budget was derived from."""
    sys.path.insert(0, str(HERE))
    try:
        from meter_tokens import count
    except Exception:
        return 0
    cwd = HERE / "sessions" / rep
    sd = Path(os.path.expanduser("~/.claude/projects/" + str(cwd).replace("/", "-")))
    if not sd.exists():
        return 0
    try:
        return count(sd)["billable"]
    except Exception:
        return 0


def ledger_resubs(rep: str, live_jobs) -> int:
    """Cross-poll resubmission count: one PBS name seen under more than one job id.

    PBS drops finished jobs from qstat and this account cannot read the accounting log, so a
    resubmission is only visible if the harness remembers what it saw. This ledger starts at
    the first poll that runs it -- resubmissions before that are not recoverable, and the
    panel says so rather than reporting them as zero.
    """
    RAW.mkdir(exist_ok=True)
    p = RAW / ("jobs_seen_%s.json" % rep)
    seen = json.loads(p.read_text()) if p.exists() else {}
    for name, jid in live_jobs:
        seen.setdefault(name, [])
        if jid not in seen[name]:
            seen[name].append(jid)
    p.write_text(json.dumps(seen))
    return sum(max(0, len(v) - 1) for v in seen.values())


# ---------------------------------------------------------------- rendering
def fmt_ts(epoch):
    if not epoch:
        return "—"
    u = datetime.fromtimestamp(epoch, timezone.utc)
    return u.strftime("%Y-%m-%d %H:%M") + "Z"


def fmt_elapsed(epoch, now):
    if not epoch:
        return "—"
    return "%.1f h" % ((now - epoch) / 3600.0)


def hist_str(h):
    if not h:
        return "—"
    def key(k):
        return (1, 0) if k == "unresolved" else (0, int(k))
    return ", ".join("%s×%d" % (k, h[k]) for k in sorted(h, key=key))


def median_max(h):
    vals = []
    for k, n in h.items():
        if k == "unresolved":
            continue
        vals.extend([int(k)] * n)
    if not vals:
        return "—"
    vals.sort()
    med = vals[len(vals) // 2] if len(vals) % 2 else (vals[len(vals)//2 - 1] + vals[len(vals)//2]) / 2
    return "%g / %d" % (med, vals[-1])


FROZEN_MIN = 90          # ~3 watchdog cycles; longer than any single turn observed


def fmt_age(mins):
    return "%.0f min" % mins if mins < 120 else "%.1f h" % (mins / 60.0)


def frozen_warning(cols):
    """A banner when an arm's agent has stopped writing, printed with the numbers it invalidates.

    SI-006: one replicate sat at a blocking "monthly spend limit" dialog for 38.6 hours while
    this panel reported it as an arm with fewer jobs and a lower token burn. Every cross-arm
    comparison was contaminated and the panel said nothing, because nothing in it measured the
    agent -- only the cluster. A caveat that has to be remembered is not a caveat.
    """
    bad = [(lab, d.get("transcript_age_min")) for lab, d in cols
           if isinstance(d.get("transcript_age_min"), (int, float))
           and d["transcript_age_min"] >= FROZEN_MIN]
    if not bad:
        return None
    who = "; ".join("**%s** (%s)" % (lab, fmt_age(m)) for lab, m in bad)
    return ("> **⚠ CROSS-ARM COMPARISON IS NOT VALID THIS CYCLE.** The agent's own transcript"
            " has not grown for: " + who + ". An arm whose agent has stopped acting still"
            " carries its finished jobs, its CPU-hours and its structure counts forward, so"
            " every row above reads as a working arm that merely did less. It did not do less;"
            " it stopped. Do not read any row as a difference between arms until this clears."
            " See SI-006 in `SI_LEDGER.md`.\n")


def render(cols, maphash, now):
    """cols = [(label, data-dict), ...] already in A/B order."""
    stale = []
    for lab, d in cols:
        if d.get("reachable") and d.get("stale"):
            stale.append("%s (%.0f min old)" % (lab, (now - d.get("collected_epoch", now)) / 60))
    def row(label, fn):
        cells = []
        for _, d in cols:
            try:
                cells.append("—" if not d.get("reachable") else fn(d))
            except Exception:
                cells.append("—")
        return "| %s | %s |" % (label, " | ".join(cells))

    def ratio(d):
        cpu = d.get("cpu_h_disk") or 0
        return "%s" % (format(round(d["tokens"] / cpu), ",") if cpu else "—")

    lines = [
        BEGIN,
        "## Mechanical divergence panel",
        "",
        "Refreshed %s (%s KST) — every watchdog cycle."
        % (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
           datetime.now(KST).strftime("%H:%M")),
        "",
        ("> **Not collected this cycle** — the cluster did not answer. Figures carried"
         " forward from the last successful collection: " + "; ".join(stale) + ".\n")
        if stale else None,
        "Arms are relabelled **A** / **B** in randomized order. The mapping was drawn once from",
        "OS randomness and sealed in `harness/divergence_map.SEALED.json`",
        "(sha256 `%s`). It is not to be opened until collection." % maphash[:32],
        "",
        "| Quantity | A | B |",
        "|---|---:|---:|",
        row("First submission (UTC)", lambda d: fmt_ts(d["first_submission_epoch"])),
        row("Elapsed since first submission", lambda d: fmt_elapsed(d["first_submission_epoch"], now)),
        row("Jobs submitted", lambda d: format(d["jobs_submitted"], ",")),
        row("Jobs completed", lambda d: format(d["jobs_completed"], ",")),
        row("Jobs running", lambda d: format(d["jobs_running"], ",")),
        row("Jobs queued", lambda d: format(d["jobs_queued"], ",")),
        row("Distinct structures touched", lambda d: format(d["structures_with_output"], ",")),
        row("— collapsed over charge-variant twins", lambda d: format(d["structures_collapsed"], ",")),
        row("Tasks across all jobs", lambda d: format(d["batch_tasks_total"], ",")),
        row("Batch size — median / max", lambda d: median_max(d["batch_hist"])),
        row("Batch-size distribution (size×jobs)", lambda d: hist_str(d["batch_hist"])),
        row("Cumulative CPU-h — from run records", lambda d: "%.1f" % d["cpu_h_disk"]),
        row("Cumulative CPU-h — from scheduler", lambda d: "%.1f" % d["cpu_h_scheduler"]),
        row("Token burn (billable)", lambda d: format(d["tokens"], ",")),
        row("Token:CPU (tokens per CPU-h)", ratio),
        row("Resubmissions", lambda d: format(d["resubmissions"], ",")),
        "| Agent transcript last grew | %s | %s |" % tuple(
            "—" if d.get("transcript_age_min") is None else fmt_age(d["transcript_age_min"])
            for _, d in cols),
        "",
        frozen_warning(cols),
        "**Definitions.** *Jobs submitted* = job scripts carrying a `#PBS -N` line; *completed*"
        " = submitted − running − queued. *Distinct structures touched* = benchmark structures"
        " whose run directory holds simulation output; the collapsed row merges the"
        " coordinate-identical charge-variant pairs. *Batch size* = simulation tasks carried by"
        " one submitted job. *Resubmissions* = one job name submitted under more than one job id.",
        "",
        "**Blind spots, stated rather than implied.** The scheduler drops a finished job from"
        " `qstat` and this account cannot read the PBS accounting log, so the scheduler CPU"
        " figure accounts only for jobs alive at a poll plus those the harvester caught"
        " leaving; the run-records figure is the more complete of the two and is single-core"
        " elapsed time per finished run. The resubmission ledger starts at its first poll —"
        " resubmissions earlier than that are not recoverable and are not counted. A job"
        " script written but never submitted would count as submitted, and therefore as"
        " completed.",
        "",
        "**The blind is procedural, not cryptographic.** Per-replicate ledgers elsewhere in"
        " this repo carry some of the same quantities under their real ids, so the mapping is"
        " recoverable by anyone who goes looking. It holds because it is not looked at.",
        END,
    ]
    return "\n".join(l for l in lines if l is not None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the panel, do not write")
    a = ap.parse_args()

    # The panel's subject is the two SMOKE arms. Once they are archived it has none, and a
    # refresh would rewrite a retired section with figures carried forward from a fleet that no
    # longer exists -- the dashboard-on-a-corpse failure the retirement notice describes. Stand
    # down instead. This does NOT unseal or touch divergence_map.SEALED.json.
    if (REPO / "harness/state/SMOKE_ARCHIVED.json").exists():
        print("[divergence] smoke arms ARCHIVED -- panel retired, not refreshed "
              "(harness/state/SMOKE_ARCHIVED.json)")
        return

    RAW.mkdir(exist_ok=True)
    m, maphash = sealed_map()
    now = datetime.now(timezone.utc).timestamp()

    data, failed = {}, []
    for rep in REPS:
        d = collect(rep)
        if d.get("reachable"):
            d["tokens"] = tokens_for(rep)
            d["resubmissions"] = max(d.get("resubmissions_scripts", 0),
                                     ledger_resubs(rep, d.get("live_jobs") or []))
            d.pop("live_jobs", None)
            (RAW / ("last_%s.json" % rep)).write_text(json.dumps(d, indent=2))
        else:
            failed.append("%s (%s)" % (rep, d.get("error")))
            prev = last_good(rep)
            if prev:
                prev["stale"] = True
                d = prev
        # SI-006: every cluster row above can be carried forward or go stale; this one cannot,
        # because it is read from the agent's own transcript on THIS machine. It is attached
        # outside the reachable branch deliberately -- when the cluster stops answering, agent
        # liveness is exactly the reading that is still trustworthy, and the cycle where the
        # panel knows least about the jobs is the cycle where it must still say who is working.
        try:
            d["transcript_age_min"] = liveness.check(rep, update=False)["age_min"]
        except Exception:
            d["transcript_age_min"] = None
        data[rep] = d

    block = render([("A", data[m["A"]]), ("B", data[m["B"]])], maphash, now)

    hits = leak_check(block)
    if hits:
        print("[divergence] REFUSING TO WRITE — leak check failed:", file=sys.stderr)
        for h in hits:
            print("    " + h, file=sys.stderr)
        return 2

    if a.dry_run:
        print(block)
        return 0

    if STATUS.exists():
        txt = STATUS.read_text()
    else:
        txt = ("# STATUS — live view of the running smoke campaign\n\n"
               "*Machine-generated. Refreshed by `harness/poll.sh` each watchdog cycle.*\n\n"
               + BEGIN + "\n" + END + "\n")
    if BEGIN in txt and END in txt:
        pre, rest = txt.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        txt = pre + block + post
    else:
        txt = txt.rstrip() + "\n\n" + block + "\n"
    STATUS.write_text(txt)
    print("[divergence] STATUS.md panel refreshed"
          + ("  -- not collected this cycle: " + ", ".join(failed) if failed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
