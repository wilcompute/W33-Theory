"""Long shot 3: the level ladder.  Level 3 (Passes 12634-12635): trop Burkhardt rays = W(3,3) POINTS, trop cubic-surface (Naruki)
cusp rays = W(3,3) LINES - the two moduli spaces see the two halves, because W(3,3) is not self-dual (Q(4,3) != W(3)).
Level 2: Segre cubic and Igusa quartic (genus-2 level-2 moduli, S6 = Sp(4,2)); Ren-Sam-Schrader-Sturmfels (arXiv:1303.1132, Thm 2.4):
the two tropical fans are AFFINELY ISOMORPHIC (multiplicity 1 vs 2), = trop M_{0,6} with 25 rays (15 duads + 10 3|3 splits),
105 edges, 105 maximal cones (trivalent trees); coordinates indexed by the 15 synthemes.  W(3,2) (the doily) IS self-dual.
Check: reconstruct the level-2 fan (rays duads + tripartitions; cones = compatible splits), its counts, and that the duad ray graph is
the doily point graph SRG(15,6,1,3); the doily line graph (synthemes, meeting = sharing a duad) has the same parameters and is
isomorphic (self-duality), unlike level 3 where perp-perp separated W(3,3) (4) from Q(4,3) (2).
usage: py -3 analysis/w33_level2_ladder.py"""
import itertools
import json
import os
from collections import Counter
import networkx as nx
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = range(6)
duads = [frozenset(d) for d in itertools.combinations(S, 2)]
trip = sorted({frozenset((frozenset(t), frozenset(set(S) - set(t)))) for t in itertools.combinations(S, 3)}, key=lambda x: sorted(map(sorted, x)))
def side(r):
    return r if (isinstance(r, frozenset) and all(isinstance(x, int) for x in r)) else sorted(r, key=sorted)[0]
def compatible(a, b):
    A, B = side(a), side(b)
    Ac, Bc = frozenset(S) - A, frozenset(S) - B
    return any(not (x & y) for x in (A, Ac) for y in (B, Bc))
def is_duad(r):
    return len(side(r)) == 2
rays = duads + trip
edges = [(a, b) for a, b in itertools.combinations(range(len(rays)), 2) if compatible(rays[a], rays[b])]
tri = [t for t in itertools.combinations(range(len(rays)), 3) if all(compatible(rays[a], rays[b]) for a, b in itertools.combinations(t, 2))]
synthemes = sorted({frozenset(m) for m in [frozenset((frozenset(p[0:2]), frozenset(p[2:4]), frozenset(p[4:6]))) for p in itertools.permutations(S)]}, key=lambda x: sorted(map(sorted, x)))
Gp = nx.Graph(); Gp.add_nodes_from(range(15)); Gp.add_edges_from((i, j) for i, j in itertools.combinations(range(15), 2) if not (duads[i] & duads[j]))
Gl = nx.Graph(); Gl.add_nodes_from(range(15)); Gl.add_edges_from((i, j) for i, j in itertools.combinations(range(15), 2) if synthemes[i] & synthemes[j])
def srg(G):
    import numpy as np
    A = nx.to_numpy_array(G, dtype=int); A2 = A @ A; n = len(A)
    k = {int(x) for x in A.sum(1)}; lam = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and A[i, j]}; mu = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and not A[i, j]}
    return (n, k.pop(), lam.pop(), mu.pop()) if len(k) == len(lam) == len(mu) == 1 else None
res = dict(rays=len(rays), edges=len(edges), max_cones=len(tri), edge_types=dict(Counter(int(is_duad(rays[a])) + int(is_duad(rays[b])) for a, b in edges)),
           duad_graph=srg(Gp), syntheme_graph=srg(Gl), point_and_line_graphs_isomorphic=nx.is_isomorphic(Gp, Gl), n_synthemes=len(synthemes))
res["matches_theorem"] = (res["rays"], res["edges"], res["max_cones"]) == (25, 105, 105)
json.dump(res, open(os.path.join(ROOT, "data", "w33_level2_ladder.json"), "w"), indent=1, default=str)
print(res)
