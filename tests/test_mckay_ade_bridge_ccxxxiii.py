"""
Tests for Part CCXXXIII — McKay Correspondence and ADE Dynkin Diagrams
from the W(3,3) strongly regular graph SRG(40,12,2,4).

74 tests across 11 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXIII_MCKAY_ADE_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER, LAP_MID, LAP_TOP,
    # B1
    order_2I_from_VQ, order_2I_from_K, order_2I_from_edges,
    irreps_2I, rank_E8_dynkin, largest_irrep_2I,
    # B2
    order_2T_from_Klam, irreps_2T, rank_E6_dynkin, weyl_E6_order,
    # B3
    order_2O_from_MUK, irreps_2O, rank_E7_dynkin,
    # B4
    cox_E6, cox_E7, cox_E8,
    cox_E6_from_2T, cox_E7_from_2O, cox_E8_from_2I,
    # B5
    roots_E6, roots_E7, roots_E8, roots_F4, roots_G2,
    # B6
    sum_sq_2I, sum_sq_2T,
    # B7
    nodes_E6, nodes_E7, nodes_E8, nodes_A2,
    nodes_Ehat6, nodes_Ehat7, nodes_Ehat8,
    # B8
    generations,
    # B9
    weyl_E6, lines_cubic,
    # B10
    mckay_edges_2I,
    # Meta
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count(self):
        assert len(checks) == 30

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXXIII_mckay_ade_results.json").exists()

    def test_json_verified(self):
        d = json.loads((ROOT / "PART_CCXXXIII_mckay_ade_results.json").read_text(encoding="utf-8"))
        assert d["Verified"] is True

    def test_json_checks(self):
        d = json.loads((ROOT / "PART_CCXXXIII_mckay_ade_results.json").read_text(encoding="utf-8"))
        assert d["checks_passed"] == 30
        assert d["checks_total"] == 30


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestBinaryIcosahedralGroup:
    """B1: 2I → E₈ via McKay correspondence."""

    def test_order_from_VQ(self):
        assert order_2I_from_VQ == 120

    def test_order_from_K(self):
        assert order_2I_from_K == 120

    def test_order_from_edges(self):
        assert order_2I_from_edges == 120

    def test_orders_consistent(self):
        assert order_2I_from_VQ == order_2I_from_K == order_2I_from_edges

    def test_irreps_count(self):
        # Extended Ê₈ has 9 nodes = irreps of 2I
        assert irreps_2I == 9

    def test_rank_E8(self):
        assert rank_E8_dynkin == 8

    def test_irreps_eq_2mu_plus_1(self):
        assert irreps_2I == 2 * MU + 1

    def test_rank_E8_eq_2mu(self):
        assert rank_E8_dynkin == 2 * MU

    def test_largest_irrep_eq_K_half(self):
        assert largest_irrep_2I == K // 2

    def test_largest_irrep_value(self):
        assert largest_irrep_2I == 6


class TestBinaryTetrahedralGroup:
    """B2: 2T → E₆ via McKay correspondence."""

    def test_order_from_Klam(self):
        assert order_2T_from_Klam == 24

    def test_order_eq_24(self):
        assert K * LAM == 24

    def test_irreps_2T(self):
        # Extended Ê₆ has 7 nodes = irreps of 2T
        assert irreps_2T == 7

    def test_rank_E6(self):
        assert rank_E6_dynkin == 6

    def test_rank_E6_eq_K_half(self):
        assert rank_E6_dynkin == K // 2

    def test_irreps_eq_K_half_plus_1(self):
        assert irreps_2T == K // 2 + 1

    def test_weyl_E6_order(self):
        assert weyl_E6_order == AUT_ORDER

    def test_weyl_E6_value(self):
        assert weyl_E6_order == 51840


class TestBinaryOctahedralGroup:
    """B3: 2O → E₇ via McKay correspondence."""

    def test_order_from_MUK(self):
        assert order_2O_from_MUK == 48

    def test_order_eq_MU_times_K(self):
        assert MU * K == 48

    def test_irreps_2O(self):
        # Extended Ê₇ has 8 nodes = irreps of 2O
        assert irreps_2O == 8

    def test_rank_E7(self):
        assert rank_E7_dynkin == 7

    def test_irreps_eq_2mu(self):
        assert irreps_2O == 2 * MU

    def test_rank_E7_eq_2mu_minus_1(self):
        assert rank_E7_dynkin == 2 * MU - 1


class TestCoxeterNumbers:
    """B4: Coxeter numbers from SRG constants."""

    def test_cox_E6_eq_K(self):
        assert cox_E6 == K

    def test_cox_E6_value(self):
        assert cox_E6 == 12

    def test_cox_E7_eq_K_plus_K_half(self):
        assert cox_E7 == K + K // 2

    def test_cox_E7_value(self):
        assert cox_E7 == 18

    def test_cox_E8_eq_V_minus_LAPMID(self):
        assert cox_E8 == V - LAP_MID

    def test_cox_E8_value(self):
        assert cox_E8 == 30

    def test_cox_E6_from_2T(self):
        assert cox_E6_from_2T == 12

    def test_cox_E8_from_2I(self):
        assert cox_E8_from_2I == 30

    def test_cox_E7_from_2O(self):
        assert cox_E7_from_2O == 18

    def test_cox_sequence_ascending(self):
        assert cox_E6 < cox_E7 < cox_E8


class TestRootSystemSizes:
    """B5: Root system sizes directly from SRG constants."""

    def test_roots_E6(self):
        assert roots_E6 == 72

    def test_roots_E6_formula(self):
        assert roots_E6 == K * (K // 2)

    def test_roots_E7(self):
        assert roots_E7 == 126

    def test_roots_E7_formula(self):
        assert roots_E7 == (K // 2 + 1) * (K + K // 2)

    def test_roots_E8(self):
        assert roots_E8 == 240

    def test_roots_E8_eq_EDGES(self):
        # This is the crown jewel: E₈ has exactly 240 roots = SRG edge count
        assert roots_E8 == EDGES

    def test_roots_F4(self):
        assert roots_F4 == 48

    def test_roots_F4_eq_order_2O(self):
        assert roots_F4 == order_2O_from_MUK

    def test_roots_G2(self):
        assert roots_G2 == 12

    def test_roots_G2_eq_K(self):
        assert roots_G2 == K


class TestSumOfSquares:
    """B6: Burnside / sum-of-squares identity for binary polyhedral groups."""

    def test_sum_sq_2I(self):
        assert sum_sq_2I == 120

    def test_sum_sq_2I_eq_order(self):
        assert sum_sq_2I == order_2I_from_VQ

    def test_sum_sq_2I_eq_VQ(self):
        assert sum_sq_2I == V * Q

    def test_sum_sq_2T(self):
        assert sum_sq_2T == 24

    def test_sum_sq_2T_eq_order(self):
        assert sum_sq_2T == order_2T_from_Klam

    def test_sum_sq_2T_eq_K_LAM(self):
        assert sum_sq_2T == K * LAM


class TestDynkinNodes:
    """B7: Node counts of ADE Dynkin diagrams from SRG constants."""

    def test_nodes_A2(self):
        # A₂: rank 2; Q generations linked to A_{Q-1}=A₂
        assert nodes_A2 == Q

    def test_nodes_E6(self):
        assert nodes_E6 == 6

    def test_nodes_E6_eq_K_half(self):
        assert nodes_E6 == K // 2

    def test_nodes_E7(self):
        assert nodes_E7 == 7

    def test_nodes_E7_eq_K_half_plus_1(self):
        assert nodes_E7 == K // 2 + 1

    def test_nodes_E8(self):
        assert nodes_E8 == 8

    def test_nodes_E8_eq_2MU(self):
        assert nodes_E8 == 2 * MU

    def test_nodes_Ehat6(self):
        assert nodes_Ehat6 == 7

    def test_nodes_Ehat7(self):
        assert nodes_Ehat7 == 8

    def test_nodes_Ehat8(self):
        assert nodes_Ehat8 == 9


class TestThreeGenerations:
    """B8: Three quark/lepton generations from binary cyclic at Q=3."""

    def test_generations(self):
        assert generations == Q

    def test_generations_value(self):
        assert generations == 3

    def test_weyl_E6(self):
        assert weyl_E6 == AUT_ORDER

    def test_lines_cubic(self):
        assert lines_cubic == M_LAM

    def test_lines_cubic_value(self):
        assert lines_cubic == 27

    def test_mckay_edges_2I_eq_EDGES(self):
        assert mckay_edges_2I == EDGES

    def test_mckay_edges_2I_value(self):
        assert mckay_edges_2I == 240
