"""
Tests for Part CCLXXXVIII: Delsarte Bounds Bridge.

Covers: Delsarte LP bounds for the cometric W(3,3) scheme, the
dual-scheme independence number = 36 = quark count, the SM
fermion partition (36+4=40), Krein parameter ratios, and the
full verify_all() gate.
"""
import pytest
from fractions import Fraction

from exploration.PART_CCLXXXVIII_DELSARTE_BOUNDS_BRIDGE import (
    # Graph / scheme constants
    V, K, LAM, MU, Q, K2, MULT_R, MULT_S, EDGES, PHI4,
    # Krein array entries
    KREIN_B_STAR_0, KREIN_C_STAR_1, KREIN_B_STAR_1, KREIN_C_STAR_2,
    KREIN_Q0_11, KREIN_Q0_22,
    KREIN_Q1_11, KREIN_Q1_12, KREIN_Q1_22,
    KREIN_Q2_11, KREIN_Q2_12, KREIN_Q2_22,
    # Delsarte bounds
    ABSOLUTE_BOUND_COMETRIC,
    DUAL_EIGENVALUE_GAPS,
    DUAL_GAP_RATIO,
    DUAL_INDEPENDENCE_BOUND,
    # SM fermion partition
    QUARKS_36, EW_GAUGE_4, TOTAL_SM_40,
    IS_TIGHT_QUARK_SUBGRAPH, QUARK_BOSON_PARTITION_SIZE,
    # Krein-to-mass ratios
    MULT_RATIO, RATIO_Q1_Q0_11, RATIO_Q2_Q1_11, NUM_GENERATIONS,
    # Functions
    eberlein_polynomial,
    verify_delsarte_structure,
    verify_krein_to_mass_connection,
    verify_all,
    build_cclxxxviii_summary,
)


# ─── W(3,3) scheme sanity ────────────────────────────────────────────────────

class TestSchemeConstants:
    def test_vertex_count(self):
        assert V == 40

    def test_valency(self):
        assert K == 12

    def test_lambda(self):
        assert LAM == 2

    def test_mu(self):
        assert MU == 4

    def test_field_order(self):
        assert Q == 3

    def test_second_valency(self):
        assert K2 == 27

    def test_mult_r(self):
        assert MULT_R == 24

    def test_mult_s(self):
        assert MULT_S == 15

    def test_edges(self):
        assert EDGES == 240

    def test_edges_formula(self):
        assert EDGES == V * K // 2


# ─── Krein array ──────────────────────────────────────────────────────────────

class TestKreinArray:
    def test_b_star_0(self):
        assert KREIN_B_STAR_0 == 24

    def test_b_star_0_eq_mult_r(self):
        assert KREIN_B_STAR_0 == MULT_R

    def test_c_star_1(self):
        assert KREIN_C_STAR_1 == 1

    def test_b_star_1(self):
        assert KREIN_B_STAR_1 == Fraction(65, 3)

    def test_c_star_2(self):
        assert KREIN_C_STAR_2 == 15

    def test_c_star_2_eq_mult_s(self):
        assert KREIN_C_STAR_2 == MULT_S

    def test_krein_array_fractions_exact(self):
        """Krein array entries are exact fractions."""
        assert isinstance(KREIN_B_STAR_1, Fraction)
        # b*_1 - c*_2 = 65/3 - 15 = 20/3
        diff = KREIN_B_STAR_1 - KREIN_C_STAR_2
        assert diff == Fraction(20, 3)

    def test_krein_q0_11(self):
        assert KREIN_Q0_11 == Fraction(24)

    def test_krein_q0_22(self):
        assert KREIN_Q0_22 == Fraction(15)

    def test_krein_q1_11(self):
        assert KREIN_Q1_11 == Fraction(44, 3)

    def test_krein_q1_12(self):
        assert KREIN_Q1_12 == Fraction(25, 3)

    def test_krein_q1_22(self):
        assert KREIN_Q1_22 == Fraction(20, 3)

    def test_krein_q2_11(self):
        assert KREIN_Q2_11 == Fraction(40, 3)

    def test_krein_q2_12(self):
        assert KREIN_Q2_12 == Fraction(32, 3)

    def test_krein_q2_22(self):
        assert KREIN_Q2_22 == Fraction(10, 3)

    def test_krein_q1_denominator_is_q(self):
        """All Q1 Krein parameters have denominator Q = 3."""
        for kp in [KREIN_Q1_11, KREIN_Q1_12, KREIN_Q1_22]:
            assert kp.denominator == Q

    def test_krein_q2_denominator_is_q(self):
        """All Q2 Krein parameters have denominator Q = 3."""
        for kp in [KREIN_Q2_11, KREIN_Q2_12, KREIN_Q2_22]:
            assert kp.denominator == Q


