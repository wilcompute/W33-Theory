from __future__ import annotations

import json
from pathlib import Path

from analysis.w33_phi4_prime_window_g2_leak import main as leak_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXVII_COMPLETED_PRIME_CUBE_MEAN_results.json'


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


def factor(n: int) -> dict[int, int]:
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def main():
    prev = leak_main()

    q = 3
    lam = 2
    chi = 4
    g2_pos = 6
    g_neg = 15
    phi4 = 10
    phi6 = 7
    F5 = 5
    E1 = 10
    v = 40
    heegner6 = 19
    q_cube = q ** q
    dense_limit = 47
    window = phi4 ** 2

    substrate_primes = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
        37, 41, 43, 47, 59, 67, 71, 89, 127, 163,
    }

    dense_shell = [p for p in range(2, dense_limit + 1) if is_prime(p)]
    transition_shell = [p for p in range(dense_limit + 1, window + 1) if is_prime(p)]
    window_primes = dense_shell + transition_shell
    transition_substrate = [p for p in transition_shell if p in substrate_primes]
    transition_leak = [p for p in transition_shell if p not in substrate_primes]
    outside_substrate = sorted(p for p in substrate_primes if p > window)
    completed_cube = sorted(set(window_primes) | set(outside_substrate))
    substrate_plus_leak = sorted(substrate_primes | set(transition_leak))

    completed_sum = sum(completed_cube)
    mean_completed = completed_sum // len(completed_cube)
    dense_sum = sum(dense_shell)
    transition_sum = sum(transition_shell)
    outside_sum = sum(outside_substrate)

    checks = {
        'inherits_phi4_prime_window_g2_leak': prev['n_verified'] == prev['n_checks'] == 15,
        'dense_shell_count_gneg': len(dense_shell) == g_neg == 15,
        'transition_shell_count_phi4': len(transition_shell) == phi4 == 10,
        'transition_split_chi_plus_g2': len(transition_substrate) == chi and len(transition_leak) == g2_pos and chi + g2_pos == phi4,
        'window_prime_count_F5_squared': len(window_primes) == F5 ** 2 == 25,
        'window_substrate_count_heegner6': len([p for p in window_primes if p in substrate_primes]) == heegner6 == 19,
        'outside_substrate_count_lambda': len(outside_substrate) == lam == 2,
        'completed_cube_size_q_cube': len(completed_cube) == q_cube == 27,
        'completed_cube_equals_substrate_plus_transition_leak': completed_cube == substrate_plus_leak,
        'q_cube_decomposition_gneg_phi4_lambda': g_neg + phi4 + lam == q_cube,
        'q_cube_decomposition_so7_plus_g2': len(substrate_primes) + len(transition_leak) == q_cube,
        'completed_sum_1350': completed_sum == 1350,
        'completed_mean_E1_F5': mean_completed == E1 * F5 == 50,
        'completed_mean_v_plus_E1': mean_completed == v + E1,
        'completed_sum_factorization': factor(completed_sum) == {2: 1, 3: 3, 5: 2},
        'completed_sum_qcube_E1_F5': completed_sum == q_cube * E1 * F5,
        'completed_sum_lambda_qcube_F5_squared': completed_sum == lam * q_cube * F5 ** 2,
        'shell_sums_decompose_completed_sum': dense_sum + transition_sum + outside_sum == completed_sum,
        'transition_sum_k_times_61': transition_sum == 12 * 61,
        'dense_sum_8_times_41': dense_sum == 8 * 41,
        'outside_sum_127_plus_163': outside_sum == 127 + 163 == 290,
        'transition_leaks_exact': transition_leak == [53, 61, 73, 79, 83, 97],
        'transition_substrate_exact': transition_substrate == [59, 67, 71, 89],
        'outside_substrate_exact': outside_substrate == [127, 163],
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXVII',
        'theorem': 'Completed prime cube mean theorem',
        'counts': {
            'dense_shell_primes_to_47': len(dense_shell),
            'transition_shell_primes_48_to_100': len(transition_shell),
            'transition_substrate': len(transition_substrate),
            'transition_leak': len(transition_leak),
            'outside_substrate': len(outside_substrate),
            'completed_cube_size': len(completed_cube),
            'completed_cube_sum': completed_sum,
            'completed_cube_mean': mean_completed,
        },
        'sets': {
            'dense_shell': dense_shell,
            'transition_substrate': transition_substrate,
            'transition_leak': transition_leak,
            'outside_substrate': outside_substrate,
            'completed_cube': completed_cube,
        },
        'identities': {
            'count_decomposition': '27 = 15 + 10 + 2 = g_neg + Phi4 + lambda',
            'transition_split': '10 = 4 + 6 = chi + positive_G2_roots',
            'substrate_plus_leak': '27 = |S| + 6 = 21 + positive_G2_roots',
            'mean_law': 'sum(C)=1350 and |C|=27, so mean(C)=50=E1*F5=v+E1',
            'sum_factorization': '1350 = 2*3^3*5^2 = lambda*q^q*F5^2',
            'shell_sums': '328 + 732 + 290 = 1350',
        },
        'interpretation': (
            'The Phi4^2 prime window has a three-shell decomposition.  The dense shell p<=47 has 15 primes; '
            'the transition shell 48..100 has 10 primes, splitting as 4 substrate primes plus 6 first leaks; '
            'the two substrate primes outside the window complete the count to 27=q^3.  The completed 27-prime cube has exact arithmetic mean 50=E1*F5=v+E1.'
        ),
        'claim_boundary': (
            'This proves a finite prime-window cube and mean law.  It does not make the completed set into a field or prove a multiplicative group law on the 27 primes.'
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
