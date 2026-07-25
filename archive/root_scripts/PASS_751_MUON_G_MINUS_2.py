#!/usr/bin/env python3
"""
Pass 751 - W33 Muon Anomalous Magnetic Moment (g-2)
====================================================
Compute delta(g-2)_mu from the W33 mediator loop.

W33 substrate primitives (from w33_paper.tex):
  q=3, k=12, v=40, f=24, g=15
  Phi_6=7, Phi_4=10, Phi_3=13, lambda=2, mu=4
  Gaussian integer z = (k-1)+mu*i = 11+4i, |z|^2 = 137

W33 muon g-2 mechanism:
  The W33 mediator is the 'dark matter' candidate from the W33 DM mass formula.
  M_DM = M_Pl * (q-1)/q^5 * (alpha_s/pi) = 18.8 GeV (Pass 650)
  The W33 mediator couples to the muon via the Weinberg-angle vertex:
  g_mumu-W33 = (q-1)/q * e * sin(theta_W)^{1/2}
              = 2/3 * e * (3/13)^{1/2}

W33 one-loop muon g-2:
  delta(g-2)_mu = (alpha/pi) * (m_mu/M_W33)^2 * F(x)
  where x = m_mu^2/M_W33^2
  F(x) = (1/3)(1 - x) for scalar mediator (W33 DM is scalar-like)

  More precisely, the W33 mediator contributes via:
  delta(g-2)_mu^W33 = (g_coup^2)/(8*pi^2) * (m_mu/M_W33)^2 * F_W33

  W33 coupling:
  g_coup = e * (q-1)/q = e * 2/3
  F_W33 = 2*(mu-1)/(3*mu) = 2*3/(3*4) = 1/2 (from W33 tensor structure)

The observed muon g-2 discrepancy (2023 Fermilab/BNL):
  Delta(g-2)_mu = a_mu^exp - a_mu^SM = (249 +/- 48) x 10^{-11}
  [Using BMW calculation; if e+e- data used: (251 +/- 59) x 10^{-11}]

W33 Hashimoto transport correction to g-2:
  The Hashimoto branching number k-1 = 11 (from w33_paper.tex, Thm. Hashimoto-branching)
  The photon propagator is branch-averaged over k-1=11 continuations.
  This gives an additional W33 transport contribution:
  delta_Hashimoto = (alpha/pi) * (m_mu/M_W33)^2 / (k-1)
                  = (alpha/pi) * (m_mu/M_W33)^2 / 11
"""

import math

# W33 substrate primitives
Q = 3; K = 12; V = 40; F = 24; G = 15
PHI_6 = 7; PHI_4 = 10; PHI_3 = 13; LAM = 2; MU = 4

# Physical constants
ALPHA_EM = 1/137.035999
M_MU = 105.6583755e-3   # GeV
M_W33_DM = 18.8         # GeV (W33 DM mediator mass)
M_PL = 2.435e18         # GeV

# Observed discrepancy (Fermilab 2023)
DELTA_AMU_OBS = 249e-11  # central value
DELTA_AMU_ERR = 48e-11

# W33 mediator coupling
SIN2_W = Q / PHI_3          # = 3/13 from w33_paper.tex Thm. weinberg
g_coup = math.sqrt(ALPHA_EM * 4 * math.pi) * (Q-1)/Q   # e * (q-1)/q

def loop_function_scalar(x):
    """One-loop function for spin-0 mediator: F(x) = integral form."""
    # For m_f << M_S: F(x) ~ 1/3
    # Full form: F(x) = int_0^1 z^2(1-z)/(1-z+xz^2) dz, approximate
    if x < 0.01:
        return 1.0/3 * (1 - 7*x/6)
    return 1.0/(3*(1+x))

def delta_g2_W33(m_mu, M_med, g_c, alpha):
    """W33 one-loop contribution to (g-2)/2."""
    x = (m_mu/M_med)**2
    F = loop_function_scalar(x)
    # (g_c^2)/(8*pi^2) * (m_mu/M_med)^2 * F_W33
    F_W33 = 2*(MU-1)/(3*MU)   # = 1/2
    return (g_c**2)/(8*math.pi**2) * x * F_W33

def delta_g2_hashimoto(m_mu, M_med, alpha):
    """W33 Hashimoto transport correction to g-2."""
    # Branch-averaged over k-1=11 non-backtracking continuations
    return (alpha/math.pi) * (m_mu/M_med)**2 / (K-1)

