"""Part CCCCXLI -- E8 two-reference signature stratification."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLI_E8_TWO_REFERENCE_SIGNATURE_STRATIFICATION")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLI_e8_two_reference_signature_stratification_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLI_e8_two_reference_signature_stratification_results.json"
    assert out.exists()


def test_verified_and_check_counts() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 7
    assert data["checks_passed"] == 7


def test_search_summary() -> None:
    data = _load_results()
    s = data["search"]
    assert s["roots"] == 240
    assert s["pairs_including_diagonal"] == 28920
    assert s["distinct_signatures"] == 3
    assert s["feasible_signatures"] == 1
    assert s["feasible_pairs"] == 15120


def test_signature_family_multiplicities() -> None:
    data = _load_results()
    families = data["signature_families"]
    counts = sorted(f["pair_count"] for f in families)
    assert counts == [360, 13440, 15120]

    feasible_counts = [f["pair_count"] for f in families if f["feasible_24_108_108"]]
    assert feasible_counts == [15120]
