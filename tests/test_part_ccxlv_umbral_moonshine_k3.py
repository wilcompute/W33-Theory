"""
Tests for Part CCXLV — Umbral Moonshine / K3 Bridge
Expected: 33 checks, Verified=True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCXLV_UMBRAL_MOONSHINE_K3_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    k3_euler, k3_h11, k3_b2,
    k3_bplus, k3_bminus, k3_signature_sum,
    umbral_count, umbral_count_form2,
    m24_degree,
    k3_hyp_planes, k3_e8_copies, k3_lattice_rank,
    checks, Verified,
)


def test_all_checks_pass():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_verified_true():
    assert Verified is True


def test_check_count():
    assert len(checks) == 33


def test_srg_params():
    assert Q == 3
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_k3_euler_characteristic():
    # χ(K3) = 24 = K*LAM
    assert k3_euler == 24
    assert k3_euler == K * LAM


def test_k3_hodge_numbers():
    # h^{1,1}(K3) = 20 = V//LAM
    assert k3_h11 == 20
    assert k3_h11 == V // LAM


def test_k3_second_betti():
    # b₂(K3) = 22
    assert k3_b2 == 22


def test_k3_signature():
    # b⁺ = 3 = Q, b⁻ = 19
    assert k3_bplus == Q
    assert k3_bminus == 19
    assert k3_signature_sum == k3_b2


def test_umbral_moonshine_count():
    # 23 Umbral Moonshine cases = M_LAM - MU = 27 - 4
    assert umbral_count == 23
    assert umbral_count == M_LAM - MU
    assert umbral_count_form2 == 23


def test_m24_degree():
    # M24 acts on 24 points = K*LAM
    assert m24_degree == K * LAM


def test_k3_lattice():
    # H² ≅ 3U ⊕ 2(-E8): 3 hyperbolic planes, 2 E8 copies
    assert k3_hyp_planes == Q
    assert k3_e8_copies == LAM
    assert k3_lattice_rank == 22
