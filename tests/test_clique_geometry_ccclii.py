"""Tests for PART CCCLII: Clique Geometry and Maximum Cliques in W(3,3)."""
import sys
from pathlib import Path
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCLII_CLIQUE_GEOMETRY_BRIDGE import (
    V, K, LAM, MU, L, EDGES, R_EIG, S_EIG, ABS_S, MULT_R, MULT_S, MULT_0,
    ALPHA, SU5_ADJ, SU5_MATTER, GENERATIONS, GUT_DIM, EW_GAUGE_4,
    clique_eigenvalue_bound, clique_number, edges_in_clique, clique_count,
    triangles_count, triangle_K4_incidence, clique_triangles,
    verify_all, build_ccclii_summary,
)


class TestSRGConstants:
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_LAM(self): assert LAM == 2
    def test_MU(self): assert MU == 4
    def test_EDGES(self): assert EDGES == 240
    def test_ABS_S(self): assert ABS_S == 4
    def test_MULT_R(self): assert MULT_R == 24
    def test_MULT_S(self): assert MULT_S == 15
    def test_multiplicity_sum(self): assert MULT_0 + MULT_R + MULT_S == V
    def test_edges_formula(self): assert EDGES == V * K // 2


class TestPhysicsConstants:
    def test_ALPHA(self): assert ALPHA == 10
    def test_SU5_ADJ_eq_MULT_R(self): assert SU5_ADJ == MULT_R
    def test_GENERATIONS(self): assert GENERATIONS == 3
    def test_EW_GAUGE_4(self): assert EW_GAUGE_4 == 4


class TestCliqueBound:
    def test_eigenvalue_bound_formula(self):
        assert clique_eigenvalue_bound() == Fraction(1) + Fraction(K, ABS_S)
    def test_eigenvalue_bound_value(self):
        assert clique_eigenvalue_bound() == Fraction(4)
    def test_clique_number(self): assert clique_number() == 4
    def test_clique_number_tight(self): assert clique_number() == int(clique_eigenvalue_bound())
    def test_omega_eq_MU(self): assert clique_number() == MU
    def test_omega_eq_ABS_S(self): assert clique_number() == ABS_S
    def test_omega_eq_EW_GAUGE_4(self): assert clique_number() == EW_GAUGE_4
    def test_omega_eq_V_div_ALPHA(self): assert clique_number() == V // ALPHA


class TestK4Structure:
    def test_edges_in_clique(self): assert edges_in_clique() == 6
    def test_edges_in_clique_formula(self): assert edges_in_clique(4) == 4 * 3 // 2
    def test_K4_count(self): assert clique_count() == 40
    def test_K4_count_eq_V(self): assert clique_count() == V
    def test_K4_edges_cover(self): assert clique_count() * edges_in_clique() == EDGES
    def test_K4_count_eq_EDGES_div_6(self): assert clique_count() == EDGES // 6
    def test_K4_triangles(self): assert clique_triangles() == 4
    def test_K4_triangles_eq_omega(self): assert clique_triangles() == clique_number()
    def test_K4_triangles_eq_MU(self): assert clique_triangles() == MU


class TestTriangles:
    def test_triangle_count(self): assert triangles_count() == 160
    def test_triangle_formula(self): assert triangles_count() == V * K * LAM // 6
    def test_triangle_K4_incidence(self): assert triangle_K4_incidence() == clique_count() * 4
    def test_triangle_K4_eq_T(self): assert triangle_K4_incidence() == triangles_count()
    def test_T_per_K4(self): assert triangles_count() // clique_count() == clique_triangles()
    def test_T_eq_V_MU(self): assert triangles_count() == V * MU
    def test_T_eq_EDGES_LAM_div_3(self): assert triangles_count() == EDGES * LAM // 3


class TestProductIdentities:
    def test_omega_times_alpha_eq_V(self): assert clique_number() * ALPHA == V
    def test_omega_times_alpha(self): assert clique_number() * 10 == 40
    def test_K_div_omega_eq_GENERATIONS(self): assert K // clique_number() == GENERATIONS
    def test_MULT_R_div_omega_eq_edges_K4(self): assert MULT_R // clique_number() == edges_in_clique()
    def test_K4_count_div_omega_eq_ALPHA(self): assert clique_count() // clique_number() == ALPHA
    def test_LAM_T_identity(self): assert LAM * triangles_count() == V * K * LAM * LAM // 6


class TestVerifyAll:
    def setup_method(self):
        self.checks, self.passed, self.total = verify_all()

    def test_total_is_27(self): assert self.total == 27
    def test_all_pass(self): assert self.passed == self.total
    def test_checks_list_length(self): assert len(self.checks) == 27
    def test_all_checks_passed(self):
        failed = [c for c in self.checks if not c["passed"]]
        assert failed == [], f"Failed: {[c['name'] for c in failed]}"


class TestSummary:
    def setup_method(self):
        self.s = build_ccclii_summary()

    def test_part(self): assert self.s["part"] == "CCCLII"
    def test_status(self): assert self.s["status"] == "PASS"
    def test_checks_pass(self): assert self.s["checks_pass"] == 27
    def test_checks_total(self): assert self.s["checks_total"] == 27
    def test_clique_number(self): assert self.s["fields"]["clique_number"] == 4
    def test_K4_count(self): assert self.s["fields"]["K4_count"] == 40
    def test_num_triangles(self): assert self.s["fields"]["num_triangles"] == 160
    def test_discoveries_nonempty(self): assert len(self.s["discoveries"]) >= 3
    def test_title_contains_clique(self): assert "Clique" in self.s["title"]
