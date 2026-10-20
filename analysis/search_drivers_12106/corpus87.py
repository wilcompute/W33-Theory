import sys
import re
import subprocess
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings

g = Gradings()
R = g.R
kind = {s.tobytes(): k for k, s in zip(g.kinds, g.vecs)}
files = subprocess.run(['wsl', '-e', 'bash', '-lc', 'ls ~/orb/ns87/models/*.txt'], capture_output=True, text=True).stdout.split()
models = []
for f in files:
    t = subprocess.run(['wsl', '-e', 'cat', f], capture_output=True, text=True).stdout
    for blk in t.split('begin model')[1:]:
        rows = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
        vec = [[Fr(x.strip()) for x in r.split(',')] for r in rows]
        models.append(vec)
print('models', len(models))


def z2class(v8):
    a = np.array([float(x) for x in v8])
    par = np.round(2 * (R @ a)).astype(int) % 2 == 1
    if not par.any():
        return 'trivial'
    return kind.get(par.tobytes(), 'other')


def z3fixed(v8):
    a = np.array([float(x) for x in v8])
    ph = np.round(3 * (R @ a)).astype(int) % 3
    keep = ph == 0
    return g.typ(keep)


tab = Counter()
for vec in models:
    V = vec[0]
    W = vec[6]
    key = []
    for part in (slice(0, 8), slice(8, 16)):
        V3 = [3 * x for x in V[part]]          # Z2 part (order-2 element)
        V2 = [2 * x for x in V[part]]          # Z3 part
        key.append((z2class(V3), z3fixed(V2), z3fixed([w for w in W[part]])))
    tab[tuple(key)] += 1
for k, v in tab.most_common():
    print(v, k)
uniq = {tuple(tuple(r) for r in m) for m in models}
print('distinct models', len(uniq))
tabu = Counter()
for m in uniq:
    V, W = m[0], m[6]
    key = tuple(z2class([3 * x for x in V[p]]) for p in (slice(0, 8), slice(8, 16)))
    wl = tuple(z3fixed(list(W[p])) for p in (slice(0, 8), slice(8, 16)))
    tabu[(tuple(sorted(key)), wl)] += 1
print(dict(tabu))
