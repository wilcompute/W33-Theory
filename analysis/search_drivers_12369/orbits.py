"""12371b: orbits of Sp(4,3) (symplectic transvections preserving omega) on the 16848 light cones kappa, acting by
kappa -> C(h) kappa C(h)^{-1}, C(h) = second compound (action on bivectors, same basis/order as 12369).  Records orbit sizes with the
second invariant G2(omega, omega) and the common-context count of a representative.  Control: |Sp(4,3)| = 51840 from BFS on V."""
import itertools, json, collections
import numpy as np
p = 3
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)
pairs = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]
def comp2(h):
    return np.array([[(h[a, c] * h[b, d] - h[a, d] * h[b, c]) % p for (c, d) in pairs] for (a, b) in pairs], dtype=np.int64)
def transvection(v):
    v = np.array(v, dtype=np.int64)
    # T(x) = x + omega(x, v) v ; matrix columns T(e_i)
    return (np.eye(4, dtype=np.int64) + np.outer(v, (Om @ v) % p * 0 + (np.array([int(e @ Om @ v) for e in np.eye(4, dtype=np.int64)])))) % p
gens = [transvection(v) for v in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1])]
for g in gens:
    assert ((g.T @ Om @ g - Om) % p == 0).all()
# group order control by BFS
seen = {np.eye(4, dtype=np.int64).tobytes()}; fr = [np.eye(4, dtype=np.int64)]
while fr:
    nf = []
    for x in fr:
        for g in gens:
            y = (g @ x) % p; b = y.tobytes()
            if b not in seen: seen.add(b); nf.append(y)
    fr = nf
print('|Sp(4,3)| =', len(seen))
K = np.load('allsols.npy'); key = {k.tobytes(): i for i, k in enumerate(K)}
Cs = [(comp2(g), comp2(np.array(np.round(np.linalg.inv(g) * round(np.linalg.det(g))) % p, dtype=np.int64))) for g in gens]
from sympy import Matrix
Cs = [(comp2(g), comp2(np.array(Matrix(g.tolist()).inv_mod(p), dtype=np.int64))) for g in gens]
w = np.array([0, 1, 0, 0, 2, 0], dtype=np.int64)
P = np.block([[np.zeros((3, 3), dtype=np.int64), np.eye(3, dtype=np.int64)], [np.eye(3, dtype=np.int64), np.zeros((3, 3), dtype=np.int64)]])
ex = json.load(open('kahler.json'))
lab = [-1] * len(K); orbs = []
for i in range(len(K)):
    if lab[i] >= 0: continue
    o = len(orbs); lab[i] = o; fr = [i]; size = 1
    while fr:
        nf = []
        for j in fr:
            for C, Ci in Cs:
                y = (C @ K[j] @ Ci) % p; t = key[y.tobytes()]
                if lab[t] < 0: lab[t] = o; nf.append(t); size += 1
        fr = nf
    orbs.append(dict(size=size, second_invariant=int(w @ P @ K[i] @ w) % p, stabilizer=51840 // size))
print(orbs)
json.dump(dict(sp_order=len(seen), orbits=orbs), open('orbits.json', 'w'), indent=1)
