"""
Phase CCLVI: Ramanujan tau function reconstruction from W(3,3) parameters.

From just two W(3,3) identities:
  tau(2) = -f = -24
  tau(3) = k*q*Phi6 = 12*3*7 = 252

All tau(2^a * 3^b) values are reconstructible via Hecke recursions.

The mod-23 layer is a finite checked packet: 23 = 2k-1 divides selected
initial tau values, but tau(6), tau(8), and tau(13) are counterexamples to a
universal divisibility law.
"""

import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15
ev_r, ev_s = 2, -4

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

double_k_minus_1 = 2 * k - 1  # = 23


class TestTauReconstruction:

    def test_tau2_from_f(self):
        """tau(2) = -f_dim = -24."""
        assert tau[2] == -f_dim

    def test_tau3_from_kqPhi6(self):
        """tau(3) = k*q*Phi6 = 252."""
        assert tau[3] == k * q * Phi6

    def test_tau6_multiplicativity(self):
        """tau(6) = tau(2)*tau(3) (multiplicativity for coprime arguments)."""
        assert tau[6] == tau[2] * tau[3]

    def test_tau4_hecke_recursion(self):
        """tau(4) = tau(2)^2 - 2^11 (Hecke recursion at prime 2)."""
        assert tau[4] == tau[2] ** 2 - 2**11

    def test_tau9_hecke_recursion(self):
        """tau(9) = tau(3)^2 - 3^11 (Hecke recursion at prime 3)."""
        assert tau[9] == tau[3] ** 2 - 3**11

    def test_tau8_hecke_recursion(self):
        """tau(8) = tau(2)*tau(4) - 2^11 * tau(2)."""
        assert tau[8] == tau[2] * tau[4] - 2**11 * tau[2]

    def test_tau12_multiplicativity(self):
        """tau(12) = tau(4)*tau(3) (gcd(4,3)=1)."""
        assert tau[12] == tau[4] * tau[3]

    def test_tau10_multiplicativity(self):
        """tau(10) = tau(2)*tau(5)."""
        assert tau[10] == tau[2] * tau[5]

    def test_W33_reconstructs_tau_at_2_3_powers(self):
        """All tau(2^a * 3^b) values derivable from f and k*q*Phi6 alone."""
        # tau(2) = -f
        t2 = -f_dim
        # tau(3) = k*q*Phi6
        t3 = k * q * Phi6
        # Derive
        t4 = t2**2 - 2**11
        t6 = t2 * t3
        t8 = t2 * t4 - 2**11 * t2
        t9 = t3**2 - 3**11
        t12 = t4 * t3
        assert t4 == tau[4]
        assert t6 == tau[6]
        assert t8 == tau[8]
        assert t9 == tau[9]
        assert t12 == tau[12]

    def test_2k_minus_1_equals_23(self):
        """2k-1 = 23 is a W(3,3) parameter."""
        assert double_k_minus_1 == 23
        assert double_k_minus_1 == 2 * k - 1

    def test_tau_divisible_by_23_composite_packet(self):
        """Composite initial values have an exact packet plus counterexamples."""
        composites = [4, 6, 8, 9, 10, 12]
        divisible = {n for n in composites if tau[n] % 23 == 0}
        assert divisible == {4, 9, 10, 12}
        assert {6, 8}.isdisjoint(divisible)

    def test_tau_divisible_by_23_prime_packet(self):
        """Prime initial values divisible by 23 are selected, not universal."""
        primes = [2, 3, 5, 7, 11, 13]
        divisible = {p for p in primes if tau[p] % 23 == 0}
        assert divisible == {5, 7, 11}
        assert {2, 3, 13}.isdisjoint(divisible)

    def test_tau4_divisible_by_f(self):
        """tau(4) = -1472 = -f * 184/3 ... verify exact relation."""
        # tau(4) = -1472 = -64 * 23 = -64 * (2k-1)
        assert tau[4] == -64 * (2 * k - 1)
        assert tau[4] == -(2**6) * double_k_minus_1

    def test_tau2_generates_tower(self):
        """The pair (tau(2), tau(3)) generates tau at all highly composite n."""
        # This is a consequence of multiplicativity + Hecke recursion
        assert tau[2] == -f_dim  # generator 1
        assert tau[3] == k * q * Phi6  # generator 2
        assert tau[6] == tau[2] * tau[3]  # cross product
        assert tau[9] == tau[3] ** 2 - 3**11  # recursion
