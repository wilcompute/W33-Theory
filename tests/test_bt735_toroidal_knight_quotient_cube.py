"""Regression tests for BT735/BT738 toroidal knight quotient cube verifier."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "bt735_toroidal_knight_quotient_cube.py"


def load_module():
    spec = importlib.util.spec_from_file_location("bt735_toroidal_knight_quotient_cube", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_all_quotient_cube_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 10


def test_projected_support_is_q3():
    mod = load_module()
    support = set(mod.projected_walk_edges())
    assert len(support) == 12
    assert mod.is_q3_support(support)


def test_missing_matching_is_perfect():
    mod = load_module()
    missing = mod.missing_edges()
    assert len(missing) == 4
    degrees = mod.degree_profile(missing)
    assert len(degrees) == 8
    assert set(degrees.values()) == {1}


def test_quotient_axis_sequence_visits_all_axes_twice_by_halves():
    mod = load_module()
    seq = mod.axis_sequence()
    assert len(seq) == 16
    assert len(set(seq)) == 8
    assert len(set(seq[:8])) == 8
    assert len(set(seq[8:])) == 8


def test_projected_trace_boundary_statement():
    mod = load_module()
    results = mod.build_results()
    assert "K4,4 minus a perfect matching" in results["theorem"]
    assert "rank-81 selector" in results["honesty_boundary"]
