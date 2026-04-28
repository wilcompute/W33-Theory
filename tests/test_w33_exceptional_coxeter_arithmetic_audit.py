from __future__ import annotations

from math import comb

from scripts.w33_exceptional_coxeter_arithmetic_audit import (
    build_exceptional_coxeter_arithmetic_summary,
)


def test_coxeter_addition_small_pair_equals_h_E7() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    h = summary["coxeter_numbers"]
    assert h["G2"] + h["F4"] == h["E7"]
    assert h["G2"] == 6
    assert h["F4"] == 12
    assert h["E7"] == 18


def test_E_tower_addition_theorem_h_E6_plus_h_E7_equals_h_E8() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    h = summary["coxeter_numbers"]
    assert h["E6"] + h["E7"] == h["E8"]
    assert 12 + 18 == 30


def test_E_tower_coxeter_sum_equals_5k_and_A5_order() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    cs = summary["coxeter_sums"]
    assert cs["E_tower_sum"] == 60
    assert cs["E_tower_sum_over_k"] == 5
    assert cs["A5_order"] == 60
    assert cs["E_tower_sum"] == 5 * summary["k"]


def test_all_five_exceptional_coxeter_sum_equals_dim_E6() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    cs = summary["coxeter_sums"]
    assert cs["all_five_sum"] == 78
    assert cs["dim_E6"] == 78
    assert cs["all_five_sum"] == cs["dim_E6"]


def test_dim_E6_equals_C_k_2_plus_k() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    k = summary["k"]
    assert summary["dimensions"]["E6"] == comb(k, 2) + k
    assert comb(k, 2) + k == 78


def test_dim_E7_equals_phi12_plus_E_tower_sum() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    da = summary["dimension_arithmetic"]
    assert summary["dimensions"]["E7"] == summary["phi12"] + summary["coxeter_sums"]["E_tower_sum"]
    assert 133 == 73 + 60


def test_dim_E7_minus_dim_E6_equals_C_k_minus_1_2() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    k = summary["k"]
    da = summary["dimension_arithmetic"]
    assert da["dim_E7_minus_E6"] == comb(k - 1, 2)
    assert da["C_k_minus_1_2"] == 55


def test_dim_E8_minus_T_equals_h_E8_plus_1() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    da = summary["dimension_arithmetic"]
    assert da["dim_E8_minus_T"] == 31
    assert da["h_E8_plus_1"] == 31
    assert summary["dimensions"]["E8"] - summary["T"] == summary["coxeter_numbers"]["E8"] + 1


def test_bosonic_string_dim_equals_2_phi3() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    sd = summary["string_dimensions"]
    assert sd["bosonic_string"] == 26
    assert 2 * summary["phi3"] == sd["bosonic_string"]
    assert 2 * 13 == 26


def test_superstring_dim_equals_k_minus_2_equals_phi4() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    sd = summary["string_dimensions"]
    assert sd["superstring"] == 10
    assert summary["k"] - 2 == sd["superstring"]
    assert summary["phi4"] == sd["superstring"]


def test_M_theory_dim_equals_k_minus_1() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    sd = summary["string_dimensions"]
    assert sd["M_theory"] == 11
    assert summary["k"] - 1 == sd["M_theory"]


def test_SM_gauge_dim_equals_k() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    sd = summary["string_dimensions"]
    assert sd["SM_gauge"] == summary["k"]
    assert sd["SM_gauge"] == 12


def test_leech_lattice_dim_equals_phi_E8_over_phi4() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    lb = summary["leech_bridge"]
    assert lb["phi_E8"] == 240
    assert lb["leech_dim"] == 24
    assert lb["leech_dim"] == 4 * summary["q_factorial"]
    assert 240 // summary["phi4"] == 24


def test_bosonic_string_equals_leech_plus_2() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    lb = summary["leech_bridge"]
    sd = summary["string_dimensions"]
    assert sd["bosonic_string"] == lb["leech_dim"] + 2
    assert 26 == 24 + 2


def test_all_exact_factorizations_hold() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    assert all(summary["exact_factorizations"].values())


def test_theorem_all_clauses_hold() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()
    theorem = summary["theorem"]

    assert theorem["the_small_exceptional_coxeter_sum_h_G2_plus_h_F4_equals_h_E7"] is True
    assert theorem["the_E_tower_addition_theorem_h_E6_plus_h_E7_equals_h_E8"] is True
    assert theorem["the_E_tower_coxeter_sum_equals_5k_equals_A5_order"] is True
    assert theorem["the_all_five_exceptional_coxeter_sum_equals_dim_E6"] is True
    assert theorem["dim_E6_equals_C_k_2_plus_k"] is True
    assert theorem["dim_E7_equals_phi12_plus_E_tower_coxeter_sum"] is True
    assert theorem["dim_E8_minus_T_equals_rank_quotient_h_E8_plus_1"] is True
    assert theorem["bosonic_string_dim_equals_2_phi3_at_q"] is True
    assert theorem["superstring_dim_equals_k_minus_2_equals_phi4"] is True
    assert theorem["leech_lattice_dim_equals_phi_E8_over_phi4_equals_4_q_factorial"] is True
    assert theorem["the_exceptional_coxeter_arithmetic_is_fully_exact"] is True


def test_status_ok() -> None:
    summary = build_exceptional_coxeter_arithmetic_summary()

    assert summary["status"] == "ok"
    assert summary["q"] == 3
    assert summary["k"] == 12
    assert summary["v"] == 40
    assert summary["T"] == 217
    assert summary["phi3"] == 13
    assert summary["phi4"] == 10
    assert summary["phi12"] == 73
