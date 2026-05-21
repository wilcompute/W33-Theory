from __future__ import annotations

from analysis.w33_vacuum_increment_action_lock import vacuum_increment_action_lock_packet


def test_mclxv_constants_packet() -> None:
    packet = vacuum_increment_action_lock_packet()

    assert packet["constants"] == {
        "v": 40,
        "k": 12,
        "K": "801/20",
        "delta_K": "1/20",
        "S_holo": "20",
        "E_seidel": "240",
        "I_temporal": "360",
        "lambda_spine": "18",
        "nu_gap": "5/6",
        "sigma_0": "15",
        "mult_gap": "24",
    }


def test_mclxv_lock_values() -> None:
    packet = vacuum_increment_action_lock_packet()

    assert packet["locks"] == {
        "deltaK_times_E_seidel": "12",
        "deltaK_times_I_temporal": "18",
        "nu_gap_times_lambda_spine": "15",
        "S_holo_times_lambda_spine": "360",
        "sigma0_times_mult_gap": "360",
        "three_halves_E_seidel": "360",
    }


def test_mclxv_all_theorem_flags_hold() -> None:
    packet = vacuum_increment_action_lock_packet()

    assert packet["checks"] == {
        "vacuum_increment_equals_one_over_S_holo": True,
        "vacuum_increment_times_seidel_energy_equals_degree": True,
        "vacuum_increment_times_temporal_incidence_equals_morita_spine_eigenvalue": True,
        "morita_spine_gap_product_equals_sigma0": True,
        "temporal_incidence_factorizes_by_holographic_shell": True,
        "temporal_incidence_factorizes_by_uv_gap_shell": True,
        "temporal_incidence_is_three_halves_seidel_energy": True,
        "lambda_spine_half_is_q_squared_history_count": True,
    }
    assert packet["n_verified"] == 8
