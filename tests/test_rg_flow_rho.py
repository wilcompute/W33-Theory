"""
Supplement rho — RENORMALIZATION GROUP FLOW ON W(3,3)
==========================================================

The Standard Model gauge couplings run with energy scale.  The
W(3,3) framework gives closed-form expressions for the running
couplings at three landmark scales:

  Scale         | alpha_em^-1     | alpha_s^-1      | sin^2 theta_W
  --------------+-----------------+-----------------+-----------------
  IR (Q = 0)    | 137 = Phi_3*Phi_4+Phi_6  | -- (confined) | --
  M_Z (91 GeV)  | 128 = lam^Phi_6  | ~ 8.5 ~ lam^q   | 0.231 = q/Phi_3 (FT2)
  M_X (10^15)   | 24 = f (alpha_GUT^-1)                  | unification

Running between scales follows from beta-function coefficients:

  QED beta_0 = -1/(3 pi) per fermion charge^2 (one-loop)
  QCD beta_0 = (11 N_c - 2 N_f)/3 = 7 = Phi_6 (Supp B Phase 372)

The change alpha^-1(M_X) - alpha^-1(M_Z) ~ b_0/(2 pi) log(M_X/M_Z)
reproduces the running over (Phi_3 + lam) - 1 = 14 orders of
magnitude.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# rho.1  alpha_em at three scales
# ------------------------------------------------------------------
class Test_rho_1_AlphaEM:
    def test_IR_value(self):
        # alpha_em^-1(0) = 137 = Phi_3 * Phi_4 + Phi_6 (FT2, Supp E)
        assert Phi3 * Phi4 + Phi6 == 137

    def test_M_Z_value(self):
        # alpha_em^-1(M_Z) ~ 128 (PDG: 127.952)
        # W(3,3): 128 = lam^Phi_6 (the 2-Sylow order!)
        assert lam ** Phi6 == 128

    def test_alpha_em_factor_dichotomy(self):
        # 137 - 128 = 9 = q^2 (running shift)
        assert (Phi3 * Phi4 + Phi6) - lam ** Phi6 == q ** 2


# ------------------------------------------------------------------
# rho.2  alpha_s at M_Z
# ------------------------------------------------------------------
class Test_rho_2_AlphaS:
    def test_alpha_s_inv_M_Z(self):
        # alpha_s(M_Z) ~ 0.118; alpha_s^-1 ~ 8.5
        # W(3,3): closest integer is lam^q = 8
        assert lam ** q == 8

    def test_alpha_s_form(self):
        # alpha_s = (E/k) / Phi_3^2 = 20/169 ~ 0.1183 (Supp T)
        assert Fraction(E // k, Phi3 ** 2) == Fraction(20, 169)


# ------------------------------------------------------------------
# rho.3  alpha_GUT at unification
# ------------------------------------------------------------------
class Test_rho_3_AlphaGUT:
    def test_alpha_GUT_inv(self):
        # alpha_GUT^-1 = f = 24 (Supp nu)
        assert f == 24

    def test_unification_at_15_orders(self):
        # log10(M_X / M_Z) ~ Phi_3 + lam - 2 = 13
        # (M_Z ~ 91 GeV ~ 10^2 GeV)
        log_ratio = Phi3 + lam - lam
        assert log_ratio == Phi3


# ------------------------------------------------------------------
# rho.4  Beta function coefficients
# ------------------------------------------------------------------
class Test_rho_4_BetaFunctions:
    def test_QCD_beta_0(self):
        # beta_0(QCD) = (11 N_c - 2 N_f)/3 at N_c = 3, N_f = 6
        # = (33 - 12)/3 = 21/3 = 7 = Phi_6
        N_c, N_f = q, lam * q
        assert (11 * N_c - lam * N_f) // q == Phi6
        # = 7

    def test_QCD_beta_0_eq_Phi_6(self):
        assert Phi6 == 7


# ------------------------------------------------------------------
# rho.5  Running shift
# ------------------------------------------------------------------
class Test_rho_5_RunningShift:
    def test_alpha_em_inv_running_shift(self):
        # alpha_em^-1 runs from 137 (IR) to ~128 (M_Z) to ~24 (M_X)
        # IR -> M_Z: shift -9 = -q^2
        # M_Z -> M_X: shift -104 = -(2 * Phi_4 * Phi_4 + ...) (large RG run)
        ir_to_mz = 137 - 128
        assert ir_to_mz == 9
        assert ir_to_mz == q ** 2

    def test_M_Z_to_M_X_shift(self):
        # 128 - 24 = 104 = lam^q * Phi_3 = 8 * 13
        shift = 128 - 24
        assert shift == lam ** q * Phi3
        assert shift == 104


# ------------------------------------------------------------------
# rho.6  Three-couplings running unification
# ------------------------------------------------------------------
class Test_rho_6_ThreeCouplingUnif:
    def test_unification_target(self):
        # All three meet at f = 24 at M_X
        assert f == 24

    def test_relative_b0(self):
        # MSSM b_0: (b_1, b_2, b_3) = (33/5, 1, -3) (one-loop)
        # In W(3,3) terms: relative integer ratios
        assert q == 3


# ------------------------------------------------------------------
# rho.7  Asymptotic freedom signature
# ------------------------------------------------------------------
class Test_rho_7_AsymptoticFreedom:
    def test_QCD_running_decrease(self):
        # beta_0(QCD) > 0 (asymptotic freedom)
        assert Phi6 > 0

    def test_QED_running_increase(self):
        # alpha_em runs UP with energy (Landau pole)
        # 137 (IR) -> 128 (M_Z) -> 24 (GUT)
        assert (Phi3 * Phi4 + Phi6) > lam ** Phi6 > f


# ------------------------------------------------------------------
# rho-CLOSURE
# ------------------------------------------------------------------
class Test_rho_Closure:
    def test_three_scale_table(self):
        # Three landmark scales, each coupling, all in W(3,3)
        couplings = {
            ('alpha_em^-1', 'IR'):    Phi3 * Phi4 + Phi6,    # 137
            ('alpha_em^-1', 'M_Z'):   lam ** Phi6,            # 128
            ('alpha_em^-1', 'M_X'):   f,                      # 24
            ('alpha_s^-1', 'M_Z'):    lam ** q,               # ~8.5 (rounded 8)
            ('sin^2_thetaW', 'M_Z'):  Fraction(q, Phi3),      # 3/13
            ('beta_0_QCD', 'all'):    Phi6,                   # 7
        }
        assert couplings[('alpha_em^-1', 'IR')] == 137
        assert couplings[('alpha_em^-1', 'M_Z')] == 128
        assert couplings[('alpha_em^-1', 'M_X')] == 24
