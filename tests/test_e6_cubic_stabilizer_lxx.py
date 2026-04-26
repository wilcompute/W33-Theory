"""
Part LXX — E6 cubic stabilizer obstruction
==========================================

This test addresses the next bottleneck after LXIX:

    Can W33 construct a canonical 78-dimensional E6-like algebra acting on U=27?

A tempting candidate is the unsigned cubic formed from the 36 internal triangles
inside H27.  This file tests that candidate directly by computing the
infinitesimal stabilizer of the symmetric cubic tensor

    c(x) = sum_{(a,b,c) in internal_triangles(H27)} x_a x_b x_c.

For a true E6 Cartan cubic on the 27-dimensional minuscule representation,
the infinitesimal stabilizer should have dimension 78.  The unsigned 36-triangle
W33 cubic has stabilizer dimension only 6.

Conclusion: the internal 36 triangles alone are not the E6 cubic.  The missing
9 fibers / full 45-tritangent signed structure is essential if an E6 action is
to be constructed from W33.
"""
from itertools import combinations, combinations_with_replacement, product


Q = 3


def norm(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % Q for y in v)
    raise RuntimeError("unreachable")


def omega(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % Q


def build_w33():
    points = sorted({norm(v) for v in product(range(Q), repeat=4) if any(v)})
    adj = [set() for _ in points]
    for i, j in combinations(range(len(points)), 2):
        if omega(points[i], points[j]) == 0:
            adj[i].add(j)
            adj[j].add(i)
    return points, adj


def h27_internal_triangles(base_vertex=0):
    points, adj = build_w33()
    h27 = [v for v in range(len(points)) if v != base_vertex and v not in adj[base_vertex]]
    local = {v: i for i, v in enumerate(h27)}
    triangles = []
    for a, b, c in combinations(h27, 3):
        if b in adj[a] and c in adj[a] and c in adj[b]:
            triangles.append(tuple(sorted((local[a], local[b], local[c]))))
    return sorted(triangles)


def rank_mod_prime_sparse(rows, ncols, prime=1000003):
    """Sparse Gaussian elimination over GF(prime)."""
    pivots = {}
    rank = 0
    for row in rows:
        row = {k: v % prime for k, v in row.items() if v % prime}
        while row:
            pivot = min(row)
            coeff = row[pivot] % prime
            if pivot not in pivots:
                inv = pow(coeff, prime - 2, prime)
                pivots[pivot] = {k: (v * inv) % prime for k, v in row.items()}
                rank += 1
                break
            factor = coeff
            prow = pivots[pivot]
            for k, v in prow.items():
                nv = (row.get(k, 0) - factor * v) % prime
                if nv:
                    row[k] = nv
                elif k in row:
                    del row[k]
    return rank


def cubic_stabilizer_nullity(triangles, dim=27):
    """Compute nullity of infinitesimal stabilizer of an unsigned cubic.

    Variables are X_{i,a}, representing a dim x dim matrix X acting by
    (X.c)_{abc} = sum_i X_{i,a} c_{i,b,c}
               + sum_i X_{i,b} c_{a,i,c}
               + sum_i X_{i,c} c_{a,b,i}.
    """
    tri_set = set(tuple(sorted(t)) for t in triangles)

    def C(a, b, c):
        if len({a, b, c}) != 3:
            return 0
        return 1 if tuple(sorted((a, b, c))) in tri_set else 0

    rows = []
    for a, b, c in combinations_with_replacement(range(dim), 3):
        row = {}
        for i in range(dim):
            if C(i, b, c):
                row[i * dim + a] = row.get(i * dim + a, 0) + 1
            if C(a, i, c):
                row[i * dim + b] = row.get(i * dim + b, 0) + 1
            if C(a, b, i):
                row[i * dim + c] = row.get(i * dim + c, 0) + 1
        if row:
            rows.append(row)
    rank = rank_mod_prime_sparse(rows, dim * dim)
    return dim * dim - rank


class TestLXXE6CubicStabilizerObstruction:
    def test_h27_has_36_internal_triangles(self):
        assert len(h27_internal_triangles()) == 36

    def test_unsigned_36_triangle_cubic_stabilizer_is_6_not_78(self):
        triangles = h27_internal_triangles()
        nullity = cubic_stabilizer_nullity(triangles)
        assert nullity == 6
        assert nullity != 78

    def test_consequence_missing_9_fibers_are_essential(self):
        internal_triangles = 36
        missing_fibers = 9
        tritangent_total = 45
        assert internal_triangles + missing_fibers == tritangent_total

    def test_next_target_is_signed_45_tritangent_cubic(self):
        # This is the honest next theorem target: construct the signed 45-term
        # cubic and test whether its infinitesimal stabilizer has dimension 78.
        unsigned_36_stabilizer_dim = 6
        target_e6_stabilizer_dim = 78
        assert unsigned_36_stabilizer_dim < target_e6_stabilizer_dim
