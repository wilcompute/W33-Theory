"""
Tests for Part CCXLIV — Niemeier Lattices Bridge
Expected: 36 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLIV_NIEMEIER_LATTICES_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    niemeier_count, leech_kissing,
    golay_length, golay_dim, golay_min_dist,
    e8_kissing, sphere_pack_8d, sphere_pack_24d,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 36


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_niemeier_count():
    # 24 Niemeier lattices = K*LAM = 12*2
    assert niemeier_count == 24
    assert niemeier_count == K * LAM


def test_leech_kissing_number():
    # Leech kissing number = 196560 = EDGES * Phi3 * Phi6 * Q^2
    assert leech_kissing == 196560


def test_golay_code_parameters():
    assert golay_length == 24   # block length
    assert golay_dim == 12      # dimension
    assert golay_min_dist == 8  # minimum distance


def test_e8_kissing():
    assert e8_kissing == 240
    assert e8_kissing == EDGES


def test_sphere_packing_dims():
    assert sphere_pack_8d == 8    # E8 optimal packing dim
    assert sphere_pack_24d == 24  # Leech optimal packing dim
    assert sphere_pack_24d == K * LAM
