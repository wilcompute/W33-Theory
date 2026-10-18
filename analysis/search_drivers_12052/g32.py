"""Witting group G32 = 3 x Sp(4,3) acting on the E8 roots; census of fixed real-form involutions per element."""
import itertools
import pickle
from collections import Counter, defaultdict

import numpy as np

exec(open('realforms.py').read().split('# inner involutions')[0])   # roots R, fib, Adj, C
W3 = np.linalg.matrix_power(C, 10)                     # omega: regular element of order 3
assert np.allclose(np.linalg.matrix_power(W3, 3), np.eye(8))
refl = lambda a: np.eye(8) - np.outer(a, a)  # noqa: E731
gens = []
for f in fib:
    a = R[f[0]]
    b = W3 @ a
    g = refl(a) @ refl(b)                               # rotation of order 3 in the A2 plane of the Eisenstein line
    assert np.allclose(g @ W3, W3 @ g)
    if not np.allclose(np.linalg.matrix_power(g, 3), np.eye(8)):
        g = refl(a) @ refl(W3 @ W3 @ a)
    gens.append(g)
key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
perm = lambda M: tuple(key[tuple(np.round((M @ r) * 2).astype(int))] for r in R)  # noqa: E731
gp = [perm(g) for g in gens]
# BFS over root permutations
start = tuple(range(240))
seen = {start}
frontier = [start]
while frontier:
    nxt = []
    for p in frontier:
        for g in gp:
            q = tuple(g[i] for i in p)
            if q not in seen:
                seen.add(q); nxt.append(q)
    frontier = nxt
    print('group size so far', len(seen), flush=True)
G = list(seen)
print('|G| =', len(G))
pickle.dump(G, open('g32_perms.pkl', 'wb'))
