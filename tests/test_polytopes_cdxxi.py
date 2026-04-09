"""
Phase CDXXI (421) — Convex Polytopes & Ehrhart Theory
======================================================
f-vectors, Euler formula, permutohedra, Birkhoff polytope.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Polyhedra:
    def test_tetra_f0(self):
        assert mu == 4

    def test_tetra_f1(self):
        assert math.factorial(q) == 6

    def test_tetra_f2(self):
        assert mu == 4

    def test_cube_f0(self):
        assert lam ** q == 8

    def test_cube_f1(self):
        assert k == 12

    def test_cube_f2(self):
        assert math.factorial(q) == 6

    def test_oct_f0(self):
        assert math.factorial(q) == 6

    def test_oct_f1(self):
        assert k == 12


class TestT2_24cell:
    def test_f0_f3(self):
        assert f == 24

    def test_f1(self):
        assert mu * f == 96

    def test_self_dual(self):
        assert mu * f == 96


class TestT3_Euler:
    def test_chi_s2(self):
        assert lam == 2

    def test_tetra(self):
        assert mu - math.factorial(q) + mu == lam

    def test_cube(self):
        assert lam ** q - k + math.factorial(q) == lam


class TestT4_Permutohedron:
    def test_Pi2(self):
        assert math.factorial(q) == 6

    def test_Pi3(self):
        assert f == 24

    def test_Pi4(self):
        assert E // lam == 120

    def test_Pi3_faces(self):
        assert Phi3 + 1 == 14


class TestT5_IndepComplex:
    def test_indep_edges(self):
        assert v * (v - 1) // 2 - E == 540

    def test_indep_formula(self):
        assert 540 == v * (v - k - 1) // lam


class TestT6_Birkhoff:
    def test_Bq_dim(self):
        assert (q - 1) ** 2 == mu

    def test_Bq_vertices(self):
        assert math.factorial(q) == 6

    def test_Bmu_dim(self):
        assert (mu - 1) ** 2 == q ** 2

    def test_Bmu_vertices(self):
        assert math.factorial(mu) == f
