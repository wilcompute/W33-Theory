"""Regression tests for upstream PART CCCCIV W33 CSS distance amplification."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCIV_W33_DISTANCE_AMPLIFICATION.py"
RESULTS_PATH = ROOT / "PART_CCCCIV_w33_distance_amplification_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("w33_distance_amplification_cccciv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def steane_level(candidates, level):
    tower = candidates.get("steane_css_tower")
    if tower is not None:
        return tower[str(level)]
    return candidates[f"steane_css_level_{level}"]


def test_all_distance_amplification_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 8
    assert all(check["passed"] for check in results["checks"])


def test_one_level_candidates_are_recorded():
    candidates = build_results()["exact_amplification_candidates"]
    steane1 = steane_level(candidates, 1)
    assert steane1["css"] is True
    assert steane1["n"] == 1680
    assert steane1["k"] == 81
    assert steane1["d"] == 9
    assert candidates["shor_css_level_1"]["n"] == 2160
    assert candidates["shor_css_level_1"]["d"] == 9
    assert candidates["five_qubit_non_css_level_1"]["n"] == 1200
    assert candidates["five_qubit_non_css_level_1"]["css"] is False


def test_steane_tower_matches_local_three_lift_scales():
    candidates = build_results()["exact_amplification_candidates"]
    assert steane_level(candidates, 1)["n"] == 1680
    assert steane_level(candidates, 1)["d"] == 9
    assert steane_level(candidates, 2)["n"] == 11760
    assert steane_level(candidates, 2)["d"] == 27
    assert steane_level(candidates, 3)["n"] == 82320
    assert steane_level(candidates, 3)["d"] == 81
    if candidates.get("steane_css_tower") is not None:
        assert steane_level(candidates, 4)["n"] == 576240
        assert steane_level(candidates, 4)["d"] == 243


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCIV"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert steane_level(artifact["exact_amplification_candidates"], 3)["n"] == 82320
    assert steane_level(artifact["exact_amplification_candidates"], 3)["d"] == 81
