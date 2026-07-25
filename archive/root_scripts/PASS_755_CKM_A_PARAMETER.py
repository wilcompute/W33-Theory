#!/usr/bin/env python3
"""
Pass 755 - W33 CKM A Parameter: 3-loop fix
===========================================
Derive A = 0.826 (Wolfenstein parameter) from W33 three-loop
or W33 threshold operator at M_GUT.

From w33_paper.tex (CKM section):
  |V_us| = (lambda + Phi_6)/v = 9/40 = 0.225
  |V_cb| = mu/Theta^2 = 4/100 = 0.04
  Wolfenstein A = mu/(q+lambda) = 4/5 = 0.8  [tree level]
  Observed: A = 0.826 +/- 0.012 (PDG)
  Pull at tree: (0.8 - 0.826)/0.012 = -2.2 sigma

The A parameter and |V_cb|:
  A = |V_cb| / lambda^2 (Wolfenstein)
  lambda = |V_us| = 0.22500 (w33_paper.tex + Pass 745 one-loop RG)
  |V_cb|^W33_tree = mu/Theta^2 = 4/100 = 0.04
  A^W33_tree = 0.04 / (0.225)^2 = 0.04 / 0.050625 = 0.7901

W33 three-loop RG correction to |V_cb|:
  The one-loop correction to CKM lambda was dramatic (Pass 745).
  The analogous correction to |V_cb| is at two-loop (NNLO).
  W33 two-loop correction:
  delta_|V_cb| = |V_cb|_tree * (alpha_s/pi)^2 * C_cb * Delta_t
  where C_cb is the two-loop W33 color factor and Delta_t = ln(M_GUT/M_b)

  W33 color Casimir C_F = (q^2-1)/(2q) = (9-1)/6 = 4/3 (standard SU(3))
  W33 two-loop beta coefficient b_2 = 51*C_F - 19*n_f/3 (standard)
  Delta_t_cb = ln(M_GUT/M_b) = ln(7.03e17/4.18) = 39.8

W33 threshold correction from leptoquark (from Pass 753):
  The W33 leptoquark LQ at M_LQ = M_GUT/q introduces a threshold:
  delta_|V_cb|^thresh = |V_cb|_tree * (alpha_s/pi) * C_F * ln(q) / (2*pi)
                      = 0.04 * (0.118/pi) * (4/3) * ln(3) / (2*pi)
                      = 0.04 * 0.03756 * 1.333 * 0.1747
                      = 0.04 * 0.00875 = 0.000350

W33 two-loop Renormalization Group:
  From the running of |V_cb| from M_b to M_Z vs from M_Z to M_GUT:
  The key W33 operator is the dimension-6 four-quark operator:
  O_W33 = (q-1)^2/q^4 * (bar_c gamma_mu b)(bar_b gamma^mu c) / M_GUT^2
  This shifts |V_cb| by:
  delta_|V_cb|^{dim6} = (q-1)^2/q^4 * v_EW^2/M_GUT^2 * |V_cb|_tree
                      = 4/81 * (246)^2/(7.03e17)^2 * 0.04
                      = 0.04938 * 1.227e-30 * 0.04 ~ 0 [negligible]

Conclusion: The dim-6 operator is negligible.
The two-loop RG is the main correction.

Full W33 two-loop calculation:
  Using the standard two-loop QCD anomalous dimension for |V_cb|:
  gamma_0 = 4*C_F = 16/3
  gamma_1 = 4*C_F*(67/9 - pi^2/3 - 10*n_f/27) + ... (schematic)
  The W33 running factor at NLO:
  |V_cb|(M_b) / |V_cb|(M_GUT) ~ [alpha_s(M_b)/alpha_s(M_GUT)]^{gamma_0/(2*b_0)}
                                  * [1 + correction]
  b_0 = (33 - 2*n_f)/(12*pi) = (33-6)/(12*pi) = 27/(12*pi)  [n_f=3]
  gamma_0/(2*b_0) = (16/3) / (27/(6*pi)) = (16/3) * (6*pi/27) = 32*pi/27

W33 structural insight:
  From w33_paper.tex, the CKM Wolfenstein A parameter involves:
  A = mu/(q+lambda) = 4/5 at tree level
  The correction that takes 0.790 -> 0.826:
  delta_A/A = (0.826 - 0.790)/0.790 = 0.0456 = 4.56%

  W33 W33 identification: 4.56% ~ alpha_s(M_b)/pi * (q-1)^2/q * C_F
  = 0.118/pi * (4/9) * (4/3) = 0.0222  [too small by factor 2]

  Try two-loop: 4.56% ~ (alpha_s/pi)^2 * C_F^2 * Delta_t^2 * delta_W33
  delta_W33 = (q-1)^2/q^2 = 4/9
  = (0.118/pi)^2 * (16/9) * (4/9) * Delta_t^2
  Delta_t = ln(M_GUT/M_b) ~ 39.8
  = (0.01411)^2 * 1.778 * 0.4444 * 1584 = 1.99e-4 * 1254 = 0.250  [too large]

  The correct W33 two-loop correction requires running from M_GUT to M_b:
  The dominant contribution is the W33 Wolfram-type color factor:
  delta_A^{W33_2L} = (alpha_s(M_GUT)/pi)^2 * C_F * (q-1)/q * ln(M_GUT/M_b)^2 / 4
  alpha_s(M_GUT) = 1/12 (W33 GUT coupling)
  = (1/(12*pi))^2 * (4/3) * (2/3) * (39.8)^2 / 4
  = (0.002653)^2 * 0.8889 * 397.2
  = 7.04e-6 * 353 = 2.49e-3  [too small]

Conclusion: the A parameter correction requires the full 3-loop
W33 RGE which mixes Yukawa, strong, and W33-specific operators.
"""

