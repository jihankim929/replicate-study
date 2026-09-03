#!/usr/bin/env python3
"""Descriptor table for the frozen world -- READ-ONLY, and from two sources only.

SOURCES. `frozen/properties.json` (n_atoms, volume_A3, density_g_cm3, tier) and the 12,499 CIFs
themselves, plus `frozen/coord_keys.json` for the coordinate-group id and `frozen/MANIFEST.sha256`
for membership. NOTHING is read from `answer-key/`, from the SI tables, or from any run output.
The script opens exactly the paths named in SRC below and no others.

MEMBERSHIP IS THE MANIFEST, not a directory walk (PI ruling, Q1). A file present on disk but
absent from the manifest is not in the world and is not exported; a manifest line with no file is
a hard error rather than a short table.

HASHES ARE VERIFIED, NOT ASSUMED. Every CIF is sha256'd against its manifest line as it is read.
The corpus is small enough that this is nearly free, and an export that silently ran against a
drifted world is the failure this study has already had four variants of.

WHAT IS NOT HERE, AND WHY. Helium void fraction, largest cavity diameter, pore-limiting diameter
and accessible surface area are NOT emitted, because they are in neither source. `properties.json`
holds four fields and none of them is a pore descriptor, and the CIFs carry exactly nine tags --
two symmetry, one formula, three cell lengths, three cell angles -- with no surface-area, void,
pore or diameter tag anywhere in the corpus (scanned, all 12,499). They are geometry that must be
COMPUTED by probe insertion; there is no field to copy. Emitting them as empty columns was
rejected: a blank cell reads downstream as "measured and null", which is a stronger and falser
claim than an absent column. See analysis/README.md for the source that does hold them.

THE METAL RULE IS MEASURED FROM THE CORPUS, NOT IMPOSED. A textbook metal/non-metal split would
put As, Si, Ge, Sb, Te and Bi on the non-metal side, but the corpus's OWN identifiers carry all six
in the metal slot of `NNNN[<metal>][<topology>]...`. So the non-metal set below is the complement
of the elements the corpus itself names as metals, and every row is cross-checked against its own
identifier token -- disagreements are counted and reported, never silently resolved.
"""
import csv, hashlib, json, re, sys
from pathlib import Path

FROZEN = Path("/home1/users/Bei/benchmark/frozen")
SRC = {
    "properties":  FROZEN / "properties.json",
    "coord_keys":  FROZEN / "coord_keys.json",
    "manifest":    FROZEN / "MANIFEST.sha256",
    "corpus":      FROZEN / "CoRE_MOF_2024_CR_united",
}

# Complement of the elements the corpus names in its own metal slot. B is here and is also emitted
# as its own count column; it appears in no metal token.
NONMETALS = {"H", "B", "C", "N", "O", "F", "P", "S", "Cl", "Se", "Br", "I",
             "He", "Ne", "Ar", "Kr", "Xe", "Rn"}
COUNTED = ["C", "H", "N", "O", "F", "Cl", "S", "B"]

CELL_TAGS = {"_cell_length_a": "cell_a", "_cell_length_b": "cell_b", "_cell_length_c": "cell_c",
             "_cell_angle_alpha": "cell_alpha", "_cell_angle_beta": "cell_beta",
             "_cell_angle_gamma": "cell_gamma"}


def parse_cif(text):
    """Return cell, symmetry, formula and per-cell element counts from one CIF.

    Element counts come from the _atom_site loop, never from _chemical_formula_sum: the loop is the
    coordinates the simulation actually reads, the formula string is an annotation. The formula is
    carried through verbatim so the two can be compared, and they are, below.
    """
    out = {"space_group_hm": "", "space_group_number": "", "chemical_formula_sum": ""}
    counts, in_loop, hdr, sym_idx = {}, False, [], None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tok = line.split()

        if tok[0] in CELL_TAGS:
            out[CELL_TAGS[tok[0]]] = tok[1]; continue
        if tok[0] == "_symmetry_space_group_name_H-M":
            out["space_group_hm"] = line.split(None, 1)[1].strip().strip('"').strip("'"); continue
        if tok[0] == "_symmetry_Int_Tables_number":
            out["space_group_number"] = tok[1]; continue
        if tok[0] == "_chemical_formula_sum":
            out["chemical_formula_sum"] = line.split(None, 1)[1].strip().strip('"').strip("'")
            continue

        if line == "loop_":
            in_loop, hdr, sym_idx = True, [], None; continue
        if in_loop and line.startswith("_"):
            hdr.append(tok[0])
            if tok[0] == "_atom_site_type_symbol":
                sym_idx = len(hdr) - 1
            continue
        if in_loop and hdr:
            # A data line under a loop whose header we have. Only the atom-site loop is counted;
            # the symmetry-operation loop has no _atom_site_type_symbol and is skipped.
            if sym_idx is None or len(tok) < len(hdr):
                continue
            el = tok[sym_idx].strip()
            el = el[0].upper() + el[1:].lower() if len(el) > 1 else el.upper()
            el = re.sub(r"[^A-Za-z]", "", el)
            if el:
                counts[el] = counts.get(el, 0) + 1
    return out, counts


