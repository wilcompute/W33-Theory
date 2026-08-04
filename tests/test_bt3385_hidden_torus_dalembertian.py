from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "analysis/bt3385_hidden_torus_dalembertian.py"
    spec = importlib.util.spec_from_file_location("bt3385_dalembertian", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hidden_torus_dalembertian_matches_frozen_certificate():
    observed = load_module().build_certificate()
    frozen = json.loads(
        (ROOT / "data/PART_BT3385_HIDDEN_TORUS_DALEMBERTIAN_results.json").read_text(encoding="utf-8")
    )
    assert observed == frozen
    assert observed["status"] == "PASS"
    assert all(observed["checks"].values())


def test_null_set_is_one_plus_four_plus_four():
    result = load_module().build_certificate()
    null_set = result["fourier_null_set"]
    assert len(null_set["constant"]) == 1
    assert len(null_set["first_ruling"]) == 4
    assert len(null_set["second_ruling"]) == 4
    assert result["rank"] == 18
    assert result["nullity"] == 9
    assert result["spectrum"] == {"-3": 2, "0": 9, "3": 12, "6": 4}
