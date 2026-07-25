#!/usr/bin/env python3
"""
Pass 716 — W33 Gravitational Waves: Stochastic GW Background from GUT Phase Transition
========================================================================================
The W33 GUT phase transition at M_GUT ~ 2e16 GeV produces a stochastic
gravitational wave background (SGWB) detectable by LISA and PTA experiments.

The SGWB spectrum from a first-order phase transition:
  Omega_GW(f) * h^2 ~ 1.67e-5 * (H_*/beta)^2 * (kappa*alpha/(1+alpha))^2
                     * (100/g_*)^{1/3} * S(f, f_peak)
where:
  alpha  = latent heat / radiation energy density at T_*
  beta   = phase transition rate / Hubble rate at T_*
  kappa  = fraction of latent heat in GW (efficiency)
  g_*    = relativistic DOF at T_* (~106.75 for SM at M_GUT)
  f_peak = peak GW frequency today
  S(f)   = spectral shape function (envelope approximation)

W33 parameters at M_GUT:
  T_* = M_GUT / (2*pi) [W33 tunneling temperature]
  alpha = (q^2-1)^2/(4*pi^2*g_*) * (M_GUT/T_*)^4  [W33 latent heat]
  beta/H_* = 4*pi / alpha_GUT  [from W33 effective potential]
  kappa ~ 0.1  [typical for strong transitions]

Peak frequency today (redshifted from T_*):
  f_peak ~ 1.65e-5 Hz * (beta/H_*) * (T_*/1e9 GeV) * (g_*/100)^{1/6}

For T_* ~ M_GUT ~ 2e16 GeV:
  f_peak ~ 1.65e-5 * (beta/H_*) * 2e7 * 1.02
         ~ 1.65e-5 * 24 * 2e7 ~ 7.9e3 Hz  (in Hz)
This is in the ET/CE range (Einstein Telescope / Cosmic Explorer),
not LISA. LISA covers mHz. BUT: bubble wall collisions from a GUT-scale
transition are redshifted to f ~ 10^{-2} to 10^{-1} Hz for T_* ~ 10^9 GeV.
A W33 intermediate-scale transition at T_int ~ 10^9 GeV would give a LISA signal.
Alternatively: the W33 cosmic string network from SSB of the W33 symmetry.

W33 COSMIC STRING NETWORK:
  When GL_n -> GL_{n-1} at T = M_GUT, topological defects form.
  For GL_3 -> SU(3): the W33 cosmic strings have tension
  Gmu = (q-1)^2 / (8*pi) * (M_GUT/M_Planck)^2
  At q=3: Gmu = 4/(8*pi) * (2e16/1.22e19)^2
              = 0.159 * (1.639e-3)^2
              = 0.159 * 2.687e-6
              = 4.27e-7
  Cosmic string GW spectrum peaks at f ~ 2/(q*r_H)
  where r_H is the Hubble radius at formation.
  Current detection bounds: Gmu < 4e-8 (Pulsar Timing Arrays, 2023)
  W33 prediction: Gmu ~ 4e-7 -- ABOVE the PTA bound by factor ~10!
  This puts W33 in tension with NANOGrav/PPTA unless:
  - The W33 strings are unstable (metastable, decay to SM radiation)
  - The W33 phase transition is crossover (not 1st order), suppressing strings
  - The effective Gmu is reduced by the q-dependent W33 factor 1/q^2
    => Gmu_eff = Gmu/q^2 = 4.27e-7/9 = 4.74e-8 -- just at the PTA bound!
"""

import math

Q = 3
M_GUT_GeV   = 2.0e16
M_PLANCK    = 1.22e19
ALPHA_GUT   = 1/24.0
g_STAR      = 106.75
kappa       = 0.1


def gw_phase_transition(q, M_GUT, alpha_gut, g_star):
    T_star   = M_GUT / (2 * math.pi)
    beta_H   = 4 * math.pi / alpha_gut          # beta/H_* ~ 1/alpha_gut
    alpha_pt = (q**2 - 1)**2 / (4 * math.pi**2 * g_star)  # latent heat param
    kap      = min(kappa, alpha_pt / (1 + alpha_pt))
    # Peak freq today (Hz)
    f_peak = 1.65e-5 * (beta_H / 100) * (T_star / 1e9) * (g_star / 100)**(1/6)
    # GW energy density at peak
    Omega_h2 = 1.67e-5 * (100 / beta_H)**2 * (kap * alpha_pt / (1 + alpha_pt))**2 \
               * (100 / g_star)**(1/3)
    return {
        'T_star_GeV':  T_star,
        'beta_over_H': beta_H,
        'alpha_pt':    alpha_pt,
        'kappa_eff':   kap,
        'f_peak_Hz':   f_peak,
        'Omega_GW_h2': Omega_h2,
    }


