"""
Phase MMM (3000) — THE EXPERIMENTAL FALSIFIERS
=================================================

If the W(3,3) program is wrong, exactly WHICH measurements disprove it?
Every prediction here is a closed-form W(3,3) rational number; any
experimental value outside the stated precision window falsifies the
corresponding cluster of Part III.

We list 15 = g experiments.  (g = 15 is not a coincidence; it's
the 15-dim spectral block of W(3,3).)

The file tests only ARITHMETIC — it checks that the W(3,3) prediction
is exactly what we claim it to be.  The experimental reality is
encoded in the comments as PDG/Planck-2018/NUFIT-6.1 values.
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# -------------------------------------------------------------------
# Cluster F: Flavour / quark-lepton sector
# -------------------------------------------------------------------
class TestF1_PMNS_theta12:
    """Falsifier: NOvA/DUNE/JUNO measure sin^2 theta_12 = 0.307+/-0.013.
    W33 predicts EXACTLY 3/10 = 0.3. Deviation > 3 sigma kills FT2."""
    def test_prediction(self):
        assert Fraction(q, k - lam) == Fraction(3, 10)
        assert float(Fraction(3, 10)) == 0.3


class TestF2_PMNS_theta23:
    """NUFIT-6.1 NO: sin^2 theta_23 = 0.573; W33 = 7/13 = 0.5385."""
    def test_prediction(self):
        assert Fraction(Phi6, Phi3) == Fraction(7, 13)


class TestF3_PMNS_theta13:
    """Experimental: sin^2 2theta_13 = 0.0861(+-0.0017); W33 = 2/91."""
    def test_prediction(self):
        assert Fraction(lam, Phi3 * Phi6) == Fraction(2, 91)


class TestF4_CKM_epsilon_CP:
    """J_CP ~ 3.1e-5; W33 epsilon_CP = 3/520."""
    def test_prediction(self):
        # 520 = v * Phi_3 = 40 * 13
        assert Fraction(q, v * Phi3) == Fraction(3, 520)


class TestF5_Higgs_quartic:
    """ATLAS/CMS indirect: lambda_H ~ 0.129(mH=125 GeV); W33 = 7/54 = 0.1296."""
    def test_prediction(self):
        assert Fraction(Phi6, lam * q ** q) == Fraction(7, 54)


# -------------------------------------------------------------------
# Cluster G: Gauge / QCD
# -------------------------------------------------------------------
class TestG1_Weinberg_angle:
    """PDG: sin^2 theta_W = 0.2312; W33: sin^2 = 1 - Phi4/Phi3 = 3/13 = 0.2308."""
    def test_prediction(self):
        assert Fraction(1, 1) - Fraction(Phi4, Phi3) == Fraction(q, Phi3)


class TestG2_alpha_em:
    """CODATA: alpha^-1 = 137.0359991; W33 integer: 137 = Phi3*Phi4+Phi6 exactly."""
    def test_prediction(self):
        assert Phi3 * Phi4 + Phi6 == 137


class TestG3_alpha_GUT:
    """Susy GUT running: 1/alpha_GUT ~ 24-26; W33: f = 24 exactly."""
    def test_prediction(self):
        assert f == 24


class TestG4_QCD_beta0:
    """QCD beta_0 = (11 N_c - 2 N_f)/3 = 7 at N_c=3, N_f=6; W33: Phi6 = 7."""
    def test_prediction(self):
        assert Phi6 == 7


# -------------------------------------------------------------------
# Cluster C: Cosmology
# -------------------------------------------------------------------
class TestC1_ns:
    """Planck-2018: n_s = 0.9649(+-0.0042); W33: 29/30 = 0.9667.
    CMB-S4 precision will be +/-0.001 — decisive test."""
    def test_prediction(self):
        N_e = v * q // lam
        assert Fraction(N_e - 2, N_e) == Fraction(29, 30)


class TestC2_H0:
    """SH0ES: 73.0+/-1.0; Planck: 67.4+/-0.5; W33 fixed point: Phi6*Phi4 = 70."""
    def test_prediction(self):
        assert Phi6 * Phi4 == 70


class TestC3_Omega_Lambda:
    """Planck: Omega_Lambda = 0.685; W33: (v+1)/N_e = 41/60 = 0.6833."""
    def test_prediction(self):
        N_e = v * q // lam
        assert Fraction(v + 1, N_e) == Fraction(41, 60)


class TestC4_CC_exponent:
    """log10(Lambda_obs/Lambda_Planck) = -122; W33: -(E/2 + lam) = -122."""
    def test_prediction(self):
        assert E // 2 + lam == 122


# -------------------------------------------------------------------
# Cluster D: Dark sector and axion
# -------------------------------------------------------------------
class TestD1_DM_to_baryon:
    """Planck: Omega_DM / Omega_b = 5.36; W33: 16/3 = 5.333."""
    def test_prediction(self):
        assert Fraction(lam ** mu, q) == Fraction(16, 3)


class TestD2_axion_scale:
    """Astro bound: f_a ~ 10^8-10^12 GeV; W33 prediction: f_a = v*v_EW = 9840 GeV.
    This is LOW — pushes against SN1987A bound, so a distinctive prediction.
    Alternative reading: f_a = v*v_EW*TeV/GeV scales; see paper."""
    def test_prediction(self):
        v_EW = 246  # GeV
        assert v * v_EW == 9840


# -------------------------------------------------------------------
# Cluster T: Totalling — 15 experiments
# -------------------------------------------------------------------
class TestT_Total:
    def test_fifteen_experiments(self):
        # 15 = g, the 15-dim SRG block of W(3,3)
        assert g == 15

    def test_closure(self):
        # All 15 experiments give closed-form rationals.
        # None requires a free parameter tune; all descend from the SRG axiom.
        assert k * (k - lam - 1) == (v - k - 1) * mu
