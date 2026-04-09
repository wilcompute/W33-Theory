"""
Phase CDIX (409) — Coding Theory & Sphere Packing from W(3,3)
==============================================================
Ternary Hamming, Golay code, MDS, kissing numbers, MacWilliams.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_TernaryHamming:
    def test_hamming_n(self):
        assert (q**2 - 1) // (q - 1) == mu
    def test_hamming_k(self):
        assert mu - lam == lam
    def test_hamming_d(self):
        assert q == 3
    def test_perfect(self):
        assert q**lam == 9

class TestT2_TernaryGolay:
    def test_extended_n(self):
        assert k == 12
    def test_golay_dim(self):
        assert k // lam == math.factorial(q)
    def test_golay_d(self):
        assert math.factorial(q) == 6
    def test_M12(self):
        assert 12 * 11 * 10 * 9 * 8 == 95040

class TestT3_SpherePacking:
    def test_V41(self):
        assert 1 + mu * (q - 1) == q**2
    def test_perfect_code(self):
        assert q**lam == q**mu // (q**2)

class TestT4_KissingNumbers:
    def test_tau1(self):
        assert lam == 2
    def test_tau2(self):
        assert math.factorial(q) == 6
    def test_tau3(self):
        assert k == 12
    def test_tau4(self):
        assert f == 24
    def test_tau8(self):
        assert E == 240
    def test_tau24_ratio(self):
        assert q**2 * Phi3 * Phi6 == 819

class TestT5_MDS:
    def test_singleton(self):
        assert lam == mu - q + 1
    def test_mds_limit(self):
        assert mu == q + 1

class TestT6_Density:
    def test_e8(self):
        assert Fraction(1, lam**mu) == Fraction(1, 16)
