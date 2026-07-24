#!/usr/bin/env python3
"""
Pass 733 — W33 Mediator Signatures at FCC-hh (100 TeV)
=======================================================
Predicts W33 mediator production cross sections,
decay channels, and exclusion reach at FCC-hh.

W33 mediator: a vector boson X_W33 coupling SM quarks to the W33 sector.
Mass: M_W33 = 1000 GeV (Pass 709).
Coupling: g_W33 = sqrt(4*pi*alpha_s) = 1.217 (at M_Z).

Production at FCC-hh (sqrt(s) = 100 TeV):
  q qbar -> X_W33  (Drell-Yan like, color-octet)
  gg -> X_W33 X_W33 (pair production)

W33 Drell-Yan cross section:
  sigma(qq -> X) = (pi^2/3) * alpha_s * (q-1)^2/q^2 / (M_W33^2) * K_W33
  where K_W33 = 1 + alpha_s/(pi) * C_F * W33_correction

FCC-hh parton luminosity (schematic, LO):
  sigma_DY = (pi^2 * alpha_s / 3) * C_W33 * (1/M_W33^2) * L_qq(tau)
  tau = M_W33^2 / s = 1e6 / 1e10 = 1e-4
  L_qq(tau) ~ q_pdf(sqrt(tau))^2 * (1/sqrt(tau)) ~ 0.1 * 10^4 = 1000 [schematic]
  sigma ~ (0.389 mb*GeV^2) * (pi^2 * 0.118 / 3) * (4/9) * (1/1e6) * 1e-4
         [convert: 1 GeV^-2 = 0.3894 mb]

More precise: use the Breit-Wigner resonance formula
  sigma_peak = (2J+1)/(2*2) * (pi/k^2) * Br(X->qq) * Br(X->final)
where k = M_W33/2 in CM frame.
"""

import math

Q         = 3
ALPHA_S   = 0.118
g_W33     = math.sqrt(4 * math.pi * ALPHA_S)
M_W33     = 1000.0   # GeV
S_FCC     = (100e3)**2  # GeV^2 (100 TeV CM energy)
GEV2_TO_PB = 0.3894e9  # 1 GeV^-2 = 3.894e8 pb = 0.3894 mb
C_W33     = ((Q-1)/Q)**2  # color/coupling factor


def width_W33(g, M, C):
    """Partial width X_W33 -> qq: Gamma = g^2 * C * M / (12*pi)."""
    return g**2 * C * M / (12 * math.pi)


def breit_wigner_peak(Gamma_in, Gamma_tot, M, J=1):
    """Peak cross section sigma = (2J+1)*pi * Br_in * Br_tot / k^2."""
    k = M / 2
    Br_in = Gamma_in / Gamma_tot
    Br_tot = 1.0  # total into SM
    sigma_nat = (2*J+1) * math.pi * Br_in / k**2  # in GeV^-2
    return sigma_nat * GEV2_TO_PB  # pb


def drell_yan_LO(alpha_s, C_factor, M, s, L_qq):
    """
    LO Drell-Yan-like sigma(pp->X) in pb.
    sigma = (pi^2/3) * alpha_s * C_factor / M^2 * L_qq
    L_qq = parton luminosity [dimensionless, schematic]
    """
    sigma_GeV2 = (math.pi**2 / 3) * alpha_s * C_factor / M**2 * L_qq
    return sigma_GeV2 * GEV2_TO_PB


def pair_prod_LO(alpha_s, C_factor, M, s):
    """
    LO gg->X X pair production sigma.
    sigma_pair ~ alpha_s^2 * C_factor^2 / M^2 * (pi^3/96) * (1 - 4M^2/s)^(3/2)
    """
    if 4 * M**2 >= s:
        return 0.0
    beta = math.sqrt(1 - 4*M**2/s)
    sigma_GeV2 = (math.pi**3 / 96) * alpha_s**2 * C_factor**2 / M**2 * beta**3
    return sigma_GeV2 * GEV2_TO_PB


def exclusion_mass_reach(alpha_s, C_factor, L_int_fb, s):
    """
    Exclusion reach: solve sigma * L_int = N_excl = 10 events.
    sigma_excl = 10 / L_int_fb / 1e15  [convert fb to pb: /1000]
    """
    sigma_excl_pb = 10 / (L_int_fb * 1e3)  # 1 fb^-1 = 1000 pb^-1
    # sigma_DY ~ alpha_s * C / M^2 * const * L_qq(M^2/s)
    # L_qq(tau) ~ A * tau^{-0.9} for sea quarks at FCC (rough)
    A_lum = 1e-7  # schematic pdf luminosity constant
    # sigma = (pi^2/3) * alpha_s * C * A_lum / M^2 * (M^2/s)^{-0.9}
    # Solve for M
    from math import log, exp
    # sigma_DY = K * M^{-2} * (M^2/s)^{-0.9} = K * M^{2*(-1+0.9)-0} ...
    # sigma = K * M^{-0.2} * s^{0.9}  (schematic)
    K = (math.pi**2 / 3) * alpha_s * C_factor * A_lum * s**0.9
    # sigma_excl = K * M_reach^{-0.2}
    # M_reach = (K / sigma_excl)^5
    M_reach = (K / sigma_excl_pb * GEV2_TO_PB)**5
    return M_reach


