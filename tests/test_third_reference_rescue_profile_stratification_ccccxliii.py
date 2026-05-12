"""Part CCCCXLIII -- sampled third-reference rescue-profile stratification."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLIII_THIRD_REFERENCE_RESCUE_PROFILE_STRATIFICATION")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLIII_third_reference_rescue_profile_stratification_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLIII_third_reference_rescue_profile_stratification_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 6
    assert data["checks_passed"] == 6


def test_profile_shape() -> None:
    data = _load_results()
    profiles = data["profiles"]
    assert len(profiles) == 3
    assert data["sample_per_signature"] == 12
    assert sorted(p["pair_count"] for p in profiles) == [360, 13440, 15120]
    assert all(p["sample_size"] == 12 for p in profiles)


def test_sampled_unique_rescue_constants() -> None:
    data = _load_results()
    profiles = data["profiles"]
    constants = sorted(p["sample_unique_counts"][0] for p in profiles)
    assert constants == [126, 234, 240]
