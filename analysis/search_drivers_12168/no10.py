"""12170: no untwisted 10_H, exhaustively: for each of the 7 e6+a2 base models and every one of the 864 A4-type order-3 lambda (12125),
the untwisted scalars of the first E8 (roots alpha with V1.alpha = 1/3 or 2/3 mod 1, Wf.alpha and W2.alpha integral, V0.alpha
integral = boson under the split parity) grouped into SU(5) multiplets (by the component orthogonal to the unbroken A4):
are any of size 10? Control: the same count for FERMIONS (V0.alpha half-integral) must find the 10s of the generations."""
import sys, json, itertools
import numpy as np
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings(); R = g.R
SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = np.array(list(itertools.product(range(3), repeat=8)))
L3 = (coefs @ SIMPLE) / 3
integ = lambda a: np.abs(a - np.round(a)) < 1e-9
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
out = {}
for base in ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
    V0, V1, Wf = v[0], v[1], v[3]
    pV0, pV1, pWf = R @ V0, R @ V1, R @ Wf
    gauge10 = integ(pV0) & integ(pV1) & integ(pWf)
    d5 = next(c for c in g.comps(gauge10) if len(c) == 40)
    P = integ(R[d5] @ L3.T)
    matter = (~integ(pV1)) & integ(3 * pV1) & integ(pWf)
    stats = Counter()
    for j in range(len(coefs)):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) != ('A4',):
            continue
        a4 = np.nonzero(mk)[0]
        B = np.linalg.svd(R[a4])[2][:4]                         # A4 Cartan span
        pW2 = R @ L3[j]
        for kind, sel in (('scalar', integ(pV0)), ('fermion', ~integ(pV0))):
            cand = np.nonzero(matter & integ(pW2) & sel)[0]
            if len(cand) == 0:
                stats[(kind, 'none')] += 1
                continue
            perp = R[cand] - (R[cand] @ B.T) @ B
            keys = Counter(tuple(np.round(p * 12).astype(int)) for p in perp)
            sizes = Counter(keys.values())
            stats[(kind, 'has10')] += int(10 in sizes)
            stats[(kind, 'sizes:' + ','.join(str(s) for s in sorted(sizes)))] += 1
        stats['models'] += 1
    out[base] = {str(k): v_ for k, v_ in stats.items()}
    print(base, dict(stats), flush=True)
json.dump(out, open('no10.json', 'w'), indent=1)
print('DONE')
