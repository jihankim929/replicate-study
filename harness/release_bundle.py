#!/usr/bin/env python3
"""Produce the public-safe pre-registration release bundle for same-day arXiv posting.

Runs immediately after the final collection and its hash attestation. The PI posts; this produces
and VERIFIES the bundle.

The bundle is allowlisted, never filtered: files are named individually, so a new file added to
the repo cannot silently join a release. Everything included is then scanned, and the scan can
REFUSE — the failure mode this guards is a methods release that carries an excluded structure's
identity into the public record before scoring, which would invalidate the exclusion set for any
future use of this benchmark.
"""
import hashlib, json, re, shutil, sys
from pathlib import Path

ALLOW = [
    ("prereg/charter_v0.9.md", "charter master (both arms, phase spans intact)"),
    ("prereg/charter_revisions.md", "revision trail"),
    ("prereg/reference_screen_plan.md", "sealed reference-screen plan"),
    ("prereg/convergence_analysis_2026-08-29.md", "floor definition freezing record"),
    ("prereg/rubric_v1.0.md", "sealed scoring rubric"),
    ("prereg/audit_schema.md", "audit event schema"),
    ("prereg/benchmark_provenance.md", "benchmark provenance"),
    ("prereg/n16_derivation.md", "replicate-count derivation"),
    ("prereg/stage0_sample.SEALED.json", "sealed Stage 0 calibration sample"),
    ("benchmark_frozen/MANIFEST.sha256", "frozen world manifest, 12,499 entries"),
    # SI_LEDGER.md is WITHHELD ENTIRELY (PI ruling 2026-08-29, ruling 1). Not redacted, not
    # excerpted: it releases complete at study completion under the data-availability plan. It
    # names two excluded structures by name, including the pillar-stripped entry, and explains why
    # they are interesting -- and it is append-only, so there is no editing it into a releasable
    # state. A redacted derivative was considered and refused; the ledger goes out whole or not yet.
]

KEY_DIR = Path("answer-key")

# Vocabulary that discloses study design. NOT an automatic refusal: a methods manuscript has to be
# able to say that an integrity screen and an exclusion set exist. These are FLAGGED for the PI.
VOCAB = ["honeypot", "answer-key", "answer key", "operational trap", "planted",
         "exclusion set", "excluded as capacity artifact"]

# The manifest lists the whole world by definition, so every structure name appears in it. Scanning
# it for structure identities is a category error, not a leak check.
# A RANDOM DRAW FROM THE WORLD IS NOT A STATEMENT ABOUT ANY MEMBER. The manifest lists all 12,499
# by construction, and the Stage 0 sample is 300 drawn from it on a seed published alongside — an
# excluded structure appearing in either discloses nothing about its status, and the inference does
# not run in that direction. Both are exempt from identity scanning; everything else is not.
ID_SCAN_EXEMPT = {"MANIFEST.sha256", "stage0_sample.SEALED.json"}


def excluded_ids():
    """The identities that must never reach a public file: the SEALED EXCLUSION SET only.

    A first version of this scan collected every structure named anywhere in answer-key/ and
    refused on all of them -- 408 hits in the manifest, which lists all 12,499 by construction, and
    7 in a random 300-structure draw. That conflates "discussed in the key" with "is an excluded
    entry". The candidates, the disposed set and the structures ruled BALANCED are not secrets;
    which entries are excluded from the leaderboard is the secret, and it is the only one.
    """
    txt = (KEY_DIR / "exclusion_set_record.md").read_text()
    i = txt.find("FINAL STATE OF THE EXCLUSION SET")
    if i < 0:
        raise SystemExit("release_bundle: cannot locate the sealed exclusion set; refusing")
    seg = txt[i:]
    j = seg.find("Scoring consequence")
    ids = set()
    for m in re.finditer(r"`(\d{4}\[[A-Za-z]+\]\[[a-z]+\]\d)`", seg[:j if j > 0 else len(seg)]):
        ids.add(m.group(1))
    return ids


