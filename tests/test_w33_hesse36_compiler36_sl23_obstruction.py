from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_compiler36_sl23_obstruction.py"
DATA = ROOT / "data/w33_hesse36_compiler36_sl23_obstruction.json"


def load():
    spec = importlib.util.spec_from_file_location("hesse36_compiler36", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_character_obstruction_is_only_order_three():
    out = json.loads(DATA.read_text())
    assert out["common_group"]["order"] == 24
    assert out["carriers"]["ordinary36"]["orbit_sizes_under_common_SL23"] == [4, 4, 4, 24]
    assert out["carriers"]["compiler_safe36"]["orbit_sizes_under_common_SL23"] == [4, 4, 4, 8, 8, 8]
    assert out["obstruction"]["mismatch_element_orders"] == [3]
    assert out["obstruction"]["order3_class_size"] == 8
    assert out["obstruction"]["order3_fixed_points_ordinary36"] == 3
    assert out["obstruction"]["order3_fixed_points_compiler_safe36"] == 9
    assert out["obstruction"]["equivariant_bijection_exists"] is False
