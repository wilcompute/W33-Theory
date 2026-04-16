"""Tests for the Ramanujan-Weber exploration utilities."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_ramanujan_weber import compute_e_pi_sqrt, derive_all_ramanujan_weber


def test_ramanujan_163_near_integer():
    try:
        import mpmath as mp
    except Exception:
        pytest.skip("mpmath not available in environment")
    # Ensure mpmath uses sufficient precision for the rounding operations
    old = mp.mp.dps
    mp.mp.dps = 160
    try:
        val = compute_e_pi_sqrt(163, prec=140)
        nearest = mp.nint(val)
        diff = mp.fabs(val - nearest)
        # Known near-integer: require high precision to see the tiny fractional part
        assert diff < mp.mpf("1e-9")
    finally:
        mp.mp.dps = old


def test_driver_chain_all_true():
    try:
        import mpmath as mp
    except Exception:
        pytest.skip("mpmath not available in environment")

    res = derive_all_ramanujan_weber(prec=80)
    assert res["summary_chain"]["ramanujan_163_near_integer"] is True
