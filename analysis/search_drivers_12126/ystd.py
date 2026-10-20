"""12126: the standard SO(10) hypercharge on the e6+a2 three-generation models. Y restricted to the Cartan of the parent so(10)
(first E8), orthogonal to SU(3)_c and SU(2)_L; exotics may carry any charge as long as they are vector-like."""
import sys
import json
import itertools
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
import sympy as sp

sys.path.insert(0, r'C:\tmp\toe_round\stype')
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import hyper as H
from w33_pass12087_standard_model_sectors import Gradings

g = Gradings()
R = g.R
integ = lambda a: np.abs(a - np.round(a)) < 1e-9  # noqa: E731
DM = {'N004_F1_03_S002': r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl',
      'N008_F1_03_S033': r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl',
      'N008_F1_04_S037': r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl',
      'N008_F1_02_S053': r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl',
      'N008_F1_04_S037_T115': r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3'}


def rat(x):
    return sp.Rational(str(Fr(x).limit_denominator(720)))


def net_of(left, y, col, L):
    cnt = Counter()
    for f in left:
        dc, dl = H.dsgn(f['dim'][col]), int(f['dim'][L])
        ys = Counter(H.dot(y, w) for w in f['W'])
        for Y, k in ys.items():
            cnt[(dc, dl, Y)] += k // (abs(dc) * dl)
    net, done = {}, set()
    for key in cnt:
        if key in done:
            continue
        dc, dl, Y = key
        conj = ((-dc if abs(dc) == 3 else dc), dl, -Y)
        done |= {key, conj}
        if key == conj:
            continue
        d = cnt.get(key, 0) - cnt.get(conj, 0)
        if d:
            net[key if d > 0 else conj] = abs(d)
    return net


res = {}
for m, d in DM.items():
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    left = r['left']
    rows = open(d + '\\' + m + '.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in row.split()[:8]]) for row in rows]
    d5 = next(c for c in g.comps(integ(R @ v[0]) & integ(R @ v[1]) & integ(R @ v[3])) if len(c) == 40)
    Bd = sp.Matrix([[rat(x) for x in R[a]] for a in d5]).T.columnspace()  # so(10) Cartan in first E8 (8D)
    S = sp.Matrix.hstack(*Bd)  # 8 x 5
    cons = [list(fac[col][1][0][:8]), list(fac[col][1][1][:8]), list(fac[L][1][0][:8])]
    Cm = sp.Matrix([[rat(x) for x in c] for c in cons]) * S
    ns = Cm.nullspace()  # coefficients in S basis
    dirs = [S * n for n in ns]
    assert len(dirs) == 2, len(dirs)
    to16 = lambda vec: [Fr(str(x)) for x in list(vec)] + [Fr(0)] * 8  # noqa: E731
    D0, D1 = to16(dirs[0]), to16(dirs[1])
    # chiral Q: (3,2) fields with three RM weights; condition Y(Q) = 1/6
    q = next(f for f in left if abs(H.dsgn(f['dim'][col])) == 3 and int(f['dim'][L]) == 2 and len(f['W']) == 6 and sum(1 for g2 in left if g2['W'] == f['W']) == 3)
    sgn = 1 if H.dsgn(q['dim'][col]) > 0 else -1
    wq = q['W'][0]
    cands = set()
    trip = [f for f in left if abs(H.dsgn(f['dim'][col])) == 3 and int(f['dim'][L]) == 1]
    for f in trip:
        for w in set(f['W']):
            for target in (Fr(-2, 3), Fr(1, 3), Fr(2, 3), Fr(-1, 3)):
                a11, a12, a21, a22 = H.dot(D0, wq), H.dot(D1, wq), H.dot(D0, w), H.dot(D1, w)
                det = a11 * a22 - a12 * a21
                if det == 0:
                    continue
                r1, r2 = sgn * Fr(1, 6), target
                cands.add(((r1 * a22 - a12 * r2) / det, (a11 * r2 - a21 * r1) / det))
    a11, a12 = H.dot(D0, wq), H.dot(D1, wq)
    targets = [Fr(k, 6) for k in range(-12, 13)]
    for (A1, A2, r1) in ((a11, a12, sgn * Fr(1, 6)),):
        if A1 == 0 and A2 != 0:
            b0 = r1 / A2
            cands.add((Fr(0), b0))
            for f in left:
                for w in set(f['W']):
                    c0, c1 = H.dot(D0, w), H.dot(D1, w)
                    if c0 != 0:
                        for t in targets:
                            cands.add(((t - b0 * c1) / c0, b0))
        elif A2 == 0 and A1 != 0:
            a0 = r1 / A1
            cands.add((a0, Fr(0)))
            for f in left:
                for w in set(f['W']):
                    c0, c1 = H.dot(D0, w), H.dot(D1, w)
                    if c1 != 0:
                        for t in targets:
                            cands.add((a0, (t - a0 * c0) / c1))
    good = []
    for a_, b_ in cands:
        y = [a_ * x + b_ * z for x, z in zip(D0, D1)]
        net = net_of(left, y, col, L)
        if H.is_sm(net):
            tA = r['basis'][0]
            good.append(dict(y2=str(H.dot(y, y)), kY=str(2 * H.dot(y, y)), y=[str(t) for t in y], orth_anomalous=H.dot(y, tA) == 0))
    res[m] = dict(n_candidates=len(cands), n_sm=len(good), sm=good)
    print(m, 'candidates', len(cands), 'exact SM', len(good), [(s['kY'], s['orth_anomalous']) for s in good], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\ystd.json', 'w'), indent=1)
