"""Item 2: an exact route for the three-qubit size-5 sets: zero forcing on the purity equation, adapted to qubits.
For a pure state with Pauli expectations chi(u) (real for Hermitian qubit Paulis), rho^2 = rho gives  d chi(w) = sum_u chi(u) chi(w+u) phi(u,w),
where phi(u,w) and phi(w+u,w) are fourth roots of unity that CANCEL when W_u and W_w anticommute and ADD (to +-2) when they commute.
So for w with chi(w) = 0 forced (covered Paulis), only commuting pairs {u, w+u} with both in the support matter; a single such pair forces
chi(u) chi(w+u) = 0 (branch).  A pure state needs support >= d (sum chi^2 = d, |chi| <= 1).  If every branch dies, no vector is unbiased
to all bases: an exact combinatorial proof of strong unextendibility.  Controls: d = 4 size-3 sets (proved strongly unextendible by SOS:
should die if the method is strong enough); subsets of complete sets (must stay alive).
usage: py -3 analysis/w33_qubit_zero_forcing.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
exec(_src[: _src.index("\nres = {}")], cs)
geometry, maximal_partial_spreads = cs["geometry"], cs["maximal_partial_spreads"]
def zero_force(n, pts, w, covered_pts, limit=400000):
    d = 2 ** n
    VEC = [u for u in itertools.product(range(2), repeat=2 * n)]
    idx = {p: i for i, p in enumerate(pts)}  # for qubits points = nonzero vectors
    add = lambda a, b: tuple((x + y) % 2 for x, y in zip(a, b))
    Z0 = frozenset(u for u in VEC if any(u) and idx[u] in covered_pts)
    stats = dict(nodes=0)
    def rec(Z):
        stats["nodes"] += 1
        if stats["nodes"] > limit:
            return "limit"
        S = [u for u in VEC if u not in Z]
        if len(S) < d:
            return "dead"
        Sset = set(S)
        for wv in Z:
            pairs = set()
            for u in S:
                v = add(wv, u)
                if v in Sset and u != v and w(u, wv) == 0:
                    pairs.add(frozenset((u, v)))
            if len(pairs) == 1:
                a, b = tuple(next(iter(pairs)))
                r1 = rec(Z | {a}) if any(a) else "dead"
                if r1 in ("alive", "limit"):
                    return r1
                return rec(Z | {b}) if any(b) else "dead"
        return "alive"
    return rec(Z0), stats["nodes"]
res = {}
for (n, size, label) in ((2, 3, "d4_size3"), (2, 5, "d4_spread"), (3, 5, "d8_size5"), (3, 9, "d8_spread")):
    pts, lag, w = geometry(2, n)
    mps, disj = maximal_partial_spreads(lag)
    S_ = sorted(next(S for S in mps if len(S) == size))
    if "spread" in label:
        S_ = S_[: (3 if n == 2 else 5)]   # a non-maximal subset of a complete set: extendible, must stay alive
    cov = frozenset().union(*[lag[L] for L in S_])
    out, nodes = zero_force(n, pts, w, cov)
    res[label] = dict(result=out, nodes=nodes)
    print(label, out, "nodes", nodes, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_qubit_zero_forcing.json"), "w"), indent=1)
