#!/usr/bin/env python3
"""Arithmetic verification companion for paper/w33_holographic_tower_final.tex."""
from __future__ import annotations

import json
from pathlib import Path


def norm_eisenstein(a: int, b: int) -> int:
    return a*a - a*b + b*b


def peval(coeffs, x):
    return sum(c*(x**i) for i, c in enumerate(coeffs))


def mul_one_plus_t(q):
    out = [0]*(len(q)+1)
    for i, c in enumerate(q):
        out[i] += c
        out[i+1] += c
    return out


def mod_phi3(coeffs):
    poly = list(coeffs)
    while len(poly) > 2:
        c = poly[-1]
        if c:
            poly[-2] -= c
            poly[-3] -= c
        poly.pop()
    return tuple(poly + [0]*(2-len(poly)))


def main():
    checks = {}
    q, g, h = 3, 6, 12
    checks['substrate_lengths'] = {
        'passed': q**5-q == 240 and g*h == 72 and g*(h-1) == 66,
        'values': {'q': q, 'g': g, 'h': h, 'nB': q**5-q, 'nH': g*h, 'kH': g*(h-1)},
    }
    checks['support_biregularity'] = {
        'passed': 160*81 == 1620*8 == 12960,
        'values': {'160*81': 160*81, '1620*8': 1620*8},
    }
    phases = {0: 984960, 1: 25920, 2: 25920}
    checks['E6_noncommutation'] = {
        'passed': sum(phases.values()) == 320*3240 and phases[1]+phases[2] == 2**7*3**4*5 == 51840,
        'values': {'phase_counts': phases, 'total': 320*3240, 'nonzero': phases[1]+phases[2]},
    }
    xrow = {1: 81, 3: 54, 9: 18, 27: 6}
    checks['X_3adic_visibility'] = {
        'passed': sum(xrow.values()) == 159 and {k: 160*v//2 for k, v in xrow.items()} == {1: 6480, 3: 4320, 9: 1440, 27: 480},
        'values': {'per_row': xrow, 'global_unordered': {k: 160*v//2 for k, v in xrow.items()}},
    }
    zrow = {0: 1187, 1: 288, 2: 96, 3: 32, 4: 16}
    checks['Z_dual_visibility'] = {
        'passed': sum(zrow.values()) == 1619 and sum(v for k, v in zrow.items() if k) == 432,
        'values': {'per_row': zrow, 'global_unordered': {k: 1620*v//2 for k, v in zrow.items()}},
    }
    P = [68,147,127,86,54,19,3]
    Q = [68,79,48,38,16,3]
    checks['toroidal_generating_function'] = {
        'passed': mul_one_plus_t(Q) == P and peval(P,-1) == 0 and peval(Q,-1) == 12 and peval(P,1) == 504 and peval(Q,1) == 252 and mod_phi3(P) == (11,55) and norm_eisenstein(11,55) == 11**2*21,
        'values': {'P': P, 'Q': Q, 'P(-1)': peval(P,-1), 'Q(-1)': peval(Q,-1), 'P(1)': peval(P,1), 'Q(1)': peval(Q,1), 'P_mod_Phi3': mod_phi3(P), 'Norm(11+55w)': norm_eisenstein(11,55)},
    }
    result = {'all_checks_passed': all(c['passed'] for c in checks.values()), 'checks': checks}
    out = Path(__file__).resolve().parents[1] / 'data' / 'w33_holographic_tower_paper_checks.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['all_checks_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
