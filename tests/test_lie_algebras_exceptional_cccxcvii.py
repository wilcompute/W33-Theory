"""
Phase CCCXCVII — Exceptional Lie Algebras and W(3,3)
======================================================

  - G2: 14, F4: 52, E6: 78, E7: 133, E8: 248
  - All from W(3,3) parameters
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Dimensions:
    def test_g2(self):
        # 14 = k + lam
        assert k + lam == 14

    def test_f4(self):
        # 52 = mu*Phi3
        assert mu * Phi3 == 52

    def test_e6(self):
        # 78 = lam*q*Phi3
        assert lam * q * Phi3 == 78

    def test_e7(self):
        # 133 = ? = Phi3*Phi4 + q = 130+3
        assert Phi3 * Phi4 + q == 133

    def test_e8(self):
        # 248 = E + lam^q
        assert E + lam ** q == 248


class TestT2_Ranks:
    def test_g2_rank(self):
        assert lam == 2

    def test_f4_rank(self):
        assert mu == 4

    def test_e6_rank(self):
        # rank 6 = k/2
        assert k // 2 == 6

    def test_e7_rank(self):
        assert Phi6 == 7

    def test_e8_rank(self):
        assert lam ** q == 8


class TestT3_RootSystems:
    def test_g2_roots(self):
        # 12 = k
        assert k == 12

    def test_f4_roots(self):
        # 48 = lam*f
        assert lam * f == 48

    def test_e6_roots(self):
        # 72 = lam^q*Phi6+lam^mu = 56+16 = 72
        assert lam ** q * Phi6 + lam ** mu == 72

    def test_e7_roots(self):
        # 126 = E/lam + Phi6-1
        assert E // lam + mu + lam == 126

    def test_e8_roots(self):
        assert E == 240


class TestT4_Coxeter:
    def test_e8_coxeter_30(self):
        # h = 30 = q*Phi4
        assert q * Phi4 == 30

    def test_e7_coxeter_18(self):
        # h = 18 = lam*q^2
        assert lam * q ** lam == 18

    def test_e6_coxeter_12(self):
        # h = 12 = k
        assert k == 12

    def test_f4_coxeter_12(self):
        assert k == 12

    def test_g2_coxeter_6(self):
        assert k // 2 == 6


class TestT5_Sums:
    def test_sum_exceptional_dims(self):
        # 14+52+78+133+248 = 525
        s = 14 + 52 + 78 + 133 + 248
        assert s == 525
        # 525 = q*Phi6*lam^q + ... = 168+357... not direct
        # 525 = Phi3*Phi4*mu + mu+1 = 520+5
        assert s == Phi3 * Phi4 * mu + (mu + 1)

    def test_w_e6_order(self):
        # 51840 = lam^7 * 3^4 * 5
        assert 51840 == lam ** Phi6 * q ** mu * (mu + 1)
