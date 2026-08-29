#!/usr/bin/env python3
"""Raw chemical evidence for hand-ruling an entry's charge state.

Written for the dossier sitting of 2026-08-29, where the PI ruled that cluster D could not be
ruled on the instrument's NUMBERS and asked instead for the evidence to rule the chemistry by
hand. This produces exactly that, and it produces NO verdict -- deliberately. Its output is the
three things a chemist needs and nothing that would prejudge them:

  1. LINKER FORMULA UNITS  -- metals stripped, the remaining connected components identified as
     discrete molecules or as periodic (polymeric) fragments, grouped by empirical formula.
  2. RING ATOMS AS DEPOSITED -- every 5-membered ring carrying >=2 N, grouped by composition.
  3. PROTONATION-RELEVANT BOND ENVIRONMENTS -- per ring nitrogen: its degree, whether it is bound
     to a metal, and whether it carries an exocyclic H or C. That triple is the entire basis on
     which azolate (anionic) separates from azole (neutral), so it is reported per nitrogen rather
     than summarised.

Instrument code, so it commits to the open repo per the PI's ruling of 2026-08-29. Its OUTPUT for
specific structures is an exclusion-set artefact and belongs in the sealed record.

Periodicity is decided honestly: components are found on the REPLICATED point set with image
tracking, so a fragment that reaches its own periodic image is reported as polymeric rather than
being silently folded into a discrete molecule.

  ./harness/charge_evidence.py --db <dir> --stem "2020[Cu][she]3[ASR]1"
"""
import argparse, collections, math, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charge_audit import parse_cif, cell_matrix, RCOV, NONMETAL, OXID, BOND_TOL


