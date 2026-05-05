"""Regression tests for PART CCCXXV canonical action kernel compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXV_CANONICAL_ACTION_KERNEL.py"


def load_module():
    spec = importlib.util.spec_from_file_location("canonical_action_cccxxv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_canonical_action_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 15


def test_unique_sector_solution():
    mod = load_module()
    assert mod.find_sector_dimension_solutions() == [(10, 16, 6)]
    results = mod.build_results()
    assert tuple(results["unique_solution"]["sector_dimensions"]) == (10, 16, 6)
    assert results["unique_solution"]["closed_forms"] == ["Phi4", "(q+1)^2", "2q"]


def test_action_constraints_are_exact():
    mod = load_module()
    results = mod.build_results()
    constraints = results["constraints"]
    assert tuple(constraints["couplings"]) == (5, -1, -7)
    assert constraints["dimension_sum"] == 32
    assert constraints["dimension_product"] == 960
    assert constraints["signed_first_moment"] == -8


def test_moment_package():
    mod = load_module()
    results = mod.build_results()
    moments = results["moments"]
    assert moments["sector_sum"] == 32
    assert moments["sector_product"] == 960
    assert moments["signed_first_moment"] == -8
    assert moments["second_moment"] == 560
    assert moments["Z(1)"] == "2^54"


def test_determinant_is_forced_form():
    mod = load_module()
    results = mod.build_results()
    assert results["determinant"] == "(1-5x)^10(1+x)^16(1+7x)^6"
    assert "unique positive-integer three-sector action kernel" in results["theorem"]
