"""12515: the good matchings are the fixed-point pairs of the polyhedral rotation axes.  For q = 7 (S4, cube) the 4 pairs should be the
fixed-point pairs of the 4 cyclic subgroups of order 3 (the cube's body diagonals = the 3-fold axes, whose fixed points on the Bloch
sphere are the 8 Bravyi-Kitaev T-type magic states); for q = 11 (A5, icosahedron) the 6 pairs should be the fixed points of the 6
subgroups of order 5 (5-fold axes = icosahedron vertices); for q = 3 (D4) the order-4 elements.  usage: py -3 matching_axes.py"""
import json, itertools
from chord_condition import INF, mob, good, involutions, matchings
from exceptional_matching import pgl, order

out = {}
for q, axis_order in ((3, 4), (7, 3), (11, 5)):
    pts = [INF] + list(range(q)); idx = {p: i for i, p in enumerate(pts)}
    sq = {x * x % q for x in range(1, q)}; invs = involutions(q)
    G = [tuple(idx[y] for y in g) for g in pgl(q)]
    m0 = next(frozenset(frozenset((idx[a], idx[b])) for a, b in m) for m in matchings(pts) if good(m, q, sq, invs))
    act = lambda g, m: frozenset(frozenset(g[i] for i in pr) for pr in m)
    stab = [g for g in G if act(g, m0) == m0]
    axis_pairs = set()
    for g in stab:
        if order(g) == axis_order:
            fixed = [i for i in range(q + 1) if g[i] == i]
            if len(fixed) == 2: axis_pairs.add(frozenset(fixed))
    out[q] = dict(stabiliser=len(stab), axis_order=axis_order, axis_pairs=len(axis_pairs), matching_pairs=len(m0),
                  matching_equals_axis_fixed_pairs=axis_pairs == set(m0))
    print(q, out[q], flush=True)
json.dump({str(k): v for k, v in out.items()}, open("matching_axes.json", "w"), indent=1)
