from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hybrid81_operator_equivariance_budget.py"
DATA = ROOT / "data/w33_hybrid81_operator_equivariance_budget.json"


def load():
    spec = importlib.util.spec_from_file_location("equiv_budget", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_exact_equivariance_deficit():
    out = json.loads(DATA.read_text())
    budget = out["equivariant_map_budget"]
    assert budget["maximum_ranks"] == {
        "visible73_to_operator81": 24,
        "dark8_to_operator81": 3,
        "full81_to_operator81": 27,
    }
    assert budget["full_equivariance_deficit"] == 54
    assert out["modules"]["dark8"]["operator_compatible"] == ["S_1_0"]
    assert set(out["modules"]["dark8"]["operator_incompatible"]) == {
        "L_0_0_1","L_0_0_2","S_2_0"
    }
    assert "No objectwise identification" in out["count_collision_firewall"]
    assert all(out["checks"].values())
