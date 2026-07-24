#!/usr/bin/env python3
"""
Pass 753 - W33 Lepton Flavor Violation: BR(mu -> e gamma)
==========================================================
Compute BR(mu -> e gamma) from the W33 leptoquark.

From w33_paper.tex:
  M_GUT = M_Pl/sqrt(q*(q+1)) = 7.03e17 GeV
  alpha_GUT = 1/(q*(q+1)) = 1/12
  The PMNS mixing (w33_paper.tex Sec. 12):
    sin^2(theta_12) = mu/Phi_3 = 4/13 ~ 0.3077
    sin^2(theta_23) = Phi_6/Phi_3 = 7/13 ~ 0.5385
    sin^2(theta_13) = lambda/(Phi_3*Phi_6) = 2/91 ~ 0.02198

W33 LFV mechanism:
  The W33 leptoquark LQ has mass M_LQ ~ M_GUT/q = M_GUT/3
  It couples to (mu, c) and (e, s) quarks via W33 DFT Yukawa:
    g_LQ = g_GUT * omega^{ij} where omega = exp(2*pi*i/q)
  The mu->e gamma diagram has a leptoquark (and quark) in the loop.

Standard LFV formula:
  BR(mu -> e gamma) = (3*alpha_EM)/(32*pi) * |sum_i (Y_mi)* Y_ei / M_LQ^2|^2 * tau_mu

W33 off-diagonal Yukawa (from Pass 749 perturbed DFT):
  (m_D)_12 = m_top * (q-1)/q^2 * (omega - omega*)
           = m_top * 2/9 * 2i*sin(2*pi/q)
  |Y_mu_e^W33| = m_top * 2/9 * 2*sin(120 deg) / M_LQ
               = m_top * 4/(9*sqrt(3)/2) / M_LQ    [using sin(120)=sqrt(3)/2]
               = m_top * 8/(9*sqrt(3)) / M_LQ

W33 branching ratio:
  BR(mu->e gamma)^W33 = (3*alpha_EM/(32*pi)) * |Y_W33|^4 * tau_mu / Gamma_mu

Experimental bound:
  BR(mu -> e gamma) < 4.2e-13 (MEG Collaboration 2016)
  MEG-II projected (2027): < 6e-14
"""

import math

Q = 3; K = 12; V = 40; F_CONST = 24
PHI_6 = 7; PHI_4 = 10; PHI_3 = 13; LAM = 2; MU = 4

# Physical
ALPHA_EM = 1/137.036
M_PL = 2.435e18         # GeV
M_GUT = M_PL / math.sqrt(Q*(Q+1))  # = 7.03e17 GeV
M_LQ = M_GUT / Q        # W33 leptoquark mass = M_GUT/3
M_TOP = 173.0           # GeV
M_MU = 105.6583755e-3   # GeV
TAU_MU = 2.1969811e-6   # s
HBAR = 6.582e-25        # GeV*s

# PMNS angles from w33_paper.tex
sin2_12 = MU/PHI_3          # 4/13
sin2_23 = PHI_6/PHI_3       # 7/13
sin2_13 = LAM/(PHI_3*PHI_6) # 2/91

# W33 DFT off-diagonal Yukawa coupling
omega = math.exp(1j * 2*math.pi/Q)  # = exp(2*pi*i/3)
Y_offdiag_mag = M_TOP * (Q-1)/Q**2 * 2*abs(omega.imag)  # |Y_12| in GeV
# Normalize to dimensionless coupling: Y / M_LQ
Y_norm = Y_offdiag_mag / M_LQ
print(f'W33 off-diagonal Yukawa: |Y_12| = {Y_offdiag_mag:.4e} GeV')
print(f'Normalized coupling |Y_12|/M_LQ = {Y_norm:.4e}')

# The full BR formula with PMNS mixing factors
# Loop function for scalar leptoquark (x = m_q^2/M_LQ^2)
def F_loop(x):
    """Loop integral for BR(mu->e gamma) with scalar LQ."""
    # F(x) = x(2+3x-6x^2+x^3+6x*ln(x))/(12*(1-x)^4)
    if x < 1e-6:
        return x/6.0
    if abs(x-1) < 1e-4:
        return 1/12.0
    return x*(2 + 3*x - 6*x**2 + x**3 + 6*x*math.log(x)) / (12*(1-x)**4)

# Sum over quark generations in the loop
# W33 couples to (e,d), (mu,s), (tau,b) in first approximation
# Off-diagonal comes from PMNS mixing
M_quarks = {'u': 2.16e-3, 's': 95e-3, 'c': 1.27, 'b': 4.18, 't': M_TOP}