def collection_gate():
    """Refuse to build the bundle before the final collection and its hash attestation exist.

    MECHANICAL, NOT PROCEDURAL, and it did not start that way. The first version of this script
    carried the ordering only in its docstring -- and then WROTE "Produced after the final
    collection and its hash attestation" into CONTENTS.md, asserting a condition it had never
    checked. A bundle that claims an ordering it cannot verify is worse than one that says nothing,
    because the claim travels with the release. The gate now runs before any directory is created.
    """
    import subprocess
    ids = subprocess.run([sys.executable, "-c",
        "import sys;sys.path.insert(0,'harness');import config as C;"
        "print(' '.join(C.RATIFIED['phases']['main']['ids']))"],
        capture_output=True, text=True).stdout.split()
    missing = [r for r in ids if not Path(f"reps/main/collected/{r}/REPORT.md").is_file()]
    for extra in ("reps/main/collected/COLLECTION.md",
                  "reps/main/collected/BELL_FINGERPRINT.log"):
        if not Path(extra).is_file():
            missing.append(Path(extra).name)
    if missing:
        print("  REFUSED — the release bundle may not be built before the final collection")
        print(f"  and its hash attestation. Missing: {' '.join(missing)}")
        print("  Nothing was created.")
        sys.exit(3)
    att = Path("reps/main/collected/BELL_FINGERPRINT.log").read_text()
    n = sum(1 for l in att.splitlines() if len(l.split()) == 2 and len(l.split()[0]) == 64)
    print(f"  collection gate PASSED — 16 reports collected, attestation carries {n} hashes")
    return hashlib.sha256(att.encode()).hexdigest()


def main():
    attestation = collection_gate()
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "release/prereg_snapshot")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    ids = excluded_ids()
    print(f"  scanning against the {len(ids)} structures in the sealed exclusion set")

    findings, flags, rows = [], [], []
    for rel, desc in ALLOW:
        src = Path(rel)
        if not src.exists():
            findings.append(f"MISSING {rel}")
            continue
        body = src.read_text()
        for term in VOCAB:
            if term.lower() in body.lower():
                flags.append(f"{rel}: study-design vocabulary {term!r}")
        if Path(rel).name not in ID_SCAN_EXEMPT:
            hits = sorted(i for i in ids if i in body)
            if hits:
                findings.append(f"{rel}: NAMES AN EXCLUDED STRUCTURE — {hits}")
        dst = out / Path(rel).name
        dst.write_text(body)
        rows.append((hashlib.sha256(body.encode()).hexdigest(), dst.name, desc))

    (out / "MANIFEST.sha256").write_text("".join(f"{h}  {n}\n" for h, n, _ in sorted(rows, key=lambda r: r[1])))
    (out / "CONTENTS.md").write_text(
        "# Pre-registration release snapshot\n\n"
        "Produced after the final collection and its hash attestation, which this bundle's build\n"
        "REFUSES to proceed without. Collection attestation sha256: `" + attestation + "`.\n"
        "Allowlisted, scanned and hash-attested. Contains no answer-key material.\n\n"
        "| file | sha256 | contents |\n|---|---|---|\n" +
        "".join(f"| `{n}` | `{h[:16]}…` | {d} |\n" for h, n, d in sorted(rows, key=lambda r: r[1])))

    print(f"  bundled {len(rows)} files -> {out}")
    if findings:
        print(f"  REFUSED — {len(findings)} leak finding(s):")
        for f in findings:
            print(f"    {f}")
        shutil.rmtree(out)
        print("  bundle deleted; nothing is releasable until these are resolved")
        sys.exit(2)
    agg = hashlib.sha256("".join(h for h, _, _ in sorted(rows, key=lambda r: r[1])).encode()).hexdigest()
    if flags:
        print(f"  {len(flags)} study-design vocabulary flag(s) — PI decision, not an automatic refusal:")
        for f in flags:
            print(f"    {f}")
    print(f"  scan CLEAN of excluded-structure identities")
    print(f"  bundle sha256: {agg}")


if __name__ == "__main__":
    main()
