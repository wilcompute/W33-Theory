#!/usr/bin/env python3
"""test_effective_y_mass_spectrum_ccccclxxvi.py - Regression tests for CCCCCLXXVI."""

import json
from pathlib import Path
import pytest


@pytest.fixture
def ccccclxxvi_result() -> dict:
    """Load CCCCCLXXVI result JSON."""
    result_file = Path("data/PART_CCCCCLXXVI_effective_y_mass_spectrum_results.json")
    assert result_file.exists(), f"Expected {result_file} to exist"
    with open(result_file, encoding="utf-8") as f:
        return json.load(f)


class TestEffectiveYMassSpectrum:
    """CCCCCLXXVI: Effective Y Mass Spectrum & Coupling Determinant."""

    def test_part_label(self, ccccclxxvi_result: dict) -> None:
        """Verify part label."""
        assert ccccclxxvi_result["part"] == "CCCCCLXXVI"

    def test_all_checks_pass(self, ccccclxxvi_result: dict) -> None:
        """Verify all regression checks pass."""
        assert ccccclxxvi_result["all_checks_pass"] is True

    def test_w33_structure(self, ccccclxxvi_result: dict) -> None:
        """Verify W(3,3) structure."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["points_40"] is True
        assert checks["edges_240"] is True
        assert checks["triangles_160"] is True

    def test_vertex_ytyt_rank_8(self, ccccclxxvi_result: dict) -> None:
        """Verify Y_v†Y_v has rank 8."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["vertex_ytyt_rank_8"] is True

    def test_triangle_ytyt_rank_2(self, ccccclxxvi_result: dict) -> None:
        """Verify Y_τ†Y_τ has rank 2."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["triangle_ytyt_rank_2"] is True

    def test_vertex_eigenvalues_match_svd_squared(self, ccccclxxvi_result: dict) -> None:
        """Verify eigenvalues of Y_v†Y_v equal squared singular values."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["vertex_eigenvalues_match_svd_squared"] is True

    def test_triangle_eigenvalues_match_svd_squared(self, ccccclxxvi_result: dict) -> None:
        """Verify eigenvalues of Y_τ†Y_τ equal squared singular values."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["triangle_eigenvalues_match_svd_squared"] is True

    def test_vertex_determinant_positive(self, ccccclxxvi_result: dict) -> None:
        """Verify det(Y_v†Y_v) > 0."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["vertex_determinant_positive"] is True

    def test_triangle_determinant_positive(self, ccccclxxvi_result: dict) -> None:
        """Verify det(Y_τ†Y_τ) > 0."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["triangle_determinant_positive"] is True

    def test_vertex_condition_number_bounded(self, ccccclxxvi_result: dict) -> None:
        """Verify condition number of Y_v†Y_v is well-behaved."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["vertex_condition_number_bounded"] is True

    def test_triangle_condition_number_bounded(self, ccccclxxvi_result: dict) -> None:
        """Verify condition number of Y_τ†Y_τ is well-behaved."""
        checks = ccccclxxvi_result["spectrum_checks"]
        assert checks["triangle_condition_number_bounded"] is True

    def test_vertex_spectrum_structure(self, ccccclxxvi_result: dict) -> None:
        """Verify vertex spectrum has correct structure."""
        v_spec = ccccclxxvi_result["marked_vertex_y_spectrum"]
        assert v_spec["rank"] == 8
        assert v_spec["nonzero_eigenvalues_count"] == 8

    def test_triangle_spectrum_structure(self, ccccclxxvi_result: dict) -> None:
        """Verify triangle spectrum has correct structure."""
        t_spec = ccccclxxvi_result["marked_triangle_y_spectrum"]
        assert t_spec["rank"] == 2
        assert t_spec["nonzero_eigenvalues_count"] == 2

    def test_coupling_determinant_values(self, ccccclxxvi_result: dict) -> None:
        """Verify determinant values are positive and consistent."""
        det_info = ccccclxxvi_result["coupling_determinant"]
        assert det_info["vertex_determinant_ytyt"] > 0
        assert det_info["triangle_determinant_ytyt"] > 0
        assert det_info["combined_determinant"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