def replicated_graph(cell, sym, frac):
    """Bond graph over a replicated supercell, keyed by (original_index, image)."""
    M = cell_matrix(*cell)
    (ax,ay,az),(bx,by,bz),(cx,cy,cz) = M
    vol = abs(ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx))
    cross = lambda u,w: (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
    norm  = lambda u: math.sqrt(sum(x*x for x in u))
    widths = [vol/norm(cross(M[(i+1)%3], M[(i+2)%3])) for i in range(3)]
    rmax = max(RCOV[s] for s in sym) * 2 * BOND_TOL
    reps = [max(1, int(math.ceil(rmax/w))) for w in widths]

    nodes = []
    for i,(fx,fy,fz) in enumerate(frac):
        for ia in range(-reps[0], reps[0]+1):
            for ib in range(-reps[1], reps[1]+1):
                for ic in range(-reps[2], reps[2]+1):
                    u,v,w = fx+ia, fy+ib, fz+ic
                    nodes.append(((i,(ia,ib,ic)),
                                  u*ax+v*bx+w*cx, u*ay+v*by+w*cy, u*az+v*bz+w*cz))
    gs = max(rmax, 1e-6)
    grid = collections.defaultdict(list)
    for n in nodes:
        grid[(int(n[1]//gs), int(n[2]//gs), int(n[3]//gs))].append(n)

    adj = collections.defaultdict(set)
    for (key,x,y,z) in nodes:
        i = key[0]; ri = RCOV[sym[i]]
        gx,gy,gz = int(x//gs), int(y//gs), int(z//gs)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for (k2,px,py,pz) in grid.get((gx+dx,gy+dy,gz+dz), ()):
                        if k2 == key: continue
                        cut = (ri + RCOV[sym[k2[0]]]) * BOND_TOL
                        if (px-x)**2+(py-y)**2+(pz-z)**2 <= cut*cut:
                            adj[key].add(k2); adj[k2].add(key)
    return adj, reps


def formula(counts):
    order = ["C","H","N","O","S","F","Cl","Br","I","B","P","Si"]
    ks = [e for e in order if e in counts] + sorted(k for k in counts if k not in order)
    return "".join(f"{e}{counts[e] if counts[e]>1 else ''}" for e in ks)


def evidence(path):
    cell, sym, frac = parse_cif(path)
    adj, reps = replicated_graph(cell, sym, frac)
    metals = [i for i,s in enumerate(sym) if s not in NONMETAL]
    mcount = collections.Counter(sym[i] for i in metals)

    # ---- 1. linkers: strip metals, find components on the replicated graph -------------
    # A component touching the outermost image shell may be TRUNCATED by the edge of the
    # replicated block rather than genuinely small, so it is discarded rather than reported.
    # Serving edge fragments as a fragment inventory would invent chemistry that is not there.
    org = {k for k in adj if sym[k[0]] in NONMETAL}
    seen, comps = set(), []
    for start in org:
        if start in seen: continue
        stack, comp = [start], []
        seen.add(start)
        while stack:
            cur = stack.pop(); comp.append(cur)
            for nb in adj[cur]:
                if nb in org and nb not in seen:
                    seen.add(nb); stack.append(nb)
        comps.append(comp)
    edge = lambda c: any(abs(k[1][ax]) >= reps[ax] for k in c for ax in (0,1,2))
    linkers, truncated, polymeric = collections.Counter(), 0, collections.Counter()
    keyed = {}
    for comp in comps:
        if edge(comp): truncated += 1; continue
        idxs = [k[0] for k in comp]
        if len(idxs) != len(set(idxs)):                 # reaches its own image
            polymeric[formula(collections.Counter(sym[i] for i in set(idxs)))] += 1
            continue
        keyed[frozenset(idxs)] = formula(collections.Counter(sym[i] for i in idxs))
    for f in keyed.values(): linkers[(f, "discrete")] += 1
    for f, n in polymeric.items(): linkers[(f, "polymeric")] += 1

    # ---- 2 + 3. rings and per-nitrogen environments -------------------------------------
    home = [(i,(0,0,0)) for i in range(len(sym))]
    rings, seenr = [], set()
    for s in home:
        if sym[s[0]] != "N": continue
        stack = [(s, [s])]
        while stack:
            cur, path = stack.pop()
            if len(path) == 5:
                if s in adj[cur]:
                    key = frozenset(k[0] for k in path)
                    if len(key) == 5 and key not in seenr:
                        seenr.add(key); rings.append(path)
                continue
            for nb in adj[cur]:
                if nb not in path: stack.append((nb, path + [nb]))

    groups = collections.defaultdict(lambda: {"count": 0, "envs": collections.Counter()})
    for ring in rings:
        els = collections.Counter(sym[k[0]] for k in ring)
        if els.get("N", 0) < 2: continue
        sig = formula(els)
        g = groups[sig]; g["count"] += 1
        for k in ring:
            if sym[k[0]] != "N": continue
            nbrs = [nb for nb in adj[k]]
            exo  = [nb for nb in nbrs if nb not in ring]
            env = (
                len(nbrs),
                any(sym[nb[0]] not in NONMETAL for nb in nbrs),          # metal-bound
                any(sym[nb[0]] == "H" for nb in exo),                    # exocyclic H
                any(sym[nb[0]] == "C" for nb in exo),                    # exocyclic C
            )
            g["envs"][env] += 1
    return {"truncated": truncated, "cell": cell, "n_atoms": len(sym), "metals": dict(mcount),
            "reps": reps, "linkers": linkers, "rings": groups,
            "composition": dict(collections.Counter(sym))}


def render(stem, e):
    out = []
    out.append(f"### `{stem}`\n")
    out.append(f"- **Cell contents as deposited:** {formula(collections.Counter(e['composition']))} "
               f"— {e['n_atoms']} atoms")
    out.append(f"- **Metal census:** " + ", ".join(
        f"{k} × {v} (assumed {OXID[k]:+d})" for k,v in sorted(e["metals"].items())))
    tot = sum(v*OXID[k] for k,v in e["metals"].items())
    out.append(f"- **Total formal metal charge, standard states:** **{tot:+d}**")
    out.append("\n**1. Linker formula units** (metals stripped; per unit cell; edge-truncated components discarded)\n")
    out.append("| formula unit | connectivity | count |")
    out.append("|---|---|---:|")
    for (f, kind), n in sorted(e["linkers"].items(), key=lambda kv: -kv[1]):
        out.append(f"| `{f}` | {kind} | {n} |")
    out.append("\n**2. Ring atoms as deposited** — 5-membered rings carrying ≥2 N\n")
    if not e["rings"]:
        out.append("*(none detected)*")
    else:
        out.append("| ring composition | rings |")
        out.append("|---|---:|")
        for sig, g in sorted(e["rings"].items(), key=lambda kv: -kv[1]["count"]):
            out.append(f"| `{sig}` | {g['count']} |")
        out.append("\n**3. Protonation-relevant bond environments, per ring nitrogen**\n")
        out.append("| ring | N degree | metal-bound | exocyclic H | exocyclic C | count |")
        out.append("|---|---:|---|---|---|---:|")
        for sig, g in sorted(e["rings"].items(), key=lambda kv: -kv[1]["count"]):
            for (deg, m, h, c), n in sorted(g["envs"].items(), key=lambda kv: -kv[1]):
                out.append(f"| `{sig}` | {deg} | {'yes' if m else 'no'} | {'**yes**' if h else 'no'} "
                           f"| {'**yes**' if c else 'no'} | {n} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", action="append", required=True)
    ap.add_argument("--stem", action="append", required=True)
    a = ap.parse_args()
    for stem in a.stem:
        path = None
        for d in a.db:
            p = os.path.join(d, stem + ".cif")
            if os.path.exists(p): path = p; break
        if not path:
            print(f"### `{stem}`\n\n*(not found)*\n"); continue
        print(render(stem, evidence(path)) + "\n")


if __name__ == "__main__":
    main()
