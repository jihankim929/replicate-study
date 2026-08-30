"""Charge-balance leg of gate G3, over the whole database.

Every CIF in this database carries DDEC6 partial charges (PACMAN v1.1) in
`_atom_site_charge`.  For an unmodified deposited framework the checkable
statement of "charge-balanced" is that the framework's own charge set sums to
zero to within numerical noise -- i.e. no charged component has been stripped of
its counter-ion in the file as supplied.  This computes that sum, plus the
element roster and a formula-unit summary, for all 12,499 entries.

The chargeless protocol of s3 means these charges never enter a simulation; they
are used here only as the integrity check G3 asks for.

usage: charges.py <out.csv>
"""
import os, re, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
DB = os.path.join(WS, "db")


def scan(path):
    q = 0.0
    n = 0
    els = {}
    inloop = False
    tags = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if s == "loop_":
                tags = []
                inloop = False
                continue
            if s.startswith("_atom_site_"):
                tags.append(s.split()[0])
                inloop = tags[0].startswith("_atom_site_")
                continue
            if s.startswith("_") or not s or s.startswith("#"):
                continue
            if inloop and tags:
                p = s.split()
                if len(p) < len(tags):
                    inloop = False
                    continue
                try:
                    ic = tags.index("_atom_site_charge")
                    q += float(p[ic])
                except (ValueError, IndexError):
                    pass
                el = re.sub(r"[^A-Za-z]", "", p[0])
                if len(el) > 1:
                    el = el[0].upper() + el[1:].lower()
                els[el] = els.get(el, 0) + 1
                n += 1
    return q, n, els


def main():
    out = sys.argv[1]
    files = sorted(f for f in os.listdir(DB) if f.endswith(".cif"))
    with open(out, "w") as fh:
        fh.write("name,natoms,qsum,qsum_per_atom,elements\n")
        for f in files:
            try:
                q, n, els = scan(os.path.join(DB, f))
                fh.write('"%s",%d,%.6f,%.3g,"%s"\n' % (
                    f[:-4], n, q, q / max(n, 1),
                    "|".join("%s%d" % (k, v) for k, v in sorted(els.items()))))
            except Exception as e:
                fh.write('"%s",0,,,"ERROR:%s"\n' % (f[:-4], str(e)[:60]))


if __name__ == "__main__":
    main()
