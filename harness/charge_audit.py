#!/usr/bin/env python3
"""Charge-balance audit — the study's integrity instrument, rebuilt and committed.

PI ruling 2026-08-29 on the pattern: **the instrument code commits to the open repo — it is
methodology, released with the study. Only its OUTPUTS (exclusion set, dossiers) stay sealed.**
Retroactive: any session-local machinery the sealed record references gets rebuilt and committed.
This file is the first discharge of that ruling. Before it, the sealed record named
`census.py`, `census2.py`, `frag.py`, `rings.py`, `bonds.py`, `periodic.py`, `sweep.py`,
`pass3.py` and `final.py` as its reproduction path, and **none of them existed anywhere** — the
audit could be described but not re-run (Q3 blocked, 2026-08-29).

WHAT IT DECIDES
    A framework is charge-unbalanced when it carries charged metal centres and the cell holds no
    species that can compensate them. That is a question about BONDED ENVIRONMENT, not about which
    elements are present -- which is the whole reason this instrument exists in three passes.

THE THREE PASSES, AND WHY EACH ONE EXISTS
    Pass 1  element-level: metal present, and no F/Cl/Br/I, no O, no S, no B anywhere.
            Wrong in BOTH directions, which is why it is only a first cut.
    Pass 2  chemistry-aware: classify each heteroatom by what it is actually bonded to.
              - halide bonded to C      -> C-F / C-Cl on a neutral linker, compensates nothing
              - O bonded to 2 C, no metal-> ether, neutral
              - S in a ring, only C nbrs -> thiophene, neutral
              - CN bridging two metals   -> IS a compensator, though it is only C and N,
                                            which pass 1 cannot see by construction
    Pass 3  azolate anions are built from C, H and N ONLY, so no presence-of-heteroatom test can
            see them. A 5-membered ring with >=2 N is an azolate anion (-1) iff at least one ring
            N is metal-bound AND no ring N carries an exocyclic H or C. That exocyclic test is the
            only connectivity signature separating azolate from neutral azole.
            Then, quantitatively: net = sum(metal x oxidation state) - n_azolate.

THE STANDING WARNING THIS INSTRUMENT CARRIES
    It has been wrong three times in the same way -- an anion, or a neutral group, that a
    presence-of-element test cannot see (cyanide at pass 1, azolate at pass 2, and the
    neutral-context heteroatoms that pass 2 itself had to add). **Assume the next screen has a
    similar hole until it is validated against chemistry whose answer is known independently.**
    The regression below is that validation, and it is not optional.

    `--regression` must reproduce, on the 1,731-structure slice:
        7 flags in the [sql] subset, 100 pass-2 flags, 70 azolate-balanced, 30 unbalanced.
    A run whose regression does not pass is not evidence about any database.

    The DDEC6 `_atom_site_charge` column is PACMAN-normalised to ~0 by construction. It carries no
    information about formal charge balance and is deliberately not read.

    ./harness/charge_audit.py --db benchmark --regression
    ./harness/charge_audit.py --db <frozen>/ASR --db <frozen>/FSR --db <frozen>/Ion --json out.json
"""
import argparse, json, math, os, sys
from collections import defaultdict

