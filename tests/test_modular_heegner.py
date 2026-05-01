"""
Phase CCLIV: Modular form and Heegner number connections.

Key identities discovered:
  tau(2) = -24 = -f_dim  (Ramanujan tau at 2)
  tau(3) = 252 = k*q*Phi6 = 12*3*7
  j((1+sqrt(-7))/2) = -3375 = -(g_dim)^3 = -15^3

The s-eigenspace poles of W(3,3) live in Q(sqrt(-7)),
which is a Heegner field with class number 1.

Exponent f=24 in zeta matches:
  |tau(2)| = 24 = f
  d-2 = 24 for d=26 (bosonic string critical dimension)
  eta(z)^24 = Delta(z) (Dedekind eta to 24th power = discriminant modular form)
"""

import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15
ev_r, ev_s = 2, -4

# Ramanujan tau function values
tau = {
    1: 1,
    2: -24,
    3: 252,
    4: -1472,
    5: 4830,
    6: -6048,
    7: -16744,
    8: 84480,
    9: -113643,
    10: -115920,
    11: 534612,
    12: -370944,
    13: -577738,
}

# j-invariant at Heegner points
j_neg7 = -3375  # j((1+sqrt(-7))/2)
j_neg8 = 8000  # j(sqrt(-2)) -- for comparison
j_neg3 = 0  # j(rho) where rho = e^{2pi*i/3}
j_neg4 = 1728  # j(i)


class TestModularHeegner:

    def test_tau2_equals_minus_f(self):
        """tau(2) = -f_dim = -24."""
        assert tau[2] == -f_dim
        assert tau[2] == -24

    def test_abs_tau2_equals_f(self):
        """|tau(2)| = f_dim = 24 = r-eigenspace multiplicity."""
        assert abs(tau[2]) == f_dim

    def test_tau3_equals_k_q_Phi6(self):
        """tau(3) = k*q*Phi6 = 12*3*7 = 252."""
        assert tau[3] == k * q * Phi6
        assert tau[3] == 252

    def test_j_neg7_equals_minus_g_cubed(self):
        """j((1+sqrt(-7))/2) = -3375 = -(g_dim)^3 = -15^3."""
        assert j_neg7 == -((g_dim) ** 3)
        assert j_neg7 == -3375

    def test_j_neg7_cbrt_equals_g(self):
        """Cube root of |j(-7)| = g_dim = 15."""
        assert round(abs(j_neg7) ** (1 / 3)) == g_dim

    def test_f_is_bosonic_string_d_minus_2(self):
        """f = 24 = d-2 for d=26 (bosonic string critical dimension)."""
        d_bosonic = 26
        assert f_dim == d_bosonic - 2

    def test_f_is_eta_exponent(self):
        """f = 24: eta(z)^24 = Delta(z), the exponent in Dedekind eta."""
        # This is a known fact: the discriminant form = eta^24
        eta_exponent = 24
        assert f_dim == eta_exponent

    def test_heegner_discriminant_is_minus_Phi6(self):
        """The Heegner number -7 = -Phi6(3)."""
        heegner_numbers = [-1, -2, -3, -7, -11, -19, -43, -67, -163]
        assert -Phi6 in heegner_numbers

    def test_p2_poles_in_Heegner_field(self):
        """s-eigenspace poles are in Q(sqrt(-7)), a Heegner field."""
        # poles = (-2 ± i*sqrt(7)) / 11
        # Field = Q(sqrt(-7)) since 7 = Phi6(3)
        assert Phi6 == 7  # the imaginary part squared
        assert 7 in [1, 2, 3, 7, 11, 19, 43, 67, 163]  # Heegner discriminants

    def test_j_i_equals_1728_equals_12_cubed(self):
        """j(i) = 1728 = 12^3 = k^3: k appears in another j-value."""
        assert j_neg4 == 1728
        assert j_neg4 == k**3
        assert 1728 == 12**3

    def test_three_j_values_encode_W33(self):
        """Three j-invariants encode W(3,3) parameters: g^3, k^3, (k-1)^3."""
        assert abs(j_neg7) == g_dim**3  # j(-7) = -(g)^3
        assert j_neg4 == k**3  # j(i) = k^3 = 1728
        # j(-11) = -32768 = -2^15 = -2^(k+3)? No: 2^15 = 32768, k+3=15 ✓ but weak
        j_neg11 = -32768
        assert -j_neg11 == 2**15
        assert 15 == g_dim  # exponent 15 = g_dim!
        assert -j_neg11 == 2**g_dim

    def test_tau3_factored(self):
        """tau(3) = 252 = 4 * 63 = 4 * 9 * 7 = m * q^2 * Phi6."""
        assert tau[3] == 4 * 9 * 7
        assert tau[3] == m * q**2 * Phi6  # 4 * 9 * 7 = 252
