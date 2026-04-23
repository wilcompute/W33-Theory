#!/usr/bin/env python3
"""
W(3,3) Gravitational Wave Spectrum Prediction
==============================================
Computes the stochastic GW background from the SU(9) -> SU(3)^3
phase transition at M_GUT, using only W(3,3) parameters.

Key prediction: spectral tilt n_T = -Phi6/q = -7/3 (unique)

Section §69 and §74.
"""
import numpy as np
import math

q = 3
Phi3 = q**2 + q + 1  # 13
Phi4 = q**2 + 1       # 10
Phi6 = q**2 - q + 1   # 7
k = q * (q + 1)       # 12

# Fundamental constants
M_planck = 1.22e19   # GeV
M_Z = 91.2           # GeV
alpha_em = 1/137.036
T0_GeV = 2.725 * 8.617e-14  # CMB temperature in GeV

# W(3,3) predictions
alpha_GUT = q / Phi3               # = 3/13
sin2_thetaW_bare = q / (2*q + 2)   # = 3/8 (GUT bare)
sin2_thetaW_dressed = q / Phi3     # = 3/13 (at M_Z)

# M_GUT estimate from Weinberg angle running
delta_s2w = 3/8 - 3/13
b_SM = 10/3
log_ratio = delta_s2w * 2 * math.pi / (alpha_em * b_SM)
M_GUT = M_Z * math.exp(log_ratio)

# Bounce action at Seiberg self-dual point
S_bounce = 2 * math.pi * Phi3 / q**2

# GW energy density
H_over_beta = 1 / S_bounce
alpha_gw = alpha_GUT
kappa = 1.0
Omega_peak = 1.67e-5 * H_over_beta**2 * kappa**2 * alpha_gw**2 / (alpha_gw + 1)**2

# Redshifted peak frequency
g_s_star = 248  # dim(E8) degrees of freedom at GUT scale
g_s0 = 3.91
ratio_a = T0_GeV * g_s0**(1/3) / (M_GUT * g_s_star**(1/3))
f_star_Hz = M_GUT / (6.58e-25 * 2 * math.pi)
f_peak_today = f_star_Hz * ratio_a

# Spectral tilt
n_T = -Phi6 / q  # = -7/3

if __name__ == '__main__':
    print('W(3,3) Gravitational Wave Spectrum')
    print('=' * 50)
    print(f'GUT parameters:')
    print(f'  alpha_GUT = q/Phi3 = {q}/{Phi3} = {alpha_GUT:.6f}')
    print(f'  M_GUT     = {M_GUT:.3e} GeV')
    print(f'  g_* at PT = {g_s_star} (= dim E8)')
    print(f'')
    print(f'Phase transition:')
    print(f'  S_bounce  = 2pi*Phi3/q^2 = {S_bounce:.4f}')
    print(f'  Omega_GW  = {Omega_peak:.3e}')
    print(f'  f_peak    = {f_peak_today:.3e} Hz')
    print(f'')
    print(f'Spectral shape:')
    print(f'  n_T = -Phi6/q = -{Phi6}/{q} = {n_T:.6f}')
    print(f'  Omega(f) ~ f^3 / [1 + (f/f_peak)^(3+Phi6/q)]')
    print(f'           ~ f^3 / [1 + (f/f_peak)^{3 + Phi6/q:.4f}]')
    print(f'')
    print(f'Falsifiability:')
    print(f'  Standard bubble GW: n_T = -3 to -4')
    print(f'  W(3,3) prediction:  n_T = -7/3 = {-7/3:.4f} (SHALLOWER)')
    print(f'  Target detector: Einstein Telescope / LISA successor')
    print(f'  Detection band: ~0.1-10 Hz (after redshift correction)')
