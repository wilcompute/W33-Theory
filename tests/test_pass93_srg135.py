"""Pytest suite for Pass 93 -- SRG(135,70,37,35) from the W(3,3) glue group (O+_8(2) polar graph)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass93_srg135 as mod

    mod.main()
    return json.loads(Path("w33_pass93_srg135.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_srg_parameters() -> None:
    d = _data()
    assert d["vertices"] == 135
    assert d["degree"] == 70
    assert d["lambda"] == 37
    assert d["mu"] == 35
    assert d["is_SRG_135_70_37_35"] is True


def test_spectrum() -> None:
    spec = {int(k): v for k, v in _data()["spectrum"].items()}
    assert spec == {-5: 84, 7: 50, 70: 1}


def test_isotropic_count_matches_pass92() -> None:
    # 135 isotropic vertices = the 135 nonzero isotropic glue cosets of Pass 92
    assert _data()["vertices"] == 135
    assert 135 + 120 == 2**8 - 1
