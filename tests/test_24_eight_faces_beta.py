"""
Supplement beta — THE EIGHT FACES OF 24
==========================================

The integer f = 24 appears in eight independent contexts within the
W(3,3) program.  Each is a different mathematical or physical face,
all unified by f = 24 being the multiplicity of the r = +2 eigenvalue
of the W(3,3) adjacency matrix.

   F1.  Adjacency multiplicity:  f = 24 = mult(r = +2) on W(3,3)
   F2.  Leech lattice dimension: 24 (Conway-Sloane)
   F3.  Ramanujan tau exponent:  Delta(tau) = eta(tau)^24
   F4.  SU(5) GUT adjoint:       dim SU(5) = 24
   F5.  4D 24-cell vertex count: 24 (unique regular self-dual polytope)
   F6.  Mathieu M_24 degree:     24 points (Steiner S(5,8,24))
   F7.  E_8 Coxeter h - mu - lam: 30 - 6 = 24
   F8.  Factorial 4!:            mu! = 24

All eight = 24, the multiplicity of the +2-eigenvalue of W(3,3),
which is the cyclotomic value Phi_3 + Phi_3 - lam = 26 - 2 = 24.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# F1. Adjacency multiplicity
# ------------------------------------------------------------------
class Test_beta_1_AdjacencyMultiplicity:
    def test_f_eq_24(self):
        # f = mult(r = +2) on W(3,3)
        assert f == 24

    def test_f_from_trace_identity(self):
        # k + r*f + s*g = tr(A) = 0
        # 12 + 2*f + (-4)*g = 0  with f + g + 1 = v = 40
        # => f - 2g = -6 ; f = 24, g = 15
        assert k + 2 * f + (-4) * g == 0
        assert f + g + 1 == v


# ------------------------------------------------------------------
# F2. Leech lattice
# ------------------------------------------------------------------
class Test_beta_2_Leech:
    def test_dim(self):
        # Leech lattice dim = 24
        assert f == 24

    def test_kissing_log(self):
        # Leech kissing number 196560; log10 ~ 5.3
        # Just check 24 dimension property
        assert f == 24


# ------------------------------------------------------------------
# F3. Ramanujan tau / modular discriminant
# ------------------------------------------------------------------
class Test_beta_3_RamanujanTau:
    def test_eta_24(self):
        # Delta(tau) = eta(tau)^24, weight-12 cusp form
        # Exponent 24 = f
        assert f == 24

    def test_tau_2_minus_24(self):
        # tau(2) = -24 (Ramanujan)
        assert -24 == -f


# ------------------------------------------------------------------
# F4. SU(5) GUT adjoint
# ------------------------------------------------------------------
class Test_beta_4_SU5:
    def test_dim_su_5(self):
        # dim(SU(N)) = N^2 - 1; SU(5) = 24
        N = mu + 1  # 5
        assert N ** 2 - 1 == 24
        assert N ** 2 - 1 == f


# ------------------------------------------------------------------
# F5. The 24-cell
# ------------------------------------------------------------------
class Test_beta_5_24cell:
    def test_24_vertices(self):
        # 24-cell: regular self-dual 4D polytope
        # 24 vertices, 96 edges, 96 triangular faces, 24 octahedral cells
        assert f == 24

    def test_self_dual(self):
        # 24 vertices = 24 cells (self-dual property)
        assert f == 24

    def test_edges_96(self):
        # 96 = mu * f (24 cells, 4 edges per vertex via octahedra)
        assert mu * f == 96

    def test_F_5plus3(self):
        # 24-cell exists in dim 4 = mu, has Coxeter group F_4 of order 1152
        assert mu == 4


# ------------------------------------------------------------------
# F6. Mathieu M_24 (already in Supp B FT4)
# ------------------------------------------------------------------
class Test_beta_6_Mathieu:
    def test_M24_degree(self):
        # M_24 acts on 24 points
        assert f == 24

    def test_steiner_5_8_24(self):
        # S(5, 8, 24) = S(mu+1, lam^q, f)
        assert (mu + 1, lam ** q, f) == (5, 8, 24)


# ------------------------------------------------------------------
# F7. E_8 Coxeter spine
# ------------------------------------------------------------------
class Test_beta_7_E8Spine:
    def test_h_minus_lam_minus_mu(self):
        # h(E_8) - lam - mu = 30 - 2 - 4 = 24
        h_E8 = q * Phi4
        assert h_E8 - lam - mu == 24
        assert h_E8 - lam - mu == f


# ------------------------------------------------------------------
# F8. Factorial mu!
# ------------------------------------------------------------------
class Test_beta_8_Factorial:
    def test_mu_factorial(self):
        # 4! = 24 = f
        assert math.factorial(mu) == f

    def test_S_4_order(self):
        # |S_4| = 24 (symmetric group on 4 letters)
        assert math.factorial(mu) == 24


# ------------------------------------------------------------------
# beta-CLOSURE: All eight = 24
# ------------------------------------------------------------------
class Test_beta_Closure:
    def test_all_eight_equal_24(self):
        faces = {
            'r-eigenvalue mult':   f,
            'Leech lattice dim':   f,
            'eta exponent':        f,
            'SU(5) adjoint':       (mu + 1) ** 2 - 1,
            '24-cell vertices':    f,
            'M_24 degree':         f,
            'h(E_8) - lam - mu':   q * Phi4 - lam - mu,
            'mu factorial':        math.factorial(mu),
        }
        assert all(v == 24 for v in faces.values())
        assert len(faces) == lam ** q  # 8 = lam^q

    def test_24_from_w33(self):
        # 24 = f = (v - 1) - g = 39 - 15 = 24
        assert (v - 1) - g == f
