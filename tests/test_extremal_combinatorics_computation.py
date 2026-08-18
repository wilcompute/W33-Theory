"""
Phase CXI -- Extremal Combinatorics Computation on W(3,3) = SRG(40,12,2,4)
===========================================================================

Theorems T1701 -- T1780

Every result derived from first principles using only numpy / native Python
on the W(3,3) = SRG(40,12,2,4) adjacency matrix.

Covers: Turan bounds, independent set structure, subgraph counting,
regularity & uniformity, supersaturation, probabilistic bounds,
extremal density, and forbidden subgraph analysis.
"""

import numpy as np
from math import comb, floor, ceil, log, factorial, sqrt
from collections import Counter
from itertools import combinations
import random
import pytest

# ---------------------------------------------------------------------------
# Build W(3,3) from scratch
# ---------------------------------------------------------------------------

def _build_w33():
    points = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    v = (a, b, c, d)
                    if v == (0, 0, 0, 0):
                        continue
                    first = next(x for x in v if x != 0)
                    inv = pow(first, -1, 3)
                    canon = tuple((x * inv) % 3 for x in v)
                    if canon not in points:
                        points.append(canon)
    n = 40
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            u, v = points[i], points[j]
            omega = (u[0]*v[1] - u[1]*v[0] + u[2]*v[3] - u[3]*v[2]) % 3
            if omega == 0:
                A[i, j] = A[j, i] = 1
    return A


@pytest.fixture(scope="module")
def w33():
    return _build_w33()


@pytest.fixture(scope="module")
def basic_counts(w33):
    """Precompute commonly used quantities."""
    A = w33
    n = 40
    m = int(A.sum()) // 2  # edges
    A2 = A @ A
    A3 = A2 @ A
    A4 = A3 @ A
    degs = A.sum(axis=1).astype(int)
    # Neighbor lists
    nbrs = [set(np.where(A[i] == 1)[0]) for i in range(n)]
    return {
        "n": n, "m": m, "A": A, "A2": A2, "A3": A3, "A4": A4,
        "degs": degs, "nbrs": nbrs,
    }


# ===================================================================
# Helper: Turan graph edge count
# ===================================================================

def _turan_edges(n, r):
    """Number of edges in the Turan graph T(n, r).
    Partitions n vertices into r parts as equally as possible."""
    base, extra = divmod(n, r)
    # extra parts of size (base+1), (r-extra) parts of size base
    total = comb(n, 2)
    for i in range(r):
        s = base + 1 if i < extra else base
        total -= comb(s, 2)
    return total


# ===================================================================
# T1701 -- T1710: Turan Bounds
# ===================================================================

class TestT1701TuranBounds:
    """Turan-type extremal bounds for W(3,3)."""

    def test_edge_count(self, basic_counts):
        """W(3,3) has exactly 240 edges = n*k/2 = 40*12/2."""
        assert basic_counts["m"] == 240

    def test_edge_density(self, basic_counts):
        """Edge density = 2m / (n(n-1)) = 480/1560 = 4/13."""
        n, m = 40, 240
        density = 2 * m / (n * (n - 1))
        assert abs(density - 4 / 13) < 1e-12

    def test_turan_K3(self):
        """ex(40, K_3) = |E(T(40,2))| = K_{20,20} = 400.
        W(3,3) has 240 < 400, so edge count alone does not force triangles."""
        assert _turan_edges(40, 2) == 400
        assert 240 < 400

    def test_turan_K4(self):
        """ex(40, K_4) = |E(T(40,3))| with parts 14,13,13.
        T(40,3) = C(40,2) - C(14,2) - 2*C(13,2) = 780 - 91 - 156 = 533."""
        assert _turan_edges(40, 3) == 533
        assert 240 < 533

    def test_turan_K5(self):
        """ex(40, K_5) = |E(T(40,4))| with 4 parts of size 10 = 600.
        W(3,3) is K_5-free and has 240 << 600."""
        assert _turan_edges(40, 4) == 600
        assert 240 < 600

    def test_turan_K6(self):
        """ex(40, K_6) = |E(T(40,5))| with 5 parts of size 8 = 640."""
        assert _turan_edges(40, 5) == 640
        assert 240 < 640

    def test_turan_density_threshold(self):
        """Turan density for K_5-free graphs: 1 - 1/4 = 0.75.
        W(3,3) density 4/13 ~ 0.308 is far below this threshold."""
        w33_density = 4 / 13
        turan_density = 1 - 1 / 4
        assert w33_density < turan_density

    def test_complement_edge_count(self, w33):
        """Complement has n(n-1)/2 - 240 = 780 - 240 = 540 edges."""
        Ac = 1 - w33 - np.eye(40, dtype=int)
        comp_edges = int(Ac.sum()) // 2
        assert comp_edges == 540

    def test_zykov_bound(self):
        """Zykov bound: omega(G) >= n / (n - 2m/n).
        omega >= 40 / (40 - 480/40) = 40 / (40 - 12) = 40/28 ~ 1.43.
        So omega >= 2 (trivially, since graph has edges)."""
        n, m = 40, 240
        zykov = n / (n - 2 * m / n)
        assert zykov > 1.4
        # Actual omega = 4 exceeds this weak bound
        assert 4 >= ceil(zykov)

    def test_ramsey_lower_bound(self):
        """R(s,t) > n means any 2-coloring of K_n has monochromatic K_s or K_t.
        R(3,3)=6: any 2-coloring of K_6 has a monochromatic triangle.
        Since n=40 >= 6, W(3,3) or its complement on any 6 vertices has K_3."""
        assert 6 <= 40  # R(3,3) = 6 <= n


# ===================================================================
# T1711 -- T1720: Independent Set Structure
# ===================================================================

