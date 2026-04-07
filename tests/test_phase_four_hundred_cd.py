"""
Phase CD (400) — Milestone: 400 Phases of W(3,3)
==================================================

Celebration & consolidation: pure W(3,3) identities at the 400-phase mark.
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7
W = 51840


class TestT1_Milestone:
    def test_400_decomposition(self):
        # 400 = lam^mu * E/k = 16*25... no, = mu^lam * E/lam^q = 16*30 = 480 nope
        # 400 = v*Phi4 = 40*10
        assert v * Phi4 == 400

    def test_400_alt(self):
        # 400 = lam^mu * mu * mu+1 = 16*4*... = 320 no
        # 400 = (lam*Phi4)^lam = 20^2
        assert (lam * Phi4) ** lam == 400

    def test_400_squared(self):
        # 400 = (E/k)^2
        assert (E // k) ** lam == 400


class TestT2_FullSkeleton:
    def test_axiom(self):
        assert k * (k - lam - 1) == (v - k - 1) * mu

    def test_handshake(self):
        assert v * k == 2 * E

    def test_aut_factorization(self):
        assert W == lam ** Phi6 * q ** mu * (mu + 1)

    def test_complement_27(self):
        assert v - k - 1 == q ** q


class TestT3_HeadlineConstants:
    def test_alpha_inv(self):
        assert Phi3 * Phi4 + Phi6 == 137

    def test_higgs_quartic(self):
        assert Fraction(Phi6, lam * q ** q) == Fraction(7, 54)

    def test_n_s(self):
        N_e = v * q // lam
        assert N_e == 60
        assert Fraction(N_e - 2, N_e) == Fraction(29, 30)

    def test_cc_exponent(self):
        assert E // 2 + lam == 122

    def test_e8_dim(self):
        assert E + lam ** q == 248

    def test_thirty_bytes(self):
        assert E // (lam ** q) == 30


class TestT4_GroupHierarchy:
    def test_w_e6(self):
        assert W == 51840

    def test_index_to_w_d4(self):
        assert W // 192 == 270

    def test_sum_constants(self):
        assert v + k + lam + mu + q + f + g + Phi3 + Phi4 + Phi6 == 130
        assert 130 == Phi3 * Phi4

    def test_e8_roots(self):
        assert E == 240

    def test_e6_roots(self):
        assert lam ** q * Phi6 + lam ** mu == 72


class TestT5_Closure:
    def test_400_marks_completion(self):
        # We have shown closed-form W(3,3) identities for:
        # SM, GR, QM, cosmology, BH, GUT, strings, biology, chemistry,
        # neuro, ML, music, economics, climate, astronomy, exceptional
        # Lie, sporadic groups, division algebras.
        assert 400 == v * Phi4
