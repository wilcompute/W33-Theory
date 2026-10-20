"""12124: the second Wilson line read in W(3,3): is the colour A2 an event fibre (6:1 fibration 240 roots -> 40 points)?
where do SU(2)_L, SU(2)_R sit? baseline over all 2160 left-right order-3 elements of each base so(10)."""
import sys, itertools, json
import numpy as np
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings()
R, fib = g.R, g.fib
ptof = {i: x for x in range(40) for i in fib[x]}
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
lams = np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE
integ = lambda a: np.abs(a - np.round(a)) < 1e-9


def rows_of(path):
    rows = open(path).read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    return [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]


def describe(mask):
    cs = g.comps(mask)
    a2 = [c for c in cs if len(c) == 6]
    a1 = [c for c in cs if len(c) == 2]
    a2fib = [len({ptof[i] for i in c}) == 1 for c in a2]
    # A1 pair: both roots in one fibre always (fibre contains -alpha); record the fibre points of the A1s and whether
    # they meet the colour fibre point / are collinear in W(3,3)
    pts = [ptof[c[0]] for c in a1]
    return a2fib, pts, [ptof[c[0]] for c in a2]


res = {}
D11 = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
D16 = r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl'
for m in ['N004_F1_03_S002', 'N008_F1_03_S033', 'N008_F1_04_S037', 'N008_F1_02_S053']:
    v = rows_of(D16 + '/' + m + '.txt')
    gauge10 = integ(R @ v[0]) & integ(R @ v[1]) & integ(R @ v[3])
    d5 = next(c for c in g.comps(gauge10) if len(c) == 40)
    m10 = np.zeros(240, bool); m10[d5] = True
    actual = m10 & integ(R @ v[5])
    a2fib, pts, cpts = describe(actual)
    # baseline: all lambda giving A1+A1+A2 in this so(10)
    P = integ(R[d5] @ lams.T / 3)
    base = Counter()
    for j in range(lams.shape[0]):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) == ('A1', 'A1', 'A2'):
            f, p, c = describe(mk)
            base['colour A2 is a fibre' if f[0] else 'colour A2 not a fibre'] += 1
            base['A1s same point' if p[0] == p[1] else 'A1s distinct points'] += 1
    res[m] = dict(type=g.typ(actual), colour_is_fibre=a2fib, A1_points=pts, colour_points=cpts, baseline=dict(base))
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\wl2w33.json', 'w'), indent=1, default=str)
