"""Regression tests for PART CCCCV protected W33/H1/E8 TOE kernel."""

from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCV_PROTECTED_TOE_KERNEL.py"
RESULTS_PATH = ROOT / "PART_CCCCV_protected_toe_kernel_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("protected_toe_kernel_ccccv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_kernel_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 17
    assert all(check["passed"] for check in results["checks"])


def test_kernel_stack_names_every_required_layer():
    stack = build_results()["kernel_stack"]
    assert len(stack) == 6
    assert "40 points, 240 edges" in stack[0]
    assert "H1(W33;Z)=Z^81" in stack[2]
    assert "E8 operation gate" in stack[3]
    assert "[[240,81,3]]" in stack[4]
    assert "[[82320,81,>=81]]" in stack[5]


def test_closure_equalities_hit_w33_h1_and_e8_scales():
    equalities = build_results()["closure_equalities"]
    assert equalities["logical_sector"] == 81
    assert equalities["protected_distance_lower_bound"] == 81
    assert equalities["correctable_weight"] == 40
    assert equalities["w33_vertices"] == 40
    assert equalities["steane_length"] == 7
    assert equalities["e8_z3_terms_checked"] == 8347


def test_theorem_and_boundary_are_bounded():
    results = build_results()
    assert "verified protected information stack" in results["theorem"]
    assert "[[82320,81,>=81]]" in results["theorem"]
    assert "solved finite protected information kernel" in results["honesty_boundary"]
    assert "does not claim" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    import json

    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCV"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["closure_equalities"] == live["closure_equalities"]


def test_docs_index_exposes_protected_kernel():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Protected W33/H1/E8 TOE Kernel" in text
    assert "PART_CCCCV_PROTECTED_TOE_KERNEL.md" in text
    assert "H1=Z^81" in text
    assert "8347" in text
    assert "[[82320,81,&ge;81]]" in text
