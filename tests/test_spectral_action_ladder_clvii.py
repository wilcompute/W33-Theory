from fractions import Fraction

from PART_CLVII_SPECTRAL_ACTION_LADDER_COMPILER import (
    A0,
    A2,
    A4,
    ETA0,
    INDEX,
    PHI6,
    RADIAL_WEDGE,
    spectral_action_ladder_audit,
)


def test_seeley_dewitt_coefficients_match_cliv():
    assert A0 == 480
    assert A2 == 2240
    assert A4 == 17600


def test_a2_over_a0_is_index_asymmetry_step():
    assert Fraction(A2, A0) == Fraction(ETA0, INDEX) == Fraction(14, 3)


def test_a4_over_a2_is_radial_threshold_step():
    assert RADIAL_WEDGE == 55
    assert Fraction(A4, A2) == Fraction(RADIAL_WEDGE, PHI6) == Fraction(55, 7)


def test_higgs_quartic_is_inverse_radial_threshold():
    lam_h = Fraction(PHI6, RADIAL_WEDGE)
    assert lam_h == Fraction(7, 55)
    assert 1 / lam_h == Fraction(A4, A2)


def test_audit_checks_all_true():
    audit = spectral_action_ladder_audit()
    assert all(audit["checks"].values())
    assert audit["radial_threshold_data"]["lambda_H"] == "7/55"
