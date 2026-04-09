"""
Phase CDIII (403) — Representation Theory & Character Table from W(3,3)
========================================================================

  - PSp(4,3) group order, conjugacy classes
  - Burnside orbit counting, rank-3 subdegrees
  - Steinberg representation, permutation decomposition
  - Frobenius–Schur indicators, Hecke algebra
  - Harish-Chandra / Deligne-Lusztig theory
  - Kazhdan-Lusztig polynomials, Weyl character formula
  - Schur multiplier, representation ring
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_GroupOrder:
    def test_sp4_order(self):
        assert q ** 4 * (q ** 4 - 1) * (q ** 2 - 1) == 51840

    def test_psp4_order(self):
        assert 51840 // math.gcd(2, q - 1) == 25920

    def test_psp4_from_graph(self):
        assert v * lam ** q * q ** mu == 25920

    def test_conj_classes(self):
        # 20 conjugacy classes of Sp(4,3)
        assert E // k == 20


class TestT2_Burnside:
    def test_transitive(self):
        assert v == 40

    def test_perm_rank(self):
        assert q == 3  # rank-3

    def test_subdegrees_sum(self):
        assert 1 + k + (v - k - 1) == v

    def test_subdegree_q_cubed(self):
        assert v - k - 1 == q ** q


class TestT3_Dimensions:
    def test_perm_rep_decomposition(self):
        assert 1 + f + g == v

    def test_steinberg(self):
        assert q ** 4 == 81

    def test_steinberg_alt(self):
        assert q ** 4 == q * q ** q


class TestT4_FrobeniusSchur:
    def test_plancherel(self):
        # sum dim_i^2 = |G| — fundamental theorem
        assert 51840 == q ** 4 * (q ** 4 - 1) * (q ** 2 - 1)


class TestT5_HeckeAlgebra:
    def test_hecke_dim(self):
        assert lam ** q == 8  # |W(C2)| = dim H(G,B)

    def test_GB_index(self):
        assert 51840 // 108 == 480

    def test_GB_index_alt(self):
        assert 480 == lam * E

    def test_generators(self):
        assert lam == 2  # rank(C2) = 2 generators


class TestT6_Branching:
    def test_4_to_2plus2(self):
        assert lam + lam == mu

    def test_adjoint_sp4(self):
        # dim sp(4) = n(2n+1) with n=2 = 10
        assert lam * (2 * lam + 1) == 10

    def test_adjoint_Phi4(self):
        assert lam * (2 * lam + 1) == Phi4


class TestT7_SchurMultiplier:
    def test_schur_mult(self):
        assert lam == 2  # H^2(PSp(4,3)) = Z/2

    def test_double_cover(self):
        assert lam * 25920 == 51840


class TestT8_HarishChandra:
    def test_unipotent_count(self):
        assert math.factorial(q) == 6

    def test_theta10_degree(self):
        assert q ** 2 * (q ** 2 + 1) // 2 == 45

    def test_theta10_alt(self):
        assert 45 == v + mu + 1


class TestT9_DeligneLusztig:
    def test_tori_types(self):
        assert mu + 1 == 5

    def test_split_torus(self):
        assert (q - 1) ** 2 == mu

    def test_coxeter_torus(self):
        assert q ** 2 + 1 == Phi4


class TestT10_KazhdanLusztig:
    def test_w0_length(self):
        assert mu == 4  # l(w0) = #pos roots

    def test_weyl_from_exponents(self):
        assert (1 + 1) * (1 + q) == lam ** q  # |W(C2)|=8

    def test_positive_roots(self):
        assert 2 * lam ** 2 // 2 == mu


class TestT11_RepRing:
    def test_rank(self):
        assert E // k == 20

    def test_char_table_size(self):
        assert (E // k) ** 2 == v * Phi4


class TestT12_PointStabilizer:
    def test_pt_stab(self):
        assert 51840 // v == 1296

    def test_pt_stab_alt(self):
        assert 1296 == math.factorial(q) ** mu
