import sys, json, itertools
import numpy as np
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_round\stype')
sys.argv = ['x']
exec(open(r'C:\tmp\toe_round\stype\wl2w33.py').read().split('res = {}')[0])
IP = g.IP
def collinear(x, y):
    return all(IP[a, b] == 0 for a in fib[x] for b in fib[y])
nb = [sum(collinear(0, y) for y in range(1, 40))]
print('neighbours of point 0 (orthogonal fibres):', nb)
out = {}
D16 = r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl'
for m in ['N004_F1_03_S002', 'N008_F1_03_S033', 'N008_F1_04_S037', 'N008_F1_02_S053']:
    v = rows_of(D16 + '/' + m + '.txt')
    gauge10 = integ(R @ v[0]) & integ(R @ v[1]) & integ(R @ v[3])
    d5 = next(c for c in g.comps(gauge10) if len(c) == 40)
    P = integ(R[d5] @ lams.T / 3)
    def lr(mk):
        a1 = [c for c in g.comps(mk) if len(c) == 2]
        return collinear(ptof[a1[0][0]], ptof[a1[1][0]])
    m10 = np.zeros(240, bool); m10[d5] = True
    act = lr(m10 & integ(R @ v[5]))
    base = Counter()
    for j in range(lams.shape[0]):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) == ('A1', 'A1', 'A2'):
            base[lr(mk)] += 1
    out[m] = dict(LR_collinear=act, baseline_collinear=base[True], baseline_total=base[True] + base[False])
    print(m, out[m], flush=True)
json.dump(out, open(r'C:\tmp\toe_round\stype\wl2col.json', 'w'), indent=1)
