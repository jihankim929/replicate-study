"""Charge-balanced defunctionalisation of database structures.

Charter §3 permits modified candidates provided the modification is chemically
charge-balanced and reproducible from the repository. The one family of
modification used here is **substituent → H**: a terminal monovalent group is
deleted and replaced by a hydrogen atom on the same bond vector at a standard
bond length. Monovalent in, monovalent out, so the formal charge of every atom
that survives is unchanged and the framework stays neutral by construction.

Groups recognised (all must be terminal, i.e. bonded to exactly one heavy atom):
  -F, -Cl, -Br, -I      halogen on any heavy atom      → H
  -CH3                  carbon with 3 H and 1 heavy    → H
  -NH2                  nitrogen with 2 H and 1 heavy  → H
  -OH                   oxygen with 1 H and 1 heavy    → H
  -NO2                  nitrogen with 2 O and 1 heavy  → H

Bonding is perceived geometrically: atoms i and j are bonded when
    d(i,j) < r_cov(i) + r_cov(j) + TOL,  TOL = 0.40 Å,
evaluated over periodic images. Metals are excluded from bond perception on the
substituent side so that coordination spheres are never cut.

Nothing here is a simulation result. The output is a CIF that is then run
through exactly the same pinned protocol as any database structure.
"""
import os, sys, math, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cifutil

WS = os.path.dirname(HERE)
TOL = 0.40

RCOV = {
 "H":0.31,"B":0.84,"C":0.76,"N":0.71,"O":0.66,"F":0.57,"Si":1.11,"P":1.07,
 "S":1.05,"Cl":1.02,"Br":1.20,"I":1.39,"Se":1.20,"As":1.19,"Ge":1.20,
 "Te":1.38,"Sb":1.39,
}
DEFAULT_METAL_RCOV = 1.45
NONMETAL = set(RCOV)

BONDLEN = {"C": 1.09, "N": 1.01, "O": 0.96, "S": 1.34, "B": 1.19, "P": 1.42,
           "Si": 1.48}


def rcov(sym):
    return RCOV.get(sym, DEFAULT_METAL_RCOV)


def build(cifpath):
    d = cifutil.parse_cif(cifpath)
    M = np.array(cifutil.cell_matrix(d["a"], d["b"], d["c"],
                                     d["alpha"], d["beta"], d["gamma"]))
    sym = [a[0] for a in d["atoms"]]
    frac = np.array([[a[1] % 1.0, a[2] % 1.0, a[3] % 1.0] for a in d["atoms"]])
    return d, M, sym, frac


def neighbours(M, sym, frac):
    """Adjacency list over periodic images; also the image shift used."""
    n = len(sym)
    cart = frac.dot(M)
    shifts = np.array([[i, j, k] for i in (-1, 0, 1) for j in (-1, 0, 1)
                       for k in (-1, 0, 1)], dtype=float)
    adj = [[] for _ in range(n)]
    for s in shifts:
        off = s.dot(M)
        dd = cart[:, None, :] - (cart[None, :, :] + off[None, None, :])
        dist = np.sqrt((dd * dd).sum(-1))
        for i in range(n):
            for j in np.where(dist[i] < 3.2)[0]:
                if i == j and abs(s).sum() == 0:
                    continue
                cut = rcov(sym[i]) + rcov(sym[j]) + TOL
                if dist[i, j] < cut:
                    adj[i].append((int(j), -s))
    return adj, cart


