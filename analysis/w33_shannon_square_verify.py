"""Pass 12653: INDEPENDENT verification of the size-57 independent set of G strong-product G (data/w33_shannon_square.json).
A second W(3) point graph is built from scratch with a different symplectic form (pairing coordinates (0,1),(2,3) instead of
(0,2),(1,3)) and a different point enumeration; checked to be a GQ(3,3) point graph (40 lines of size 4, each point on 4 lines,
GQ axiom); an explicit isomorphism to the producer's graph is found by VF2 and the 57 codewords are re-checked pair by pair in the
second graph.  usage: py -3 analysis/w33_shannon_square_verify.py"""
import itertools, json, os
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
pts = sorted({min(tuple((c * x) % 3 for x in v) for c in (1, 2)) for v in itertools.product(range(3), repeat=4) if any(v)}, reverse=True)
assert len(pts) == 40
om = lambda a, b: (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % 3
G2 = nx.Graph(); G2.add_nodes_from(range(40))
G2.add_edges_from((i, j) for i, j in itertools.combinations(range(40), 2) if om(pts[i], pts[j]) == 0)
assert all(d == 12 for _, d in G2.degree())
cl = [c for c in nx.find_cliques(G2)]; assert len(cl) == 40 and all(len(c) == 4 for c in cl)
for p in range(40):  # GQ axiom: for a point p not on line L, exactly one point of L is collinear with p
    for L in cl:
        if p not in L: assert sum(1 for x in L if G2.has_edge(p, x)) == 1
d = json.load(open(os.path.join(ROOT, "data", "w33_shannon_square.json")))
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_capacity_audit.py")}
exec(open(os.path.join(HERE, "w33_shannon_capacity_audit.py"), encoding="utf-8").read().split("t0 = time.time(); res = {}")[0], g)
G1 = nx.from_numpy_array(g["w33"]())
iso = nx.vf2pp_isomorphism(G1, G2); assert iso is not None
S = [(iso[u], iso[v]) for u, v in d["set"]]
assert len(set(S)) == len(S) == d["alpha_G2_best"]
close = lambda a, b: a == b or G2.has_edge(a, b)
bad = [(x, y) for x, y in itertools.combinations(S, 2) if close(x[0], y[0]) and close(x[1], y[1])]
res = dict(size=len(S), conflicts=len(bad), GQ_axiom=True, isomorphism_found=True, Theta_lower=len(S) ** 0.5)
print(res); assert not bad
json.dump(res, open(os.path.join(ROOT, "data", "w33_shannon_square_verify.json"), "w"), indent=1)
