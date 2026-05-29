#!/usr/bin/env python3
"""Verify a selection of W(3,3) substrate predictions against reference values.

Saves a short report to stdout. Intended as a lightweight, reproducible checker
for the closed-form identities present in the TeX companions.
"""
from fractions import Fraction
import math


def pctdiff(pred, ref):
    try:
        return 100.0 * (pred - ref) / ref
    except Exception:
        return float('nan')


def main():
    # Substrate primitives
    q = 3
    mu = q + 1
    qfact = math.factorial(q)
    Phi3 = q**2 + q + 1
    Phi4 = q**2 + 1
    Phi6 = q**2 - q + 1
    k = mu * q
    v = (q**4 - 1) // (q - 1)
    E = v * k // 2

    # Reference (approx.) experimental values (rounded to companion precision)
    ref = {
        'alpha_inv': 137.035999084,   # CODATA-ish
        'mp_me': 1836.15267343,
        'sin2_thetaW': 0.23122,
        'nu_ratio': 33.96,
        'V_us_sq': 0.0495,
        'alpha_s_inv': 8.467,
        'mW_GeV': 80.379,
        'mZ_GeV': 91.1876,
        'mH_GeV': 125.10,
        'n_s': 0.9649,
    }

    results = []

    # alpha inverse (companion formula)
    alpha_inv_pred = 2**Phi6 + q**2 + float(Fraction(1, mu * Phi6))
    results.append(('alpha_inv', alpha_inv_pred, ref['alpha_inv']))

    # proton / electron mass ratio (companion uses Ogg_7 = 17)
    Ogg_7 = 17
    mp_me_pred = k * q**2 * Ogg_7
    results.append(('mp_me', mp_me_pred, ref['mp_me']))

    # sin^2 theta_W
    sin2_pred = q / Phi3
    results.append(('sin2_thetaW', sin2_pred, ref['sin2_thetaW']))

    # neutrino mass-squared ratio
    nu_ratio_pred = v - qfact
    results.append(('nu_ratio', nu_ratio_pred, ref['nu_ratio']))

    # |V_us|^2
    Vus_sq_pred = 2.0 / v
    results.append(('V_us_sq', Vus_sq_pred, ref['V_us_sq']))

    # alpha_s inverse prediction
    alpha_s_inv_pred = (2**q) + qfact / Phi3
    results.append(('alpha_s_inv', alpha_s_inv_pred, ref['alpha_s_inv']))

    # electroweak masses (integer-ish predictions in companion)
    mW_pred = 2 * v
    mZ_pred = Phi6 * Phi3
    mH_pred = (mu + 1) ** q
    results.append(('mW_GeV', mW_pred, ref['mW_GeV']))
    results.append(('mZ_GeV', mZ_pred, ref['mZ_GeV']))
    results.append(('mH_GeV', mH_pred, ref['mH_GeV']))

    # CMB tilt
    n_s_pred = q**q / (mu * Phi6)
    results.append(('n_s', n_s_pred, ref['n_s']))

    # Print report
    print('W(3,3) substrate quick verification')
    print('-----------------------------------')
    print(f'q={q}, mu={mu}, k={k}, v={v}, Phi3={Phi3}, Phi4={Phi4}, Phi6={Phi6}')
    print()
    print(f'{"name":<15}{"pred":>12}{"ref":>12}{"pctdiff":>10}')

    for name, pred, r in results:
        pd = pctdiff(pred, r)
        print(f'{name:<15s}{pred:12.6g}{r:12.6g}{pd:10.3f}%')


if __name__ == '__main__':
    main()
