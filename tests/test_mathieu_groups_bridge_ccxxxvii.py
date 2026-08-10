"""
Tests for Part CCXXXVII — Mathieu Groups from W(3,3)
SRG(40,12,2,4) constants.

~65 tests across 10 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXVII_MATHIEU_GROUPS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    num_sporadic, num_Mathieu,
    deg_M11, deg_M12, deg_M22, deg_M23, deg_M24,
    order_M11, order_M12, order_PSL34,
    order_M22, order_M23, order_M24,
    M12_stab_eq_M11,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count_at_least_30(self):
        assert len(checks) >= 30

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXXVII_mathieu_groups_results.json").exists()

    def test_json_verified(self):
        d = json.loads((ROOT / "PART_CCXXXVII_mathieu_groups_results.json").read_text(encoding="utf-8"))
        assert d["Verified"] is True

    def test_json_checks_equal(self):
        d = json.loads((ROOT / "PART_CCXXXVII_mathieu_groups_results.json").read_text(encoding="utf-8"))
        assert d["checks_passed"] == d["checks_total"]


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240


class TestCounting:
    """C1/C2: Sporadic group count and Mathieu group count."""

    def test_num_sporadic_value(self):
        assert num_sporadic == 26

    def test_num_sporadic_eq_V_minus_K_minus_LAM(self):
        assert num_sporadic == V - K - LAM

    def test_V_minus_K_minus_LAM_26(self):
        assert V - K - LAM == 26

    def test_num_Mathieu_value(self):
        assert num_Mathieu == 5

    def test_num_Mathieu_eq_K_div_LAM_minus_1(self):
        assert num_Mathieu == K // LAM - 1

    def test_K_div_LAM_minus_1_eq_5(self):
        assert K // LAM - 1 == 5


class TestMathieuDegrees:
    """D1–D5: Minimal permutation degrees of M₁₁ through M₂₄."""

    def test_deg_M11_eq_K_minus_1(self):
        assert deg_M11 == K - 1

    def test_deg_M11_value(self):
        assert deg_M11 == 11

    def test_deg_M12_eq_K(self):
        assert deg_M12 == K

    def test_deg_M12_value(self):
        assert deg_M12 == 12

    def test_deg_M22_eq_2_K_minus_1(self):
        assert deg_M22 == 2 * (K - 1)

    def test_deg_M22_value(self):
        assert deg_M22 == 22

    def test_deg_M23_eq_2K_minus_1(self):
        assert deg_M23 == 2 * K - 1

    def test_deg_M23_value(self):
        assert deg_M23 == 23

    def test_deg_M24_eq_K_LAM(self):
        assert deg_M24 == K * LAM

    def test_deg_M24_value(self):
        assert deg_M24 == 24

    def test_consecutive_degree_pairs(self):
        # M₁₁–M₁₂ and M₂₂–M₂₃–M₂₄ differ by 1
        assert deg_M12 - deg_M11 == 1
        assert deg_M23 - deg_M22 == 1
        assert deg_M24 - deg_M23 == 1


class TestGroupOrders:
    """O1–O12: Orders of all five Mathieu groups and PSL(3,4)."""

    def test_order_M11_value(self):
        assert order_M11 == 7920

    def test_order_M11_formula(self):
        assert order_M11 == K * (K - 1) * (K - LAM) * Q * LAM

    def test_K_K1_KLAM_Q_LAM_eq_7920(self):
        assert K * (K - 1) * (K - LAM) * Q * LAM == 7920

    def test_order_M12_value(self):
        assert order_M12 == 95040

    def test_order_M12_formula(self):
        assert order_M12 == EDGES * K * (K - 1) * Q

    def test_EDGES_K_K1_Q_eq_95040(self):
        assert EDGES * K * (K - 1) * Q == 95040

    def test_order_PSL34_value(self):
        assert order_PSL34 == 20160

    def test_order_PSL34_formula(self):
        assert order_PSL34 == EDGES * K * (K // 2 + 1)

    def test_EDGES_K_Khalf1_eq_20160(self):
        assert EDGES * K * (K // 2 + 1) == 20160

    def test_order_M22_value(self):
        assert order_M22 == 443520

    def test_order_M22_formula(self):
        assert order_M22 == 2 * (K - 1) * order_PSL34

    def test_order_M23_value(self):
        assert order_M23 == 10200960

    def test_order_M23_formula(self):
        assert order_M23 == (2 * K - 1) * order_M22

    def test_order_M24_value(self):
        assert order_M24 == 244823040

    def test_order_M24_formula(self):
        assert order_M24 == K * LAM * order_M23


class TestStabilizerChain:
    """S1–S5: Orbit-stabilizer theorem through the Mathieu chain."""

    def test_M12_stab_eq_M11(self):
        assert M12_stab_eq_M11 is True

    def test_M12_div_deg_eq_M11(self):
        assert order_M12 // deg_M12 == order_M11

    def test_M22_div_deg_eq_PSL34(self):
        assert order_M22 // deg_M22 == order_PSL34

    def test_M23_div_deg_eq_M22(self):
        assert order_M23 // deg_M23 == order_M22

    def test_M24_div_deg_eq_M23(self):
        assert order_M24 // deg_M24 == order_M23


class TestGolayConnections:
    """G1–G3: Connections to Golay codes and Leech lattice."""

    def test_deg_M24_eq_binary_Golay_n(self):
        # M₂₄ acts on K·λ = 24 = binary Golay code length
        assert deg_M24 == K * LAM

    def test_deg_M12_eq_ternary_Golay_n(self):
        # M₁₂ acts on K = 12 = ternary Golay code length
        assert deg_M12 == K

    def test_deg_M24_eq_Leech_dim(self):
        # deg(M₂₄) = K·λ = 24 = dim(Λ₂₄)
        assert deg_M24 == K * LAM == 24


class TestCrossChecks:
    def test_num_sporadic_is_26(self):
        assert num_sporadic == 26

    def test_num_Mathieu_is_5(self):
        assert num_Mathieu == 5

    def test_K_half_plus_1_in_PSL34(self):
        # K//2 + 1 = 7 appears in |PSL(3,4)|
        assert K // 2 + 1 == 7

    def test_order_ratios_are_integer(self):
        assert order_M24 % order_M23 == 0 or order_M24 // deg_M24 == order_M23
        assert order_M23 % order_M22 == 0 or order_M23 // deg_M23 == order_M22
