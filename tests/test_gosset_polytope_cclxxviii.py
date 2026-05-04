"""Tests for Part CCLXXVIII — Gosset Polytope Tower and the W(3,3) Arithmetic Atlas."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))

from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import (
    build_cclxxviii_bridge_summary,
    verify_gosset_vertex_tower,
    verify_gosset_W33_alignment,
    verify_weyl_group_orders,
    verify_weyl_coset_indices,
    verify_e8_roots_equal_edges,
    verify_e8_dimension,
    verify_e8_coxeter_number,
    verify_local_graph_tower,
    verify_gosset_edges,
    verify_gewirtz_V_formula,
    verify_e6_data,
    verify_e7_data,
    verify_e8_we8_factorisation,
    verify_240_factorizations,
    verify_transport_via_gosset,
    verify_wd5_as_stab_line,
    verify_e8_theta_series,
    verify_gosset_ambient_dimensions,
    verify_schlafli_graph_in_gosset,
    verify_e8_kissing_number,
    verify_gosset_ratio_chain,
    verify_e6_e7_e8_dimensions,
    verify_combinatorial_batch,
    verify_gosset_and_ternary_golay,
    verify_e8_modular_connection,
    verify_gosset_to_w33_vertex_map,
    # Constants
    V, K, LAM, MU, Q, PHI4, EDGES, AUT_ORDER,
    P_1_21, P_2_21, P_3_21, P_4_21,
    WD4_ORDER, WD5_ORDER, WE6_ORDER, WE7_ORDER, WE8_ORDER,
    E8_RANK, E8_ROOTS, E8_DIM, E8_COXETER,
    LINES_27, GEWIRTZ_V, TRANSPORT_EDGES,
)


def _assert_ok(result):
    ok, details = result
    failed = {k: v for k, v in details.items() if isinstance(v, bool) and not v}
    assert ok, f"Failed sub-checks: {failed}"


class TestGossetVertexTower:
    def test_gosset_vertex_tower(self):
        _assert_ok(verify_gosset_vertex_tower())

    def test_gosset_W33_alignment(self):
        _assert_ok(verify_gosset_W33_alignment())

    def test_vertex_count_is_PHI4(self):
        assert P_1_21 == PHI4 == 10

    def test_vertex_count_is_LINES_27(self):
        assert P_2_21 == LINES_27 == 27

    def test_vertex_count_is_GEWIRTZ_V(self):
        assert P_3_21 == GEWIRTZ_V == 56

    def test_vertex_count_is_EDGES(self):
        assert P_4_21 == EDGES == 240


class TestWeylGroups:
    def test_weyl_group_orders(self):
        _assert_ok(verify_weyl_group_orders())

    def test_weyl_coset_indices(self):
        _assert_ok(verify_weyl_coset_indices())

    def test_D5_D4_index_is_10(self):
        assert WD5_ORDER // WD4_ORDER == 10 == PHI4

    def test_E6_D5_index_is_27(self):
        assert WE6_ORDER // WD5_ORDER == 27 == LINES_27

    def test_E7_E6_index_is_56(self):
        assert WE7_ORDER // WE6_ORDER == 56 == GEWIRTZ_V

    def test_E8_E7_index_is_240(self):
        assert WE8_ORDER // WE7_ORDER == 240 == EDGES


class TestE8Roots:
    def test_e8_roots_equal_edges(self):
        _assert_ok(verify_e8_roots_equal_edges())

    def test_e8_roots_count(self):
        assert E8_ROOTS == 240 == EDGES

    def test_e8_positive_roots(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import E8_POSITIVE_ROOTS
        assert E8_POSITIVE_ROOTS == 120 == EDGES // 2


class TestE8Dimension:
    def test_e8_dimension(self):
        _assert_ok(verify_e8_dimension())

    def test_dim_e8_formula(self):
        assert E8_DIM == E8_RANK + E8_ROOTS == 8 + 240 == 248


class TestCoxeterNumber:
    def test_e8_coxeter_number(self):
        _assert_ok(verify_e8_coxeter_number())

    def test_coxeter_is_30(self):
        assert E8_COXETER == 30

    def test_coxeter_formula(self):
        assert E8_ROOTS // E8_RANK == E8_COXETER


class TestLocalGraphTower:
    def test_local_graph_tower(self):
        _assert_ok(verify_local_graph_tower())

    def test_4_21_local_is_3_21(self):
        # Each vertex of 4₂₁ (240 verts) has 56 neighbours = P_3_21
        assert P_3_21 == GEWIRTZ_V == 56

    def test_3_21_local_is_Schlafli(self):
        # Each vertex of 3₂₁ (56 verts) has 27 neighbours = P_2_21 = Schläfli
        assert P_2_21 == LINES_27 == 27


class TestGossetEdges:
    def test_gosset_edges(self):
        _assert_ok(verify_gosset_edges())

    def test_2_21_edges_are_6cubed(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import EDGES_2_21
        assert EDGES_2_21 == 216 == 6 ** 3

    def test_3_21_edges_formula(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import EDGES_3_21
        assert EDGES_3_21 == P_3_21 * P_2_21 // 2 == 756

    def test_4_21_edges_formula(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import EDGES_4_21
        assert EDGES_4_21 == P_4_21 * P_3_21 // 2 == 6720


class TestGewirtzFormula:
    def test_gewirtz_V_formula(self):
        _assert_ok(verify_gewirtz_V_formula())

    def test_striking_identity(self):
        # GEWIRTZ_V = V + K + MU is a zero-parameter identity
        assert GEWIRTZ_V == V + K + MU == 40 + 12 + 4 == 56

    def test_gewirtz_equals_P_3_21(self):
        assert GEWIRTZ_V == P_3_21


class TestE6Data:
    def test_e6_data(self):
        _assert_ok(verify_e6_data())

    def test_e6_positive_roots_eq_double_sixes(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import E6_POSITIVE_ROOTS, NUM_DOUBLE_SIXES
        assert E6_POSITIVE_ROOTS == 36 == NUM_DOUBLE_SIXES


class TestE7Data:
    def test_e7_data(self):
        _assert_ok(verify_e7_data())

    def test_WE7_is_56_times_WE6(self):
        assert WE7_ORDER == 56 * WE6_ORDER == 56 * AUT_ORDER


class TestWE8Factorisation:
    def test_e8_we8_factorisation(self):
        _assert_ok(verify_e8_we8_factorisation())

    def test_WE8_factored(self):
        assert WE8_ORDER == (2 ** 14) * (3 ** 5) * (5 ** 2) * 7


class Test240Factorizations:
    def test_240_factorizations(self):
        _assert_ok(verify_240_factorizations())

    def test_240_is_VK_over2(self):
        assert 240 == V * K // 2

    def test_240_div_V_is_6(self):
        assert EDGES // V == 6


class TestTransport:
    def test_transport_via_gosset(self):
        _assert_ok(verify_transport_via_gosset())

    def test_transport_is_product(self):
        assert TRANSPORT_EDGES == P_2_21 * P_1_21 == 27 * 10 == 270

    def test_transport_eq_Qsq_coxeter(self):
        assert TRANSPORT_EDGES == Q ** 2 * E8_COXETER == 9 * 30


class TestWD5StabLine:
    def test_wd5_as_stab_line(self):
        _assert_ok(verify_wd5_as_stab_line())

    def test_WD5_equals_stab_line(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import STAB_LINE_WE6
        assert WD5_ORDER == STAB_LINE_WE6 == 1920


class TestThetaSeries:
    def test_e8_theta_series(self):
        _assert_ok(verify_e8_theta_series())

    def test_theta_a2_is_EDGES(self):
        assert 240 == EDGES

    def test_theta_ratio_a4_a2(self):
        assert 2160 // 240 == 9 == Q ** 2

    def test_theta_a4_is_AUT_div24(self):
        assert 2160 == AUT_ORDER // 24


class TestAmbientDimensions:
    def test_gosset_ambient_dimensions(self):
        _assert_ok(verify_gosset_ambient_dimensions())

    def test_4_21_in_R8(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import DIM_4_21
        assert DIM_4_21 == 8 == E8_RANK

    def test_DIM_4_21_eq_V_div5(self):
        from PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE import DIM_4_21
        assert DIM_4_21 == V // 5


class TestSchlaflInGosset:
    def test_schlafli_graph_in_gosset(self):
        _assert_ok(verify_schlafli_graph_in_gosset())


class TestKissingNumber:
    def test_e8_kissing_number(self):
        _assert_ok(verify_e8_kissing_number())

    def test_kissing_is_EDGES(self):
        assert 240 == EDGES == P_4_21


class TestRatioChain:
    def test_gosset_ratio_chain(self):
        _assert_ok(verify_gosset_ratio_chain())

    def test_tower_sum_is_333(self):
        assert P_1_21 + P_2_21 + P_3_21 + P_4_21 == 333

    def test_tower_product_12_is_transport(self):
        assert P_1_21 * P_2_21 == TRANSPORT_EDGES == 270


class TestAlgebraDimensions:
    def test_e6_e7_e8_dimensions(self):
        _assert_ok(verify_e6_e7_e8_dimensions())

    def test_E8_dim_248(self):
        assert E8_DIM == 248

    def test_E8_dim_is_EDGES_plus_rank(self):
        assert E8_DIM == EDGES + E8_RANK


class TestCombinatorialBatch:
    def test_combinatorial_batch(self):
        _assert_ok(verify_combinatorial_batch())


class TestTernaryGolay:
    def test_gosset_and_ternary_golay(self):
        _assert_ok(verify_gosset_and_ternary_golay())

    def test_golay3_length_is_K(self):
        assert 12 == K


class TestModularConnection:
    def test_e8_modular_connection(self):
        _assert_ok(verify_e8_modular_connection())

    def test_theta_weight_is_MU(self):
        assert 4 == MU  # weight of E₈ theta form = MU — novel W(3,3) link


class TestVertexMap:
    def test_gosset_to_w33_vertex_map(self):
        _assert_ok(verify_gosset_to_w33_vertex_map())

    def test_tower_sum_factorisation(self):
        total = P_1_21 + P_2_21 + P_3_21 + P_4_21
        assert total == 333 == Q ** 2 * 37

    def test_37_eq_V_minus_Q(self):
        assert 37 == V - Q


class TestMasterSummary:
    def test_all_checks_pass(self):
        summary = build_cclxxviii_bridge_summary()
        failures = [n for n, r in summary["check_results"].items() if not r["pass"]]
        assert summary["all_checks_pass"], f"Failed: {failures}"

    def test_total_checks_gte_42(self):
        summary = build_cclxxviii_bridge_summary()
        assert summary["total_checks"] >= 42

    def test_summary_constants(self):
        summary = build_cclxxviii_bridge_summary()
        c = summary["constants"]
        assert c["P_4_21"] == EDGES == 240
        assert c["P_3_21"] == GEWIRTZ_V == 56
        assert c["P_2_21"] == LINES_27 == 27
        assert c["P_1_21"] == PHI4 == 10

    def test_part_number(self):
        summary = build_cclxxviii_bridge_summary()
        assert summary["part"] == "CCLXXVIII"
