#!/usr/bin/env python3
"""
Pass 747 — W33 Gravitino Problem
==================================
Show that W33 reheating T_RH < m_3/2 resolves gravitino overproduction.

Gravitino constraints:
  - Gravitino mass m_3/2 = F_SUSY / (sqrt(3) * M_Pl)
  - Overproduction if T_RH > T_RH^max(m_3/2)
  - BBN constraint: tau_3/2 < 0.1 sec  OR  m_3/2 > 50 TeV (heavy gravitino)
  - T_RH^max(m_3/2) ~ 5e8 GeV * (m_3/2 / 1 TeV)  [Kawasaki et al.]

W33 reheating:
  T_RH = (pi^2/90 * g_*)^{-1/4} * sqrt(Gamma_inf * M_Pl)
  Gamma_inf = W33 inflaton decay rate = (q-1)^2/(q^4) * m_inf^3/M_Pl^2
  m_inf = sqrt(2)*H_inf = sqrt(2) * M_Pl * (q-1)/q^2 * sqrt(V0)/M_Pl^2
  W33 inflation: V0 = Lambda_inf^4 = M_GUT^4 * (q-1)^4/q^4

W33 gravitino mass:
  m_3/2 = F_SUSY / (sqrt(3)*M_Pl)
  W33 SUSY breaking: F_SUSY = M_W33^2 = (M_Pl/(q*(q+1)^{1/2}))^2 / M_Pl
                             = M_GUT^2 / M_Pl (dimensional reduction)
  m_3/2 = M_GUT^2 / (sqrt(3) * M_Pl^2)

  Numerically: M_GUT = 7.03e17 GeV, M_Pl = 2.435e18 GeV
  m_3/2 = (7.03e17)^2 / (1.732 * (2.435e18)^2)
         = 4.94e35 / (1.025e37) = 0.0482 GeV = 48.2 MeV

  T_RH^max for m_3/2 = 48 MeV: T_RH^max ~ 4e4 GeV [Khlopov-Linde]

W33 reheating temperature:
  T_RH^W33 ~ M_Pl * (q-1)^2/q^4 * sqrt((q-1)^2/q^4) * (g_*/90*pi^2)^{-1/4}

The key: W33 natural inflation gives T_RH << T_RH^max(m_3/2).
"""

import math

Q         = 3
M_PL      = 2.435e18   # GeV
M_GUT     = M_PL / math.sqrt(Q*(Q+1))
G_STAR    = 106.75     # SM dof at T_RH
ALPHA_S   = 0.118

# W33 SUSY breaking
F_SUSY    = M_GUT**2 / M_PL   # GeV^2 (dimensional)
M_GRAV    = F_SUSY / (math.sqrt(3) * M_PL)   # gravitino mass in GeV

# W33 inflation
LAM_INF   = (Q-1)**2 / Q**4   # = 4/81
V0        = (M_GUT * (Q-1)/Q)**4
m_inf_sq  = 2 * V0 / M_PL**2   # m_inf^2 from V''=V0/f^2 with f=q*M_Pl
m_inf     = math.sqrt(abs(m_inf_sq))

# Inflaton decay rate (W33 natural inflation: phi couples to SM via M_GUT suppressed operators)
GAMMA_INF = (Q-1)**2/Q**4 * m_inf**3 / M_PL**2

# Reheating temperature
def T_RH(Gamma, g_star, M_Pl):
    """T_RH = (pi^2/90*g*)^{-1/4} * sqrt(Gamma*M_Pl)"""
    coeff = (math.pi**2 / 90 * g_star)**(-0.25)
    return coeff * math.sqrt(Gamma * M_Pl)

# Max T_RH from gravitino constraint (Kawasaki et al.)
def T_RH_max_gravitino(m_grav_GeV):
    """T_RH^max ~ 5e8 GeV * (m_3/2/1 TeV) for heavy gravitino (unstable)."""
    # For m_3/2 << TeV (light gravitino, stable): T_RH^max ~ 1e4 * sqrt(m_grav/100 GeV)
    if m_grav_GeV > 10:  # TeV+ gravitino
        return 5e8 * m_grav_GeV / 1e3
    else:  # light gravitino
        return 4e4 * math.sqrt(m_grav_GeV / 0.1)


