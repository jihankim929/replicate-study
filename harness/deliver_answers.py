#!/usr/bin/env python3
"""Deliver a directory of per-replicate escalation answers and close the rows they answer.

    ./harness/deliver_answers.py harness/escalation_answers/2026-08-31 [--dry-run]

ONE FILE PER REPLICATE, NAMED FOR IT: `<rep>.md` goes to `<rep>` and to nobody else. That is the
whole point rather than a convenience. `deliver_escalation_answers.py` -- the resume batch this
generalises -- had to reason case by case about which notice could go fleet-wide, because a
notice that quotes Appendix A reaching a workspace whose charter omits Appendix A is the SI-016
leak shape and is not recoverable. A per-replicate directory cannot make that mistake by
accident: there is no fleet-uniform path in this file at all. A notice that really is uniform is
sixteen identical files, written deliberately.

Every file is checked against config.LEAK_DENY_* before anything is sent, and a HARD hit aborts
the whole run rather than that one file -- the same abort-as-a-whole rule the resume uses.

ROWS ARE CLOSED ONLY WHERE THE NOTICE SAYS IT CLOSES THEM. Each file declares the rows it
answers in a header comment:

    <!-- closes: 2026-08-30T12:30:56.123456+09:00 -->

matched for EXACT equality against the row's `ts`. A file with no such header delivers and closes
NOTHING, and says so. Exact, not a prefix: replicates file escalations in one pass, so two rows
from the same replicate routinely share a timestamp to the second and differ only in
microseconds -- rep01 has two at 12:30:43 and rep10 two at 12:31:02. A second-resolution match
closed the wrong one of each pair on this script's first two runs. The first version of this script closed every open row belonging to any
replicate it delivered to, which on its first run marked rep07's report of unscheduled processes
on the login node as answered by a notice about the spend meter -- a different subject entirely.
An escalation recorded as answered is one nobody will read again, so the failure is silent and
permanent. Closing is now something a notice has to claim, per row.

The queue carries answer fields by design, so it is updated in place with a timestamped backup
alongside; the append-only ledgers elsewhere are untouched.
"""
import json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
QUEUE = Path("harness/escalation_queue.jsonl")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    d = Path(args[0])
    files = sorted(d.glob("rep*.md"))
    if not files:
        sys.exit(f"no <rep>.md files in {d}")

    # --- leak check, before a single byte is sent ------------------------------------------
    hard = []
    for f in files:
        low = f.read_text().lower()
        for t in C.LEAK_DENY_HARD:
            if t in low:
                hard.append(f"{f.name}: {t!r}")
        for t in C.LEAK_DENY_WARN:
            if t in low:
                print(f"  warn: {f.name} contains {t!r}")
    if hard:
        print("  ABORTING -- nothing sent. Hard leak terms:")
        for h in hard:
            print("   ", h)
        sys.exit(1)
    print(f"  leak check clean over {len(files)} file(s)")

    delivered, closes = [], {}
    for f in files:
        rep = f.stem
        raw = f.read_text()
        m = re.search(r"<!--\s*closes:\s*([^>]*?)\s*-->", raw)
        closes[rep] = [t.strip() for t in m.group(1).split(",") if t.strip()] if m else []
        if not closes[rep]:
            print(f"  note: {f.name} declares no rows to close -- it will deliver only")
        body = re.sub(r"<!--\s*closes:[^>]*-->\n?", "", raw).replace("{STAMP}", STAMP)
        if dry:
            print(f"  (dry-run) would append {len(body)} bytes to {rep}/INBOX.md")
            delivered.append(rep); continue
        p = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", "dirac-bei",
                            f"cat >> /home1/users/Bei/ws/{rep}/INBOX.md"],
                           input=body, text=True, capture_output=True)
        if p.returncode:
            print(f"  !! {rep}: FAILED {p.stderr[:200]}")
        else:
            print(f"  {rep}: delivered")
            delivered.append(rep)

    if dry:
        print("  (dry-run) escalation rows not modified"); return

    shutil.copy2(QUEUE, str(QUEUE) + f".pre-answer.{STAMP.replace(':', '')}")
    out, closed = [], 0
    for line in QUEUE.read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            out.append(line); continue
        rep = row.get("replicate")
        ts = str(row.get("ts") or "")
        if (rep in delivered and not row.get("answered_at")
                and ts in closes.get(rep, [])):
            row["answered_at"] = STAMP
            row["disposition"] = "answered"
            row["reply"] = f"answered per-replicate; see INBOX.md and {d}/{rep}.md"
            closed += 1
        out.append(json.dumps(row))
    QUEUE.write_text("\n".join(out) + "\n")
    print(f"\n  delivered {len(delivered)}/{len(files)}; escalation rows closed: {closed}")


if __name__ == "__main__":
    main()
