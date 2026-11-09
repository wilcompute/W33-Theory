"""Bridge between the two tropical fans (Passes 12634/12635).
Naruki fan (cubic surfaces): 36 roots, 40 A2^3 (= W(3,3) lines via Q(4,3)), 45 D4 (aaaa classes).
Burkhardt fan (flavour modulus): 40 W(3,3) points, 45 splits {b, b-perp}.
(i) Explicit graph isomorphism phi: A2^3 (root-disjoint relation) -> isotropic lines of W(3,3) in F_3^4 (meeting relation).
(ii) Roots -> spreads: the 10 A2^3 containing a root must map to 10 pairwise disjoint lines, i.e. one of the 36 spreads, bijectively.
(iii) D4 -> splits: a D4 induces on the 40 A2^3 the function T -> |D4 cap roots(T)|; a split induces on the 40 lines the function
L -> (#points of L in b, in b-perp).  Test that under phi each D4's partition of the lines equals exactly one split's, bijectively.
(iv) Points of W(3,3) on the Naruki side: each W(3,3) point is the set of 4 lines through it = a 4-clique of A2^3 that are pairwise
root-disjoint; report what these 40 objects are in E6 (the union of their roots).
usage: py -3 analysis/w33_split_bridge.py"""
import itertools
import json
import os
from collections import Counter, defaultdict

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0]
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(src, g)
POS, IP, T3, roots_of, np = g["POS"], g["IP"], g["T3"], g["roots_of"], g["np"]
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
P, iso, splits, w = sb["P"], sb["iso"], sb["splits"], sb["w"]
lines = [frozenset(L) for L in iso]
assert len(lines) == 40

GN = nx.Graph(); GN.add_nodes_from(range(40))
GN.add_edges_from((s, t) for s, t in itertools.combinations(range(40), 2) if not (roots_of[s] & roots_of[t]))
GW = nx.Graph(); GW.add_nodes_from(range(40))
GW.add_edges_from((a, b) for a, b in itertools.combinations(range(40), 2) if lines[a] & lines[b])
phi = nx.vf2pp_isomorphism(GN, GW)
assert phi is not None
res = dict(isomorphism_found=True)

# (ii) roots -> spreads
spread_of_root = []
for r in range(36):
    Ts = [t for t in range(40) if r in roots_of[t]]
    Ls = [lines[phi[t]] for t in Ts]
    disjoint = all(not (a & b) for a, b in itertools.combinations(Ls, 2))
    covers = len(frozenset().union(*Ls)) == 40
    spread_of_root.append((len(Ts), disjoint, covers, frozenset(phi[t] for t in Ts)))
res["roots_to_spreads"] = dict(sizes=sorted({x[0] for x in spread_of_root}), all_pairwise_disjoint=all(x[1] for x in spread_of_root),
                               all_cover_40_points=all(x[2] for x in spread_of_root), distinct=len({x[3] for x in spread_of_root}))
print("roots -> spreads:", res["roots_to_spreads"])

# (iii) D4 -> splits
def span_roots(S):
    M = POS[sorted(S)].astype(float)
    Pm = M.T @ np.linalg.pinv(M.T)
    return frozenset(i for i in range(36) if np.allclose(Pm @ POS[i], POS[i]))
orth4 = []
def ext(S, start):
    if len(S) == 4:
        orth4.append(S); return
    for k in range(start, 36):
        if all(IP[k, x] == 0 for x in S):
            ext(S + [k], k + 1)
ext([], 0)
D4s = sorted({span_roots(S) for S in orth4}, key=sorted)
assert len(D4s) == 45
def partition(fn, n=40):
    cls = defaultdict(set)
    for i in range(n):
        cls[fn(i)].add(i)
    return frozenset(frozenset(c) for c in cls.values())
d4_part = [partition(lambda t, D=D: len(D & roots_of[t])) for D in D4s]
d4_part_lines = [frozenset(frozenset(phi[t] for t in c) for c in p) for p in d4_part]
split_part = [partition(lambda l, b=b, bp=bp: (len(lines[l] & b), len(lines[l] & bp))) for b, bp in splits]
# compare the partitions up to relabelling of classes (unordered pair b, b-perp: symmetrise)
split_part_sym = [partition(lambda l, b=b, bp=bp: tuple(sorted((len(lines[l] & b), len(lines[l] & bp))))) for b, bp in splits]
match = [[i for i, sp in enumerate(split_part_sym) if sp == dp] for dp in d4_part_lines]
res["d4_class_sizes"] = sorted(Counter(len(c) for c in d4_part[0]).items())
res["split_class_sizes"] = sorted(Counter(len(c) for c in split_part_sym[0]).items())
res["d4_to_split_matches"] = Counter(len(m) for m in match)
res["d4_to_split_bijective"] = all(len(m) == 1 for m in match) and len({m[0] for m in match}) == 45
print("D4 partition class sizes", res["d4_class_sizes"], "| split partition class sizes", res["split_class_sizes"])
print("D4 -> split matches per D4:", dict(res["d4_to_split_matches"]), "bijective:", res["d4_to_split_bijective"])

# (iv) W(3,3) points on the Naruki side
pt_objects = Counter()
for p in range(40):
    Ls = [l for l in range(40) if p in lines[l]]
    inv = {v: k for k, v in phi.items()}
    Ts = [inv[l] for l in Ls]
    U = frozenset().union(*[roots_of[t] for t in Ts])
    pt_objects[(len(Ts), len(U))] += 1
res["points_as_A2cubed_4cliques"] = {str(k): v for k, v in pt_objects.items()}
print("each W(3,3) point = 4 pairwise root-disjoint A2^3; (count, size of union of roots):", dict(pt_objects))
json.dump(res, open(os.path.join(ROOT, "data", "w33_split_bridge.json"), "w"), indent=1, default=str)

# (iii') finer D4 invariant: the shape of D4 cap roots(T) = number of orthogonal pairs among its 3 roots (0: an A2, 3: orthogonal triple)
def shape(D, t):
    S = sorted(D & roots_of[t])
    return (len(S), sum(1 for a, b in itertools.combinations(S, 2) if IP[a, b] == 0))
d4_part2 = [partition(lambda t, D=D: shape(D, t)) for D in D4s]
d4_part2_lines = [frozenset(frozenset(phi[t] for t in c) for c in p) for p in d4_part2]
match2 = [[i for i, sp in enumerate(split_part_sym) if sp == dp] for dp in d4_part2_lines]
res["d4_shape_classes"] = sorted(Counter((shape(D4s[0], t)) for t in range(40)).items())
res["d4_to_split_matches_shape"] = dict(Counter(len(m) for m in match2))
res["d4_to_split_bijective_shape"] = all(len(m) == 1 for m in match2) and len({m[0] for m in match2}) == 45
# what the split classes are: (points of L in b, in b-perp) histogram
res["split_line_types"] = sorted(Counter(tuple(sorted((len(lines[l] & splits[0][0]), len(lines[l] & splits[0][1])))) for l in range(40)).items())
print("D4 cap T shapes (size, orthogonal pairs): count", res["d4_shape_classes"], "| split line types", res["split_line_types"])
print("D4 -> split (shape invariant) matches per D4:", res["d4_to_split_matches_shape"], "bijective:", res["d4_to_split_bijective_shape"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_split_bridge.json"), "w"), indent=1, default=str)
