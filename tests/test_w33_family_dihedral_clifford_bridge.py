from __future__ import annotations

from exploration.w33_family_dihedral_clifford_bridge import build_summary


def test_family_dihedral_clifford_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_dihedral_clifford_theorem"]
    dictionary = summary["family_algebra_dictionary"]

    assert theorem["the_family_reflection_and_triality_cycle_generate_an_exact_D6_action"] is True
    assert theorem["the_family_complex_structure_is_recovered_exactly_from_the_triality_cycle"] is True
    assert theorem["R_and_J_are_exact_Cl_1_1_generators_with_R_squared_1_J_squared_minus1_and_anticommutator_zero"] is True
    assert theorem["the_span_of_I_R_J_RJ_is_exactly_four_dimensional_and_so_is_the_full_family_plane_matrix_algebra"] is True
    assert theorem["the_quark_and_neutrino_axis_projectors_are_exactly_the_two_idempotents_of_the_family_reflection"] is True
    assert theorem["the_common_family_plane_is_therefore_one_exact_D6_inside_Cl_1_1_operator_algebra"] is True

    assert dictionary["d6_group_span_rank"] == 4
    assert dictionary["clifford_basis_rank"] == 4
