from fractions import Fraction
from scripts.verify_substrate_predictions import compute_substrate_predictions


def test_substrate_primitives_and_formulas():
    vals = compute_substrate_predictions()

    assert vals["q"] == 3
    assert vals["mu"] == 4
    assert vals["q_fact"] == 6
    assert vals["k"] == 12
    assert vals["Phi_3"] == 13
    assert vals["Phi_6"] == 7
    assert vals["v"] == 40
    assert vals["E_edges"] == 240

    # exact rational checks
    assert vals["alpha_inv"] == Fraction(3837, 28)  # 137 + 1/28
    assert vals["sin2_theta_w"] == Fraction(3, 13)
    assert vals["neutrino_wimp_exponent"] == 34

    assert vals["Omega_b"] == Fraction(25, 511)
    assert vals["Omega_DM"] == Fraction(135, 511)
    assert vals["Omega_L"] == Fraction(351, 511)

    assert vals["key_rate"] == Fraction(13, 40)
    assert vals["F3_visibility"] == Fraction(1, 3)
