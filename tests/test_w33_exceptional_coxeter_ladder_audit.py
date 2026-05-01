from __future__ import annotations

from scripts.w33_exceptional_coxeter_ladder_audit import (
    build_exceptional_coxeter_ladder_summary,
)


def test_exceptional_coxeter_numbers_are_multiples_of_q_factorial() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    assert summary["q_factorial"] == 6
    assert summary["coxeter_numbers"]["h_G2"] == 6
    assert summary["coxeter_numbers"]["h_F4"] == 12
    assert summary["coxeter_numbers"]["h_E6"] == 12
    assert summary["coxeter_numbers"]["h_E7"] == 18
    assert summary["coxeter_numbers"]["h_E8"] == 30
    assert summary["coxeter_multipliers_over_q_factorial"] == {
        "G2": 1, "F4": 2, "E6": 2, "E7": 3, "E8": 5
    }


def test_h_E6_equals_SRG_degree_k() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    assert summary["coxeter_numbers"]["h_E6"] == summary["k"]
    assert summary["coxeter_numbers"]["h_F4"] == summary["k"]
    assert summary["k"] == 12


def test_distinct_multipliers_are_fibonacci_and_sum_to_k_minus_1() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    assert summary["distinct_multipliers"] == [1, 2, 3, 5]
    assert sum(summary["distinct_multipliers"]) == summary["k"] - 1


def test_fibonacci_context_is_correct() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    fib = summary["fibonacci_context"]
    assert fib["F1"] == 1
    assert fib["F3"] == 2
    assert fib["F4"] == 3
    assert fib["F5"] == 5


def test_E_tower_step_sizes_are_q_factorial_and_k() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    steps = summary["step_sizes"]
    assert steps["h_E7_minus_h_E6"] == summary["q_factorial"]  # 6
    assert steps["h_E8_minus_h_E7"] == summary["k"]             # 12


def test_sum_identities_hold() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    sums = summary["sum_identities"]
    assert sums["h_G2_plus_h_E6_plus_h_E7_plus_h_E8"] == 66
    assert sums["C_k_2"] == 66
    assert sums["sum_all_five"] == 78
    assert sums["dim_E6"] == 78


def test_dimension_rank_identities_hold() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    dr = summary["dimension_rank_identities"]
    assert dr["dim_E6"] == 78
    assert dr["rank_E6"] == 6
    assert dr["dim_E6_over_rank_E6"] == 13   # = Phi3
    assert dr["dim_E8"] == 248
    assert dr["rank_E8"] == 8
    assert dr["dim_E8_over_rank_E8"] == 31   # = h(E8)+1
    assert dr["h_E8_plus_1"] == 31


def test_transport_bridge_connects_Coxeter_ladder_to_T_217() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    bridge = summary["transport_bridge"]
    assert bridge["T"] == 217
    assert bridge["phi6"] == 7
    assert bridge["dim_E8_over_rank_E8"] == 31
    assert bridge["factorization"] == "7 * (dim(E8)/rank(E8)) = 7 * 31 = 217"


def test_all_exact_factorizations_hold() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    assert all(summary["exact_factorizations"].values())


def test_theorem_all_clauses_hold() -> None:
    summary = build_exceptional_coxeter_ladder_summary()
    theorem = summary["theorem"]

    assert theorem["all_exceptional_coxeter_numbers_are_multiples_of_q_factorial"] is True
    assert theorem["h_E6_equals_the_SRG_degree_k"] is True
    assert theorem["the_distinct_multipliers_1_2_3_5_are_fibonacci_and_sum_to_k_minus_1"] is True
    assert theorem["the_E_tower_step_sizes_are_q_factorial_and_k"] is True
    assert theorem["the_G2_E_tower_sum_equals_C_k_2"] is True
    assert theorem["the_sum_of_all_five_exceptional_coxeter_numbers_equals_dim_E6"] is True
    assert theorem["dim_E6_over_rank_equals_phi3"] is True
    assert theorem["dim_E8_over_rank_equals_h_E8_plus_1"] is True
    assert theorem["the_transport_numerator_T_equals_phi6_times_dim_E8_over_rank_E8"] is True
    assert theorem["the_exceptional_coxeter_ladder_is_fully_exact"] is True


def test_status_ok() -> None:
    summary = build_exceptional_coxeter_ladder_summary()

    assert summary["status"] == "ok"
    assert summary["q"] == 3
    assert summary["k"] == 12
    assert summary["v"] == 40
