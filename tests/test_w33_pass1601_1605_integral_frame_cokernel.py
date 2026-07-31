from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1601_1605_integral_frame_cokernel.py"
DATA = ROOT / "data" / "w33_pass1601_1605_integral_frame_cokernel.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1601_1605", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_integral_frame_cokernel_certificate() -> None:
    module = load_module()
    fresh = module.certificate()
    frozen = json.loads(DATA.read_text(encoding="utf-8"))
    assert fresh == frozen
    assert fresh["status"] == "PASS"
    assert all(fresh["checks"].values())
    assert fresh["passes"]["1601"]["smith_normal_form_M_transpose"] == {
        "1": 195,
        "2": 30,
        "0": 15,
    }
    assert fresh["passes"]["1602"]["explicit_quotient_rank"] == 30
    assert fresh["passes"]["1603"]["half_incidence_design"]["gram_spectrum"] == {
        "432": 1,
        "72": 24,
        "54": 20,
    }
