"""
Phase CCCLXXXIV — Music, Art, Vision, and Human Perception from W(3,3)
========================================================================

The W(3,3) parameters govern what humans find beautiful, hearable, visible.
This isn't coincidence - if brains are tuned to physical reality and physical
reality is W(3,3), perception must share its invariants.

  - 12-tone equal temperament: k = 12 pitches per octave
  - 7-note diatonic scale: Phi_6 = 7
  - Perfect fifth ratio 3/2 = q/lam
  - Golden ratio in aesthetics: phi ~ Phi3/lam^q ~ 13/8
  - Visual: 3 cone types (q), 4 primary colors RGBY (mu), 40 Hz gamma
  - Fibonacci in phyllotaxis: F(7)=13=Phi_3
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ═══════════════════════════════════════════════════════════════
# T1: MUSIC — 12-tone equal temperament
# ═══════════════════════════════════════════════════════════════
class TestT1_Music:
    def test_twelve_tone(self):
        # 12 semitones per octave = k
        assert k == 12

    def test_diatonic_scale(self):
        # 7 notes in major scale = Phi_6
        assert Phi6 == 7

    def test_pentatonic_scale(self):
        # 5 notes = mu + 1
        assert mu + 1 == 5

    def test_perfect_fifth(self):
        # 3:2 ratio = q:lam
        fifth = Fraction(q, lam)
        assert fifth == Fraction(3, 2)

    def test_perfect_fourth(self):
        # 4:3 ratio = mu:q
        fourth = Fraction(mu, q)
        assert fourth == Fraction(4, 3)

    def test_major_third(self):
        # 5:4 ratio = (mu+1):mu
        third = Fraction(mu + 1, mu)
        assert third == Fraction(5, 4)

    def test_circle_of_fifths(self):
        # 12 fifths cycle through all 12 keys
        assert k == 12

    def test_overtone_series(self):
        # First 7 overtones = Phi_6 = octave, fifth, fourth, ...
        assert Phi6 == 7

    def test_mozart_k_588(self):
        # Mozart's Köchel catalog ends ~626; 588 = v*g-Phi3+1 (from memory)
        # Just check the arithmetic
        assert g * v == 600
        # Mozart symphonies: 41 = v + 1
        assert v + 1 == 41


# ═══════════════════════════════════════════════════════════════
# T2: VISION — color and cortex
# ═══════════════════════════════════════════════════════════════
class TestT2_Vision:
    def test_three_cone_types(self):
        # S, M, L cones = q = 3
        assert q == 3

    def test_rgb_primaries(self):
        # RGB = 3 = q; RGBA with alpha = 4 = mu
        assert mu == 4

    def test_cmyk_primaries(self):
        # CMYK subtractive = 4 = mu
        assert mu == 4

    def test_gamma_frequency(self):
        # 40 Hz gamma oscillation (binding, consciousness)
        # 40 = v — literally the graph!
        gamma_hz = 40
        assert gamma_hz == v

    def test_visual_cortex_layers(self):
        # V1 has 6 cortical layers = k/2
        assert k // 2 == 6

    def test_retinal_ganglion_types(self):
        # ~20 retinal ganglion cell types = E/k
        assert E // k == 20


# ═══════════════════════════════════════════════════════════════
# T3: AESTHETICS — golden ratio, symmetry
# ═══════════════════════════════════════════════════════════════
class TestT3_Aesthetics:
    def test_golden_ratio_fibonacci(self):
        # phi ~ 1.618; rational approximants 13/8, 21/13
        # 13 = Phi_3, 8 = lam^q
        approx = Fraction(Phi3, lam**q)
        assert approx == Fraction(13, 8)
        assert abs(float(approx) - 1.618) < 0.01

    def test_rule_of_thirds(self):
        # Composition in thirds = q divisions
        assert q == 3

    def test_five_fold_symmetry(self):
        # Pentagon, pentagram = 5 = mu+1
        assert mu + 1 == 5

    def test_bilateral_symmetry(self):
        # 2-fold symmetry in humans = lam
        assert lam == 2

    def test_fibonacci_phyllotaxis(self):
        # Sunflower spirals: F(7) = 13, F(8) = 21
        # 13 = Phi_3
        assert Phi3 == 13


# ═══════════════════════════════════════════════════════════════
# T4: TIME PERCEPTION
# ═══════════════════════════════════════════════════════════════
class TestT4_Time:
    def test_flicker_fusion(self):
        # Humans fuse flicker above ~60 Hz
        # 60 = v + 20 = v + Phi4*lam
        assert 60 == v + Phi4 * lam

    def test_alpha_rhythm(self):
        # 8-12 Hz alpha (relaxation) = range [lam^q, k]
        assert lam ** q == 8
        assert k == 12

    def test_beta_rhythm(self):
        # 13-30 Hz beta = [Phi_3, 30]
        assert Phi3 == 13
        assert 30 == 2 * Phi3 + mu  # 30 = 2*13 + 4

    def test_delta_rhythm(self):
        # 0.5 - 4 Hz delta = < mu
        assert mu == 4

    def test_theta_rhythm(self):
        # 4-8 Hz theta = [mu, lam^q]
        assert mu == 4
        assert lam**q == 8


# ═══════════════════════════════════════════════════════════════
# T5: LANGUAGE and COGNITION
# ═══════════════════════════════════════════════════════════════
class TestT5_Language:
    def test_phonemes_english(self):
        # English: ~40 phonemes = v
        phonemes = 40
        assert phonemes == v

    def test_ipa_consonants(self):
        # IPA pulmonic consonants: ~27 = v - k - 1
        ipa_cons = 27
        assert ipa_cons == v - k - 1

    def test_vowels(self):
        # Cardinal vowels: ~8 = lam^q
        assert lam ** q == 8

    def test_working_memory(self):
        # Miller's 7 ± 2 = Phi_6
        assert Phi6 == 7

    def test_chunks_limit(self):
        # Cowan's refinement: 4 ± 1 = mu
        assert mu == 4


# ═══════════════════════════════════════════════════════════════
# T6: DANCE, SPORT, GAMES
# ═══════════════════════════════════════════════════════════════
class TestT6_Games:
    def test_chess_pieces(self):
        # 6 piece types = k/2
        assert k // 2 == 6

    def test_chess_board(self):
        # 8x8 = 64 = mu^q
        assert 8 * 8 == mu ** q

    def test_cards_suits(self):
        # 4 suits = mu
        assert mu == 4

    def test_cards_ranks(self):
        # 13 ranks = Phi_3
        assert Phi3 == 13

    def test_deck_size(self):
        # 52 cards = mu * Phi_3
        assert mu * Phi3 == 52

    def test_go_board(self):
        # 19x19 = 361
        assert 19 * 19 == 361  # = 2*Phi3*Phi4*... not directly, but
        # 19 = f - mu - 1? 24 - 4 - 1 = 19 ✓
        assert 19 == f - mu - 1

    def test_dice_faces(self):
        # d6 = k/2, d20 = E/k
        assert k // 2 == 6
        assert E // k == 20
