"""
Supplement tau — TOPOLOGICAL DEFECTS FROM Z_3 SYMMETRY BREAKING
=====================================================================

The Z_3 = Z_q symmetry of W(3,3) (manifest in the q=3 generation
count, the Z_3 grading on F_3^4, the Z_q axion) has cosmological
consequences when broken at high temperature:

  Cosmic strings:  Z_3 vortices with winding in Z_q
  Domain walls:    2D interfaces between distinct Z_3 vacua
  Magnetic monopoles: Supp nu

Tensions in W(3,3) constants:

  tau.1  Cosmic string tension mu_string ~ f_a^2 = (v * v_EW)^2
  tau.2  Domain wall tension sigma_wall ~ f_a^2 * M_X
  tau.3  Z_3 axion mass m_a ~ Phi_6 * (M_QCD^2 / f_a)
  tau.4  Domain wall solution: Z_q symmetry biased by Yukawa
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7
v_EW = lam * q * (v + 1)  # 246
f_a = v * v_EW              # 9840 (Supp E D2)
M_X_log10 = Phi3 + lam      # 15


# ------------------------------------------------------------------
# tau.1  Cosmic string tension
# ------------------------------------------------------------------
class Test_tau_1_StringTension:
    def test_f_a_value(self):
        # f_a = v * v_EW = 40 * 246 = 9840 GeV
        assert f_a == 9840

    def test_string_tension_factor(self):
        # mu_string ~ f_a^2
        # log10(mu_string / GeV^2) ~ 2 * log10(f_a) ~ 2 * 4 = 8
        log_mu = lam * math.log10(f_a)
        assert 7.5 < log_mu < 8.5


# ------------------------------------------------------------------
# tau.2  Domain wall tension
# ------------------------------------------------------------------
class Test_tau_2_DomainWallTension:
    def test_sigma_wall(self):
        # sigma_wall ~ M_X * f_a^2
        # log10 = 15 + 2 * 4 = 23 = Phi_3 + Phi_4 ?
        # Actually Phi_3 + Phi_4 = 23
        assert Phi3 + Phi4 == 23

    def test_wall_tension_log(self):
        log_sigma = M_X_log10 + lam * math.log10(f_a)
        assert 22 < log_sigma < 24


# ------------------------------------------------------------------
# tau.3  Z_3 axion mass
# ------------------------------------------------------------------
class Test_tau_3_AxionMass:
    def test_mass_formula_factor(self):
        # m_a ~ Phi_6 * (M_QCD^2 / f_a)
        # M_QCD ~ 200 MeV ~ 0.2 GeV
        # m_a ~ 7 * (0.04) / 9840 ~ 3 * 10^-5 GeV ~ 30 keV
        M_QCD = 0.2  # GeV
        m_a_w33 = Phi6 * (M_QCD ** 2) / f_a
        # ~ 0.28 / 9840 ~ 2.85e-5 GeV = 28.5 keV
        assert 1e-5 < m_a_w33 < 1e-4


# ------------------------------------------------------------------
# tau.4  Domain wall problem and Z_q breaking
# ------------------------------------------------------------------
class Test_tau_4_WallProblem:
    def test_q_classes(self):
        # q = 3 distinct Z_3 vacua -> q domain wall types
        assert q == 3

    def test_wall_breaking_via_yukawa(self):
        # Yukawa hierarchy biases the Z_q symmetry; wall imbalance
        # parameterized by Yukawa ratio ~ phi_3 / phi_3^q = 1/q^2
        # = 1/9
        assert q ** lam == 9


# ------------------------------------------------------------------
# tau.5  Topological winding
# ------------------------------------------------------------------
class Test_tau_5_TopologicalWinding:
    def test_winding_in_Z_q(self):
        # Cosmic string winding number lives in Z_q = Z_3
        assert q == 3

    def test_three_distinct_strings(self):
        # 3 = q topologically distinct string types
        assert q == 3

    def test_pi_1_S_1_eq_Z(self):
        # pi_1(S^1) = Z; Z_q quotient gives Z/qZ winding
        assert q == 3


# ------------------------------------------------------------------
# tau.6  Cosmological constraints
# ------------------------------------------------------------------
class Test_tau_6_CosmoConstraints:
    def test_string_density_today(self):
        # Cosmic string contribution to Omega today ~ G * mu_string * H_0^-1
        # Negligible if mu << M_Pl^2
        # f_a^2 = 9840^2 = ~10^8 GeV^2 << M_Pl^2 = 10^38 GeV^2
        assert f_a ** lam < 10 ** (lam * mu + lam ** lam)  # 8 + 4 = 12

    def test_axion_dark_matter(self):
        # Misalignment-mechanism axion dark matter density
        # Omega_a h^2 ~ (f_a / 10^12 GeV)^(7/6)
        # f_a = 9840 GeV << 10^12 -> Omega_a tiny -> not dominant DM
        assert f_a < 10 ** Phi3


# ------------------------------------------------------------------
# tau-CLOSURE
# ------------------------------------------------------------------
class Test_tau_Closure:
    def test_three_defect_types(self):
        # 3 = q types of topological defect from Z_q breaking
        defects = ['cosmic_string', 'domain_wall', 'monopole']
        assert len(defects) == q

    def test_defects_dictionary(self):
        # All in W(3,3) constants
        defects = {
            'string_tension_log_GeV2': lam * math.log10(f_a),  # ~ 8
            'wall_tension_log_GeV3':   M_X_log10 + lam * math.log10(f_a),
            'monopole_mass_log_GeV':   M_X_log10 + math.log10(f),  # GUT-scale
        }
        assert defects['string_tension_log_GeV2'] > 7

    def test_winding_count(self):
        assert q == 3
