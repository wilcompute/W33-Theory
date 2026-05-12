"""Part CCCCXL -- E8 two-reference non-uniqueness witness."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXL_e8_two_reference_partition_nogo_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXL_e8_two_reference_partition_nogo_results.json"
    assert out.exists()


def test_verified_and_counts() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 8
    assert data["checks_passed"] == 8


def test_pair_search_size() -> None:
    data = _load_results()
    assert data["search"]["roots"] == 240
    assert data["search"]["pairs_including_diagonal"] == 28920


def test_expected_degeneracy_hits() -> None:
    data = _load_results()
    assert data["search"]["distinct_signatures"] == 3
    assert data["search"]["feasible_signatures"] == 1
    assert data["search"]["hits"] == 15120
