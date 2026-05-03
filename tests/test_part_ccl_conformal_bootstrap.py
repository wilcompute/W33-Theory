"""
Tests for Part CCL — Conformal Bootstrap Bridge
Expected: 26 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCL_CONFORMAL_BOOTSTRAP_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    bootstrap_dim, conf_group_dim, conf_rank,
    crossing_operators, crossing_channels,
    stress_tensor_spin,
    max_spin_truncation, num_functionals,
    ope_matrix_size, island_corners,
    regge_intercept, regge_double_trace,
    laplacian_gap, laplacian_top, laplacian_sum,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 26


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_conformal_group():
    assert bootstrap_dim == Q       # 3d bootstrap
    assert conf_group_dim == LAP_MID  # SO(5) dim = (3+2)(3+1)//2 = 10
    assert conf_rank == LAM         # rank of SO(d+2) at d=2 ... 2


def test_crossing_symmetry():
    assert crossing_operators == MU    # 4 independent operators at crossing
    assert crossing_channels == Q     # 3 channels (s,t,u)


def test_stress_tensor():
    assert stress_tensor_spin == LAM   # spin-2


def test_bootstrap_truncation():
    assert max_spin_truncation == LAP_MID   # 10
    assert num_functionals == K // LAM      # 6


def test_ope_and_island():
    assert ope_matrix_size == V        # 40
    assert island_corners == MU       # 4 corners of 3d Ising island


def test_regge_limit():
    assert regge_intercept == LAM        # j₀ = 2 (stress tensor)
    assert regge_double_trace == MU      # j₀ = 4 (double-trace)


def test_laplacian_relation():
    assert laplacian_gap == LAP_MID     # 10
    assert laplacian_top == LAP_TOP     # 16
    assert laplacian_sum == LAP_MID + LAP_TOP  # 26
