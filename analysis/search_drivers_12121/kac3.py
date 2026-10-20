"""12125a: every order-3 element lambda/3 (lambda in E8 mod 3E8) restricted to the so(10) of each three-generation base model:
fixed subalgebra types inside so(10)."""
import sys, itertools, json
import numpy as np
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings()
R = g.R
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
lams = np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
integ = lambda a: np.abs(a - np.round(a)) < 1e-9
res = {}
for base in ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    vec = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
    gauge = integ(R @ vec[0]) & integ(R @ vec[1]) & integ(R @ vec[3])
    d5 = next(c for c in g.comps(gauge) if len(c) == 40)
    m10 = np.zeros(240, bool); m10[d5] = True
    P = R[d5] @ lams.T / 3  # 40 x 6561
    fix = integ(P)
    types = Counter()
    for j in range(lams.shape[0]):
        mask = np.zeros(240, bool); mask[np.array(d5)[fix[:, j]]] = True
        types[g.typ(mask)] += 1
    res[base] = {' + '.join(k) if k else 'u(1)^5': v for k, v in types.items()}
    print(base, res[base], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\kac3.json', 'w'), indent=1)
