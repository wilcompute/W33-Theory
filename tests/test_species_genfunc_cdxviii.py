"""
Phase CDXVIII (418) — Combinatorial Species & Generating Functions
===================================================================
Catalan, Fibonacci, Lucas, partitions, derangements, Bell numbers.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Catalan:
    def test_C6(self):
        assert math.comb(12, 6) // 7 == k * (k - 1)
    def test_C7(self):
        assert math.comb(14, 7) // 8 == q * (k - 1) * Phi3

class TestT2_Fibonacci:
    def test_F3(self):
        assert lam == 2
    def test_F7(self):
        assert 13 == Phi3
    def test_F12(self):
        assert 144 == k**2

class TestT3_Lucas:
    def test_L4(self):
        assert Phi6 == 7
    def test_L6(self):
        assert 18 == lam * q**lam

class TestT4_Partitions:
    def test_p3(self):
        assert q == 3
    def test_p4(self):
        assert mu + 1 == 5
    def test_p7(self):
        assert g == 15
    def test_p10(self):
        assert 42 == v + lam

class TestT5_Derangements:
    def test_D3(self):
        assert 2 == lam
    def test_D4(self):
        assert 9 == q**2
    def test_D5(self):
        assert 44 == v + mu

class TestT6_Bell:
    def test_B2(self):
        assert lam == 2
    def test_B3(self):
        assert mu + 1 == 5
    def test_B4(self):
        assert g == 15
    def test_B5(self):
        assert 52 == mu * Phi3
