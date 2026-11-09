"""Item 4: the E7 rung with other relations.  Pass 12636: E7 pezzotopes (60480 = |Sp(6,2)|/24) are NOT unextendible 3-qubit MUB sets.
Census of Sp(6,2) orbits on small configurations of Lagrangian planes of W(5,2) (three-qubit maximal commuting sets): unordered pairs
and triples, classified by orbit size (union-find under the 63 transvections), looking for an orbit of size 60480 (stabiliser 24) or
120960 (two chiral halves of 60480 under a Z2).  Also (plane, point off the plane) flags and (plane, plane, plane) with pairwise
intersection dimensions recorded per orbit.
usage: py -3 analysis/w33_e7_orbit_census.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e7_rung_mubs.py")}
src = open(os.path.join(HERE, "w33_e7_rung_mubs.py"), encoding="utf-8").read().split("G = nx.Graph()")[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ns)
P, lag, idx, w, add = ns["P"], ns["lag"], ns["idx"], ns["w"], ns["add"]
L = len(lag)
lag_index = {x: i for i, x in enumerate(lag)}
gens = []
for v in P:
    perm = [idx[add(p, v) if w(p, v) else p] for p in P]
    gens.append([lag_index[frozenset(perm[x] for x in Q)] for Q in lag])
def inter_dim(a, b):
    k = len(lag[a] & lag[b])  # 0, 1, 3, 7 points -> dims 0, 1, 2, 3
    return {0: 0, 1: 1, 3: 2, 7: 3}[k]
def orbits_of(objs, act):
    parent = {o: o for o in objs}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for o in objs:
        for g in gens:
            a, b = find(o), find(act(g, o))
            if a != b:
                parent[a] = b
    cnt = Counter(find(o) for o in objs)
    return cnt, find
pairs = [frozenset(p) for p in itertools.combinations(range(L), 2)]
cp, fp = orbits_of(pairs, lambda g, o: frozenset(g[x] for x in o))
pair_orbits = sorted((v, inter_dim(*sorted(k))) for k, v in cp.items())
print("pairs of Lagrangians: orbits (size, intersection dim):", pair_orbits)
triples = [frozenset(t) for t in itertools.combinations(range(L), 3)]
ct, ft = orbits_of(triples, lambda g, o: frozenset(g[x] for x in o))
trip_orbits = sorted((v, tuple(sorted(inter_dim(a, b) for a, b in itertools.combinations(sorted(k), 2)))) for k, v in ct.items())
print("triples of Lagrangians: %d orbits" % len(trip_orbits))
for s, d in trip_orbits:
    print("   size", s, "pairwise intersection dims", d, "stabiliser", 1451520 // s)
hits = [o for o in trip_orbits + pair_orbits if o[0] in (60480, 120960)]
res = dict(pair_orbits=pair_orbits, triple_orbits=trip_orbits, orbits_60480_or_120960=hits)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_orbit_census.json"), "w"), indent=1)
print("orbits of size 60480 or 120960:", hits)
