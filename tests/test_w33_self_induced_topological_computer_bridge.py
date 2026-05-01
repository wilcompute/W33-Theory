from __future__ import annotations

from pathlib import Path

import pytest
from w33_self_induced_topological_computer_bridge import (
    build_self_induced_topological_computer_summary,
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


def test_self_induced_topological_computer_dictionary_is_exact() -> None:
    summary = build_self_induced_topological_computer_summary()
    data = summary["self_induced_topological_computer_dictionary"]

    processor = data["processor_layer"]
    memory = data["memory_compute_layer"]
    measure = data["measurement_layer"]
    torus = data["toroidal_seed_layer"]
    protection = data["protection_layer"]
    nonlinear = data["nonlinear_frontier_layer"]

    assert processor["two_qutrit_hilbert_dimension"] == 9
    assert processor["projective_pauli_class_count"] == 40
    assert processor["weyl_operator_basis_size"] == 81
    assert processor["projective_clifford_order"] == 25920
    assert processor["full_graph_symmetry_order"] == 51840
    assert processor["neighbor_bus_order"] == 432

    assert memory["projective_screen_size"] == 13
    assert memory["affine_bulk_size"] == 27
    assert memory["affine_direction_count"] == 13
    assert memory["anchor_fiber_count"] == 9
    assert memory["anchor_fiber_size"] == 3

    assert measure["spread_count"] == 36
    assert measure["spread_size"] == 10
    assert measure["sample_memory_lines"] == 1
    assert measure["sample_affine_measurement_lines"] == 9
    assert measure["mub_max_deviation"] < 1e-12

    assert torus["selector_line_dimension"] == 1
    assert torus["shared_six_channel"] == 6
    assert torus["phi6"] == 7
    assert torus["first_closed_torus_genus"] == 1
    assert torus["tetrahedral_directed_packet"] == 12
    assert torus["synthetic_torus_shape"] == (3, 3)
    assert torus["synthetic_torus_cell_count"] == 9

    assert protection["dirac_gap_radicand"] == 10
    assert protection["laplacian_gap"] == 10
    assert protection["yang_mills_gap"] == 100
    assert protection["normalized_gap"] == "5/6"

    assert nonlinear["quartic_magic_atom_count"] == 2
    assert nonlinear["quartic_magic_min_degree"] == 4
    assert nonlinear["h2_galois_group_label"] == "D4"
    assert nonlinear["hbar2_galois_group_label"] == "D4"
    assert nonlinear["root_field_compositum_degree"] == 16
    assert nonlinear["splitting_field_compositum_degree"] == 64


def test_self_induced_topological_computer_theorem_all_hold() -> None:
    summary = build_self_induced_topological_computer_summary()
    assert all(summary["self_induced_topological_computer_theorem"].values())
    assert "device theorem" in summary["boundary_note"]
