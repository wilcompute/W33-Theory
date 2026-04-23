from __future__ import annotations

from scripts.w33_symplectic_spread_frame_audit import analyze


def test_symplectic_spread_frame_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["symplectic_spread_frame_theorem"]

    assert theorem["the_40_isotropic_lines_of_w33_admit_exactly_36_spreads"] is True
    assert theorem["every_spread_is_a_partition_of_the_40_points_into_10_isotropic_lines"] is True
    assert theorem["every_isotropic_line_lies_in_exactly_9_spreads"] is True
    assert theorem["for_every_anchor_point_the_36_spreads_split_as_4_anchor_lines_times_9"] is True
    assert theorem["for_every_anchor_point_each_spread_is_one_memory_line_plus_9_affine_measurement_lines"] is True
    assert theorem["every_spread_yields_a_complete_2qutrit_stabilizer_mub_frame"] is True
    assert theorem["the_symplectic_spread_frame_bridge_is_fully_closed"] is True


def test_symplectic_spread_frame_counts_and_anchor_sector_are_uniform() -> None:
    payload = analyze()
    spread_dictionary = payload["spread_dictionary"]
    anchor = payload["canonical_anchor_frame"]

    assert spread_dictionary["point_count"] == 40
    assert spread_dictionary["isotropic_line_count"] == 40
    assert spread_dictionary["spread_count"] == 36
    assert spread_dictionary["spread_size"] == 10
    assert spread_dictionary["line_occurrence_distribution"] == {9: 40}
    assert spread_dictionary["mub_max_deviation"] < 1e-12

    assert anchor["anchor_point"] == (1, 0, 0, 0)
    assert isinstance(anchor["anchor_index"], int)
    assert len(anchor["anchor_lines"]) == 4
    assert set(anchor["sector_sizes"].values()) == {9}

    sample = anchor["sample_spread_profile"]
    assert sample["lines_inside_hyperplane"] == 1
    assert sample["affine_direction_count"] == 9
    assert sample["affine_direction_points"] == sample["expected_affine_direction_points"]
