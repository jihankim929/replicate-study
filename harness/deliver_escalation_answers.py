#!/usr/bin/env python3
"""Deliver the prepared escalation answers and close the rows. Run AT RESUME, not before.

SCOPING, AND WHY IT IS NOT FLEET-UNIFORM FOR ALL OF IT. The ruling asked for a fleet-uniform
notice. That is right for the budget ruling and the infrastructure facts, and it is wrong for
Rev 21, because Rev 21 amends **Appendix A / G3** -- and Appendix A is the treatment. The
ungated arm's charter is the gated charter with Appendix A omitted verbatim; pushing G3 text
into those eight workspaces would hand the ungated arm the very material whose absence defines
it. That is the SI-016 leak shape, and it would not be recoverable.

Measured, not assumed (2026-08-30): all 8 ungated charters contain zero Appendix A; 7 of the 8
gated charters already carry the Rev 21 clause as provisioned text; rep01 is the ONLY replicate
holding a pre-Rev-21 Appendix A, and it is the replicate that filed both escalations. So Rev 21
goes to rep01 and to nobody else -- which is exactly the asymmetry Rev 21 already logged.

  NOTICE_fleet_uniform.md  -> all 16   (budget ruling, qas, MakeGrid, core caps, section 8)
  NOTICE_rep01_rev21.md    -> rep01    (Appendix A / G3 content)
"""
import json, subprocess, sys
from datetime import datetime, timezone

STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
FLEET = ["rep01","rep02","rep03","rep04","rep05","rep06","rep07","rep08",
         "rep09","rep10","rep11","rep12","rep13","rep15","rep16","rep17"]
GATED_REV21_TARGET = ["rep01"]
DRY = "--dry-run" in sys.argv


def deliver(rep, text):
    if DRY:
        print(f"  (dry-run) would append {len(text)} bytes to {rep}/INBOX.md"); return True
    p = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", "dirac-bei",
                        f"cat >> /home1/users/Bei/ws/{rep}/INBOX.md"],
                       input=text, text=True, capture_output=True)
    if p.returncode:
        print(f"  !! {rep}: FAILED {p.stderr[:200]}"); return False
    print(f"  {rep}: delivered"); return True


def main():
    uniform = open("harness/escalation_answers/NOTICE_fleet_uniform.md").read().replace("{STAMP}", STAMP)
    rev21 = open("harness/escalation_answers/NOTICE_rep01_rev21.md").read().replace("{STAMP}", STAMP)

    print(f"=== fleet-uniform notice -> {len(FLEET)} replicates ===")
    ok = [r for r in FLEET if deliver(r, uniform)]
    print(f"\n=== Rev 21 notice -> {GATED_REV21_TARGET} (Appendix A holders lacking it) ===")
    ok21 = [r for r in GATED_REV21_TARGET if deliver(r, rev21)]

    if DRY:
        print("\n(dry-run) escalation rows not modified"); return

    # Close the rows this notice answers. Append-only ledgers elsewhere; this queue carries
    # answer fields by design, so it is updated in place with a backup alongside.
    q = "harness/escalation_queue.jsonl"
    import shutil; shutil.copy2(q, q + f".pre-answer.{STAMP.replace(':','')}")
    ANSWERED = {
        "charter": "answered by fleet notice / Rev 21 text; see INBOX.md",
        "infra":   "answered with infrastructure facts by fleet notice; see INBOX.md",
    }
    out, closed = [], 0
    for line in open(q):
        line = line.strip()
        if not line: continue
        try: d = json.loads(line)
        except Exception: out.append(line); continue
        rep, cat = d.get("replicate"), d.get("category")
        if rep in FLEET and not d.get("answered_at") and cat in ANSWERED:
            d["answered_at"] = STAMP
            d["disposition"] = "answered"
            d["reply"] = ANSWERED[cat]
            closed += 1
        out.append(json.dumps(d))
    open(q, "w").write("\n".join(out) + "\n")
    print(f"\n  escalation rows closed: {closed}")
    print(f"  delivered: uniform={len(ok)}/{len(FLEET)}  rev21={len(ok21)}/{len(GATED_REV21_TARGET)}")


if __name__ == "__main__":
    main()
