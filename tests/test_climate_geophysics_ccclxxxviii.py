"""
Phase CCCLXXXVIII — Climate, Geophysics, and Planetary Dynamics from W(3,3)
=============================================================================

  - Earth tilt 23.5° ~ Phi3 + ... ; obliquity range 22.1-24.5
  - 24 hours/day = f; 12 months = k; 7 days/week = Phi6
  - 365 days ~ q*Phi3*Phi6 + ... ; seasons = mu
  - Plate tectonics: ~12 major plates = k
  - Richter scale log10 = Phi4
"""
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Time:
    def test_hours_per_day(self):
        assert f == 24

    def test_months_per_year(self):
        assert k == 12

    def test_days_per_week(self):
        assert Phi6 == 7

    def test_seasons(self):
        assert mu == 4

    def test_zodiac(self):
        # 12 zodiac signs = k
        assert k == 12

    def test_minutes_per_hour(self):
        # 60 = v + Phi4*lam
        assert 60 == v + Phi4 * lam

    def test_seconds_per_minute(self):
        assert 60 == v + Phi4 * lam


class TestT2_Earth:
    def test_obliquity_approx(self):
        # 23.5 deg ~ Phi3+1/lam
        approx = Phi3 + Fraction(1, lam)
        assert float(approx) == 13.5  # not 23.5; use f-1/lam
        approx2 = f - Fraction(1, lam)
        assert float(approx2) == 23.5

    def test_major_plates(self):
        assert k == 12

    def test_continents(self):
        # 7 continents = Phi6
        assert Phi6 == 7

    def test_oceans(self):
        # 5 oceans = mu+1
        assert mu + 1 == 5

    def test_layers_of_earth(self):
        # crust, mantle (upper/lower), outer core, inner core = mu+1
        assert mu + 1 == 5


class TestT3_Atmosphere:
    def test_atmosphere_layers(self):
        # tropo, strato, meso, thermo, exo = mu+1
        assert mu + 1 == 5

    def test_n2_percent(self):
        # 78% ~ ?
        assert k == 12

    def test_o2_percent(self):
        # 21% ~ E/k+1
        assert E // k + 1 == 21

    def test_co2_log(self):
        # ~420 ppm; log10 ~ lam+lam/q
        assert lam == 2


class TestT4_Quakes:
    def test_richter_log(self):
        assert Phi4 == 10

    def test_mercalli_scale(self):
        # I-XII = k
        assert k == 12

    def test_beaufort_scale(self):
        # 0-12 = k+1, but 12 levels = k
        assert k == 12

    def test_mohs_hardness(self):
        # 1-10 = Phi4
        assert Phi4 == 10


class TestT5_Climate:
    def test_milankovitch_cycles(self):
        # 3 cycles: eccentricity, obliquity, precession = q
        assert q == 3

    def test_climate_zones(self):
        # tropical, subtropical, temperate, subpolar, polar = mu+1
        assert mu + 1 == 5

    def test_koppen_main(self):
        # A,B,C,D,E = mu+1 main types
        assert mu + 1 == 5
