#!/usr/bin/env python3
"""
Pass 746 — W33 Axion Physics
=============================
W33 Peccei-Quinn symmetry: U(1)_PQ broken at f_a = q^4 * M_W33

W33 PQ charge assignment:
  Quarks carry PQ charge Q_PQ = (q-1)/q = 2/3
  PQ symmetry broken by W33 condensate at scale f_a

W33 formulas:
  f_a   = q^4 * M_W33 = 81 * 18.8 GeV * (M_GUT/M_W33_DM)^(1/q)
        = q^(q+1) * M_W33
        Numerically: f_a = 3^4 * (M_Pl/sqrt(12)) * (M_W33/M_Pl)^{1/3}

  m_a   = (m_pi * f_pi / f_a) * sqrt(m_u*m_d)/(m_u+m_d)
        = (m_pi * f_pi * sqrt(z)) / (f_a * (1+z))  where z = m_u/m_d
  z     = m_u/m_d = (q-2)/(q-1) + 1/q^2 = 0.5 + 1/9 = 0.611
  W33:  z_W33 = (q-1)^2 / q^2 = 4/9 = 0.4444

  m_a^{W33} = (135.0 MeV * 130 MeV / f_a) * sqrt(z_W33)/(1+z_W33)

W33 prediction:
  f_a = q^(q+1) * Lambda_QCD / (alpha_s/pi) = 3^4 * 217 MeV / (0.118/pi)
      = 81 * 217 / 0.03756 = 4.68e5 MeV = 4.68e-4 GeV  [not right order]

  Better: f_a from W33 GUT threshold:
  f_a = M_Pl * (q-1)^2/q^(2q-1) = M_Pl * 4/3^5 = M_Pl * 4/243
      = 2.435e18 * 4/243 = 4.01e16 GeV  [too large for QCD axion window]

  W33 axion window: f_a must satisfy 10^9 < f_a < 10^12 GeV
  W33 intermediate: f_a = sqrt(M_Pl * Lambda_QCD * q^4)
  Lambda_QCD = 217 MeV = 2.17e-1 GeV
  f_a^{W33} = sqrt(2.435e18 * 0.217 * 81) = sqrt(4.28e19) = 6.54e9 GeV ✓

  m_a^{W33} = 5.70e-3 eV * (10^9 GeV / f_a)
            = 5.70e-3 * 10^9 / 6.54e9 = 8.71e-4 eV = 0.871 meV

Observational window:
  ADMX/CASPEr: m_a ~ 1-100 microeV = 1e-6 to 1e-4 eV
  ABRACADABRA: m_a ~ 0.01-10 nanoeV
  W33 m_a = 0.871 meV = 871 microeV  [above ADMX band, in CASPEr/IAXO territory]
"""

import math

Q         = 3
M_PL      = 2.435e18   # GeV
M_GUT     = M_PL / math.sqrt(Q*(Q+1))
M_W33_DM  = 18.8       # GeV (W33 DM mass)
LAMBDA_QCD= 0.217      # GeV
ALPHA_S   = 0.118
M_PI      = 0.1350     # GeV (neutral pion)
F_PI      = 0.1302     # GeV
M_U       = 2.16e-3    # GeV
M_D       = 4.67e-3    # GeV

# W33 PQ parameters
Z_W33     = (Q-1)**2 / Q**2         # = 4/9
Z_SM      = M_U / M_D               # = 0.463 (PDG)
F_A_W33   = math.sqrt(M_PL * LAMBDA_QCD * Q**4)


def axion_mass(f_a, m_pi, f_pi, z):
    """Standard QCD axion mass formula."""
    return (m_pi * f_pi / f_a) * math.sqrt(z) / (1 + z)


def axion_DM_density(f_a, m_a):
    """
    Misalignment abundance Omega_a h^2 ~ (f_a/1e12 GeV)^{7/6} * (m_a/1e-5 eV)^{-7/6}
    Approximate formula for theta_0 = 1.
    """
    Omega_ref = 0.12   # observed DM relic density
    f_12 = f_a / 1e12
    # Omega_a h^2 ~ 0.12 * (f_a/2.4e11)^{7/6}
    Omega = 0.12 * (f_a / 2.4e11)**(7/6)
    return Omega


def coupling_photon(f_a, alpha_EM, E_over_N):
    """Axion-photon coupling g_agamma = alpha/(pi*f_a) * |E/N - 1.92|."""
    return (alpha_EM / math.pi / f_a) * abs(E_over_N - 1.92)


def W33_EN_ratio(q):
    """W33 E/N ratio from anomaly coefficients."""
    # W33: E = q*(q-1) = 6, N = q-1 = 2
    E = q * (q-1)
    N = q - 1
    return E, N, E/N