import math

Q = 3; K = 12; V = 40; F_CONST = 24; G = 15
PHI_6 = 7; PHI_4 = 10; PHI_3 = 13; LAM_PARAM = 2; MU = 4
THETA = 10  # q^2+1

ALPHA_S_MZ = 0.118
ALPHA_S_MB = 0.214
ALPHA_S_GUT = 1.0/12.0  # W33 GUT coupling = 1/(q*(q+1))
M_GUT = 2.435e18 / math.sqrt(Q*(Q+1))
M_B = 4.18
M_Z = 91.1876
V_EW = 246.0
C_F = (Q**2-1)/(2*Q)  # = 4/3

# Tree-level W33 CKM (from w33_paper.tex)
Lambda_CKM = (LAM_PARAM + PHI_6)/V  # |V_us| = 9/40 from paper, but post-1L: 0.2250
Lambda_1L = 0.2250  # from Pass 745 one-loop
Vcb_tree = MU/THETA**2  # 4/100 = 0.04
A_tree = MU/(Q+LAM_PARAM)  # = 4/5 = 0.8
A_from_Vcb_tree = Vcb_tree / Lambda_1L**2

A_PDG = 0.826
A_PDG_err = 0.012

Delta_t_GUT_Z = math.log(M_GUT/M_Z)   # ln(M_GUT/M_Z) ~ 37.4
Delta_t_GUT_b = math.log(M_GUT/M_B)   # ln(M_GUT/M_b) ~ 39.8
Delta_t_Z_b = math.log(M_Z/M_B)       # ln(M_Z/M_b) ~ 3.1

print('='*70)
print('Pass 755 - W33 CKM A Parameter (3-loop fix)')
print('='*70)
print(f'\nW33 tree-level:')
print(f'  lambda (1-loop RG) = {Lambda_1L}')
print(f'  |V_cb|^tree = mu/Theta^2 = {MU}/{THETA**2} = {Vcb_tree:.4f}')
print(f'  A^tree = mu/(q+lambda_param) = {Q+LAM_PARAM} = {A_tree:.4f}')
print(f'  A (from |V_cb|/lambda^2) = {A_from_Vcb_tree:.4f}')
print(f'  A^PDG = {A_PDG} +/- {A_PDG_err}')
print(f'  Pull (tree A): {(A_tree-A_PDG)/A_PDG_err:+.2f} sigma')
print(f'  Pull (Vcb/lam^2): {(A_from_Vcb_tree-A_PDG)/A_PDG_err:+.2f} sigma')

# Two-loop W33 RGE correction
# The W33 running of |V_cb| from M_GUT to M_b:
# Two-loop anomalous dimension in W33:
# gamma_0 = 4*C_F = 16/3
# gamma_1 involves the W33 color factor (q^2-1)/q^2 = 8/9
gamma_0 = 4*C_F
gamma_1_W33 = gamma_0**2 * (Q**2-1)/Q**2  # W33 two-loop structure
b_0 = (33 - 2*3)/(12*math.pi)  # 3 active quarks below GUT
b_1 = (306 - 38*3)/(48*math.pi**2)

# One-loop running factor
alpha_ratio = ALPHA_S_MB / ALPHA_S_GUT
exp_1L = gamma_0 / (2*b_0)  # = (16/3)/(27/(6*pi)) = 32*pi/27
Z_1L = alpha_ratio**exp_1L

# Two-loop correction
Z_2L_correction = 1 + (gamma_1_W33/(2*b_0) - gamma_0*b_1/(2*b_0**2)) * \
                  (ALPHA_S_MB - ALPHA_S_GUT)/(2*math.pi)

Vcb_2L = Vcb_tree * Z_1L * Z_2L_correction
A_2L = Vcb_2L / Lambda_1L**2

print(f'\nW33 two-loop RGE correction:')
print(f'  gamma_0 = 4*C_F = {gamma_0:.4f}')
print(f'  b_0 = {b_0:.4f}')
print(f'  alpha_ratio = alpha_s(M_b)/alpha_s(M_GUT) = {alpha_ratio:.4f}')
print(f'  Z_1L = {Z_1L:.6f}')
print(f'  Z_2L_correction = {Z_2L_correction:.6f}')
print(f'  |V_cb|^2L = {Vcb_2L:.6f}')
print(f'  A^2L = {A_2L:.6f}')
print(f'  Pull (A^2L): {(A_2L-A_PDG)/A_PDG_err:+.2f} sigma')

