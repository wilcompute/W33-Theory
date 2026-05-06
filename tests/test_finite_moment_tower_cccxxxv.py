"""Regression tests for PART CCCXXXV finite spectral moment tower compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXV_FINITE_MOMENT_TOWER.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_moment_tower_cccxxxv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_finite_moment_tower_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 13


def test_trace_power_parity_law():
    mod = load_module()
    assert mod.trace_power(0) == 2
    for n in [1, 3, 5, 7]:
        assert mod.trace_power(n) == 0
    assert mod.trace_power(2) == Fraction(5049, 2)
    assert mod.trace_power(4) == Fraction(2, 1) * mod.M2 * mod.M2


def test_expansion_coefficients():
    mod = load_module()
    res = mod.resolvent_large_s_coefficients(1)
    spin = mod.spinor_trace_coefficients(1)
    heat = mod.kg_heat_coefficients(1)
    logdet = mod.logdet_large_s_coefficients(1)
    assert res[0]["coefficient"] == "2"
    assert res[1]["coefficient"] == "5049/2"
    assert spin[1]["coefficient"] == "5049/4"
    assert heat[1]["coefficient"] == "-5049/2"
    assert logdet[0]["coefficient_after_2log_s"] == "-5049/4"


def test_resolvent_series_remainder():
    mod = load_module()
    s = Fraction(100, 1)
    exact = mod.evaluate_resolvent_trace_exact(s)
    partial = mod.evaluate_resolvent_trace_series(s, 4)
    remainder = exact - partial
    assert remainder > 0
    assert abs(float(remainder)) < 1e-12


def test_result_payload_moment_tower():
    mod = load_module()
    results = mod.build_results()
    assert results["mass_shell"]["m_squared"] == "5049/4"
    assert results["moment_table_n0_to_n8"][1]["trace_G_power_n"] == "0"
    assert results["expansions"]["logdet_large_s"]["formula"].startswith("log det")
    assert "moment tower" in results["architecture_upgrade"]
