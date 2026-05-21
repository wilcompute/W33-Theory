"""Tests for Part MCLXI: Lovász Theta and Hoffman Bound for W(3,3)."""
import pytest
from fractions import Fraction
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_lovasz_hoffman import (
    hoffman_bound,
    lovasz_theta,
    lovasz_theta_complement,
    sandwich_theorem_check,
    clique_number,
    chromatic_number_bounds,
    fractional_chromatic,
    theta_product_bound,
    delsarte_bound,
    lovasz_hoffman_main,
    v, k, r, s,
)


class TestHoffmanBound:
    def test_value(self):
        assert hoffman_bound() == Fraction(10)

    def test_formula(self):
        # v * (-s) / (k - s) = 40*4/16
        assert hoffman_bound() == Fraction(v * (-s), k - s)

    def test_is_v_over_4(self):
        assert hoffman_bound() == Fraction(v, 4)

    def test_type(self):
        assert isinstance(hoffman_bound(), Fraction)


class TestLovaszTheta:
    def test_theta_value(self):
        assert lovasz_theta() == Fraction(10)

    def test_theta_equals_hoffman(self):
        assert lovasz_theta() == hoffman_bound()

    def test_formula(self):
        # theta(G) = -v*s/(k-s) = 40*4/16
        assert lovasz_theta() == Fraction(-v * s, k - s)


class TestLovaszThetaComplement:
    def test_theta_bar_value(self):
        theta_bar, _, _, _ = lovasz_theta_complement()
        assert theta_bar == Fraction(4)

    def test_k_bar(self):
        _, k_bar, _, _ = lovasz_theta_complement()
        assert k_bar == Fraction(27)

    def test_r_bar(self):
        _, _, r_bar, _ = lovasz_theta_complement()
        assert r_bar == Fraction(3)

    def test_s_bar(self):
        _, _, _, s_bar = lovasz_theta_complement()
        assert s_bar == Fraction(-3)

    def test_k_bar_formula(self):
        _, k_bar, _, _ = lovasz_theta_complement()
        assert k_bar == Fraction(v - 1 - k)

    def test_s_bar_formula(self):
        _, _, _, s_bar = lovasz_theta_complement()
        assert s_bar == Fraction(-1) - r

    def test_r_bar_formula(self):
        _, _, r_bar, _ = lovasz_theta_complement()
        assert r_bar == Fraction(-1) - s


class TestThetaProduct:
    def test_product_equals_v(self):
        product, v_check = theta_product_bound()
        assert product == Fraction(v)

    def test_product_tight(self):
        product, v_check = theta_product_bound()
        assert product == v_check

    def test_product_value(self):
        product, _ = theta_product_bound()
        assert product == Fraction(40)


class TestSandwichTheorem:
    def test_sandwich_holds(self):
        _, _, _, _, sandwich_ok = sandwich_theorem_check()
        assert sandwich_ok

    def test_alpha_equals_theta(self):
        alpha, theta, _, _, _ = sandwich_theorem_check()
        assert alpha == theta

    def test_alpha_value(self):
        alpha, _, _, _, _ = sandwich_theorem_check()
        assert alpha == Fraction(10)

    def test_theta_value(self):
        _, theta, _, _, _ = sandwich_theorem_check()
        assert theta == Fraction(10)

    def test_theta_bar_value(self):
        _, _, theta_bar, _, _ = sandwich_theorem_check()
        assert theta_bar == Fraction(4)

    def test_chi_f_value(self):
        _, _, _, chi_f, _ = sandwich_theorem_check()
        assert chi_f == Fraction(4)


class TestCliqueNumber:
    def test_clique_number_value(self):
        assert clique_number() == Fraction(4)

    def test_hoffman_clique_formula(self):
        # omega = 1 + k/|s|
        assert clique_number() == Fraction(1) + Fraction(k, int(-s))

    def test_type(self):
        assert isinstance(clique_number(), Fraction)


class TestChromaticNumber:
    def test_chi_value(self):
        chi, _, _, _ = chromatic_number_bounds()
        assert chi == Fraction(4)

    def test_all_lower_bounds_equal_4(self):
        _, lb1, lb2, lb3 = chromatic_number_bounds()
        assert lb1 == lb2 == lb3 == Fraction(4)

    def test_chi_equals_omega(self):
        chi, _, _, _ = chromatic_number_bounds()
        assert chi == clique_number()


class TestFractionalChromatic:
    def test_chi_f_value(self):
        assert fractional_chromatic() == Fraction(4)

    def test_chi_f_equals_chi(self):
        chi, _, _, _ = chromatic_number_bounds()
        assert fractional_chromatic() == chi

    def test_chi_f_formula(self):
        # v / alpha = 40/10 = 4
        assert fractional_chromatic() == Fraction(v, int(hoffman_bound()))


class TestDelsarteBound:
    def test_delsarte_equals_hoffman(self):
        assert delsarte_bound() == hoffman_bound()

    def test_delsarte_value(self):
        assert delsarte_bound() == Fraction(10)


class TestFullPacket:
    def test_part_and_theorem_fields(self):
        res = lovasz_hoffman_main()
        assert res["part"] == "MCLXI"
        assert res["theorem"] == "Lovasz-Hoffman extremal certificate"

    def test_n_verified(self):
        res = lovasz_hoffman_main()
        assert res["n_verified"] >= 20

    def test_hoffman_bound_field(self):
        res = lovasz_hoffman_main()
        assert res["hoffman_bound"] == "10"

    def test_alpha_field(self):
        res = lovasz_hoffman_main()
        assert res["alpha_G"] == "10"

    def test_lovasz_theta_field(self):
        res = lovasz_hoffman_main()
        assert res["lovasz_theta"] == "10"

    def test_lovasz_theta_bar_field(self):
        res = lovasz_hoffman_main()
        assert res["lovasz_theta_bar"] == "4"

    def test_theta_product_field(self):
        res = lovasz_hoffman_main()
        assert res["theta_product"] == "40"

    def test_chi_G_field(self):
        res = lovasz_hoffman_main()
        assert res["chi_G"] == "4"

    def test_chi_f_field(self):
        res = lovasz_hoffman_main()
        assert res["chi_f_G"] == "4"

    def test_omega_field(self):
        res = lovasz_hoffman_main()
        assert res["omega_G"] == "4"

    def test_sandwich_and_boundary_fields(self):
        res = lovasz_hoffman_main()
        assert res["sandwich_ok"]
        assert res["claim_boundary"] == "finite W33 Lovasz-Hoffman extremal certificate"
