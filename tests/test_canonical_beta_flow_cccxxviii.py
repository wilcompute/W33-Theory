"""Regression tests for PART CCCXXVIII canonical beta flow compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXVIII_CANONICAL_BETA_FLOW.py"


def load_module():
    spec = importlib.util.spec_from_file_location("canonical_beta_cccxxviii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_beta_flow_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 17


def test_beta_flow_equations():
    mod = load_module()
    results = mod.build_results()
    assert results["inverse_scale_equation"] == "y^2 - 67y - 140 = 0"
    assert results["fixed_point_law"] == "F(y)=67+140/y"
    assert results["rational_beta"] == "beta(y)=F(y)-y=67+140/y-y"
    assert results["polynomial_beta_numerator"] == "B(y)=y beta(y)=67y+140-y^2"


def test_fixed_points_and_derivatives():
    mod = load_module()
    results = mod.build_results()
    fixed = results["fixed_points"]
    derivs = results["branch_derivatives"]
    assert fixed["y_plus_exact"] == "(67+sqrt(5049))/2"
    assert fixed["y_minus_exact"] == "(67-sqrt(5049))/2"
    assert abs(fixed["sum"] - 67) < 1e-12
    assert abs(fixed["product"] + 140) < 1e-9
    assert abs(derivs["beta_prime_y_plus"] + derivs["sqrt_discriminant"]) < 1e-12
    assert abs(derivs["beta_prime_y_minus"] - derivs["sqrt_discriminant"]) < 1e-12


def test_branch_classification():
    mod = load_module()
    results = mod.build_results()
    classification = results["branch_classification"]
    assert classification["below_y_minus"] == "decreasing-scale"
    assert classification["between_roots"] == "increasing-scale"
    assert classification["above_y_plus"] == "decreasing-scale"
    assert "attracting" in classification["positive_fixed_point"]
    assert "repelling" in classification["negative_fixed_point"]


def test_sample_flow_grid_signs():
    mod = load_module()
    results = mod.build_results()
    grid = {entry["y"]: entry["class"] for entry in results["sample_flow_grid"]}
    assert grid[-10] == "decreasing-scale"
    assert grid[10] == "increasing-scale"
    assert grid[80] == "decreasing-scale"
    assert grid[140] == "decreasing-scale"
