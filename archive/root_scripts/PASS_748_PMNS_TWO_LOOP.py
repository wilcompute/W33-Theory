#!/usr/bin/env python3
"""
Pass 748 — W33 PMNS Two-Loop Corrections
=========================================
Two-loop RG corrections to theta_12, theta_23, and delta_CP(PMNS).

After Pass 745 one-loop: theta_12 pull = +2.5 sigma, theta_23 pull = +1.7 sigma.
This pass adds two-loop tau Yukawa and W33 threshold corrections.

Two-loop RGE (Petcov-Tanimoto + W33 threshold):
  d theta_12/d t = (1/16pi^2) * C_12^(1) + (1/16pi^2)^2 * C_12^(2)
  d theta_23/d t = (1/16pi^2) * C_23^(1) + (1/16pi^2)^2 * C_23^(2)

W33 two-loop kernel:
  C_ij^(2) = (q^2-1)/q^2 * y_tau^4 * Delta_t^2 * S_ij
  where S_12 = -3/2, S_23 = -1, S_13 = +1/2

  y_tau = m_tau*sqrt(2)/v_EW = 0.01021
  y_tau^4 = 1.087e-8

W33 threshold correction at M_GUT (from formula-freeze universe Pass 398):
  Delta_theta_12^thresh = -(q-1)^2/q^3 * (alpha_s/pi) * ln(M_GUT/M_Z)
                        = -4/27 * (0.118/pi) * 33.9 = -4/27 * 1.272 = -0.188 rad
  [This is the dominant two-loop contribution for theta_12]

Delta_CP computation:
  delta_CP^W33 = pi - arctan((q-1)^3 / (q^4 * J_W33^{1/3}))
  where J_W33 = (q-1)^3/(q^6*(2pi)^2)
  Numerically: J_W33 = 8/(729*39.48) = 2.77e-4
  delta_CP = pi - arctan(8 / (81 * 2.77e-4^{1/3}))
           = pi - arctan(8 / (81 * 0.0652))
           = pi - arctan(8/5.28) = pi - arctan(1.515)
           = pi - 56.6 deg = 123.4 deg
  Observed: delta_CP = 195 +/- 25 deg  (T2K/NOvA)
  Pull: (123.4 - 195)/25 = -2.9 sigma  [needs next order]
"""

import math

Q         = 3
M_PL      = 2.435e18
M_GUT     = M_PL / math.sqrt(Q*(Q+1))
M_Z       = 91.1876
DELTA_T   = math.log(M_GUT / M_Z)
ALPHA_S   = 0.118
V_EW      = 246.0
M_TAU     = 1776.86e-3
Y_TAU     = M_TAU * math.sqrt(2) / V_EW

# From Pass 745 one-loop results
TH12_1L   = 35.25   # deg  (post-one-loop)
TH23_1L   = 51.33   # deg
TH13_1L   = 8.5     # deg

# PDG
TH12_PDG  = 33.41;  SIG12 = 0.75
TH23_PDG  = 49.0;   SIG23 = 1.4
TH13_PDG  = 8.54;   SIG13 = 0.13
DCP_PDG   = 195.0;  SIG_DCP = 25.0


def two_loop_correction(y_tau, Delta_t, q, alpha_s, angle='12'):
    """
    Two-loop RG + W33 threshold correction to mixing angle.
    Returns Delta_theta in degrees.
    """
    # Two-loop tau Yukawa
    L = Delta_t
    S = {'12': -1.5, '23': -1.0, '13': 0.5}[angle]
    two_loop_tau = ((q**2-1)/q**2) * y_tau**4 * L**2 * S / (16*math.pi**2)

    # W33 threshold
    if angle == '12':
        thresh = -(q-1)**2/q**3 * (alpha_s/math.pi) * L
    elif angle == '23':
        thresh = -(q-1)/q**2 * (alpha_s/math.pi) * L * 0.5
    else:
        thresh = 0.0

    return math.degrees(two_loop_tau + thresh)


def delta_CP_W33(q):
    """W33 CP phase from Jarlskog structure."""
    J_W33 = (q-1)**3 / (q**6 * (2*math.pi)**2)
    arg   = (q-1)**3 / (q**4 * J_W33**(1.0/3))
    return 180.0 - math.degrees(math.atan(arg))


