"""12371c: joint structures.  For each Kahler complex structure J (from the 540 compatible metrics, 12370) its action on bivectors
L2J = second compound of J; (L2J)^2 = +1.  Count light cones kappa (12369) commuting with L2J, with their second invariant on omega.
Also: L2J fixes omega (J is symplectic) -- checked."""
import json, collections
import numpy as np
from sympy import Matrix
p = 3
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)
pairs = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]
def comp2(h):
    return np.array([[(h[a, c] * h[b, d] - h[a, d] * h[b, c]) % p for (c, d) in pairs] for (a, b) in pairs], dtype=np.int64)
G = np.load('kahler_metrics.npy'); K = np.load('allsols.npy')
w = np.array([0, 1, 0, 0, 2, 0], dtype=np.int64)
P = np.block([[np.zeros((3, 3), dtype=np.int64), np.eye(3, dtype=np.int64)], [np.eye(3, dtype=np.int64), np.zeros((3, 3), dtype=np.int64)]])
Js = {}
for g in G:
    J = np.array(Matrix(g.tolist()).inv_mod(p), dtype=np.int64) @ Om % p
    Js[J.tobytes()] = J
print('distinct J:', len(Js))
stats = collections.Counter(); fix = 0; per = []
for J in Js.values():
    C = comp2(J)
    fix += ((C @ w - w) % p == 0).all() or ((C @ w + w) % p == 0).all()
    comm = [k for k in K if ((C @ k - k @ C) % p == 0).all()]
    per.append(len(comm))
    for k in comm: stats[int(w @ P @ k @ w) % p] += 1
print('L2J fixes omega (up to sign) for', fix, 'of', len(Js))
print('cones commuting with L2J per J:', collections.Counter(per), ' second-invariant of those:', dict(stats))
json.dump(dict(distinct_J=len(Js), omega_fixed=int(fix), commuting_per_J=dict(collections.Counter(per)), second_invariant=dict(stats)), open('joint.json', 'w'), indent=1)
