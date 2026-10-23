"""12218: SM_2751 (the only Z6-II W(3,3) Standard Model with all three generations unpaired, as an untwisted family triplet):
unbroken untwisted gauge roots of E8 x E8 with the actual Wilson lines and with W5 and/or W6 set to zero.  A root survives iff its
products with the Z6 shift and every Wilson line are integral.  Reports the root-system type (component sizes and ranks)."""
import itertools, json, sys
import numpy as np
from fractions import Fraction as F
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings(); R8 = g.R
R = np.vstack([np.hstack([R8, np.zeros_like(R8)]), np.hstack([np.zeros_like(R8), R8])])
V = np.array([float(F(x)) for x in "0 0 0 0 0 1/6 1/3 1/2 0 0 0 0 1/6 1/6 1/6 1/2".split()])
W5 = np.array([float(F(x)) for x in "-1/4 -1/4 1/4 1/4 1/4 -1/4 -3/4 3/4 -1/4 -1/4 3/4 3/4 -3/4 1/4 9/4 -3/4".split()])
W6 = np.array([float(F(x)) for x in "-2 -3/2 -1 1/2 1 2 0 1 5/4 5/4 -5/4 9/4 -5/4 -1/4 -5/4 -3/4".split()])
integ = lambda a: np.abs(a - np.round(a)) < 1e-9


def rtype(mask):
    idx = np.nonzero(mask)[0]
    Rm = R[idx]
    G = np.abs(Rm @ Rm.T) > 1e-9
    seen, comps = set(), []
    for s in range(len(idx)):
        if s in seen: continue
        stack, comp = [s], []
        seen.add(s)
        while stack:
            a = stack.pop(); comp.append(a)
            for b in np.nonzero(G[a])[0]:
                if b not in seen:
                    seen.add(b); stack.append(b)
        rank = np.linalg.matrix_rank(Rm[comp])
        comps.append((len(comp), int(rank)))
    names = {(2, 1): 'A1', (6, 2): 'A2', (12, 3): 'A3', (20, 4): 'A4', (30, 5): 'A5', (42, 6): 'A6', (56, 7): 'A7', (24, 4): 'D4',
             (40, 5): 'D5', (60, 6): 'D6', (84, 7): 'D7', (112, 8): 'D8', (72, 6): 'E6', (126, 7): 'E7', (12, 2): 'G2', (240, 8): 'E8'}
    return sorted(names.get(c, str(c)) for c in comps)


out = {}
for name, ws in (('actual', [W5, W6]), ('W5=0', [W6]), ('W6=0', [W5]), ('W5=W6=0', [])):
    m = integ(R @ V)
    for w in ws:
        m &= integ(R @ w)
    out[name] = dict(roots=int(m.sum()), type=rtype(m))
    print(name, out[name])
json.dump(out, open('roots2751.json', 'w'), indent=1)
