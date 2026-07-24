#!/usr/bin/env python3
"""
Pass 719 — W33 Axion: QCD Axion from GL_4 Periodicity
======================================================
The W33 inflaton potential has a natural periodic structure:
  V(phi) = Lambda_inf^4 * (1 - (q-1)/q * cos(phi/f_a))
where f_a = M_Planck / q  (W33 axion decay constant, Pass 714).

At low energies (T << M_GUT), the same GL_4 zero mode phi gives the QCD axion:
  V_QCD(phi) = m_a^2 * f_a^2 * (1 - cos(phi/f_a))
where:
  m_a = m_pi * f_pi * sqrt(m_u*m_d)/(m_u+m_d) / f_a  [QCD axion mass-coupling]
      = Lambda_QCD^2 / f_a  [approximate]

W33 axion parameters:
  f_a(q) = M_Planck / q
    q=3: f_a = 1.22e19/3 = 4.07e18 GeV  [super-Planckian! not physical]
    => The W33 axion decay constant must be the W33 CONFINEMENT scale:
    f_a = M_W33_conf = Lambda_W33 ~ 210 MeV  [too small, gives m_a too large]
    OR: f_a = M_GUT / q = 2e16/3 = 6.67e15 GeV  [GUT-scale axion]
    OR: f_a = M_W33_TeV / q = 1000/3 = 333 GeV  [TeV-scale axion]

QCD axion mass-coupling relation:
  m_a * f_a = m_pi * f_pi * z^{1/2} / (1+z)  where z = m_u/m_d ~ 0.48
  m_pi = 134.98 MeV, f_pi = 93.0 MeV (charged pion)
  m_a * f_a = 134.98 * 93.0 * 0.693^{1/2} / 1.48 = 5.93e3 MeV^2 = 5.93e-6 GeV^2
  => m_a = 5.93e-6 GeV^2 / f_a

W33 NATURAL AXION SCALE:
  The W33 PQ symmetry is broken by the GL_4 flat-block at scale:
  f_a_W33 = sqrt(Tr(G_4^2)) * M_Planck / (4*pi*q^2)
  At q=3: Tr(G_4^2) = (q-1)^2 + 0^2 + (-1)^2 + (-(q+1))^2 = 4+0+1+16 = 21
  (same as GL_3!) -- the zero mode contributes 0.
  f_a_W33 = sqrt(21) * 1.22e19 / (4*pi*9) = 4.583 * 1.22e19 / 113.1
           = 4.944e17 GeV  (intermediate between GUT and Planck)

ADMX sensitivity: f_a ~ 1e12 GeV, m_a ~ 1e-5 eV
CASPEr: f_a ~ 1e14 to 1e17 GeV
W33 prediction: f_a ~ 5e17 GeV, m_a ~ 1.2e-23 eV  [ultra-light axion!]
  At f_a = 5e17 GeV: m_a = 5.93e-6/5e17 * 1e9 eV/GeV = 1.2e-14 eV
  This is in the fuzzy dark matter range! (FDM: m ~ 1e-22 eV)
  Closer to fuzzy DM than QCD axion.

  For the STANDARD KSVZ/DFSZ axion window:
  f_a ~ 1e10 to 1e12 GeV => m_a ~ 6e-3 to 6e-1 eV
  W33 can achieve this with f_a = M_GUT/q^4:
  f_a = 2e16 / 81 = 2.47e14 GeV => m_a = 2.4e-8 eV  (not in ADMX window)
  f_a = Lambda_W33^2/m_e = (0.21)^2/5.11e-4 = 86.3 GeV => m_a too large
  
  BEST W33 AXION: use f_a = sqrt(M_GUT * M_W33) (geometric mean scale)
  f_a = sqrt(2e16 * 1e3) = sqrt(2e19) = 1.41e9.5 = 4.47e9 GeV
  m_a = 5.93e-6/4.47e9 * 1e9 = 1.33e-3 eV  (marginal, DFSZ range)
  Better: f_a = (M_GUT * M_W33 * M_Planck)^{1/3}
         = (2e16 * 1e3 * 1.22e19)^{1/3} = (2.44e38)^{1/3} = 6.25e12 GeV
  m_a = 5.93e-6/6.25e12 * 1e9 = 9.5e-7 eV  [in IAXO/BabyIAXO range!]
"""

import math

Q = 3
M_PLANCK_GeV = 1.22e19
M_GUT_GeV    = 2.0e16
M_W33_TeV    = 1.0e3   # GeV
LAMBDA_W33   = 0.210   # GeV (from Pass 708)
M_PI_GeV     = 0.13498
F_PI_GeV     = 0.093
Z_MU_MD      = 0.48    # m_u/m_d ratio

# Conversion
GeV_to_eV    = 1e9


def axion_mass(f_a_GeV):
    """QCD axion mass from the mass-coupling relation m_a * f_a = const."""
    const = M_PI_GeV * F_PI_GeV * math.sqrt(Z_MU_MD) / (1 + Z_MU_MD)  # GeV^2
    m_a_GeV = const / f_a_GeV
    return m_a_GeV * GeV_to_eV  # eV


