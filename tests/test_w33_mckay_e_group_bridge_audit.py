from __future__ import annotations

from scripts.w33_mckay_e_group_bridge_audit import (
    build_mckay_e_group_bridge_summary,
)


def test_mckay_e_group_orders_are_multiples_of_k() -> None:
    summary = build_mckay_e_group_bridge_summary()

    k = summary["k"]
    assert k == 12
    mg = summary["mckay_e_groups"]
    assert mg["mE6"]["order"] == 24
    assert mg["mE7"]["order"] == 48
    assert mg["mE8"]["order"] == 120
    assert mg["mE6"]["order"] % k == 0
    assert mg["mE7"]["order"] % k == 0
    assert mg["mE8"]["order"] % k == 0
    assert mg["mE6"]["order_over_k"] == 2
    assert mg["mE7"]["order_over_k"] == 4
    assert mg["mE8"]["order_over_k"] == 10


def test_PSL_2_q_order_equals_SRG_degree_k() -> None:
    summary = build_mckay_e_group_bridge_summary()

    assert summary["PSL_2_q"] == summary["k"]
    assert summary["PSL_2_q"] == 12


def test_sum_mckay_E_orders_equals_W_D4_flag_count() -> None:
    summary = build_mckay_e_group_bridge_summary()

    assert summary["sum_mckay_E"] == 192
    assert summary["sum_mckay_E"] == 16 * summary["k"]
    assert summary["sum_mckay_E"] == summary["W_D4"]
    assert summary["W_D4"] == 192


def test_mE7_plus_mE8_equals_PSL_2_phi6() -> None:
    summary = build_mckay_e_group_bridge_summary()

    mg = summary["mckay_e_groups"]
    mE7 = mg["mE7"]["order"]
    mE8 = mg["mE8"]["order"]
    assert mE7 + mE8 == 168
    assert mE7 + mE8 == summary["PSL_2_phi6"]
    assert summary["PSL_2_phi6"] == 168
    assert summary["phi6"] == 7


def test_T_equals_h_E7_times_k_plus_1() -> None:
    summary = build_mckay_e_group_bridge_summary()

    assert summary["T"] == 217
    assert summary["h_E7"] == 18
    assert summary["h_E7"] * summary["k"] + 1 == summary["T"]


def test_T_equals_W_D4_plus_mE6_plus_1() -> None:
    summary = build_mckay_e_group_bridge_summary()

    mE6 = summary["mckay_e_groups"]["mE6"]["order"]
    assert summary["W_D4"] + mE6 + 1 == summary["T"]
    assert 192 + 24 + 1 == 217


def test_T_minus_1_equals_q_factorial_cubed_and_h_E6_times_h_E7() -> None:
    summary = build_mckay_e_group_bridge_summary()

    T = summary["T"]
    q_fact = summary["q_factorial"]
    h_E6 = summary["h_E6"]
    h_E7 = summary["h_E7"]
    assert T - 1 == q_fact**3
    assert T - 1 == h_E6 * h_E7
    assert T - 1 == 216


def test_mE7_equals_F4_root_count() -> None:
    summary = build_mckay_e_group_bridge_summary()

    # |Phi(F4)| = rank(F4)*h(F4) = 4*12 = 48
    mE7 = summary["mckay_e_groups"]["mE7"]["order"]
    assert mE7 == 4 * summary["k"]
    assert mE7 == 48


def test_mE8_multiplier_over_k_equals_phi4() -> None:
    summary = build_mckay_e_group_bridge_summary()

    mE8_over_k = summary["mckay_e_groups"]["mE8"]["order_over_k"]
    assert mE8_over_k == summary["phi4"]
    assert mE8_over_k == 10


def test_mE8_equals_q_plus_2_factorial() -> None:
    summary = build_mckay_e_group_bridge_summary()

    q = summary["q"]
    mE8 = summary["mckay_e_groups"]["mE8"]["order"]
    assert mE8 == 120
    # (q+2)! = 5! = 120
    factorial_q_plus_2 = 1
    for i in range(1, q + 3):
        factorial_q_plus_2 *= i
    assert mE8 == factorial_q_plus_2


def test_all_exact_factorizations_hold() -> None:
    summary = build_mckay_e_group_bridge_summary()

    assert all(summary["exact_factorizations"].values())


def test_theorem_all_clauses_hold() -> None:
    summary = build_mckay_e_group_bridge_summary()
    theorem = summary["theorem"]

    assert theorem["all_mckay_E_orders_are_multiples_of_SRG_degree_k"] is True
    assert theorem["PSL_2_q_order_equals_SRG_degree_k"] is True
    assert theorem["sum_of_mckay_E_orders_equals_W_D4_tomotope_flag_count"] is True
    assert theorem["mE7_plus_mE8_equals_PSL_2_Phi6"] is True
    assert theorem["the_transport_numerator_T_equals_h_E7_times_k_plus_1"] is True
    assert theorem["the_transport_numerator_T_equals_W_D4_plus_mE6_plus_1"] is True
    assert theorem["T_minus_1_equals_q_factorial_cubed_equals_h_E6_times_h_E7"] is True
    assert theorem["mE7_equals_F4_root_count"] is True
    assert theorem["mE8_multiplier_over_k_equals_phi4"] is True
    assert theorem["the_mckay_e_group_bridge_is_fully_exact"] is True


def test_status_ok() -> None:
    summary = build_mckay_e_group_bridge_summary()

    assert summary["status"] == "ok"
    assert summary["q"] == 3
    assert summary["k"] == 12
    assert summary["v"] == 40
    assert summary["W_D4"] == 192
    assert summary["T"] == 217
