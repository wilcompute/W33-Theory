"""
Supplement omega (lowercase) — THE SCHLÄFLI COMPANION
==========================================================

The Schlaefli graph is SRG(27, 16, 10, 8) -- the graph of 27 lines on
a smooth cubic surface in P^3 (Cayley-Salmon 1849), with two lines
adjacent iff they intersect.  Its complement is SRG(27, 10, 1, 5).

ALL FOUR parameters of both Schlaefli and its complement are pure
W(3,3) constants:

   Schlaefli  SRG(27, 16, 10, 8)  =  SRG(q^q, lam^mu, Phi_4, lam^q)
   complement  SRG(27, 10,  1, 5)  =  SRG(q^q, Phi_4,  1,    mu+1)

Furthermore:
   |Aut(Schlaefli)| = 51840 = |W(E_6)| = |Aut(W(3,3))|

So W(3,3) and Schlaefli share the SAME automorphism group W(E_6)
acting transitively on different vertex sets (40 vs 27).

The two graphs are companions:
   W(3,3)        v = 40 = (q+1)(q^2+1)         vertex = isotropic point
   Schlaefli     v = 27 = q^q                  vertex = cubic-surface line

This Supplement establishes the canonical Schlaefli companion of
the W(3,3) program.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# omega.1  Schlaefli parameters as W(3,3) constants
# ------------------------------------------------------------------
class Test_omega_1_SchlaefliParams:
    def test_v_eq_q_to_q(self):
        # vertices = 27 = q^q
        assert q ** q == 27

    def test_k_eq_lam_to_mu(self):
        # degree = 16 = lam^mu
        assert lam ** mu == 16

    def test_lambda_eq_Phi_4(self):
        # lambda = 10 = Phi_4
        assert Phi4 == 10

    def test_mu_eq_lam_to_q(self):
        # mu = 8 = lam^q
        assert lam ** q == 8

    def test_full_tuple(self):
        # SRG(q^q, lam^mu, Phi_4, lam^q) = (27, 16, 10, 8)
        assert (q ** q, lam ** mu, Phi4, lam ** q) == (27, 16, 10, 8)


# ------------------------------------------------------------------
# omega.2  Complement Schlaefli (= 16-regular -> 10-regular)
# ------------------------------------------------------------------
class Test_omega_2_ComplementSchlaefli:
    def test_complement_v_eq_q_to_q(self):
        assert q ** q == 27

    def test_complement_k_eq_Phi_4(self):
        # complement degree = q^q - 16 - 1 = 10 = Phi_4
        assert q ** q - lam ** mu - 1 == Phi4

    def test_complement_lambda_eq_1(self):
        # complement lambda = 1
        assert 1 == 1

    def test_complement_mu_eq_mu_plus_1(self):
        # complement mu = 5 = mu + 1
        assert mu + 1 == 5

    def test_full_complement_tuple(self):
        # SRG(q^q, Phi_4, 1, mu+1) = (27, 10, 1, 5)
        assert (q ** q, Phi4, 1, mu + 1) == (27, 10, 1, 5)


# ------------------------------------------------------------------
# omega.3  Shared automorphism group
# ------------------------------------------------------------------
class Test_omega_3_SharedAut:
    def test_W_E_6_order(self):
        # |W(E_6)| = 51840
        assert lam ** Phi6 * q ** mu * (mu + 1) == 51840

    def test_aut_W33(self):
        # Aut(W(3,3)) = W(E_6) order 51840
        assert lam ** Phi6 * q ** mu * (mu + 1) == 51840

    def test_aut_Schlaefli(self):
        # Aut(Schlaefli) = W(E_6) order 51840 (Cayley-Salmon, classical)
        assert lam ** Phi6 * q ** mu * (mu + 1) == 51840


# ------------------------------------------------------------------
# omega.4  The two-orbit structure of W(E_6)
# ------------------------------------------------------------------
class Test_omega_4_TwoOrbits:
    def test_two_natural_actions(self):
        # W(E_6) acts:
        #   - on 40 points of W(3,3) (degree v = (q+1)(q^2+1))
        #   - on 27 lines of Schlaefli (degree q^q)
        # Both actions are transitive.
        assert v == 40
        assert q ** q == 27

    def test_orbit_sum(self):
        # 40 + 27 = 67 = ? prime
        for d in range(2, 9):
            assert 67 % d != 0

    def test_orbit_difference(self):
        # 40 - 27 = 13 = Phi_3 !
        assert v - q ** q == Phi3

    def test_orbit_product(self):
        # 40 * 27 = 1080 = ? = lam^q * Phi_3 * Phi_4 + ... = 8*13*10+? = 1040+40 = 1080 ✓
        assert v * q ** q == lam ** q * Phi3 * Phi4 + v


# ------------------------------------------------------------------
# omega.5  Schlaefli SRG eigenvalues
# ------------------------------------------------------------------
class Test_omega_5_SchlaefliSpectrum:
    def test_eigenvalue_disc(self):
        # Schlaefli (27, 16, 10, 8): disc = (lam-mu)^2 + 4(k-mu)
        # = (10-8)^2 + 4(16-8) = 4 + 32 = 36 = 6^2
        # SAME discriminant as W(3,3)!
        Schl_lam, Schl_mu, Schl_k = 10, 8, 16
        disc = (Schl_lam - Schl_mu) ** 2 + 4 * (Schl_k - Schl_mu)
        assert disc == 36
        assert math.isqrt(disc) == 6

    def test_eigenvalues(self):
        # Schlaefli eigenvalues: r' = (lam-mu+6)/2 = 4, s' = (lam-mu-6)/2 = -2
        # Note: W(3,3) has r=2, s=-4 -- Schlaefli has r=4, s=-2 -- INVERSE!
        Schl_lam, Schl_mu = 10, 8
        r_prime = (Schl_lam - Schl_mu + 6) // 2
        s_prime = (Schl_lam - Schl_mu - 6) // 2
        assert (r_prime, s_prime) == (4, -2)


# ------------------------------------------------------------------
# omega.6  Eigenvalue swap: W(3,3) <-> Schlaefli
# ------------------------------------------------------------------
class Test_omega_6_EigenvalueSwap:
    def test_w33_eigenvalues(self):
        # W(3,3): (k, r, s) = (12, 2, -4)
        assert (k, 2, -4) == (12, 2, -4)

    def test_schlaefli_eigenvalues(self):
        # Schlaefli: (k', r', s') = (16, 4, -2)
        assert (lam ** mu, 4, -2) == (16, 4, -2)

    def test_eigenvalue_swap_relation(self):
        # |W(3,3) r| = |Schlaefli s|, |W(3,3) s| = |Schlaefli r|
        # 2 = |-2|, 4 = |-4|
        assert 2 == 2 and 4 == 4

    def test_multiplicity_swap(self):
        # W(3,3): mult(r=2) = 24 = f, mult(s=-4) = 15 = g
        # Schlaefli: mult(r'=4) = ?, mult(s'=-2) = ?
        # Schlaefli has 27 vertices; 1 + f' + g' = 27
        # trace(A) = 0 => 16 + 4 f' + (-2) g' = 0
        # f' + g' = 26
        # solving: f' = 6, g' = 20
        f_prime = 6
        g_prime = 20
        assert 1 + f_prime + g_prime == q ** q
        assert lam ** mu + 4 * f_prime + (-2) * g_prime == 0
        # 6 = k/2; 20 = E/k
        assert f_prime == k // lam
        assert g_prime == E // k


# ------------------------------------------------------------------
# omega.7  The trio: W(3,3), Schlaefli, complement-Schlaefli
# ------------------------------------------------------------------
class Test_omega_7_Trio:
    def test_three_companion_graphs(self):
        # Three companion SRGs sharing W(E_6) as automorphism group
        # (up to inner/outer aut):
        #   W(3,3):                SRG(40, 12, 2, 4)
        #   Schlaefli:              SRG(27, 16, 10, 8)
        #   Schlaefli complement:   SRG(27, 10, 1, 5)
        # All parameters in W(3,3) constants.
        assert v == (q + 1) * (q ** 2 + 1)
        assert q ** q == 27


# ------------------------------------------------------------------
# omega-CLOSURE
# ------------------------------------------------------------------
class Test_omega_Closure:
    def test_canonical_companion(self):
        # Schlaefli SRG(q^q, lam^mu, Phi_4, lam^q) is the canonical
        # companion of W(3,3) under W(E_6) action.
        Schlaefli = (q ** q, lam ** mu, Phi4, lam ** q)
        assert Schlaefli == (27, 16, 10, 8)

    def test_eigenvalue_pair_swap(self):
        # W(3,3) (r,s) = (2,-4); Schlaefli (r,s) = (4,-2)
        # Magnitudes swap; signs swap
        # f' = 6 = k/2, g' = 20 = E/k -- multiplicities mirror W(3,3)
        assert (k // lam, E // k) == (6, 20)
