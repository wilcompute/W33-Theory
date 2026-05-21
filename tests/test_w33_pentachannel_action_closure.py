from __future__ import annotations

from analysis.w33_pentachannel_action_closure import pentachannel_action_closure_packet


def test_mclxviii_action_star_channels_match() -> None:
    packet = pentachannel_action_closure_packet()

    assert packet["action_star"] == {
        "value": "360",
        "channels": {
            "temporal_harmonic": "360",
            "geometric_frame": "360",
            "holographic_morita": "360",
            "uv_gap_shell": "360",
            "seidel_rescaled": "360",
        },
        "identities": [
            "360 = 9*40",
            "360 = 40*(10-1)",
            "360 = 20*18",
            "360 = 15*24",
            "360 = (3/2)*240",
        ],
    }


def test_mclxviii_bell_cloud_bridge_values() -> None:
    packet = pentachannel_action_closure_packet()

    assert packet["bell_cloud_bridge"] == {
        "bell_spreads": 9,
        "history_cells": 9,
        "total_companion_incidences": 81,
        "distinct_companions": 27,
        "identity": "81 = 9*9 = 27*3",
        "action_to_cloud_ratio": "40/9",
    }


def test_mclxviii_all_checks_pass() -> None:
    packet = pentachannel_action_closure_packet()

    assert packet["checks"] == {
        "all_five_channel_actions_are_identical": True,
        "shared_action_is_360": True,
        "history_times_frame_closure_is_action_star": True,
        "rays_times_nonanchor_contexts_is_action_star": True,
        "holographic_spine_is_action_star": True,
        "uv_shell_is_action_star": True,
        "seidel_rescaled_action_is_action_star": True,
        "bell_cloud_factors_as_9_times_9": True,
        "bell_cloud_compression_factor_is_4_to_action": True,
        "triangle_energy_bridge_holds": True,
        "radius_times_spine_exceeds_gap_threshold": True,
        "cloud_distinct_plus_shell_intersections_plus_bell_is_w33_line_total": True,
    }
    assert packet["n_verified"] == 12
