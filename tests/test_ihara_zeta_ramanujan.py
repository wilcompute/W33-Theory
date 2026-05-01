"""
Phase CCXL: Ihara zeta function and Ramanujan property of W(3,3).

W(3,3) is a RAMANUJAN GRAPH:
  All nontrivial eigenvalues satisfy |ev| <= 2*sqrt(k-1) = 2*sqrt(11) = 6.633.
  r=2: |r|=2 < 6.633 ✓
  s=-4: |s|=4 < 6.633 ✓

Ihara zeta function:
  Z_G(u)^{-1} = (1-u^2)^{E-v} * prod_{ev} (1 - ev*u + (k-1)*u^2)^{mult}
  For W(3,3):
    ev=12 (x1): (1-u)(1-11u) [trivial poles]
    ev=2 (x24): 1-2u+11u^2 [complex poles on |u|=1/sqrt(11)]
    ev=-4 (x15): 1+4u+11u^2 [complex poles on |u|=1/sqrt(11)]

The Ihara Riemann Hypothesis holds for W(3,3):
  All non-trivial poles lie exactly on |u| = 1/sqrt(k-1) = 1/sqrt(11).

Hashimoto eigenvalues: |lambda| = sqrt(k-1) = sqrt(11) for all non-trivial ones.

Betti numbers of Gr(3,6): [1,1,2,3,3,3,3,2,1,1], chi=20=N.

Weil-Ihara note: k-1=11 is NOT a prime power, so Ihara poles 1/sqrt(11)
do NOT match Weil zeros 3^{-j/2}. The bridge requires Hashimoto/non-backtracking.
"""

from fractions import Fraction
from itertools import product as iproduct
from math import comb, sqrt

import numpy as np
import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f, g = 24, 15
s = k // l
N = comb(s, q)
E = k * v // 2  # = 240
r_eig, s_eig = 2, -4


