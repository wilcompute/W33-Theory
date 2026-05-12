"""Part CCCCLI -- E8 rescue distribution and generating-function law."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCLI_E8_RESCUE_DISTRIBUTION_MGF")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCLI_e8_rescue_distribution_mgf_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCLI_e8_rescue_distribution_mgf_results.json"
    assert out.exists()


def test_verified_and_counts() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 8
    assert data["checks_passed"] == 8
    assert data["pair_count"] == 28920


def test_exact_distribution_and_polynomial() -> None:
    data = _load_results()
    assert data["rescue_distribution"] == {
        "126": 360,
        "234": 13440,
        "240": 15120,
    }
    assert data["weighted_rescue_total"] == 6819120
    assert "360 t^126" in data["counting_generating_polynomial"]
    assert "13440 t^234" in data["counting_generating_polynomial"]
    assert "15120 t^240" in data["counting_generating_polynomial"]


def test_moment_payloads() -> None:
    data = _load_results()
    m = data["moments"]
    assert m["raw_m1"]["denominator"] > 0
    assert m["variance"]["numerator"] > 0
