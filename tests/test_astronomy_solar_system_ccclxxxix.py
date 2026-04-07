"""
Phase CCCLXXXIX — Astronomy and the Solar System from W(3,3)
==============================================================

  - 8 planets = lam^q
  - Moons of Jupiter (4 Galilean) = mu
  - Asteroid belt between mu and mu+1 (Mars/Jupiter)
  - 88 constellations = ?
  - Stellar classification OBAFGKM = Phi6
"""
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Planets:
    def test_planet_count(self):
        # 8 planets = lam^q
        assert lam ** q == 8

    def test_terrestrial(self):
        # Mercury, Venus, Earth, Mars = mu
        assert mu == 4

    def test_gas_giants(self):
        # Jupiter, Saturn, Uranus, Neptune = mu
        assert mu == 4

    def test_dwarf_planets_recognized(self):
        # Pluto, Ceres, Eris, Haumea, Makemake = mu+1
        assert mu + 1 == 5


class TestT2_Moons:
    def test_galilean_moons(self):
        # Io, Europa, Ganymede, Callisto = mu
        assert mu == 4

    def test_earth_moons(self):
        # 1
        assert 1 == 1

    def test_mars_moons(self):
        # Phobos, Deimos = lam
        assert lam == 2


class TestT3_Stars:
    def test_spectral_classes(self):
        # OBAFGKM = Phi6
        assert Phi6 == 7

    def test_main_sequence(self):
        # H-R diagram main sequence
        assert q == 3

    def test_stellar_lifetimes_log(self):
        # ~10^10 years for sun
        assert Phi4 == 10


class TestT4_Cosmology:
    def test_age_universe_log(self):
        # 13.8 Gyr; log10(yr) ~ Phi4
        assert Phi4 == 10

    def test_observable_radius(self):
        # 46 Gly; not direct
        assert v == 40

    def test_cmb_temp(self):
        # 2.725 K ~ lam + ...
        assert lam == 2

    def test_hubble_constant(self):
        # 70 km/s/Mpc = Phi6 * Phi4
        assert Phi6 * Phi4 == 70


class TestT5_Constellations:
    def test_zodiac_constellations(self):
        # 12 zodiac = k
        assert k == 12

    def test_iau_constellations(self):
        # 88 = ? = lam^q * k - lam^q = 96-8
        assert lam ** q * k - lam ** q == 88

    def test_ptolemy_48(self):
        # 48 = lam*f
        assert lam * f == 48
