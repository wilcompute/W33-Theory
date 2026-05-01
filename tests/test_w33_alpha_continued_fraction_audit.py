"""Tests for the W(3,3) α⁻¹ continued-fraction audit."""

from __future__ import annotations

from fractions import Fraction

from scripts.w33_alpha_continued_fraction_audit import (
    ALPHA_INV_W33,
    CODATA_ALPHA_INV,
    continued_fraction,
    continued_fraction_decimal,
    matching_prefix_length,
    reconstruct_from_cf,
    w33_alpha_continued_fraction_audit,
)


def test_alpha_inv_w33_fraction_is_expected_form() -> None:
    assert ALPHA_INV_W33 == Fraction(669969, 4889)
    assert ALPHA_INV_W33 == Fraction(137) + Fraction(880, 24445)


def test_continued_fraction_of_w33_alpha_inv() -> None:
    cf = continued_fraction(ALPHA_INV_W33)
    assert cf == (137, 27, 1, 3, 1, 1, 19)


def test_continued_fraction_of_codata_leading_matches_first_six() -> None:
    cf_codata = continued_fraction_decimal(float(CODATA_ALPHA_INV), max_terms=8)
    assert cf_codata[:6] == (137, 27, 1, 3, 1, 1)


def test_match_length_is_six() -> None:
    packet = w33_alpha_continued_fraction_audit()
    assert packet["match_length"] == 6
    assert packet["matching_prefix"] == (137, 27, 1, 3, 1, 1)


def test_structural_convergent_reconstructs_cleanly() -> None:
    packet = w33_alpha_continued_fraction_audit()
    convergent = Fraction(*map(int, packet["structural_convergent_fraction"].split("/")))
    # Recovered from [137, 27, 1, 3, 1, 1] — this is a well-defined convergent.
    reconstructed = reconstruct_from_cf((137, 27, 1, 3, 1, 1))
    assert convergent == reconstructed
    # Convergent accuracy should be within a few ppm of CODATA.
    deviation = abs(float(convergent) - float(CODATA_ALPHA_INV))
    assert deviation < 1e-5


def test_matching_prefix_length_helper_is_monotone() -> None:
    a = (137, 27, 1, 3, 1, 1, 19)
    b = (137, 27, 1, 3, 1, 1, 18, 1)
    assert matching_prefix_length(a, b) == 6
    assert matching_prefix_length(a, a) == len(a)
    assert matching_prefix_length((1, 2), (2, 1)) == 0


def test_first_two_partial_quotients_are_w33_invariants() -> None:
    """The first two partial quotients of the CF come out as
    137 = (k-1)^2 + mu^2 and 27 = v-k-1 = q^3, both W(3,3) structural."""
    k = 12
    mu = 4
    v = 40
    q = 3
    assert (k - 1) ** 2 + mu ** 2 == 137
    assert v - k - 1 == 27
    assert q ** 3 == 27
    cf = continued_fraction(ALPHA_INV_W33)
    assert cf[0] == (k - 1) ** 2 + mu ** 2
    assert cf[1] == v - k - 1 == q ** 3


def test_audit_packet_shape() -> None:
    packet = w33_alpha_continued_fraction_audit()
    for key in (
        "alpha_inv_w33_fraction",
        "alpha_inv_w33_decimal",
        "alpha_inv_codata_decimal",
        "cf_w33",
        "cf_codata_leading",
        "match_length",
        "matching_prefix",
        "annotated_prefix",
        "structural_convergent_fraction",
        "tier_note",
    ):
        assert key in packet, f"missing key: {key}"
    # The annotated prefix should explicitly name the Gaussian norm and q^3.
    annotations = " ".join(a["structural_meaning"] for a in packet["annotated_prefix"])
    assert "Gaussian norm" in annotations
    assert "q^3" in annotations
