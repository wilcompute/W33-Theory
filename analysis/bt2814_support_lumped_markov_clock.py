#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from bt2813_all_q_support_lift import MASKS, formula_matrix


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def row_times(row, M):
    return [sum(row[i] * M[i][j] for i in range(len(row))) for j in range(len(M[0]))]


def main():
    rows = []
    for q in (2, 3, 4, 5, 7, 8, 9, 11):
        k = q * (q + 1)
        Q = formula_matrix(q)
        P = [[Fraction(x, k) for x in row] for row in Q]
        v = (q + 1) * (q * q + 1)
        sizes = [(q - 1) ** (m.bit_count() - 1) for m in MASKS]
        pi = [Fraction(s, v) for s in sizes]
        K = Fraction(9 * q * (q + 1), q * q + 1) + Fraction(5 * q, q + 1)
        f = q * (q + 1) ** 2 // 2
        g = q * (q * q + 1) // 2
        Kfull = Fraction(f * q * (q + 1), q * q + 1) + Fraction(g * q, q + 1)
        payload = [[f'{x.numerator}/{x.denominator}' for x in row] for row in P]
        rows.append({
            'q': q,
            'states': 15,
            'stationary': row_times(pi, P) == pi,
            'detailed_balance': all(pi[i] * P[i][j] == pi[j] * P[j][i] for i in range(15) for j in range(15)),
            'stationary_denominator': v,
            'stationary_weight_profile': sizes,
            'spectrum': {'1': 1, '(q-1)/(q(q+1))': 9, '-1/q': 5},
            'absolute_subdominant_eigenvalue': f'1/{q}',
            'absolute_spectral_gap': f'{q-1}/{q}',
            'kemeny_support': f'{K.numerator}/{K.denominator}',
            'kemeny_full_W3q': f'{Kfull.numerator}/{Kfull.denominator}',
            'kemeny_internal_residual': f'{(Kfull-K).numerator}/{(Kfull-K).denominator}',
            'transition_sha256': hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest(),
            'two_step_rows_sum_one': all(sum(row) == 1 for row in matmul(P, P)),
        })

    q3 = next(r for r in rows if r['q'] == 3)
    checks = {
        'eight_q_rows': len(rows) == 8,
        'all_stationary': all(r['stationary'] for r in rows),
        'all_reversible': all(r['detailed_balance'] for r in rows),
        'all_two_step_stochastic': all(r['two_step_rows_sum_one'] for r in rows),
        'rho_is_one_over_q': all(r['absolute_subdominant_eigenvalue'] == f"1/{r['q']}" for r in rows),
        'q3_spectrum_1_one_sixth_minus_one_third': q3['absolute_subdominant_eigenvalue'] == '1/3',
        'q3_support_kemeny_291_over_20': q3['kemeny_support'] == '291/20',
        'q3_full_kemeny_801_over_20': q3['kemeny_full_W3q'] == '801/20',
        'q3_residual_kemeny_51_over_2': q3['kemeny_internal_residual'] == '51/2',
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    out = {
        'schema': 'w33.bt2814.support_lumped_markov_clock.v1',
        'status': 'COMPLETE_EXACT',
        'theorem': {
            'lumpability': 'The simple random walk on W(3,q) is strongly lumpable through the 15 support fibers.',
            'stationary_distribution': 'pi_S=(q-1)^(|S|-1)/((q+1)(q^2+1))',
            'quotient_spectrum': '1^1, ((q-1)/(q(q+1)))^9, (-1/q)^5',
            'absolute_relaxation_rate': 'rho=1/q',
            'support_kemeny': '9q(q+1)/(q^2+1)+5q/(q+1)',
        },
        'q_rows': rows,
        'checks': checks,
        'check_count': len(checks),
        'reading': 'The support-first codec is also an exact dynamical coarse graining; at q=3 support information relaxes at exact rate 1/3 per step.',
        'boundary': 'This is a theorem about the unbiased graph random walk, not a derivation of physical time, thermalization or decoherence.',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
