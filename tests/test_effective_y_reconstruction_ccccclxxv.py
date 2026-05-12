#!/usr/bin/env python3
"""
test_effective_y_reconstruction_ccccclxxv.py

Regression test suite for PART_CCCCCLXXV: Effective Y Reconstruction.

This suite verifies:
  1. Correct reconstruction of marked-vertex Y_v in V_39 + H_81 basis
  2. Correct reconstruction of marked-triangle Y_τ in V_39 + H_81 basis
  3. Preservation of S_2, S_4 singular value sums
  4. Rank preservation (rank 8 for Y_v, rank 2 for Y_τ)
  5. Machine-epsilon reconstruction errors
  6. Basis dimension correctness (39 vertex-gradient, 81 cohomology)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def ccccclxxv_result() -> dict:
    """Load CCCCCLXXV result JSON."""
    result_file = Path("data/PART_CCCCCLXXV_effective_y_reconstruction_results.json")
    assert result_file.exists(), f"Expected {result_file} to exist"
    with open(result_file, encoding="utf-8") as f:
        return json.load(f)


class TestEffectiveYReconstruction:
    """CCCCCLXXV: Effective Y Reconstruction from V_39 + H_81."""

    def test_part_label(self, ccccclxxv_result: dict) -> None:
        """Verify part label."""
        assert ccccclxxv_result["part"] == "CCCCCLXXV"

    def test_all_checks_pass(self, ccccclxxv_result: dict) -> None:
        """Verify all regression checks pass."""
        assert ccccclxxv_result["all_checks_pass"] is True

    def test_w33_structure(self, ccccclxxv_result: dict) -> None:
        """Verify W(3,3) structure: 40 points, 240 edges, 160 triangles, 40 K4 lines."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["points_40"] is True
        assert checks["edges_240"] is True
        assert checks["triangles_160"] is True
        assert checks["k4_lines_40"] is True

    def test_basis_dimensions(self, ccccclxxv_result: dict) -> None:
        """Verify basis dimensions: V_39 rank 39, H_81 rank 81."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["basis_v39_rank"] is True
        assert checks["basis_h81_rank"] is True

    def test_decomposition_structure(self, ccccclxxv_result: dict) -> None:
        """Verify decomposition: V_39 ⊕ H_81 = 120 active modes."""
        decomp = ccccclxxv_result["decomposition"]
        assert decomp["vertex_gradient_dimension"] == 39
        assert decomp["cohomology_dimension"] == 81
        assert decomp["active_dimension"] == 120
        assert decomp["k4_line_sums_dimension"] == 40

    def test_vertex_y_rank(self, ccccclxxv_result: dict) -> None:
        """Verify marked-vertex Y_v has rank 8."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["vertex_y_rank_8"] is True

    def test_vertex_y_s2_exact(self, ccccclxxv_result: dict) -> None:
        """Verify marked-vertex Y_v has S_2 = 81/80."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["vertex_y_S2_exact"] is True

    def test_vertex_y_s4_exact(self, ccccclxxv_result: dict) -> None:
        """Verify marked-vertex Y_v has S_4 = 6561/51200."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["vertex_y_S4_exact"] is True

    def test_triangle_y_rank(self, ccccclxxv_result: dict) -> None:
        """Verify marked-triangle Y_τ has rank 2."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["triangle_y_rank_2"] is True

    def test_triangle_y_s2_exact(self, ccccclxxv_result: dict) -> None:
        """Verify marked-triangle Y_τ has S_2 = 81/320."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["triangle_y_S2_exact"] is True

    def test_triangle_y_s4_exact(self, ccccclxxv_result: dict) -> None:
        """Verify marked-triangle Y_τ has S_4 = 6561/204800."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["triangle_y_S4_exact"] is True

    def test_vertex_decomp_error_tiny(self, ccccclxxv_result: dict) -> None:
        """Verify vertex Y_v reconstruction error < 1e-8."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["vertex_decomp_error_tiny"] is True

    def test_triangle_decomp_error_tiny(self, ccccclxxv_result: dict) -> None:
        """Verify triangle Y_τ reconstruction error < 1e-8."""
        checks = ccccclxxv_result["reconstruction_checks"]
        assert checks["triangle_decomp_error_tiny"] is True

    def test_vertex_y_decomposition_structure(self, ccccclxxv_result: dict) -> None:
        """Verify marked-vertex Y_v decomposition has 39 + 81 = 120 coefficients."""
        v_decomp = ccccclxxv_result["marked_vertex_y_decomposition"]
        assert v_decomp["basis_39_coeffs_count"] == 39
        assert v_decomp["basis_81_coeffs_count"] == 81
        assert v_decomp["rank"] == 8
        assert v_decomp["S2_exact"] == "81/80"
        assert v_decomp["S4_exact"] == "6561/51200"

    def test_triangle_y_decomposition_structure(self, ccccclxxv_result: dict) -> None:
        """Verify marked-triangle Y_τ decomposition has 39 + 81 = 120 coefficients."""
        t_decomp = ccccclxxv_result["marked_triangle_y_decomposition"]
        assert t_decomp["basis_39_coeffs_count"] == 39
        assert t_decomp["basis_81_coeffs_count"] == 81
        assert t_decomp["rank"] == 2
        assert t_decomp["S2_exact"] == "81/320"
        assert t_decomp["S4_exact"] == "6561/204800"

    def test_vertex_decomp_relative_error_bound(self, ccccclxxv_result: dict) -> None:
        """Verify vertex Y_v reconstruction relative error < 1e-7."""
        v_decomp = ccccclxxv_result["marked_vertex_y_decomposition"]
        assert v_decomp["reconstruction_error"] < 1e-7

    def test_triangle_decomp_relative_error_bound(self, ccccclxxv_result: dict) -> None:
        """Verify triangle Y_τ reconstruction relative error < 1e-7."""
        t_decomp = ccccclxxv_result["marked_triangle_y_decomposition"]
        assert t_decomp["reconstruction_error"] < 1e-7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
