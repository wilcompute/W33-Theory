"""
Tests for PART CCCL: Spectral Moments and Walk Counting in W(3,3).
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCL_SPECTRAL_MOMENTS_BRIDGE import (
    V, K, LAM, MU, L, EDGES, R_EIG, S_EIG, MULT_R, MULT_S, MULT_0,
    GLUON_COUNT, EW_GAUGE_4, TOTAL_GAUGE, GENERATIONS, GUT_DIM, ALPHA,
    SU5_ADJ, SU5_MATTER, K4_FLAGS, S4_ORDER, TORUS_MAP_FACES,
    moment, num_triangles, num_triangles_direct, closed_walks_per_vertex,
    verify_all, build_cccl_summary,
)

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# TestConstants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_V(self):            assert V == 40
    def test_K(self):            assert K == 12
    def test_LAM(self):          assert LAM == 2
    def test_MU(self):           assert MU == 4
    def test_L(self):            assert L == 27
    def test_EDGES(self):        assert EDGES == 240
    def test_R_EIG(self):        assert R_EIG == 2
    def test_S_EIG(self):        assert S_EIG == -4
    def test_MULT_R(self):       assert MULT_R == 24
    def test_MULT_S(self):       assert MULT_S == 15
    def test_MULT_0(self):       assert MULT_0 == 1
    def test_multiplicity_sum(self):
        assert MULT_0 + MULT_R + MULT_S == V
    def test_SU5_ADJ(self):      assert SU5_ADJ == 24
    def test_SU5_MATTER(self):   assert SU5_MATTER == 15
    def test_ALPHA(self):        assert ALPHA == 10
    def test_TOTAL_GAUGE(self):  assert TOTAL_GAUGE == K
    def test_GUT_DIM(self):      assert GUT_DIM == L


# ---------------------------------------------------------------------------
# TestK4Flags
# ---------------------------------------------------------------------------

class TestK4Flags:
    def test_k4_flags_value(self):
        assert K4_FLAGS == 24
    def test_k4_flags_equals_mult_r(self):
        assert K4_FLAGS == MULT_R
    def test_k4_flags_equals_su5_adj(self):
        assert K4_FLAGS == SU5_ADJ
    def test_s4_order(self):
        assert S4_ORDER == 24
    def test_s4_order_factorial(self):
        import math
        assert S4_ORDER == math.factorial(4)
    def test_torus_map_faces(self):
        assert TORUS_MAP_FACES == 24
    def test_all_three_equal(self):
        assert K4_FLAGS == S4_ORDER == TORUS_MAP_FACES == 24


# ---------------------------------------------------------------------------
# TestMoments
# ---------------------------------------------------------------------------

class TestMoments:
    def test_mu_0(self):
        assert moment(0) == 40
    def test_mu_0_equals_V(self):
        assert moment(0) == V
    def test_mu_1(self):
        assert moment(1) == 0
    def test_mu_2(self):
        assert moment(2) == 480
    def test_mu_2_equals_VK(self):
        assert moment(2) == V * K
    def test_mu_2_equals_2_edges(self):
        assert moment(2) == 2 * EDGES
    def test_mu_3(self):
        assert moment(3) == 960
    def test_mu_3_equals_VKlam(self):
        assert moment(3) == V * K * LAM
    def test_mu_4(self):
        assert moment(4) == 24960
    def test_mu_4_exact(self):
        expected = MULT_0 * K**4 + MULT_R * R_EIG**4 + MULT_S * S_EIG**4
        assert moment(4) == expected
    def test_moment_formula_ell_5(self):
        expected = MULT_0 * K**5 + MULT_R * R_EIG**5 + MULT_S * S_EIG**5
        assert moment(5) == expected


# ---------------------------------------------------------------------------
# TestNormalized
# ---------------------------------------------------------------------------

class TestNormalized:
    def test_mu2_over_mu0_equals_K(self):
        assert Fraction(moment(2), moment(0)) == Fraction(K)
    def test_mu3_over_V_equals_KLam(self):
        assert moment(3) // V == K * LAM
    def test_mu3_over_V_equals_SU5_ADJ(self):
        assert moment(3) // V == SU5_ADJ
    def test_mu3_over_V_equals_MULT_R(self):
        assert moment(3) // V == MULT_R
    def test_closed_walks_per_vertex_2(self):
        assert closed_walks_per_vertex(2) == Fraction(K)
    def test_closed_walks_per_vertex_3(self):
        assert closed_walks_per_vertex(3) == Fraction(K * LAM)
    def test_mu4_over_mu2(self):
        assert moment(4) // moment(2) == V + K


# ---------------------------------------------------------------------------
# TestTriangles
# ---------------------------------------------------------------------------

class TestTriangles:
    def test_triangles_formula(self):
        assert num_triangles() == num_triangles_direct()
    def test_triangles_value(self):
        assert num_triangles() == 160
    def test_triangles_from_mu3(self):
        assert moment(3) // 6 == 160
    def test_triangles_VKlam6(self):
        assert V * K * LAM // 6 == 160
    def test_mu1_plus_mu3(self):
        assert moment(1) + moment(3) == V * K * LAM


# ---------------------------------------------------------------------------
# TestPhysics
# ---------------------------------------------------------------------------

class TestPhysics:
    def test_EDGES_over_ALPHA(self):
        assert EDGES // ALPHA == SU5_ADJ
    def test_mu2_half_edges(self):
        assert moment(2) // 2 == EDGES
    def test_mu3_over_MULT_R(self):
        assert moment(3) // MULT_R == V * K * LAM // MULT_R
    def test_mu4_mu2_ratio(self):
        assert moment(4) // moment(2) == V + K
    def test_VplusK(self):
        assert V + K == 52
    def test_sum_mod_V(self):
        total = sum(moment(i) for i in range(5))
        assert total % V == 0
    def test_mathieu_24_equals_MULT_R(self):
        # M24 acts on 24 points = MULT_R
        M24_POINTS = 24
        assert M24_POINTS == MULT_R
    def test_mathieu_12_equals_K(self):
        # M12 acts on 12 points = K
        M12_POINTS = 12
        assert M12_POINTS == K
    def test_24_is_2K(self):
        assert MULT_R == 2 * K


# ---------------------------------------------------------------------------
# TestVerifyAll
# ---------------------------------------------------------------------------

class TestVerifyAll:
    def setup_method(self):
        self.checks, self.passed, self.total = verify_all()

    def test_total_checks(self):
        assert self.total == 27
    def test_all_pass(self):
        assert self.passed == 27
    def test_no_failures(self):
        failures = [c["name"] for c in self.checks if not c["passed"]]
        assert failures == []
    def test_checks_list_length(self):
        assert len(self.checks) == 27


# ---------------------------------------------------------------------------
# TestSummary
# ---------------------------------------------------------------------------

class TestSummary:
    def setup_method(self):
        self.s = build_cccl_summary()

    def test_part(self):
        assert self.s["part"] == "CCCL"
    def test_status(self):
        assert self.s["status"] == "PASS"
    def test_checks_pass(self):
        assert self.s["checks_pass"] == 27
    def test_checks_total(self):
        assert self.s["checks_total"] == 27
    def test_fields_present(self):
        for key in ("mu_0", "mu_1", "mu_2", "mu_3", "mu_4",
                    "num_triangles", "closed_walks_per_vertex_2",
                    "closed_walks_per_vertex_3"):
            assert key in self.s["fields"]
    def test_mu_values_in_fields(self):
        f = self.s["fields"]
        assert f["mu_0"] == 40
        assert f["mu_1"] == 0
        assert f["mu_2"] == 480
        assert f["mu_3"] == 960
        assert f["mu_4"] == 24960
    def test_triangle_in_fields(self):
        assert self.s["fields"]["num_triangles"] == 160
    def test_discoveries_nonempty(self):
        assert len(self.s["discoveries"]) > 0
    def test_json_file_exists(self):
        p = ROOT / "PART_CCCL_spectral_moments_results.json"
        assert p.exists()
    def test_json_parseable(self):
        p = ROOT / "PART_CCCL_spectral_moments_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["part"] == "CCCL"
        assert data["status"] == "PASS"
