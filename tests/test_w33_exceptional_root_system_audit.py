from __future__ import annotations

from scripts.w33_exceptional_root_system_audit import (
    build_exceptional_root_system_summary,
)


def test_all_exceptional_root_counts_are_multiples_of_q_factorial() -> None:
    summary = build_exceptional_root_system_summary()

    table = summary["root_count_table"]
    assert table["G2"]["root_count"] == 12
    assert table["F4"]["root_count"] == 48
    assert table["E6"]["root_count"] == 72
    assert table["E7"]["root_count"] == 126
    assert table["E8"]["root_count"] == 240
    assert all(row["root_count"] % summary["q_factorial"] == 0 for row in table.values())
    assert [row["root_count_over_q_fact"] for row in table.values()] == [2, 8, 12, 21, 40]


def test_E8_root_count_equals_SRG_edge_count() -> None:
    summary = build_exceptional_root_system_summary()

    assert summary["root_count_table"]["E8"]["root_count"] == 240
    assert summary["E"] == 240
    assert summary["v"] * summary["q_factorial"] == 240


def test_E6_root_count_equals_rank_times_k() -> None:
    summary = build_exceptional_root_system_summary()

    table = summary["root_count_table"]
    assert table["E6"]["root_count"] == table["E6"]["rank"] * summary["k"]
    assert table["E6"]["root_count"] == 72


def test_E7_root_count_over_q_fact_equals_C_phi6_2() -> None:
    summary = build_exceptional_root_system_summary()

    phi6 = summary["phi6"]
    C_phi6_2 = phi6 * (phi6 - 1) // 2   # C(7,2) = 21
    assert summary["root_count_table"]["E7"]["root_count_over_q_fact"] == C_phi6_2
    assert C_phi6_2 == 21


def test_e_tower_sum_over_q_fact_equals_phi12() -> None:
    summary = build_exceptional_root_system_summary()

    et = summary["e_tower"]
    assert et["phi_E6"] == 72
    assert et["phi_E7"] == 126
    assert et["phi_E8"] == 240
    assert et["sum"] == 438
    assert et["sum_over_q_fact"] == 73
    assert et["phi12"] == 73
    assert summary["phi12"] == summary["q"]**4 - summary["q"]**2 + 1


def test_phi12_index_equals_k_and_h_E6() -> None:
    summary = build_exceptional_root_system_summary()

    conn = summary["phi12_connections"]
    assert conn["phi12"] == 73
    assert conn["index"] == 12
    assert conn["index_equals_k"] is True
    assert conn["index_equals_h_E6"] is True
    assert conn["C_phi6_2"] == 21


def test_partition_sum_identities() -> None:
    summary = build_exceptional_root_system_summary()

    p = summary["partitions"]
    assert p["G2_F4_sum"] == 60
    assert p["G2_F4_sum_over_q_fact"] == summary["phi4"]   # 10
    assert p["E6_E8_cross_sum"] == 312
    assert p["E6_E8_cross_sum_over_q_fact"] == 52           # dim(F4)
    assert p["dim_F4"] == 52
    assert p["all_five_sum"] == 498
    assert p["all_five_sum_over_q_fact"] == 83
    assert p["q4_plus_2"] == 83


def test_cyclotomic_product_identity() -> None:
    summary = build_exceptional_root_system_summary()

    q = summary["q"]
    conn = summary["phi12_connections"]
    assert conn["cyclotomic_product"] == f"Phi1*Phi2*Phi3*Phi4*Phi6*Phi12 = {q**12 - 1} = q^12-1"


def test_all_exact_factorizations_hold() -> None:
    summary = build_exceptional_root_system_summary()

    assert all(summary["exact_factorizations"].values())


def test_theorem_all_clauses_hold() -> None:
    summary = build_exceptional_root_system_summary()
    theorem = summary["theorem"]

    assert theorem["all_exceptional_root_counts_are_multiples_of_q_factorial"] is True
    assert theorem["the_E8_root_count_equals_the_SRG_edge_count_v_times_q_factorial"] is True
    assert theorem["the_E6_root_count_equals_rank_E6_times_k"] is True
    assert theorem["the_E7_root_count_over_q_factorial_equals_C_phi6_2"] is True
    assert theorem["the_E_tower_root_count_sum_over_q_factorial_equals_phi12_q"] is True
    assert theorem["the_G2_F4_partition_sum_over_q_factorial_equals_phi4"] is True
    assert theorem["the_E6_E8_cross_sum_over_q_factorial_equals_dim_F4"] is True
    assert theorem["the_phi12_index_equals_k_the_E6_coxeter_number_and_SRG_degree"] is True
    assert theorem["the_exceptional_root_system_counting_is_fully_exact"] is True


def test_status_ok() -> None:
    summary = build_exceptional_root_system_summary()

    assert summary["status"] == "ok"
    assert summary["q"] == 3
    assert summary["k"] == 12
    assert summary["v"] == 40
    assert summary["E"] == 240
    assert summary["q_factorial"] == 6
    assert summary["phi4"] == 10
    assert summary["phi6"] == 7
    assert summary["phi12"] == 73
