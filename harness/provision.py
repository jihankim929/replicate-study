#!/usr/bin/env python3
"""(a) Provisioning — build a replicate workspace from the frozen benchmark.

Enforces:
  charter section 1  -- database provided at <workspace>/db/
  charter section 4  -- "you operate exclusively inside [workspace path]"
  Appendix A header  -- appendix present for the gated arm, "omitted verbatim" for the other
  constitution      -- answer-key/ is sealed; never appears in a replicate workspace

Design notes that matter:
  * Provisioning reads ONLY from config.SOURCE_ALLOWLIST. It never walks the repo root, so
    answer-key/ is structurally unreachable rather than excluded by a rule someone could edit.
  * Files are COPIED, never symlinked -- a symlink would be a path back into this repo.
  * The workspace git repo is created with NO remote, for the same reason.
  * Checksums are verified ON ARRIVAL, against the frozen manifest, after the copy.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

KST = timezone(timedelta(hours=9))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def split_charter(text: str, arm: str) -> str:
    """Gated arm gets the whole charter. Ungated gets everything before Appendix A.

    'omitted verbatim' is taken literally: the appendix is not summarised, not referred to,
    not replaced by a placeholder. The ungated charter simply ends at section 9.
    """
    idx = text.find(C.APPENDIX_MARKER)
    if idx == -1:
        raise RuntimeError(f"appendix marker not found in charter: {C.APPENDIX_MARKER!r}")
    if arm == "gated":
        return text
    body = text[:idx]
    # drop the trailing '---' separators that introduced the appendix
    while body.rstrip().endswith("---"):
        body = body.rstrip()[: -3]
    return body.rstrip() + "\n"


def leak_scan(ws: Path, repo: Path) -> list:
    """Belt-and-braces check that no sealed material or path-back reached the workspace."""
    problems = []
    sealed = repo / "answer-key"
    sealed_hashes = {sha256(p) for p in sealed.rglob("*") if p.is_file()} if sealed.exists() else set()
    for p in ws.rglob("*"):
        if p.is_symlink():
            problems.append(f"symlink present (path back / escape risk): {p.relative_to(ws)}")
            continue
        if not p.is_file() or ".git/" in str(p.relative_to(ws)):
            continue
        if p.suffix in {".cif", ".sha256"}:
            continue                      # database payload: checked by manifest instead
        if sha256(p) in sealed_hashes:
            problems.append(f"SEALED FILE COPIED INTO WORKSPACE: {p.relative_to(ws)}")
        try:
            txt = p.read_text(errors="replace")
        except Exception:
            continue
        if str(repo) in txt:
            problems.append(f"contains a path back to the study repo: {p.relative_to(ws)}")
        low = txt.lower()
        for term in C.LEAK_DENY_HARD:
            if term in low:
                problems.append(f"study-design term {term!r} present in {p.relative_to(ws)}")
    return problems


def leak_warn(ws: Path) -> list:
    """Terms that disclose study design but sit in documents Bei does not own.

    Reported, never auto-edited: the charter is the PI's document. See
    prereg/charter_revisions.md, standing leak-control note, item 2.
    """
    warns = []
    for p in ws.rglob("*"):
        if not p.is_file() or p.suffix in {".cif", ".sha256"} or ".git/" in str(p):
            continue
        try:
            low = p.read_text(errors="replace").lower()
        except Exception:
            continue
        for term in C.LEAK_DENY_WARN:
            if term in low:
                warns.append(f"{p.name}: discloses {term!r}")
    return warns


def provision(rep_id, dest_root, dry_run=False, db_limit=None, force=False):
    arm = C.arm_of(rep_id)
    phase = C.phase_of(rep_id)
    C.require_ratified(["cycles_screen", "cycles_claim", "raspa", "tail_corrections"], dry_run)

    ws = Path(dest_root).resolve() / rep_id
    if ws.exists():
        if not force:
            raise SystemExit(f"refusing to overwrite existing workspace {ws} (use --force)")
        shutil.rmtree(ws)
    print(f"[provision] {rep_id}  arm={arm}  phase={phase}  ->  {ws}")
    if dry_run:
        print("[provision] DRY RUN")

    (ws / "db").mkdir(parents=True)

    # --- 1. charter, arm-appropriate ----------------------------------------------------
    charter = split_charter(C.SOURCE_ALLOWLIST["charter"].read_text(), arm)
    (ws / "CHARTER.md").write_text(charter)
    has_appendix = C.APPENDIX_MARKER in charter
    assert has_appendix == (arm == "gated"), "appendix/arm mismatch"
    shutil.copy2(C.SOURCE_ALLOWLIST["addendum"], ws / "CHARTER_ADDENDUM.md")
    if arm == "gated":
        shutil.copy2(C.SOURCE_ALLOWLIST["audit_schema"], ws / "AUDIT_SCHEMA.md")
        (ws / "AUDIT.jsonl").write_text("")

    # --- 2. database + checksum verification on arrival ---------------------------------
    manifest = {}
    for line in C.SOURCE_ALLOWLIST["manifest"].read_text().splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            manifest[name.strip()] = digest
    names = sorted(manifest)
    if db_limit:
        names = names[:db_limit]
    for n in names:
        shutil.copy2(C.SOURCE_ALLOWLIST["db_dir"] / n, ws / "db" / n)
    (ws / "db" / "MANIFEST.sha256").write_text(
        "".join(f"{manifest[n]}  {n}\n" for n in names))

    bad = [n for n in names if sha256(ws / "db" / n) != manifest[n]]
    if bad:
        raise SystemExit(f"CHECKSUM FAILURE on arrival for {len(bad)} file(s): {bad[:5]}")
    print(f"[provision] db: {len(names)} files copied, {len(names)}/{len(names)} checksums verified")

    # --- 3. workspace record files ------------------------------------------------------
    deadline = (datetime.now(KST) + timedelta(days=C.RATIFIED["phases"][phase]["days"])
                ).replace(hour=9, minute=0, second=0, microsecond=0)
    # WORKSPACE.json is READ BY THE REPLICATE. It carries what a replicate needs to obey the
    # charter and NOTHING about study design -- no arm, no appendix flag, no replicate count.
    # Arm and appendix state live in the provisioning receipt, which is written OUTSIDE the
    # workspace. See prereg/charter_revisions.md, standing leak-control note.
    meta = {
        "replicate_id": rep_id,
        "phase": phase,
        "provisioned_at": datetime.now(KST).isoformat(),
        "deadline_kst": deadline.isoformat(),
        "campaign_days": C.RATIFIED["phases"][phase]["days"],
        "db_files": len(names),
        "budget_status": "ratified 2026-08-26",
        "compute_cpu_h": C.RATIFIED["compute_cpu_h"][phase],
        "token_budget": C.RATIFIED["token_budget"][phase],
        "token_metering_basis": C.RATIFIED["token_metering_basis"],
        "max_queued_jobs": C.RATIFIED["max_queued_jobs"][phase],
        "queue": C.RATIFIED["queue"],
        "job_tag_prefix": f"{rep_id}_",
    }
    (ws / "WORKSPACE.json").write_text(json.dumps(meta, indent=2) + "\n")
    (ws / "LOG.md").write_text("# LOG — append-only narrative\n\n")
    (ws / "STATE.md").write_text("# STATE — current tasks and beliefs\n\n")
    (ws / "JOBS.md").write_text(
        "# Cluster Job Ledger (append-only)\n\n"
        "| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |\n"
        "|---|---|---|---|---|---|---|\n")
    (ws / "ESCALATIONS.md").write_text(
        "# Escalations\n\n"
        "One per line. Format (charter section 8), with the two words replaced:\n\n"
        "    [ESC:\u200b category / one-line question]\n\n"
        "Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.\n"
        "The example above contains a zero-width space so the router does not read it as a\n"
        "filed escalation; type yours fresh rather than copying it.\n\n")
    (ws / "INBOX.md").write_text("# Inbox — harness notices and escalation responses\n\n")

    # --- 4. git, deliberately with no remote --------------------------------------------
    if not dry_run or True:   # the mock workspace gets a repo too, so isolation is testable
        subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
        subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
        subprocess.run(["git", "-c", "user.name=replicate", "-c", "user.email=rep@local",
                        "commit", "-q", "-m", f"provision: workspace {rep_id} ({arm}, {phase})"],
                       cwd=ws, check=True)
    remotes = subprocess.run(["git", "remote"], cwd=ws, capture_output=True, text=True).stdout.strip()
    if remotes:
        raise SystemExit(f"workspace git has a remote ({remotes}) -- that is a path back")

    # --- 5. leak scan -------------------------------------------------------------------
    problems = leak_scan(ws, C.REPO)
    if problems:
        for p in problems:
            print("  LEAK:", p)
        raise SystemExit(f"provisioning aborted: {len(problems)} isolation problem(s)")
    for w in sorted(set(leak_warn(ws))):
        print("  WARN (study-design disclosure, not auto-edited):", w)
    print(f"[provision] isolation: no remote, no symlinks, no sealed material, no path back  OK")

    # receipt lives OUTSIDE the workspace and is the harness-side record of arm assignment
    receipt = {"workspace": str(ws), "arm": arm, "appendix_a_present": has_appendix, **meta,
               "charter_sha256": hashlib.sha256(charter.encode()).hexdigest()}
    (ws.parent / f"{rep_id}-provision-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"[provision] receipt -> {ws.parent / (rep_id + '-provision-receipt.json')}")
    return ws


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("rep_id")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db-limit", type=int, help="mock mode: copy only the first N structures")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    provision(a.rep_id, a.dest, a.dry_run, a.db_limit, a.force)