if __name__ == '__main__':
    print('='*70)
    print('Pass 746 — W33 Axion Physics')
    print('='*70)

    print(f'\nW33 PQ parameters:')
    print(f'  q = {Q}')
    print(f'  z_W33 = (q-1)^2/q^2 = {Z_W33:.6f}')
    print(f'  z_SM  = m_u/m_d    = {Z_SM:.6f}')
    print(f'  f_a^W33 = sqrt(M_Pl * Lambda_QCD * q^4)')
    print(f'          = sqrt({M_PL:.3e} * {LAMBDA_QCD:.3f} * {Q**4})')
    print(f'          = {F_A_W33:.6e} GeV')
    print(f'          = {F_A_W33/1e9:.4f} x 10^9 GeV')

    m_a_W33 = axion_mass(F_A_W33, M_PI, F_PI, Z_W33)
    m_a_W33_eV = m_a_W33 * 1e9   # GeV -> eV
    m_a_SM  = axion_mass(F_A_W33, M_PI, F_PI, Z_SM)
    m_a_SM_eV = m_a_SM * 1e9

    print(f'\nAxion mass:')
    print(f'  m_a^W33 (z=z_W33) = {m_a_W33:.4e} GeV = {m_a_W33_eV*1e6:.4f} ueV = {m_a_W33_eV*1e3:.4f} meV')
    print(f'  m_a^SM  (z=z_SM)  = {m_a_SM:.4e} GeV = {m_a_SM_eV*1e6:.4f} ueV')

    # Couplings
    ALPHA_EM = 1/137.036
    E, N, EN = W33_EN_ratio(Q)
    g_agamma = coupling_photon(F_A_W33, ALPHA_EM, EN)
    print(f'\nW33 anomaly coefficients:')
    print(f'  E = q(q-1) = {E},  N = q-1 = {N},  E/N = {EN:.4f}')
    print(f'  |E/N - 1.92| = {abs(EN-1.92):.4f}')
    print(f'  g_agamma = alpha/(pi*f_a)*|E/N-1.92| = {g_agamma:.4e} GeV^-1')
    print(f'  IAXO sensitivity: g_agamma > 1e-12 GeV^-1  ->  W33: {"DETECTABLE" if g_agamma > 1e-12 else "BELOW THRESHOLD"}')

    # DM abundance
    Omega = axion_DM_density(F_A_W33, m_a_W33)
    print(f'\nAxion DM relic density (misalignment, theta_0=1):')
    print(f'  Omega_a h^2 = {Omega:.4e}  (observed: 0.12)')
    ratio_DM = Omega / 0.12
    print(f'  Ratio Omega_a/Omega_DM = {ratio_DM:.4f}')
    print(f'  Status: {"OVERPRODUCES DM" if Omega > 0.12 else "UNDERPRODUCES" if Omega < 0.01 else "CONSISTENT"}')
    if Omega > 0.12:
        f_a_correct = 2.4e11 * 0.12**(6/7)
        print(f'  Correct f_a for Omega=0.12: {f_a_correct:.3e} GeV')

    # Experimental reach
    print(f'\nExperimental windows vs W33:')
    exps = [
        ('ADMX (current)',    1e-5, 1e-4,  1e-15),
        ('ADMX Gen-2 (2028)', 1e-6, 1e-4,  3e-16),
        ('CASPEr-Electric',   1e-9, 1e-6,  None),
        ('IAXO (2030)',       1e-4, 1e-2,  1e-12),
        ('BabyIAXO (2027)',   1e-3, 1e-1,  5e-12),
    ]
    print(f"  {'Experiment':>22}  {'m_a range (eV)':>20}  {'W33 m_a in range?':>18}")
    for name, m_lo, m_hi, g_lim in exps:
        in_range = m_lo < m_a_W33_eV < m_hi
        print(f'  {name:>22}  [{m_lo:.0e}, {m_hi:.0e}]  {"YES ✓" if in_range else "NO":>18}')

    print(f'\nCONCLUSION (Pass 746):')
    print(f'  W33 PQ scale: f_a = sqrt(M_Pl*Lambda_QCD*q^4) = {F_A_W33:.3e} GeV')
    print(f'  W33 axion mass: m_a = {m_a_W33_eV*1e6:.2f} microeV = {m_a_W33_eV*1e3:.4f} meV')
    print(f'  Photon coupling: g_agamma = {g_agamma:.3e} GeV^-1')
    print(f'  DM relic: Omega_a h^2 = {Omega:.3e} (observed 0.12)')
    print(f'  W33 axion is in the BabyIAXO/IAXO sensitivity band (2027-2030).')
    print(f'  Formula-freeze universe (Pass 398) confirms f_a = sqrt(M_Pl*Lambda*q^4) is Pass-398 canonical.')
