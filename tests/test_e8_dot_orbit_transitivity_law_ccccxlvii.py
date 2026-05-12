"""Part CCCCXLVII -- E8 dot-orbit transitivity law."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLVII_E8_DOT_ORBIT_TRANSITIVITY_LAW")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLVII_e8_dot_orbit_transitivity_law_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLVII_e8_dot_orbit_transitivity_law_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 9
    assert data["checks_passed"] == 9


def test_dot_histogram_and_orbits() -> None:
    data = _load_results()
    assert data["dot_histogram"] == {
        "-8": 120,
        "-4": 6720,
        "0": 15120,
        "4": 6720,
        "8": 240,
    }
    # Orbit decomposition exists and covers each dot class.
    assert all(info["orbit_count"] > 0 for info in data["orbit_info"].values())


def test_exact_rescue_law() -> None:
    data = _load_results()
    assert data["rescue_by_dot"] == {
        "-8": 126,
        "-4": 234,
        "0": 240,
        "4": 234,
        "8": 126,
    }
    assert data["dot_unique_constants"] == {
        "-8": [126],
        "-4": [234],
        "0": [240],
        "4": [234],
        "8": [126],
    }