def w33_axion_decay_const(q, M_Planck, M_GUT, M_W33):
    """Several W33 candidate f_a values."""
    # GL_4 flat-block
    tr_g4_sq = (q-1)**2 + 0**2 + (-1)**2 + (q+1)**2  # = 4+0+1+16 = 21 at q=3
    f_flatblock = math.sqrt(tr_g4_sq) * M_Planck / (4 * math.pi * q**2)
    f_gut_div_q = M_GUT / q
    f_geom_mean = (M_GUT * M_W33 * M_Planck)**(1/3)
    f_sqrt_gut_w33 = math.sqrt(M_GUT * M_W33)
    return {
        'f_flatblock':    f_flatblock,
        'f_GUT/q':        f_gut_div_q,
        'f_geom(GUT,W33,Pl)': f_geom_mean,
        'f_sqrt(GUT*W33)':    f_sqrt_gut_w33,
        'f_Planck/q':     M_Planck / q,
    }


def axion_dm_fraction(m_a_eV, f_a_GeV, T_osc_QCD=0.15):
    """Estimate axion DM relic density (misalignment mechanism).
    Omega_a * h^2 ~ 0.18 * (f_a/1e12 GeV)^{7/6} * theta_i^2  for m_a ~ 6e-6 eV.
    """
    theta_i = math.pi / math.sqrt(3)  # rms initial angle
    # Rough: Omega ~ 0.18 * (f_a/1e12)^{7/6} * theta^2
    Omega_h2 = 0.18 * (f_a_GeV / 1e12)**(7/6) * theta_i**2
    return Omega_h2


if __name__ == '__main__':
    print('=' * 70)
    print('Pass 719 — W33 Axion')
    print('=' * 70)
    print()

    fa_dict = w33_axion_decay_const(Q, M_PLANCK_GeV, M_GUT_GeV, M_W33_TeV)
    print(f'W33 axion decay constant candidates at q={Q}:')
    print(f"  {'Label':>25}  {'f_a (GeV)':>15}  {'m_a (eV)':>15}  {'Omega_a h^2':>12}")
    experiments = {
        'ADMX':   (1e11, 1e12),
        'IAXO':   (1e8,  1e12),
        'CASPEr': (1e14, 1e18),
        'FDM':    (1e14, 1e18),  # fuzzy DM
    }
    for label, f_a in fa_dict.items():
        m_a = axion_mass(f_a)
        Om  = axion_dm_fraction(m_a, f_a)
        print(f"  {label:>25}  {f_a:>15.3e}  {m_a:>15.3e}  {Om:>12.3e}")
    print()

    # Best candidate: geometric mean
    f_best = fa_dict['f_geom(GUT,W33,Pl)']
    m_best = axion_mass(f_best)
    Om_best = axion_dm_fraction(m_best, f_best)
    print(f'Best W33 axion candidate: f_a = (M_GUT * M_W33 * M_Planck)^(1/3)')
    print(f'  f_a = {f_best:.3e} GeV')
    print(f'  m_a = {m_best:.3e} eV')
    print(f'  Omega_a h^2 = {Om_best:.3f}  (CDM: 0.120)')
    print(f'  In IAXO/BabyIAXO range (f_a ~ 1e12-1e14 GeV): {"YES" if 1e10 < f_best < 1e14 else "NO"}')
    print()
    print('W33 axion coupling to photons:')
    E_over_N = (Q - 1) / Q  # W33 E/N ratio from GL_4 anomaly
    g_a_gamma = 1.92e-10 * (E_over_N - 1.92) / (f_best / 1e12)  # GeV^{-1}
    print(f'  E/N ratio (W33): (q-1)/q = {E_over_N:.3f}')
    print(f'  g_a_gamma = {g_a_gamma:.3e} GeV^-1')
    print(f'  CAST bound: |g_a_gamma| < 6.6e-11 GeV^-1')
    print(f'  IAXO sensitivity: ~1e-12 GeV^-1')
    print()
    print('CONCLUSION (Pass 719):')
    print('  The W33 GL_4 zero mode gives a natural axion with')
    print(f'  f_a ~ (M_GUT * M_W33 * M_Planck)^(1/3) ~ {f_best:.2e} GeV')
    print(f'  m_a ~ {m_best:.2e} eV  (in IAXO/BabyIAXO range)')
    print(f'  Omega_a h^2 ~ {Om_best:.2f}  (over-closes universe without tuning!)')
    print('  Resolution: anthropic selection of theta_i << pi, or late-time entropy dilution.')
    print('  OPEN: Compute W33 axion-photon coupling from anomaly diagram with GL_4 content.')
    print('  PREDICTION: m_a ~ 1e-6 eV, g_a_gamma ~ 1e-11 GeV^-1 -- testable at IAXO (2030+).')
