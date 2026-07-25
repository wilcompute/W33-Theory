#!/usr/bin/env python3
"""
PASS 983 — W(3,3) Theta Series and Modular Form Connection
==========================================================

The adjacency spectrum {12^1, 2^24, (-4)^15} defines a theta series:

    Theta_{W33}(q) = sum_{n>=0} N(n) q^n

where N(n) = Tr(A^n)/v = [12^n + 24*2^n + 15*(-4)^n] / 40

KEY RESULTS:
- N(0) = 1, N(1) = 0, N(2) = 12 = k, N(3) = 24 = 6T/v
- Spectral zeta: zeta_L(-1) = 480 = kv (sum of degrees = partition fn)
- Heat kernel: K(t) = 1 + 24*e^{-10t} + 15*e^{-16t}
- Natural modular parameter: tau = 5i/8 = i*(lambda_L1/lambda_L2)
- zeta_L(2) = 24/100 + 15/256 = 0.2986,  v/zeta_L(2) = 133.94
  (close to 137 - 3 = 134, not exact — OPEN: what is the modular significance?)

Co-Authored-By: Perplexity AI
"""

import numpy as np
import json


def closed_walk_counts(n_max=20):
    """
    N(n) = Tr(A^n) / 40 = [12^n + 24*2^n + 15*(-4)^n] / 40
    """
    return {n: (12**n + 24*2**n + 15*(-4)**n) / 40 for n in range(n_max+1)}


def spectral_zeta_L(s):
    """zeta_L(s) = 24*10^{-s} + 15*16^{-s} (Laplacian, skip zero eval)."""
    return 24*10**(-s) + 15*16**(-s)


def heat_kernel_trace(t):
    """K(t) = Tr(e^{-tL}) = 1 + 24*e^{-10t} + 15*e^{-16t}."""
    return 1 + 24*np.exp(-10*t) + 15*np.exp(-16*t)


def run_all():
    print('='*60)
    print('PASS 983: W(3,3) Theta Series')
    print('='*60)

    # Closed walks
    print('\n[1] Closed Walk Counts N(n):')
    cwc = closed_walk_counts(20)
    for n in range(12):
        print(f'    N({n:2d}) = {cwc[n]}')
    print(f'    N(3) = 24 = 6 * (T/v) = 6 * (160/40) = 6*4  [triangles]  CHECK: {cwc[3]==24}')
    print(f'    N(2) = 12 = k = degree  CHECK: {cwc[2]==12}')

    # Spectral zeta values
    print('\n[2] Spectral Zeta zeta_L(s):')
    for s in [-1, 0, 0.5, 1, 2, 3]:
        if s == 0:
            val = 39.0  # number of nonzero Laplacian evals
        elif s == -1:
            val = 24*10 + 15*16  # = 480
        else:
            val = spectral_zeta_L(s)
        print(f'    zeta_L({s:4.1f}) = {val:.6f}')
    print(f'    zeta_L(-1) = 480 = k*v = 12*40  [sum of degrees]')
    print(f'    v/zeta_L(2) = {40/spectral_zeta_L(2):.4f}  [OPEN: significance?]')

    # Heat kernel
    print('\n[3] Heat Kernel Trace:')
    for t in [0.01, 0.1, 0.5, 1.0, 2.0]:
        print(f'    K({t:.2f}) = {heat_kernel_trace(t):.6f}')

    # Modular parameter
    tau = 5j/8  # = i * (lambda_L1/lambda_L2) = i * 10/16
    q = np.exp(2j*np.pi*tau)
    print(f'\n[4] Modular Parameter:')
    print(f'    tau = i*(10/16) = 5i/8 = {tau}')
    print(f'    q = e^{{2pi*i*tau}} = e^{{-5*pi/4}}')
    print(f'    |q| = {abs(q):.6f},  e^{{-5pi/4}} = {np.exp(-5*np.pi/4):.6f}')
    print(f'    CHECK: {abs(abs(q) - np.exp(-5*np.pi/4)) < 1e-12}')

    # Theta series first few terms
    print('\n[5] Theta series partial sum (first 10 terms):')
    theta_partial = sum(cwc[n] * abs(q)**n for n in range(10))
    print(f'    sum_{{n=0}}^9 N(n)|q|^n = {theta_partial:.6f}')

    cert = {
        'pass': 983,
        'N_2_eq_k': cwc[2] == 12,
        'N_3_eq_6Tv': cwc[3] == 24,
        'zeta_L_minus1': 480,
        'zeta_L_2': float(spectral_zeta_L(2)),
        'v_over_zeta_L_2': float(40/spectral_zeta_L(2)),
        'tau': '5i/8',
        'OPEN_modular_significance_of_v_over_zeta_L_2': True,
    }
    with open('analysis/w33_pass983_cert.json', 'w') as f:
        json.dump(cert, f, indent=2)
    print('\n[Certificate saved: analysis/w33_pass983_cert.json]')
    print(json.dumps(cert, indent=2))
    return cert


if __name__ == '__main__':
    run_all()
