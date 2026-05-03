"""
Tests for Part CCXLVI — Borcherds-Kac-Moody Algebras / Monster Moonshine Bridge
Expected: 21 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLVI_BORCHERDS_ALGEBRAS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    e8_roots, e8_rank, e8_dim, e6_weyl_order,
    j_constant, leech_kissing, j_c1,
    sporadic_count, happy_family_count, pariah_count,
    bosonic_critical_dim,
    fake_monster_simple_roots, bkm_weyl_order,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 21


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_e8_parameters():
    assert e8_roots == 240
    assert e8_roots == EDGES
    assert e8_rank == 8
    assert e8_dim == 248
    assert e8_dim == EDGES + K - MU


def test_j_function():
    # j(τ) = 1/q + 744 + 196884q + ...
    assert j_constant == 744
    assert j_constant == Q * 248
    assert j_c1 == 196884


def test_leech_kissing():
    assert leech_kissing == 196560


def test_sporadic_groups():
    assert sporadic_count == 26
    assert happy_family_count == EDGES // K   # 20
    assert pariah_count == K // LAM           # 6
    assert happy_family_count + pariah_count == sporadic_count


def test_bosonic_string():
    # Bosonic string critical dimension = 26
    assert bosonic_critical_dim == 26
    assert bosonic_critical_dim == V - K - LAM


def test_bkm_weyl():
    assert bkm_weyl_order == AUT_ORDER
    assert fake_monster_simple_roots == M_LAM


def test_e6_weyl_order():
    assert e6_weyl_order == AUT_ORDER