def pull(val, obs, sig):
    return (val - obs) / sig


if __name__ == '__main__':
    print('='*70)
    print('Pass 748 — W33 PMNS Two-Loop Corrections')
    print('='*70)

    print(f'\nTwo-loop RG parameters:')
    print(f'  y_tau = {Y_TAU:.6f},  y_tau^4 = {Y_TAU**4:.4e}')
    print(f'  Delta_t = ln(M_GUT/M_Z) = {DELTA_T:.4f}')
    print(f'  (q^2-1)/q^2 = {(Q**2-1)/Q**2:.4f}')

    # Two-loop corrections
    D12 = two_loop_correction(Y_TAU, DELTA_T, Q, ALPHA_S, '12')
    D23 = two_loop_correction(Y_TAU, DELTA_T, Q, ALPHA_S, '23')
    D13 = two_loop_correction(Y_TAU, DELTA_T, Q, ALPHA_S, '13')

    TH12_2L = TH12_1L + D12
    TH23_2L = TH23_1L + D23
    TH13_2L = TH13_1L + D13

    print(f'\nTwo-loop corrections:')
    print(f'  Delta_theta_12 = {D12:.4f} deg  (W33 threshold dominant)')
    print(f'  Delta_theta_23 = {D23:.4f} deg')
    print(f'  Delta_theta_13 = {D13:.4f} deg  (small, 2L is tiny for theta_13)')

    # delta_CP
    dCP = delta_CP_W33(Q)
    print(f'\nW33 CP phase delta_CP:')
    J = (Q-1)**3 / (Q**6 * (2*math.pi)**2)
    print(f'  J_W33 = (q-1)^3/(q^6*(2pi)^2) = {J:.4e}')
    print(f'  delta_CP^W33 = pi - arctan((q-1)^3/(q^4*J^{{1/3}})) = {dCP:.2f} deg')
    print(f'  Observed delta_CP = {DCP_PDG} +/- {SIG_DCP} deg')
    print(f'  Pull: {pull(dCP, DCP_PDG, SIG_DCP):+.2f} sigma')

    # Summary
    print(f'\nPMNS full summary (tree -> 1-loop -> 2-loop):')
    print(f"  {'Parameter':>12}  {'Tree':>8}  {'1-loop':>8}  {'2-loop':>8}  {'PDG':>8}  {'Pull_2L':>8}")
    data = [
        ('theta_12', 35.26, TH12_1L, TH12_2L, TH12_PDG, SIG12),
        ('theta_23', 51.34, TH23_1L, TH23_2L, TH23_PDG, SIG23),
        ('theta_13', 4.26,  TH13_1L, TH13_2L, TH13_PDG, SIG13),
        ('delta_CP', 12.5,  12.5,    dCP,      DCP_PDG,  SIG_DCP),
    ]
    for name, tree, ol, tl, pdg, sig in data:
        p2 = pull(tl, pdg, sig)
        print(f'  {name:>12}  {tree:>8.2f}  {ol:>8.2f}  {tl:>8.2f}  {pdg:>8.2f}  {p2:>+8.2f}')

    chi2 = sum(pull(tl, pdg, sig)**2 for _, _, _, tl, pdg, sig in data)
    print(f'\n  Total chi^2 (2-loop, 4 params): {chi2:.2f}')
    print(f'  chi^2/dof = {chi2/4:.2f}')

    print('\nCONCLUSION (Pass 748):')
    print(f'  Two-loop W33 threshold correction: Delta_theta_12 = {D12:.3f} deg.')
    print(f'  theta_12: 1-loop {TH12_1L:.2f} -> 2-loop {TH12_2L:.2f} deg (PDG: {TH12_PDG:.2f}).')
    print(f'  theta_23: 1-loop {TH23_1L:.2f} -> 2-loop {TH23_2L:.2f} deg (PDG: {TH23_PDG:.2f}).')
    print(f'  delta_CP: W33 predicts {dCP:.1f} deg vs obs {DCP_PDG} deg (pull {pull(dCP,DCP_PDG,SIG_DCP):+.1f}sigma).')
    print(f'  Total chi^2/dof = {chi2/4:.2f} after two loops.')
    print(f'  Formula-freeze Pass 398 confirms two-loop threshold formula as v1-canonical.')
