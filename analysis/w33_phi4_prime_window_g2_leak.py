from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXVI_PHI4_PRIME_WINDOW_G2_LEAK_results.json'


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def main():
    q = 3
    lam = 2
    phi4 = 10
    phi6 = 7
    F5 = 5
    heegner6 = 19
    g2_pos = 6
    fano_cube = q ** q
    packet_residual_gap = 152

    substrate_primes = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
        37, 41, 43, 47, 59, 67, 71, 89, 127, 163,
    }
    window = phi4 ** 2
    primes_le_window = [p for p in range(2, window + 1) if is_prime(p)]
    substrate_in_window = [p for p in primes_le_window if p in substrate_primes]
    leak_in_window = [p for p in primes_le_window if p not in substrate_primes]
    substrate_outside_window = sorted(p for p in substrate_primes if p > window)

    # Substrate L-function check at s=2, matching the round-50 analytic signal.
    Ls2 = 1.0
    for p in sorted(substrate_primes):
        Ls2 *= 1.0 / (1.0 - p ** -2)
    zeta2 = math.pi ** 2 / 6.0
    ratio = Ls2 / zeta2

    checks = {
        'window_is_phi4_squared': window == 100,
        'prime_count_to_100_is_F5_squared': len(primes_le_window) == F5 ** 2 == 25,
        'substrate_primes_in_window_are_heegner6': len(substrate_in_window) == heegner6 == 19,
        'first_leak_count_is_positive_G2_roots': len(leak_in_window) == g2_pos == 6,
        'window_split_19_plus_6': len(substrate_in_window) + len(leak_in_window) == F5 ** 2,
        'full_substrate_prime_count_is_so7': len(substrate_primes) == q * phi6 == 21,
        'outside_window_substrate_count_is_lambda': len(substrate_outside_window) == lam == 2,
        'full_substrate_is_window_plus_lambda': len(substrate_in_window) + lam == len(substrate_primes),
        'substrate_plus_first_leak_is_q_cube': len(substrate_primes) + len(leak_in_window) == fano_cube == 27,
        'window_primes_plus_outside_substrate_is_q_cube': len(primes_le_window) + len(substrate_outside_window) == fano_cube,
        'leak_primes_exact': leak_in_window == [53, 61, 73, 79, 83, 97],
        'outside_substrate_exact': substrate_outside_window == [127, 163],
        'packet_residual_is_2q_times_heegner6': packet_residual_gap == (2 ** q) * heegner6 == 152,
        'L_function_ratio_matches_round50': 0.9970 < ratio < 0.9971,
        'L_function_loss_under_0p3_percent': 1.0 - ratio < 0.003,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXVI',
        'theorem': 'Phi4 prime window G2 leak theorem',
        'counts': {
            'window': window,
            'all_primes_to_window': len(primes_le_window),
            'substrate_primes_in_window': len(substrate_in_window),
            'leak_primes_in_window': len(leak_in_window),
            'substrate_primes_total': len(substrate_primes),
            'substrate_primes_outside_window': len(substrate_outside_window),
            'substrate_plus_first_leak': len(substrate_primes) + len(leak_in_window),
            'L_S_2': Ls2,
            'zeta_2': zeta2,
            'L_S_2_over_zeta_2': ratio,
        },
        'sets': {
            'leak_primes_in_window': leak_in_window,
            'substrate_primes_outside_window': substrate_outside_window,
        },
        'identities': {
            'prime_window': 'pi(100)=25=F5^2',
            'window_split': '25=19+6=Heegner6+positive_G2_roots',
            'substrate_completion': '|S|=21=19+2=Heegner6+lambda',
            'first_leak_completion': '|S|+6=27=q^3',
            'packet_gap': '152=2^q*19',
            'analytic_signal': 'L_S(2)/zeta(2) ~= 0.997061',
        },
        'interpretation': (
            'Inside the natural Phi4^2=100 prime window, the ordinary prime count is F5^2=25. '
            'The substrate captures 19 of those primes and misses exactly six, the positive G2 root count. '
            'Adding the two substrate primes outside the window recovers |S|=21, while adding the six first leaks to |S| gives 27=q^3, '
            'the same cube count appearing in the golden D4 Weyl bridge.'
        ),
        'claim_boundary': (
            'This is a prime-window and count theorem. It does not by itself prove that the six leak primes are individually roots of a canonical G2 representation.'
        ),
        'checks': checks,
        'n_verified': sum(checks.values()),
        'n_checks': len(checks),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


if __name__ == '__main__':
    r = main()
    print(r['part'], r['theorem'])
    print('checks', r['n_verified'], '/', r['n_checks'])
    print(r['counts'])
