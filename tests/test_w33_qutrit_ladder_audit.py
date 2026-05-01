from __future__ import annotations

from pathlib import Path

import pytest

from scripts.w33_qutrit_ladder_audit import (
    analyze,
    classify_qutrit_ladder,
    e8_side_exact_decomposition_summary,
    one_qutrit_local_layer_summary,
    six_qutrit_backbone_summary,
    three_qutrit_sl27_layer_summary,
    two_qutrit_global_layer_summary,
)

SAGE_TRANSPORT = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "sage_h27_to_schlafli_effective_triads_conjugacy.json"
)

pytestmark = pytest.mark.skipif(
    not SAGE_TRANSPORT.exists(),
    reason="optional Sage H27-to-Schlafli transport artifact is absent",
)


def test_one_qutrit_local_layer_is_exact_heisenberg_mub_shell() -> None:
    summary = one_qutrit_local_layer_summary()

    assert summary["visible_shell_size"] == 27
    assert summary["mub_class_count"] == 4
    assert summary["mub_class_sizes"] == (3, 3, 3, 3)
    assert summary["fiber_count"] == 9
    assert summary["fiber_size"] == 3
    assert summary["generation_fiber_sizes"] == (9, 9, 9)
    assert summary["schlafli_parameters"] == (27, 16, 10, 8)
    assert summary["tritangent_split"] == {
        "classical_total": 45,
        "internal_shell": 36,
        "missing_center_cosets": 9,
    }
    assert summary["heisenberg_sl23_order"] == 648
    assert summary["heisenberg_gl23_order"] == 1296
    assert summary["affine_point_stabilizer_order"] == 48
    assert summary["full_45_triads_invariant"] is True


def test_two_qutrit_global_layer_is_exact_pauli_clifford_kernel() -> None:
    summary = two_qutrit_global_layer_summary()

    assert summary["weyl_basis_size"] == 81
    assert summary["projective_point_count"] == 40
    assert summary["edge_count"] == 240
    assert summary["generator_names"] == ("S1", "T1", "S2", "T2", "SWAP")
    assert summary["all_generators_verified"] is True
    assert summary["line_count"] == 40
    assert summary["line_size"] == 4
    assert summary["lines_per_point"] == 4
    assert summary["laplacian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
    assert summary["kernel_dimension"] == 1
    assert summary["projective_group_order"] == 25920
    assert summary["projective_point_stabilizer_order"] == 648
    assert summary["full_graph_group_order"] == 51840


def test_three_qutrit_and_six_qutrit_layers_match_on_the_729_operator_size() -> None:
    three = three_qutrit_sl27_layer_summary()
    six = six_qutrit_backbone_summary()

    assert three["monster_class"] == "3B"
    assert three["extraspecial_order"] == 3**13
    assert three["heisenberg_irrep_dim"] == 729
    assert three["golay_codeword_count"] == 729
    assert three["golay_nonzero_count"] == 728
    assert three["golay_lagrangian"] is True
    assert three["sl27_hilbert_dim"] == 27
    assert three["sl27_operator_basis_dim"] == 729
    assert three["sl27_traceless_dim"] == 728

    assert six["field_p"] == 3
    assert six["phase_space_dim"] == 12
    assert six["qutrits_n"] == 6
    assert six["heisenberg_irrep_dim"] == 729
    assert six["ord_A"] == 4
    assert six["ord_B"] == 3
    assert six["ord_AB"] == 13
    assert six["invariant_form_nullspace_dim"] == 1
    assert six["invariant_form_rank"] == 12
    assert six["standardized_generators_preserve_J0"] is True


def test_e8_side_exact_decomposition_keeps_the_three_27_generation_orbits() -> None:
    summary = e8_side_exact_decomposition_summary()

    assert summary["dot_pair_class_count"] == 13
    assert summary["total_root_count"] == 240
    assert summary["e6_root_count"] == 72
    assert summary["a2_root_count"] == 6
    assert summary["mixed_root_count"] == 162
    assert summary["edgepair_orbit_sizes"] == (120,)
    assert summary["line_orbit_sizes"] == (36, 27, 27, 27, 1, 1, 1)
    assert summary["matter_lines_per_generation"] == 27
    assert summary["generation_count"] == 3
    assert summary["structure_correct"] is True


def test_ladder_classification_separates_kernel_from_exact_finite_extensions() -> None:
    records = {record["name"]: record for record in classify_qutrit_ladder()}

    assert (
        records["local_one_qutrit_heisenberg_e6_shell"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert (
        records["local_one_qutrit_heisenberg_e6_shell"]["depends_only_on_qutrit_kernel"]
        is True
    )

    assert (
        records["global_two_qutrit_pauli_clifford_kernel"]["support_level"]
        == "repo-exact"
    )
    assert (
        records["global_two_qutrit_pauli_clifford_kernel"][
            "depends_only_on_qutrit_kernel"
        ]
        is True
    )

    assert (
        records["three_qutrit_sl27_closure"]["support_level"]
        == "repo-exact finite extension"
    )
    assert (
        records["three_qutrit_sl27_closure"]["depends_only_on_qutrit_kernel"] is False
    )

    assert (
        records["six_qutrit_sp12_clifford_backbone"]["support_level"]
        == "repo-exact finite extension"
    )
    assert (
        records["six_qutrit_sp12_clifford_backbone"]["depends_only_on_qutrit_kernel"]
        is False
    )

    assert (
        records["e8_side_e6_a2_decomposition"]["support_level"]
        == "exact E8-side decomposition"
    )
    assert (
        records["e8_side_e6_a2_decomposition"]["depends_only_on_qutrit_kernel"] is False
    )


def test_overall_audit_closes_the_exact_ladder_up_to_the_e8_side_boundary() -> None:
    summary = analyze()
    theorem = summary["qutrit_ladder_theorem"]

    assert summary["status"] == "ok"
    assert summary["kernel_record_names"] == (
        "local_one_qutrit_heisenberg_e6_shell",
        "global_two_qutrit_pauli_clifford_kernel",
    )
    assert summary["finite_extension_record_names"] == (
        "three_qutrit_sl27_closure",
        "six_qutrit_sp12_clifford_backbone",
        "e8_side_e6_a2_decomposition",
    )
    assert (
        theorem[
            "the_local_h27_shell_size_matches_the_exact_e8_side_generation_orbit_size"
        ]
        is True
    )
    assert theorem["the_two_qutrit_edge_count_matches_the_exact_e8_root_count"] is True
    assert (
        theorem[
            "the_three_qutrit_operator_basis_matches_the_six_qutrit_heisenberg_irrep"
        ]
        is True
    )
    assert theorem["the_exact_kernel_stops_after_the_first_two_rungs"] is True
    assert (
        theorem[
            "the_later_rungs_are_exact_but_require_additional_finite_input_beyond_the_kernel"
        ]
        is True
    )
    assert (
        theorem["the_exact_qutrit_ladder_is_closed_up_to_the_e8_side_boundary"] is True
    )
    assert "continuum/dynamical lift" in summary["boundary_note"]
