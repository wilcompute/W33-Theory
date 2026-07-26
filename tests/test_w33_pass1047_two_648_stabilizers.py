"""Regression test for Pass 1047."""

import importlib.util
from pathlib import Path


def _load_module():
    path = Path(__file__).resolve().parents[1] / "analysis" / "w33_pass1047_two_648_stabilizers.py"
    spec = importlib.util.spec_from_file_location("w33_pass1047", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_two_648_stabilizers_select_point_side():
    result = _load_module().main()
    assert result["status"] == "PASS"
    assert result["point_stabilizer"] == {
        "order": 648,
        "center_order": 3,
        "derived_order": 216,
        "abelianization_order": 3,
    }
    assert result["line_stabilizer"] == {
        "order": 648,
        "center_order": 1,
        "derived_order": 324,
        "abelianization_order": 2,
    }
    assert all(result["checks"].values())
