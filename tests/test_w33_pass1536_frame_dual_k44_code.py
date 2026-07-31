from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "analysis" / "w33_pass1536_frame_dual_k44_code.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1536", MODULE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fast_exact_certificate():
    module = load_module()
    payload = module.certificate(run_milp=False)
    assert payload["status"] == "PASS"
    assert payload["parameters"]["frame_code"] == [240, 195, 4]
    assert payload["parameters"]["frame_dual_code"] == [240, 45, 16]
    assert payload["overlap_geometry"]["Gram_rank_mod_2"] == 14
    assert payload["overlap_geometry"]["Gram_rank_mod_3"] == 15
    assert all(payload["checks"].values())