# Cordero covalent radii (Å). Only elements this benchmark family contains need entries; an
# unknown element raises rather than defaulting, so a silent mis-bond is impossible.
RCOV = {
 "H":0.31,"B":0.84,"C":0.76,"N":0.71,"O":0.66,"F":0.57,"Si":1.11,"P":1.07,"S":1.05,"Cl":1.02,
 "As":1.19,"Se":1.20,"Br":1.20,"Te":1.38,"I":1.39,"Li":1.28,"Na":1.66,"K":2.03,"Rb":2.20,
 "Cs":2.44,"Be":0.96,"Mg":1.41,"Ca":1.76,"Sr":1.95,"Ba":2.15,"Sc":1.70,"Ti":1.60,"V":1.53,
 "Cr":1.39,"Mn":1.50,"Fe":1.42,"Co":1.38,"Ni":1.24,"Cu":1.32,"Zn":1.22,"Y":1.90,"Zr":1.75,
 "Nb":1.64,"Mo":1.54,"Ru":1.46,"Rh":1.42,"Pd":1.39,"Ag":1.45,"Cd":1.44,"In":1.42,"Sn":1.39,
 "Sb":1.39,"Hf":1.75,"Ta":1.70,"W":1.62,"Re":1.51,"Os":1.44,"Ir":1.41,"Pt":1.36,"Au":1.36,
 "Hg":1.32,"Tl":1.45,"Pb":1.46,"Bi":1.48,"La":2.07,"Ce":2.04,"Pr":2.03,"Nd":2.01,"Sm":1.98,
 "Eu":1.98,"Gd":1.96,"Tb":1.94,"Dy":1.92,"Ho":1.92,"Er":1.89,"Tm":1.90,"Yb":1.87,"Lu":1.87,
 "Th":2.06,"U":1.96,"Np":1.90,"Pu":1.87,"Am":1.80,"Ga":1.22,"Ge":1.20,
 # Al was omitted on the first build. It did not mis-bond -- the table RAISES on an unknown
 # element rather than defaulting, so 55 Al-bearing structures failed loudly instead of
 # being silently mis-analysed. That is the intended behaviour and it is why this line exists.
 "Al":1.21,
}
NONMETAL = {"H","B","C","N","O","F","Si","P","S","Cl","As","Se","Br","Te","I"}
HALIDE   = {"F","Cl","Br","I"}
# Standard divalent states, with the well-determined exceptions the sealed method names.
OXID = defaultdict(lambda: 2)
OXID.update({"Li":1,"Na":1,"K":1,"Rb":1,"Cs":1,"Ag":1,
             "Al":3,"Ga":3,"In":3,"Sc":3,"Y":3,"La":3,"Ce":3,"Pr":3,"Nd":3,"Sm":3,"Eu":3,
             "Gd":3,"Tb":3,"Dy":3,"Ho":3,"Er":3,"Tm":3,"Yb":3,"Lu":3,"Bi":3,"Fe":3,"Cr":3,
             "Zr":4,"Hf":4,"Ti":4,"Th":4,"U":6,"Sn":4,"Ge":4,"Si":4})
BOND_TOL = 1.15   # sealed method: 1.15 x sum-of-covalent-radii


def parse_cif(path):
    a=b=c=al=be=ga=None; sym=[]; frac=[]; cols=[]; inloop=False
    for ln in open(path, errors="replace"):
        s = ln.strip()
        if   s.startswith("_cell_length_a"):     a  = float(s.split()[1])
        elif s.startswith("_cell_length_b"):     b  = float(s.split()[1])
        elif s.startswith("_cell_length_c"):     c  = float(s.split()[1])
        elif s.startswith("_cell_angle_alpha"):  al = float(s.split()[1])
        elif s.startswith("_cell_angle_beta"):   be = float(s.split()[1])
        elif s.startswith("_cell_angle_gamma"):  ga = float(s.split()[1])
        if s.startswith("loop_"): inloop=True; cols=[]; continue
        if inloop and s.startswith("_"): cols.append(s.split()[0]); continue
        if inloop and cols:
            if "_atom_site_type_symbol" in cols and s and not s.startswith("#"):
                p = s.split()
                if len(p) >= len(cols):
                    sym.append(p[cols.index("_atom_site_type_symbol")])
                    frac.append(tuple(float(p[cols.index(f"_atom_site_fract_{k}")]) for k in "xyz"))
                continue
            inloop=False; cols=[]
    return (a,b,c,al,be,ga), sym, frac


def cell_matrix(a,b,c,al,be,ga):
    ra,rb,rg = (math.radians(x) for x in (al,be,ga))
    ca,cb,cg,sg = math.cos(ra), math.cos(rb), math.cos(rg), math.sin(rg)
    v = math.sqrt(max(1-ca*ca-cb*cb-cg*cg+2*ca*cb*cg, 1e-12))
    return ((a,0.0,0.0), (b*cg,b*sg,0.0), (c*cb, c*(ca-cb*cg)/sg, c*v/sg))


