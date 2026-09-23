from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_q3_extended_clifford_saturation.py"
DATA = ROOT / "data/w33_q3_extended_clifford_saturation.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_q3_clifford_saturation", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_q3_extended_clifford_saturation_replays_frozen_certificate():
    module = load_module()
    got = module.main(write=False)
    frozen = json.loads(DATA.read_text())
    # JSON stringifies the integer dictionary keys in the wide-prime scan.
    got = json.loads(json.dumps(got))
    assert got == frozen
    assert got["theorem"]["index"] == "(p-1)/2"
    assert got["theorem"]["saturation_condition"] == "(p-1)/2=1 iff p=3"
    cases = {row["p"]: row for row in got["cases"]}
    assert cases[3]["saturates_full_automorphism_group"] is True
    assert cases[5]["index_full_over_extended_Clifford"] == 2
    assert cases[7]["index_full_over_extended_Clifford"] == 3
    assert all(got["checks"].values())