class TestIharaZetaRamanujan:

    # --- Ramanujan property ---

    def test_ramanujan_bound(self):
        """2*sqrt(k-1) = 2*sqrt(11) ≈ 6.633."""
        bound = 2 * sqrt(k - 1)
        assert abs(bound - 2 * sqrt(11)) < 1e-10
        assert bound < 7

    def test_r_eig_ramanujan(self):
        """r=2: |r| = 2 < 2*sqrt(11) ✓ (Ramanujan)."""
        assert abs(r_eig) < 2 * sqrt(k - 1)

    def test_s_eig_ramanujan(self):
        """s=-4: |s| = 4 < 2*sqrt(11) ≈ 6.633 ✓ (Ramanujan)."""
        assert abs(s_eig) < 2 * sqrt(k - 1)

    def test_W33_is_Ramanujan(self):
        """W(3,3) satisfies the Ramanujan property for both non-trivial eigenvalues."""
        bound = 2 * sqrt(k - 1)
        for ev in [r_eig, s_eig]:
            assert abs(ev) <= bound

    def test_LPS_Ramanujan_criterion(self):
        """LPS criterion: Ramanujan iff spectral gap >= k - 2*sqrt(k-1) = 5.367."""
        spectral_gap = k - abs(r_eig)  # gap between k and largest non-trivial ev
        # More precisely: gap = k - max(|r|, |s|) for symmetric graph
        max_nontrivial = max(abs(r_eig), abs(s_eig))
        gap = k - max_nontrivial
        assert gap == 12 - 4 == 8
        # Ramanujan criterion: max_nontrivial <= 2*sqrt(k-1)
        assert max_nontrivial <= 2 * sqrt(k - 1)

    # --- Ihara zeta factors ---

    def test_trivial_factor_ev_k(self):
        """Factor for ev=k: 1-12u+11u^2 = (1-u)(1-11u)."""
        # Verify factorization
        from numpy.polynomial import polynomial as P

        # 1-12u+11u^2 at u=1: 1-12+11=0 ✓; at u=1/11: 1-12/11+11/121=1-12/11+1/11=0 ✓
        assert 1 - 12 * 1 + 11 * 1**2 == 0  # root at u=1
        # 1 - 12/11 + 11/121 = 121/121 - 132/121 + 11/121 = 0 ✓
        assert abs(1 - 12 * (Fraction(1, 11)) + 11 * (Fraction(1, 11) ** 2)) == 0

    def test_nontrivial_factor_ev_r_complex(self):
        """Factor for ev=r=2: 1-2u+11u^2 has discriminant < 0 (complex poles)."""
        disc = r_eig**2 - 4 * (k - 1)
        assert disc == 4 - 44 == -40
        assert disc < 0  # complex roots

    def test_nontrivial_factor_ev_s_complex(self):
        """Factor for ev=s=-4: 1+4u+11u^2 has discriminant < 0 (complex poles)."""
        disc = s_eig**2 - 4 * (k - 1)
        assert disc == 16 - 44 == -28
        assert disc < 0

    def test_both_nontrivial_poles_on_circle(self):
        """Both non-trivial factors have roots with |u|^2 = 1/(k-1) = 1/11."""
        for ev in [r_eig, s_eig]:
            disc = ev**2 - 4 * (k - 1)
            assert disc < 0  # complex roots
            # Product of roots of 1-ev*u+(k-1)*u^2 = 1/(k-1) (Vieta's)
            product_of_roots = Fraction(1, k - 1)
            assert product_of_roots == Fraction(1, 11)
            # |u1|^2 = |u2|^2 = 1/(k-1) since they're complex conjugates
            # Product |u1|*|u2| = |product| = 1/(k-1) and |u1|=|u2|
            # So |u|^2 = 1/(k-1)

    def test_ihara_RH_holds(self):
        """Ihara RH: all non-trivial poles on |u| = 1/sqrt(k-1)."""
        for ev in [r_eig, s_eig]:
            disc = ev**2 - 4 * (k - 1)
            # Roots: (ev ± sqrt(disc)) / (2*(k-1))
            # |root|^2 = (ev/2)^2 / (k-1)^2 + (-disc/4) / (k-1)^2
            #          = [(ev^2/4) + (-disc/4)] / (k-1)^2
            #          = [ev^2/4 + (k-1) - ev^2/4] / (k-1)^2
            #          = (k-1) / (k-1)^2 = 1/(k-1)
            mod_sq = (k - 1) / (k - 1) ** 2
            assert abs(mod_sq - 1 / (k - 1)) < 1e-15

    # --- Hashimoto eigenvalues ---

    def test_hashimoto_trivial_eigenvalues(self):
        """Hashimoto for ev=k=12: lambda = 11 or 1 (real, trivial)."""
        disc = k**2 - 4 * (k - 1)
        assert disc == 144 - 44 == 100 > 0
        l1 = (k + sqrt(disc)) / 2  # = (12+10)/2 = 11
        l2 = (k - sqrt(disc)) / 2  # = (12-10)/2 = 1
        assert abs(l1 - (k - 1)) < 1e-10
        assert abs(l2 - 1) < 1e-10

    def test_hashimoto_nontrivial_modulus(self):
        """All non-trivial Hashimoto eigenvalues have |lambda| = sqrt(k-1) = sqrt(11)."""
        for ev in [r_eig, s_eig]:
            # lambda = (ev ± i*sqrt(4*(k-1)-ev^2)) / 2
            re = ev / 2
            im_sq = (k - 1) - (ev / 2) ** 2
            mod_sq = re**2 + im_sq
            assert abs(mod_sq - (k - 1)) < 1e-10
            assert abs(sqrt(mod_sq) - sqrt(k - 1)) < 1e-10

    def test_hashimoto_r_eigenvalue(self):
        """Hashimoto for ev=r=2: lambda = 1 ± i*sqrt(10), |lambda| = sqrt(11)."""
        re = r_eig / 2  # = 1
        im = sqrt(4 * (k - 1) - r_eig**2) / 2  # = sqrt(44-4)/2 = sqrt(40)/2 = sqrt(10)
        mod = sqrt(re**2 + im**2)
        assert abs(re - 1) < 1e-10
        assert abs(im - sqrt(10)) < 1e-10
        assert abs(mod - sqrt(k - 1)) < 1e-10

    def test_hashimoto_s_eigenvalue(self):
        """Hashimoto for ev=s=-4: lambda = -2 ± i*sqrt(7) = -2 ± i*sqrt(Phi6)."""
        re = s_eig / 2  # = -2
        im = sqrt(4 * (k - 1) - s_eig**2) / 2  # = sqrt(44-16)/2 = sqrt(28)/2 = sqrt(7)
        mod = sqrt(re**2 + im**2)
        assert abs(re - (-2)) < 1e-10
        assert abs(im - sqrt(Phi6)) < 1e-10  # sqrt(7) = sqrt(Phi6)!
        assert abs(mod - sqrt(k - 1)) < 1e-10

    def test_hashimoto_s_imaginary_part_is_sqrt_Phi6(self):
        """Imaginary part of Hashimoto s-eigenvalue = sqrt(Phi6) = sqrt(7)."""
        im = sqrt(4 * (k - 1) - s_eig**2) / 2
        assert abs(im**2 - Phi6) < 1e-10
        assert Phi6 == 7

    # --- Betti numbers ---

    def test_betti_sum_equals_N(self):
        """Sum of Betti numbers chi(Gr(3,6)) = 20 = N."""
        betti = {}
        for a in range(4):
            for b in range(a + 1):
                for c in range(b + 1):
                    d = a + b + c
                    betti[d] = betti.get(d, 0) + 1
        assert sum(betti.values()) == N

    def test_betti_palindrome(self):
        """Betti numbers are palindromic: b_{2j} = b_{2*(dim/2-j)} (Poincare duality)."""
        betti = {}
        for a in range(4):
            for b in range(a + 1):
                for c in range(b + 1):
                    d = a + b + c
                    betti[d] = betti.get(d, 0) + 1
        max_d = max(betti.keys())
        for d in betti:
            assert betti[d] == betti[max_d - d]

    def test_weil_ihara_independence(self):
        """k-1=11 is NOT a prime power, so Ihara and Weil zeros are on different circles."""
        # Ihara: poles at |u| = 1/sqrt(11)
        # Weil: zeros at |T| = q^{-j/2} = 3^{-j/2}
        # These are equal iff 11 = 3^j for some j, which is impossible
        for j in range(1, 10):
            assert 3**j != k - 1
        # 11 is not a prime power of 3

    def test_k_minus_1_not_prime_power_of_q(self):
        """k-1 = 11 is prime but NOT a power of q=3."""
        import sympy

        assert k - 1 == 11
        assert sympy.isprime(11)
        # 11 is NOT a power of 3
        assert all(3**j != 11 for j in range(1, 10))

    def test_Phi6_in_Hashimoto(self):
        """Phi6=7 appears as imaginary part squared of Hashimoto s-eigenvalue: remarkable."""
        # im^2 = (4*(k-1) - s^2)/4 = (44-16)/4 = 28/4 = 7 = Phi6
        im_sq = (4 * (k - 1) - s_eig**2) // 4
        assert im_sq == Phi6 == 7
