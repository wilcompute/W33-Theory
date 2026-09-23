from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_hesse36_physical_fi_orientation_selector.py"
DATA = ROOT / "data/w33_hesse36_physical_fi_orientation_selector.json"


def load():
    spec = importlib.util.spec_from_file_location("fi_orientation", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_frozen_physical_orientation_selects_identity_character_order():
    out = json.loads(DATA.read_text())
    assert out["selection"]["upstream_survivors"] == [[0,1,2],[0,2,1]]
    assert out["selection"]["safe_sheet_order"] == [0,1,2]
    assert out["selection"]["selected_assignment"] == [0,1,2]
    assert out["selection"]["conjugate_assignment"] == [0,2,1]
    assert out["selection"]["selected_character_values_on_z"] == ["1","omega","omega^2"]
    assert out["selection"]["unique_relative_to_frozen_orientation"] is True
    assert out["selection"]["absolute_orientation_without_frozen_convention"] is False
    assert out["transport_chain"]["dictionary_central_z_physical_coordinate"] == [0,0,1]
    assert all(out["checks"].values())
