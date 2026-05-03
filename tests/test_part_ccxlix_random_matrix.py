"""
Tests for Part CCXLIX — Random Matrix Theory Bridge
Expected: 27 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLIX_RANDOM_MATRIX_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    beta_GOE, beta_GUE, beta_GSE, beta_sum,
    wigner_GUE_prefactor_int,
    srg_eval_trivial, srg_eval_r, srg_eval_s,
    gap_K_r, gap_K_s, gap_r_s,
    montgomery_peak, spectral_gap, srg_nonzero,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 27


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_dyson_beta_ensemble():
    assert beta_GOE == 1
    assert beta_GUE == LAM       # 2
    assert beta_GSE == MU        # 4
    assert beta_sum == 7         # Phi6 = Q^2 - Q + 1 = 7


def test_wigner_prefactor():
    assert wigner_GUE_prefactor_int == LAM * LAP_TOP  # 2*16 = 32


def test_srg_eigenvalue_gaps():
    assert gap_K_r == LAP_MID     # 10
    assert gap_K_s == LAP_TOP     # 16
    assert gap_r_s == K // LAM    # 6


def test_spectral_gap():
    assert spectral_gap == LAP_MID - LAM   # 8


def test_srg_nonzero():
    assert srg_nonzero == EDGES * LAM   # 480


def test_montgomery_peak():
    # Montgomery correlation peak at spacing ~ Q
    assert montgomery_peak == Q
