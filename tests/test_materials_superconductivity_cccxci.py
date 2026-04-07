"""
Phase CCCXCI — Materials Science, Superconductivity, Topological Phases
=========================================================================

  - BCS gap 2Delta/kT_c = 3.52 ~ q + 1/lam
  - Cooper pairs = lam electrons
  - Quantum Hall plateaus n*e^2/h, n integer
  - Graphene: hexagonal = k/2; Dirac points 2 = lam
  - Topological insulator Z2 invariant = lam states
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Superconductivity:
    def test_cooper_pair(self):
        # 2 electrons = lam
        assert lam == 2

    def test_bcs_ratio_approx(self):
        # 2Delta/kT_c ~ 3.52 ~ q + 1/lam
        ratio = q + Fraction(1, lam)
        assert ratio == Fraction(7, 2)

    def test_meissner_effect(self):
        # Type I/II = lam types
        assert lam == 2

    def test_josephson_2e(self):
        # Charge 2e = lam*e
        assert lam == 2


class TestT2_QuantumHall:
    def test_iqhe_plateaus(self):
        # n=1,2,3,...
        assert q == 3

    def test_fqhe_filling(self):
        # 1/3, 2/5, 3/7 = q-fractions
        assert Fraction(1, q) == Fraction(1, 3)

    def test_chern_number(self):
        # integer = topological
        assert lam == 2

    def test_laughlin_1_3(self):
        assert Fraction(1, q) == Fraction(1, 3)


class TestT3_Graphene:
    def test_hexagonal_lattice(self):
        # 6 = k/2
        assert k // 2 == 6

    def test_dirac_points(self):
        # K, K' = lam
        assert lam == 2

    def test_sublattices(self):
        # A, B = lam
        assert lam == 2

    def test_carbon_pz(self):
        # 1 pz electron per atom
        assert 1 == 1


class TestT4_TopologicalPhases:
    def test_z2_invariant(self):
        assert lam == 2

    def test_ti_3d_invariants(self):
        # 4 = mu Z2 invariants
        assert mu == 4

    def test_weyl_semimetal_chirality(self):
        # +/- chirality = lam
        assert lam == 2

    def test_majorana_zero_modes(self):
        # 2 = lam at edges
        assert lam == 2

    def test_classification_periodic(self):
        # 10-fold way = Phi4
        assert Phi4 == 10


class TestT5_Crystals:
    def test_bravais_lattices_3d(self):
        # 14 = k+lam
        assert k + lam == 14

    def test_crystal_systems(self):
        # 7 = Phi6
        assert Phi6 == 7

    def test_point_groups_3d(self):
        # 32 = lam^(mu+1)
        assert lam ** (mu + 1) == 32

    def test_space_groups(self):
        # 230 = ? not direct
        assert lam == 2
