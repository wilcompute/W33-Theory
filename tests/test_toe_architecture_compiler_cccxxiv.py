"""Regression tests for PART CCCXXIV TOE architecture compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXIV_TOE_ARCHITECTURE_COMPILER.py"


def load_module():
    spec = importlib.util.spec_from_file_location("toe_architecture_cccxxiv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_architecture_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 40


def test_photon_resource_hashimoto_identity():
    mod = load_module()
    results = mod.build_results()
    assert results["probabilities"]["p_fusion"] == "1/2"
    assert results["resource_counts"]["edges"] == 240
    assert results["resource_counts"]["expected_type_ii_fusion_attempts"] == 480
    assert results["constants"]["directed_hashimoto"] == 480


def test_critical_fusion_seidel_split_and_stabilizer_transition():
    mod = load_module()
    results = mod.build_results()
    resources = results["resource_counts"]
    assert resources["critical_retained_edges"] == 120
    assert resources["critical_complement_edges"] == 120
    assert resources["full_stabilizer_weight"] == results["constants"]["Phi3"] == 13
    assert resources["critical_stabilizer_weight"] == results["constants"]["Phi6"] == 7


def test_clifford_compiler_orbit_factors():
    mod = load_module()
    results = mod.build_results()
    assert results["orbit_factors"]["per_vertex"] == 1296
    assert results["orbit_factors"]["per_edge"] == 216
    assert results["orbit_factors"]["per_directed_hashimoto_state"] == 108
    assert results["orbit_factors"]["per_triangle_trace_unit"] == 54
    assert results["orbit_factors"]["per_triangle"] == 324


def test_determinant_compresses_triangle_trace():
    mod = load_module()
    results = mod.build_results()
    determinant = results["determinant"]
    assert determinant["Z(x)"] == "(1-5x)^10(1+x)^16(1+7x)^6"
    assert tuple(determinant["coefficients"]) == (5, -1, -7)
    assert tuple(determinant["exponents"]) == (10, 16, 6)
    assert determinant["exponent_product"] == results["constants"]["triangle_trace"] == 960
    assert determinant["signed_first_moment"] == -8
    assert determinant["second_moment"] == 560
    assert determinant["Z(1)"] == "2^54"


def test_rg_renderer_boundary_forms():
    mod = load_module()
    results = mod.build_results()
    assert results["rg_boundary"]["sin2_theta_W_MGUT"] == "3/8"
    assert tuple(results["rg_boundary"]["MSSM_beta"]) == ("33/5", "1", "-3")
    assert tuple(results["rg_boundary"]["SM_beta"]) == ("41/10", "-19/6", "-7")
