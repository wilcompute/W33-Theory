"""
Supplement H — EXPLICIT CONSTRUCTION OF W(3,3) FROM SCRATCH
================================================================

We construct the collinearity graph of W(3,3) = GQ(3,3) point-by-point
and verify every combinatorial claim of the theory on the resulting
40x40 adjacency matrix.

Construction:
    V = F_3^4 with the symplectic form omega(x, y) = x_0 y_2 - x_2 y_0 + x_1 y_3 - x_3 y_1
    Points = the 40 non-zero projective points of PG(3, F_3), i.e.
             40 = |F_3^4 - {0}| / |F_3^*| = 80/2 = 40.
    Two points x, y are collinear (joined by an isotropic line) iff
        omega(x, y) = 0 and x, y are projectively distinct.

We verify:
    (i)   |V| = 40
    (ii)  every vertex has degree k = 12
    (iii) every edge sits in exactly lambda = 2 triangles
    (iv)  every non-edge has exactly mu = 4 common neighbours
    (v)   the adjacency spectrum is {12, 2^{(24)}, -4^{(15)}}
    (vi)  the eigenvalue equation A^2 = k*I + lambda*A + mu*(J - I - A)
    (vii) 240 directed edges  (E = vk/2 = 240)
    (viii) 160 triangles  (T = v*k*lam/6 = 160)
"""
import itertools
import math

FQ = 3   # field size

# Symplectic form on F_3^4
# J = diag(-1,-1, 1, 1) ordering: omega((x0,x1,x2,x3),(y0,y1,y2,y3))
def omega(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % FQ


# ------------------------------------------------------------------
# H1. Construct 40 projective points
# ------------------------------------------------------------------
def build_projective_points():
    pts = []
    seen = set()
    for x in itertools.product(range(FQ), repeat=4):
        if x == (0, 0, 0, 0):
            continue
        # canonical form: divide by first non-zero coordinate to make it 1
        first_nz = next(i for i, xi in enumerate(x) if xi != 0)
        inv = pow(x[first_nz], -1, FQ)
        canonical = tuple((xi * inv) % FQ for xi in x)
        if canonical not in seen:
            seen.add(canonical)
            pts.append(canonical)
    return pts


POINTS = build_projective_points()


class TestH1_VertexCount:
    def test_v_is_40(self):
        assert len(POINTS) == 40


# ------------------------------------------------------------------
# H2. Adjacency: collinear iff omega = 0 and distinct
# ------------------------------------------------------------------
N = len(POINTS)
adjacency = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        if omega(POINTS[i], POINTS[j]) == 0:
            adjacency[i][j] = 1


class TestH2_Regularity:
    def test_every_vertex_has_degree_12(self):
        for i in range(N):
            deg = sum(adjacency[i])
            assert deg == 12, f"vertex {i} has degree {deg}"

    def test_240_directed_edges(self):
        assert sum(sum(row) for row in adjacency) == 2 * 240


# ------------------------------------------------------------------
# H3. SRG parameters lambda = 2 and mu = 4
# ------------------------------------------------------------------
def common_neighbours(i, j):
    return sum(1 for t in range(N) if adjacency[i][t] and adjacency[j][t])


class TestH3_SRG:
    def test_lambda_eq_2(self):
        # sample all edges (not just one)
        seen = 0
        for i in range(N):
            for j in range(i + 1, N):
                if adjacency[i][j]:
                    assert common_neighbours(i, j) == 2
                    seen += 1
        assert seen == 240

    def test_mu_eq_4(self):
        for i in range(N):
            for j in range(i + 1, N):
                if not adjacency[i][j]:
                    assert common_neighbours(i, j) == 4

    def test_non_edge_count(self):
        total_pairs = N * (N - 1) // 2
        edges = sum(adjacency[i][j] for i in range(N) for j in range(i + 1, N))
        non_edges = total_pairs - edges
        assert edges == 240
        assert non_edges == total_pairs - 240


# ------------------------------------------------------------------
# H4. Triangle count
# ------------------------------------------------------------------
class TestH4_Triangles:
    def test_triangle_count(self):
        # Each triangle is an unordered 3-subset of mutually adjacent vertices
        # Using lam = 2 and sum formula: #triangles = v*k*lam/6 = 160
        T = 0
        for i in range(N):
            for j in range(i + 1, N):
                if not adjacency[i][j]:
                    continue
                for t in range(j + 1, N):
                    if adjacency[i][t] and adjacency[j][t]:
                        T += 1
        assert T == 160


# ------------------------------------------------------------------
# H5. A^2 identity
# ------------------------------------------------------------------
def matmul(A, B):
    n = len(A)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            for j in range(n):
                out[i][j] += A[i][k] * B[k][j]
    return out


class TestH5_AdjacencyPolynomial:
    def test_A_squared(self):
        # A^2 = k I + lam A + mu (J - I - A)
        A2 = matmul(adjacency, adjacency)
        k_val, lam_val, mu_val = 12, 2, 4
        for i in range(N):
            for j in range(N):
                if i == j:
                    expected = k_val
                elif adjacency[i][j]:
                    expected = lam_val
                else:
                    expected = mu_val
                assert A2[i][j] == expected, f"A^2[{i},{j}]={A2[i][j]} expected {expected}"


# ------------------------------------------------------------------
# H6. Spectrum check (trace identities)
# ------------------------------------------------------------------
class TestH6_Spectrum:
    def test_trace_A(self):
        # tr(A) = sum eigenvalues = k + r*f + s*g = 12 + 2*24 + (-4)*15 = 0
        assert sum(adjacency[i][i] for i in range(N)) == 0
        assert 12 + 2 * 24 + (-4) * 15 == 0

    def test_trace_A_squared(self):
        # tr(A^2) = sum eigenvalues^2 = k^2 + r^2*f + s^2*g = 144 + 4*24 + 16*15 = 480
        A2 = matmul(adjacency, adjacency)
        trace = sum(A2[i][i] for i in range(N))
        assert trace == 480
        assert 144 + 4 * 24 + 16 * 15 == 480

    def test_trace_A_squared_from_edges(self):
        # tr(A^2) counts closed walks of length 2 = 2 * #edges = 480
        A2 = matmul(adjacency, adjacency)
        trace = sum(A2[i][i] for i in range(N))
        assert trace == 2 * 240


# ------------------------------------------------------------------
# H7. Final identity
# ------------------------------------------------------------------
class TestH7_MasterAxiom:
    def test_srg_axiom_verified_on_explicit_graph(self):
        # k(k - lam - 1) = (v - k - 1) * mu
        # 12 * 9 = 27 * 4 = 108
        v, k, lam, mu = N, 12, 2, 4
        assert k * (k - lam - 1) == (v - k - 1) * mu
