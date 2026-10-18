import pickle
from collections import Counter, defaultdict

import numpy as np

exec(open('realforms.py').read().replace("print(", "(lambda *a, **k: None)("))   # rebuild R, fib, Adj, lat_reps
G = np.array(pickle.load(open('g32_perms.pkl', 'rb')), dtype=np.int16)
pt_of = np.empty(240, int)
for p, f in enumerate(fib):
    pt_of[f] = p
sigs = {'clock': [], 'split': []}
for sig, h in lat_reps.items():
    s = np.array(sig, bool)
    dimk = 8 + 240 - s.sum()
    sigs['clock' if dimk == 136 else 'split'].append(s)
S = {k: np.array(v) for k, v in sigs.items()}
fix = {}
for k, M in S.items():
    cnt = np.zeros(len(G), int)
    for s in M:
        cnt += np.all(s[G] == s[None, :], axis=1)
    fix[k] = cnt
# induced action on points
P = pt_of[G[:, [f[0] for f in fib]]]                     # image point of each fibre
fixpts = (P == np.arange(40)[None, :]).sum(1)
# element order on roots
def order(p):
    q, k = p.copy(), 1
    idn = np.arange(240)
    while not np.array_equal(q, idn):
        q = p[q]; k += 1
    return k
orders = np.array([order(g.astype(int)) for g in G])
# factorisations: the 45 split even-sets as sets of points
splitsets = []
for s in S['split']:
    st = frozenset(p for p in range(40) if not s[fib[p]].any())
    if st not in splitsets:
        splitsets.append(st)
assert len(splitsets) == 45
fixfact = np.zeros(len(G), int)
for st in splitsets:
    idx = np.array(sorted(st))
    fixfact += np.array([set(P[g, idx]) == st for g in range(len(G))])
table = defaultdict(Counter)
for g in range(len(G)):
    table[(int(orders[g]), int(fixpts[g]), int(fixfact[g]))][(int(fix['clock'][g]), int(fix['split'][g]))] += 1
rows = []
for k in sorted(table):
    rows.append((k, dict(table[k])))
    print('order %2d, fixed points %2d, fixed factorisations %2d ->' % k, {str(a): b for a, b in table[k].items()})
pickle.dump(dict(rows=rows, fix=fix, orders=orders, fixpts=fixpts, fixfact=fixfact), open('census.pkl', 'wb'))
tot = len(G)
print('elements fixing >=1 clock involution:', int((fix['clock'] > 0).sum()), ' >=1 split:', int((fix['split'] > 0).sum()), ' of', tot)
print('fix clock but no split:', int(((fix['clock'] > 0) & (fix['split'] == 0)).sum()), ' fix split but no clock:', int(((fix['split'] > 0) & (fix['clock'] == 0)).sum()),
      ' neither:', int(((fix['split'] == 0) & (fix['clock'] == 0)).sum()))
