from __future__ import annotations

from exploration.w33_family_triality_complex_structure_bridge import build_summary


def test_family_triality_complex_structure_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_triality_complex_structure_theorem"]

    assert theorem["the_family_reflection_is_exactly_diag_1_minus1_in_the_qn_basis"] is True
    assert theorem["the_triality_three_cycle_is_exactly_minus_half_I_plus_sqrt3_over_2_times_J"] is True
    assert theorem["the_derived_family_J_squares_to_minus_identity"] is True
    assert theorem["the_neutrino_axis_is_exactly_minus_J_times_the_quark_axis"] is True
    assert theorem["the_family_plane_is_therefore_a_true_triality_complex_plane_not_just_a_real_cartan_plane"] is True
