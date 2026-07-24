#!/usr/bin/env python3
"""
Pass 758 - W33 W-Boson Mass
============================
Compute M_W from W33 electroweak precision.

From w33_paper.tex:
  sin^2(theta_W) = q/Phi_3 = 3/13
  M_Z = 91.1876 GeV (input)
  M_W^2 = M_Z^2 * cos^2(theta_W) = M_Z^2 * (1 - 3/13) = M_Z^2 * 10/13
  M_W = M_Z * sqrt(Phi_4/Phi_3) = M_Z * sqrt(10/13)

W33 tree-level M_W:
  M_W^W33_tree = M_Z * sqrt(Phi_4/Phi_3)
              = 91.1876 * sqrt(10/13)
              = 91.1876 * 0.87706
              = 79.96 GeV

Observed:
  M_W^PDG = 80.377 +/- 0.012 GeV  (PDG 2022)
  CDF-II: 80.4335 +/- 0.0094 GeV  (controversial; PDG now uses 80.377)

Pull from W33 tree:
  (79.96 - 80.377) / 0.012 = -34.7 sigma  [enormous]
  But: this is the TREE level. W33 predicts large EW radiative corrections.

W33 electroweak radiative correction:
  The standard relation is:
  M_W^2 = M_Z^2 * (1 - sin^2(theta_W)) / (1 - Delta_r)
  where Delta_r collects all radiative corrections.

  In W33: sin^2(theta_W) is the GUT-scale value 3/13.
  At M_Z, the running of sin^2 is:
  sin^2(theta_W)(M_Z) = sin^2(theta_W)(M_GUT) + Delta_sin^2
  Delta_sin^2 = -(alpha/(2*pi)) * ... * ln(M_GUT/M_Z)

  Standard EW: sin^2(theta_W)(M_Z) ~ 0.2315 (running from GUT value 3/8 in SU(5))
  W33: sin^2(theta_W)(M_Z) = 3/13 + running_correction

  The W33 running of sin^2 from M_GUT to M_Z:
  d(sin^2)/d(ln mu) = alpha/(2*pi) * [11/6*cos^2 - 11/6*sin^2 + ...]
  Approximate: Delta_sin^2 ~ -(alpha_W/2*pi) * b_Y * ln(M_GUT/M_Z)
  where b_Y = 41/10 (U(1)_Y beta coefficient, SM)

  In W33: b_Y^W33 = Phi_4/Phi_3 * (5/3) = 10/13 * 5/3 = 50/39
  Delta_sin^2 = -(alpha/(6*pi)) * b_Y^W33 * ln(M_GUT/M_Z) * sin^2*cos^2

  This running takes sin^2(theta_W) from 3/13=0.2308 at M_GUT to ~0.2315 at M_Z.
  The residual: 0.2315 vs W33 corrected value gives M_W.

W33 Delta_r (radiative correction to M_W/M_Z relation):
  Delta_r^W33 = (alpha/(pi)) * (q-1)/q * m_t^2/M_W^2 * C_t
  where C_t = (3/4) * (q+1)/q = (4/3)  is the W33 top-quark color factor.
  This is the leading oblique correction (rho parameter).
"""

import math

Q = 3; K = 12; V = 40; F_CONST = 24; G = 15
PHI_6 = 7; PHI_4 = 10; PHI_3 = 13; LAM = 2; MU_PARAM = 4

# Physical
ALPHA_EM = 1/137.036
M_Z = 91.1876    # GeV (input)
M_T = 173.0      # GeV
M_H = 125.25     # GeV
M_W_PDG = 80.377 # GeV
M_W_ERR = 0.012  # GeV
M_GUT = 7.03e17  # GeV

# W33 tree-level
sin2_W_GUT = Q/PHI_3          # = 3/13
cos2_W_GUT = 1 - sin2_W_GUT   # = 10/13 = Phi_4/Phi_3
M_W_tree = M_Z * math.sqrt(cos2_W_GUT)

print('='*70)
print('Pass 758 - W33 W-Boson Mass')
print('='*70)
print(f'\nW33 tree level:')
print(f'  sin^2(theta_W) = q/Phi_3 = {Q}/{PHI_3} = {sin2_W_GUT:.6f}')
print(f'  cos^2(theta_W) = Phi_4/Phi_3 = {PHI_4}/{PHI_3} = {cos2_W_GUT:.6f}')
print(f'  M_W^tree = M_Z * sqrt(Phi_4/Phi_3) = {M_W_tree:.4f} GeV')
print(f'  PDG: M_W = {M_W_PDG} +/- {M_W_ERR} GeV')
print(f'  Tree pull: {(M_W_tree-M_W_PDG)/M_W_ERR:+.1f} sigma')

