"""Items 1 + 3: the sentinel principle across rungs.  For a set of Pauli MUBs in C^d (d = p^n), M = sum_e A_e (x) A_e = (1/d) sum_{u covered} W_u (x) W_u^dag
and SWAP = (1/d) sum_{all u} W_u (x) W_u^dag, so on Sym^2: M = (d - 1 - T_U)/d, T_U = sum over uncovered nonzero Pauli vectors.
If the uncovered points are covered with uniform multiplicity m by 'splits' (pairs of complementary nondegenerate subspaces b, b-perp of
dimension n each = tensor factorisations d = p^(n/2)... for n = 2: two-qudit splits; for n = 3: no balanced splits), T_U is affine in swaps.
Report per rung: uncovered point count, whether it is a union of splits with uniform multiplicity (n = 2 cases), and for three qubits the
structure of the 28 uncovered points (is it the non-singular set of a quadratic form polarising to the symplectic form, i.e. O+ / O-?).
usage: py -3 analysis/w33_sentinel_rungs.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
exec(open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read().split("res = {}")[0], cs)
geometry, maximal_partial_spreads = cs["geometry"], cs["maximal_partial_spreads"]
out = {}
for (p, n, size, label) in ((2, 2, 3, "d4_size3"), (3, 2, 5, "d9_size5"), (3, 2, 8, "d9_size8"), (2, 3, 5, "d8_size5")):
    pts, lag, w = geometry(p, n)
    mps, disj = maximal_partial_spreads(lag)
    S_ = sorted(next(S for S in mps if len(S) == size))
    covered = frozenset().union(*[lag[L] for L in S_]); unc = frozenset(range(len(pts))) - covered
    row = dict(points=len(pts), uncovered=len(unc))
    if n == 2:
        # splits: nondegenerate 2-dim subspaces b with b-perp, both inside the uncovered set
        idx = {q: i for i, q in enumerate(pts)}
        def norm(v):
            c = next(x for x in v if x); inv = pow(c, -1, p); return tuple((x * inv) % p for x in v)
        planes = set()
        for a, b in itertools.combinations(range(len(pts)), 2):
            if w(pts[a], pts[b]) != 0:
                S2 = frozenset(idx[norm(tuple((x * pts[a][k] + y * pts[b][k]) % p for k in range(4)))] for x in range(p) for y in range(p) if (x, y) != (0, 0))
                planes.add(S2)
        perp = lambda S2: frozenset(i for i in range(len(pts)) if all(w(pts[i], pts[j]) == 0 for j in S2))
        sp = {frozenset((S2, perp(S2))) for S2 in planes}
        inside = [tuple(s) for s in sp if all(x <= unc for x in s)]
        mult = Counter(q for b, bp in inside for q in (b | bp))
        row.update(splits_inside=len(inside), multiplicities=sorted(set(mult.values())) if mult else [], covers_all=set(mult) == unc)
    else:
        # three qubits: quadratic forms Q with polarisation w; Q(x) = sum_i a_i b_i (standard) + linear correction l(x)^2 = <c, x>: Q_c(x) = Q0(x) + w(c, x)
        Q0 = lambda x: (x[0] * x[3] + x[1] * x[4] + x[2] * x[5]) % 2
        found = []
        for c in itertools.product(range(2), repeat=6):
            Qc = lambda x, c=c: (Q0(x) + sum(ci * xi for ci, xi in zip((c[3], c[4], c[5], c[0], c[1], c[2]), x))) % 2
            nonsing = frozenset(i for i, q in enumerate(pts) if Qc(q) == 1)
            if nonsing == unc:
                found.append(("O+" if len(nonsing) == 28 else "O-", c))
            if frozenset(range(len(pts))) - nonsing == unc:
                found.append(("singular set", c))
        row.update(uncovered_is_quadric_class=[f[0] for f in found])
    out[label] = row
    print(label, row)
json.dump(out, open(os.path.join(ROOT, "data", "w33_sentinel_rungs.json"), "w"), indent=1, default=str)
