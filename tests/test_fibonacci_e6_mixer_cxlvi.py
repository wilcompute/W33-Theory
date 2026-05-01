from fractions import Fraction

from PART_CXLVI_FIBONACCI_E6_MIXER import (
    CARRIER_NUM,
    MIXER_DEN,
    PHI3,
    Q,
    THRESHOLD_NUM,
    carrier_weight,
    fibonacci_e6_mixer_audit,
    imbalance_weight,
    q_generation_lift,
    reduce_ratio,
    threshold_weight,
)


def test_24_15_reduces_to_8_5():
    assert reduce_ratio(24, 15) == (8, 5)
    assert reduce_ratio(48, 30) == (8, 5)


def test_mixer_denominator_is_phi3():
    assert CARRIER_NUM + THRESHOLD_NUM == MIXER_DEN == PHI3 == 13


def test_carrier_and_threshold_weights_sum_to_one():
    assert carrier_weight() == Fraction(8, 13)
    assert threshold_weight() == Fraction(5, 13)
    assert carrier_weight() + threshold_weight() == 1


def test_imbalance_is_q_over_phi3():
    assert imbalance_weight() == Fraction(Q, PHI3) == Fraction(3, 13)


def test_q_generation_lifts_recover_qcd_factors():
    assert q_generation_lift(carrier_weight()) == Fraction(24, 13)
    assert q_generation_lift(threshold_weight()) == Fraction(15, 13)


def test_audit_checks_all_true():
    audit = fibonacci_e6_mixer_audit()
    assert all(audit["checks"].values())
    assert audit["reduced_mixer"]["carrier_weight"] == "8/13"
    assert audit["reduced_mixer"]["threshold_weight"] == "5/13"
    assert audit["reduced_mixer"]["imbalance_weight"] == "3/13"


def test_electroweak_diagnostic_records_q_over_phi3():
    audit = fibonacci_e6_mixer_audit()
    assert "3/13" in audit["electroweak_diagnostic"]["mixer_imbalance"]
    assert "q/Phi3" in audit["electroweak_diagnostic"]["interpretation"]
