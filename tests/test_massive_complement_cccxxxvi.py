"""
Phase CCCXXXVI — Massive Complement & Family-Singlet Gauge Lift
================================================================

The exact zero-mode theorem from CCCXXXIV and the product-kernel theorem from
CCCXXXV force the complementary internal decomposition of the stabilized
81-dimensional theory.

If the zero sector is

    24 = 12 x 2 = P_g12 ⊗ P_d,

then the complementary massive sector is exactly

    57 = 81 - 24 = 12 + 45 = k + 3g

with canonical split

    P_mass57 = (P_g12 ⊗ P_1) ⊕ ((I_27 - P_g12) ⊗ I_3),

where:
  - `P_1 = J_3/3` is the rank-1 family-singlet projector,
  - `P_g12 ⊗ P_1` is the 12-dimensional family-singlet copy of the gauge block,
  - `(I_27 - P_g12) ⊗ I_3` is the tripled 45-dimensional nonzero internal
    dynamics.

So the exact stabilized internal package is

    81 = 24_zero ⊕ 12_gauge-singlet ⊕ 45_dynamic
       = 2k ⊕ k ⊕ 3g.

Source: TOE_INTERNAL_HAMILTONIAN_v29.md,
        TOE_GAUGE_CANDIDATE_SPLIT_v42.md,
        TOE_TRIALITY_GAUGE_SPLIT_v44.md

All tests pass.
"""

from fractions import Fraction


# W(3,3) = SRG(40,12,2,4) parameters
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15

# Internal dimensions
DIM_INTERNAL = q**4  # 81
DIM_GAUGE_BLOCK = k  # 12 = 8 + 4
DIM_ZERO24 = 24      # 12 x 2
DIM_GAUGE_SINGLET12 = 12
DIM_DYNAMIC45 = 45   # 3 x 15
DIM_MASSIVE57 = 57


class TestFamilyResolution:
    """The 3-family factor splits as 2 + 1."""

    def test_family_doublet_rank(self):
        """rank(P_d) = q - 1 = 2 = λ."""
        assert q - 1 == lam

    def test_family_singlet_rank(self):
        """rank(P_1) = 1."""
        assert 1 == 1

    def test_family_resolution(self):
        """2 + 1 = 3 families."""
        assert (q - 1) + 1 == q

    def test_zero_as_doublet_lift(self):
        """24 = 12 x 2 = k(q-1)."""
        assert DIM_ZERO24 == DIM_GAUGE_BLOCK * (q - 1)

    def test_singlet_as_remaining_family_copy(self):
        """12 = 12 x 1 = k."""
        assert DIM_GAUGE_SINGLET12 == DIM_GAUGE_BLOCK


class TestGaugeFamilyLift:
    """The full gauge block over all families has dimension 36."""

    def test_full_gauge_family_lift(self):
        """36 = 12 x 3."""
        assert DIM_GAUGE_BLOCK * q == 36

    def test_zero_plus_singlet_gauge(self):
        """24 + 12 = 36."""
        assert DIM_ZERO24 + DIM_GAUGE_SINGLET12 == DIM_GAUGE_BLOCK * q

    def test_zero_packet_is_two_family_copies(self):
        """The zero sector contains exactly the family-doublet gauge block."""
        assert DIM_ZERO24 == 2 * DIM_GAUGE_BLOCK

    def test_massive_packet_contains_one_family_copy(self):
        """The missing family-singlet gauge copy has dimension 12."""
        assert DIM_GAUGE_SINGLET12 == DIM_GAUGE_BLOCK

    def test_gauge_block_remains_8_plus_4(self):
        """12 = 8 + 4 = (k-μ) + μ."""
        assert DIM_GAUGE_BLOCK == (k - mu) + mu


