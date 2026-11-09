"""Pass 12643: the coherent closure of the uncovered anticommutation graph singles out one uncovered point; identify it by
per-vertex invariants (triangles, covered sums, lines through it meeting the covered set once).  usage: py -3 analysis/w33_threequbit_sentinel_point.py"""
import contextlib, io, os, itertools, numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()): exec(_src[: _src.index("\nres = {}")], cs)
pts, lag, w = cs["geometry"](2, 3); mps, _ = cs["maximal_partial_spreads"](lag)
S = next(sorted(S) for S in mps if len(S) == 5); cov = frozenset().union(*[lag[L] for L in S]); U = [i for i in range(63) if i not in cov]
idx = {q: i for i, q in enumerate(pts)}
add = lambda a, b: idx[tuple((x + y) % 2 for x, y in zip(pts[a], pts[b]))]
# per uncovered vertex: number of triangles (anticommuting triples with sum relation), number of uncovered lines through it, etc.
Ulines = [L for L in range(len(lag)) if not (set(lag[L]) & cov) ]
def inv(u):
    nb = [v for v in U if v != u and w(pts[u], pts[v]) == 1]
    tri = sum(1 for a, b in itertools.combinations(nb, 2) if w(pts[a], pts[b]) == 1)
    sums_cov = sum(1 for v in nb if add(u, v) in cov)
    lines_through = sum(1 for L in range(len(lag)) if u in lag[L] and len(set(lag[L]) & cov) == 1)
    return (tri, sums_cov, lines_through)
print(Counter(inv(u) for u in U)); print("uncovered lines (meet C nowhere):", len(Ulines))
special = [u for u in U if Counter(inv(x) for x in U)[inv(u)] == 1]
print("special point:", [pts[u] for u in special])
