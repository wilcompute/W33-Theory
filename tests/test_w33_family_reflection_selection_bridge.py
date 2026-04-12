from __future__ import annotations

from exploration.w33_family_reflection_selection_bridge import build_summary


def test_family_reflection_selection_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_reflection_selection_theorem"]
    packet = summary["family_reflection_dictionary"]

    assert theorem["the_selected_family_operator_is_an_exact_involution"] is True
    assert theorem["the_selected_family_operator_has_trace_zero_and_determinant_minus_one"] is True
    assert theorem["the_ckm_family_axis_is_exactly_the_plus_one_eigenline_of_the_family_reflection"] is True
    assert theorem["the_promoted_neutrino_axis_is_exactly_the_minus_one_eigenline_of_the_same_family_reflection"] is True
    assert theorem["quark_family_asymmetry_and_neutrino_family_splitting_are_the_two_eigenlines_of_one_exact_family_involution"] is True

    assert packet["tetra_stabilizer_transposition"] == [0, 3, 2, 1]
    assert abs(packet["reflection_trace"]) < 1e-12
    assert abs(packet["reflection_determinant"] + 1.0) < 1e-12
