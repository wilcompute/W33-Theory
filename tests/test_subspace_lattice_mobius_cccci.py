"""
Tests for PART CCCCI: Möbius Function, Posets and the Lattice of Subspaces of GF(3)^4
"""

import json
import pathlib
import pytest

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCCI_SUBSPACE_LATTICE_MOBIUS_BRIDGE import (
    gaussian_binom,
    subspaces_dim0, subspaces_dim1, subspaces_dim2, subspaces_dim3, subspaces_dim4,
    total_subspaces,
    mobius_zero_to_k,
    mobius_0_to_0, mobius_0_to_1, mobius_0_to_2, mobius_0_to_3, mobius_0_to_4,
    mobius_abs_0_to_n,
    whitney_number_first_kind,
    characteristic_poly_coeffs,
    characteristic_poly_at_1, characteristic_poly_at_q, characteristic_poly_at_0,
    num_bases_gf3_4,
    order_of_gsp4_3,
    aut_w33_order_from_subspace_count,
    gaussian_binom_symmetry,
    subspace_incidence_count_12, subspace_incidence_count_23, incidences_12_eq_23,
    lines_per_point, points_per_line,
    sm_crosswalk,
    verify_all,
    build_cccci_summary,
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, TRIANGLES, K4_COUNT, ALPHA, CLIQUE_NU,
    q, n, GUT_DIM, SU5_MATTER, GENERATIONS,
)


class TestVerifyAll:
    def test_verify_all_passes_27(self):
        _, passed, total = verify_all()
        assert total == 27
        assert passed == 27

    def test_no_failing_checks(self):
        checks, passed, total = verify_all()
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_returns_tuple_of_3(self):
        result = verify_all()
        assert len(result) == 3

    def test_checks_list_length(self):
        checks, _, _ = verify_all()
        assert len(checks) == 27

    def test_all_checks_have_bool_result(self):
        checks, _, _ = verify_all()
        for name, ok in checks:
            assert isinstance(ok, bool), f"Check {name!r} did not return bool"


class TestGaussianBinomialCoefficients:
    def test_subspaces_dim0_is_1(self):
        assert subspaces_dim0() == 1

    def test_subspaces_dim1_is_V(self):
        assert subspaces_dim1() == V
        assert subspaces_dim1() == 40

    def test_subspaces_dim2_is_130(self):
        assert subspaces_dim2() == 130

    def test_subspaces_dim3_is_V(self):
        assert subspaces_dim3() == V
        assert subspaces_dim3() == 40

    def test_subspaces_dim4_is_1(self):
        assert subspaces_dim4() == 1

    def test_total_subspaces_is_212(self):
        assert total_subspaces() == 212

    def test_total_subspaces_decomposed(self):
        assert total_subspaces() == 1 + 40 + 130 + 40 + 1

    def test_gaussian_binom_symmetry(self):
        assert gaussian_binom_symmetry()

    def test_dim1_eq_dim3_self_dual(self):
        assert subspaces_dim1() == subspaces_dim3()

    def test_gaussian_binom_q2_formula(self):
        # [4,2]_3 = (q^4-1)(q^3-1)/((q^2-1)(q-1))
        expected = (3**4 - 1) * (3**3 - 1) // ((3**2 - 1) * (3 - 1))
        assert gaussian_binom(4, 2, 3) == expected

    def test_gaussian_binom_out_of_range_gives_0(self):
        assert gaussian_binom(4, 5, 3) == 0
        assert gaussian_binom(4, -1, 3) == 0

    def test_gaussian_binom_boundary_k0(self):
        assert gaussian_binom(4, 0, 3) == 1

    def test_gaussian_binom_boundary_kn(self):
        assert gaussian_binom(4, 4, 3) == 1

    def test_gaussian_binom_q3_values(self):
        # Test a few specific q=3 values
        assert gaussian_binom(4, 0, 3) == 1
        assert gaussian_binom(4, 1, 3) == 40
        assert gaussian_binom(4, 2, 3) == 130
        assert gaussian_binom(4, 3, 3) == 40
        assert gaussian_binom(4, 4, 3) == 1

    def test_total_subspaces_gt_v(self):
        assert total_subspaces() > V


