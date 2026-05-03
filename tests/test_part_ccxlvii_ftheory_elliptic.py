"""
Tests for Part CCXLVII — F-theory and Elliptic Fibrations Bridge
Expected: 31 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLVII_FTHEORY_ELLIPTIC_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    f_theory_dim, m_theory_dim, iia_iib_dim, fiber_torus_dim,
    kodaira_II, kodaira_III, kodaira_IV, kodaira_I0s,
    kodaira_IIs, kodaira_IIIs, kodaira_IVs,
    e8_rank, e7_rank, e6_rank, e8_dim, e8xe8_dim, so32_rank, so32_dim,
    k3_b2, mw_bound,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 31


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_string_theory_dimensions():
    assert f_theory_dim == K           # 12
    assert m_theory_dim == K - 1      # 11
    assert iia_iib_dim == LAP_MID     # 10
    assert fiber_torus_dim == LAM     # 2


def test_kodaira_types():
    # Non-simply-laced Kodaira types: II, III, IV, I0* have Euler characters 2,3,4,6
    assert kodaira_II == LAM       # 2
    assert kodaira_III == Q        # 3
    assert kodaira_IV == MU        # 4
    assert kodaira_I0s == K // LAM  # 6
    # Star types: II*, III*, IV*
    assert kodaira_IIs == LAP_MID           # 10
    assert kodaira_IIIs == LAP_MID - 1      # 9
    assert kodaira_IVs == LAP_MID - LAM     # 8


def test_exceptional_gauge_groups():
    assert e8_rank == LAP_MID - LAM   # 8
    assert e7_rank == e8_rank - 1     # 7
    assert e6_rank == e8_rank - LAM   # 6
    assert e8_dim == 248


def test_heterotic_gauge_groups():
    assert e8xe8_dim == 496
    assert so32_rank == 32
    assert so32_dim == 496
    assert e8xe8_dim == so32_dim


def test_k3_mordell_weil():
    assert k3_b2 == 22
    assert mw_bound >= 0