def main():
    props = json.loads(SRC["properties"].read_text())
    ckeys = json.loads(SRC["coord_keys"].read_text())

    manifest = {}
    for line in SRC["manifest"].read_text().splitlines():
        if not line.strip():
            continue
        h, rel = line.split(None, 1)
        manifest[Path(rel.strip()).stem] = (h, rel.strip())

    if len(manifest) != 12499:
        sys.exit(f"manifest is {len(manifest)} entries, expected 12499")

    group_id = {k: i for i, k in enumerate(sorted(set(ckeys.values())), start=1)}

    cols = (["structure_id", "coordinate_group_id", "coordinate_group_sha256", "tier",
             "n_atoms", "n_atoms_cif", "volume_A3", "density_g_cm3",
             "cell_a", "cell_b", "cell_c", "cell_alpha", "cell_beta", "cell_gamma",
             "space_group_hm", "space_group_number", "chemical_formula_sum",
             "metal_elements", "n_metal_atoms"]
            + [f"n_{e}" for e in COUNTED])

    rows, bad = [], {"hash": [], "natoms": [], "metal_vs_id": [], "no_spacegroup": [], "formula": []}

    for sid in sorted(manifest):
        h_expect, rel = manifest[sid]
        path = SRC["corpus"] / rel
        blob = path.read_bytes()
        if hashlib.sha256(blob).hexdigest() != h_expect:
            bad["hash"].append(sid)
        cif, counts = parse_cif(blob.decode("utf-8", "replace"))

        p = props[sid]
        n_cif = sum(counts.values())
        if n_cif != p["n_atoms"]:
            bad["natoms"].append(sid)
        if not cif["space_group_hm"]:
            bad["no_spacegroup"].append(sid)

        metals = sorted(e for e in counts if e not in NONMETALS)
        n_metal = sum(counts[e] for e in metals)

        # Cross-check against the identifier's own metal token -- the corpus grading its own rule.
        m = re.match(r"^\d{4}\[([^\]]+)\]", sid)
        if m:
            named = set(re.findall(r"[A-Z][a-z]?", m.group(1)))
            if named - set(metals):
                bad["metal_vs_id"].append(sid)

        # Formula string vs counted loop, compared as multisets.
        fs = dict((e, int(n or 1)) for e, n in
                  re.findall(r"([A-Z][a-z]?)(\d*)", cif["chemical_formula_sum"]) if e)
        if fs and fs != counts:
            bad["formula"].append(sid)

        row = {"structure_id": sid,
               "coordinate_group_id": group_id[ckeys[sid]],
               "coordinate_group_sha256": ckeys[sid],
               "tier": p["tier"], "n_atoms": p["n_atoms"], "n_atoms_cif": n_cif,
               "volume_A3": p["volume_A3"], "density_g_cm3": p["density_g_cm3"],
               "space_group_hm": cif["space_group_hm"],
               "space_group_number": cif["space_group_number"],
               "chemical_formula_sum": cif["chemical_formula_sum"],
               "metal_elements": ";".join(metals), "n_metal_atoms": n_metal}
        for t in CELL_TAGS.values():
            row[t] = cif.get(t, "")
        for e in COUNTED:
            row[f"n_{e}"] = counts.get(e, 0)
        rows.append(row)

    out = Path(sys.argv[1])
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"rows={len(rows)} groups={len(set(r['coordinate_group_id'] for r in rows))}")
    for k, v in bad.items():
        print(f"CHECK {k}: {len(v)}" + (f"  e.g. {v[:3]}" if v else ""))


if __name__ == "__main__":
    main()
