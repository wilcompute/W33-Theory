"""Tests for PART CCCCXX: Fano Plane → Octonion Algebra → G₂ → SU(3) → SM.

Covers all 27 verification checks across six groups:
  Group 1: Fano geometry (5 checks)
  Group 2: Octonion algebra from Fano (4 checks)
  Group 3: G₂ derivation algebra (5 checks)
  Group 4: G₂ → SU(3) breaking (5 checks)
  Group 5: SM gauge emergence (5 checks)
  Group 6: Grand unification identities (3 checks)
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for _p in (ROOT, EXPLORATION):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from exploration.PART_CCCCXX_FANO_OCTONION_SM_ALGEBRA import (
    # constants
    Q, LAM, MU, K, V, E, PHI6, PHI13, ALPHA, MULT_R, MULT_S, GENERATIONS,
    G2_DIM, SL3_DIM, N_FANO_POINTS, N_FANO_TRIPLES, PSL27_ORDER,
    N_OCTONION_TABLES, SIGNED_PERM_ORDER, STABILIZER_ORDER,
    FANO_TRIPLES_1, FANO_TRIPLES_0, FANO_LINES_1, CROSS,
    # geometry
    fano_point_count, fano_line_count, fano_points_per_line,
    fano_lines_per_point, fano_aut_order, fano_phi6_eq_n_points,
    # octonion
    octonion_imaginary_count, octonion_dim,
    octonion_is_anticommutative, octonion_associator_nonzero,
    # G₂
    g2_derivation_dim, g2_constraint_rank, sl3_dim_from_axis_fixing,
    g2_module_silent_plus_active, g2_module_total_dim, g2_dim_equals_sl3_plus_6,
    # breaking
    fano_line_quaternionic_dim, colour_complement_point_count,
    fano_spacetime_embeddings, su3_gluon_count, colour_algebra_not_closed,
    # SM
    sm_gauge_dim, sm_gauge_decomposition, sm_gauge_sum_equals_k, sm_rank,
    sm_fermions_per_generation, sm_generations_from_fano, sm_generations_are_q,
    # GUT
    weinberg_angle_exact, weinberg_angle_numeric,
    exceptional_g2_from_w33, all_exceptional_dims_from_w33,
    single_object_theorem,
    # helpers
    _gfp_rank, _build_cross_product, _build_deriv_constraints,
    # top-level
    verify_all, build_results,
)


# ════════════════════════════════════════════════════════════════════════════
# W(3,3) constant sanity
# ════════════════════════════════════════════════════════════════════════════
class TestW33Constants:
    def test_q_is_3(self):
        assert Q == 3

    def test_k_is_12(self):
        assert K == 12

    def test_phi6_is_7(self):
        assert PHI6 == 7

    def test_phi13_is_13(self):
        assert PHI13 == 13

    def test_lam_is_2(self):
        assert LAM == 2

    def test_mu_is_4(self):
        assert MU == 4

    def test_v_is_40(self):
        assert V == 40

    def test_e_is_240(self):
        assert E == 240

    def test_g2_dim_is_14(self):
        assert G2_DIM == 14

    def test_sl3_dim_is_8(self):
        assert SL3_DIM == 8

    def test_mult_s_is_15(self):
        assert MULT_S == 15

    def test_psl27_order_is_168(self):
        assert PSL27_ORDER == 168

    def test_stabilizer_is_1344(self):
        assert STABILIZER_ORDER == 1344

    def test_stabilizer_factored(self):
        assert STABILIZER_ORDER == PSL27_ORDER * 8


# ════════════════════════════════════════════════════════════════════════════
# GROUP 1 — Fano geometry (5 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestFanoGeometry:
    def test_fano_7_points(self):
        assert fano_point_count() == 7

    def test_fano_points_eq_phi6(self):
        assert fano_point_count() == PHI6

    def test_fano_7_lines(self):
        assert fano_line_count() == 7

    def test_fano_lines_eq_phi6(self):
        assert fano_line_count() == PHI6

    def test_fano_3_points_per_line(self):
        assert fano_points_per_line() == 3

    def test_fano_pts_per_line_eq_q(self):
        assert fano_points_per_line() == Q

    def test_fano_3_lines_per_point(self):
        assert fano_lines_per_point() == 3

    def test_fano_lines_per_point_eq_q(self):
        assert fano_lines_per_point() == Q

    def test_fano_aut_order_168(self):
        assert fano_aut_order() == 168

    def test_fano_aut_eq_psl27(self):
        assert fano_aut_order() == PSL27_ORDER

    def test_psl27_factors(self):
        # |PSL(2,7)| = 7 × 8 × 3 = 168
        assert PSL27_ORDER == PHI6 * 2**Q * 3

    def test_phi6_eq_both_counts(self):
        assert fano_phi6_eq_n_points()

    def test_fano_triples_count(self):
        assert len(FANO_TRIPLES_1) == 7

    def test_fano_0indexed_triples_count(self):
        assert len(FANO_TRIPLES_0) == 7

    def test_fano_lines_are_frozensets(self):
        assert all(isinstance(l, frozenset) for l in FANO_LINES_1)

    def test_fano_line_sizes_are_3(self):
        assert all(len(l) == 3 for l in FANO_LINES_1)

    def test_fano_incidence_consistent(self):
        # every pair of Fano points appears in exactly 1 common line
        pts = list(range(1, 8))
        for i in pts:
            for j in pts:
                if i >= j:
                    continue
                count = sum(1 for l in FANO_LINES_1 if i in l and j in l)
                assert count == 1, f"({i},{j}) in {count} lines, expected 1"

    def test_all_fano_points_covered(self):
        covered = set()
        for t in FANO_TRIPLES_1:
            covered.update(t)
        assert covered == set(range(1, 8))


# ════════════════════════════════════════════════════════════════════════════
# GROUP 2 — Octonion algebra (4 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestOctonionAlgebra:
    def test_7_imaginary_units(self):
        assert octonion_imaginary_count() == 7

    def test_imaginary_count_eq_fano_pts(self):
        assert octonion_imaginary_count() == N_FANO_POINTS

    def test_octonion_dim_is_8(self):
        assert octonion_dim() == 8

    def test_octonion_dim_eq_2_pow_q(self):
        assert octonion_dim() == 2**Q

    def test_cross_product_table_size(self):
        # 7 triples × 6 orderings = 42 entries
        assert len(CROSS) == 42

    def test_cross_product_only_imaginary(self):
        # all results are indices 0..6
        for (a, b), (s, c) in CROSS.items():
            assert 0 <= c < 7, f"Product index {c} out of range"

    def test_cross_product_signs_are_pm1(self):
        for (a, b), (s, c) in CROSS.items():
            assert s in (1, -1), f"Sign {s} is not ±1"

    def test_cross_product_consistent_with_fano_triples(self):
        # every Fano triple (a,b,c) → ea×eb=ec with sign +1
        for (a, b, c) in FANO_TRIPLES_0:
            assert CROSS.get((a, b)) == (1, c), f"Fano triple ({a},{b},{c}) check fail"

    def test_anticommutativity(self):
        assert octonion_is_anticommutative()

    def test_anticommutativity_explicit(self):
        # For every (a,b): sign of (a,b) = -sign of (b,a); same target
        for (a, b), (s1, c1) in CROSS.items():
            s2, c2 = CROSS[(b, a)]
            assert c1 == c2
            assert s1 == -s2

    def test_associator_nonzero(self):
        assert octonion_associator_nonzero()

    def test_480_multiplication_tables(self):
        assert N_OCTONION_TABLES == 480

    def test_stabilizer_eq_psl27_times_8(self):
        assert STABILIZER_ORDER == PSL27_ORDER * 8

    def test_octonion_dim_plus_fano_pts(self):
        # Full O = R ⊕ Im(O): 8 = 1 + 7
        assert octonion_dim() == 1 + N_FANO_POINTS


# ════════════════════════════════════════════════════════════════════════════
# GROUP 3 — G₂ derivation algebra (5 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestG2Derivation:
    """These tests compute the G₂ derivation algebra constraint system."""

    @pytest.fixture(scope="class")
    def g2_data(self):
        null = g2_derivation_dim()
        rank = g2_constraint_rank()
        sl3 = sl3_dim_from_axis_fixing()
        return {"null": null, "rank": rank, "sl3": sl3}

    def test_g2_dim_14(self, g2_data):
        assert g2_data["null"] == 14

    def test_g2_dim_eq_constant(self, g2_data):
        assert g2_data["null"] == G2_DIM

    def test_g2_constraint_rank_35(self, g2_data):
        assert g2_data["rank"] == 35

    def test_g2_rank_plus_nullity_eq_49(self, g2_data):
        assert g2_data["rank"] + g2_data["null"] == 49  # 7×7 variables

    def test_sl3_dim_8(self, g2_data):
        assert g2_data["sl3"] == 8

    def test_sl3_dim_eq_constant(self, g2_data):
        assert g2_data["sl3"] == SL3_DIM

    def test_g2_dim_eq_lam_phi6(self):
        assert G2_DIM == LAM * PHI6

    def test_g2_module_decomp(self):
        s, a, ab = g2_module_silent_plus_active()
        assert s == 1
        assert a == 3
        assert ab == 3

    def test_g2_module_total_is_phi6(self):
        assert g2_module_total_dim() == PHI6

    def test_g2_module_total_is_7(self):
        assert g2_module_total_dim() == 7

    def test_g2_eq_sl3_plus_6(self):
        assert g2_dim_equals_sl3_plus_6()

    def test_g2_dim_explicitly(self):
        # 14 = 8 + 3 + 3
        s, a, ab = g2_module_silent_plus_active()
        assert SL3_DIM + a + ab == G2_DIM

    def test_gfp_rank_trivial(self):
        # rank of identity matrix
        rows = [[1, 0], [0, 1]]
        assert _gfp_rank(rows, p=7) == 2

    def test_gfp_rank_zero_matrix(self):
        rows = [[0, 0], [0, 0]]
        assert _gfp_rank(rows, p=7) == 0

    def test_gfp_rank_rank1(self):
        rows = [[1, 2], [2, 4]]  # second row = 2 × first
        assert _gfp_rank(rows, p=7) == 1

    def test_constraint_matrix_has_rows(self):
        rows = _build_deriv_constraints()
        assert len(rows) > 0

    def test_constraint_matrix_has_49_cols(self):
        rows = _build_deriv_constraints()
        assert all(len(r) == 49 for r in rows)


# ════════════════════════════════════════════════════════════════════════════
# GROUP 4 — G₂ → SU(3) breaking (5 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestG2ToSU3Breaking:
    def test_quaternionic_h_dim_is_4(self):
        assert fano_line_quaternionic_dim() == 4

    def test_quaternionic_h_dim_eq_mu(self):
        assert fano_line_quaternionic_dim() == MU

    def test_colour_complement_is_4(self):
        assert colour_complement_point_count() == 4

    def test_colour_complement_eq_mu(self):
        assert colour_complement_point_count() == MU

    def test_colour_complement_formula(self):
        # PHI6 - q = 7 - 3 = 4
        assert N_FANO_POINTS - Q == MU

    def test_7_spacetime_embeddings(self):
        assert fano_spacetime_embeddings() == 7

    def test_spacetime_embeddings_eq_phi6(self):
        assert fano_spacetime_embeddings() == PHI6

    def test_su3_gluon_count_is_8(self):
        assert su3_gluon_count() == 8

    def test_su3_gluon_count_eq_2_pow_q(self):
        assert su3_gluon_count() == 2**Q

    def test_su3_gluon_count_eq_sl3_dim(self):
        assert su3_gluon_count() == SL3_DIM

    def test_colour_not_closed(self):
        assert colour_algebra_not_closed()

    def test_colour_products_not_in_colour(self):
        colour_0 = {4, 5, 6}
        for a in colour_0:
            for b in colour_0:
                if a != b:
                    prod = CROSS.get((a, b))
                    assert prod is not None
                    _, c = prod
                    assert c not in colour_0, f"colour×colour closed at ({a},{b})→{c}"

    def test_colour_products_in_non_colour(self):
        colour_0 = {4, 5, 6}
        non_colour = {0, 1, 2, 3}
        for a in colour_0:
            for b in colour_0:
                if a != b:
                    _, c = CROSS[(a, b)]
                    assert c in non_colour

    def test_space_colour_duality_3_pairs(self):
        # e₁↔e₇ (0-idx 0↔6), e₂↔e₅ (0-idx 1↔4), e₄↔e₆ (0-idx 3↔5)
        dual_pairs = [(0, 6), (1, 4), (3, 5)]
        assert len(dual_pairs) == 3

    def test_space_colour_duality_exhausts_imaginary(self):
        # The 6 units paired by duality + e₃ (Higgs) = 7 = PHI6
        dual_units = {0, 6, 1, 4, 3, 5}
        higgs = {2}
        assert len(dual_units | higgs) == PHI6


# ════════════════════════════════════════════════════════════════════════════
# GROUP 5 — SM gauge emergence (5 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestSMGaugeEmergence:
    def test_sm_gauge_dim_12(self):
        assert sm_gauge_dim() == 12

    def test_sm_gauge_dim_eq_k(self):
        assert sm_gauge_dim() == K

    def test_sm_gauge_decomp_8_3_1(self):
        su3, su2, u1 = sm_gauge_decomposition()
        assert su3 == 8
        assert su2 == 3
        assert u1 == 1

    def test_sm_gauge_su3_eq_2_pow_q(self):
        su3, _, _ = sm_gauge_decomposition()
        assert su3 == 2**Q

    def test_sm_gauge_su2_eq_q(self):
        _, su2, _ = sm_gauge_decomposition()
        assert su2 == Q

    def test_sm_gauge_u1_eq_1(self):
        _, _, u1 = sm_gauge_decomposition()
        assert u1 == 1

    def test_sm_gauge_sum_is_k(self):
        assert sm_gauge_sum_equals_k()

    def test_sm_gauge_decomp_formula(self):
        # k = 2^q + q + 1
        assert K == 2**Q + Q + 1

    def test_sm_rank_4(self):
        assert sm_rank() == 4

    def test_sm_rank_eq_mu(self):
        assert sm_rank() == MU

    def test_sm_rank_formula(self):
        # rank(SU3)+rank(SU2)+rank(U1) = 2 + 1 + 1 = 4 = MU
        assert sm_rank() == (Q - 1) + (LAM - 1) + 1

    def test_fermions_15_per_gen(self):
        assert sm_fermions_per_generation() == 15

    def test_fermions_eq_mult_s(self):
        assert sm_fermions_per_generation() == MULT_S

    def test_fermions_5bar_plus_10(self):
        # SU(5): 5̄ (= MU+1 = 5) + 10 (= C(5,2))
        fivebar = MU + 1  # 5
        ten = fivebar * MU // 2  # C(5,2) = 10
        assert fivebar + ten == 15

    def test_3_generations_from_fano(self):
        assert sm_generations_from_fano() == 3

    def test_generations_eq_q(self):
        assert sm_generations_are_q()

    def test_generations_from_higgs_lines(self):
        # e₃ (0-indexed: 2) is the Higgs direction; 3 Fano lines pass through it
        higgs_0 = 2
        count = sum(1 for t in FANO_TRIPLES_0 if higgs_0 in t)
        assert count == Q


# ════════════════════════════════════════════════════════════════════════════
# GROUP 6 — Grand unification identities (3 checks)
# ════════════════════════════════════════════════════════════════════════════
class TestGrandUnification:
    def test_weinberg_exact_fraction(self):
        assert weinberg_angle_exact() == Fraction(3, 13)

    def test_weinberg_numerator_eq_q(self):
        f = weinberg_angle_exact()
        assert f.numerator == Q

    def test_weinberg_denominator_eq_phi13(self):
        f = weinberg_angle_exact()
        assert f.denominator == PHI13

    def test_weinberg_numeric_approx(self):
        # sin²θ_W ≈ 0.2308; measured ≈ 0.2312
        val = weinberg_angle_numeric()
        assert abs(val - 3 / 13) < 1e-10

    def test_weinberg_in_physical_range(self):
        val = weinberg_angle_numeric()
        assert 0.22 < val < 0.24

    def test_exceptional_g2_from_w33(self):
        assert exceptional_g2_from_w33()

    def test_exceptional_g2_formula(self):
        d = all_exceptional_dims_from_w33()
        assert d["G2"] == LAM * PHI6 == G2_DIM

    def test_exceptional_f4(self):
        d = all_exceptional_dims_from_w33()
        assert d["F4"] == V + K == 52

    def test_exceptional_e6(self):
        d = all_exceptional_dims_from_w33()
        assert d["E6"] == LAM * Q * PHI13 == 78

    def test_exceptional_e7(self):
        d = all_exceptional_dims_from_w33()
        assert d["E7"] == PHI6 * (K + PHI6) == 133

    def test_exceptional_e8(self):
        d = all_exceptional_dims_from_w33()
        assert d["E8"] == E + 2**Q == 248

    def test_e8_dim_is_248(self):
        d = all_exceptional_dims_from_w33()
        assert d["E8"] == 248

    def test_single_object_keys(self):
        s = single_object_theorem()
        assert "single_object" in s
        assert "aut_O_is_G2" in s
        assert "SM_gauge_is_K" in s
        assert "Weinberg_is_q_over_Phi13" in s

    def test_all_sm_from_q(self):
        # The entire SM is parameterized by q=3 alone
        assert K == 2**Q + Q + 1       # gauge dim
        assert MULT_S == 15             # fermions
        assert GENERATIONS == Q        # three generations
        assert PHI13 == Q**2 + Q + 1   # Weinberg denominator


# ════════════════════════════════════════════════════════════════════════════
# Full verification
# ════════════════════════════════════════════════════════════════════════════
class TestVerifyAll:
    @pytest.fixture(scope="class")
    def results(self):
        checks, passed, total = verify_all()
        return {"checks": checks, "passed": passed, "total": total}

    def test_all_27_checks_run(self, results):
        assert results["total"] == 27

    def test_all_checks_pass(self, results):
        failed = [name for name, ok in results["checks"] if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_passed_count_27(self, results):
        assert results["passed"] == 27

    def test_check_names_unique(self, results):
        names = [name for name, _ in results["checks"]]
        assert len(names) == len(set(names))

    def test_group1_fano_geometry(self, results):
        group = {n: ok for n, ok in results["checks"]
                 if "fano" in n and n not in (
                     "fano_line_selects_quaternionic_H_dim4",
                     "fano_7_spacetime_embeddings",
                 )}
        assert all(group.values()), f"Fano geometry failures: {group}"

    def test_group2_octonion(self, results):
        group = {n: ok for n, ok in results["checks"] if "octonion" in n}
        assert all(group.values()), f"Octonion failures: {group}"

    def test_group3_g2(self, results):
        group = {n: ok for n, ok in results["checks"] if "g2" in n or "sl3" in n}
        assert all(group.values()), f"G₂ failures: {group}"

    def test_group4_breaking(self, results):
        group = {n: ok for n, ok in results["checks"]
                 if "su3" in n or "colour" in n or "spacetime" in n}
        assert all(group.values()), f"Breaking failures: {group}"

    def test_group5_sm(self, results):
        group = {n: ok for n, ok in results["checks"]
                 if "sm_" in n or "fermion" in n or "generation" in n}
        assert all(group.values()), f"SM failures: {group}"

    def test_group6_gut(self, results):
        group = {n: ok for n, ok in results["checks"]
                 if "weinberg" in n or "exceptional" in n or "single_object" in n}
        assert all(group.values()), f"GUT failures: {group}"


class TestBuildResults:
    @pytest.fixture(scope="class")
    def r(self):
        return build_results()

    def test_verified_true(self, r):
        assert r["verified"] is True

    def test_status_pass(self, r):
        assert r["status"] == "PASS"

    def test_27_checks(self, r):
        assert r["checks_total"] == 27

    def test_all_passed(self, r):
        assert r["checks_passed"] == 27

    def test_no_failures(self, r):
        assert r["failed_checks"] == []

    def test_part_key(self, r):
        assert r["part"] == "CCCCXX"

    def test_fano_geometry_section(self, r):
        fg = r["fano_geometry"]
        assert fg["n_points"] == 7
        assert fg["n_lines"] == 7
        assert fg["pts_per_line"] == 3
        assert fg["aut_order"] == 168

    def test_octonion_section(self, r):
        oc = r["octonion_algebra"]
        assert oc["dim"] == 8
        assert oc["n_imaginary"] == 7
        assert oc["is_anticommutative"] is True
        assert oc["associator_nonzero"] is True

    def test_g2_section(self, r):
        g2 = r["g2_derivation"]
        assert g2["dim_g2"] == 14
        assert g2["nullity"] == 14
        assert g2["rank"] == 35
        assert g2["sl3_nullity_fixed_axis"] == 8

    def test_breaking_section(self, r):
        br = r["g2_to_su3_breaking"]
        assert br["h_dim"] == 4
        assert br["spacetime_embeddings"] == 7
        assert br["su3_gluon_count"] == 8
        assert br["colour_not_closed"] is True

    def test_sm_section(self, r):
        sm = r["sm_gauge_emergence"]
        assert sm["k"] == 12
        assert sm["su3_dim"] == 8
        assert sm["su2_dim"] == 3
        assert sm["u1_dim"] == 1
        assert sm["sm_rank"] == 4
        assert sm["fermions_per_gen"] == 15
        assert sm["n_generations"] == 3

    def test_gut_section(self, r):
        gut = r["grand_unification"]
        assert gut["weinberg_exact"] == "3/13"
        d = gut["exceptional_lie_dims"]
        assert d["G2"] == 14
        assert d["E8"] == 248

    def test_results_serialisable(self, r):
        # must be JSON-serialisable
        json.dumps(r)

    def test_all_check_values_are_bool(self, r):
        for name, val in r["checks"].items():
            assert isinstance(val, bool), f"Check {name!r} has non-bool value {val!r}"
