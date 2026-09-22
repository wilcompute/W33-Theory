from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_objectwise_matter_parity_cubic_incidence.py"
DATA = ROOT / "data/w33_objectwise_matter_parity_cubic_incidence.json"


def test_checked_objectwise_parity_certificate_is_valid_and_current():
    checked = json.loads(DATA.read_text())
    spec = importlib.util.spec_from_file_location("objectwise_parity_replay", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    recomputed = module.main(write=False)
    assert checked == recomputed
    assert checked["tritangent_census"] == {
        "SO10": {"1+10+10": 5, "10+16+16": 40},
        "Qpsi": {"-2,-2,4": 5, "-2,1,1": 40},
        "matter_odd_count": {"0": 5, "2": 40},
    }