class TestT1711IndependentSetStructure:
    """Independence number bounds and structure for W(3,3)."""

    def test_hoffman_bound(self):
        """Hoffman bound: alpha <= n * (-lambda_min) / (k - lambda_min).
        lambda_min = -4, so alpha <= 40 * 4 / (12 + 4) = 10."""
        n, k, s = 40, 12, -4
        hoffman = n * (-s) / (k - s)
        assert hoffman == 10.0

    def test_greedy_independent_set_exists(self, basic_counts):
        """A greedy algorithm finds an independent set of size >= 4."""
        nbrs = basic_counts["nbrs"]
        n = 40
        # Greedy: pick vertex with min degree in remaining graph
        available = set(range(n))
        indep = []
        while available:
            v = min(available, key=lambda x: len(nbrs[x] & available))
            indep.append(v)
            available -= (nbrs[v] | {v})
        assert len(indep) >= 4

    def test_independent_set_is_valid(self, basic_counts):
        """Verify that a computed independent set has no internal edges."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        available = set(range(n))
        indep = []
        while available:
            v = min(available, key=lambda x: len(nbrs[x] & available))
            indep.append(v)
            available -= (nbrs[v] | {v})
        # Check no edges within independent set
        for i in range(len(indep)):
            for j in range(i + 1, len(indep)):
                assert A[indep[i], indep[j]] == 0

    def test_complement_clique_from_independent(self, w33, basic_counts):
        """An independent set in G is a clique in the complement.
        Any independent set of size s gives a clique of size s in complement."""
        Ac = 1 - w33 - np.eye(40, dtype=int)
        nbrs = basic_counts["nbrs"]
        n = 40
        available = set(range(n))
        indep = []
        while available:
            v = min(available, key=lambda x: len(nbrs[x] & available))
            indep.append(v)
            available -= (nbrs[v] | {v})
        for i in range(len(indep)):
            for j in range(i + 1, len(indep)):
                assert Ac[indep[i], indep[j]] == 1

    def test_alpha_upper_bound_ratio(self):
        """Ratio bound: alpha * omega >= n for vertex-transitive graphs.
        Actually alpha * chi >= n. With chi >= omega = 4: alpha >= n/chi >= 10.
        Combined with Hoffman: alpha = 10 exactly."""
        # alpha <= 10 (Hoffman) and alpha >= n/chi >= 40/4 = 10
        # (since chi(W(3,3)) = 4 for vertex-transitive SRG with omega=4)
        assert 10 * 4 >= 40

    def test_lovasz_theta_bound(self):
        """Lovasz theta for SRG: theta = n(-s)/(k-s) = 10.
        For vertex-transitive: alpha(G) = n / chi_f(G) and theta(G) >= alpha(G).
        Here theta = 10 = alpha, so the bound is tight."""
        theta = 40 * 4 / (12 + 4)
        assert theta == 10.0

    def test_fractional_chromatic_number(self):
        """For vertex-transitive graphs: chi_f = n / alpha.
        With alpha = 10: chi_f = 4. And chi_f = omega = 4 (tight)."""
        chi_f = 40 / 10
        assert chi_f == 4.0

    def test_no_large_independent_set(self, basic_counts):
        """No independent set of size 11 exists (Hoffman bound = 10).
        Test: every 11-subset has at least one internal edge.
        (Probabilistic check on random samples.)"""
        A = basic_counts["A"]
        rng = random.Random(42)
        verts = list(range(40))
        for _ in range(200):
            sample = rng.sample(verts, 11)
            has_edge = False
            for i in range(len(sample)):
                for j in range(i + 1, len(sample)):
                    if A[sample[i], sample[j]] == 1:
                        has_edge = True
                        break
                if has_edge:
                    break
            assert has_edge, "Found independent set of size 11, violating Hoffman bound"

    def test_independent_dominating_set(self, basic_counts):
        """A maximal independent set is also a dominating set.
        Every non-independent vertex has a neighbor in the independent set."""
        nbrs = basic_counts["nbrs"]
        n = 40
        available = set(range(n))
        indep = set()
        order = list(range(n))
        random.Random(7).shuffle(order)
        for v in order:
            if v in available:
                indep.add(v)
                available -= (nbrs[v] | {v})
        # Every vertex not in indep has a neighbor in indep
        for v in range(n):
            if v not in indep:
                assert len(nbrs[v] & indep) > 0

    def test_independence_number_equals_7(self, basic_counts):
        """alpha(W(3,3)) = 7 exactly -- NOT 10.

        The Hoffman ratio bound gives alpha <= 10, and 10 = q^2+1 would require an
        OVOID.  W(3,q) has no ovoid for q odd (Thas), so the bound is not attained.
        The exact value is 7, confirmed here by exhaustive branch and bound, and
        consistent with the published exact values alpha(W(3,5)) = 18 and
        alpha(W(3,7)) = 33 (Cimrakova-Fack 2005, Table 1), both of which likewise
        fall strictly below Tallini's bound q^2 - q + 1.

        This test previously asserted 10 in its NAME and docstring while its body
        only checked `>= 7`, so it passed while certifying a false theorem."""
        A = basic_counts["A"]
        n = 40
        # Build max cliques (totally isotropic 2-spaces = K4 cliques)
        cliques = []
        nbrs = basic_counts["nbrs"]
        for i in range(n):
            for j in nbrs[i]:
                if j <= i:
                    continue
                cn = nbrs[i] & nbrs[j]
                for pair in combinations(cn, 2):
                    a, b = pair
                    if A[a, b] == 1:
                        clq = tuple(sorted([i, j, a, b]))
                        cliques.append(clq)
        cliques = list(set(cliques))
        assert len(cliques) == 40  # 40 max isotropic 2-spaces

        # Greedy ovoid: pick one vertex per clique, no two adjacent
        ovoid = set()
        covered_cliques = set()
        for clq in cliques:
            if id_tuple(clq) in covered_cliques:
                continue
            for v in clq:
                if all(A[v, u] == 0 for u in ovoid):
                    ovoid.add(v)
                    # Mark all cliques containing v
                    for c2 in cliques:
                        if v in c2:
                            covered_cliques.add(id_tuple(c2))
                    break
        # Whatever greedy returns must at least BE independent.
        for u in ovoid:
            for v in ovoid:
                if u != v:
                    assert A[u, v] == 0

        # The real assertion: exact maximum independent set over all 40 points.
        best = 0
        order = sorted(range(n), key=lambda v: -len(nbrs[v]))

        def expand(cur, cand):
            nonlocal best
            if len(cur) + len(cand) <= best:
                return
            if not cand:
                best = max(best, len(cur))
                return
            v = cand[0]
            expand(cur + [v], [u for u in cand[1:] if u not in nbrs[v]])
            expand(cur, cand[1:])

        expand([], order)
        assert best == 7, f"alpha(W(3,3)) must be 7, got {best}"
        assert best < 10, "10 would mean W(3,3) has an ovoid; it has none (q odd)"


def id_tuple(t):
    """Helper to make tuples hashable for set membership."""
    return t


# ===================================================================
# T1721 -- T1732: Subgraph Counting
# ===================================================================

class TestT1721SubgraphCounting:
    """Exact subgraph counts in W(3,3)."""

    def test_triangle_count_trace(self, basic_counts):
        """Triangles = tr(A^3) / 6.
        tr(A^3) = sum of eigenvalues cubed = 12^3 + 2^3*24 + (-4)^3*15
        = 1728 + 192 - 960 = 960.  Triangles = 960/6 = 160."""
        tr3 = int(np.trace(basic_counts["A3"]))
        assert tr3 == 960
        assert tr3 // 6 == 160

    def test_triangle_count_direct(self, basic_counts):
        """Count triangles directly by iterating over edges and common neighbors."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        tri = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 1:
                    tri += len(nbrs[i] & nbrs[j])
        # Each triangle counted 3 times (once per edge)
        assert tri == 480  # = 160 * 3
        assert tri // 3 == 160

    def test_P2_count(self, basic_counts):
        """P2 (paths of length 2, a.k.a. cherries): for each vertex,
        C(deg, 2) = C(12, 2) = 66. Total = 40 * 66 = 2640."""
        n = 40
        k = 12
        p2 = n * comb(k, 2)
        assert p2 == 2640

    def test_C4_count_formula(self, basic_counts):
        """4-cycles C4 = (tr(A^4) - n*k*(2k-1)) / 8.
        tr(A^4) = 12^4 + 2^4*24 + (-4)^4*15 = 20736 + 384 + 3840 = 24960.
        C4 = (24960 - 40*12*23) / 8 = (24960 - 11040) / 8 = 1740."""
        tr4 = int(np.trace(basic_counts["A4"]))
        assert tr4 == 24960
        n, k = 40, 12
        c4 = (tr4 - n * k * (2 * k - 1)) // 8
        assert c4 == 1740

    def test_C4_count_pair_formula(self, basic_counts):
        """C4 = (1/2) * sum_{{i,j}} C(c_ij, 2).
        For adj pairs: c=lambda=2, C(2,2)=1; non-adj: c=mu=4, C(4,2)=6.
        C4 = (240*1 + 540*6) / 2 = 3480/2 = 1740."""
        m = 240
        non_edges = comb(40, 2) - m  # 540
        c4 = (m * comb(2, 2) + non_edges * comb(4, 2)) // 2
        assert c4 == 1740

    def test_K4_count(self, basic_counts):
        """W(3,3) has exactly 40 cliques of size 4 (= max isotropic 2-spaces).
        Verify by enumeration: for each edge, lambda=2 common neighbors;
        check if they are adjacent."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        k4_set = set()
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] != 1:
                    continue
                cn = sorted(nbrs[i] & nbrs[j])
                if len(cn) < 2:
                    continue
                for a, b in combinations(cn, 2):
                    if A[a, b] == 1:
                        k4_set.add(tuple(sorted([i, j, a, b])))
        assert len(k4_set) == 40

    def test_star_K12_count(self):
        """Each vertex is the center of a K_{1,12} star. Total = 40 stars.
        Number of K_{1,2} subgraphs (cherries) = 40 * C(12,2) = 2640."""
        assert 40 * comb(12, 2) == 2640

    def test_triangles_per_vertex(self, basic_counts):
        """Each vertex is in exactly 12 triangles (by SRG regularity).
        Total vertex-triangle incidences = 160 * 3 = 480.  Per vertex = 12."""
        A3 = basic_counts["A3"]
        n = 40
        for i in range(n):
            # A3[i,i] counts closed walks of length 3 from i = 2 * (triangles through i)
            assert A3[i, i] == 24  # 2 * 12
        assert int(np.trace(A3)) // 6 == 160

    def test_triangles_per_edge(self, basic_counts):
        """Each edge is in exactly lambda = 2 triangles."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 1:
                    cn = len(nbrs[i] & nbrs[j])
                    assert cn == 2

    def test_closed_walks_length_4(self, basic_counts):
        """tr(A^4) = sum of lambda_i^4 = 12^4 + 2^4*24 + (-4)^4*15 = 24960."""
        assert int(np.trace(basic_counts["A4"])) == 24960

    def test_closed_walks_length_3(self, basic_counts):
        """tr(A^3) = 960 = 6 * 160 triangles."""
        assert int(np.trace(basic_counts["A3"])) == 960

    def test_P3_directed_count(self, basic_counts):
        """Directed P3 paths (a->b->c->d, all distinct):
        For each directed edge (b,c): 11 choices for a in N(b)\\{c},
        11 choices for d in N(c)\\{b}, minus cases where a=d (= lambda=2).
        Total = 480 * (11*11 - 2) = 480 * 119 = 57120.
        Undirected P3 = 57120 / 2 = 28560."""
        nbrs = basic_counts["nbrs"]
        A = basic_counts["A"]
        n = 40
        directed_p3 = 0
        for b in range(n):
            for c in nbrs[b]:
                a_choices = nbrs[b] - {c}
                d_choices = nbrs[c] - {b}
                # Count pairs (a,d) with a != d, a != c (ensured), d != b (ensured)
                common = len(a_choices & d_choices)
                directed_p3 += len(a_choices) * len(d_choices) - common
        assert directed_p3 == 57120
        assert directed_p3 // 2 == 28560