class TestMobiusFunction:
    def test_mobius_0_to_0_is_1(self):
        assert mobius_0_to_0() == 1

    def test_mobius_0_to_1_is_neg1(self):
        assert mobius_0_to_1() == -1

    def test_mobius_0_to_2_is_q(self):
        assert mobius_0_to_2() == q
        assert mobius_0_to_2() == 3

    def test_mobius_0_to_3_is_neg_q3(self):
        assert mobius_0_to_3() == -(q**3)
        assert mobius_0_to_3() == -27

    def test_mobius_0_to_4_is_q6(self):
        assert mobius_0_to_4() == q**6
        assert mobius_0_to_4() == 729

    def test_mobius_abs_0_to_n_is_q6(self):
        assert mobius_abs_0_to_n() == q**6
        assert mobius_abs_0_to_n() == 729

    def test_mobius_abs_0_to_n_formula(self):
        # |mu(0, V_n)| = q^{C(n,2)} = q^6 for n=4
        assert mobius_abs_0_to_n() == q ** (n * (n - 1) // 2)

    def test_mobius_alternating_sign(self):
        # (-1)^k sign
        for k in range(5):
            val = mobius_zero_to_k(k)
            assert ((-1) ** k) * val > 0, f"k={k}: sign error"

    def test_mobius_0_to_4_positive(self):
        assert mobius_0_to_4() > 0

    def test_mobius_0_to_3_negative(self):
        assert mobius_0_to_3() < 0


class TestWhitneyAndCharacteristicPoly:
    def test_characteristic_poly_at_1_is_0(self):
        assert characteristic_poly_at_1() == 0

    def test_characteristic_poly_at_q_is_0(self):
        assert characteristic_poly_at_q() == 0

    def test_characteristic_poly_at_0_is_q6(self):
        assert characteristic_poly_at_0() == q**6
        assert characteristic_poly_at_0() == 729

    def test_coeffs_count_is_n_plus_1(self):
        assert len(characteristic_poly_coeffs()) == n + 1

    def test_leading_coeff_is_1(self):
        assert characteristic_poly_coeffs()[0] == 1

    def test_coeff_t3_is_neg_40(self):
        # t^3 coeff = -subspaces_dim1() = -40
        assert characteristic_poly_coeffs()[1] == -40

    def test_coeff_t2_is_390(self):
        # t^2 coeff = gaussian_binom(4,2,3)*q = 130*3 = 390
        assert characteristic_poly_coeffs()[2] == 390

    def test_coeff_t1_is_neg_1080(self):
        # -1080 = -GUT_DIM * V = -27 * 40
        assert characteristic_poly_coeffs()[3] == -1080
        assert characteristic_poly_coeffs()[3] == -(GUT_DIM * V)

    def test_constant_coeff_is_729(self):
        # q^6
        assert characteristic_poly_coeffs()[4] == 729

    def test_sum_of_coeffs_is_0(self):
        # chi(1) = 0
        assert sum(characteristic_poly_coeffs()) == 0

    def test_whitney_w1_eq_neg_40(self):
        assert whitney_number_first_kind(1) == -40

    def test_whitney_w0_eq_1(self):
        assert whitney_number_first_kind(0) == 1

    def test_whitney_w4_eq_729(self):
        assert whitney_number_first_kind(4) == 729


class TestLatticeIncidences:
    def test_incidence_12_is_520(self):
        assert subspace_incidence_count_12() == 520

    def test_incidence_23_is_520(self):
        assert subspace_incidence_count_23() == 520

    def test_incidences_equal(self):
        assert incidences_12_eq_23()

    def test_lines_per_point_is_13(self):
        assert lines_per_point() == 13

    def test_points_per_line_is_4(self):
        assert points_per_line() == 4
        assert points_per_line() == CLIQUE_NU

    def test_incidence_12_formula(self):
        # subspaces_dim2 * (q+1)
        assert subspace_incidence_count_12() == subspaces_dim2() * (q + 1)

    def test_incidence_23_formula(self):
        # subspaces_dim3 * (q^2+q+1)
        assert subspace_incidence_count_23() == subspaces_dim3() * (q**2 + q + 1)

    def test_lines_per_point_formula(self):
        # [3 choose 1]_3 = (q^3-1)/(q-1) = 13
        assert lines_per_point() == (q**3 - 1) // (q - 1)

    def test_points_per_line_formula(self):
        # [2 choose 1]_3 = q+1 = 4
        assert points_per_line() == q + 1

    def test_subspaces_dim2_double_count(self):
        # Counting via lines-through-point: V * lines_per_point / points_per_line
        assert subspaces_dim2() == V * lines_per_point() // points_per_line()


class TestGroupOrders:
    def test_aut_w33_order_is_51840(self):
        assert aut_w33_order_from_subspace_count() == 51840

    def test_order_gsp4_3_is_51840(self):
        assert order_of_gsp4_3() == 51840

    def test_both_formulas_agree(self):
        assert aut_w33_order_from_subspace_count() == order_of_gsp4_3()

    def test_num_bases_gf3_4(self):
        # (q^4-1)(q^4-q)(q^4-q^2)(q^4-q^3)
        expected = (81 - 1) * (81 - 3) * (81 - 9) * (81 - 27)
        assert num_bases_gf3_4() == expected

    def test_num_bases_over_aut(self):
        assert num_bases_gf3_4() // aut_w33_order_from_subspace_count() == 468

    def test_aut_order_divisible_by_V(self):
        assert aut_w33_order_from_subspace_count() % V == 0

    def test_aut_order_divisible_by_K(self):
        assert aut_w33_order_from_subspace_count() % K == 0


class TestSMCrosswalk:
    def test_sm_crosswalk_has_7_entries(self):
        cw = sm_crosswalk()
        assert len(cw) == 7

    def test_sm_crosswalk_keys_present(self):
        cw = sm_crosswalk()
        assert "V_eq_gaussian_binom_4_1" in cw
        assert "mobius_0_to_4_eq_q6" in cw
        assert "aut_order_51840" in cw
        assert "lines_per_point_13" in cw
        assert "characteristic_poly_vanishes" in cw

    def test_sm_crosswalk_all_nonempty_strings(self):
        for key, val in sm_crosswalk().items():
            assert isinstance(val, str) and len(val) > 0, f"Empty value for {key}"


class TestBuildSummary:
    def test_build_cccci_summary_runs(self):
        s = build_cccci_summary()
        assert s is not None

    def test_summary_status_pass(self):
        s = build_cccci_summary()
        assert s["status"] == "PASS"

    def test_summary_part_label(self):
        s = build_cccci_summary()
        assert s["part"] == "CCCCI"

    def test_summary_checks(self):
        s = build_cccci_summary()
        assert s["checks_pass"] == 27
        assert s["checks_total"] == 27

    def test_summary_no_failed_checks(self):
        s = build_cccci_summary()
        assert s["failed_checks"] == []

    def test_summary_discoveries_nonempty(self):
        s = build_cccci_summary()
        assert len(s["discoveries"]) >= 5

    def test_json_written(self):
        build_cccci_summary()
        out = (
            pathlib.Path(__file__).resolve().parents[1]
            / "PART_CCCCI_SUBSPACE_LATTICE_MOBIUS_results.json"
        )
        assert out.exists()

    def test_json_content(self):
        build_cccci_summary()
        out = (
            pathlib.Path(__file__).resolve().parents[1]
            / "PART_CCCCI_SUBSPACE_LATTICE_MOBIUS_results.json"
        )
        with open(out) as fh:
            data = json.load(fh)
        assert data["status"] == "PASS"
        assert data["checks_pass"] == 27

    def test_summary_fields_total_subspaces(self):
        s = build_cccci_summary()
        assert s["fields"]["total_subspaces"] == 212
