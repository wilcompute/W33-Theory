import sys
import itertools
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings

g = Gradings()
R, fib = g.R, g.fib
ptof = {i: x for x in range(40) for i in fib[x]}
key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
for base in ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']:
    t = open(D + '\\' + base + '_9.txt').read()
    rows = t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    vec = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
    V0, V1, W = vec[0], vec[1], vec[3]
    frac = lambda x: (x - np.round(x))  # noqa: E731
    pV0, pV1, pW = R @ V0, R @ V1, R @ W
    integral = lambda a: np.abs(a - np.round(a)) < 1e-9  # noqa: E731
    gauge = integral(pV0) & integral(pV1) & integral(pW)
    comps = g.comps(gauge)
    d5 = next(c for c in comps if len(c) == 40)
    Bd = np.linalg.svd(R[d5])[2][:5]
    proj = np.array([np.sum((Bd @ R[a]) ** 2) for a in range(240)])
    ph13 = np.abs(((pV1 % 1) - 1 / 3)) < 1e-9
    sig_odd = np.abs((pV0 % 1) - 0.5) < 1e-9
    fer16 = [a for a in range(240) if ph13[a] and sig_odd[a] and integral(pW[a]) and np.isclose(proj[a], 1.25)]
    bos10 = [a for a in range(240) if ph13[a] and not sig_odd[a] and integral(pW[a]) and np.isclose(proj[a], 1.0)]
    trip = 0
    S = set(bos10)
    for a, b in itertools.combinations_with_replacement(fer16, 2):
        c = key.get(tuple(np.round(-(R[a] + R[b]) * 2).astype(int)))
        if c is not None and c in S:
            trip += 1
    # family a2 of the shift (first E8 part of V1)
    ph = np.round(3 * pV1).astype(int) % 3
    fam = next(c for c in g.comps(ph == 0) if len(c) == 6)
    fpts = {ptof[i] for i in fam}
    print(base, '16-fermion roots', len(fer16), ' 10-scalar roots', len(bos10), ' 16.16.10 root triples', trip,
          ' family a2 event fibre:', len(fpts) == 1)
