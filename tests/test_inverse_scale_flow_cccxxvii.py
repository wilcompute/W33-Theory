"""Regression tests for PART CCCXXVII inverse scale flow compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXVII_INVERSE_SCALE_FLOW.py"


def load_module():
    spec = importlib.util.spec_from_file_location("inverse_scale_cccxxvii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_inverse_scale_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 13


def test_inverse_scale_equation_and_coefficients():
    mod = load_module()
    results = mod.build_results()
    assert results["inverse_scale_equation"] == "y^2 - 67y - 140 = 0"
    assert results["fixed_point_law"] == "y = 67 + 140/y"
    assert results["coefficients"]["B"] == 67
    assert results["coefficients"]["A"] == 140
    assert results["coefficients"]["discriminant"] == 5049


def test_roots_and_stability():
    mod = load_module()
    results = mod.build_results()
    roots = results["roots"]
    assert roots["y_plus_exact"] == "(67 + sqrt(5049))/2"
    assert roots["y_minus_exact"] == "(67 - sqrt(5049))/2"
    assert 69.0 < roots["y_plus_decimal"] < 69.1
    assert -2.1 < roots["y_minus_decimal"] < -2.0
    stability = results["stability"]
    assert stability["positive_branch"] == "attracting"
    assert stability["negative_branch"] == "repelling"
    assert stability["positive_derivative_magnitude"] < 1
    assert stability["negative_derivative_magnitude"] > 1


def test_fixed_point_iteration_converges_from_B():
    mod = load_module()
    results = mod.build_results()
    flow = results["iteration_from_B"]
    y_plus = results["roots"]["y_plus_decimal"]
    assert flow[0] == 67.0
    assert abs(flow[-1] - y_plus) < 1e-8


def test_continued_fraction_signal():
    mod = load_module()
    results = mod.build_results()
    cf = results["continued_fraction_y_plus"]
    assert cf[0] == 69
    for item in [17, 3, 8, 7]:
        assert item in cf
