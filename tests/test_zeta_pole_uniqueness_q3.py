"""
Phase CCLIII: The Hashimoto zeta pole-calibration identity holds ONLY at q=3.

For W(3,q), the zeta characteristic factors are:
  p1(u) = 1 - (q-1)*u + q(q+1)*u^2   [r-eigenvalue factor]
  p2(u) = 1 + (q+1)*u + q(q+1)*u^2   [s-eigenvalue factor]

The pole imaginary parts satisfy:
  Im(poles of p1)^2 / 4 = Phi4(q)  <==>  q = 3
  Im(poles of p2)^2 / 4 = Phi6(q)  <==>  q = 3

The deficit: Im^2/4 - Phi_cyc(q) = -(q-3)^2 / 4   [universal]

Consequence: At q=3, the zeta poles live in Q(sqrt(-7)) [Heegner!]
and Q(sqrt(-10)), encoding the cyclotomic values exactly.
"""

from math import sqrt

import pytest
from sympy import Rational, factor, simplify
from sympy import solve as ssym_solve
from sympy import sqrt as ssqrt
from sympy import symbols

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15
ev_r, ev_s = 2, -4


class TestZetaPoleUniqueness:

    def test_deficit_formula_symbolic(self):
        """Im^2/4 - Phi_cyc(q) = -(q-3)^2/4 for both p1 and p2."""
        q_sym = symbols("q", positive=True)
        r_sym = q_sym - 1
        s_sym = -(q_sym + 1)
        km1 = q_sym * (q_sym + 1) - 1
        Phi4_sym = q_sym**2 + 1
        Phi6_sym = q_sym**2 - q_sym + 1

        disc1 = r_sym**2 - 4 * km1
        disc2 = s_sym**2 - 4 * km1
        deficit1 = simplify(-disc1 / 4 - Phi4_sym)
        deficit2 = simplify(-disc2 / 4 - Phi6_sym)

        assert factor(deficit1) == -((q_sym - 3) ** 2) / 4
        assert factor(deficit2) == -((q_sym - 3) ** 2) / 4

    def test_deficits_are_equal(self):
        """Both deficits (p1 and p2) are identical: -(q-3)^2/4."""
        q_sym = symbols("q", positive=True)
        r_sym = q_sym - 1
        s_sym = -(q_sym + 1)
        km1 = q_sym * (q_sym + 1) - 1
        Phi4_sym = q_sym**2 + 1
        Phi6_sym = q_sym**2 - q_sym + 1
        disc1 = r_sym**2 - 4 * km1
        disc2 = s_sym**2 - 4 * km1
        deficit1 = simplify(-disc1 / 4 - Phi4_sym)
        deficit2 = simplify(-disc2 / 4 - Phi6_sym)
        assert simplify(deficit1 - deficit2) == 0

    def test_deficit_vanishes_only_at_q3(self):
        """The deficit -(q-3)^2/4 = 0 only at q=3."""
        q_sym = symbols("q", positive=True)
        deficit = -((q_sym - 3) ** 2) / 4
        zeros = ssym_solve(deficit, q_sym)
        assert zeros == [3]

    def test_q3_calibration_p1(self):
        """At q=3: Im(poles of p1)^2 / 4 = Phi4(3) = 10."""
        # p1 = 1 - 2u + 11u^2, discriminant = 4 - 44 = -40
        disc1 = ev_r**2 - 4 * (k - 1)
        im1_sq = -disc1  # = 40
        assert im1_sq // 4 == Phi4
        assert im1_sq == 4 * Phi4

    def test_q3_calibration_p2(self):
        """At q=3: Im(poles of p2)^2 / 4 = Phi6(3) = 7."""
        disc2 = ev_s**2 - 4 * (k - 1)  # 16 - 44 = -28
        im2_sq = -disc2  # = 28
        assert im2_sq // 4 == Phi6
        assert im2_sq == 4 * Phi6

    def test_other_q_values_fail_calibration(self):
        """For q != 3, calibration fails."""
        for qq in [2, 4, 5, 7, 8, 9]:
            kq = qq * (qq + 1)
            rq = qq - 1
            sq = -(qq + 1)
            Phi4q = qq**2 + 1
            Phi6q = qq**2 - qq + 1
            disc1 = rq**2 - 4 * (kq - 1)
            disc2 = sq**2 - 4 * (kq - 1)
            # deficit = (-disc)/4 - Phi_cyc = -(q-3)^2/4 != 0 for q!=3
            deficit = (-disc1) / 4 - Phi4q
            assert deficit == -((qq - 3) ** 2) / 4
            assert deficit != 0

    def test_p1_poles_in_Q_sqrt_minus_Phi4(self):
        """At q=3: p1 poles are in Q(sqrt(-Phi4)) = Q(sqrt(-10))."""
        # poles = (1 ± i*sqrt(10)) / 11
        disc1 = ev_r**2 - 4 * (k - 1)
        assert -disc1 == 4 * Phi4  # im^2 = 4*Phi4
        # The quadratic field is Q(sqrt(-10))
        assert Phi4 == 10  # the discriminant (up to sign and square)

    def test_p2_poles_in_Q_sqrt_minus_Phi6(self):
        """At q=3: p2 poles are in Q(sqrt(-Phi6)) = Q(sqrt(-7))."""
        disc2 = ev_s**2 - 4 * (k - 1)
        assert -disc2 == 4 * Phi6  # im^2 = 4*Phi6
        assert Phi6 == 7

    def test_heegner_sqrt_minus_7(self):
        """Q(sqrt(-7)) is a Heegner field with class number 1."""
        heegner_numbers = [-1, -2, -3, -7, -11, -19, -43, -67, -163]
        assert -Phi6 in heegner_numbers
        assert -7 in heegner_numbers

    def test_not_heegner_sqrt_minus_10(self):
        """Q(sqrt(-10)) is NOT a Heegner field (class number 2)."""
        heegner_numbers = [-1, -2, -3, -7, -11, -19, -43, -67, -163]
        assert -Phi4 not in heegner_numbers
        assert -10 not in heegner_numbers

    def test_both_conditions_equivalent(self):
        """Both calibration conditions vanish simultaneously (same deficit)."""
        # At q=3:
        disc1 = ev_r**2 - 4 * (k - 1)
        disc2 = ev_s**2 - 4 * (k - 1)
        deficit1 = (-disc1) / 4 - Phi4
        deficit2 = (-disc2) / 4 - Phi6
        assert deficit1 == 0 == deficit2

    def test_pole_modulus_equals_1_over_sqrt_km1(self):
        """All nontrivial poles have |u| = 1/sqrt(k-1) = 1/sqrt(11)."""
        km1 = k - 1
        # |u from p1|^2 = (r^2 + 4*Phi4) / (4*km1^2)
        # = (4 + 40) / (4*121) = 44/484 = 1/11 = 1/km1
        mod_sq_1 = (ev_r**2 + 4 * Phi4) / (4 * (km1) ** 2)
        assert abs(mod_sq_1 - 1 / km1) < 1e-12
        mod_sq_2 = (ev_s**2 + 4 * Phi6) / (4 * (km1) ** 2)
        assert abs(mod_sq_2 - 1 / km1) < 1e-12
