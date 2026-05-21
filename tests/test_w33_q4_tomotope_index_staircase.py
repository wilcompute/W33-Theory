from __future__ import annotations

from analysis.w33_q4_tomotope_index_staircase import q4_tomotope_index_staircase_packet


def test_mclxxxiv_staircase_and_area_values() -> None:
    packet = q4_tomotope_index_staircase_packet()

    assert packet["staircase"] == {
        "m0_medial_incidences": 48,
        "m1_q4_incidences": 96,
        "m2_tomotope_flags": 192,
        "m3_flag_doubler": 384,
        "identity": "48 -> 96 -> 192 -> 384 (x2 each step)",
    }
    assert packet["monodromy_area_lock"] == {
        "monodromy": 18432,
        "outer_rectangle": 18432,
        "inner_rectangle": 18432,
        "identity": "18432 = 48*384 = 96*192",
    }


def test_mclxxxiv_all_checks_pass() -> None:
    packet = q4_tomotope_index_staircase_packet()

    assert packet["checks"] == {
        "doubling_step_48_to_96": True,
        "doubling_step_96_to_192": True,
        "doubling_step_192_to_384": True,
        "staircase_ratio_is_1_2_4_8": True,
        "monodromy_equals_outer_rectangle": True,
        "monodromy_equals_inner_rectangle": True,
        "outer_inner_rectangles_match": True,
        "monodromy_over_m0_is_m3": True,
        "monodromy_over_m1_is_m2": True,
        "monodromy_over_m2_is_m1": True,
        "monodromy_over_m3_is_m0": True,
    }
    assert packet["n_verified"] == 11
