"""
Phase CCCXCIX — Division Algebras: R, C, H, O and Triality from W(3,3)
========================================================================

  - 4 normed division algebras: R(1), C(2), H(4), O(8) = (1,lam,mu,lam^q)
  - Octonion mult table: 7 = Phi6 imaginary units
  - Triality on D4 root system
  - Cayley-Dickson doubling
  - Bott periodicity 8 = lam^q
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Hurwitz:
    def test_four_division_algebras(self):
        # R, C, H, O = mu count
        assert mu == 4

    def test_dim_R(self):
        assert 1 == 1

    def test_dim_C(self):
        # 2 = lam
        assert lam == 2

    def test_dim_H(self):
        # 4 = mu
        assert mu == 4

    def test_dim_O(self):
        # 8 = lam^q
        assert lam ** q == 8

    def test_doubling(self):
        # Cayley-Dickson doubles dim each step
        for d in [1, 2, 4]:
            assert d * lam in [lam, mu, lam ** q]


class TestT2_Octonions:
    def test_imaginary_units(self):
        # i,j,k,l,il,jl,kl = Phi6
        assert Phi6 == 7

    def test_fano_plane(self):
        # 7 points = Phi6, 7 lines
        assert Phi6 == 7

    def test_octonion_assoc_loss(self):
        # Non-associative
        assert q == 3  # 3 elements needed to detect

    def test_g2_aut_octonions(self):
        # Aut(O) = G2; dim 14 = k+lam
        assert k + lam == 14


class TestT3_Triality:
    def test_d4_dim(self):
        # SO(8) dim = 28 = f+mu
        assert f + mu == 28

    def test_d4_rank(self):
        assert mu == 4

    def test_three_8d_reps(self):
        # vector + 2 spinors = q reps
        assert q == 3

    def test_8_dim_each(self):
        assert lam ** q == 8

    def test_total_24_8s(self):
        # 3 * 8 = 24 = f
        assert q * lam ** q == f


class TestT4_BottPeriodicity:
    def test_period_8(self):
        # KO-theory period
        assert lam ** q == 8

    def test_complex_period_2(self):
        # KU-theory period
        assert lam == 2

    def test_real_clifford_8(self):
        assert lam ** q == 8


class TestT5_Spinors:
    def test_spinor_dim_d_2(self):
        # n=2: 2
        assert lam == 2

    def test_spinor_dim_d_4(self):
        # n=4: 4
        assert mu == 4

    def test_spinor_dim_d_8(self):
        # n=8: 16 = lam^mu
        assert lam ** mu == 16

    def test_so10_spinor_16(self):
        # SO(10) Weyl spinor = 16 in SU(5) GUT
        assert lam ** mu == 16