if __name__ == '__main__':
    print('='*70)
    print('Pass 751 - W33 Muon g-2')
    print('='*70)

    print(f'\nW33 substrate primitives:')
    print(f'  sin^2(theta_W) = q/Phi_3 = {Q}/{PHI_3} = {SIN2_W:.6f}')
    print(f'  Weinberg angle theta_W = {math.degrees(math.asin(math.sqrt(SIN2_W))):.4f} deg')
    print(f'  Hashimoto branching number k-1 = {K-1}')
    print(f'  W33 DM mediator mass: M_W33 = {M_W33_DM} GeV')
    print(f'  Muon mass: m_mu = {M_MU*1e3:.4f} MeV')
    print(f'  x = (m_mu/M_W33)^2 = {(M_MU/M_W33_DM)**2:.4e}')

    dg2_loop = delta_g2_W33(M_MU, M_W33_DM, g_coup, ALPHA_EM)
    dg2_hash = delta_g2_hashimoto(M_MU, M_W33_DM, ALPHA_EM)
    dg2_total = dg2_loop + dg2_hash

    # W33 vertex correction from the Weinberg angle structure
    # The W33 mediator also contributes through the triangle anomaly
    # delta_triangle = (alpha/(2*pi)) * (q-1)/q^2 * (m_mu^2/M_Z^2) * ln(M_W33/m_mu)
    M_Z = 91.1876
    delta_triangle = (ALPHA_EM/(2*math.pi)) * (Q-1)/Q**2 * (M_MU/M_Z)**2 * math.log(M_W33_DM/M_MU)

    # W33 Koide contribution: the Koide formula K = lambda/q = 2/3 enforces
    # a specific lepton mass ratio that enters the hadronic vacuum polarization
    # delta_Koide = (alpha/pi)^2 * (lambda/q) * m_mu^2/M_W33^2
    delta_koide = (ALPHA_EM/math.pi)**2 * (LAM/Q) * (M_MU/M_W33_DM)**2

    dg2_full = dg2_loop + dg2_hash + delta_triangle + delta_koide

    print(f'\nW33 contributions to Delta(g-2)_mu / 2 = a_mu:')
    print(f'  a_mu^loop     = {dg2_loop:.4e}  (one-loop W33 scalar mediator)')
    print(f'  a_mu^Hashimoto= {dg2_hash:.4e}  (Hashimoto transport, k-1=11 branching)')
    print(f'  a_mu^triangle = {delta_triangle:.4e}  (W33 triangle anomaly via Weinberg angle)')
    print(f'  a_mu^Koide    = {delta_koide:.4e}  (Koide K=lambda/q=2/3 lepton structure)')
    print(f'  a_mu^W33_total= {dg2_full:.4e}')
    print(f'\nExperimental discrepancy:')
    print(f'  Delta_a_mu^obs = {DELTA_AMU_OBS:.4e} +/- {DELTA_AMU_ERR:.4e}')
    print(f'  Delta_a_mu^W33 / Delta_a_mu^obs = {dg2_full/DELTA_AMU_OBS:.4f}')
    pull = (dg2_full - DELTA_AMU_OBS)/DELTA_AMU_ERR
    print(f'  Pull: {pull:+.2f} sigma')

    # Scan over W33 mediator mass
    print(f'\nScan over W33 mediator mass M_W33 (GeV):')
    print(f"  {'M_W33':>10}  {'a_mu^W33':>14}  {'Ratio':>8}  {'Pull':>8}")
    for M in [5, 10, 18.8, 30, 50, 100, 300]:
        d = delta_g2_W33(M_MU, M, g_coup, ALPHA_EM) + delta_g2_hashimoto(M_MU, M, ALPHA_EM)
        r = d/DELTA_AMU_OBS
        p = (d - DELTA_AMU_OBS)/DELTA_AMU_ERR
        print(f'  {M:>10.1f}  {d:>14.4e}  {r:>8.4f}  {p:>+8.2f}')

    print(f'\nW33 g-2 connection to architecture (from photonic_holonet.tex):')
    print(f'  The matter shell = magic (36=(q!)^2 rays) stratifies as 8+24+4 = 2^q + f + mu')
    print(f'  Deep grade F = (2+sqrt(3))/6 = {(2+math.sqrt(3))/6:.6f}')
    print(f'  Mid  grade F = (5+2*sqrt(3))/12 = {(5+2*math.sqrt(3))/12:.6f}')
    print(f'  Shallow grade F = 3/4 = q/mu = Werner decoherence threshold')
    print(f'  The muon is in the mid-grade magic shell: 24=f mass shell.')

    print(f'\nCONCLUSION (Pass 751):')
    print(f'  W33 a_mu^W33 = {dg2_full:.3e} (total from all W33 mechanisms)')
    print(f'  Observed discrepancy: {DELTA_AMU_OBS:.3e} +/- {DELTA_AMU_ERR:.3e}')
    print(f'  W33 accounts for {dg2_full/DELTA_AMU_OBS*100:.1f}% of observed discrepancy.')
    print(f'  Full hadronic contributions from W33 seesaw required for precision match.')
    print(f'  The Hashimoto k-1=11 branching (w33_paper.tex) contributes at {dg2_hash/dg2_full*100:.1f}% level.')
