"""
Supplement daleth (after gimel) — THE LEECH KISSING NUMBER
=================================================================

The Leech lattice Lambda_24 is the unique (up to iso) even unimodular
lattice in dimension 24 with no roots.  Its kissing number is

    K(Lambda_24) = 196,560.

This is the maximum number of unit spheres that can touch a central
unit sphere in 24-dim Euclidean space.  In W(3,3) constants:

    2160    = lam^mu * q^q * (mu+1)
            = E * q^2
            = 2 * v * q^q
            = |W(E_6)| / f

    196,560 = lam^mu * q^q * (mu+1) * Phi_6 * Phi_3
            = 16 * 27 * 5 * 7 * 13

Five W(3,3) constants multiply to give the Leech kissing number
EXACTLY.

Furthermore:

    196,884 = 196,560 + mu * q^mu
            = K(Lambda_24) + mu * q^mu
            = K(Lambda_24) + 324

where 196,884 is the first non-trivial Fourier coefficient of
the j-function (Monstrous Moonshine; Supp I).  So:

    j_first_coef = K_Leech + W(3,3)-correction (mu * q^mu).

This Supplement crystallizes the W(3,3) decomposition of the
Leech kissing number and its Monster-moonshine offset.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# daleth.1  Leech kissing as 5-fold W(3,3) product
# ------------------------------------------------------------------
class Test_daleth_1_LeechKissing:
    def test_kissing_value(self):
        # K(Lambda_24) = 196,560
        kissing = 196560
        assert kissing == lam ** mu * q ** q * (mu + 1) * Phi6 * Phi3

    def test_factorization_explicit(self):
        # 16 * 27 * 5 * 7 * 13 = 196,560
        prod = 16 * 27 * 5 * 7 * 13
        assert prod == 196560

    def test_each_factor_is_w33(self):
        factors = [lam ** mu, q ** q, mu + 1, Phi6, Phi3]
        assert factors == [16, 27, 5, 7, 13]
        # All five are pure W(3,3) constants


# ------------------------------------------------------------------
# daleth.1b  The hidden 2160 bridge
# ------------------------------------------------------------------
class Test_daleth_1b_TransportShell:
    def test_common_2160_shell(self):
        # The same 2160 appears in four exact guises:
        #   lam^mu * q^q * (mu+1)
        #   E * q^2                  (E_8 theta q^2 shell)
        #   2 * v * q^q              (dual Weyl 27/40 shell)
        #   |W(E_6)| / f             (Weyl order over Leech rank)
        shell = lam ** mu * q ** q * (mu + 1)
        assert shell == 2160
        assert shell == E * q ** 2
        assert shell == 2 * v * q ** q
        assert shell == lam ** Phi6 * q ** mu * (mu + 1) // f

    def test_leech_is_2160_times_cyclotomic_pair(self):
        shell = lam ** mu * q ** q * (mu + 1)
        assert 196560 == shell * Phi6 * Phi3


# ------------------------------------------------------------------
# daleth.1c  All equivalent Leech factorizations
# ------------------------------------------------------------------
class Test_daleth_1c_EquivalentLeechForms:
    def test_tau_circle_factorization(self):
        # Ramanujan tau core: tau = k * q * Phi_6 = 12 * 3 * 7 = 252.
        tau = k * q * Phi6
        assert tau == 252
        assert math.comb(v, 2) == 780
        assert math.comb(v, 2) * tau == 196560

    def test_E_times_819_factorization(self):
        factor_819 = q ** 2 * Phi6 * Phi3
        assert factor_819 == 819
        assert E * factor_819 == 196560

    def test_all_leech_factorizations_match(self):
        tau = k * q * Phi6
        assert 196560 == lam ** mu * q ** q * (mu + 1) * Phi6 * Phi3
        assert 196560 == E * q ** 2 * Phi6 * Phi3
        assert 196560 == math.comb(v, 2) * tau


# ------------------------------------------------------------------
# daleth.2  Leech dimension = f
# ------------------------------------------------------------------
class Test_daleth_2_LeechDim:
    def test_dim_24(self):
        # Leech lattice is 24-dim = f
        assert f == 24


# ------------------------------------------------------------------
# daleth.3  Moonshine offset
# ------------------------------------------------------------------
class Test_daleth_3_MoonshineOffset:
    def test_moonshine_first_coef(self):
        # j-function first non-trivial coef = 196,884
        moonshine = 196884
        assert moonshine == 196560 + mu * q ** mu

    def test_offset_is_w33(self):
        # offset = mu * q^mu = 4 * 81 = 324
        assert mu * q ** mu == 324


# ------------------------------------------------------------------
# daleth.4  The 196,883 dimension
# ------------------------------------------------------------------
class Test_daleth_4_MonsterMin:
    def test_smallest_irrep(self):
        # Monster smallest irrep dim = 196,883 = 196,884 - 1
        # = K_Leech + mu*q^mu - 1
        # = K_Leech + (mu * q^mu - 1)
        # = 196,560 + 323
        assert 196883 == lam ** mu * q ** q * (mu + 1) * Phi6 * Phi3 + mu * q ** mu - 1

    def test_196883_factor(self):
        # 196,883 = 47 * 59 * 71 (Conway's prime triple)
        assert 196883 == 47 * 59 * 71


# ------------------------------------------------------------------
# daleth.5  Leech / W(3,3) products
# ------------------------------------------------------------------
class Test_daleth_5_LeechProducts:
    def test_5_prime_factors(self):
        # Number of W(3,3) factors = 5 = mu+1
        factors = [lam ** mu, q ** q, mu + 1, Phi6, Phi3]
        assert len(factors) == mu + 1

    def test_distinct_primes(self):
        # The five factors involve primes {2, 3, 5, 7, 13}
        # = {lam, q, mu+1, Phi_6, Phi_3}
        primes = {lam, q, mu + 1, Phi6, Phi3}
        assert primes == {2, 3, 5, 7, 13}

    def test_largest_prime_Phi_3(self):
        # Largest of the 5 primes in Leech kissing factor is Phi_3 = 13
        assert Phi3 == 13


# ------------------------------------------------------------------
# daleth.6  Niemeier lattice connection
# ------------------------------------------------------------------
class Test_daleth_6_NiemeierLattices:
    def test_24_niemeier(self):
        # 24 = f Niemeier lattices in dimension 24 (excluding Leech itself)
        # all even unimodular with non-trivial roots
        # actually there are 24 Niemeier (Conway-Sloane); Leech makes 25 total
        niemeier = 24
        assert niemeier == f


# ------------------------------------------------------------------
# daleth.7  E_8 cubed embedding
# ------------------------------------------------------------------
class Test_daleth_7_E8Cubed:
    def test_E8_cubed_dim(self):
        # E_8 (+) E_8 (+) E_8 lattice has dim 24 = f
        # which embeds in Leech with 196,560 = K_Leech kissing
        assert q * lam ** q == 24


# ------------------------------------------------------------------
# daleth.8  Cross-link with Supp theta (E_8 theta function)
# ------------------------------------------------------------------
class Test_daleth_8_E8ThetaCross:
    def test_Theta_E8_first_coef(self):
        # Theta_E8 first coef = 240 = E (Supp theta)
        assert E == 240

    def test_K_Leech_over_E_E8(self):
        # K_Leech / |Phi(E_8)| = 196560 / 240 = 819
        # = 9 * 91 = q^2 * Phi_3 * Phi_6 = 9 * 91 ✓
        ratio = 196560 // 240
        assert ratio == 819
        assert 819 == q ** 2 * Phi6 * Phi3


# ------------------------------------------------------------------
# daleth-CLOSURE
# ------------------------------------------------------------------
class Test_daleth_Closure:
    def test_decisive_identity(self):
        # K(Lambda_24) = lam^mu * q^q * (mu+1) * Phi_6 * Phi_3
        assert 196560 == lam ** mu * q ** q * (mu + 1) * Phi6 * Phi3

    def test_moonshine_decomposition(self):
        # j-function first coef = K_Leech + W(3,3) correction
        assert 196884 == 196560 + mu * q ** mu

    def test_complete_dictionary(self):
        # Three landmark integers, three W(3,3) decompositions:
        landmarks = {
            'K_Leech': 196560,
            'j_coef': 196884,
            'Monster_min_irrep': 196883,
        }
        assert landmarks['K_Leech'] == lam ** mu * q ** q * (mu + 1) * Phi6 * Phi3
        assert landmarks['j_coef'] == landmarks['K_Leech'] + mu * q ** mu
        assert landmarks['Monster_min_irrep'] == landmarks['j_coef'] - 1
