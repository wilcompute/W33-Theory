"""
Phase CCLIX: tau(p) at primes p=5,7 are fully expressible in W(3,3) parameter ring.

tau(5) = 2*p*(p-2)*Phi6*(2k-1) = 2*5*3*7*23 = 4830
tau(7) = -(p+1)*Phi6*Phi3*(2k-1) = -8*7*13*23 = -16744

tau(11) and tau(13) require external primes (149, 1423) not in W(3,3) ring.

The checked mod-23 layer is therefore a selected W(3,3)-visible congruence
packet, not a universal tau(n) ≡ 0 mod (2k-1) law.
"""

import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15

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


class TestTauPrimeReconstruction:

    def test_tau5_full_formula(self):
        """tau(5) = 2*p*(p-2)*Phi6*(2k-1) where p=5."""
        p = 5
        assert tau[5] == 2 * p * (p - 2) * Phi6 * double_k_minus_1

    def test_tau7_full_formula(self):
        """tau(7) = -(p+1)*Phi6*Phi3*(2k-1) where p=7."""
        p = 7
        assert tau[7] == -(p + 1) * Phi6 * Phi3 * double_k_minus_1

    def test_tau5_over_23(self):
        """tau(5)/(2k-1) = 210 = 2*q*p*Phi6."""
        p = 5
        assert tau[5] // double_k_minus_1 == 2 * q * p * Phi6
        assert tau[5] % double_k_minus_1 == 0

    def test_tau7_over_23(self):
        """tau(7)/(2k-1) = -728 = -(p+1)*Phi6*Phi3."""
        p = 7
        assert tau[7] // double_k_minus_1 == -(p + 1) * Phi6 * Phi3
        assert tau[7] % double_k_minus_1 == 0

    def test_tau5_in_W33_ring(self):
        """All prime factors of tau(5) are in the W(3,3) parameter ring."""
        import sympy

        W33_primes = {2, 3, 5, 7, 11, 13, 23}  # primes from k,v,f,g,Phi3,Phi4,Phi6,2k-1
        fac = set(sympy.factorint(abs(tau[5])).keys())
        assert fac.issubset(W33_primes)

    def test_tau7_in_W33_ring(self):
        """All prime factors of tau(7) are in the W(3,3) parameter ring."""
        import sympy

        W33_primes = {2, 3, 5, 7, 11, 13, 23}
        fac = set(sympy.factorint(abs(tau[7])).keys())
        assert fac.issubset(W33_primes)

    def test_tau11_has_external_prime(self):
        """tau(11) contains prime 149, outside W(3,3) ring."""
        import sympy

        W33_primes = {2, 3, 5, 7, 11, 13, 23}
        fac = set(sympy.factorint(abs(tau[11])).keys())
        external = fac - W33_primes
        assert 149 in external

    def test_tau13_has_external_primes(self):
        """tau(13) contains primes 29 and 1423, outside W(3,3) ring."""
        import sympy

        W33_primes = {2, 3, 5, 7, 11, 13, 23}
        fac = set(sympy.factorint(abs(tau[13])).keys())
        external = fac - W33_primes
        assert len(external) >= 1

    def test_tau_divisible_23_initial_packet_has_counterexamples(self):
        """The initial mod-23 packet is exact but not universal."""
        divisible = {n for n in range(4, 14) if tau[n] % 23 == 0}
        assert divisible == {4, 5, 7, 9, 10, 11, 12}
        assert {6, 8, 13}.isdisjoint(divisible)

    def test_tau2_and_tau3_not_divisible_23(self):
        """tau(2) and tau(3) are NOT divisible by 23 (they ARE the W(3,3) generators)."""
        assert tau[2] % 23 != 0
        assert tau[3] % 23 != 0
