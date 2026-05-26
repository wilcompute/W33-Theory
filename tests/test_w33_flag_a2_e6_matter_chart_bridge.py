from __future__ import annotations

from analysis.w33_flag_a2_e6_matter_chart_bridge import flag_a2_e6_matter_chart_packet


PACKET = flag_a2_e6_matter_chart_packet()


def test_mccxlv_representative_flag_counts() -> None:
    counts = PACKET["representative_flag"]["counts"]

    assert counts["a2_root_singletons"] == 6
    assert counts["e6_triplets"] == 24
    assert counts["line_adjacent_triplets"] == 12
    assert counts["zero_adjacent_triplets"] == 12
    assert counts["plus_matter_triplets"] == 27
    assert counts["minus_matter_triplets"] == 27
    assert counts["all_triplets"] == 78
    assert counts["covered_corners"] == 240
    assert counts["plus_matter_corners"] == 81
    assert counts["minus_matter_corners"] == 81
    assert counts["e6_corners"] == 72


def test_mccxlv_all_flags_have_same_split() -> None:
    summary = PACKET["all_flag_summary"]

    assert summary["flags_checked"] == 160
    assert summary["bad_flags"] == []
    assert summary["affine_nonneighbor_count_profile"] == {"27": 40}
    assert summary["minus2_chart_rank_profile"] == {"81": 320}
    assert summary["e6_golden_rank_profile"] == {"24": 160}
    assert summary["induced_degree_profile"] == {"8": 25920}


def test_mccxlv_exact_minus2_coordinate_chart_certificate() -> None:
    certificate = PACKET["representative_flag"]["exact_mod7_chart_certificate"]

    assert certificate["rank_A3_plus_2I"] == 159
    assert certificate["minus2_nullity"] == 81
    assert certificate["rank_with_plus_sector_zero_constraints"] == 240
    assert certificate["rank_with_minus_sector_zero_constraints"] == 240


def test_mccxlv_ternary_hypercube_budget_is_twisted() -> None:
    budget = PACKET["representative_flag"]["ternary_hypercube_budget"]

    assert budget["vertices_per_matter_sector"] == 81
    assert budget["affine_nonneighbor_base"] == 27
    assert budget["fiber_size"] == 3
    assert budget["plus_induced_edges"] == 324
    assert budget["minus_induced_edges"] == 324
    assert budget["same_budget_as_hamming_H_4_3"] is True
    assert budget["not_plain_hamming_graph"] is True
    assert budget["plus_induced_spectrum"] != budget["hamming_H_4_3_spectrum"]
    assert budget["minus_induced_spectrum"] != budget["hamming_H_4_3_spectrum"]


def test_mccxlv_naive_triplet_sum_boundary() -> None:
    quotient = PACKET["representative_flag"]["triplet_quotient_rank_test"]

    assert quotient["golden_24d_triplet_sum_rank"] == 24
    assert quotient["minus2_triplet_sum_rank"] == 35
    assert "not the missing rank-8" in quotient["reading"]


def test_mccxlv_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())