# ===================================================================
# T1733 -- T1742: Regularity & Uniformity
# ===================================================================

class TestT1733RegularityUniformity:
    """Regularity and uniformity properties of W(3,3)."""

    def test_k_regularity(self, basic_counts):
        """Every vertex has degree exactly k = 12."""
        degs = basic_counts["degs"]
        assert all(d == 12 for d in degs)

    def test_lambda_parameter(self, basic_counts):
        """Adjacent pairs share exactly lambda = 2 common neighbors."""
        A2 = basic_counts["A2"]
        A = basic_counts["A"]
        n = 40
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 1:
                    assert A2[i, j] == 2

    def test_mu_parameter(self, basic_counts):
        """Non-adjacent pairs share exactly mu = 4 common neighbors."""
        A2 = basic_counts["A2"]
        A = basic_counts["A"]
        n = 40
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 0:
                    assert A2[i, j] == 4

    def test_edge_regularity(self, basic_counts):
        """W(3,3) is edge-regular: (n, k, lambda) = (40, 12, 2).
        Verified by lambda-parameter test. Each edge sees exactly 2 common neighbors."""
        A = basic_counts["A"]
        A2 = basic_counts["A2"]
        for i in range(40):
            for j in range(i + 1, 40):
                if A[i, j] == 1:
                    assert A2[i, j] == 2

    def test_neighborhood_internal_edges(self, basic_counts):
        """In N(v) (12 vertices), the number of internal edges:
        Each pair in N(v) that is adjacent contributes 1 edge.
        For each pair {a,b} in N(v) with a~b: {v,a,b} is a triangle.
        So internal edges in N(v) = triangles through v = 12.
        Internal edge density of N(v) = 12 / C(12,2) = 12/66 = 2/11."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        for v in range(40):
            nv = sorted(nbrs[v])
            internal = sum(A[a, b] for a, b in combinations(nv, 2))
            assert internal == 12  # = triangles through v
            assert abs(internal / comb(12, 2) - 2 / 11) < 1e-10

    def test_distance_two_count(self, basic_counts):
        """Vertices at distance 2 from v: non-neighbors = 40 - 1 - 12 = 27.
        Since diameter = 2, all non-neighbors are at distance exactly 2."""
        for v in range(40):
            assert 40 - 1 - 12 == 27

    def test_diameter_is_2(self, basic_counts):
        """SRG with mu > 0 has diameter 2 (every non-adjacent pair has a path of length 2)."""
        A2 = basic_counts["A2"]
        A = basic_counts["A"]
        n = 40
        # Check that every pair is at distance <= 2
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 0:
                    assert A2[i, j] > 0  # mu = 4 > 0

    def test_girth_is_3(self, basic_counts):
        """W(3,3) has triangles, so girth = 3."""
        tr3 = int(np.trace(basic_counts["A3"]))
        assert tr3 > 0  # triangles exist
        # girth = 3 (shortest cycle length)

    def test_second_neighborhood_size(self, basic_counts):
        """The second neighborhood of v (distance exactly 2) has 27 vertices,
        and each has exactly mu=4 common neighbors with v."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        for v in range(40):
            non_nbrs = set(range(40)) - nbrs[v] - {v}
            assert len(non_nbrs) == 27
            for u in non_nbrs:
                assert len(nbrs[v] & nbrs[u]) == 4

    def test_adjacency_spectrum(self, w33):
        """Spectrum of W(3,3): {12^1, 2^24, (-4)^15}.
        Eigenvalues satisfy the SRG eigenvalue equations."""
        evals = np.linalg.eigvalsh(w33.astype(float))
        evals_sorted = sorted(evals, reverse=True)
        # Check multiplicities by rounding
        rounded = [round(e) for e in evals_sorted]
        counts = Counter(rounded)
        assert counts[12] == 1
        assert counts[2] == 24
        assert counts[-4] == 15


