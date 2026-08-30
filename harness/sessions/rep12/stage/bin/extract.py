"""Pull the reported quantities out of one RASPA output file into one CSV line.

Charter s4 forbids reading raw simulation output into the session; this is the
parser that stands in for that.  Everything downstream reads the CSV.
"""
import re, sys

PAT_V = re.compile(r"Average loading absolute \[cm\^3 \(STP\)/cm\^3 framework\]\s+([-\d.eE+]+)\s*\+/-\s*([-\d.eE+]+)")
PAT_M = re.compile(r"Average loading absolute \[mol/kg framework\]\s+([-\d.eE+]+)\s*\+/-\s*([-\d.eE+]+)")
PAT_N = re.compile(r"Average loading absolute \[molecules/unit cell\]\s+([-\d.eE+]+)")
PAT_VER = re.compile(r"^RASPA (\S+)")
PAT_CUT = re.compile(r"CutOff VDW : ([\d.]+)")


def main():
    path, tag, cif, press, ncyc, ninit, gspc, sec = sys.argv[1:9]
    v = m = nm = None
    ve = me = None
    ver = cut = None
    unshift = tail_ok = True
    nunknown = 0
    with open(path) as f:
        for line in f:
            r = PAT_V.search(line)
            if r:
                v, ve = float(r.group(1)), float(r.group(2))
            r = PAT_M.search(line)
            if r:
                m, me = float(r.group(1)), float(r.group(2))
            r = PAT_N.search(line)
            if r:
                nm = float(r.group(1))
            r = PAT_VER.match(line)
            if r and ver is None:
                ver = r.group(1)
            r = PAT_CUT.search(line)
            if r and cut is None:
                cut = r.group(1)
            if "tailcorrection: yes" in line:
                tail_ok = False
            if "All potentials are shifted" in line:
                unshift = False
    status = "OK"
    if v is None:
        status = "NOVALUE"
    if ver != "2.0.37" or cut != "12.800000" or not tail_ok or not unshift:
        status = "PROTOCOL_MISMATCH:%s/%s/%s/%s" % (ver, cut, tail_ok, unshift)
    print("%s,\"%s\",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
        tag, cif, press, ncyc, ninit, gspc,
        "" if v is None else "%.4f" % v, "" if ve is None else "%.4f" % ve,
        "" if m is None else "%.5f" % m, "" if me is None else "%.5f" % me,
        "" if nm is None else "%.3f" % nm, sec, status))


if __name__ == "__main__":
    main()
