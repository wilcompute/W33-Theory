"""Regression gate for the ladder checkpoint placement binding."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

from w33_ladder_checkpoint_placement import verify  # noqa: E402


def test_placement_certificate_passes() -> None:
    payload = verify()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())


def test_placement_matches_frozen_artifact() -> None:
    payload = verify()
    frozen_path = os.path.join(ROOT, "data", "w33_ladder_checkpoint_placement.json")
    with open(frozen_path, encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["certificate_sha256"] == payload["certificate_sha256"]


def test_binding_uses_certified_ladder_table() -> None:
    payload = verify()
    assert payload["boundary_table"] == [36, 64, 84, 96, 100, 96, 84, 64, 36, 0]
    assert payload["source_certificate"]["schema"] == "w33.spread-ladder-reversible-gc.v1"
    for row in payload["placed_regimes"].values():
        assert row["plan"]["peak_live_boundary"] <= 100
