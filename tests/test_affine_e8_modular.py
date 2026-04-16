"""Tests for numeric modular-invariance of the affine E8 character."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

import pytest

from w33_affine_e8_modular import verify_affine_e8_modular


def test_affine_e8_S_invariance():
    try:
        import mpmath as mp  # noqa: F401
    except Exception:
        pytest.skip("mpmath not available")

    r = verify_affine_e8_modular(q_order=40, tau_im=0.5, prec=80)
    assert r.get("match", False) is True
