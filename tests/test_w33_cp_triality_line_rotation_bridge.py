from __future__ import annotations

from exploration.w33_cp_triality_line_rotation_bridge import build_summary


def test_cp_triality_line_rotation_bridge() -> None:
    summary = build_summary()
    theorem = summary["cp_triality_line_rotation_theorem"]
    split = summary["triality_line_rotation_split"]

    assert theorem["each_bivector_triplet_splits_under_the_triality_cycle_as_fixed_line_plus_rotating_plane"] is True
    assert theorem["the_live_sector_3_fixed_line_norm_squared_is_exactly_4_delta_squared_over_3"] is True
    assert theorem["the_live_sector_3_rotating_plane_norm_squared_is_exactly_2_sigma_squared_plus_8_delta_squared_over_3"] is True
    assert theorem["the_live_sector_3prime_fixed_line_norm_squared_is_exactly_4_sigma_squared_over_3"] is True
    assert theorem["the_live_sector_3prime_rotating_plane_norm_squared_is_exactly_2_sigma_squared_over_3"] is True
    assert theorem["cp_is_therefore_the_triality_line_rotation_shadow_of_the_same_family_scalars_sigma_and_delta"] is True

    assert abs(split["3"]["total_norm_squared"] - 0.183217935) < 1e-12
    assert abs(split["3'"]["total_norm_squared"] - 0.07908264500000002) < 1e-12
