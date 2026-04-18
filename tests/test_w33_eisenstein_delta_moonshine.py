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
