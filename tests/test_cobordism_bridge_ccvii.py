"""Regression tests for Part CCVII: Cobordism Bridge."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
if str(_ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(_ROOT / "exploration"))

from PART_CCVII_COBORDISM_BRIDGE import (
    K, PHI6, MULT_K2, LEECH_DIM,
    CobordismBridge, build_cobordism_bridge_summary, _verify,
)


def test_ccvii_bridge_values():
    b = CobordismBridge()
    assert b.omega_so_rank == K == 12
    assert b.omega_o_rank == PHI6 == 7
    assert b.signature_shadow == 8
    assert b.euler_cobordism == -200
    assert b.pontryagin_shadow == -140
    assert b.sw_parity == 0
    assert b.framed_stem_shadow == MULT_K2 == 6
    assert b.boundary_index == K
    assert b.thom_degree == 24
    assert b.mu_grade == LEECH_DIM == 24


def test_ccvii_verifier():
    assert _verify(CobordismBridge()) == []


def test_ccvii_summary():
    s = build_cobordism_bridge_summary()
    assert s["verified"] is True
    assert s["failures"] == []
    assert s["omega_so_rank"] == 12
    assert s["omega_o_rank"] == 7
    assert s["thom_degree"] == 24
    assert s["mu_grade"] == 24
