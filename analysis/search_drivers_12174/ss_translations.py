"""12177 driver: Scherk-Schwarz (order-2 translation) obstruction.  A Z2 translation t in (1/2)Lambda commuting with the point
group mod Lambda exists iff the generators' integer matrices M_g have a common nonzero kernel of (M_g - 1) over F2.  For a cyclic
group the kernel is nonzero iff det(1 - theta) (= number of theta fixed points on T6) is even."""
import glob, json, os, re, sys
from fractions import Fraction
import numpy as np
from sympy import Matrix, GF
from sympy.polys.matrices import DomainMatrix

D = os.path.dirname(os.path.abspath(__file__))


def parse(path):
    s = open(path).read().split("\n")
    tw, lat, i = [], [], 0
    while i < len(s):
        if s[i].strip() == "begin twist":
            i += 1
            while s[i].strip() != "end twist":
                tw.append([Fraction(x) for x in s[i].replace(",", " ").split()][1:])
                i += 1
        if s[i].strip() == "next lattice vector":
            lat.append([float(s[i + k]) for k in range(1, 7)])
            i += 6
        i += 1
    return tw, np.array(lat).T


def rot(v):
    R = np.zeros((6, 6))
    for k, a in enumerate(v):
        c, s = np.cos(2 * np.pi * float(a)), np.sin(2 * np.pi * float(a))
        R[2 * k:2 * k + 2, 2 * k:2 * k + 2] = [[c, -s], [s, c]]
    return R


def analyse(path):
    tw, B = parse(path)
    mats, err = [], 0.0
    for v in tw:
        M = np.linalg.solve(B, rot(v) @ B)
        err = max(err, float(np.abs(M - np.round(M)).max()))
        mats.append(np.round(M).astype(int))
    stack = np.vstack([(M - np.eye(6, dtype=int)) % 2 for M in mats])
    dm = DomainMatrix.from_Matrix(Matrix(stack.tolist())).convert_to(GF(2))
    ker = 6 - dm.rank()
    dets = [int(round(np.linalg.det(np.eye(6) - M))) for M in mats]
    return dict(twists=[[str(x) for x in v] for v in tw], integrality_error=err, det_1_minus_theta=dets, ss_kernel_dim=ker)


if __name__ == "__main__":
    out = {}
    for f in sorted(glob.glob(os.path.join(D, "geometry", "Geometry_Z*.txt"))):
        name = os.path.basename(f)[9:-4]
        try:
            out[name] = analyse(f)
        except Exception as e:
            out[name] = dict(error=repr(e))
        print(name, out[name])
    json.dump(out, open(os.path.join(D, "ss_translations.json"), "w"), indent=1)
