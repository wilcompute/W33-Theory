from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from w33_qutrit_syndrome_circuits import audit as circuit_audit
from w33_surface_refinement_limit import (
    audit as refinement_audit,
    matrices,
    physical_matrices,
    refine,
)


def test_refinement_contract_and_checked_certificate():
    for invalid in (-1, 1.5, True, "4"):
        with pytest.raises(ValueError):
            refinement_audit(invalid)

    level_zero = refinement_audit(0)
    assert [row["level"] for row in level_zero["rows"]] == [0]
    assert level_zero["eigenvalue_count_per_level"] == 12

    actual = refinement_audit(4)
    stored = json.loads(
        (ROOT / "analysis/w33_surface_refinement_limit.json").read_text()
    )
    assert actual.keys() == stored.keys()
    for key in actual.keys() - {"rows"}:
        assert actual[key] == stored[key]
    assert len(actual["rows"]) == len(stored["rows"]) == 5

    integer_fields = ("level", "vertices", "edges", "faces")
    float_fields = (
        "triangle_side_length",
        "physical_area",
        "consistent_mass_total",
        "raw_graph_laplacian_gap",
        "max_generalized_eigenpair_relative_residual",
    )
    optional_error_fields = (
        "integer_stiffness_galerkin_max_abs_error",
        "integer_mass_galerkin_max_abs_error",
        "physical_stiffness_galerkin_max_abs_error",
        "physical_mass_galerkin_max_abs_error",
    )
    for actual_row, stored_row in zip(actual["rows"], stored["rows"]):
        assert actual_row.keys() == stored_row.keys()
        for key in integer_fields:
            assert actual_row[key] == stored_row[key]
        for key in float_fields:
            np.testing.assert_allclose(actual_row[key], stored_row[key], atol=1e-10)
        np.testing.assert_allclose(
            actual_row["cone_laplacian_ritz_eigenvalues"],
            stored_row["cone_laplacian_ritz_eigenvalues"],
            atol=1e-8,
        )
        np.testing.assert_allclose(
            actual_row["raw_graph_laplacian_eigenvalues"],
            stored_row["raw_graph_laplacian_eigenvalues"],
            atol=1e-10,
        )
        assert len(actual_row["cone_laplacian_ritz_eigenvalues"]) == 12
        assert len(actual_row["raw_graph_laplacian_eigenvalues"]) == 2
        assert actual_row["has_coarse_galerkin_inclusion"] == (
            actual_row["level"] > 0
        )
        for key in optional_error_fields:
            if actual_row["level"] == 0:
                assert actual_row[key] is None and stored_row[key] is None
            else:
                np.testing.assert_allclose(actual_row[key], stored_row[key], atol=1e-12)

    first_positive = [
        row["cone_laplacian_ritz_eigenvalues"][1] for row in actual["rows"]
    ]
    assert all(b <= a + 1e-7 for a, b in zip(first_positive, first_positive[1:]))
    raw_gaps = [row["raw_graph_laplacian_gap"] for row in actual["rows"]]
    assert raw_gaps[-1] < raw_gaps[0] / 100


def test_integer_and_physical_galerkin_identities():
    coarse_faces = [(0, 1, 2)]
    coarse_s, coarse_b = matrices(coarse_faces, 3)
    fine_faces, fine_vertex_count, doubled_prolongation = refine(coarse_faces, 3)
    fine_s, fine_b = matrices(fine_faces, fine_vertex_count)

    assert not np.any(
        (doubled_prolongation.T @ fine_s @ doubled_prolongation - 4 * coarse_s).data
    )
    assert not np.any(
        (doubled_prolongation.T @ fine_b @ doubled_prolongation - 16 * coarse_b).data
    )

    coarse_k, coarse_m = physical_matrices(coarse_s, coarse_b, 1.0)
    fine_k, fine_m = physical_matrices(fine_s, fine_b, 0.5)
    prolongation = doubled_prolongation.astype(float) * 0.5
    np.testing.assert_allclose(
        (prolongation.T @ fine_k @ prolongation).toarray(),
        coarse_k.toarray(),
        atol=1e-14,
    )
    np.testing.assert_allclose(
        (prolongation.T @ fine_m @ prolongation).toarray(),
        coarse_m.toarray(),
        atol=1e-14,
    )
    expected_area = np.sqrt(3.0) / 4.0
    np.testing.assert_allclose(np.ones(3) @ coarse_m @ np.ones(3), expected_area)
    np.testing.assert_allclose(
        np.ones(fine_vertex_count) @ fine_m @ np.ones(fine_vertex_count),
        expected_area,
    )


def test_executable_syndromes_and_complete_bare_hook_census():
    actual = circuit_audit()
    stored = json.loads(
        (ROOT / "analysis/w33_qutrit_syndrome_circuits.json").read_text()
    )
    assert actual.keys() == stored.keys()
    for key in actual.keys() - {
        "max_probability_error",
        "maximum_postmeasurement_infidelity",
    }:
        assert actual[key] == stored[key]
    np.testing.assert_allclose(
        actual["max_probability_error"], stored["max_probability_error"], atol=1e-14
    )
    np.testing.assert_allclose(
        actual["maximum_postmeasurement_infidelity"],
        stored["maximum_postmeasurement_infidelity"],
        atol=1e-14,
    )

    assert actual["measurement_checks"] == 584
    assert actual["logical_basis_postmeasurement_checks"] == 24
    assert actual["explicit_sign_checks"] == {
        "Z0_Z1inv_against_X0": 1,
        "weight6_X_against_Z0": 2,
    }
    assert actual["two_qutrit_gates_per_block_round"] == 24
    assert actual["six_handle_gates_per_round"] == 144
    assert actual["bare_ancilla_x_fault_cases"] == 64
    assert len(actual["bare_ancilla_x_malignant_cases"]) == 12
    assert len(actual["bare_ancilla_x_undetected_logical_cases"]) == 4
    assert actual["conditional_cat_single_site_cases"] == 48

    malignant_boundaries = {
        (row["stabilizer"], row["completed_couplings"])
        for row in actual["bare_ancilla_x_malignant_cases"]
    }
    assert malignant_boundaries == {
        (6, 2),
        (6, 3),
        (6, 4),
        (7, 2),
        (7, 3),
        (7, 4),
    }
    undetected_boundaries = {
        (row["stabilizer"], row["completed_couplings"])
        for row in actual["bare_ancilla_x_undetected_logical_cases"]
    }
    assert undetected_boundaries == {(6, 3), (7, 3)}

