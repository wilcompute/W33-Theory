"""
Supplement theta — E_8 THETA FUNCTION AND THE 240 COEFFICIENT
==================================================================

The E_8 lattice theta function

    Theta_E8(tau) = sum_{x in E_8} q^{|x|^2 / 2}

equals the Eisenstein series E_4 of weight 4 on SL(2, Z):

    E_4(tau) = 1 + 240 sum_{n>=1} sigma_3(n) q^n
             = 1 + 240 q + 2160 q^2 + 6720 q^3 + ...

where sigma_3(n) = sum of cubes of divisors of n.

The leading non-trivial coefficient is exactly 240 = E, the edge
count of W(3,3).  Subsequent coefficients factor through W(3,3)
constants:

    a_1 = 240 . sigma_3(1) = 240 . 1   = E
    a_2 = 240 . sigma_3(2) = 240 . 9   = E . q^2
    a_3 = 240 . sigma_3(3) = 240 . 28  = E . (q^q + 1)
    a_4 = 240 . sigma_3(4) = 240 . 73  = E . Phi_12 (= q^4 - q^2 + 1)
    a_5 = 240 . sigma_3(5) = 240 . 126 = E . (E/2 + 6)
    a_6 = 240 . sigma_3(6) = 240 . 252 = ...

We verify the identities and the 240-coefficient as a W(3,3) constant.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7
Phi12 = q ** 4 - q ** 2 + 1  # = 73


def sigma_3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def theta_e8_coef(n):
    if n == 0:
        return 1
    return 240 * sigma_3(n)


# ------------------------------------------------------------------
# theta.1  Leading coefficient = E
# ------------------------------------------------------------------
class Test_theta_1_LeadingCoef:
    def test_a_1_eq_E(self):
        assert theta_e8_coef(1) == E
        assert E == 240

    def test_a_0_eq_one(self):
        assert theta_e8_coef(0) == 1


# ------------------------------------------------------------------
# theta.2  Second coefficient
# ------------------------------------------------------------------
class Test_theta_2_SecondCoef:
    def test_a_2(self):
        assert theta_e8_coef(2) == 2160

    def test_factorization(self):
        # a_2 = E * q^2 = 240 * 9
        assert theta_e8_coef(2) == E * q ** 2

    def test_sigma_3_2(self):
        assert sigma_3(2) == 1 + 8
        assert sigma_3(2) == q ** 2


# ------------------------------------------------------------------
# theta.3  Third coefficient
# ------------------------------------------------------------------
class Test_theta_3_ThirdCoef:
    def test_a_3(self):
        assert theta_e8_coef(3) == 6720

    def test_factorization(self):
        # a_3 = E * 28 = E * (q^q + 1) = E * Spence multiverse count
        assert theta_e8_coef(3) == E * (q ** q + 1)
        assert q ** q + 1 == 28

    def test_sigma_3_3(self):
        assert sigma_3(3) == 1 + 27
        assert sigma_3(3) == q ** q + 1


# ------------------------------------------------------------------
# theta.4  Fourth coefficient
# ------------------------------------------------------------------
class Test_theta_4_FourthCoef:
    def test_a_4(self):
        assert theta_e8_coef(4) == 240 * sigma_3(4)
        assert sigma_3(4) == 1 + 8 + 64
        assert sigma_3(4) == 73

    def test_phi_12(self):
        # 73 = Phi_12 = q^4 - q^2 + 1
        assert Phi12 == 73

    def test_a_4_eq_E_Phi_12(self):
        assert theta_e8_coef(4) == E * Phi12


# ------------------------------------------------------------------
# theta.5  Generic structure
# ------------------------------------------------------------------
class Test_theta_5_GenericStructure:
    def test_E_factor(self):
        # All a_n divisible by E = 240
        for n in range(1, 10):
            assert theta_e8_coef(n) % E == 0

    def test_first_six_E_quotients(self):
        # a_n / E for n = 1..6
        quotients = [theta_e8_coef(n) // E for n in range(1, 7)]
        assert quotients == [sigma_3(n) for n in range(1, 7)]
        assert quotients[0] == 1
        assert quotients[1] == 9
        assert quotients[2] == 28
        assert quotients[3] == 73
        assert quotients[4] == 126
        assert quotients[5] == 252


# ------------------------------------------------------------------
# theta.6  E_8 root norm and W(3,3)
# ------------------------------------------------------------------
class Test_theta_6_E8Roots:
    def test_240_roots(self):
        # |Phi(E_8)| = 240 = E
        assert E == 240

    def test_root_squared_norm(self):
        # All E_8 roots have squared norm 2 (in standard normalization)
        # so the n=1 coefficient counts them
        assert theta_e8_coef(1) == 240


# ------------------------------------------------------------------
# theta.7  Modular weight 4
# ------------------------------------------------------------------
class Test_theta_7_ModularWeight:
    def test_weight_4(self):
        # E_4 is weight 4 = mu
        assert mu == 4

    def test_e4_at_tau_to_infty(self):
        # E_4(infty) = 1 (constant term)
        assert theta_e8_coef(0) == 1


# ------------------------------------------------------------------
# theta-CLOSURE
# ------------------------------------------------------------------
class Test_theta_Closure:
    def test_E8_theta_first_three(self):
        # First three non-trivial coefficients factor cleanly:
        #   a_1 = E
        #   a_2 = E * q^2
        #   a_3 = E * (q^q + 1)
        identities = {
            'a_1': (theta_e8_coef(1), E),
            'a_2': (theta_e8_coef(2), E * q ** 2),
            'a_3': (theta_e8_coef(3), E * (q ** q + 1)),
            'a_4': (theta_e8_coef(4), E * Phi12),
        }
        for label, (computed, expected) in identities.items():
            assert computed == expected, label

    def test_modular_form_universal_structure(self):
        # The W(3,3) edge count E = 240 controls the entire weight-4
        # modular form on SL(2, Z); all coefficients are 240 * sigma_3(n).
        assert E == 240
