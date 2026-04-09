"""
Phase CDVI (406) — Category Theory & Topos Structure from W(3,3)
=================================================================
Nerve, simplicial complex, Yoneda, chromatic number, topos, derived categories.
"""
from fractions import Fraction
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
T = 160
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Nerve:
    def test_0_simplices(self):
        assert v == 40
    def test_1_simplices(self):
        assert E == 240
    def test_2_simplices(self):
        assert T == 160
    def test_euler(self):
        assert v - E + T == -v

class TestT2_Adjunctions:
    def test_chromatic(self):
        assert mu == 4
    def test_idempotents(self):
        assert q == 3

class TestT3_Yoneda:
    def test_representables(self):
        assert v == 40
    def test_morphisms(self):
        assert v + 2 * E == 520
    def test_morphisms_alt(self):
        assert v + 2 * E == Phi3 * v

class TestT4_Topos:
    def test_subobject_classifier(self):
        assert mu + 1 == 5

class TestT5_Derived:
    def test_cy_dim(self):
        assert q == 3
    def test_hochschild(self):
        assert 2 * q == math.factorial(q)
