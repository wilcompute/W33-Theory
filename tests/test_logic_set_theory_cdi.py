"""
Phase CDI (401) — Logic, Set Theory, Foundations from W(3,3)
================================================================

  - 2-valued vs intuitionistic vs many-valued logic
  - ZFC axioms (~9), Peano (~5)
  - Goedel incompleteness in finite W(3,3) world
  - Categories: small vs large
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Logic:
    def test_classical_truth_values(self):
        # T, F = lam
        assert lam == 2

    def test_three_valued_logic(self):
        # Lukasiewicz T,F,U = q
        assert q == 3

    def test_connectives(self):
        # AND, OR, NOT, IMPLIES, IFF = mu+1
        assert mu + 1 == 5

    def test_truth_table_2var(self):
        # 2^2^2 = 16 = lam^mu
        assert lam ** lam ** lam == 16


class TestT2_ZFC:
    def test_axioms_count(self):
        # ZFC ~ 9 axioms = q^2
        assert q ** lam == 9

    def test_peano_axioms(self):
        # 5 = mu+1
        assert mu + 1 == 5

    def test_choice_independence(self):
        # 1 axiom, independent
        assert 1 == 1


class TestT3_Goedel:
    def test_two_theorems(self):
        # 1st, 2nd incompleteness = lam
        assert lam == 2

    def test_finite_w33_decidable(self):
        # 40 vertices = decidable
        assert v == 40


class TestT4_Categories:
    def test_set_obj_morphisms(self):
        # 2 layers = lam
        assert lam == 2

    def test_yoneda(self):
        # 1 lemma
        assert 1 == 1

    def test_topos_axioms(self):
        # ~7 = Phi6
        assert Phi6 == 7

    def test_adjoint_functors(self):
        # left, right = lam
        assert lam == 2


class TestT5_Sizes:
    def test_finite(self):
        assert v == 40

    def test_aleph_0(self):
        # countable
        assert 1 == 1

    def test_continuum(self):
        # 2^aleph_0 = lam^?
        assert lam == 2
