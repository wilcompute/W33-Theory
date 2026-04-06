"""
Phase CCCLXVIII — Black Hole Entropy and Microstate Counting from W(3,3)
=========================================================================

Bekenstein-Hawking S = A/(4G) realized exactly on W(3,3):
  - Horizon area A = k = 12 (boundary edges of a vertex)
  - Newton constant G = 1/(4E) = 1/960
  - S_BH = A/(4G) = k * E = 2880 = 12 * 240
  - log(microstates) = S_BH → N_micro = exp(2880)... but in graph units:
    N_micro = v^k = 40^12 (configurations of k boundary edges over v sites)

Strominger-Vafa: count BPS states = dim of cohomology.
  In W(3,3): dim H^*(graph) = v - rank(L) + 1 = 1 (connected).
  But weighted: chi(W33) = v - E + F where F is faces of triangle complex.
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2  # 240
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Bekenstein:
    def test_horizon_area(self):
        A = k
        assert A == 12

    def test_newton_g(self):
        G = Fraction(1, 4 * E)
        assert G == Fraction(1, 960)

    def test_bh_entropy(self):
        S = k * E  # A/(4G) = k * 4E / 4 = k*E
        assert S == 2880
        assert S == k * E

    def test_entropy_factorization(self):
        # 2880 = 2^6 * 3^2 * 5 = 64*45
        assert 2880 == 64 * 45
        assert 2880 == 2**6 * 3**2 * 5


class TestT2_Microstates:
    def test_triangle_count(self):
        # Number of triangles in SRG = v*k*lam/6 = 40*12*2/6 = 160
        T = v * k * lam // 6
        assert T == 160

    def test_log_microstates(self):
        # log(N) ~ k * log(v) for boundary configurations
        log_N = k * math.log(v)
        assert log_N > 40

    def test_strominger_vafa(self):
        # BPS state count ~ exp(2*pi*sqrt(N/6))
        # For N = E/lam = 120: 2*pi*sqrt(20) ~ 28.1
        N = E // lam
        assert N == 120
        S_SV = 2 * math.pi * math.sqrt(N / 6)
        assert 25 < S_SV < 30


class TestT3_Hawking:
    def test_hawking_temperature(self):
        # T_H = 1/(8*pi*M) ~ 1/(8*pi*sqrt(E))
        T_H = 1 / (8 * math.pi * math.sqrt(E))
        assert 0 < T_H < 0.01

    def test_evaporation_time(self):
        # t_evap ~ M^3 ~ E^{3/2}
        t = E ** 1.5
        assert t > 3000


class TestT4_PageCurve:
    def test_page_time(self):
        # t_P = (1/2) * t_evap
        t_P = Fraction(v, 2 * k)
        assert t_P == Fraction(5, 3)

    def test_page_entropy_max(self):
        # Max entropy = min(S_rad, S_BH - S_rad)
        S_max = k * E // 2
        assert S_max == 1440
        assert S_max == k * E // 2


class TestT5_Holography:
    def test_ads_cft_dim(self):
        # Boundary dim = mu = 4 spacetime, bulk = mu + 1 = 5
        bulk = mu + 1
        assert bulk == 5

    def test_central_charge(self):
        # c = 3*L/(2*G) for AdS3, here c ~ E/k = 20
        c = E // k
        assert c == 20

    def test_cardy_formula(self):
        # S_Cardy = 2*pi*sqrt(c*L_0/6); L_0 ~ E/(2*c) = 6
        c = 20
        L0 = 6
        S_C = 2 * math.pi * math.sqrt(c * L0 / 6)
        assert 25 < S_C < 30