# Wilson coefficient for mu->e gamma from LQ loop
# C = (3/(32*pi^2)) * |Y_mu_q * Y_e_q*| / M_LQ^2 * F(m_q^2/M_LQ^2)
C_sum_sq = 0
for qname, mq in [('s', 95e-3), ('c', 1.27), ('b', 4.18)]:
    x = (mq/M_LQ)**2
    Fval = F_loop(x)
    Y_mu_q = Y_norm  # W33 coupling (off-diagonal)
    Y_e_q = Y_norm * math.sqrt(sin2_13)  # suppressed by theta_13
    C = Y_mu_q * Y_e_q * Fval / M_LQ**2
    C_sum_sq += C**2
    print(f'  q={qname}: x={x:.4e}, F(x)={Fval:.4e}, contrib |C|^2 = {C**2:.4e}')

Gamma_mu = HBAR / TAU_MU   # GeV
BR_W33 = (3*ALPHA_EM/(32*math.pi)) * C_sum_sq * (M_MU**2 / Gamma_mu * HBAR)
# Actually: BR = (alpha_EM * tau_mu / HBAR) * (3/(32*pi)) * |sum C|^2 * m_mu^4 / ...
# Correct formula:
# BR(mu->e gamma) = (3*alpha)/(16*pi) * |Delta_12|^2
# where Delta_12 = sum_q Y_{mu,q}^* Y_{e,q} / M_LQ^2 * F(m_q^2/M_LQ^2)
Delta12_sq = 0
for qname, mq in [('s', 95e-3), ('c', 1.27), ('b', 4.18)]:
    x = (mq/M_LQ)**2
    Fval = F_loop(x)
    D = Y_norm**2 * math.sqrt(sin2_13) * Fval / M_LQ**2
    Delta12_sq += D**2

BR_W33_v2 = (3*ALPHA_EM)/(16*math.pi) * Delta12_sq * M_MU**4

print(f'\nBR(mu -> e gamma) W33:')
print(f'  BR = {BR_W33_v2:.4e}')
print(f'  MEG bound (2016): 4.2e-13')
print(f'  MEG-II projected (2027): 6e-14')
print(f'  W33 / MEG bound ratio: {BR_W33_v2/4.2e-13:.4e}')

if BR_W33_v2 < 6e-14:
    status = 'BELOW MEG-II projected reach'
elif BR_W33_v2 < 4.2e-13:
    status = 'BELOW current MEG bound, ABOVE MEG-II reach -> testable!'
else:
    status = 'ABOVE current MEG bound -> EXCLUDED by current data'

print(f'  Status: {status}')

# Scan over leptoquark mass
print(f'\nScan over leptoquark mass M_LQ:')
print(f"  {'M_LQ (GeV)':>12}  {'BR':>12}  {'Status':>30}")
for M_scan in [1e14, 1e15, M_GUT/Q, M_GUT, 1e18]:
    Delta_sq = 0
    for mq in [95e-3, 1.27, 4.18]:
        x = (mq/M_scan)**2
        Fv = F_loop(x)
        D = (Y_offdiag_mag/M_scan)**2 * math.sqrt(sin2_13) * Fv / M_scan**2
        Delta_sq += D**2
    BR = (3*ALPHA_EM)/(16*math.pi) * Delta_sq * M_MU**4
    s = 'above MEG' if BR > 4.2e-13 else ('MEG-II reach' if BR > 6e-14 else 'below MEG-II')
    print(f'  {M_scan:>12.3e}  {BR:>12.4e}  {s:>30}')

print(f'\nPMNS mixing context (w33_paper.tex):')
print(f'  theta_13: sin^2 = lambda/(Phi_3*Phi_6) = 2/91 = {sin2_13:.6f}')
print(f'  This suppresses mu->e gamma relative to mu->tau e gamma.')
print(f'  The W33 leptoquark contributes both LFV and leptogenesis (Pass 749).')
print(f'\nCONCLUSION (Pass 753):')
print(f'  W33 BR(mu->e gamma) = {BR_W33_v2:.3e}')
print(f'  M_LQ = M_GUT/q = {M_LQ:.3e} GeV (GUT-scale leptoquark)')
print(f'  Status: {status}')
print(f'  Suppression by sin^2(theta_13) = 2/91 = {sin2_13:.5f}')
print(f'  W33 LFV is small due to GUT-scale M_LQ and theta_13 suppression.')
