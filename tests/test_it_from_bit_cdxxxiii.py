"""
Phase CDXXXIII (433) — It from Bit: Wheeler's Program
=====================================================
Landauer, Kolmogorov complexity, logical depth, observer-participancy.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_BinaryDecomposition:
    def test_bits_v(self):
        assert math.ceil(math.log2(v + 1)) == math.factorial(q)

    def test_bits_k(self):
        assert math.ceil(math.log2(k + 1)) == mu

    def test_bits_E(self):
        assert math.ceil(math.log2(E + 1)) == lam ** q


class TestT2_Landauer:
    def test_total_bits(self):
        assert v == 40

    def test_entangled_bits(self):
        assert E == 240

    def test_ratio(self):
        assert Fraction(E, v) == Fraction(k, lam)


class TestT3_Kolmogorov:
    def test_upper_bound(self):
        K = (math.ceil(math.log2(v + 1)) +
             math.ceil(math.log2(k + 1)) +
             math.ceil(math.log2(lam + 2)) +
             math.ceil(math.log2(mu + 1)))
        assert K == g

    def test_compression(self):
        assert E // g == mu ** lam


class TestT4_LogicalDepth:
    def test_v_squared(self):
        assert v ** 2 == 1600

    def test_depth_ratio(self):
        assert Fraction(v ** 2, E) == Fraction(v, lam * q)


class TestT5_Observer:
    def test_factorial(self):
        assert math.factorial(q + 1) == f

    def test_binomial(self):
        qf = math.factorial(q)
        assert math.factorial(qf) // (math.factorial(lam) * math.factorial(qf - lam)) == g

    def test_total(self):
        assert 1 + f + g == v


class TestT6_Digital:
    def test_all_integer(self):
        assert all(isinstance(x, int) for x in [v, k, lam, mu, r, s, f, g])

    def test_minimal_poly(self):
        coeffs = [1, -(k + r + s), k*r + k*s + r*s, -(k*r*s)]
        assert coeffs == [1, -10, -32, 96]
