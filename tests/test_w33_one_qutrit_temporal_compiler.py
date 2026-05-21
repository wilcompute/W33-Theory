from __future__ import annotations

from analysis.w33_one_qutrit_temporal_compiler import one_qutrit_temporal_compiler_packet


def test_mclxvii_seed_and_compiled_substrate() -> None:
    packet = one_qutrit_temporal_compiler_packet()

    assert packet["seed"] == {
        "q": 3,
        "single_qutrit_dim": 3,
        "temporal_double_dim": 9,
        "history_cells": 9,
        "history_split": "9 = 3 + 6",
        "choi_now_rule": "<Omega|(I tensor U)|Omega> = Tr(U)/3",
    }
    assert packet["compiled_substrate"] == {
        "projective_rays": 40,
        "w33_edges": 240,
        "complete_context_count": 10,
        "context_size": 4,
        "frame_closure": 40,
        "maximal_mub_for_d9": 10,
    }


def test_mclxvii_bell_cloud_and_minimality() -> None:
    packet = one_qutrit_temporal_compiler_packet()

    assert packet["bell_local_cloud"] == {
        "bell_spreads": 9,
        "shell": "1 + 12 + 27 = 40",
        "cloud_identity": "9 Bell spreads * 9 companions = 81 incidences = 27 lines * 3",
        "distinct_companions": 27,
        "total_companion_incidences": 81,
    }
    assert packet["minimality_dictionary"] == {
        "projective_count_formula": "(q^4-1)/(q-1)",
        "q_equals_2_value": 15,
        "q_equals_3_value": 40,
        "w33_target": 40,
        "statement": "q=3 is the smallest prime-power seed producing 40 projective two-qutrit rays",
    }


def test_mclxvii_all_checks_pass() -> None:
    packet = one_qutrit_temporal_compiler_packet()

    assert packet["checks"] == {
        "single_qutrit_temporal_double_has_9_history_cells": True,
        "history_split_is_diagonal_plus_directed": True,
        "projective_two_qutrit_geometry_is_exactly_w33": True,
        "complete_now_frame_closure_is_10_times_4_equals_40": True,
        "bell_line_cloud_closes_as_1_plus_12_plus_27": True,
        "bell_companion_cloud_is_81_equals_27_times_3": True,
        "harmonic_and_cloud_counts_lock": True,
        "q3_is_smallest_seed_for_w33_cardinality": True,
        "maximal_stabilizer_mub_count_for_d9_is_10": True,
    }
    assert packet["n_verified"] == 9
