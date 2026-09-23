from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_q8_equivariant_repair.py"
DATA = ROOT / "data/w33_hesse36_q8_equivariant_repair.json"


def load():
    spec = importlib.util.spec_from_file_location("hesse36_q8_repair", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_q8_repair_and_gauge_count():
    out = json.loads(DATA.read_text())
    assert out["group"]["repair_subgroup"] == "Q8"
    assert out["group"]["order"] == 8
    assert out["group"]["element_order_profile"] == {"1": 1, "2": 1, "4": 6}
    assert out["orbit_structure"]["ordinary36"] == [4, 4, 4, 8, 8, 8]
    assert out["orbit_structure"]["compiler_safe36"] == [4, 4, 4, 8, 8, 8]
    mapping = out["explicit_bijection"]["ordinary_canonical_index_to_safe_canonical_index"]
    assert len(mapping) == len(set(mapping)) == 36
    assert out["explicit_bijection"]["all_288_equivariance_checks_pass"] is True
    assert out["gauge_count"]["total_Q8_equivariant_bijections"] == 1179648
    assert out["checks"]["order3_is_only_extension_obstruction"] is True