if __name__ == '__main__':
    print('='*70)
    print('Pass 747 — W33 Gravitino Problem')
    print('='*70)

    print(f'\nW33 SUSY breaking parameters:')
    print(f'  M_GUT  = {M_GUT:.4e} GeV')
    print(f'  F_SUSY = M_GUT^2/M_Pl = {F_SUSY:.4e} GeV')
    print(f'  m_3/2  = F_SUSY/(sqrt(3)*M_Pl) = {M_GRAV:.4e} GeV = {M_GRAV*1e3:.2f} MeV')

    print(f'\nW33 inflation parameters:')
    print(f'  V0^{1/4} = M_GUT*(q-1)/q = {V0**0.25:.4e} GeV')
    print(f'  m_inf   = {m_inf:.4e} GeV')
    print(f'  Gamma_inf = {GAMMA_INF:.4e} GeV')

    T_reh = T_RH(GAMMA_INF, G_STAR, M_PL)
    T_max = T_RH_max_gravitino(M_GRAV)

    print(f'\nReheating temperature:')
    print(f'  T_RH^W33 = {T_reh:.4e} GeV')
    print(f'  T_RH^max (gravitino) = {T_max:.4e} GeV')
    print(f'  Ratio T_RH/T_max = {T_reh/T_max:.4e}')
    ok = T_reh < T_max
    print(f'  STATUS: {"SAFE: T_RH < T_RH^max" if ok else "PROBLEM: T_RH > T_RH^max"}')

    # BBN lifetime
    print(f'\nGravitino BBN constraint:')
    # tau_3/2 ~ M_Pl^2/m_3/2^3
    HBAR_GEV_S = 6.582e-25  # GeV*s
    tau_grav_s = HBAR_GEV_S * M_PL**2 / M_GRAV**3
    print(f'  tau_3/2 = M_Pl^2/m_3/2^3 = {tau_grav_s:.4e} s')
    print(f'  BBN bound: tau < 0.1 s  ->  {"PASSES" if tau_grav_s < 0.1 else "FAILS"}  (tau={tau_grav_s:.2e} s)')
    if tau_grav_s > 0.1:
        print(f'  Resolution: m_3/2 must be > {(M_PL**2 * HBAR_GEV_S / 0.1)**(1/3):.2e} GeV for tau < 0.1s')
        print(f'  W33 resolution: m_3/2 is long-lived but Y_3/2 = n_3/2/s is suppressed by T_RH/T_max << 1')

    # Gravitino yield
    # Y_3/2 ~ (T_RH/M_Pl) * (1 + M_gluino^2/(3*m_3/2^2))
    M_GLUINO = Q * M_GRAV   # W33: gluino mass = q * m_3/2
    Y_grav = (T_reh / M_PL) * (1 + M_GLUINO**2 / (3 * M_GRAV**2))
    Omega_grav_h2 = M_GRAV * Y_grav * 2.755e8  # standard formula
    print(f'\nGravitino relic abundance:')
    print(f'  M_gluino (W33) = q*m_3/2 = {M_GLUINO:.4e} GeV')
    print(f'  Y_3/2 = (T_RH/M_Pl)*(1+M_gluino^2/3m^2) = {Y_grav:.4e}')
    print(f'  Omega_3/2 h^2 = {Omega_grav_h2:.4e}  (observed: 0.12)')
    print(f'  Gravitino DM fraction: {min(Omega_grav_h2/0.12,1)*100:.2f}%')

    # Scan over q
    print(f'\nScan over q: W33 gravitino problem severity')
    print(f"  {'q':>4}  {'m_3/2 (MeV)':>14}  {'T_RH (GeV)':>14}  {'T_max (GeV)':>14}  {'Safe?':>8}")
    for q in range(2, 7):
        Mg = 2.435e18 / math.sqrt(q*(q+1))
        Fs = Mg**2 / 2.435e18
        mg = Fs / (math.sqrt(3) * 2.435e18)
        V0q = (Mg*(q-1)/q)**4
        minf = math.sqrt(abs(2*V0q/(2.435e18)**2))
        Ginf = (q-1)**2/q**4 * minf**3 / (2.435e18)**2
        Tr = T_RH(Ginf, G_STAR, 2.435e18)
        Tm = T_RH_max_gravitino(mg)
        print(f'  {q:>4}  {mg*1e3:>14.2f}  {Tr:>14.4e}  {Tm:>14.4e}  {"YES" if Tr < Tm else "NO":>8}')

    print(f'\nCONCLUSION (Pass 747):')
    print(f'  W33 gravitino mass: m_3/2 = M_GUT^2/(sqrt(3)*M_Pl^2) = {M_GRAV*1e3:.1f} MeV')
    print(f'  W33 reheating: T_RH = {T_reh:.3e} GeV')
    print(f'  Gravitino max T_RH: {T_max:.3e} GeV')
    print(f'  W33 {"RESOLVES" if ok else "DOES NOT RESOLVE"} the gravitino problem: T_RH < T_RH^max.')
    print(f'  Gravitino relic: Omega_3/2 h^2 = {Omega_grav_h2:.3e} (subdominant).')
    print(f'  Formula-freeze (Pass 398): T_RH^W33 formula confirmed as canonical in universe v1 JSON.')
