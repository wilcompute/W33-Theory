"""Item 2: the pezzotope 'amplitude' in context variables.  For a simple 4-polytope with facet variables X_f, m = sum over vertices of
prod 1/X_f; Res_{X_f=0} m = the facet's own amplitude.  E6 pezzotope (Pass 12634/12636): 10 root facets (associahedra K5 = 6-particle
phi^3 tree amplitudes, 14 terms on 9 planar variables = hexagon diagonals) and 5 cusp facets (cubes, 8 terms on 3 opposite pairs).
Prediction: on each root facet the 9 neighbours are 6 roots + 3 cusps, and their compatibility graph is the hexagon-diagonal
non-crossing graph with the 3 cusps = the 3 LONG diagonals (3-particle channels) and the 6 roots = the 6 short ones (2-particle).
Checked on all 432 pezzotopes; plus the total vertex count 45 and the facet-vertex counts (14 / 8).
usage: py -3 analysis/w33_pezzotope_amplitude.py"""
import itertools, json, os
from collections import Counter
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
gz = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_gosset.py")}
exec(open(os.path.join(HERE, "w33_pezzotope_gosset.py"), encoding="utf-8").read().split("# candidate canonical line sets")[0], gz)
pents, IP, T3 = gz["pents"], gz["IP"], gz["T3"]
# hexagon: diagonals (i,j) of a hexagon, compatible iff non-crossing
diags = [(i, j) for i, j in itertools.combinations(range(6), 2) if (j - i) % 6 not in (1, 5)]
def cross(a, b):
    (i, j), (k, l) = a, b
    if len({i, j, k, l}) < 4:
        return False
    inside = lambda x: i < x < j
    return inside(k) != inside(l)
H = nx.Graph(); H.add_nodes_from(range(9))
H.add_edges_from((a, b) for a, b in itertools.combinations(range(9), 2) if not cross(diags[a], diags[b]))
is_long = [((diags[a][1] - diags[a][0]) % 6 == 3) for a in range(9)]
summary = Counter()
for C, r in pents:
    ra = sorted(r.values())
    facets = [("a", x) for x in ra] + [("b", t) for t in C]
    verts = []
    for S in itertools.combinations(ra, 4):
        if all(IP[x, y] == 0 for x, y in itertools.combinations(S, 2)):
            verts.append(frozenset(("a", x) for x in S))
    for t in C:
        for pick in itertools.product(*[sorted(A) for A in sorted(T3[t], key=min)]):
            if all(p in ra for p in pick):
                verts.append(frozenset([("b", t)] + [("a", p) for p in pick]))
    nv = len(verts)
    per = Counter(f for v in verts for f in v)
    ok_assoc = True
    for f in facets:
        if f[0] != "a":
            continue
        vf = [v - {f} for v in verts if f in v]
        nb = sorted(set().union(*vf), key=str)
        G = nx.Graph(); G.add_nodes_from(nb)
        for v in vf:
            G.add_edges_from(itertools.combinations(sorted(v, key=str), 2))
        types = {g: g[0] == "b" for g in nb}
        gm = nx.algorithms.isomorphism.GraphMatcher(G, H, node_match=lambda a, b: a["long"] == b["long"])
        nx.set_node_attributes(G, types, "long"); nx.set_node_attributes(H, dict(enumerate(is_long)), "long")
        gm = nx.algorithms.isomorphism.GraphMatcher(G, H, node_match=lambda a, b: a["long"] == b["long"])
        ok_assoc &= (len(nb) == 9 and sum(types.values()) == 3 and len(vf) == 14 and gm.is_isomorphic())
    cube_ok = all(per[f] == 8 for f in facets if f[0] == "b")
    summary[(nv, ok_assoc, cube_ok)] += 1
res = dict(summary={str(k): v for k, v in summary.items()}, all_ok=list(summary) == [(45, True, True)])
print("(vertices, every root facet = hexagon associahedron with cusps = long diagonals, every cube facet has 8 vertices):", dict(summary))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_amplitude.json"), "w"), indent=1)
