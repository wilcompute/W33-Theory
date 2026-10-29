"""12403: the joint symmetry of the quantum i and a light cone on F_3^4.  Sp(4,3) enumerated (51840).  For a Kahler J (12370): stabilizer
S_J = {h : h J = J h} (expected GU(2,3), order 96 -- the finite U(2)); its centre, its intersection with SL (det-1 part ~ SU(2,3) = SL(2,3)),
derived subgroup.  For each of the 288 light cones kappa commuting with J (12371c): S_{J,kappa} = {h in S_J : C(h) kappa = kappa C(h)},
C = action on bivectors.  Reports the orders and the structure of the joint stabilizers (centre, exponent, abelian?)."""
import json, collections, itertools
import numpy as np
from sympy import Matrix
p = 3
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)
pairs = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]
def comp2(h):
    return np.array([[(h[a, c] * h[b, d] - h[a, d] * h[b, c]) % p for (c, d) in pairs] for (a, b) in pairs], dtype=np.int64)
def tv(v):
    v = np.array(v, dtype=np.int64); return (np.eye(4, dtype=np.int64) + np.outer(v, np.array([int(e @ Om @ v) for e in np.eye(4, dtype=np.int64)]))) % p
gens = [tv(v) for v in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1])]
seen = {np.eye(4, dtype=np.int64).tobytes(): np.eye(4, dtype=np.int64)}; fr = [np.eye(4, dtype=np.int64)]
while fr:
    nf = []
    for x in fr:
        for g in gens:
            y = (g @ x) % p; b = y.tobytes()
            if b not in seen: seen[b] = y; nf.append(y)
    fr = nf
G = list(seen.values()); print('|Sp(4,3)| =', len(G))
g0 = np.load('../search_drivers_12369/kahler_metrics.npy')[0]
J = np.array(Matrix(g0.tolist()).inv_mod(p), dtype=np.int64) @ Om % p
SJ = [h for h in G if ((h @ J - J @ h) % p == 0).all()]
def order(h):
    x = h.copy(); k = 1
    while not (x == np.eye(4, dtype=np.int64)).all(): x = (x @ h) % p; k += 1
    return k
def centre(S):
    return [z for z in S if all(((z @ h - h @ z) % p == 0).all() for h in S)]
def det3(h): return int(round(np.linalg.det(h))) % p
ZJ = centre(SJ)
info = dict(order_SJ=len(SJ), centre_order=len(ZJ), centre_element_orders=sorted(order(z) for z in ZJ),
            element_orders=dict(collections.Counter(order(h) for h in SJ)))
# 'SU' part: elements acting with F_9-determinant 1 -- here: those in the derived subgroup; compute derived subgroup by closure of commutators
comm = {}
for a in SJ[:96]:
    for b in SJ[:96]:
        ai = np.array(Matrix(a.tolist()).inv_mod(p), dtype=np.int64); bi = np.array(Matrix(b.tolist()).inv_mod(p), dtype=np.int64)
        c = (a @ b @ ai @ bi) % p; comm[c.tobytes()] = c
D = dict(comm); fr = list(comm.values())
while fr:
    nf = []
    for x in fr:
        for y in list(comm.values()):
            z = (x @ y) % p; k = z.tobytes()
            if k not in D: D[k] = z; nf.append(z)
    fr = nf
info['derived_order'] = len(D); info['derived_element_orders'] = dict(collections.Counter(order(h) for h in D.values()))
K = np.load('../search_drivers_12369/allsols.npy'); C = comp2(J)
cones = [k for k in K if ((C @ k - k @ C) % p == 0).all()]
w = np.array([0, 1, 0, 0, 2, 0], dtype=np.int64)
P = np.block([[np.zeros((3, 3), dtype=np.int64), np.eye(3, dtype=np.int64)], [np.eye(3, dtype=np.int64), np.zeros((3, 3), dtype=np.int64)]])
CS = [(h, comp2(h)) for h in SJ]
joint = collections.Counter(); examples = {}
for k in cones:
    St = [h for h, ch in CS if ((ch @ k - k @ ch) % p == 0).all()]
    inv = int(w @ P @ k @ w) % p
    key = (len(St), inv, tuple(sorted(order(h) for h in St)), len(centre(St)) == len(St))
    joint[key] += 1
print(info)
for k, v in sorted(joint.items()): print('joint stabilizer order', k[0], 'invariant', k[1], 'element orders', k[2], 'abelian', k[3], ':', v, 'cones')
json.dump(dict(info=info, joint={str(k): v for k, v in joint.items()}, cones=len(cones)), open('joint_stab.json', 'w'), indent=1)
