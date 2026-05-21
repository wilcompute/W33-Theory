from __future__ import annotations

from analysis.w33_temporal_morita_holographic_lock import (
    temporal_morita_holographic_lock_packet,
)


def test_temporal_shell_matches_bell_spread_lock() -> None:
    packet = temporal_morita_holographic_lock_packet()

    assert packet["temporal_shell"] == {
        "q": 3,
        "bell_line": (6, 16, 27, 35),
        "temporal_history_square": 9,
        "spreads_through_bell_line": 9,
        "spread_size": 10,
        "context_size": 4,
        "identity": "9 Bell-line spreads × 10 contexts × 4 rays = 360 line-spread incidences",
    }


def test_extremal_shell_matches_temporal_frame_sizes() -> None:
    packet = temporal_morita_holographic_lock_packet()

    assert packet["extremal_shell"] == {
        "alpha": "10",
        "theta_G": "10",
        "theta_Gbar": "4",
        "omega": "4",
        "chi_f": "4",
    }


def test_morita_and_holographic_shells_lock_exactly() -> None:
    packet = temporal_morita_holographic_lock_packet()

    assert packet["morita_shell"] == {
        "spread_kernel_dimension": 20,
        "line_cokernel_dimension": 24,
        "common_spine_dimension": 16,
        "common_spine_formula": "k - s",
        "common_spine_value": 16,
        "obstruction_gap": 4,
    }
    assert packet["holographic_shell"] == {
        "S_holo": "20",
        "nu_gap": "5/6",
        "S_holo_over_nu_gap": "24",
        "gap_multiplicity": 24,
    }


def test_all_mclxiv_lock_checks_hold() -> None:
    packet = temporal_morita_holographic_lock_packet()

    assert packet["checks"] == {
        "bell_line_lies_in_q_squared_spreads": True,
        "spread_size_equals_theta_and_alpha": True,
        "context_size_equals_theta_bar_omega_chi_f": True,
        "spread_kernel_equals_S_holo": True,
        "line_cokernel_equals_gap_multiplicity": True,
        "line_cokernel_equals_S_holo_over_nu_gap": True,
        "common_spine_equals_k_minus_s": True,
        "obstruction_gap_equals_context_size": True,
        "incidence_counts_match_temporal_frame_shell": True,
    }
    assert packet["n_verified"] == 9