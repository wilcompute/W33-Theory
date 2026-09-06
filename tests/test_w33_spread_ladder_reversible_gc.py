"""Regression gate for the spread-ladder reversible GC optimality certificate."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

from w33_spread_ladder_reversible_gc import verify  # noqa: E402


def test_spread_ladder_reversible_gc_certificate_passes() -> None:
    payload = verify()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())


def test_certificate_matches_frozen_artifact() -> None:
    payload = verify()
    frozen_path = os.path.join(ROOT, "data", "w33_spread_ladder_reversible_gc.json")
    with open(frozen_path, encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["certificate_sha256"] == payload["certificate_sha256"]
    assert frozen["status"] == "PASS"


def test_economics_core_numbers() -> None:
    payload = verify()
    econ = payload["reversible_gc_economics"]
    assert econ["per_tier_release_boundary"] == [36, 64, 84, 96, 100, 96, 84, 64, 36, 0]
    assert econ["total_boundary_single_pass"] == 660
    assert econ["total_boundary_full_cycle"] == 1320
    assert econ["peak_live_boundary"] == 100
    assert econ["migration_cost_per_resize"] == 0
