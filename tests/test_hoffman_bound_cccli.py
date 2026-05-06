"""Tests for PART CCCLI: Hoffman Bound and Maximum Independent Sets in W(3,3)."""
import sys
from pathlib import Path
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCLI_HOFFMAN_BOUND_BRIDGE import (
    V, K, LAM, MU, L, EDGES, R_EIG, S_EIG, ABS_S, MULT_R, MULT_S, MULT_0,
    ALPHA, SU5_ADJ, SU5_MATTER, GENERATIONS, GUT_DIM, EW_GAUGE_4,
    hoffman_bound, independence_number, hoffman_denominator,
    edges_between_coclique_and_complement, edges_seen_from_complement,
    verify_all, build_cccli_summary,
)


class TestSRGConstants:
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_LAM(self): assert LAM == 2
    def test_MU(self): assert MU == 4
    def test_EDGES(self): assert EDGES == 240
    def test_R_EIG(self): assert R_EIG == 2
    def test_S_EIG(self): assert S_EIG == -4
    def test_ABS_S(self): assert ABS_S == 4
    def test_MULT_R(self): assert MULT_R == 24
    def test_MULT_S(self): assert MULT_S == 15
    def test_MULT_0(self): assert MULT_0 == 1
    def test_multiplicity_sum(self): assert MULT_0 + MULT_R + MULT_S == V
    def test_edges_formula(self): assert EDGES == V * K // 2


class TestPhysicsConstants:
    def test_ALPHA(self): assert ALPHA == 10
    def test_SU5_ADJ(self): assert SU5_ADJ == 24
    def test_SU5_MATTER(self): assert SU5_MATTER == 15
    def test_GENERATIONS(self): assert GENERATIONS == 3
    def test_GUT_DIM(self): assert GUT_DIM == 27
    def test_EW_GAUGE_4(self): assert EW_GAUGE_4 == 4
    def test_SU5_ADJ_eq_MULT_R(self): assert SU5_ADJ == MULT_R
    def test_SU5_MATTER_eq_MULT_S(self): assert SU5_MATTER == MULT_S


class TestHoffmanBound:
    def test_abs_s_equals_4(self): assert ABS_S == 4
    def test_hoffman_denominator(self): assert hoffman_denominator() == K + ABS_S
    def test_hoffman_denominator_value(self): assert hoffman_denominator() == 16
    def test_hoffman_bound_exact(self): assert hoffman_bound() == Fraction(V * ABS_S, K + ABS_S)
    def test_hoffman_bound_equals_10(self): assert hoffman_bound() == Fraction(10)
    def test_hoffman_bound_is_integer(self): assert int(hoffman_bound()) == 10
    def test_hoffman_bound_formula(self):
        assert hoffman_bound() == Fraction(40 * 4, 12 + 4)
    def test_hoffman_denom_power_of_2(self): assert hoffman_denominator() == 2**4
    def test_hoffman_denom_eq_edges_over_mult_s(self): assert hoffman_denominator() == EDGES // MULT_S


class TestIndependenceNumber:
    def test_alpha_equals_10(self): assert independence_number() == 10
    def test_alpha_equals_ALPHA(self): assert independence_number() == ALPHA
    def test_alpha_equals_hoffman_tight(self): assert independence_number() == int(hoffman_bound())
    def test_alpha_leq_hoffman_bound(self): assert independence_number() <= int(hoffman_bound())
    def test_alpha_V_ratio(self): assert Fraction(independence_number(), V) == Fraction(1, 4)
    def test_alpha_ratio_eq_s_ratio(self):
        assert Fraction(independence_number(), V) == Fraction(ABS_S, K + ABS_S)


class TestCocliqueStructure:
    def test_edges_coclique_complement(self):
        assert edges_between_coclique_and_complement() == independence_number() * K
    def test_edges_coclique_complement_value(self):
        assert edges_between_coclique_and_complement() == 120
    def test_edges_from_complement(self):
        assert edges_seen_from_complement() == (V - independence_number()) * MU
    def test_edges_from_complement_value(self):
        assert edges_seen_from_complement() == 120
    def test_edge_count_consistent(self):
        assert edges_between_coclique_and_complement() == edges_seen_from_complement()
    def test_V_minus_alpha(self): assert V - independence_number() == 30
    def test_V_minus_alpha_eq_2_MULT_S(self): assert V - independence_number() == 2 * MULT_S
    def test_V_minus_alpha_eq_ALPHA_times_GENERATIONS(self):
        assert V - independence_number() == ALPHA * GENERATIONS
    def test_alpha_K_eq_5_SU5_ADJ(self): assert independence_number() * K == 5 * SU5_ADJ
    def test_V_over_alpha(self): assert V // independence_number() == 4
    def test_V_over_alpha_eq_MU(self): assert V // independence_number() == MU
    def test_V_over_alpha_eq_ABS_S(self): assert V // independence_number() == ABS_S


class TestPhysicsBridge:
    def test_alpha_eq_ALPHA(self): assert independence_number() == ALPHA
    def test_hoffman_denom_eq_2_to_4(self): assert hoffman_denominator() == 2**4
    def test_V_over_denom_times_4_eq_ALPHA(self):
        assert Fraction(V, hoffman_denominator()) * 4 == ALPHA
    def test_V_minus_alpha_30_eq_ALPHA_GENS(self):
        assert (V - independence_number()) == ALPHA * GENERATIONS
    def test_alpha_K_div_SU5_eq_5(self):
        assert independence_number() * K // SU5_ADJ == GENERATIONS + 2
    def test_K4_vertices_eq_V_over_alpha(self): assert V // independence_number() == 4
    def test_K4_vertices_eq_MU(self): assert V // independence_number() == MU
    def test_MULT_R_eq_SU5_ADJ_eq_24(self): assert MULT_R == SU5_ADJ == 24


class TestVerifyAll:
    def setup_method(self):
        self.checks, self.passed, self.total = verify_all()

    def test_total_is_27(self): assert self.total == 27
    def test_all_pass(self): assert self.passed == self.total
    def test_checks_list_length(self): assert len(self.checks) == 27
    def test_all_checks_passed(self):
        failed = [c for c in self.checks if not c["passed"]]
        assert failed == [], f"Failed: {[c['name'] for c in failed]}"
    def test_checks_have_name(self):
        for c in self.checks:
            assert "name" in c and c["name"]
    def test_checks_have_passed_field(self):
        for c in self.checks: assert "passed" in c


class TestSummary:
    def setup_method(self):
        self.s = build_cccli_summary()

    def test_part(self): assert self.s["part"] == "CCCLI"
    def test_status(self): assert self.s["status"] == "PASS"
    def test_checks_pass(self): assert self.s["checks_pass"] == 27
    def test_checks_total(self): assert self.s["checks_total"] == 27
    def test_independence_number(self): assert self.s["fields"]["independence_number"] == 10
    def test_hoffman_tight(self): assert self.s["fields"]["hoffman_tight"] is True
    def test_hoffman_bound_str(self): assert self.s["fields"]["hoffman_bound"] == "10"
    def test_discoveries_nonempty(self): assert len(self.s["discoveries"]) >= 3
    def test_title_contains_hoffman(self): assert "Hoffman" in self.s["title"]
