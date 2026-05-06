"""Regression tests for PART CCCXL anchor prediction table compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXL_ANCHOR_PREDICTION_TABLE.py"


def load_module():
    spec = importlib.util.spec_from_file_location("anchor_prediction_cccxl", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_anchor_prediction_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_prediction_formulas_are_positive_and_gap_ratio():
    mod = load_module()
    predictions = mod.predictions_from_kappa(7.0 / 3.0)
    assert abs(predictions["projective_gap_over_mass"] - 2.0) < 1e-12
    assert predictions["heat_trace"] > 0
    assert predictions["spinor_trace"] >= 2
    assert predictions["zeta"] > 0


def test_each_anchor_round_trips_to_same_kappa():
    mod = load_module()
    kappa = 7.0 / 3.0
    tables = mod.make_all_anchor_tables(kappa)
    for table in tables.values():
        assert abs(table["recovered_kappa_from_anchor"] - kappa) < 1e-12
        assert table["round_trip_max_deviation"] < 1e-12


def test_anchor_tables_agree():
    mod = load_module()
    tables = mod.make_all_anchor_tables(7.0 / 3.0)
    comparison = mod.compare_prediction_tables(tables)
    assert comparison["all_tables_agree"] is True
    for diff in comparison["max_prediction_differences"].values():
        assert diff < 1e-10


def test_result_payload_prediction_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["prediction_formulas"]["mass"] == "M_phys=kappa M"
    assert results["prediction_formulas"]["projective_gap"] == "gap_phys=2 M_phys"
    assert results["table_comparison"]["all_tables_agree"] is True
    assert "predictive" in results["architecture_upgrade"]
