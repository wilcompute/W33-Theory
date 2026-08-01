from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1867_1871_outer_doily_transfer_clock.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1867_1871", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_outer_doily_transfer_clock(tmp_path):
    # Rebuilding the certificate is part of the test: no frozen-data-only pass.
    module = load_module()
    result = module.main(tmp_path / "certificate.json")
    assert result["status"] == "PASS"
    assert result["n_verified"] == result["n_checks"] == 24
    assert result["rank"] == result["rank_mod2"] == 10
    assert result["nullity"] == 5
    assert result["smith_nonzero"] == [1] * 10
    assert result["sha256_without_hash_field"] == "f032136a1c9ff987cf7cc0f6bef4503573e97a099ea6c5f345b418e3de1512eb"
    assert result["checks"]["twisted_equivariance_generators"]
    assert result["checks"]["clock_integer_identity"]
    assert result["checks"]["doily_srg_identity"]