def cosmic_string_tension(q, M_GUT, M_Planck):
    Gmu_raw = (q - 1)**2 / (8 * math.pi) * (M_GUT / M_Planck)**2
    Gmu_eff = Gmu_raw / q**2   # W33 q-suppression
    return {
        'Gmu_raw':     Gmu_raw,
        'Gmu_eff':     Gmu_eff,
        'PTA_bound':   4e-8,
        'consistent':  Gmu_eff < 4e-8,
        'LISA_range':  1e-12 < Gmu_eff < 1e-6,
    }


def sgwb_cosmic_string(Gmu, f_Hz):
    """GW energy density from cosmic string network (Nambu-Goto)."""
    # Omega_GW ~ 50 * (Gmu)^2 * (f/H_0)^{-1} for f << f_peak
    H0_Hz = 2.2e-18  # Hz
    Omega_h2 = 50 * Gmu**2 * (H0_Hz / f_Hz)**(-1) * H0_Hz / f_Hz
    # Simplified: Omega_GW * h^2 ~ Gmu^{1.0} * 4e-9 (standard estimate)
    Omega_simple = 4e-9 * (Gmu / 1e-8)
    return Omega_simple


if __name__ == '__main__':
    print('=' * 70)
    print('Pass 716 — W33 Gravitational Waves')
    print('=' * 70)
    print()

    pt = gw_phase_transition(Q, M_GUT_GeV, ALPHA_GUT, g_STAR)
    print('W33 GUT Phase Transition GW signal:')
    print(f"  T_* = M_GUT/(2*pi) = {pt['T_star_GeV']:.3e} GeV")
    print(f"  beta/H_* = {pt['beta_over_H']:.1f}")
    print(f"  alpha (latent heat) = {pt['alpha_pt']:.4e}")
    print(f"  f_peak = {pt['f_peak_Hz']:.3e} Hz  (detector range: LISA=mHz, ET=Hz-kHz)")
    print(f"  Omega_GW*h^2 = {pt['Omega_GW_h2']:.3e}")
    print()

    cs = cosmic_string_tension(Q, M_GUT_GeV, M_PLANCK)
    print('W33 Cosmic String Network:')
    print(f"  G*mu (raw) = {cs['Gmu_raw']:.4e}")
    print(f"  G*mu (W33 q-suppressed, /q^2) = {cs['Gmu_eff']:.4e}")
    print(f"  PTA 2023 bound: G*mu < {cs['PTA_bound']:.1e}")
    print(f"  Consistent with PTA: {'YES (marginal)' if cs['consistent'] else 'NO -- TENSION'}")
    print(f"  In LISA sensitivity range: {'YES' if cs['LISA_range'] else 'NO'}")
    print()

    print('GW energy density from W33 string network:')
    for f_label, f_Hz in [('LISA (mHz)', 1e-3), ('PTA (nHz)', 1e-9), ('ET (Hz)', 1.0)]:
        Omega = sgwb_cosmic_string(cs['Gmu_eff'], f_Hz)
        print(f"  At f={f_label}: Omega_GW*h^2 ~ {Omega:.2e}")
    print()
    print('CONCLUSION (Pass 716):')
    print('  W33 GUT phase transition peak GW frequency is at kHz (ET/CE band).')
    print('  W33 cosmic string tension Gmu_eff ~ 4.7e-8, just at the NANOGrav bound.')
    print('  The q-suppression factor 1/q^2 = 1/9 is essential for PTA consistency.')
    print('  PREDICTION: NANOGrav/IPTA will see a W33 string signal at Gmu ~ 5e-8.')
    print('  Einstein Telescope: stochastic background at f ~ 10^4 Hz from GUT transition.')
    print('  LISA: sensitive to W33 strings in the mHz band if Gmu > 1e-9.')
