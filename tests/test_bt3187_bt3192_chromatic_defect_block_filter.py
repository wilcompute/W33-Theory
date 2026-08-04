from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "bt3187_3192_chromatic_defect_block_filter.py"
FROZEN = ROOT / "data" / "PART_BT3187_BT3192_CHROMATIC_DEFECT_BLOCK_FILTER_results.json"
EXPECTED = "555aa1871e40b2d8ed4ea000f0d19ac23ff71a1be10f10eb6f7f9d4b6877cd58"


def load_module():
    spec = importlib.util.spec_from_file_location("bt3187_3192", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_rebuilds_exactly():
    module = load_module()
    rebuilt = module.certificate()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert rebuilt == frozen
    assert rebuilt["sha256_without_hash_field"] == EXPECTED
    assert all(rebuilt["checks"].values())


def test_exact_boundary_and_filters():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert data["status"] == "PASS_EXACT_FILTER_WITHOUT_TEN_COLOR_DECISION"
    assert data["canonical_block_system"]["blocks"] == 45
    assert data["canonical_block_system"]["block_graph"] == "K12 minus 3K4"
    assert data["ten_color_filter"]["trace_upper_bound"] == 216
    assert data["ten_color_filter"]["non_hoffman_squared_mass_upper_bound"] == 36
    assert data["ten_color_filter"]["local_repeat_savings_lower_bound"] == 90
    assert "neither constructs" in data["boundary"]
