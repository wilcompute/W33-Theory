"""
Phase CDXXII (422) — Distance-Regular Graphs & Association Schemes II
=====================================================================
Intersection array, Krein parameters, eigenmatrices,
distance distribution, Leonard pairs.
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_IntersectionArray:
    def test_b0(self):
        assert k == 12

    def test_b1(self):
        assert k - lam - 1 == q ** 2

    def test_c1(self):
        assert 1 == 1

    def test_c2(self):
        assert mu == 4

    def test_a1(self):
        assert k - (k - lam - 1) - 1 == lam

    def test_a2(self):
        assert k - mu == lam ** q


class TestT2_DistanceDistribution:
    def test_k0(self):
        assert 1 == 1

    def test_k1(self):
        assert k == 12

    def test_k2(self):
        assert v - k - 1 == q ** q

    def test_balance(self):
        assert k * (k - lam - 1) == (v - k - 1) * mu


class TestT3_KreinParameters:
    def test_krein1(self):
        LHS = r ** 2 * (s + 1) ** 2
        RHS = k * s ** 2 * (r + 1)
        assert LHS <= RHS

    def test_krein2_tight(self):
        LHS = s ** 2 * (r + 1) ** 2
        RHS = k * r ** 2 * (abs(s) - 1)
        assert LHS == RHS


class TestT4_Eigenmatrix:
    def test_P1(self):
        assert -(r + 1) == -3

    def test_P2(self):
        assert -(s + 1) == 3

    def test_row_sum_1(self):
        assert 1 + r - (r + 1) == 0

    def test_row_sum_2(self):
        assert 1 + s - (s + 1) == 0


class TestT5_QMatrix:
    def test_Q11(self):
        assert Fraction(f * r, k) == 4

    def test_Q12(self):
        assert Fraction(f * (-(r + 1)), v - k - 1) == Fraction(-8, 3)

    def test_Q21(self):
        assert Fraction(g * s, k) == -5

    def test_Q22(self):
        assert Fraction(g * (-(s + 1)), v - k - 1) == Fraction(5, 3)
