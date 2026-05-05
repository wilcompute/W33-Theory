"""Regression tests for PART CCCXXVI finite Euler variation compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXVI_FINITE_EULER_VARIATION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_euler_cccxxvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_finite_euler_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 14


def test_log_derivative_collapses_to_euler_quadratic():
    mod = load_module()
    factor, a, b, c = mod.log_derivative_numerator_coefficients()
    assert factor == -8
    assert (a, b, c) == (140, 67, -1)
    results = mod.build_results()
    assert results["finite_euler_polynomial"]["equation"] == "140x^2 + 67x - 1 = 0"


def test_euler_coefficients_have_w33_forms():
    mod = load_module()
    results = mod.build_results()
    poly = results["finite_euler_polynomial"]
    assert poly["A"] == 140
    assert poly["B"] == 67
    assert poly["C"] == -1
    assert poly["A_form"] == "(v/2) Phi6"
    assert poly["B_form"] == "2v - Phi3"
    assert poly["discriminant"] == 5049
    assert poly["discriminant_form"] == "q^3 (k-1) (Phi4 + Phi6)"


def test_root_sum_and_product():
    mod = load_module()
    assert Fraction(-mod.B, mod.A) == Fraction(-67, 140)
    assert Fraction(mod.C, mod.A) == Fraction(-1, 140)


def test_positive_inverse_scale_near_69():
    mod = load_module()
    root_data = mod.roots()
    assert 69.0 < root_data["inverse_x_plus_decimal"] < 69.1
    assert -2.1 < root_data["inverse_x_minus_decimal"] < -2.0
    assert root_data["inverse_scales_exact"] == ["(67 + sqrt(5049))/2", "(67 - sqrt(5049))/2"]
