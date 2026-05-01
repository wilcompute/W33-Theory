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


# --- Individual algebra data tests ---

def test_root_count_table_ranks() -> None:
    summary = build_exceptional_root_system_summary()
    table = summary["root_count_table"]
    assert table["G2"]["rank"] == 2
    assert table["F4"]["rank"] == 4
    assert table["E6"]["rank"] == 6
    assert table["E7"]["rank"] == 7
    assert table["E8"]["rank"] == 8


def test_root_count_table_coxeter_numbers() -> None:
    summary = build_exceptional_root_system_summary()
    table = summary["root_count_table"]
    assert table["G2"]["h"] == 6
    assert table["F4"]["h"] == 12
    assert table["E6"]["h"] == 12
    assert table["E7"]["h"] == 18
    assert table["E8"]["h"] == 30


def test_root_count_table_dimensions() -> None:
    summary = build_exceptional_root_system_summary()
    table = summary["root_count_table"]
    assert table["G2"]["dim"] == 14
    assert table["F4"]["dim"] == 52
    assert table["E6"]["dim"] == 78
    assert table["E7"]["dim"] == 133
    assert table["E8"]["dim"] == 248


def test_root_count_over_q_fact_individual() -> None:
    summary = build_exceptional_root_system_summary()
    table = summary["root_count_table"]
    assert table["G2"]["root_count_over_q_fact"] == 2
    assert table["F4"]["root_count_over_q_fact"] == 8
    assert table["E6"]["root_count_over_q_fact"] == 12
    assert table["E7"]["root_count_over_q_fact"] == 21
    assert table["E8"]["root_count_over_q_fact"] == 40


def test_root_count_equals_rank_times_h() -> None:
    summary = build_exceptional_root_system_summary()
    table = summary["root_count_table"]
    for name, row in table.items():
        assert row["root_count"] == row["rank"] * row["h"], f"{name} root_count != rank*h"


def test_G2_root_count_equals_k() -> None:
    summary = build_exceptional_root_system_summary()
    # |Phi(G2)| = 12 = k
    assert summary["root_count_table"]["G2"]["root_count"] == summary["k"]


def test_F4_root_count_over_q_fact_equals_rank_E8() -> None:
    summary = build_exceptional_root_system_summary()
    # |Phi(F4)|/q! = 8 = rank(E8)
    table = summary["root_count_table"]
    assert table["F4"]["root_count_over_q_fact"] == table["E8"]["rank"]


def test_E8_root_count_over_q_fact_equals_v() -> None:
    summary = build_exceptional_root_system_summary()
    # |Phi(E8)|/q! = 40 = v
    assert summary["root_count_table"]["E8"]["root_count_over_q_fact"] == summary["v"]


# --- E-tower sub-field tests ---

def test_e_tower_identity_string() -> None:
    summary = build_exceptional_root_system_summary()
    et = summary["e_tower"]
    # identity is formatted as "(72+126+240)/6 = 73 = Phi_12(3) = 73"
    assert "72" in et["identity"]
    assert "126" in et["identity"]
    assert "240" in et["identity"]
    assert "73" in et["identity"]
    assert "Phi_12" in et["identity"]


def test_e_tower_sum_equals_phi_E6_plus_phi_E7_plus_phi_E8() -> None:
    summary = build_exceptional_root_system_summary()
    et = summary["e_tower"]
    assert et["sum"] == et["phi_E6"] + et["phi_E7"] + et["phi_E8"]
    assert et["sum"] == 438


def test_e_tower_sum_over_q_fact_equals_12_plus_21_plus_40() -> None:
    summary = build_exceptional_root_system_summary()
    et = summary["e_tower"]
    assert et["sum_over_q_fact"] == 12 + 21 + 40
    assert et["sum_over_q_fact"] == 73


# --- Partition sub-field tests ---

def test_partitions_phi4_equals_G2_F4_sum_over_q_fact() -> None:
    summary = build_exceptional_root_system_summary()
    p = summary["partitions"]
    assert p["G2_F4_sum_over_q_fact"] == summary["phi4"]
    assert summary["phi4"] == 10


def test_partitions_all_five_sum_over_q_fact_equals_phi4_plus_phi12() -> None:
    summary = build_exceptional_root_system_summary()
    p = summary["partitions"]
    assert p["all_five_sum_over_q_fact"] == summary["phi4"] + summary["phi12"]
    assert p["all_five_sum_over_q_fact"] == 83


def test_partitions_all_five_sum_over_q_fact_equals_q4_plus_2() -> None:
    summary = build_exceptional_root_system_summary()
    q = summary["q"]
    p = summary["partitions"]
    assert p["all_five_sum_over_q_fact"] == q**4 + 2


def test_E6_E8_cross_sum_over_q_fact_equals_dim_F4() -> None:
    summary = build_exceptional_root_system_summary()
    p = summary["partitions"]
    assert p["E6_E8_cross_sum_over_q_fact"] == p["dim_F4"]
    assert p["dim_F4"] == summary["root_count_table"]["F4"]["dim"]


# --- Phi12 connections ---

def test_phi12_equals_q4_minus_q2_plus_1_at_q3() -> None:
    summary = build_exceptional_root_system_summary()
    q = summary["q"]
    assert summary["phi12"] == q**4 - q**2 + 1
    assert summary["phi12"] == 73


def test_phi12_connections_index_equals_k_and_h_E6() -> None:
    summary = build_exceptional_root_system_summary()
    conn = summary["phi12_connections"]
    assert conn["index"] == summary["k"]
    assert conn["index"] == summary["root_count_table"]["E6"]["h"]
    assert conn["index_equals_k"] is True
    assert conn["index_equals_h_E6"] is True


def test_phi12_connections_C_phi6_2_equals_21() -> None:
    summary = build_exceptional_root_system_summary()
    phi6 = summary["phi6"]
    expected = phi6 * (phi6 - 1) // 2
    assert summary["phi12_connections"]["C_phi6_2"] == expected
    assert expected == 21


def test_phi12_connections_cyclotomic_product_equals_q12_minus_1() -> None:
    summary = build_exceptional_root_system_summary()
    q = summary["q"]
    conn = summary["phi12_connections"]
    # the string should contain the numeric value of q^12-1
    assert str(q**12 - 1) in conn["cyclotomic_product"]


def test_interpretation_field_present_and_nonempty() -> None:
    summary = build_exceptional_root_system_summary()
    assert "interpretation" in summary
    assert len(summary["interpretation"]) > 50


def test_lru_cache_returns_same_object() -> None:
    s1 = build_exceptional_root_system_summary()
    s2 = build_exceptional_root_system_summary()
    assert s1 is s2  # same cached object
