"""Regression tests for PART CCCXXIX integrated finite RG flow compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXIX_INTEGRATED_RG_FLOW.py"


def load_module():
    spec = importlib.util.spec_from_file_location("integrated_rg_cccxxix", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_integrated_flow_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 13


def test_cross_ratio_linearizes_flow():
    mod = load_module()
    y0 = float(mod.B)
    y_forward = mod.integrated_flow(y0, 0.1)
    tau0 = mod.rg_time_coordinate(y0)
    tau_forward = mod.rg_time_coordinate(y_forward)
    assert abs((tau_forward - tau0) - 0.1) < 1e-10


def test_integrated_solution_limits():
    mod = load_module()
    y0 = float(mod.B)
    assert abs(mod.integrated_flow(y0, 1.0) - mod.Y_PLUS) < 1e-12
    assert abs(mod.integrated_flow(y0, -1.0) - mod.Y_MINUS) < 1e-12


def test_derivative_matches_beta():
    mod = load_module()
    y0 = float(mod.B)
    dy_dt = mod.flow_derivative_numeric(y0, 0.0)
    assert abs(dy_dt - mod.beta(y0)) < 1e-4


def test_result_payload_has_integrated_formula():
    mod = load_module()
    results = mod.build_results()
    assert results["beta_flow"] == "dy/dt = 67y + 140 - y^2 = -(y-y_+)(y-y_-)"
    assert results["linearizing_coordinate"]["R(y)"] == "(y-y_-)/(y_+-y)"
    assert "exp(sqrt(5049)t)" in results["integrated_solution"]["formula"]
