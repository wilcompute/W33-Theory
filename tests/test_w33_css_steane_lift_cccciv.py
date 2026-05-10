"""Regression tests for PART CCCCIV W33 CSS Steane-lift protection stack."""

from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCIV_W33_CSS_STEANE_LIFT.py"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("w33_css_steane_lift_cccciv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 15


def test_base_and_inner_codes():
    results = build_results()
    assert results["base_code"] == {"notation": "[[240,81,3]]", "n": 240, "k": 81, "d": 3}
    inner = results["inner_code"]
    assert inner["notation"] == "[[7,1,3]]"
    assert inner["n"] == 7
    assert inner["k"] == 1
    assert inner["d"] == 3
    assert "7 = Phi6" in inner["w33_read"]


def test_lift_table_closes_on_w33_scales():
    table = build_results()["lift_table"]
    assert [row["n"] for row in table] == [240, 1680, 11760, 82320]
    assert [row["distance_lower_bound"] for row in table] == [3, 9, 27, 81]
    assert [row["k"] for row in table] == [81, 81, 81, 81]
    assert table[1]["correctable_weight"] == 4
    assert table[3]["correctable_weight"] == 40


def test_three_lift_fault_tolerance_read():
    ft = build_results()["fault_tolerance_read"]
    assert ft["three_lift_code"] == "[[82320,81,>=81]]"
    assert ft["guaranteed_correctable_weight"] == 40
    assert ft["logical_sector_count"] == 81
    assert "H1 matter rank" in ft["interpretation"]


def test_formula_helpers():
    mod = load_module()
    assert mod.PHI6 == 7
    assert mod.correctable_errors(81) == 40
    assert mod.lift_level(3).n == 240 * 7**3
    assert mod.lift_level(3).distance_lower_bound == 3**4


def test_docs_index_exposes_steane_lift():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "W33 CSS Steane-Lift" in text
    assert "[[82320,81,&ge;81]]" in text
    assert "correctable weight" in text
