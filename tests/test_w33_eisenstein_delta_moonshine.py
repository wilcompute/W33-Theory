"""Pin the Eisenstein/Delta/j/moonshine layer.

Tests cover:
    (1) divisor-sum pins for sigma_3 and sigma_5;
    (2) first coefficients of E_4 and E_6;
    (3) Delta = eta^24 = (E_4^3 - E_6^2) / 1728;
    (4) Ramanujan tau values, Hecke multiplicativity, and mod-691 congruence;
    (5) j-function reference coefficients;
    (6) McKay decompositions at q, q^2, q^3;
    (7) deep constants and the driver summary chain.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_eisenstein_delta_moonshine import (  # noqa: E402
    J_FUNCTION_REFERENCE,
    MCKAY_DECOMPOSITIONS,
    MONSTER_IRREDUCIBLE_DIMS,
    RAMANUJAN_TAU,
    delta_from_eisenstein,
    derive_all,
    eisenstein_E4,
    eisenstein_E6,
    eta_24_coefficients,
    j_function_coefficients,
    sigma_k,
    tau,
    verify_deep_constants,
    verify_delta_identity,
    verify_j_function_coefficients,
    verify_mckay_observation,
    verify_ramanujan_691_congruence,
    verify_ramanujan_tau_table,
    verify_tau_multiplicativity,
)


def test_sigma_3_of_2_is_9():
    assert sigma_k(3, 2) == 1 + 8


def test_sigma_5_of_2_is_33():
    assert sigma_k(5, 2) == 1 + 32


def test_E4_first_four_coefficients():
    assert eisenstein_E4(5) == [1, 240, 2160, 6720, 17520]


def test_E6_first_four_coefficients():
    assert eisenstein_E6(5) == [1, -504, -16632, -122976, -532728]


def test_delta_from_eisenstein_matches_eta_24():
    delta = delta_from_eisenstein(16)
    eta24 = eta_24_coefficients(16)
    assert delta == eta24


def test_delta_q_and_q2_coefficients():
    delta = delta_from_eisenstein(4)
    assert delta[1] == 1
    assert delta[2] == -24
    assert delta[3] == 252


def test_tau_table_matches_reference():
    result = verify_ramanujan_tau_table()
    assert result["all_match"] is True
    assert result["failures"] == []


def test_tau_13_matches_reference_value():
    assert tau(13) == RAMANUJAN_TAU[13] == -577738


def test_delta_identity_verifier_is_green():
    result = verify_delta_identity(N=16)
    assert result["all_match"] is True


def test_tau_is_hecke_multiplicative_up_to_40():
    result = verify_tau_multiplicativity(max_mn=40)
    assert result["all_hold"] is True
    assert result["failures"] == []


def test_ramanujan_691_congruence_holds_up_to_40():
    result = verify_ramanujan_691_congruence(max_n=40)
    assert result["all_hold"] is True
    assert result["failures"] == []


def test_j_function_reference_coefficients_match():
    result = verify_j_function_coefficients()
    assert result["all_match"] is True
    assert result["failures"] == []
    assert result["coefficients"] == J_FUNCTION_REFERENCE


def test_mckay_decomposition_rows_match_j_coefficients():
    result = verify_mckay_observation()
    assert result["all_match"] is True
    for row in result["rows"]:
        predicted = sum(
            multiplicity * dim
            for multiplicity, dim in zip(row["multiplicities"], MONSTER_IRREDUCIBLE_DIMS)
        )
        assert predicted == row["j_coefficient"]
        assert row["multiplicities"] == MCKAY_DECOMPOSITIONS[row["n"]]


def test_196884_is_one_plus_196883():
    assert j_function_coefficients(2)[1] == 1 + 196883


def test_deep_constants_are_all_true():
    constants = verify_deep_constants()
    assert all(constants.values()) is True


def test_driver_summary_chain_is_all_true():
    summary = derive_all()
    for key, value in summary["summary_chain"].items():
        assert value is True, f"{key} = {value}"


# ----------------------------------------------------------------------
# Additional structural pins.
# ----------------------------------------------------------------------
def test_tau_6_equals_tau_2_times_tau_3_hecke_product():
    assert tau(6) == tau(2) * tau(3) == -6048


def test_tau_15_equals_tau_3_times_tau_5_hecke_product():
    assert tau(15) == tau(3) * tau(5) == 1217160


def test_ramanujan_691_for_small_primes_matches_1_plus_p_to_11():
    """tau(p) ≡ 1 + p^11 (mod 691) for primes p — specialisation of
    the sigma_11(n) congruence when n = p is prime."""
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        assert (tau(p) - (1 + p ** 11)) % 691 == 0


def test_j_constant_term_equals_3_dim_E8():
    """744 = 3 * 248 = 3 * dim(E_8)."""
    assert J_FUNCTION_REFERENCE[0] == 744
    assert 744 == 3 * 248


def test_1728_equals_12_cubed():
    """Delta normaliser 1728 = 12^3."""
    assert 1728 == 12 ** 3


def test_240_is_eisenstein_e4_leading_is_roots_E8():
    """E_4 = 1 + 240 q + ... and 240 = |roots(E_8)|."""
    assert eisenstein_E4(2)[1] == 240


def test_504_is_minus_E6_leading():
    assert eisenstein_E6(2)[1] == -504


def test_eta_exponent_24_matches_leech_and_bosonic():
    """eta^{24} = Delta; the 24 is the bosonic critical dim / Leech rank."""
    from w33_eisenstein_delta_moonshine import _pow_series, euler_phi_series
    phi = euler_phi_series(3)
    phi24 = _pow_series(phi, 24, 3)
    assert phi24[:2] == [1, -24]


def test_monster_smallest_faithful_irrep_is_196883():
    assert MONSTER_IRREDUCIBLE_DIMS[1] == 196883


def test_extended_mckay_row_at_q3_sum():
    """864299970 = 2 + 2.196883 + 21296876 + 842609326."""
    assert 864299970 == 2 + 2 * 196883 + 21296876 + 842609326