# ─── Delsarte LP bounds ───────────────────────────────────────────────────────

class TestDelsarteBounds:
    def test_absolute_bound_value(self):
        assert ABSOLUTE_BOUND_COMETRIC == 325

    def test_absolute_bound_formula(self):
        assert ABSOLUTE_BOUND_COMETRIC == (MULT_R + 1) * (MULT_R + 2) // 2

    def test_dual_gap_large(self):
        """First eigenvalue gap: theta*_0 - theta*_1 = 24 - 4 = 20."""
        assert DUAL_EIGENVALUE_GAPS[0] == 20

    def test_dual_gap_small(self):
        """Second gap: theta*_1 - theta*_2 = 4 - (-8/3) = 20/3."""
        assert DUAL_EIGENVALUE_GAPS[1] == Fraction(20, 3)

    def test_dual_gap_ratio(self):
        """Ratio of eigenvalue gaps = Q = 3 (field order)."""
        assert DUAL_GAP_RATIO == Q

    def test_dual_gap_ratio_is_integer(self):
        assert int(DUAL_GAP_RATIO) == 3

    def test_dual_independence_bound(self):
        """The dual-scheme Delsarte independence bound is 36."""
        assert DUAL_INDEPENDENCE_BOUND == 36

    def test_dual_independence_bound_equals_quarks(self):
        """The bound matches exactly the SM quark count."""
        assert DUAL_INDEPENDENCE_BOUND == QUARKS_36


# ─── SM fermion partition ─────────────────────────────────────────────────────

class TestSMFermionPartition:
    def test_quarks_36(self):
        assert QUARKS_36 == 36

    def test_ew_gauge_4(self):
        assert EW_GAUGE_4 == 4

    def test_total_sm_40(self):
        assert TOTAL_SM_40 == 40

    def test_total_sm_equals_v(self):
        assert TOTAL_SM_40 == V

    def test_quarks_plus_gauge_equals_v(self):
        assert QUARKS_36 + EW_GAUGE_4 == V

    def test_quark_boson_partition(self):
        assert QUARK_BOSON_PARTITION_SIZE == V

    def test_tight_quark_subgraph(self):
        """The quark subgraph IS tight: its count = Delsarte bound."""
        assert IS_TIGHT_QUARK_SUBGRAPH is True

    def test_quarks_match_dual_bound(self):
        assert QUARKS_36 == DUAL_INDEPENDENCE_BOUND

    def test_ew_gauge_eq_mu(self):
        """Number of EW gauge bosons equals MU (co-neighbourhood size)."""
        assert EW_GAUGE_4 == MU

    def test_phi4_independence_number(self):
        """PHI4 = 10 = Hoffman independence number of the original W(3,3) graph."""
        assert PHI4 == 10


# ─── Krein-to-mass connection ─────────────────────────────────────────────────

class TestKreinToMassConnection:
    def test_mult_ratio(self):
        assert MULT_RATIO == Fraction(8, 5)

    def test_mult_ratio_numerator(self):
        assert MULT_RATIO == Fraction(MULT_R, MULT_S)

    def test_q1_q0_ratio(self):
        assert RATIO_Q1_Q0_11 == Fraction(11, 18)

    def test_q2_q1_ratio(self):
        assert RATIO_Q2_Q1_11 == Fraction(10, 11)

    def test_num_generations(self):
        assert NUM_GENERATIONS == 3

    def test_num_generations_eq_q(self):
        """The number of SM generations equals the field order Q."""
        assert NUM_GENERATIONS == Q


# ─── Eberlein polynomial ──────────────────────────────────────────────────────

