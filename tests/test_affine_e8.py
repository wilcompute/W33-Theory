"""Tests for affine E8 character exploration."""
from __future__ import annotations

import sys
from pathlib import Path
from fractions import Fraction

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_affine_e8 import affine_e8_series, derive_all_affine_e8


def test_affine_e8_shift_and_leading_coeff():
    r = affine_e8_series(q_order=10)
    assert r["shift"] == Fraction(-1, 3)
    assert isinstance(r["series"][0], int)
    assert r["series"][0] == 1


def test_driver_chain():
    r = derive_all_affine_e8(q_order=8)
    assert r["summary_chain"]["vacuum_shift_minus_one_third"] is True
    assert r["summary_chain"]["leading_coeff_1"] is True
