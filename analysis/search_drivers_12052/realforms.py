"""Real forms of E8 as configurations on the forty W(3,3) points (via the 6:1 fibration of Pass 1021)."""
import itertools
from collections import Counter

import numpy as np

# E8 roots (even coordinate system)
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si in (1, -1):
        for sj in (1, -1):
            v = np.zeros(8); v[i] = si; v[j] = sj; roots.append(v)
for signs in itertools.product((0.5, -0.5), repeat=8):
    if sum(1 for s in signs if s < 0) % 2 == 0:
        roots.append(np.array(signs))
R = np.array(roots)
assert len(R) == 240
# simple roots (Bourbaki-like for this lattice)
simple = [np.array(v, float) for v in (
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0])]
G = np.array([[a @ b for b in simple] for a in simple])
assert np.allclose(np.diag(G), 2) and abs(np.linalg.det(G) - 1) < 1e-9
refl = lambda a: np.eye(8) - np.outer(a, a)  # noqa: E731  (norm 2)
C = np.eye(8)
for a in simple:
    C = C @ refl(a)
order = next(k for k in range(1, 100) if np.allclose(np.linalg.matrix_power(C, k), np.eye(8)))
assert order == 30
C5 = np.linalg.matrix_power(C, 5)
key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
img = [key[tuple(np.round((C5 @ r) * 2).astype(int))] for r in R]
fib, seen = [], set()
for i in range(240):
    if i in seen:
        continue
    orb, j = [], i
    while j not in orb:
        orb.append(j); j = img[j]
    seen |= set(orb); fib.append(orb)
assert len(fib) == 40 and all(len(f) == 6 for f in fib)
pt = np.empty(240, int)
for p, f in enumerate(fib):
    pt[f] = p
# collinearity: classify point pairs by the multiset of inner products between fibres
IP = R @ R.T
rel = {}
for p in range(40):
    for q in range(p + 1, 40):
        rel[(p, q)] = tuple(sorted(Counter(np.round(IP[np.ix_(fib[p], fib[q])].ravel()).astype(int)).items()))
cls = Counter(rel.values())
deg = {c: 2 * n / 40 for c, n in cls.items()}
print('pair classes (degree):', {str(k): v for k, v in deg.items()})
adjc = next(c for c, d in deg.items() if d == 12)
Adj = np.zeros((40, 40), int)
for (p, q), c in rel.items():
    if c == adjc:
        Adj[p, q] = Adj[q, p] = 1
ev = np.round(np.linalg.eigvalsh(Adj), 6)
print('collinearity spectrum:', Counter(ev))

# inner involutions h in E8 / 2E8: h ranges over lattice vectors mod 2; use representatives: 0, roots, norm-4 vectors
lat_reps = {}
cand = list(R) + [R[i] + R[j] for i in range(240) for j in range(i + 1, 240) if abs(IP[i, j]) < 1e-9]
for h in cand:
    sig = tuple(((np.round(R @ h).astype(int)) % 2).tolist())     # parity of <h, alpha> on all roots
    if sig not in lat_reps:
        lat_reps[sig] = h
print('distinct nontrivial involution classes:', len(lat_reps))
stats = Counter()
configs = {'clock': [], 'split': []}
for sig, h in lat_reps.items():
    s = np.array(sig)
    even = 240 - s.sum()
    dimk = 8 + even
    form = 'clock' if dimk == 136 else ('split' if dimk == 120 else str(dimk))
    n0 = [p for p in range(40) if s[fib[p]].sum() == 0]
    pattern = Counter(int(s[fib[p]].sum()) for p in range(40))
    stats[(form, len(n0), tuple(sorted(pattern.items())))] += 1
    configs[form].append(n0)
for k, v in stats.items():
    print(k, 'x', v)
# geometry of the even sets
for form, sets in configs.items():
    S = sets[0]
    sub = Adj[np.ix_(S, S)]
    common = [int(np.all(Adj[S].sum(0) == 0)) for _ in [0]]
    nbr_of = [p for p in range(40) if set(np.nonzero(Adj[p])[0]) == set(S)]
    print(form, 'n0 =', len(S), ' induced edges:', sub.sum() // 2, ' induced degrees:', Counter(sub.sum(0)),
          ' is the neighbourhood of point(s):', nbr_of, ' distinct sets among class:', len({tuple(x) for x in sets}))
np.save('rf_adj.npy', Adj)