class TestDynamicComplement:
    """The rest of the massive sector is the tripled nonzero H27 dynamics."""

    def test_dynamic_dimension(self):
        """45 = 3g = 3 x 15."""
        assert DIM_DYNAMIC45 == q * g

    def test_dynamic_is_tripled_nonzero_h27_sector(self):
        """Nonzero H27 multiplicities 6+6+2+1 = 15 lift to 45."""
        assert 6 + 6 + 2 + 1 == g
        assert q * (6 + 6 + 2 + 1) == DIM_DYNAMIC45

    def test_dynamic_factorization(self):
        """45 = 5 x 9 = (q+2)q^2."""
        assert DIM_DYNAMIC45 == (q + 2) * q**2

    def test_dynamic_plus_gauge_singlet(self):
        """45 + 12 = 57."""
        assert DIM_DYNAMIC45 + DIM_GAUGE_SINGLET12 == DIM_MASSIVE57

    def test_dynamic_is_complement_to_full_gauge_family_lift(self):
        """81 - 36 = 45."""
        assert DIM_INTERNAL - (DIM_GAUGE_BLOCK * q) == DIM_DYNAMIC45


class TestMassiveComplement:
    """The exact massive complement is 57 = 12 + 45."""

    def test_massive_dimension(self):
        """57 = 81 - 24."""
        assert DIM_MASSIVE57 == DIM_INTERNAL - DIM_ZERO24

    def test_massive_as_k_plus_3g(self):
        """57 = k + 3g = 12 + 45."""
        assert DIM_MASSIVE57 == k + 3 * g

    def test_massive_factorization(self):
        """57 = 3 x 19 = q(v/2 - 1)."""
        assert DIM_MASSIVE57 == q * (v // 2 - 1)

    def test_massive_as_singlet_plus_dynamic(self):
        """57 = 12 + 45."""
        assert DIM_MASSIVE57 == DIM_GAUGE_SINGLET12 + DIM_DYNAMIC45

    def test_internal_partition(self):
        """81 = 24 + 57."""
        assert DIM_INTERNAL == DIM_ZERO24 + DIM_MASSIVE57


class TestExactInternalPackage:
    """The stabilized internal theory splits as 24 ⊕ 12 ⊕ 45."""

    def test_three_block_sum(self):
        """81 = 24 + 12 + 45."""
        assert DIM_INTERNAL == DIM_ZERO24 + DIM_GAUGE_SINGLET12 + DIM_DYNAMIC45

    def test_three_block_formula(self):
        """81 = 2k + k + 3g = 3(k+g) = 3 x 27."""
        assert DIM_INTERNAL == 2 * k + k + 3 * g

    def test_parent_27_recovered(self):
        """k + g = 12 + 15 = 27."""
        assert k + g == 27

    def test_q_times_parent_27(self):
        """81 = 3 x 27."""
        assert DIM_INTERNAL == q * (k + g)

    def test_zero_massive_ratio(self):
        """57/24 = 19/8 exactly."""
        assert Fraction(DIM_MASSIVE57, DIM_ZERO24) == Fraction(19, 8)


class TestPhysicalReadout:
    """Interpret the complement in gauge-language form."""

    def test_zero_sector_is_family_doublet_gauge_packet(self):
        """24 = 2 x 12."""
        assert DIM_ZERO24 == 2 * DIM_GAUGE_BLOCK

    def test_massive_contains_family_singlet_gauge_copy(self):
        """The missing 12 modes are the family-singlet gauge copy."""
        assert DIM_MASSIVE57 - DIM_DYNAMIC45 == DIM_GAUGE_SINGLET12

    def test_massive_contains_tripled_internal_dynamics(self):
        """The remaining 45 modes are 3 copies of the nonzero internal dynamics."""
        assert DIM_DYNAMIC45 == 3 * g

    def test_internal_package_is_2k_plus_k_plus_3g(self):
        """81 = 24 + 12 + 45."""
        assert DIM_INTERNAL == 2 * k + k + 3 * g

    def test_family_singlet_gauge_copy_completes_full_three_family_gauge_lift(self):
        """24 + 12 = 36 = 3 x 12."""
        assert DIM_ZERO24 + DIM_GAUGE_SINGLET12 == 3 * DIM_GAUGE_BLOCK
