from __future__ import annotations

from analysis.w33_temporal_bell_cocontext_cloud import temporal_bell_cocontext_cloud_packet


def test_mclxvi_bell_local_shell_is_exact() -> None:
    packet = temporal_bell_cocontext_cloud_packet()

    assert packet["bell_local_line_shell"] == {
        "total_lines": 40,
        "bell_line": 1,
        "intersecting_lines": 12,
        "disjoint_lines": 27,
        "identity": "1 + 12 + 27 = 40",
    }


def test_mclxvi_cocontext_cloud_counts() -> None:
    packet = temporal_bell_cocontext_cloud_packet()

    assert packet["cocontext_cloud"] == {
        "spreads_with_bell": 9,
        "companions_per_spread": 9,
        "total_companion_incidences": 81,
        "distinct_companion_lines": 27,
        "multiplicity_distribution": {3: 27},
        "identity": "9 Bell spreads * 9 companions = 81 incidences = 27 lines * 3",
    }


def test_mclxvi_all_checks_pass() -> None:
    packet = temporal_bell_cocontext_cloud_packet()

    assert packet["checks"] == {
        "bell_line_is_in_exactly_9_spreads": True,
        "bell_centered_companion_incidence_total_is_81": True,
        "distinct_companion_lines_are_exactly_27": True,
        "all_companion_lines_have_multiplicity_3": True,
        "companion_set_equals_disjoint_shell": True,
        "bell_local_shell_is_1_plus_12_plus_27": True,
        "weighted_companion_multiplicity_matches_incidence": True,
    }
    assert packet["n_verified"] == 7