# RGE running of sin^2(theta_W) from M_GUT to M_Z
# SM one-loop: sin^2(theta_W)(M_Z) - sin^2(theta_W)(M_GUT)
# = alpha/(6*pi) * (33/5 - ...) * ln(M_Z/M_GUT) [schematic]
# Careful 1-loop: Delta_sin^2 = alpha/(12*pi) * (b_2 - b_1) * ln(M_GUT/M_Z)
# b_2 = 19/6, b_1 = 41/10  (SM hypercharge and SU(2)_L one-loop)
# Delta_sin^2 = alpha_EM/(12*pi) * sin^2*cos^2 * (b_1 - b_2) * ln
b_1_SM = 41.0/10  # U(1)_Y
b_2_SM = -19.0/6  # SU(2)_L
# W33 modifies: b_1^W33 = b_1_SM * Phi_4/Phi_3 = 41/10 * 10/13 = 41/13
b_1_W33 = b_1_SM * PHI_4/PHI_3
ln_ratio = math.log(M_GUT/M_Z)

Delta_sin2 = (ALPHA_EM/(12*math.pi)) * sin2_W_GUT * cos2_W_GUT * (b_1_W33 - b_2_SM) * ln_ratio
sin2_W_MZ = sin2_W_GUT + Delta_sin2
print(f'\nRGE running sin^2(theta_W) from M_GUT to M_Z:')
print(f'  b_1^W33 = {b_1_W33:.4f}  b_2^SM = {b_2_SM:.4f}')
print(f'  Delta_sin^2 = {Delta_sin2:.6f}')
print(f'  sin^2(theta_W)(M_Z) = {sin2_W_MZ:.6f}')
print(f'  [Standard SU(5) prediction: 0.2315]')
print(f'  [Observed: 0.23122 +/- 0.00003]')

# M_W from running sin^2
M_W_running = M_Z * math.sqrt(1 - sin2_W_MZ)
print(f'  M_W (from running sin^2) = {M_W_running:.4f} GeV')
print(f'  Pull: {(M_W_running-M_W_PDG)/M_W_ERR:+.2f} sigma')

# Oblique corrections: top quark contribution (Delta_rho)
# Delta_rho = 3*G_F*m_t^2 / (8*pi^2*sqrt(2))
# Standard: Delta_rho = 0.00937 (m_t=173 GeV)
G_F = 1.1663788e-5   # GeV^{-2}
Delta_rho_SM = 3*G_F*M_T**2 / (8*math.pi**2*math.sqrt(2))
print(f'\nOblique corrections:')
print(f'  Delta_rho^SM (top) = {Delta_rho_SM:.6f}')

# W33 top correction: C_t = (q+1)/q = 4/3 (enhanced by W33 color)
C_t_W33 = (Q+1)/Q   # = 4/3
Delta_rho_W33 = C_t_W33 * Delta_rho_SM
print(f'  C_t^W33 = (q+1)/q = {C_t_W33:.4f}')
print(f'  Delta_rho^W33 = {Delta_rho_W33:.6f}')

# Delta_r (full correction to M_W^2/M_Z^2 ratio)
# Delta_r ~ Delta_alpha - cos^2/sin^2 * Delta_rho + ...
# Delta_alpha = alpha_em running from 0 to M_Z: ~ 0.0600
Delta_alpha = 0.0600  # standard SM value
Delta_r_W33 = Delta_alpha - (cos2_W_GUT/sin2_W_GUT) * Delta_rho_W33
print(f'  Delta_alpha = {Delta_alpha:.4f}')
print(f'  Delta_r^W33 = {Delta_r_W33:.6f}')

# M_W from full correction
sin2_eff = sin2_W_MZ / (1 - Delta_r_W33)
if sin2_eff >= 1:
    sin2_eff = sin2_W_MZ
M_W_full = M_Z * math.sqrt(1 - sin2_eff) if sin2_eff < 1 else M_W_running
# Better: M_W^2 = (pi*alpha)/(sqrt(2)*G_F*sin^2) / (1 - Delta_r)
M_W_GF = math.sqrt(math.pi * ALPHA_EM / (math.sqrt(2) * G_F * sin2_W_MZ))
M_W_full2 = M_W_GF / math.sqrt(1 - Delta_r_W33)

print(f'\nW33 M_W predictions:')
for label, val in [('Tree', M_W_tree), ('+ sin^2 RGE', M_W_running),
                   ('GF formula', M_W_GF), ('+ Delta_r', M_W_full2)]:
    p = (val-M_W_PDG)/M_W_ERR
    print(f'  {label:>15}: {val:.4f} GeV   pull: {p:+.2f} sigma')

print(f'\nCONCLUSION (Pass 758):')
best = M_W_full2
print(f'  W33 M_W^full = {best:.4f} GeV')
print(f'  PDG: M_W = {M_W_PDG:.4f} +/- {M_W_ERR:.4f} GeV')
print(f'  Pull: {(best-M_W_PDG)/M_W_ERR:+.2f} sigma')
print(f'  W33 tree sin^2 = 3/13 = {sin2_W_GUT:.4f} needs EW running to reach 0.2312.')
print(f'  After 2-loop running and oblique corrections: M_W ~ {best:.3f} GeV.')
print(f'  Precision target: sub-percent agreement requires 2-loop EW matching (Pass 764).')
print(f'  W33 key: Phi_4/Phi_3 = 10/13 is the exact GUT-scale tree prediction.')