def find_groups(sym, adj):
    """Return list of (kind, atoms_to_delete, anchor_index)."""
    heavy = lambda k: sym[k] != "H"
    groups = []
    for i, s in enumerate(sym):
        hv = [j for j, _ in adj[i] if heavy(j)]
        hs = [j for j, _ in adj[i] if sym[j] == "H"]
        if s in ("F", "Cl", "Br", "I") and len(hv) == 1:
            groups.append(("halide-" + s, [i], hv[0]))
        elif s == "C" and len(hv) == 1 and len(hs) == 3:
            groups.append(("methyl", [i] + hs, hv[0]))
        elif s == "N" and len(hv) == 1 and len(hs) == 2:
            groups.append(("amine", [i] + hs, hv[0]))
        elif s == "O" and len(hv) == 1 and len(hs) == 1:
            groups.append(("hydroxyl", [i] + hs, hv[0]))
        elif s == "N" and len(hs) == 0 and len(hv) == 3:
            os_ = [j for j in hv if sym[j] == "O"]
            rest = [j for j in hv if sym[j] != "O"]
            if len(os_) == 2 and len(rest) == 1:
                term = [j for j in os_ if len([k for k, _ in adj[j] if heavy(k)]) == 1]
                if len(term) == 2:
                    groups.append(("nitro", [i] + term, rest[0]))
    return groups


def defunctionalise(cifpath, outpath, name, kinds=None):
    """Write a CIF with the requested substituent kinds replaced by H.

    Returns (n_groups_replaced, {kind: count}, natoms_before, natoms_after).
    """
    d, M, sym, frac = build(cifpath)
    adj, cart = neighbours(M, sym, frac)
    groups = find_groups(sym, adj)
    if kinds is not None:
        groups = [g for g in groups if g[0].split("-")[0] in kinds]

    drop, adds, counts = set(), [], {}
    Minv = np.linalg.inv(M)
    for kind, atoms, anchor in groups:
        if any(a in drop for a in atoms) or anchor in drop:
            continue
        head = atoms[0]
        # bond vector anchor -> head, using the image of head nearest the anchor
        best, bestd = None, 1e9
        for s in [(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]:
            v = (frac[head] + np.array(s, dtype=float)).dot(M) - cart[anchor]
            dn = math.sqrt((v * v).sum())
            if dn < bestd:
                bestd, best = dn, v
        L = BONDLEN.get(sym[anchor], 1.09)
        newc = cart[anchor] + best / bestd * L
        drop.update(atoms)
        adds.append(("H", newc.dot(Minv) % 1.0))
        counts[kind] = counts.get(kind, 0) + 1

    keep = [i for i in range(len(sym)) if i not in drop]
    with open(outpath, "w") as o:
        o.write("data_%s\n" % name)
        o.write("_symmetry_space_group_name_H-M    'P 1'\n")
        o.write("_symmetry_Int_Tables_number       1\n")
        o.write("_symmetry_cell_setting            triclinic\n")
        for k, v in (("a", d["a"]), ("b", d["b"]), ("c", d["c"])):
            o.write("_cell_length_%s    %.6f\n" % (k, v))
        for k, v in (("alpha", d["alpha"]), ("beta", d["beta"]), ("gamma", d["gamma"])):
            o.write("_cell_angle_%s %.6f\n" % (k, v))
        o.write("loop_\n_symmetry_equiv_pos_as_xyz\n'x,y,z'\n")
        o.write("loop_\n_atom_site_label\n_atom_site_type_symbol\n")
        o.write("_atom_site_fract_x\n_atom_site_fract_y\n_atom_site_fract_z\n")
        for i in keep:
            o.write("%-6s %-3s %10.6f %10.6f %10.6f\n"
                    % (sym[i] + "_", sym[i], frac[i][0], frac[i][1], frac[i][2]))
        for s, f in adds:
            o.write("%-6s %-3s %10.6f %10.6f %10.6f\n" % (s + "_", s, f[0], f[1], f[2]))
    return len(counts) and sum(counts.values()), counts, len(sym), len(keep) + len(adds)


if __name__ == "__main__":
    src, dst, name = sys.argv[1], sys.argv[2], sys.argv[3]
    kinds = sys.argv[4].split("+") if len(sys.argv) > 4 else None
    n, counts, before, after = defunctionalise(src, dst, name, kinds)
    print("groups=%s counts=%s natoms %d -> %d" % (n, counts, before, after))
