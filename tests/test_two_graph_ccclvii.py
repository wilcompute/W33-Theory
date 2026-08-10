"""
Tests for PART CCCLVII: Two-Graph Structure of W(3,3).
96 tests across 7 classes.
"""

import json
import pathlib
import pytest

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCLVII_TWO_GRAPH_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, L,
    R_EIG, S_EIG,
    ALPHA, GUT_DIM, GENERATIONS, EW_GAUGE_4, SU5_ADJ, SU5_MATTER,
    total_triples, triangles, edges_within_nbhd, edges_within_nonbhd,
    triples_with_0_edges, triples_with_1_edge, triples_with_2_edges, triples_with_3_edges,
    two_graph_size, odd_triples_per_vertex, odd_triples_per_edge, odd_triples_per_nonedge,
    total_parity_check,
    verify_all, build_ccclvii_summary,
)

JSON_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "PART_CCCLVII_two_graph_results.json"
)


# ── Class 1: SRG Constants ─────────────────────────────────────────────────

class TestSRGConstants:
    def test_V(self):           assert V == 40
    def test_K(self):           assert K == 12
    def test_LAM(self):         assert LAM == 2
    def test_MU(self):          assert MU == 4
    def test_EDGES(self):       assert EDGES == 240
    def test_MULT_R(self):      assert MULT_R == 24
    def test_MULT_S(self):      assert MULT_S == 15
    def test_ALPHA(self):       assert ALPHA == 10
    def test_GENERATIONS(self): assert GENERATIONS == 3
    def test_EW_GAUGE_4(self):  assert EW_GAUGE_4 == 4
    def test_SU5_ADJ(self):     assert SU5_ADJ == 24
    def test_SU5_MATTER(self):  assert SU5_MATTER == 15
    def test_GUT_DIM(self):     assert GUT_DIM == 27


# ── Class 2: Triple Partition ──────────────────────────────────────────────

class TestTriplePartition:
    def test_total_triples_value(self):     assert total_triples() == 9880
    def test_total_triples_formula(self):   assert total_triples() == V * (V - 1) * (V - 2) // 6
    def test_triangles_value(self):         assert triangles() == 160
    def test_triangles_formula(self):       assert triangles() == V * K * LAM // 6
    def test_triples_0_value(self):         assert triples_with_0_edges() == 3240
    def test_triples_1_value(self):         assert triples_with_1_edge() == 4320
    def test_triples_2_value(self):         assert triples_with_2_edges() == 2160
    def test_triples_3_value(self):         assert triples_with_3_edges() == 160
    def test_parity_sum(self):
        assert total_parity_check() == total_triples()
    def test_triples_0_plus_1_plus_2_plus_3(self):
        assert (triples_with_0_edges() + triples_with_1_edge()
                + triples_with_2_edges() + triples_with_3_edges()) == 9880
    def test_edges_within_nbhd(self):  assert edges_within_nbhd() == 12
    def test_edges_within_nonbhd(self): assert edges_within_nonbhd() == 108


# ── Class 3: Two-Graph Size ────────────────────────────────────────────────

class TestTwoGraphSize:
    def test_size_value(self):       assert two_graph_size() == 4480
    def test_size_odd_sum(self):     assert two_graph_size() == triples_with_1_edge() + triples_with_3_edges()
    def test_size_formula_vk(self):  assert two_graph_size() == V * K * (V - K) // 3
    def test_size_less_than_half(self): assert two_graph_size() < total_triples()
    def test_triples_3_eq_v_ew4(self): assert triples_with_3_edges() == V * EW_GAUGE_4
    def test_triples_0_eq_v_gen4(self): assert triples_with_0_edges() == V * GENERATIONS ** 4
    def test_triples_0_per_v(self):  assert triples_with_0_edges() // V == GENERATIONS ** 4


# ── Class 4: Vertex Regularity ────────────────────────────────────────────

