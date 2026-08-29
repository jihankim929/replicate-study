"""Add framework density to the manifest and reorder the s1 task files by it.

Volumetric uptake rises as framework density falls, so ascending density is a
free prior on where the high-capacity materials are. Reordering costs nothing
scientifically -- the screen is still exhaustive if it finishes -- but if the
queue starves it, the part that ran is the part that mattered.
"""
import os, sys, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cifutil

WS = os.path.dirname(HERE)
MASS = {
 "H":1.008,"He":4.003,"Li":6.94,"Be":9.012,"B":10.811,"C":12.011,"N":14.007,
 "O":15.999,"F":18.998,"Na":22.990,"Mg":24.305,"Al":26.982,"Si":28.086,
 "P":30.974,"S":32.06,"Cl":35.45,"K":39.098,"Ca":40.078,"Sc":44.956,
 "Ti":47.867,"V":50.942,"Cr":51.996,"Mn":54.938,"Fe":55.845,"Co":58.933,
 "Ni":58.693,"Cu":63.546,"Zn":65.38,"Ga":69.723,"Ge":72.63,"As":74.922,
 "Se":78.971,"Br":79.904,"Rb":85.468,"Sr":87.62,"Y":88.906,"Zr":91.224,
 "Nb":92.906,"Mo":95.95,"Ru":101.07,"Rh":102.91,"Pd":106.42,"Ag":107.87,
 "Cd":112.41,"In":114.82,"Sn":118.71,"Sb":121.76,"Te":127.60,"I":126.90,
 "Cs":132.91,"Ba":137.33,"La":138.91,"Ce":140.12,"Pr":140.91,"Nd":144.24,
 "Sm":150.36,"Eu":151.96,"Gd":157.25,"Tb":158.93,"Dy":162.50,"Ho":164.93,
 "Er":167.26,"Tm":168.93,"Yb":173.05,"Lu":174.97,"Hf":178.49,"Ta":180.95,
 "W":183.84,"Re":186.21,"Os":190.23,"Ir":192.22,"Pt":195.08,"Au":196.97,
 "Hg":200.59,"Tl":204.38,"Pb":207.2,"Bi":208.98,"Th":232.04,"U":238.03,
 "Np":237.0,"Pu":244.0,"Am":243.0,
}


def densities():
    rows = list(csv.DictReader(open(os.path.join(WS, "manifests/structures.csv"))))
    out = []
    for r in rows:
        d = cifutil.parse_cif(os.path.join(WS, "db", r["cif"] + ".cif"))
        m = sum(MASS.get(a[0], 0.0) for a in d["atoms"])
        rho = m / 6.02214076e23 / (float(r["volume"]) * 1e-24)   # g/cm3
        out.append((int(r["id"]), r["cif"], rho))
    return out


if __name__ == "__main__":
    import multiprocessing as mp
    dens = densities()
    with open(os.path.join(WS, "manifests/density.csv"), "w") as f:
        f.write("id,cif,density_gcm3\n")
        for i, n, rho in dens:
            f.write("%d,%s,%.4f\n" % (i, n, rho))
    order = [i for i, n, rho in sorted(dens, key=lambda x: x[2])]
    nch = 11
    for k in range(nch):
        p = os.path.join(WS, "jobs", "s1_%02d.tasks" % k)
        with open(p, "w") as f:
            for i in order[k::nch]:
                f.write("%d,6500000,200,500,1\n" % i)
    rr = [x[2] for x in sorted(dens, key=lambda x: x[2])]
    n = len(rr)
    print("density g/cm3  min %.3f  p10 %.3f  p50 %.3f  p90 %.3f  max %.3f"
          % (rr[0], rr[n//10], rr[n//2], rr[9*n//10], rr[-1]))
    print("task files reordered by ascending density, interleaved over %d chunks" % nch)
