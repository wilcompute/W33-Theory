import sys
import glob
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
from w33_pass12053_gate_sets_and_real_forms import setup

g = Gradings()
R, fib = g.R, g.fib
Adj, invs, tick, _ = setup()
ptof = {i: x for x in range(40) for i in fib[x]}
key = {s.tobytes(): h for h, s in enumerate(g.vecs)}
ev = {h: frozenset(x for x in range(40) if not g.vecs[h][fib[x]].any()) for h in range(g.n)}
cpt = {h: next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(ev[h])) for h in range(g.n) if g.kinds[h] == 'clock'}
models = set()
for f in sorted(glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12109\susy_*.txt')):
    t = open(f).read()
    for blk in t.split('begin model')[1:]:
        rws = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
        models.add(tuple(tuple(Fr(x.strip()) for x in r.split(',')) for r in rws))


def cls(v8):
    a = np.array([float(x) for x in v8])
    par = np.round(2 * (R @ a)).astype(int) % 2 == 1
    return key.get(par.tobytes())


def fam_event(v8):
    a = np.array([float(x) for x in v8])
    ph = np.round(3 * (R @ a)).astype(int) % 3
    comps = g.comps(ph == 0)
    a2 = next((c for c in comps if len(c) == 6), None)
    if a2 is None:
        return None
    pts = {ptof[i] for i in a2}
    return next(iter(pts)) if len(pts) == 1 else 'nonfibre'


tab = Counter()
for m in models:
    V, W = m[0], m[6]
    parts = {}
    for name, sl in (('A', slice(0, 8)), ('B', slice(8, 16))):
        h = cls([3 * x for x in V[sl]])
        parts[name] = (h, fam_event(list(W[sl])))
    clock_side = next(n for n in parts if g.kinds[parts[n][0]] == 'clock')
    split_side = 'B' if clock_side == 'A' else 'A'
    x = cpt[parts[clock_side][0]]
    F = ev[parts[split_side][0]]
    wc, ws = parts[clock_side][1], parts[split_side][1]
    rel = ('x in F' if x in F else 'x not in F',
           'clock-side WL a2: ' + ('fibre of x' if wc == x else ('fibre (collinear to x)' if isinstance(wc, (int, np.integer)) and Adj[x, wc] else ('fibre (far)' if isinstance(wc, (int, np.integer)) else str(wc)))),
           'split-side WL a2: ' + ('fibre in F' if isinstance(ws, (int, np.integer)) and ws in F else ('fibre outside F' if isinstance(ws, (int, np.integer)) else str(ws))))
    tab[rel] += 1
for k, v in tab.most_common():
    print(v, k)