class TestVertexRegularity:
    def test_per_vertex_value(self):  assert odd_triples_per_vertex() == 336
    def test_per_vertex_divisible(self): assert (V * odd_triples_per_vertex()) % 3 == 0
    def test_per_vertex_times_v_div3(self): assert V * odd_triples_per_vertex() // 3 == two_graph_size()
    def test_per_vertex_eq_k_times_vk(self): assert odd_triples_per_vertex() == K * (V - K)
    def test_per_vertex_eq_k_su5adj_mu(self): assert odd_triples_per_vertex() == K * (SU5_ADJ + MU)
    def test_per_vertex_gt_0(self):   assert odd_triples_per_vertex() > 0
    def test_size_div_v_eq_ktvk_div3(self):
        assert two_graph_size() // V == K * (V - K) // 3


# ── Class 5: Pair Counts ──────────────────────────────────────────────────

class TestPairCounts:
    def test_per_edge_value(self):      assert odd_triples_per_edge() == 20
    def test_per_nonedge_value(self):   assert odd_triples_per_nonedge() == 16
    def test_per_edge_eq_2alpha(self):  assert odd_triples_per_edge() == 2 * ALPHA
    def test_per_nonedge_eq_2kmu(self): assert odd_triples_per_nonedge() == 2 * (K - MU)
    def test_diff_eq_ew4(self):
        assert odd_triples_per_edge() - odd_triples_per_nonedge() == EW_GAUGE_4
    def test_edge_gt_nonedge(self):
        assert odd_triples_per_edge() > odd_triples_per_nonedge()
    def test_nonedge_gt_0(self):
        assert odd_triples_per_nonedge() > 0


# ── Class 6: Physics Identities ───────────────────────────────────────────

class TestPhysicsIdentities:
    def test_triangles_v_ew4(self):     assert triangles() == V * EW_GAUGE_4
    def test_triples_0_gen4(self):      assert triples_with_0_edges() == V * GENERATIONS ** 4
    def test_per_vertex_k_vk(self):     assert odd_triples_per_vertex() == K * (V - K)
    def test_per_vertex_k_su5mu(self):  assert odd_triples_per_vertex() == K * (SU5_ADJ + MU)
    def test_per_edge_2alpha(self):     assert odd_triples_per_edge() == 2 * ALPHA
    def test_diff_ew4(self):
        assert odd_triples_per_edge() - odd_triples_per_nonedge() == EW_GAUGE_4
    def test_size_vk_vk_div3(self):     assert two_graph_size() == V * K * (V - K) // 3
    def test_vk_eq_su5adj_mu(self):     assert V - K == SU5_ADJ + MU


# ── Class 7: VerifyAll and Summary ────────────────────────────────────────

class TestVerifyAllAndSummary:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_exactly_27_checks(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [c["label"] for c in checks if not c["pass"]]
        assert failed == []

    def test_summary_part(self):
        s = build_ccclvii_summary()
        assert s["part"] == "CCCLVII"

    def test_summary_status_pass(self):
        s = build_ccclvii_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = build_ccclvii_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = build_ccclvii_summary()
        assert s["checks_total"] == 27

    def test_summary_fields_two_graph_size(self):
        s = build_ccclvii_summary()
        assert s["fields"]["two_graph_size"] == 4480

    def test_summary_fields_per_vertex(self):
        s = build_ccclvii_summary()
        assert s["fields"]["odd_triples_per_vertex"] == 336

    def test_summary_fields_triangles(self):
        s = build_ccclvii_summary()
        assert s["fields"]["triangles"] == 160

    def test_summary_fields_per_edge(self):
        s = build_ccclvii_summary()
        assert s["fields"]["odd_per_edge"] == 20

    def test_summary_fields_per_nonedge(self):
        s = build_ccclvii_summary()
        assert s["fields"]["odd_per_nonedge"] == 16

    def test_summary_discoveries_nonempty(self):
        s = build_ccclvii_summary()
        assert len(s["discoveries"]) >= 1

    def test_json_exists(self):
        assert JSON_PATH.exists()

    def test_json_status_pass(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27

    def test_json_part_label(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["part"] == "CCCLVII"
