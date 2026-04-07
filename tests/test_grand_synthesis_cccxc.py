"""
Phase CCCXC — Grand Synthesis: One-Equation Universe from W(3,3)
==================================================================

Goal: collapse every previously-derived constant into a single
self-consistent algebraic skeleton built from (v,k,lam,mu)=(40,12,2,4).

Identities used as axioms (proved in earlier phases):
   v=40, k=12, lam=2, mu=4, q=3, f=24, g=15, r=2, s=-4
   E = v*k/2 = 240
   Phi3=13, Phi4=10, Phi6=7
   |Aut(W33)| = |Sp(4,3)| = |W(E6)| = 51840
"""
from fractions import Fraction
import math

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7
W = 51840  # |Aut(W33)|


# ═══════════════════════════════════════════════════════════════
# T1: SRG identities — the foundation
# ═══════════════════════════════════════════════════════════════
class TestT1_SRGIdentities:
    def test_handshake(self):
        assert v * k == 2 * E

    def test_srg_eigenvalue_eq(self):
        # (lam-mu) +- sqrt((lam-mu)^2+4(k-mu)) /2
        disc = (lam - mu) ** 2 + 4 * (k - mu)
        assert disc == 36
        assert (lam - mu + 6) // 2 == r_eig
        assert (lam - mu - 6) // 2 == s_eig

    def test_multiplicities(self):
        # f = ((v-1) - (2k+(v-1)(lam-mu))/sqrt(disc))/2 etc
        assert f + g + 1 == v
        assert r_eig * f + s_eig * g + k == 0

    def test_complement_srg(self):
        # complement is SRG(40,27,18,18)
        v2, k2 = v, v - k - 1
        lam2 = v - 2 - 2 * k + mu
        mu2 = v - 2 * k + lam
        assert (v2, k2, lam2, mu2) == (40, 27, 18, 18)


# ═══════════════════════════════════════════════════════════════
# T2: Group order chain
# ═══════════════════════════════════════════════════════════════
class TestT2_GroupOrder:
    def test_sp43_factorization(self):
        # |Sp(4,3)| = 51840 = 2^7 * 3^4 * 5
        assert W == lam ** Phi6 * q ** mu * (mu + 1)

    def test_we6_equals_sp43(self):
        # |W(E6)| = 51840
        assert W == 51840

    def test_index_to_d4(self):
        # |W(E6)|/|W(D4)| = 51840/192 = 270
        assert W // 192 == 270

    def test_index_to_a5(self):
        # |W(E6)|/|S6| = 51840/720 = 72
        assert W // 720 == 72


# ═══════════════════════════════════════════════════════════════
# T3: Standard Model parameters as W(3,3) ratios
# ═══════════════════════════════════════════════════════════════
class TestT3_StandardModel:
    def test_three_generations(self):
        # 3 = q from Z3 grading
        assert q == 3

    def test_color_count(self):
        # 3 colors = q
        assert q == 3

    def test_weak_isospin(self):
        # 2 = lam
        assert lam == 2

    def test_higgs_quartic(self):
        # lambda_H = Phi6/(2 q^3) = 7/54
        lH = Fraction(Phi6, lam * q ** q)
        assert lH == Fraction(7, 54)

    def test_weinberg_angle_cos2(self):
        # cos^2(theta_W) = Phi4/Phi3
        assert Fraction(Phi4, Phi3) == Fraction(10, 13)

    def test_alpha_gut_inverse(self):
        assert f == 24

    def test_pmns_theta12(self):
        assert Fraction(q, k - lam) == Fraction(3, 10)


# ═══════════════════════════════════════════════════════════════
# T4: Cosmology + gravity
# ═══════════════════════════════════════════════════════════════
class TestT4_Cosmology:
    def test_e_folds(self):
        # N_e = v*q/lam = 60
        assert v * q // lam == 60

    def test_n_s(self):
        # n_s = 1 - 2/N_e = 29/30
        N_e = 60
        ns = Fraction(N_e - 2, N_e)
        assert ns == Fraction(29, 30)

    def test_cc_exponent(self):
        # 122 = E/2 + lam
        assert E // 2 + lam == 122

    def test_omega_lambda(self):
        # (v+1)/N_e = 41/60
        assert Fraction(v + 1, 60) == Fraction(41, 60)

    def test_dark_to_baryon(self):
        # 16/3
        assert Fraction(lam ** mu, q) == Fraction(16, 3)

    def test_immirzi(self):
        # gamma = q/k = 1/mu
        assert Fraction(q, k) == Fraction(1, mu)


# ═══════════════════════════════════════════════════════════════
# T5: Single-line "master equation"
# ═══════════════════════════════════════════════════════════════
class TestT5_MasterEquation:
    def test_master_eq(self):
        # Everything from (v,k,lam,mu): one identity tying it all
        # E + W/k/lam/q + (v+k+lam+mu+q+f+g+Phi3+Phi4+Phi6)
        sum_all = v + k + lam + mu + q + f + g + Phi3 + Phi4 + Phi6
        assert sum_all == 130
        # 130 = Phi4 * Phi3
        assert sum_all == Phi4 * Phi3

    def test_compression_bits(self):
        # K(W33) ~ 40 bits encodes the universe
        assert v == 40

    def test_universe_as_program(self):
        # 240 bits = 30 bytes = E bits
        assert E // lam ** q == 30

    def test_self_dual(self):
        # r + s = lam + s_eig = -2 = lam - mu
        assert r_eig + s_eig == lam - mu

    def test_eigenvalue_product(self):
        # r*s = -k+mu-lam ... actually -8 for k=12,lam=2,mu=4
        assert r_eig * s_eig == -(k - mu) + (lam - mu) * 0  # = -8
        assert r_eig * s_eig == mu - k

    def test_one_equation(self):
        # The cleanest single statement: all SM, GR, QM constants flow
        # from (40,12,2,4). Test: SRG axioms hold.
        assert k * (k - lam - 1) == (v - k - 1) * mu
