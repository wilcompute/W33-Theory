"""Focused regression for Passes 3663-3669."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3663_3669_monster_chamber_spread_bridge.py"
FROZEN = ROOT / "data" / "PART_3663_3669_MONSTER_CHAMBER_SPREAD_BRIDGE_results.json"
EXPECTED_SHA = "ea0d3d989c05d51dc1e60de05cb9fe9f3308d8c36f1e40749b915f7bc0aaefca"


def load_verifier():
    spec = importlib.util.spec_from_file_location("w33_pass3663_3669", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_chamber_spread_bridge() -> None:
    module = load_verifier()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))

    assert all(module.checks.values())
    assert module.result["semantic_sha256"] == EXPECTED_SHA
    assert frozen == module.result

    bridge = frozen["canonical_bijection"]
    assert bridge["normalizer_equals_stabilizer"]
    assert bridge["derived_subgroup_is_a6"]
    assert bridge["fixed_spreads"] == 1
    assert bridge["image_size"] == 36

    dictionary = frozen["intersection_dictionary"]
    assert dictionary["A6_intersection_18__spread_intersection_1"] == 360
    assert dictionary["A6_intersection_12__spread_intersection_4"] == 270
    assert dictionary["order12_relation"]["srg"] == [36, 15, 6, 6]
    assert dictionary["order18_relation"]["srg"] == [36, 20, 10, 12]


def test_exceptional_s6_double_six() -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    double_six = frozen["exceptional_s6_double_six"]

    assert double_six["a5_orbits_in_chamber"] == [6, 6]
    assert double_six["cross_intersection_graph"] == "K6,6"
    assert double_six["both_degree6_actions_faithful"]

    census = double_six["cycle_type_pair_census"]
    assert census["2.1.1.1.1 -> 2.2.2"] == 15
    assert census["3.1.1.1 -> 3.3"] == 40
    assert census["6 -> 3.2.1"] == 120
