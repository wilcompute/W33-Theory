from __future__ import annotations

from exploration.w33_levi_unitarity_triangle_bridge import build_summary


def test_levi_unitarity_triangle_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_unitarity_triangle_theorem"]
    data = summary["levi_unitarity_triangle_dictionary"]

    assert theorem["the_exact_apex_radius_Ru_is_108_over_265"] is True
    assert theorem["the_exact_gamma_phase_tangent_is_16_sqrt_15_over_27"] is True
    assert theorem["the_gamma_phase_has_exact_rational_squares_cos2_243_over_1523_and_sin2_1280_over_1523"] is True
    assert theorem["the_CKM_apex_is_exactly_the_polar_packet_Ru_times_cos_gamma_sin_gamma"] is True
    assert theorem["the_remaining_unitarity_triangle_angles_close_exactly_alpha_plus_beta_plus_gamma_equals_pi"] is True
    assert theorem["the_exact_Levi_family_seed_package_closes_to_a_realistic_unitarity_triangle"] is True

    assert data["R_u"]["exact"] == "108/265"
    assert data["cos2_gamma"]["exact"] == "243/1523"
    assert data["sin2_gamma"]["exact"] == "1280/1523"
