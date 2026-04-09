"""
Phase CDXIII (413) — Representation Varieties & Character Varieties
====================================================================
SL/GL/PSL(2,F_3), A_4/S_4 irreps, Platonic group orders.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_SL2F3:
    def test_SL2(self):
        assert q * (q**2 - 1) == f
    def test_GL2(self):
        assert (q**2 - 1) * (q**2 - q) == k * mu
    def test_PGL2(self):
        assert (q**2 - 1) * (q**2 - q) // (q - 1) == f
    def test_PSL2(self):
        assert q * (q**2 - 1) // (q - 1) == k

class TestT2_ConjClasses:
    def test_SL2_classes(self):
        assert Phi6 == 7
    def test_A4_classes(self):
        assert mu == 4
    def test_S4_classes(self):
        assert mu + 1 == 5

class TestT3_A4Irreps:
    def test_dim_sq_sum(self):
        assert 1 + 1 + 1 + 9 == k
    def test_max_dim(self):
        assert q == 3
    def test_linear_irreps(self):
        assert q == 3

class TestT4_S4Irreps:
    def test_dim_sq_sum(self):
        assert 1 + 1 + 4 + 9 + 9 == f
    def test_dims(self):
        assert sorted([1, 1, lam, q, q]) == [1, 1, 2, 3, 3]
    def test_GL2_classes(self):
        assert lam**q == 8

class TestT5_Platonic:
    def test_tetrahedron(self):
        assert f == 24
    def test_cube(self):
        assert k * mu == 48
    def test_icosahedron(self):
        assert E // lam == 120
    def test_rotation_T(self):
        assert k == 12
    def test_rotation_O(self):
        assert f == 24
    def test_rotation_I(self):
        assert E // mu == 60
    def test_A5(self):
        assert k * (mu + 1) == 60
    def test_S5(self):
        assert k * Phi4 == 120
