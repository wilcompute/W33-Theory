"""Pytest suite for Pass 86 -- MacWilliams dual [40,24] of C_2(W)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass86_macwilliams_dual as mod

    mod.main()
    return json.loads(Path("w33_pass86_macwilliams_dual.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_dual_is_40_24_6() -> None:
    d = _data()["dual_C2perp"]
    assert (d["n"], d["k"], d["d"]) == (40, 24, 6)
    assert d["total"] == 2**24


def test_dual_min_weight_240_e8_roots() -> None:
    d = _data()["dual_C2perp"]
    wd = {int(k): v for k, v in d["weight_distribution"].items()}
    assert wd[6] == 240  # = 240 E8 roots = edges of W(3,3)


def test_self_orthogonal_containment() -> None:
    assert _data()["self_orthogonal_containment"] is True


def test_e6_e8_numbers_appear() -> None:
    apps = _data()["e6_appearances"]
    counts = {(a["count"], a["e6"]) for a in apps}
    assert (45, "tritangent planes") in counts  # E6
    assert (240, "E8 roots = edges") in counts  # E8