class TestEberleinPolynomial:
    def test_e0_at_all_eigenvalues(self):
        """E_0(x) = 1 for all x (zeroth polynomial is constant)."""
        for i in range(3):
            assert eberlein_polynomial(j=0, x=i) == Fraction(1)

    def test_e1_at_eigenvalue_0(self):
        """E_1(theta*_0) = Q-matrix[0][1] = 24."""
        assert eberlein_polynomial(j=1, x=0) == Fraction(24)

    def test_e1_at_eigenvalue_1(self):
        """E_1(theta*_1) = Q-matrix[1][1] = 4."""
        assert eberlein_polynomial(j=1, x=1) == Fraction(4)

    def test_e1_at_eigenvalue_2(self):
        """E_1(theta*_2) = Q-matrix[2][1] = -8/3."""
        assert eberlein_polynomial(j=1, x=2) == Fraction(-8, 3)

    def test_e2_at_eigenvalue_0(self):
        """E_2(theta*_0) = Q-matrix[0][2] = 15."""
        assert eberlein_polynomial(j=2, x=0) == Fraction(15)

    def test_e2_at_eigenvalue_1(self):
        """E_2(theta*_1) = Q-matrix[1][2] = -5."""
        assert eberlein_polynomial(j=2, x=1) == Fraction(-5)

    def test_e2_at_eigenvalue_2(self):
        """E_2(theta*_2) = Q-matrix[2][2] = 5/3."""
        assert eberlein_polynomial(j=2, x=2) == Fraction(5, 3)

    def test_invalid_x_returns_none(self):
        assert eberlein_polynomial(j=1, x=5) is None


# ─── verify_* functions ───────────────────────────────────────────────────────

class TestVerifyFunctions:
    def test_verify_delsarte_structure_all_true(self):
        result = verify_delsarte_structure()
        assert all(result.values()), f"Failed keys: {[k for k,v in result.items() if not v]}"

    def test_verify_delsarte_structure_keys(self):
        result = verify_delsarte_structure()
        expected_keys = {
            "absolute_bound_325",
            "dual_gap_ratio_eq_q",
            "dual_independence_bound_36",
            "quarks_match_bound",
            "total_vertices_40",
            "quark_boson_partition",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_verify_krein_to_mass_connection_all_true(self):
        result = verify_krein_to_mass_connection()
        assert all(result.values()), f"Failed keys: {[k for k,v in result.items() if not v]}"

    def test_verify_krein_to_mass_connection_keys(self):
        result = verify_krein_to_mass_connection()
        expected_keys = {
            "mult_ratio_8_5",
            "q1_11_ratio_ok",
            "q2_11_ratio_ok",
            "num_generations_3",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_verify_all_all_true(self):
        result = verify_all()
        assert all(result.values()), f"Failed keys: {[k for k,v in result.items() if not v]}"

    def test_verify_all_has_ten_checks(self):
        result = verify_all()
        assert len(result) == 10

    def test_verify_all_superset_of_sub_verifies(self):
        all_result = verify_all()
        delsarte = verify_delsarte_structure()
        mass = verify_krein_to_mass_connection()
        for k in delsarte:
            assert k in all_result
        for k in mass:
            assert k in all_result


# ─── build_cclxxxviii_summary ─────────────────────────────────────────────────

class TestBuildSummary:
    def setup_method(self):
        self.summary = build_cclxxxviii_summary()

    def test_part_number(self):
        assert self.summary["part_number"] == "CCLXXXVIII"

    def test_title_contains_delsarte(self):
        assert "Delsarte" in self.summary["title"]

    def test_verification_status_pass(self):
        assert self.summary["verification_status"] == "ALL CHECKS PASS"

    def test_delsarte_bounds_section(self):
        bounds = self.summary["delsarte_bounds"]
        assert bounds["dual_independence_bound"] == "36"
        assert bounds["absolute_bound"] == "325"

    def test_sm_partition_section(self):
        part = self.summary["sm_partition"]
        assert part["quarks"] == 36
        assert part["ew_gauge"] == 4
        assert part["total"] == 40
        assert part["matches_bound"] is True

    def test_krein_array_ratios_section(self):
        ratios = self.summary["krein_array_ratios"]
        assert "8/5" in ratios["mult_r_over_mult_s"]

    def test_key_discoveries_not_empty(self):
        assert len(self.summary["key_discoveries"]) > 0

    def test_connections_not_empty(self):
        assert len(self.summary["connections"]) > 0

    def test_quark_count_discovery_mentioned(self):
        discoveries = " ".join(self.summary["key_discoveries"])
        assert "36" in discoveries

    def test_q_field_order_in_connections(self):
        connections = " ".join(self.summary["connections"])
        # Q=3 should appear somewhere
        assert "3" in connections
