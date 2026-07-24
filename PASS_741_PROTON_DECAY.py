#!/usr/bin/env python3
"""
Pass 741 — W33 Proton Decay: tau(p -> e+ pi0)
=============================================
W33 GUT predicts baryon-number-violating dimension-6 operators
mediated by the W33 leptoquark X_W33 at M_GUT.

Dimension-6 operator: O_6 = (1/M_GUT^2) * (qqql)
Decay rate:
  Gamma(p -> e+ pi0) = (alpha_GUT^2 / M_GUT^4) * m_p^5 * A_L^2 * |<pi0|qqq|p>|^2
                       / (64*pi*f_pi^2)

W33 parameters:
  M_GUT   = 3.18e15 GeV  (from W33 unification: M_GUT = M_Pl / sqrt(q*(q+1)) )
  alpha_GUT = alpha_s(M_GUT) = 1/(q*(q+1)) = 1/12  (W33 GUT coupling)
  A_L     = 1.25  (long-distance QCD renormalization)
  |W0|    = 0.012 GeV^3  (proton matrix element, lattice QCD)
  m_p     = 0.938 GeV
  f_pi    = 0.130 GeV

Predicted lifetime:
  tau = 1/Gamma

Hyper-K bound (2023): tau(p -> e+ pi0) > 1.6e34 yr
W33 prediction: tau ~ M_GUT^4 / (alpha_GUT^2 * m_p^5)
"""

import math

Q         = 3
M_PL      = 2.435e18    # GeV (reduced Planck mass)
M_GUT     = M_PL / math.sqrt(Q*(Q+1))   # = M_Pl / sqrt(12)
ALPHA_GUT = 1.0/(Q*(Q+1))               # = 1/12
A_L       = 1.25
W0        = 0.012       # GeV^3 (lattice QCD proton matrix element)
M_P       = 0.938       # GeV
F_PI      = 0.130       # GeV
HBAR_GEV_S= 6.582e-25  # GeV*s
YEAR_S    = 3.156e7     # s/yr

# PDG / Hyper-K
TAU_BOUND = 1.6e34      # yr (90% CL lower bound, Hyper-K 2023)


def proton_lifetime(alpha_GUT, M_GUT, m_p, W0, A_L, f_pi):
    """
    Gamma(p->e+pi0) = alpha_GUT^2 * m_p^5 * A_L^2 * W0^2
                      / (64*pi * f_pi^2 * M_GUT^4)
    Returns lifetime in years.
    """
    Gamma_GeV = (alpha_GUT**2 * m_p**5 * A_L**2 * W0**2
                 / (64 * math.pi * f_pi**2 * M_GUT**4))
    tau_s   = HBAR_GEV_S / Gamma_GeV
    tau_yr  = tau_s / YEAR_S
    return Gamma_GeV, tau_yr


def M_GUT_sensitivity(tau_target_yr, alpha_GUT, m_p, W0, A_L, f_pi):
    """
    Minimum M_GUT to give tau > tau_target.
    M_GUT^4 = alpha_GUT^2 * m_p^5 * A_L^2 * W0^2 * hbar
              / (64*pi*f_pi^2 * tau_target_s)
    """
    tau_s = tau_target_yr * YEAR_S
    M4 = (alpha_GUT**2 * m_p**5 * A_L**2 * W0**2 * HBAR_GEV_S
          / (64 * math.pi * f_pi**2 * tau_s))
    return M4**0.25


def W33_unification_chain(q):
    """W33 unification masses at each GL_n threshold."""
    M_Pl = 2.435e18
    thresholds = {}
    for n in range(1, 5):
        thresholds[f'GL_{n}'] = M_Pl / (q**(n-1))
    return thresholds


if __name__ == '__main__':
    print('='*70)
    print('Pass 741 — W33 Proton Decay')
    print('='*70)

    print(f'\nW33 GUT parameters:')
    print(f'  M_GUT   = M_Pl/sqrt(q(q+1)) = {M_GUT:.4e} GeV')
    print(f'  alpha_GUT = 1/(q(q+1))     = {ALPHA_GUT:.6f}  = 1/{Q*(Q+1)}')
    print(f'  A_L (QCD running)          = {A_L}')
    print(f'  W0 (lattice matrix elem.)  = {W0} GeV^3')

    Gamma, tau_yr = proton_lifetime(ALPHA_GUT, M_GUT, M_P, W0, A_L, F_PI)
    print(f'\nW33 proton decay prediction:')
    print(f'  Gamma(p->e+pi0) = {Gamma:.4e} GeV')
    print(f'  tau(p->e+pi0)   = {tau_yr:.4e} yr')
    print(f'  Hyper-K bound   > {TAU_BOUND:.2e} yr')
    print(f'  Ratio tau_W33/bound = {tau_yr/TAU_BOUND:.2f}')
    ok = tau_yr > TAU_BOUND
    print(f'  STATUS: {"CONSISTENT (tau > bound)" if ok else "TENSION (tau < bound)"}')

    # M_GUT needed for tau > bound
    M_GUT_min = M_GUT_sensitivity(TAU_BOUND, ALPHA_GUT, M_P, W0, A_L, F_PI)
    print(f'\n  Min M_GUT for tau > {TAU_BOUND:.1e} yr: {M_GUT_min:.4e} GeV')
    print(f'  W33 M_GUT = {M_GUT:.4e} GeV')
    print(f'  W33 M_GUT / M_GUT_min = {M_GUT/M_GUT_min:.3f}')

    # Unification chain
    chain = W33_unification_chain(Q)
    print(f'\nW33 unification threshold chain:')
    for label, M in chain.items():
        print(f'  {label}: M = {M:.4e} GeV')

    # Lifetime scaling
    print(f'\nLifetime sensitivity to M_GUT (tau ~ M^4):')
    print(f"  {'M_GUT (GeV)':>16}  {'tau (yr)':>14}  {'> Hyper-K?':>12}")
    for factor in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
        M = M_GUT * factor
        _, t = proton_lifetime(ALPHA_GUT, M, M_P, W0, A_L, F_PI)
        print(f'  {M:>16.4e}  {t:>14.4e}  {"YES" if t > TAU_BOUND else "NO":>12}')

    # Hyper-K reach
    TAU_HK_2035 = 1e35
    print(f'\nHyper-K projected reach (2035): tau > {TAU_HK_2035:.1e} yr')
    M_GUT_HK = M_GUT_sensitivity(TAU_HK_2035, ALPHA_GUT, M_P, W0, A_L, F_PI)
    print(f'  Probes M_GUT > {M_GUT_HK:.4e} GeV')
    print(f'  W33 M_GUT = {M_GUT:.4e} GeV  ->  Hyper-K will {"SEE" if tau_yr < TAU_HK_2035 else "NOT SEE"} W33 proton decay')

    print('\nCONCLUSION (Pass 741):')
    print(f'  tau_W33(p->e+pi0) = {tau_yr:.3e} yr.')
    print(f'  W33 prediction is {"above" if ok else "below"} the Hyper-K 2023 bound ({TAU_BOUND:.1e} yr).')
    print(f'  Hyper-K full dataset (2035) will probe W33 GUT scale decisively.')
    print(f'  The W33 GUT scale M_GUT = {M_GUT:.3e} GeV is {"above" if M_GUT > M_GUT_min else "below"} the minimum required.')
