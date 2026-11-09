"""Long shot 2: the E7 rung.  E6 / two qutrits (Pass 12636): maximal partial spreads of W(3,3) = {10: 36 roots, 8: 135 aaaa cones,
5: 432 pezzotopes}.  E7 / three qubits: W(E7) = Z2 x Sp(6,2); W(5,2) = three-qubit Pauli geometry (63 points = 63 positive roots;
135 Lagrangian planes = maximal commuting sets = the 135 orthogonal 7-frames of E7).  E7 pezzotopes (Early-Geiger-Panizzut-
Sturmfels-Yun): 60480 regions = |Sp(6,2)|/24.
Enumerate all maximal partial spreads of W(5,2) (sets of pairwise disjoint Lagrangian planes = weakly unextendible 3-qubit Pauli
MUBs), by size and by Sp(6,2)-orbit (orbit sizes via transvection closure), and compare with E7 numbers (63, 135, 315, 960, 4032,
30240, 60480, ...).
usage: py -3 analysis/w33_e7_rung_mubs.py"""
import itertools
import json
import os
from collections import Counter

import networkx as nx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 6
vecs = [v for v in itertools.product(range(2), repeat=n) if any(v)]
P = vecs  # over F2 projective points = nonzero vectors
idx = {p: i for i, p in enumerate(P)}
w = lambda u, v: (u[0] * v[3] + u[3] * v[0] + u[1] * v[4] + u[4] * v[1] + u[2] * v[5] + u[5] * v[2]) % 2
add = lambda u, v: tuple((a + b) % 2 for a, b in zip(u, v))
# Lagrangian planes: totally isotropic 3-dim subspaces (7 points)
lag = set()
for a, b, c in itertools.combinations(P, 3):
    if w(a, b) or w(a, c) or w(b, c):
        continue
    S = {a, b, c, add(a, b), add(a, c), add(b, c), add(add(a, b), c)}
    if len(S) == 7:
        lag.add(frozenset(idx[s] for s in S))
lag = sorted(lag, key=sorted)
print("Lagrangian planes:", len(lag))
G = nx.Graph(); G.add_nodes_from(range(len(lag)))
G.add_edges_from((i, j) for i, j in itertools.combinations(range(len(lag)), 2) if not (lag[i] & lag[j]))
print("disjointness degree:", sorted(set(dict(G.degree()).values())))
sizes = Counter()
cl_by_size = {}
for c in nx.find_cliques(G):
    sizes[len(c)] += 1
    cl_by_size.setdefault(len(c), []).append(frozenset(c))
print("maximal partial spreads by size:", dict(sorted(sizes.items())))
# Sp(6,2) orbits: transvections x -> x + w(x, v) v
lag_index = {L: i for i, L in enumerate(lag)}
gens = []
for v in P:
    perm = [idx[add(p, v) if w(p, v) else p] for p in P]
    gens.append([lag_index[frozenset(perm[x] for x in L)] for L in lag])
orbits = {}
for s, cls in cl_by_size.items():
    seen = set()
    osz = []
    for C in cls:
        if C in seen:
            continue
        orb = {C}; todo = [C]
        while todo:
            X = todo.pop()
            for gp in gens:
                Y = frozenset(gp[x] for x in X)
                if Y not in orb:
                    orb.add(Y); todo.append(Y)
        seen |= orb
        osz.append(len(orb))
    orbits[s] = sorted(osz)
    print("size", s, "orbit sizes under Sp(6,2):", sorted(osz), "| stabiliser orders:", [1451520 // o for o in sorted(osz)])
res = dict(n_lagrangian=len(lag), sizes=dict(sizes), orbits=orbits, has_60480=any(60480 in o for o in orbits.values()))
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_rung_mubs.json"), "w"), indent=1)
print("an orbit of size 60480 (E7 pezzotope count):", res["has_60480"])
