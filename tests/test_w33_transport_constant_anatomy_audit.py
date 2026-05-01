from __future__ import annotations

from fractions import Fraction

from scripts.w33_transport_constant_anatomy_audit import (
    build_transport_constant_anatomy_summary,
)


def test_transport_numerator_217_has_two_exact_factorizations() -> None:
    summary = build_transport_constant_anatomy_summary()

    assert summary["transport_numerator"]["T"] == 217
    assert summary["transport_numerator"]["q_factorial"] == 6
    assert summary["transport_numerator"]["T_from_factorial"] == 217
    assert summary["transport_numerator"]["h_E8"] == 30
    assert summary["transport_numerator"]["T_from_coxeter"] == 217
    assert summary["transport_numerator"]["factorization_1"] == "6^3 + 1 = 217"
    assert summary["transport_numerator"]["factorization_2"] == "7 * (30 + 1) = 217"


def test_transport_numerator_has_third_factorization_h_E6_times_h_E7_plus_1() -> None:
    summary = build_transport_constant_anatomy_summary()

    tn = summary["transport_numerator"]
    assert tn["h_E6"] == 12
    assert tn["h_E7"] == 18
    assert tn["T_from_E6_E7"] == 217
    assert tn["factorization_3"] == "h(E6) * h(E7) + 1 = 12 * 18 + 1 = 217"


def test_transport_scale_is_217_over_12() -> None:
    summary = build_transport_constant_anatomy_summary()

    assert summary["transport_scale"] == "217/12"


def test_cyclotomic_values_at_q3_are_exact() -> None:
    summary = build_transport_constant_anatomy_summary()

    cyc = summary["cyclotomic_values"]
    assert cyc["phi1"] == 2
    assert cyc["phi2"] == 4
    assert cyc["phi3"] == 13
    assert cyc["phi4"] == 10
    assert cyc["phi6"] == 7


def test_C_witness_14105_has_two_exact_factorizations() -> None:
    summary = build_transport_constant_anatomy_summary()

    assert summary["C_v2"] == 780
    assert summary["C_witness"] == 14105
    assert summary["C_witness_factorization_1"] == "C(40,2) * 217 / 12 = 780 * 217 / 12 = 14105"
    assert summary["C_witness_factorization_2"] == "Phi3 * (mu+1) * T = 13 * 5 * 217 = 14105"
    assert summary["phi3_mu_plus_1"] == 65


def test_4320_ordered_paths_equal_2_times_W_E6_over_W_A3() -> None:
    summary = build_transport_constant_anatomy_summary()

    paths = summary["paths_4320"]
    assert paths["value"] == 4320
    assert summary["W_E6"] == 51840
    assert summary["W_A3"] == 24
    assert paths["factorization"] == "2 * |W(E6)| / |W(A3)| = 2 * 51840 / 24 = 4320"


def test_540_non_adjacent_pairs_equal_complement_degree() -> None:
    summary = build_transport_constant_anatomy_summary()

    nap = summary["non_adjacent_pairs_540"]
    assert nap["value"] == 540
    assert nap["from_binomial_minus_edges"] == 540
    assert nap["from_complement_degree"] == 540
    assert nap["factorization"] == "C(40,2) - 240 = 780 - 240 = 540"


def test_all_exact_factorizations_hold() -> None:
    summary = build_transport_constant_anatomy_summary()

    assert all(summary["exact_factorizations"].values())


def test_theorem_all_clauses_hold() -> None:
    summary = build_transport_constant_anatomy_summary()
    theorem = summary["theorem"]

    assert theorem["the_transport_numerator_217_equals_q_factorial_cubed_plus_1"] is True
    assert theorem["the_transport_numerator_217_equals_phi6_times_coxeter_E8_plus_1"] is True
    assert theorem["the_transport_numerator_217_equals_h_E6_times_h_E7_plus_1"] is True
    assert theorem["the_E8_coxeter_number_is_q_times_phi4"] is True
    assert theorem["the_transport_scale_is_217_over_12"] is True
    assert theorem["the_exact_witness_dC_14105_equals_C_v2_times_T_over_k"] is True
    assert theorem["the_exact_witness_dC_14105_equals_phi3_times_mu_plus_1_times_T"] is True
    assert theorem["the_phi3_mu_plus_1_factor_65_equals_C_v2_over_k"] is True
    assert theorem["the_4320_ordered_paths_equal_2_times_W_E6_over_W_A3"] is True
    assert theorem["the_540_non_adjacent_pairs_equal_C_v2_minus_edges"] is True
    assert theorem["the_transport_anatomy_is_fully_exact"] is True


def test_status_ok() -> None:
    summary = build_transport_constant_anatomy_summary()

    assert summary["status"] == "ok"
    assert summary["q"] == 3
    assert summary["k"] == 12
    assert summary["v"] == 40
    assert summary["mu"] == 4
    assert summary["E"] == 240
