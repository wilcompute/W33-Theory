"""Part CCCCXLVI -- E8 inner-product rescue trichotomy."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLVI_E8_INNER_PRODUCT_RESCUE_TRICHOTOMY")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLVI_e8_inner_product_rescue_trichotomy_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLVI_e8_inner_product_rescue_trichotomy_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 7
    assert data["checks_passed"] == 7


def test_dot_histogram_and_constants() -> None:
    data = _load_results()
    hist = data["dot_histogram"]
    assert hist == {"-8": 120, "-4": 6720, "0": 15120, "4": 6720, "8": 240}
    assert data["trichotomy_constants"] == [126, 234, 240]


def test_profile_shape() -> None:
    data = _load_results()
    profiles = data["profiles"]
    assert len(profiles) == 3
    assert sorted(p["pair_count"] for p in profiles) == [360, 13440, 15120]
    # Each dot subprofile is constant over sampled first-50 pairs.
    assert all(
        info["constant_over_sample"]
        for p in profiles
        for info in p["dot_profiles"].values()
    )
