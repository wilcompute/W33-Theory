"""12533 follow-up: the triangle of codewords selected by the TL basis.  A = C + X, B = C + Y, D = X + Y with C the 5 caps.  In totals language: their double-sixes; how their five-circuits overlap; whether the triangle is one of a family: count all triples of codewords summing to zero, and the orbits under PSp(4,3); is this one's stabiliser related to the braid group?  usage: py -3 codeword_triangle.py"""
import collections
import itertools
import json
import runpy

ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
ids = json.load(open("caps_codewords.json"))["noncrossing_line_ids"]
cw = [frozenset(S) for S in codewords]
cwset = set(cw)
tri = {frozenset((a, b, a ^ b)) for a, b in itertools.combinations(cw, 2) if (a ^ b) in cwset}
out = dict(triples_summing_to_zero=len(tri))
inter = collections.Counter()
for a, b in itertools.combinations(cw, 2):
    inter[len(a & b)] += 1
out["pairwise_intersection_counts"] = {str(k): v for k, v in sorted(inter.items())}
six = [S for S in cw if set(ids) <= S]
A, B = six
D = A ^ B
assert D in cwset
out["this_triangle"] = dict(sizes=[len(A), len(B), len(D)], common_A_B=len(A & B), common_A_D=len(A & D), common_B_D=len(B & D))
P = list(group([T(pts[i]) for i in range(40)]))
Gl = {g: lmap(g) for g in P}
act = lambda g, S: frozenset(Gl[g][j] for j in S)
this = frozenset((A, B, D))
st = [g for g in P if frozenset(act(g, S) for S in this) == this]
out["triangle_stabiliser_order"] = len(st)
orb = {frozenset(act(g, S) for S in this) for g in P}
out["triangle_orbit_size"] = len(orb)
out["orbit_times_stabiliser"] = len(orb) * len(st)
cap_stab = [g for g in P if frozenset(Gl[g][j] for j in ids) == frozenset(ids)]
out["caps_stabiliser_order"] = len(cap_stab)
prof = collections.Counter()
e = tuple(range(40))
for g in cap_stab:
    p, n = g, 1
    while p != e:
        p = compose(g, p)
        n += 1
    prof[n] += 1
out["caps_stabiliser_element_orders"] = dict(sorted(prof.items()))
# 5 lines: their set of 20 - overlaps points covered
sets = [set(L) for L in lines]
cov = collections.Counter()
for j in ids:
    for p in sets[j]:
        cov[p] += 1
out["caps_point_coverage"] = dict(collections.Counter(cov.values()))
print(json.dumps(out, default=str))
json.dump(out, open("codeword_triangle.json", "w"), indent=1, default=str)
