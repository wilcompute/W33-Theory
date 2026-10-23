"""12212: twisted 10s by lattice computation (necessary condition, no projection phases).  For each saved SU(5) x U(1) model of
the e6+a2 route (Passes 12161-12182): SU(5) = the A4 component of the first-E8 roots invariant under every shift and Wilson
line; for all 27 fixed-point shifts V_f = V1 + n1 W(t1) + n2 W(t2) + n3 W(t3) and their Witten partners V_f + V0, enumerate
vectors of Gamma + V_f with norm exactly 4/3 (the oscillator-free massless shell; with one oscillator the shell is 2/3 < 6/5)
and count those whose SU(5) projection has norm 6/5 (10-type weights).  Control: the same count on the untwisted shell
(roots, norm 2, Witten-untwisted) must find the generation 10s."""
import glob, os, itertools, json, re, sys
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
sys.path.insert(0, r'C:\tmp\toe_wt\analysis\search_drivers_12174')
from w33_pass12087_standard_model_sectors import Gradings
from tenD import e8_vectors

g = Gradings(); R = g.R
E8 = e8_vectors(10)
integ = lambda a: np.abs(a - np.round(a)) < 1e-9


def coset_vectors(V8, maxn):
    P = E8 + V8
    n = (P * P).sum(1)
    k = n <= maxn + 1e-9
    return P[k], n[k]


def analyse(path, v=None):
    if v is None:
        t = open(path).read()
        rows = t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
        v = [np.array([float(Fr(x)) for x in r.replace(',', ' ').split()[:16]]) for r in rows]
    V0, V1, Wt = v[0], v[1], [v[3], v[5], v[7]]
    first = np.ones(240, bool)
    for s in [V0, V1] + Wt:
        first &= integ(R @ s[:8])
    comps = [c for c in g.comps(first) if len(c) == 20]
    if len(comps) != 1:
        return None
    A = R[comps[0]]
    B = np.linalg.svd(A)[2][:4]
    hits = 0
    for ns in itertools.product(range(3), repeat=3):
        Vf = V1 + sum(n * w for n, w in zip(ns, Wt))
        for W in (Vf, Vf + V0):
            P1, n1 = coset_vectors(W[:8], 4 / 3)
            P2, n2 = coset_vectors(W[8:], 4 / 3)
            for i, a in enumerate(n1):
                rest = 4 / 3 - a
                j = np.nonzero(np.abs(n2 - rest) < 1e-9)[0]
                if len(j) == 0:
                    continue
                proj = P1[i] @ B.T
                if abs(proj @ proj - 6 / 5) < 1e-9:
                    hits += len(j)
    # control: untwisted 10-type roots with integral V1/WL products are the generation 10s (fermions under V0)
    ctrl = sum(1 for k in range(240) if abs((R[k] @ B.T) @ (R[k] @ B.T) - 6 / 5) < 1e-9)
    return dict(twisted_10_type_vectors=hits, control_untwisted_10_type_roots=ctrl)


def main():
    res = {}
    for f in sorted(glob.glob(r'C:\tmp\toe_round\stype\flipscan2\*.txt')):
        o = f[:-4] + '.out'
        try:
            txt = open(o).read()
        except OSError:
            continue
        if 'A4' not in txt.split('GAUGE')[-1].split('\n')[0] if 'GAUGE' in txt else True:
            continue
        r = analyse(f)
        if r:
            res[os.path.basename(f)[:-4]] = r
    print('models', len(res), 'with twisted 10-type vectors:', sum(1 for r in res.values() if r['twisted_10_type_vectors']),
          'control min/max', min(r['control_untwisted_10_type_roots'] for r in res.values()), max(r['control_untwisted_10_type_roots'] for r in res.values()))
    json.dump(res, open('twisted10.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