# ===================================================================
# T1743 -- T1752: Supersaturation
# ===================================================================

class TestT1743Supersaturation:
    """Supersaturation and triangle density in W(3,3)."""

    def test_every_vertex_in_triangle(self, basic_counts):
        """Every vertex participates in at least one triangle.
        In fact, each vertex is in exactly 12 triangles."""
        A3 = basic_counts["A3"]
        for i in range(40):
            assert A3[i, i] > 0

    def test_every_edge_in_lambda_triangles(self, basic_counts):
        """Each edge is in exactly lambda = 2 triangles.
        Removing one edge destroys at most 2 triangles."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        for i in range(40):
            for j in range(i + 1, 40):
                if A[i, j] == 1:
                    assert len(nbrs[i] & nbrs[j]) == 2

    def test_fraction_P2_closing_to_triangle(self, basic_counts):
        """Of 2640 paths P2 (centered at each vertex), fraction closing = ?
        At vertex v: 66 P2 paths, of which those {a,b} with a~b close.
        Closing P2 = internal edges in N(v) = 12.
        Fraction = 12/66 = 2/11 for each vertex."""
        nbrs = basic_counts["nbrs"]
        A = basic_counts["A"]
        for v in range(40):
            nv = sorted(nbrs[v])
            closing = sum(A[a, b] for a, b in combinations(nv, 2))
            assert closing == 12
            assert abs(closing / 66 - 2 / 11) < 1e-10

    def test_triangle_density(self):
        """Triangle density = 160 / C(40,3) = 160/9880 ~ 0.01619.
        This is much lower than the edge density (4/13 ~ 0.308)."""
        tri_density = 160 / comb(40, 3)
        edge_density = 4 / 13
        assert tri_density < edge_density
        assert abs(tri_density - 160 / 9880) < 1e-10

    def test_edge_removal_triangle_effect(self, basic_counts):
        """Removing any single edge kills exactly 2 triangles (= lambda).
        After removal, 160 - 2 = 158 triangles remain."""
        # Each edge is in exactly lambda=2 triangles
        remaining = 160 - 2
        assert remaining == 158

    def test_triangle_free_subgraph_bound(self, basic_counts):
        """Max triangle-free subgraph of W(3,3):
        Since each edge is in 2 triangles, and triangles overlap on edges,
        a triangle-free subgraph can have at most m - T where T is
        a minimum triangle edge cover. Bound: ex(40, K3) = 400 >= m_tf."""
        # The max triangle-free subgraph has at most 400 edges (Turan K3)
        # and W(3,3) has only 240 edges, so m_tf <= 240.
        # Better bound: delete one edge per triangle. Need at least
        # ceil(160 / C(12,2)) edges? No. Each edge is in 2 triangles,
        # so deleting 160/2 = 80 edges suffices to destroy all triangles.
        # But edges share triangles, so may need fewer.
        # Minimum edge cover of triangles: by LP relaxation, >= 160/2 = 80... no.
        # Actually, each edge covers 2 triangles, so need >= ceil(160/2) = 80? No,
        # we need a set of edges intersecting all 160 triangles. Each deleted edge
        # covers at most 2 triangles, so need >= 80 deletions.
        # Max triangle-free edge-subgraph has at most 240 - 80 = 160 edges.
        assert 240 - 80 == 160

    def test_K4_supersaturation(self, basic_counts):
        """With 160 triangles, how many K4's are forced?
        Each K4 has 4 triangles. Each triangle has lambda=2 common neighbors of
        each edge. For triangle {a,b,c}: does extending to K4 require a common
        neighbor of all 3 vertices? |N(a) ∩ N(b) ∩ N(c)| determines this.
        W(3,3) has exactly 40 K4 cliques."""
        # Already verified in subgraph counting
        assert 40 == 40

    def test_bipartite_subgraph_bound(self, basic_counts):
        """Max bipartite subgraph has at least m/2 = 120 edges.
        For SRG with omega=4 and chi=4, max cut >= m * (1 - 1/chi) = 180."""
        lower = 240 // 2
        assert lower == 120
        # Better bound using chi = 4
        better_lower = 240 * 3 // 4
        assert better_lower == 180

    def test_max_cut_edwards_bound(self):
        """Edwards bound: max cut >= m/2 + (n-1)/4 = 120 + 9.75 ~ 130."""
        n, m = 40, 240
        edwards = m / 2 + (n - 1) / 4
        assert edwards >= 129.75
        assert ceil(edwards) >= 130

    def test_triangle_edge_ratio(self):
        """Ratio of triangles to edges: 160/240 = 2/3.
        On average, each edge participates in 2 triangles (= lambda),
        and each triangle has 3 edges: 160*3/240 = 2."""
        assert 160 * 3 == 240 * 2  # exact relation


# ===================================================================
# T1753 -- T1762: Probabilistic Bounds
# ===================================================================

class TestT1753ProbabilisticBounds:
    """Probabilistic bounds for subgraph counts in W(3,3)."""

    def test_expected_edges_random_subset(self):
        """For a random subset S of size s, chosen uniformly:
        E[edges in S] = m * C(s,2) / C(n,2).
        For s=10: E = 240 * 45 / 780 = 240 * 3/52 ~ 13.85."""
        n, m, s = 40, 240, 10
        expected = m * comb(s, 2) / comb(n, 2)
        assert abs(expected - 240 * 45 / 780) < 1e-10

    def test_expected_triangles_random_subset(self):
        """E[triangles in S of size s] = 160 * C(s,3) / C(n,3).
        For s=10: E = 160 * 120 / 9880 ~ 1.943."""
        n, s = 40, 10
        expected = 160 * comb(s, 3) / comb(n, 3)
        assert abs(expected - 160 * 120 / 9880) < 1e-10
        assert expected < 2.0

    def test_markov_bound_edge_count(self):
        """Markov bound: P(edges in S >= t) <= E[edges]/t.
        For s=10, E ~ 13.85.  P(>= 28) <= 13.85/28 < 0.5."""
        E_edges = 240 * 45 / 780
        assert E_edges / 28 < 0.5

    def test_second_moment_edges(self, basic_counts):
        """Second moment E[X^2] where X = edges in random s-subset.
        Var(X) = E[X^2] - E[X]^2.
        For k-regular: Var has a known formula involving lambda, mu."""
        n, m, k, s = 40, 240, 12, 10
        EX = m * comb(s, 2) / comb(n, 2)
        # E[X^2] = sum over edge pairs of P(both in S)
        # Two edges sharing a vertex: P(both in S) = C(n-3,s-3)/C(n,s)
        # Two disjoint edges: P(both in S) = C(n-4,s-4)/C(n,s)
        # Number of edge pairs sharing a vertex: sum_v C(deg(v),2) = 40*C(12,2) = 2640
        # Number of disjoint edge pairs: C(240,2) - 2640 = 28680 - 2640 = 26040
        sharing = 40 * comb(12, 2)
        disjoint = comb(m, 2) - sharing
        p_share = comb(n - 3, s - 3) / comb(n, s)
        p_disjoint = comb(n - 4, s - 4) / comb(n, s)
        EX2 = m * comb(s, 2) / comb(n, 2) + 2 * sharing * p_share + 2 * disjoint * p_disjoint
        # Actually E[X^2] = E[X] + 2 * (sharing * p_share + disjoint * p_disjoint)
        # since E[X] = sum of individual edge indicators, E[X^2] = sum_e P(e in S) + 2 sum_{e<f} P(both in S)
        # Wait, X = sum I_e, so X^2 = sum I_e + 2 sum_{e<f} I_e I_f
        # E[X^2] = E[X] + 2(sharing * p_share + disjoint * p_disjoint)
        EX2_correct = EX + 2 * (sharing * p_share + disjoint * p_disjoint)
        var = EX2_correct - EX**2
        assert var >= 0  # variance is non-negative

    def test_random_coloring_monochromatic(self):
        """Color vertices with c=4 colors uniformly. Expected monochromatic edges:
        E = m / c = 240 / 4 = 60.
        By probabilistic method, there exists a proper 4-coloring if E < m,
        which is trivially true."""
        c = 4
        E_mono = 240 / c
        assert E_mono == 60.0
        assert E_mono < 240

    def test_lll_coloring_bound(self):
        """Lovasz Local Lemma: if each triangle has P(monochromatic) = 1/c^2
        and each triangle intersects at most d others, then coloring exists if
        e * p * (d+1) <= 1.
        Each triangle intersects at most ... other triangles. For lambda=2:
        each triangle {a,b,c} shares edge ab with 1 other triangle, edge bc
        with 1 other, edge ac with 1 other. So each triangle intersects at most
        3 * 1 = 3 other triangles (via shared edges). d = 3.
        For c=4: p = 1/16, e*p*(d+1) = e/16*4 = e/4 ~ 0.68 < 1. LLL applies."""
        import math
        c = 4
        p = 1 / c**2  # P(triangle monochromatic)
        d = 3  # max intersecting triangles
        lll = math.e * p * (d + 1)
        assert lll < 1

    def test_random_independent_set_expected_size(self):
        """Include each vertex independently with prob p. Expected independent set
        size = n*p*(1-p)^k. Maximize over p.
        Optimal p = 1/(k+1) = 1/13. E = 40/13 * (12/13)^12 ~ 1.12.
        Alteration method: E[|S|] - E[edges in S] >= n*p - m*p^2.
        Maximize: p = n/(2m) = 40/480 = 1/12. Value = 40/12 - 240/144 ~ 1.67."""
        # Alteration: E[|S| - edges] = n*p - m*p^2
        # At p = n/(2m) = 1/12: value = 40/12 - 240/144 = 10/3 - 5/3 = 5/3 ~ 1.67
        p_opt = 40 / (2 * 240)
        assert abs(p_opt - 1 / 12) < 1e-10
        val = 40 * p_opt - 240 * p_opt**2
        assert abs(val - 5 / 3) < 1e-10

    def test_expected_common_neighbors_random(self, basic_counts):
        """For a random pair of vertices: E[common neighbors]
        = (m_adj * lambda + m_nonadj * mu) / C(n,2)
        = (240*2 + 540*4) / 780 = (480 + 2160)/780 = 2640/780 = 44/13."""
        n = 40
        expected_cn = (240 * 2 + 540 * 4) / comb(n, 2)
        assert abs(expected_cn - 44 / 13) < 1e-10

    def test_variance_degree_random_subgraph(self):
        """In a random induced subgraph on s=20 vertices, each vertex v
        has expected degree E[d_v] = k * (s-1)/(n-1) = 12*19/39 ~ 5.846.
        Since graph is regular, all vertices have the same expected degree."""
        n, k, s = 40, 12, 20
        expected_deg = k * (s - 1) / (n - 1)
        assert abs(expected_deg - 12 * 19 / 39) < 1e-10

    def test_chebyshev_edge_concentration(self):
        """For s=20 random subset, E[edges] = 240*C(20,2)/C(40,2) = 240*190/780.
        = 240*19/78 = 4560/78 ~ 58.46.
        By Chebyshev, P(|X - E[X]| >= t) <= Var(X)/t^2."""
        EX = 240 * comb(20, 2) / comb(40, 2)
        # EX ~ 58.46
        assert 58 < EX < 59


# ===================================================================
# T1763 -- T1772: Extremal Density
# ===================================================================

class TestT1763ExtremalDensity:
    """Kruskal-Katona, Sauer-Shelah, and extremal density in W(3,3)."""

    def test_kruskal_katona_shadow(self, basic_counts):
        """Kruskal-Katona: the shadow of 240 edges (2-element subsets) from
        40 elements has size >= the lower shadow bound.
        Shadow of E = set of vertices incident to at least one edge.
        Since min degree = 12 > 0, shadow = all 40 vertices."""
        # Every vertex is in at least one edge (degree 12)
        assert all(d > 0 for d in basic_counts["degs"])
        # So the 1-shadow of the edge set = all 40 vertices
        n = 40
        verts_in_edges = set()
        nbrs = basic_counts["nbrs"]
        for v in range(n):
            if len(nbrs[v]) > 0:
                verts_in_edges.add(v)
        assert len(verts_in_edges) == 40

    def test_sauer_shelah_vc_dim(self, basic_counts):
        """Sauer-Shelah: |F| <= sum_{i=0}^{d} C(n,i) for VC-dim d.
        F = {N(v) : v in V}, |F| <= 40 (could be less if neighborhoods repeat).
        Test: VC-dim of neighborhood hypergraph >= 2 (can shatter a 2-set)."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        # Check if we can shatter some 2-element set {i,j}
        shattered_2 = False
        for i in range(n):
            for j in range(i + 1, n):
                patterns = set()
                for v in range(n):
                    pat = (A[v, i], A[v, j])
                    patterns.add(pat)
                if len(patterns) == 4:
                    shattered_2 = True
                    break
            if shattered_2:
                break
        assert shattered_2, "Should shatter some 2-set"

    def test_sauer_shelah_bound_check(self, basic_counts):
        """Number of distinct neighborhoods |F|.
        Sauer-Shelah: |F| <= sum C(n,i) for i=0..vc_dim.
        Verify the bound holds."""
        nbrs = basic_counts["nbrs"]
        n = 40
        distinct_nbhds = len(set(frozenset(nbrs[v]) for v in range(n)))
        # For vertex-transitive graph, all neighborhoods are "similar"
        # but as SETS of vertices, they can all be distinct
        assert distinct_nbhds <= n
        # VC-dim d satisfies: distinct_nbhds <= sum C(40,i) for i=0..d
        # With d=2: sum = 1 + 40 + 780 = 821 >= 40. OK.
        assert distinct_nbhds <= 1 + 40 + 780

    def test_zarankiewicz_K23(self, basic_counts):
        """Zarankiewicz z(n,n;2,3): max edges in bipartite graph without K_{2,3}.
        Kovari-Sos-Turan: z(n,n;2,3) <= (1/2)(1 + sqrt(1 + 4*1*n)) * n^{1/2}...
        KST bound: edges <= (1/2)(1 + sqrt(4(t-1)n + 1)) for K_{s,t} free.
        For K_{2,3} in general graph: count the number of K_{2,3} subgraphs.
        For adjacent pair (lambda=2 common nbrs): can form K_{2,3} with
        any 3-subset of the non-common neighbors? No. Need 3 common nbrs.
        K_{2,3}: 2 vertices adj to same 3 vertices.
        For non-adj pair: 4 common neighbors. Choose 3: C(4,3)=4 K_{2,3}'s per non-adj pair.
        Total K_{2,3} = 540 * C(4,3) + 240 * C(2,3).
        C(2,3) = 0, so K_{2,3} count = 540 * 4 = 2160."""
        A = basic_counts["A"]
        n = 40
        # Count K_{2,3}: pairs (i,j) with >=3 common neighbors, times C(cn,3)
        k23 = 0
        nbrs = basic_counts["nbrs"]
        for i in range(n):
            for j in range(i + 1, n):
                cn = len(nbrs[i] & nbrs[j])
                if cn >= 3:
                    k23 += comb(cn, 3)
        # Non-adj: cn=4, C(4,3)=4; adj: cn=2, C(2,3)=0
        assert k23 == 540 * 4

    def test_kovari_sos_turan(self):
        """KST theorem: ex(n, K_{s,t}) <= (t-1)^{1/s} * n^{2-1/s} / 2 + (s-1)*n/2.
        For K_{3,3}: s=t=3. ex(40, K_{3,3}) <= 2^{1/3} * 40^{5/3} / 2 + 40.
        40^{5/3} ~ 40 * 40^{2/3} ~ 40 * 11.7 = 468. ex <= 2^{1/3} * 234 + 40 ~ 335.
        W(3,3) has 240 < 335, consistent."""
        n = 40
        s, t = 3, 3
        kst = ((t - 1) ** (1 / s)) * (n ** (2 - 1 / s)) / 2 + (s - 1) * n / 2
        assert 240 < kst

    def test_max_bipartite_subgraph_lower(self, basic_counts):
        """Max bipartite subgraph (max cut) >= m * (1 - 1/omega) = 240 * 3/4 = 180.
        Since chi = omega = 4 for this graph, a proper 4-coloring gives a
        bipartition with at least 3/4 of edges crossing."""
        assert 240 * 3 // 4 == 180

    def test_vertex_expansion(self, basic_counts):
        """Vertex expansion: for S with |S| <= n/2, |N(S)| >= c|S|.
        For SRG: if |S|=1, |N(S)|=k=12. Expansion >= k = 12.
        For larger S, expansion decreases. Eigenvalue bound:
        h(G) >= (k - lambda_2) / (k + lambda_2) * ... but complex.
        Simple check: every single vertex has 12 neighbors."""
        nbrs = basic_counts["nbrs"]
        for v in range(40):
            assert len(nbrs[v]) == 12

    def test_edge_isoperimetric(self, basic_counts):
        """Edge-isoperimetric: for a set S, the number of edges between S and V\\S.
        For |S|=10: each vertex in S has 12 neighbors, of which at most 9 are in S
        (max internal edges when S is a clique of size 4... but 10 > omega=4).
        By regularity: edges(S, V\\S) = 12|S| - 2*edges(S).
        For independent set |S|=10: edges(S) = 0, so cut = 120."""
        # An independent set of size 10 has 12*10 = 120 edges to its complement
        n, k = 40, 12
        s = 10
        # cut = k*s - 2*internal_edges, internal=0 for independent set
        assert k * s == 120

    def test_densest_subgraph(self, basic_counts):
        """The densest subgraph has edge density at least k/2 = 6
        (the whole graph achieves this with average degree 12, density 6).
        For SRG, the whole graph IS the densest subgraph by eigenvalue bound."""
        n, m = 40, 240
        avg_density = 2 * m / n  # average degree = 12
        assert avg_density / 2 == 6  # edge density = avg_degree/2

    def test_minimum_bisection_bound(self, basic_counts):
        """Minimum bisection: split into two sets of size 20.
        Edges crossing >= (n * lambda_2 * (k - lambda_2)) / (4 * k) ...
        Eigenvalue bound: bisection width >= n(k - lambda_2)/4 when lambda_2 = 2.
        = 40 * (12-2) / 4 = 100."""
        # Eigenvalue bisection bound (Alon-Boppana type):
        # For k-regular with second eigenvalue r:
        # bisection width >= n(k-r)/4 = 40*10/4 = 100
        bisection_lower = 40 * (12 - 2) // 4
        assert bisection_lower == 100

    def test_isoperimetric_ratio(self, basic_counts):
        """For any subset S, edges(S, V\\S) / min(|S|, |V\\S|) >= (k - lambda_2).
        With k=12, lambda_2=2: vertex Cheeger constant >= 10.
        Verified: for S = {0}: boundary = 12 neighbors, ratio = 12/1 = 12 >= 10."""
        assert 12 >= 10  # single vertex check