def neighbours(cell, sym, frac):
    """Periodic covalent graph via a spatial hash over a replicated supercell.

    Replication is chosen PER AXIS from the perpendicular cell widths, so bonds are never missed
    in thin cells -- the failure mode that made the brute-force version wrong on large cells
    before it was rebuilt (sealed method, 'Instrument changes').
    """
    M = cell_matrix(*cell)
    (ax,ay,az),(bx,by,bz),(cx,cy,cz) = M
    vol = abs(ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx))
    def cross(u,w): return (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
    def norm(u):   return math.sqrt(sum(x*x for x in u))
    widths = [vol/norm(cross(M[(i+1)%3], M[(i+2)%3])) for i in range(3)]
    rmax = max(RCOV[s] for s in sym) * 2 * BOND_TOL
    reps = [max(1, int(math.ceil(rmax / w))) for w in widths]

    pts = []   # (x, y, z, original_index)
    for i,(fx,fy,fz) in enumerate(frac):
        for ia in range(-reps[0], reps[0]+1):
            for ib in range(-reps[1], reps[1]+1):
                for ic in range(-reps[2], reps[2]+1):
                    u,v,w = fx+ia, fy+ib, fz+ic
                    pts.append((u*ax+v*bx+w*cx, u*ay+v*by+w*cy, u*az+v*bz+w*cz, i))
    gs = max(rmax, 1e-6)
    grid = defaultdict(list)
    for p in pts:
        grid[(int(p[0]//gs), int(p[1]//gs), int(p[2]//gs))].append(p)

    nb = [set() for _ in sym]
    for i,(fx,fy,fz) in enumerate(frac):
        x,y,z = fx*ax+fy*bx+fz*cx, fx*ay+fy*by+fz*cy, fx*az+fy*bz+fz*cz
        gx,gy,gz = int(x//gs), int(y//gs), int(z//gs)
        ri = RCOV[sym[i]]
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for (px,py,pz,j) in grid.get((gx+dx,gy+dy,gz+dz), ()):
                        if j == i and abs(px-x)<1e-9 and abs(py-y)<1e-9 and abs(pz-z)<1e-9:
                            continue
                        cut = (ri + RCOV[sym[j]]) * BOND_TOL
                        if (px-x)**2 + (py-y)**2 + (pz-z)**2 <= cut*cut:
                            nb[i].add(j)
    return nb


def rings5(nb, sym, limit=4000):
    """Enumerate 5-membered rings, seeded from N only (azolates always contain >=2 N)."""
    out, seen = [], set()
    ns = [i for i,s in enumerate(sym) if s == "N"]
    for start in ns[:limit]:
        stack = [(start, [start])]
        while stack:
            cur, path = stack.pop()
            if len(path) == 5:
                if start in nb[cur]:
                    key = frozenset(path)
                    if key not in seen:
                        seen.add(key); out.append(list(path))
                continue
            for j in nb[cur]:
                if j not in path and (len(path) < 4 or True):
                    stack.append((j, path + [j]))
    return out


def audit(path):
    cell, sym, frac = parse_cif(path)
    if any(v is None for v in cell) or not sym:
        return {"error": "unparseable"}
    nb = neighbours(cell, sym, frac)
    metals = [i for i,s in enumerate(sym) if s not in NONMETAL]
    els = set(sym)

    # ---- pass 1: element-level, as literally stated in the kill note --------------------
    p1 = bool(metals) and not (els & (HALIDE | {"O","S","B"}))

    # ---- pass 2: classify each candidate compensator by its bonded environment ----------
    real = 0
    for i,s in enumerate(sym):
        if s not in (HALIDE | {"O","S","B"}):
            continue
        nbs = [sym[j] for j in nb[i]]
        if s in HALIDE and "C" in nbs and not any(x not in NONMETAL for x in nbs):
            continue                                    # C-F / C-Cl: neutral linker
        if s == "O" and nbs.count("C") == 2 and not any(x not in NONMETAL for x in nbs):
            continue                                    # ether: neutral
        if s == "S" and nbs and all(x == "C" for x in nbs):
            continue                                    # thiophene: neutral
        real += 1
    # cyanide bridging two metals IS a compensator, though built only from C and N
    cn = 0
    for i,s in enumerate(sym):
        if s != "C":
            continue
        nn = [j for j in nb[i] if sym[j] == "N"]
        mm = [j for j in nb[i] if sym[j] not in NONMETAL]
        if len(nn) == 1 and mm and any(sym[k] not in NONMETAL for k in nb[nn[0]]):
            cn += 1
    p2 = bool(metals) and real == 0 and cn == 0

    # ---- pass 3: azolate anions, invisible to any presence-of-element test --------------
    azolate = 0
    if p2:
        for ring in rings5(nb, sym):
            rn = [i for i in ring if sym[i] == "N"]
            if len(rn) < 2:
                continue
            if not any(any(sym[j] not in NONMETAL for j in nb[i]) for i in rn):
                continue                                # no ring N is metal-bound
            exo = False
            for i in rn:
                for j in nb[i]:
                    if j not in ring and sym[j] in ("H", "C"):
                        exo = True
            if not exo:
                azolate += 1                            # metal-bound only -> anionic
    net = sum(OXID[sym[i]] for i in metals) - azolate if p2 else None
    return {"n_atoms": len(sym), "elements": sorted(els), "n_metals": len(metals),
            "pass1": p1, "pass2": p2, "azolate": azolate, "net_charge": net,
            "unbalanced": bool(p2 and net not in (None, 0))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", action="append", required=True, help="directory of .cif (repeatable)")
    ap.add_argument("--regression", action="store_true", help="assert the sealed slice result")
    ap.add_argument("--json", help="write full per-structure output here")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()

    files = []
    for d in a.db:
        files += [os.path.join(d, n) for n in sorted(os.listdir(d)) if n.endswith(".cif")]
    if a.limit:
        files = files[:a.limit]

    res, errs = {}, 0
    for p in files:
        sid = os.path.basename(p)[:-4]
        try:
            r = audit(p)
        except Exception as exc:
            r = {"error": f"{type(exc).__name__}: {exc}"}
        if "error" in r:
            errs += 1
        res[sid] = r

    ok  = {k: v for k, v in res.items() if "error" not in v}
    p1  = [k for k, v in ok.items() if v["pass1"]]
    p2  = [k for k, v in ok.items() if v["pass2"]]
    bal = [k for k in p2 if ok[k]["net_charge"] == 0]
    unb = [k for k in p2 if ok[k]["unbalanced"]]

    print(f"  parsed        : {len(ok)}/{len(files)}  (errors {errs})")
    print(f"  pass-1 flags  : {len(p1)}")
    print(f"  pass-2 flags  : {len(p2)}")
    print(f"  azolate-balanced (net=0): {len(bal)}")
    print(f"  UNBALANCED    : {len(unb)}")

    if a.json:
        json.dump({"summary": {"parsed": len(ok), "errors": errs, "pass1": len(p1),
                               "pass2": len(p2), "balanced": len(bal), "unbalanced": len(unb)},
                   "unbalanced": sorted(unb), "per_structure": res}, open(a.json, "w"), indent=1)
        print(f"  -> {a.json}")

    if a.regression:
        sql_unb = [k for k in unb if "[sql]" in k]
        exp = {"pass2": 100, "balanced": 70, "unbalanced": 30, "sql_unbalanced": 7}
        got = {"pass2": len(p2), "balanced": len(bal), "unbalanced": len(unb),
               "sql_unbalanced": len(sql_unb)}
        print("\n  REGRESSION vs the sealed slice result:")
        allok = True
        for k in exp:
            good = got[k] == exp[k]
            allok &= good
            print(f"    {k:<16} expected {exp[k]:>4}  got {got[k]:>4}   {'OK' if good else 'MISMATCH'}")
        print(f"  REGRESSION {'PASS' if allok else 'FAIL'}")
        sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
