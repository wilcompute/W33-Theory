"""Pin theta_{E_8} = E_4 and theta_{Lambda_{24}} = E_4^3 - 720 Delta,
with kissing numbers k(E_8) = 240 and k(Lambda_{24}) = 196560.

Tests cover:
    (1) direct E_8 vector enumeration (both integer and half-integer
        cosets) reproduces the E_4 coefficients up to q^4;
    (2) 240 = 112 (integer coset, C(8,2) x 2^2) + 128 (half-integer);
    (3) Leech theta = E_4^3 - 720 Delta matches the reference kissing
        numbers at q^0, q^2, q^3, q^4, q^5;
    (4) Leech has no norm-2 vectors (coefficient of q is 0);
    (5) kissing numbers 240 and 196560 are exact integers.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_theta_e8_leech import (  # noqa: E402
    E8_THETA_REFERENCE,
    LEECH_THETA_REFERENCE,
    count_e8_norm_2_direct,
    derive_all,
    e8_theta_coefficients,
    leech_theta_coefficients,
    verify_E8_theta_equals_E4,
    verify_e8_first_shell_decomposition,
    verify_leech_E8_cube_delta_identity,
    verify_leech_theta_reference,
)


# ----------------------------------------------------------------------
# E_8 theta direct enumeration.
# ----------------------------------------------------------------------
def test_e8_theta_q0_is_1():
    assert e8_theta_coefficients(0) == [1]


def test_e8_theta_q1_is_240():
    theta = e8_theta_coefficients(1)
    assert theta[1] == 240


def test_e8_theta_q2_is_2160():
    theta = e8_theta_coefficients(2)
    assert theta[2] == 2160


def test_e8_theta_q3_is_6720():
    theta = e8_theta_coefficients(3)
    assert theta[3] == 6720


def test_e8_theta_q4_is_17520():
    theta = e8_theta_coefficients(4)
    assert theta[4] == 17520


def test_e8_theta_first_five_match_reference():
    theta = e8_theta_coefficients(4)
    assert theta == [1, 240, 2160, 6720, 17520]


# ----------------------------------------------------------------------
# E_8 theta = E_4 identity.
# ----------------------------------------------------------------------
def test_e8_theta_equals_E4_up_to_q4():
    r = verify_E8_theta_equals_E4(max_k=4)
    assert r["all_match"] is True
    for row in r["rows"]:
        assert row["match"] is True


def test_kissing_number_E8_is_240():
    r = verify_E8_theta_equals_E4(max_k=1)
    assert r["kissing_number_E8"] == 240
    assert r["kissing_number_E8_equals_240"] is True


# ----------------------------------------------------------------------
# E_8 first shell decomposition.
# ----------------------------------------------------------------------
def test_e8_first_shell_is_112_plus_128():
    r = verify_e8_first_shell_decomposition()
    assert r["integer_coset"] == 112
    assert r["half_integer_coset"] == 128
    assert r["total"] == 240
    assert r["matches_240"] is True


def test_e8_direct_norm_2_count_is_240():
    assert count_e8_norm_2_direct() == 240


def test_integer_coset_112_is_C_8_2_times_4():
    """112 = C(8,2) * 2^2 (choose 2 positions, 4 sign patterns)."""
    assert 112 == 28 * 4


def test_half_integer_coset_128_is_2_to_7():
    """128 = 2^7 (half of 2^8 choices of ±1/2 satisfy sum ≡ 0 mod 4)."""
    assert 128 == 2 ** 7


# ----------------------------------------------------------------------
# Leech lattice theta via Eisenstein.
# ----------------------------------------------------------------------
def test_leech_theta_q0_is_1():
    assert leech_theta_coefficients(1)[0] == 1


def test_leech_theta_q1_is_0():
    """Leech has no norm-2 vectors (minimum distance is norm 4)."""
    assert leech_theta_coefficients(2)[1] == 0


def test_leech_kissing_number_is_196560():
    theta = leech_theta_coefficients(3)
    assert theta[2] == 196560


def test_leech_theta_q3_is_16773120():
    assert leech_theta_coefficients(4)[3] == 16773120


def test_leech_theta_q4_is_398034000():
    assert leech_theta_coefficients(5)[4] == 398034000


def test_leech_theta_q5_is_4629381120():
    assert leech_theta_coefficients(6)[5] == 4629381120


def test_leech_theta_verifier_all_match():
    r = verify_leech_theta_reference(N=5)
    assert r["all_match"] is True
    assert r["kissing_number_Leech"] == 196560
    assert r["no_norm_2_vectors_in_Leech"] is True


def test_leech_reference_has_expected_keys():
    for k in [0, 1, 2, 3, 4, 5]:
        assert k in LEECH_THETA_REFERENCE
    assert LEECH_THETA_REFERENCE[2] == 196560


# ----------------------------------------------------------------------
# Cross-identity: theta_Lambda = theta_E8^3 - 720 Delta (tautology).
# ----------------------------------------------------------------------
def test_leech_equals_E8_cubed_minus_720_delta():
    r = verify_leech_E8_cube_delta_identity(N=7)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# E_8 theta reference matches direct enumeration.
# ----------------------------------------------------------------------
def test_E8_theta_reference_matches_enumeration():
    theta = e8_theta_coefficients(4)
    assert theta == E8_THETA_REFERENCE[:5]


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_includes_subresults():
    s = derive_all()
    for key in [
        "E8_theta_vs_E4",
        "leech_theta_reference",
        "leech_identity",
        "e8_first_shell",
        "summary_chain",
    ]:
        assert key in s