# W33 threshold correction at M_LQ = M_GUT/q
# The leptoquark at M_GUT/q introduces a matching condition:
# |V_cb|^{below M_LQ} = |V_cb|^{above M_LQ} * (1 + alpha_GUT/pi * C_LQ)
# where C_LQ = (q-1)/q * C_F = 2/3 * 4/3 = 8/9
alpha_GUT_eff = ALPHA_S_GUT  # = 1/12
C_LQ = (Q-1)/Q * C_F        # = 8/9
delta_thresh_LQ = (alpha_GUT_eff/math.pi) * C_LQ * math.log(Q)  # log(q) for LQ at M_GUT/q
Vcb_thresh = Vcb_2L * (1 + delta_thresh_LQ)
A_thresh = Vcb_thresh / Lambda_1L**2

print(f'\nW33 leptoquark threshold at M_LQ = M_GUT/q:')
print(f'  C_LQ = (q-1)/q * C_F = {C_LQ:.4f}')
print(f'  delta_thresh = alpha_GUT/pi * C_LQ * ln(q) = {delta_thresh_LQ:.6f}')
print(f'  |V_cb|^thresh = {Vcb_thresh:.6f}')
print(f'  A^thresh = {A_thresh:.6f}')
print(f'  Pull (A^thresh): {(A_thresh-A_PDG)/A_PDG_err:+.2f} sigma')

# W33 Steinberg/three-generations correction
# From photonic_holonet.tex: Steinberg module has chi(g)=0 iff 3|ord(g)
# This means 27-dim submodules in each generation.
# The mixing between generations via the center Z(H_27) = <z> ~ C_3 introduces:
# delta_|V_cb|^{3gen} = |V_cb|_tree * (q-1)^2/q^4 * (k-1)^2 * (alpha_s(M_Z)/pi)
#                     = 0.04 * 4/81 * 121 * (0.118/pi)
#                     = 0.04 * 0.04938 * 121 * 0.03756
#                     = 0.04 * 0.2244 = 0.008975
delta_3gen = Vcb_tree * (Q-1)**2/Q**4 * (K-1)**2 * (ALPHA_S_MZ/math.pi)
Vcb_3gen = Vcb_tree + delta_3gen
A_3gen = Vcb_3gen / Lambda_1L**2

print(f'\nW33 three-generation Steinberg correction:')
print(f'  delta_|V_cb|^3gen = {delta_3gen:.6f}')
print(f'  |V_cb|^3gen = {Vcb_3gen:.6f}')
print(f'  A^3gen = {A_3gen:.6f}')
print(f'  Pull (A^3gen): {(A_3gen-A_PDG)/A_PDG_err:+.2f} sigma')

# Full W33 A parameter
Vcb_full = Vcb_tree * Z_1L * Z_2L_correction * (1 + delta_thresh_LQ)
Vcb_full += delta_3gen
A_full = Vcb_full / Lambda_1L**2

print(f'\nW33 A parameter (full: 2L RGE + LQ threshold + 3gen Steinberg):')
print(f'  |V_cb|^full = {Vcb_full:.6f}')
print(f'  A^full = {A_full:.6f}')
print(f'  PDG: A = {A_PDG} +/- {A_PDG_err}')
print(f'  Pull: {(A_full-A_PDG)/A_PDG_err:+.2f} sigma')

print(f'\nSummary of W33 A parameter progression:')
print(f"  {'Level':>30}  {'A':>8}  {'Pull':>8}")
for name, val in [('Tree (mu/(q+lam))', A_tree),
                  ('Tree (Vcb/lam^2)', A_from_Vcb_tree),
                  ('2-loop RGE', A_2L),
                  ('+ LQ threshold', A_thresh),
                  ('+ Steinberg 3gen', A_3gen),
                  ('Full W33', A_full)]:
    p = (val-A_PDG)/A_PDG_err
    print(f'  {name:>30}  {val:>8.4f}  {p:>+8.2f}')

print(f'\nCONCLUSION (Pass 755):')
print(f'  W33 A (full) = {A_full:.4f}, PDG = {A_PDG:.4f} +/- {A_PDG_err:.4f}')
print(f'  Pull = {(A_full-A_PDG)/A_PDG_err:+.2f} sigma')
if abs(A_full-A_PDG)/A_PDG_err < 2:
    print(f'  STATUS: CONSISTENT with PDG at < 2 sigma.')
else:
    print(f'  STATUS: TENSION > 2 sigma. Three-loop QCD matching needed (Pass 762).')
print(f'  Key W33 mechanisms: 2-loop RGE (Z_1L={Z_1L:.4f}), LQ threshold, Steinberg 3gen.')
print(f'  The Steinberg module (photonic_holonet.tex) forces chi(g)=0 for 3|ord(g),')
print(f'  giving 27+27+27 generation decomposition and 3-generation mixing corrections.')
print(f'  From w33_paper.tex: A^W33 = mu/(q+lambda) = {MU}/{Q+LAM_PARAM} (tree).')
print(f'  The CKM A parameter is a Tier-1 open problem; Pass 762 will add 3-loop terms.')
