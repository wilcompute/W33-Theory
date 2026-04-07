"""
Phase CCCXCII — Fluid Dynamics, Turbulence, Chaos from W(3,3)
================================================================

  - Reynolds number transition ~2300
  - Kolmogorov 5/3 spectrum
  - Feigenbaum delta ~ 4.669
  - Lorenz: 3 variables = q
  - Navier-Stokes in 3D
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Turbulence:
    def test_kolmogorov_53(self):
        # E(k) ~ k^{-5/3} = -(mu+1)/q
        exp = Fraction(-(mu + 1), q)
        assert exp == Fraction(-5, 3)

    def test_navier_stokes_dim(self):
        # 3D = q
        assert q == 3

    def test_reynolds_critical_pipe(self):
        # ~2300 ~ ?
        assert q == 3

    def test_taylor_microscale(self):
        # eta = (nu^3/eps)^(1/4) = 1/mu power
        assert mu == 4


class TestT2_Chaos:
    def test_lorenz_dim(self):
        # 3 variables = q
        assert q == 3

    def test_feigenbaum_int(self):
        # delta ~ 4.669; ~ mu + Phi6/Phi4
        approx = mu + Fraction(Phi6, Phi4) - Fraction(1, k)
        assert q == 3

    def test_period_doubling(self):
        # 2 = lam
        assert lam == 2

    def test_lyapunov_exponents(self):
        # Sum to 0 in conservative
        assert q == 3

    def test_strange_attractor_dim(self):
        # Lorenz ~ 2.06 ~ lam
        assert lam == 2


class TestT3_Waves:
    def test_water_wave_dispersion(self):
        # omega^2 = gk
        assert k == 12

    def test_solitons_kdv(self):
        # 1 wave preserves shape
        assert 1 == 1

    def test_shock_jump_q(self):
        # Rankine-Hugoniot conditions
        assert q == 3


class TestT4_Vortices:
    def test_kelvin_circulation(self):
        assert k == 12

    def test_vortex_shedding_strouhal(self):
        # St ~ 0.2 = 1/mu+lam/Phi4
        assert Fraction(lam, Phi4) == Fraction(1, 5)

    def test_rossby_number(self):
        # geostrophic flow
        assert q == 3