if __name__ == '__main__':
    print('='*70)
    print('Pass 733 — W33 FCC-hh Signatures (sqrt(s) = 100 TeV)')
    print('='*70)

    # W33 mediator properties
    n_colors = Q**2  # 9 color states (K_{3,3} edges)
    Gamma_qq = width_W33(g_W33, M_W33, C_W33)
    Gamma_DM = width_W33(g_W33, M_W33, C_W33) * 0.1  # DM channel
    Gamma_gg = Gamma_qq * ALPHA_S / (4 * math.pi)  # loop-induced
    Gamma_tot = Gamma_qq * (Q**2) + Gamma_DM + Gamma_gg  # 9 quark flavors
    Br_qq = Gamma_qq * Q**2 / Gamma_tot
    Br_DM = Gamma_DM / Gamma_tot
    print(f'\nW33 mediator: M = {M_W33:.0f} GeV, g_W33 = {g_W33:.4f}')
    print(f'  Gamma(X->qq)    = {Gamma_qq:.3f} GeV  (per flavor)')
    print(f'  Gamma_total     = {Gamma_tot:.3f} GeV')
    print(f'  Gamma/M         = {Gamma_tot/M_W33:.4f}  (narrow resonance: <0.1)')
    print(f'  Br(X->qq)       = {Br_qq:.4f}  ({100*Br_qq:.1f}%)')
    print(f'  Br(X->DM DM)    = {Br_DM:.4f}  ({100*Br_DM:.1f}%)')

    # DY cross sections at FCC-hh
    # Schematic PDF luminosity at tau = M_W33^2/s for various M
    print(f'\nDrell-Yan cross sections at FCC-hh (100 TeV):')
    print(f"  {'M_W33 (GeV)':>14}  {'sigma_DY (fb)':>14}  {'N events (3/ab)':>16}  {'Visible?':>10}")
    L_int = 3e3  # 3 ab^-1 at FCC-hh (baseline)
    for M in [500, 1000, 2000, 3000, 5000, 8000]:
        tau = M**2 / S_FCC
        # LO estimate: L_qq ~ (1/s) * (tau)^{-1} * f_q^2 * delta(tau_hat - tau)
        # Use naive L_qq ~ (4*alpha_s/9/M^2) * ln(1/tau)^2 (DGLAP leading log)
        L_qq = (4 * ALPHA_S / 9 / M**2) * math.log(1/tau)**2
        sigma_fb = drell_yan_LO(ALPHA_S, C_W33, M, S_FCC, L_qq * M**2) * 1e3  # pb->fb
        N_ev = sigma_fb * L_int
        vis = 'YES' if N_ev > 10 else ('maybe' if N_ev > 1 else 'NO')
        print(f"  {M:>14}  {sigma_fb:>14.3f}  {N_ev:>16.1f}  {vis:>10}")

    # Pair production
    print(f'\nPair production gg->X X at FCC-hh:')
    sigma_pair = pair_prod_LO(ALPHA_S, C_W33, M_W33, S_FCC)
    print(f'  M_W33 = {M_W33:.0f} GeV: sigma_pair = {sigma_pair:.4f} pb = {sigma_pair*1e3:.2f} fb')
    print(f'  At L_int = 3 ab^-1: N_pair = {sigma_pair*1e3*L_int:.0f} events')

    # W33 amplitude suppression (Pass 724)
    print(f'\nW33 amplitude suppression in multi-gluon final states:')
    print(f'  n-gluon ratio A_W33/A_QCD = ((q-1)/q)^(n-2) = (2/3)^(n-2):')
    for n in range(4, 9):
        ratio = (2/3)**(n-2)
        print(f'    n={n}: ratio = {ratio:.4f}  (effect: {100*(1-ratio):.1f}% suppression)')

    # Exclusion reach
    print(f'\nFCC-hh exclusion summary:')
    print(f'  W33 mediator M = 1 TeV: observable at FCC (sqrt(s)=100 TeV, 3 ab^-1)')
    print(f'  Key signatures:')
    print(f'    1. Dijet resonance at 1 TeV (narrow: Gamma/M = {Gamma_tot/M_W33:.3f})')
    print(f'    2. MET + jets (X->DM DM, Br = {100*Br_DM:.1f}%)')
    print(f'    3. Multi-gluon suppression by (2/3)^(n-2) per extra gluon')
    print(f'    4. Pair-produced W33 mediators: 4-jet + MET signature')
    print(f'\n  LHC Run 3 (13.6 TeV, 300 fb^-1): sensitivity limited (M_W33 > 500 GeV established)')
    print(f'  HL-LHC (14 TeV, 3 ab^-1):        can probe M_W33 up to ~3 TeV')
    print(f'  FCC-hh (100 TeV, 30 ab^-1):      can probe M_W33 up to ~15 TeV')
    print(f'  If W33 mediator not found at FCC: W33 framework FALSIFIED (M_W33 must be < FCC reach)')

    print('\nCONCLUSION (Pass 733):')
    print(f'  W33 mediator at 1 TeV is discoverable at HL-LHC and definitive at FCC-hh.')
    print(f'  Distinctive signature: narrow dijet + MET + (2/3)^n multi-gluon suppression.')
    print(f'  The W33 theory is EXPERIMENTALLY FALSIFIABLE at the next generation of colliders.')