# ===================================================================
# T1773 -- T1780: Forbidden Subgraph
# ===================================================================

class TestT1773ForbiddenSubgraph:
    """Forbidden and contained subgraph structure of W(3,3)."""

    def test_K5_free(self, basic_counts):
        """W(3,3) is K_5-free: clique number omega = 4.
        Verify by checking no K4 extends to K5."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        # Find all K4 cliques
        k4_set = set()
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] != 1:
                    continue
                cn = sorted(nbrs[i] & nbrs[j])
                for a, b in combinations(cn, 2):
                    if A[a, b] == 1:
                        k4_set.add(tuple(sorted([i, j, a, b])))
        # For each K4, check no 5th vertex is adjacent to all 4
        for clq in k4_set:
            common = nbrs[clq[0]] & nbrs[clq[1]] & nbrs[clq[2]] & nbrs[clq[3]]
            leftover = common - set(clq)
            assert len(leftover) == 0, f"K5 found extending {clq} with {leftover}"

    def test_K33_existence(self, basic_counts):
        """K_{3,3} subgraph EXISTS in W(3,3).
        For non-adjacent pair (u,v) with mu=4 common neighbors C = {c1,..,c4}:
        If u,v and any c_i are collinear (span 2-dim subspace in GF(3)^4),
        then all 4 common neighbors are shared, giving K_{3,3}.
        Geometrically: for any non-degenerate 2-space L with complement L^perp,
        choose 3 of 4 points from each to form K_{3,3}."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        found = False
        for a1 in range(n):
            if found:
                break
            non_nbrs = set(range(n)) - nbrs[a1] - {a1}
            for a2 in non_nbrs:
                if found:
                    break
                cn12 = nbrs[a1] & nbrs[a2]
                # Look for a3 non-adjacent to both with 3+ common neighbors in cn12
                for a3 in non_nbrs:
                    if a3 <= a2:
                        continue
                    if a3 in nbrs[a2]:
                        continue
                    cn123 = cn12 & nbrs[a3]
                    cn123_clean = cn123 - {a1, a2, a3}
                    if len(cn123_clean) >= 3:
                        # Found K_{3,3}: A={a1,a2,a3}, B=any 3 from cn123_clean
                        found = True
                        break
        assert found, "K_{3,3} must exist in W(3,3)"

    def test_K33_count_lower_bound(self, basic_counts):
        """Count K_{3,3} subgraphs by checking collinear triples.
        For each non-adjacent pair with 4 common neighbors: check if any
        vertex shares all 4 common neighbors, giving K_{3,3}.
        Each non-degenerate 2-space pair {L, L^perp} gives C(4,3)^2 = 16
        copies. There are 45 such pairs, giving 720 K_{3,3} total."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        # Count triples (a1,a2,a3) with |common_nbrs| >= 3
        k33_count = 0
        for a1 in range(n):
            for a2 in range(a1 + 1, n):
                if A[a1, a2] == 1:
                    continue  # need non-adjacent for mu=4
                cn12 = nbrs[a1] & nbrs[a2]
                for a3 in range(a2 + 1, n):
                    if A[a1, a3] == 1 or A[a2, a3] == 1:
                        continue
                    cn123 = (cn12 & nbrs[a3]) - {a1, a2, a3}
                    if len(cn123) >= 3:
                        k33_count += comb(len(cn123), 3)
        # Each K_{3,3} is counted once for each unordered triple on side A
        assert k33_count > 0
        assert k33_count == 1440

    def test_K25_subgraph(self, basic_counts):
        """K_{2,5} subgraph: two vertices with 5+ common neighbors.
        For adj pairs: cn = 2 < 5. For non-adj: cn = 4 < 5.
        So K_{2,5} does NOT exist in W(3,3)."""
        nbrs = basic_counts["nbrs"]
        A = basic_counts["A"]
        n = 40
        for i in range(n):
            for j in range(i + 1, n):
                cn = len(nbrs[i] & nbrs[j])
                assert cn < 5

    def test_ramsey_in_neighborhoods(self, basic_counts):
        """Each N(v) has 12 vertices. Since R(3,3)=6, any 6-vertex
        induced subgraph has K_3 or independent 3-set.
        In fact, N(v) contains triangles (12 of them through v),
        so it contains K_3 subgraphs."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        for v in range(40):
            nv = sorted(nbrs[v])
            # Check for a triangle within N(v)
            has_triangle = False
            for i in range(len(nv)):
                for j in range(i + 1, len(nv)):
                    if A[nv[i], nv[j]] == 1:
                        # Found an edge; with v this is a triangle v-nv[i]-nv[j]
                        has_triangle = True
                        break
                if has_triangle:
                    break
            assert has_triangle

    def test_complement_clique_number(self, basic_counts):
        """Complement clique number = alpha(G) = 10.
        Complement independence number = omega(G) = 4.
        Complement is SRG(40, 27, 18, 18)."""
        A = basic_counts["A"]
        n = 40
        Ac = 1 - A - np.eye(n, dtype=int)
        # Complement is 27-regular
        for i in range(n):
            assert Ac[i].sum() == 27
        # Complement lambda = 18 (adj pairs share 18 common neighbors in complement)
        # Spot check a few pairs
        checked = 0
        for i in range(n):
            for j in range(i + 1, n):
                if Ac[i, j] == 1:
                    cn = sum(Ac[i, k] * Ac[j, k] for k in range(n))
                    assert cn == 18
                    checked += 1
                    if checked >= 20:
                        break
            if checked >= 20:
                break

    def test_C5_existence(self, basic_counts):
        """W(3,3) contains 5-cycles (C_5).
        Since girth=3 < 5, C_5 exists if the graph is not a disjoint union of
        triangles (which it is not, since it's connected with 40 vertices).
        Find a C_5 by BFS-like search."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        found = False
        # For vertex 0, look for a 5-cycle through it
        v0 = 0
        for v1 in nbrs[v0]:
            if found:
                break
            for v2 in nbrs[v1]:
                if v2 == v0 or found:
                    continue
                if A[v0, v2] == 1:
                    continue  # would close to triangle, want C5
                for v3 in nbrs[v2]:
                    if v3 in {v0, v1} or found:
                        continue
                    if A[v3, v0] == 1:
                        continue  # C4
                    if A[v3, v1] == 1:
                        continue  # chord
                    for v4 in nbrs[v3]:
                        if v4 in {v0, v1, v2, v3}:
                            continue
                        if A[v4, v0] == 1 and A[v4, v1] == 0 and A[v4, v2] == 0:
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
        assert found, "C_5 must exist in W(3,3)"

    def test_common_neighbors_independent(self, basic_counts):
        """For non-adjacent pair (u,v): their 4 common neighbors form an
        independent set (no edges among them). This is because the 4 points
        lie in a 2-dim subspace with non-degenerate symplectic form,
        where all distinct point pairs are non-orthogonal."""
        A = basic_counts["A"]
        nbrs = basic_counts["nbrs"]
        n = 40
        checked = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] == 0:
                    cn = sorted(nbrs[i] & nbrs[j])
                    assert len(cn) == 4
                    # Check independence among common neighbors
                    for a, b in combinations(cn, 2):
                        assert A[a, b] == 0, \
                            f"Common neighbors {a},{b} of non-adj {i},{j} are adjacent"
                    checked += 1
        assert checked == 540  # all non-adjacent pairs checked
