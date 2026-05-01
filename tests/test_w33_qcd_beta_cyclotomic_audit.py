"""Tests for the QCD β-coefficient cyclotomic audit at W(3,3) parameters."""

from __future__ import annotations

from fractions import Fraction

from scripts.w33_qcd_beta_cyclotomic_audit import (
    msbar_beta_coefficients,
    w33_qcd_beta_cyclotomic_audit,
    assert_all_identities_hold,
)


def test_audit_packet_structure() -> None:
    packet = w33_qcd_beta_cyclotomic_audit()
    assert packet["scheme"] == "MS-bar"
    assert packet["gauge"] == "SU(3)_c"
    assert "Nf=6" in packet["matter"]
    constants = packet["w33_constants"]
    assert constants["q"] == 3
    assert constants["Phi3"] == 13
    assert constants["Phi6"] == 7


def test_beta0_equals_phi6_at_q3() -> None:
    standard_model = msbar_beta_coefficients(Nc=3, Nf=6)
    assert standard_model["beta0"] == Fraction(7)
    assert standard_model["beta0"] == Fraction(3 * 3 - 3 + 1)  # Phi6(3)


def test_beta1_equals_two_phi3_at_q3() -> None:
    standard_model = msbar_beta_coefficients(Nc=3, Nf=6)
    assert standard_model["beta1"] == Fraction(26)
    assert standard_model["beta1"] == 2 * Fraction(3 * 3 + 3 + 1)  # 2*Phi3(3)


def test_beta2_equals_minus_five_halves_phi3_at_q3() -> None:
    standard_model = msbar_beta_coefficients(Nc=3, Nf=6)
    assert standard_model["beta2"] == -Fraction(65, 2)
    assert standard_model["beta2"] == -Fraction(5, 2) * Fraction(3 * 3 + 3 + 1)


def test_identity_flags_are_true() -> None:
    packet = w33_qcd_beta_cyclotomic_audit()
    assert packet["identity"]["beta0"]["equal_Phi6"] is True
    assert packet["identity"]["beta1"]["equal_2Phi3"] is True
    assert packet["identity"]["beta2"]["equal_minus_5_over_2_Phi3"] is True


def test_cross_ratios_are_clean_rationals() -> None:
    packet = w33_qcd_beta_cyclotomic_audit()
    assert packet["cross_ratios"]["beta1_over_beta0"] == "26/7"
    assert packet["cross_ratios"]["beta1_over_beta2"] == "-4/5"
    assert packet["cross_ratios"]["beta0_beta1_product"] == "182"


def test_assertion_helper_passes() -> None:
    # Should not raise.
    assert_all_identities_hold()


def test_identity_breaks_for_pure_yang_mills() -> None:
    """Sanity: at Nf=0 the cyclotomic identity must NOT hold; the
    coincidence is specific to the SM matter content."""
    pure_ym = msbar_beta_coefficients(Nc=3, Nf=0)
    assert pure_ym["beta0"] == Fraction(11)  # not Phi6(3)=7
    assert pure_ym["beta1"] == Fraction(102)  # not 2*Phi3(3)=26


def test_eisenstein_norms_match_cyclotomics() -> None:
    """β₀ = |q+ω|², β₁/2 = |q−ω|² in the Eisenstein integer ring Z[ω]."""
    q = 3
    # In Z[ω] with ω² + ω + 1 = 0:
    #   N(a + b ω) = a² − a b + b²
    norm_q_plus_omega = q * q - q * 1 + 1 * 1  # = q² − q + 1 = Φ₆
    norm_q_minus_omega = q * q + q * 1 + 1 * 1  # = q² + q + 1 = Φ₃ ?
    #  Actually: N(a + bω) with b = -1: a² - a(-1) + 1 = a² + a + 1 = Φ₃ ✓
    assert norm_q_plus_omega == 7
    assert norm_q_minus_omega == 13
    sm = msbar_beta_coefficients(Nc=3, Nf=6)
    assert sm["beta0"] == Fraction(norm_q_plus_omega)
    assert sm["beta1"] == 2 * Fraction(norm_q_minus_omega)
