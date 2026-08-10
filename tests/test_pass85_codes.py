"""Pytest suite for Pass 85 -- the binary code C_2(W) = [40,16,8] weight enumerator.

Reads the committed GUAVA certificate w33_pass85_codes_out.txt; no live GAP needed.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass85_codes as mod

    mod.main()
    return json.loads(Path("w33_pass85_codes.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_is_40_16_8() -> None:
    c = _data()["code"]
    assert (c["n"], c["k"], c["d"]) == (40, 16, 8)


def test_weight_distribution() -> None:
    c = _data()["code"]
    wd = {int(k): v for k, v in c["weight_distribution"].items()}
    assert wd == {
        0: 1,
        8: 45,
        12: 1120,
        16: 15570,
        20: 32064,
        24: 15570,
        28: 1120,
        32: 45,
        40: 1,
    }
    assert c["total_codewords"] == 2**16
    assert sum(wd.values()) == 2**16


def test_code_structure() -> None:
    c = _data()["code"]
    assert c["doubly_even"] is True
    assert c["self_orthogonal"] is True  # A^2 = 0 mod 2 (k,lambda,mu even)
    assert c["symmetric_contains_allones"] is True


def test_45_tritangent_planes() -> None:
    d = _data()
    wd = {int(k): v for k, v in d["code"]["weight_distribution"].items()}
    assert wd[8] == 45  # = 45 tritangent planes (E6)
    assert d["connections"]["45_min_weight_words_are_tritangent_planes"] is True
