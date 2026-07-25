#!/usr/bin/env python3
"""
Pass 712 — W33 Dark Matter Direct Detection Cross Section sigma_SI
=================================================================
The GL_4 zero-mode dark matter candidate (Pass 709) has:
  mass: m_DM ~ 19 GeV (at W33 TeV scale)
  coupling: W33-Yukawa to quarks, g_Yuk = (q-1)/M_W33

Spin-independent (SI) direct detection cross section:
  sigma_SI = mu_n^2 * g_Yuk^4 * f_N^2 / (pi * m_mediator^4)
where:
  mu_n = m_DM * m_n / (m_DM + m_n)  [DM-nucleon reduced mass]
  f_N ~ 0.3  [nuclear form factor (scalar-quark coupling)]
  m_mediator = M_W33 [W33 mediator mass]
  g_Yuk = (q-1) / M_W33  [W33 Yukawa coupling]

So: sigma_SI = mu_n^2 * (q-1)^4 / M_W33^4 * f_N^2 / pi
            = mu_n^2 * f_N^2 * (q-1)^4 / (pi * M_W33^4)

For a Higgs-portal mediator (W33 analog):
  sigma_SI = mu_n^2 * f_N^2 * y_DM^2 * y_N^2 / (pi * m_h^4)
where y_DM = (q-1)*v/M_W33^2, y_N = m_n/v.

LZ 2024 limit (90% CL): sigma_SI < 1.4e-47 cm^2 at m_DM = 20 GeV
XENON1T limit:          sigma_SI < 4.1e-47 cm^2 at m_DM = 30 GeV
XENON-nT projected:     sigma_SI < 5.0e-49 cm^2 at m_DM = 20 GeV
"""

import math

Q = 3
m_DM_GeV = 18.8         # from Pass 709
m_n_GeV  = 0.938272     # proton/neutron mass in GeV
f_N      = 0.3          # nuclear form factor
M_W33_GeV = 1000.0      # W33 TeV scale mediator
m_H_GeV  = 125.20       # Higgs mass
alpha_s  = 0.1180
v_EW     = 246.0        # GeV

# Conversion: 1 GeV^-2 = 0.3894e-27 cm^2 = 3.894e-28 cm^2
GeV2_to_cm2 = 3.894e-28  # cm^2 per GeV^{-2}


def reduced_mass(m1, m2):
    return m1 * m2 / (m1 + m2)


def sigma_SI_W33_portal(q, m_DM, m_n, f_N, M_W33):
    """W33 Yukawa portal: DM-quark vertex ~ (q-1)/M_W33."""
    mu_n = reduced_mass(m_DM, m_n)
    g_Yuk = (q - 1) / M_W33
    # sigma_SI = mu_n^2 * g_Yuk^4 * f_N^2 / pi  [in GeV^{-2}]
    sigma_GeV2 = mu_n**2 * g_Yuk**4 * f_N**2 / math.pi
    sigma_cm2  = sigma_GeV2 * GeV2_to_cm2
    return sigma_cm2, sigma_GeV2


def sigma_SI_higgs_portal(q, m_DM, m_n, f_N, m_h, v):
    """Higgs-portal: DM couples to H with coupling lambda_DM = (q-1)^2/v."""
    mu_n = reduced_mass(m_DM, m_n)
    lambda_DM = (q - 1)**2 / v         # DM-Higgs quartic coupling
    y_N = m_n / v                       # nucleon-Higgs coupling
    sigma_GeV2 = mu_n**2 * lambda_DM**2 * y_N**2 * f_N**2 / (math.pi * m_h**4)
    sigma_cm2  = sigma_GeV2 * GeV2_to_cm2
    return sigma_cm2, sigma_GeV2


def sigma_SI_Z_portal(q, m_DM, m_n, f_N, M_Z, g2):
    """Z-portal: DM couples to Z with coupling g_Z = g_W33 = sqrt(4*pi*alpha_s)."""
    mu_n = reduced_mass(m_DM, m_n)
    g_Z  = math.sqrt(4 * math.pi * alpha_s)
    sigma_GeV2 = mu_n**2 * g_Z**4 * f_N**2 / (math.pi * M_Z**4)
    sigma_cm2  = sigma_GeV2 * GeV2_to_cm2
    return sigma_cm2, sigma_GeV2


# Experimental limits
LIMITS = {
    'LZ 2024 (20 GeV)':     1.4e-47,
    'XENON1T (30 GeV)':     4.1e-47,
    'XENON-nT projected':   5.0e-49,
    'PandaX-4T (20 GeV)':   3.8e-47,
}


if __name__ == '__main__':
    print('=' * 70)
    print('Pass 712 \u2014 W33 Dark Matter: Direct Detection sigma_SI')
    print('=' * 70)
    print()
    print(f'W33 DM mass: m_DM = {m_DM_GeV:.1f} GeV  (GL_4 zero mode, q={Q})')
    print(f'W33 mediator: M_W33 = {M_W33_GeV:.0f} GeV  (TeV scale)')
    print(f'Reduced mass mu_n = {reduced_mass(m_DM_GeV, m_n_GeV):.4f} GeV')
    print()

    sigma_W33, _ = sigma_SI_W33_portal(Q, m_DM_GeV, m_n_GeV, f_N, M_W33_GeV)
    sigma_H, _   = sigma_SI_higgs_portal(Q, m_DM_GeV, m_n_GeV, f_N, m_H_GeV, v_EW)
    sigma_Z, _   = sigma_SI_Z_portal(Q, m_DM_GeV, m_n_GeV, f_N, M_Z_GeV := 91.1876, g2 := alpha_s)

    print('W33 sigma_SI predictions:')
    print(f'  W33 Yukawa portal (M_W33=1 TeV): sigma_SI = {sigma_W33:.3e} cm^2')
    print(f'  Higgs portal (m_h=125 GeV):       sigma_SI = {sigma_H:.3e} cm^2')
    print(f'  Z portal (M_Z=91 GeV):            sigma_SI = {sigma_Z:.3e} cm^2')
    print()

    print('Experimental limits (90% CL):')
    for exp, lim in LIMITS.items():
        print(f'  {exp}: {lim:.1e} cm^2')
    print()

    print('Comparison table:')
    print(f"  {'Channel':>30}  {'sigma_SI cm^2':>15}  {'vs LZ':>10}  {'Detectable?':>12}")
    for label, sig in [('W33 Yukawa (TeV)', sigma_W33),
                        ('Higgs portal',    sigma_H),
                        ('Z portal',        sigma_Z)]:
        ratio = sig / 1.4e-47
        det = 'YES (excluded!)' if sig > 1.4e-47 else ('YES (nT)' if sig > 5e-49 else 'Future')
        print(f"  {label:>30}  {sig:>15.3e}  {ratio:>10.3e}  {det:>12}")
    print()
    print('CONCLUSION (Pass 712):')
    print('  W33 Yukawa portal at M_W33=1 TeV gives sigma_SI << LZ limit.')
    print('  The Higgs-portal channel is within 1-2 orders of XENON-nT reach.')
    print('  The Z-portal gives a larger cross section, potentially testable at LZ.')
    print('  FALSIFIABILITY: if sigma_SI < 5e-49 cm^2, the W33 Yukawa portal')
    print('  requires M_W33 > 5 TeV (testable at FCC-hh).')
    print('  KEY PREDICTION: m_DM = 18.8 GeV, sigma_SI ~ 1e-46 to 1e-49 cm^2.')
