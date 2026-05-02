from fractions import Fraction

from PART_CLIX_ROOT_STABILIZER_SPECTRAL_ACTION import (
    A0,
    A2,
    A4,
    PHI6,
    Q,
    MU,
    RADIAL_WEDGE,
    WEYL_E6_ORDER,
    DIRECTED_EDGE_STABILIZER,
    NORMALIZER_DEN,
    TRIANGLE_STABILIZER,
    root_stabilizer_spectral_action_audit,
)


def test_global_normalized_coefficients():
    assert Fraction(A0, WEYL_E6_ORDER) == Fraction(1, 108)
    assert Fraction(A2, WEYL_E6_ORDER) == Fraction(7, 162)
    assert Fraction(A4, WEYL_E6_ORDER) == Fraction(55, 162)


def test_a0_is_inverse_directed_edge_stabilizer():
    assert DIRECTED_EDGE_STABILIZER == MU * Q**3 == 108
    assert Fraction(A0, WEYL_E6_ORDER) == Fraction(1, DIRECTED_EDGE_STABILIZER)


def test_a2_a4_are_threshold_and_radial_wedge_over_2q4():
    assert NORMALIZER_DEN == 2 * Q**4 == 162
    assert Fraction(A2, WEYL_E6_ORDER) == Fraction(PHI6, NORMALIZER_DEN)
    assert Fraction(A4, WEYL_E6_ORDER) == Fraction(RADIAL_WEDGE, NORMALIZER_DEN)


def test_ratios_survive_global_normalization():
    assert Fraction(A2, WEYL_E6_ORDER) / Fraction(A0, WEYL_E6_ORDER) == Fraction(A2, A0) == Fraction(14, 3)
    assert Fraction(A4, WEYL_E6_ORDER) / Fraction(A2, WEYL_E6_ORDER) == Fraction(A4, A2) == Fraction(55, 7)


def test_triangle_half_normalizer():
    assert NORMALIZER_DEN == TRIANGLE_STABILIZER // 2


def test_audit_checks_all_true():
    audit = root_stabilizer_spectral_action_audit()
    assert all(audit["checks"].values())
    assert audit["normalized_coefficients"][1]["normalized_value"] == "7/162"
