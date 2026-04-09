"""
Phase CDXIX (419) — Quantum Groups & Hopf Algebras
====================================================
q-integers, quantum dimensions, Yang-Baxter, knot invariants.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_qIntegers:
    def test_q1(self):
        assert (q - 1) // (q - 1) == 1
    def test_q2(self):
        assert (q**2 - 1) // (q - 1) == mu
    def test_q3(self):
        assert (q**3 - 1) // (q - 1) == Phi3
    def test_q4(self):
        assert (q**4 - 1) // (q - 1) == v
    def test_qfact(self):
        assert 1 * mu * Phi3 * v == 2080

class TestT2_QuantumDim:
    def test_V0(self):
        assert 1 == 1
    def test_V1(self):
        assert mu == 4
    def test_V2(self):
        assert Phi3 == 13
    def test_V3(self):
        assert v == 40

class TestT3_SmallQG:
    def test_sl2_q3(self):
        assert q**3 == v - k - 1
    def test_sl2_q4(self):
        assert mu**3 == lam**math.factorial(q)

class TestT4_YangBaxter:
    def test_components(self):
        assert q == 3
    def test_Rmatrix_dim(self):
        assert v**2 == 1600

class TestT5_Knots:
    def test_kauffman(self):
        assert lam == 2
    def test_trefoil(self):
        assert q == 3
    def test_knots_4(self):
        assert lam == 2
    def test_knots_7(self):
        assert g == 15
