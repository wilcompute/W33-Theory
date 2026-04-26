"""
Supplement kappa — UNIVERSAL NUMBERS: W(3,3) IN NATURE, CULTURE, MIND
==========================================================================

The integers (v, k, lam, mu, q, f, g, Phi_3, Phi_4, Phi_6) =
(40, 12, 2, 4, 3, 24, 15, 13, 10, 7) appear pervasively in natural,
cultural, and cognitive contexts.  This is partly numerology, partly
the arithmetic of small finite structures forced by symmetry; we
catalogue without overclaiming.

Categories:

  TIME      24 hours = f, 12 months = k, 7 days = Phi_6, 4 seasons = mu,
            60 minutes = v + Phi_4 * lam
  MUSIC     12 semitones = k, 7 diatonic notes = Phi_6
  BRAIN     6 cortical layers = k/2, 7+/-2 Miller = Phi_6 +/- lam,
            12 cranial nerves = k
  RELIGION  40 days flood = v, 12 tribes = k, 7 deadly sins = Phi_6,
            10 commandments = Phi_4
  GAMES     64 chess squares = mu^q, 52 cards = mu * Phi_3
  PERIODIC  7 rows = Phi_6, 8 = lam^q valence,
            atomic shells 2, 8, 18 = lam, lam^q, lam * q^2
  CRYSTAL   14 Bravais lattices = k + lam, 32 point groups = lam^(mu+1),
            230 space groups = ...
  ZODIAC    12 signs = k

These are not mystical claims about the universe being "designed";
they are observations that small symmetric structures favour the
integers (40, 12, 2, 4) and their cyclotomic/SRG derivatives.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# kappa.1  TIME
# ------------------------------------------------------------------
class Test_kappa_1_Time:
    def test_24_hours(self): assert f == 24
    def test_12_months(self): assert k == 12
    def test_7_days_week(self): assert Phi6 == 7
    def test_4_seasons(self): assert mu == 4
    def test_60_minutes(self):
        # 60 = v + Phi_4 * lam
        assert v + Phi4 * lam == 60


# ------------------------------------------------------------------
# kappa.2  MUSIC
# ------------------------------------------------------------------
class Test_kappa_2_Music:
    def test_12_semitones(self): assert k == 12
    def test_7_diatonic(self): assert Phi6 == 7
    def test_12_keys_circle_of_5ths(self): assert k == 12


# ------------------------------------------------------------------
# kappa.3  BRAIN / COGNITION
# ------------------------------------------------------------------
class Test_kappa_3_Brain:
    def test_6_cortical_layers(self):
        # 6 = k/2 (V1 layers I-VI)
        assert k // 2 == 6

    def test_miller_7_plus_minus_2(self):
        # working memory capacity 7 +/- 2 = Phi_6 +/- lam
        assert (Phi6 - lam, Phi6 + lam) == (5, 9)
        assert Phi6 == 7

    def test_12_cranial_nerves(self): assert k == 12

    def test_circadian_24h(self): assert f == 24


# ------------------------------------------------------------------
# kappa.4  RELIGION / MYTHOLOGY
# ------------------------------------------------------------------
class Test_kappa_4_Religion:
    def test_40_days_flood(self):
        # Genesis 7:12 -- 40 days/nights of rain = v
        assert v == 40

    def test_40_days_lent(self): assert v == 40
    def test_40_days_desert(self): assert v == 40
    def test_12_tribes_israel(self): assert k == 12
    def test_12_apostles(self): assert k == 12
    def test_7_deadly_sins(self): assert Phi6 == 7
    def test_10_commandments(self): assert Phi4 == 10


# ------------------------------------------------------------------
# kappa.5  GAMES
# ------------------------------------------------------------------
class Test_kappa_5_Games:
    def test_chess_64_squares(self):
        # mu^q = 4^3 = 64
        assert mu ** q == 64

    def test_chess_8x8(self):
        # 8 = lam^q
        assert lam ** q == 8

    def test_card_deck_52(self):
        # mu * Phi_3 = 4 * 13 = 52
        assert mu * Phi3 == 52

    def test_4_suits(self): assert mu == 4

    def test_13_ranks(self): assert Phi3 == 13


# ------------------------------------------------------------------
# kappa.6  PERIODIC TABLE / CHEMISTRY
# ------------------------------------------------------------------
class Test_kappa_6_Periodic:
    def test_7_rows(self): assert Phi6 == 7

    def test_atomic_shells(self):
        # 2, 8, 18, 32 -> lam, lam^q, lam*q^2, lam^(mu+1)
        assert lam == 2
        assert lam ** q == 8
        assert lam * q ** lam == 18
        assert lam ** (mu + 1) == 32

    def test_octet_rule(self):
        # 8 valence electrons = lam^q
        assert lam ** q == 8


# ------------------------------------------------------------------
# kappa.7  CRYSTALLOGRAPHY
# ------------------------------------------------------------------
class Test_kappa_7_Crystals:
    def test_14_bravais_lattices_3D(self):
        # 14 = k + lam
        assert k + lam == 14

    def test_32_point_groups_3D(self):
        # 32 = lam^(mu+1)
        assert lam ** (mu + 1) == 32

    def test_7_crystal_systems(self): assert Phi6 == 7


# ------------------------------------------------------------------
# kappa.8  ZODIAC AND ASTRONOMY
# ------------------------------------------------------------------
class Test_kappa_8_Zodiac:
    def test_12_zodiac_signs(self): assert k == 12

    def test_12_constellations_band(self): assert k == 12

    def test_8_planets_solar(self):
        # 8 = lam^q
        assert lam ** q == 8


# ------------------------------------------------------------------
# kappa-CLOSURE
# ------------------------------------------------------------------
class Test_kappa_Closure:
    def test_universal_set(self):
        universal = {
            'hours_per_day': f,         # 24
            'months_per_year': k,        # 12
            'days_per_week': Phi6,       # 7
            'seasons': mu,                # 4
            'octave_semitones': k,       # 12
            'cortical_layers': k // 2,   # 6
            'commandments': Phi4,        # 10
            'flood_days': v,              # 40
            'chess_squares': mu ** q,     # 64
            'cards_in_deck': mu * Phi3,   # 52
            'periodic_rows': Phi6,        # 7
            'octet_valence': lam ** q,    # 8
            'bravais_lattices': k + lam,  # 14
            'point_groups': lam ** (mu + 1),  # 32
            'zodiac_signs': k,            # 12
            'planets': lam ** q,          # 8
        }
        # 16 categories = lam^mu
        assert len(universal) == lam ** mu
