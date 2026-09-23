from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_extended_clifford_g26_no_go.py"
DATA = ROOT / "data/w33_extended_clifford_g26_no_go.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_ext_cliff_g26_nogo", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extended_clifford_g26_no_go_replays_frozen_certificate():
    module = load_module()
    got = module.main(write=False)
    frozen = json.loads(DATA.read_text())
    assert got == frozen
    assert got["extended_qutrit_group"]["center_order"] == 1
    assert got["G26_classification_input"]["explicit_central_C2_factor"] is True
    assert got["checks"]["center_invariant_proves_nonisomorphism"] is True
    assert got["important_non_no_go"].startswith("This theorem does not rule out")
    assert all(got["checks"].values())
