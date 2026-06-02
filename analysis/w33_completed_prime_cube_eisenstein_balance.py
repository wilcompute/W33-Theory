from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from analysis.w33_completed_prime_cube_mean import main as cube_mean_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXVIII_COMPLETED_PRIME_CUBE_EISENSTEIN_BALANCE_results.json'


def main():
    prev = cube_mean_main()

    q = 3
    lam = 2
    phi3 = 13
    phi4 = 10
    phi6 = 7
    F5 = 5
    g_neg = 15
    g2_pos = 6
    q_cube = q ** q

    substrate = sorted({
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
        37, 41, 43, 47, 59, 67, 71, 89, 127, 163,
    })
    completed = prev['sets']['completed_cube']
    dense = prev['sets']['dense_shell']
    transition_substrate = prev['sets']['transition_substrate']
    transition_leak = prev['sets']['transition_leak']
    outside_substrate = prev['sets']['outside_substrate']
    transition = sorted(transition_substrate + transition_leak)

    def residue_profile(xs):
        return Counter(x % q for x in xs)

    def split(xs):
        return [x for x in xs if x % q == 1]

    def inert(xs):
        return [x for x in xs if x % q == 2]

    def ramified(xs):
        return [x for x in xs if x % q == 0]

    completed_split = split(completed)
    completed_inert = inert(completed)
    completed_ramified = ramified(completed)

    substrate_profile = residue_profile(substrate)
    leak_profile = residue_profile(transition_leak)
    transition_profile = residue_profile(transition)
    dense_profile = residue_profile(dense)
    outside_profile = residue_profile(outside_substrate)
    completed_profile = residue_profile(completed)

    checks = {
        'inherits_completed_prime_cube_mean': prev['n_verified'] == prev['n_checks'] == 24,
        'completed_size_q_cube': len(completed) == q_cube == 27,
        'completed_eisenstein_split_phi3_phi3_one': completed_profile == Counter({1: phi3, 2: phi3, 0: 1}),
        'completed_split_count_phi3': len(completed_split) == phi3,
        'completed_inert_count_phi3': len(completed_inert) == phi3,
        'completed_ramified_is_q': completed_ramified == [q],
        'q_cube_equals_two_phi3_plus_one': q_cube == 2 * phi3 + 1,
        'substrate_profile_has_lambda_inert_excess': substrate_profile == Counter({2: 11, 1: 9, 0: 1}) and substrate_profile[2] - substrate_profile[1] == lam,
        'first_leak_profile_has_lambda_split_excess': leak_profile == Counter({1: 4, 2: 2}) and leak_profile[1] - leak_profile[2] == lam,
        'leak_corrects_substrate_eisenstein_imbalance': substrate_profile[1] + leak_profile[1] == substrate_profile[2] + leak_profile[2] == phi3,
        'transition_shell_eisenstein_balanced': transition_profile == Counter({1: 5, 2: 5}),
        'transition_count_phi4': len(transition) == phi4 == 10,
        'dense_shell_profile': dense_profile == Counter({2: 8, 1: 6, 0: 1}),
        'outside_substrate_two_split_primes': outside_profile == Counter({1: 2}),
        'dense_plus_outside_compensates_to_phi3': dense_profile[1] + outside_profile[1] == dense_profile[2] + outside_profile[2] == 8,
        'transition_leak_count_positive_g2_roots': len(transition_leak) == g2_pos == 6,
        'leak_split_plus_inert_equals_positive_g2_roots': leak_profile[1] + leak_profile[2] == g2_pos,
        'leak_split_inert_vector_4_2': (leak_profile[1], leak_profile[2]) == (4, 2),
        'substrate_plus_leak_is_completed': sorted(set(substrate) | set(transition_leak)) == completed,
        'completed_sum_mean_inherited': sum(completed) == 1350 and sum(completed) // len(completed) == 50,
        'dense_count_gneg': len(dense) == g_neg,
        'split_inert_product_phi3_squared': len(completed_split) * len(completed_inert) == phi3 ** 2,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXVIII',
        'theorem': 'Completed prime cube Eisenstein balance theorem',
        'counts': {
            'completed_size': len(completed),
            'split_mod_3': len(completed_split),
            'inert_mod_3': len(completed_inert),
            'ramified_mod_3': len(completed_ramified),
            'substrate_profile': dict(substrate_profile),
            'first_leak_profile': dict(leak_profile),
            'transition_profile': dict(transition_profile),
        },
        'sets': {
            'split_mod_3_primes': completed_split,
            'inert_mod_3_primes': completed_inert,
            'ramified_mod_3_primes': completed_ramified,
            'first_leak_split_primes': split(transition_leak),
            'first_leak_inert_primes': inert(transition_leak),
        },
        'identities': {
            'cube_balance': '27 = 13 split + 13 inert + 1 ramified = 2*Phi3 + 1',
            'substrate_imbalance': 'S has 9 split and 11 inert primes below Eisenstein residue classes: inert excess = lambda',
            'leak_correction': 'first leak has 4 split and 2 inert primes: split excess = lambda',
            'completed_balance': '(9+4) split = (11+2) inert = 13 = Phi3',
            'transition_balance': '48<p<=100 has 5 split and 5 inert primes',
            'G2_leak': 'six first leaks carry the positive G2-root count and repair Eisenstein balance',
        },
        'interpretation': (
            'The completed 27-prime cube is exactly balanced in Eisenstein residue classes: 13 primes are 1 mod 3, '
            '13 are 2 mod 3, and 3 is the single ramified prime.  The substrate alone is imbalanced by lambda=2 toward inert primes; '
            'the six-prime first leak shell is imbalanced by lambda=2 toward split primes, and exactly repairs the imbalance.  '
            'Thus the positive-G2-root leakage shell is also the Eisenstein-balance correction that upgrades |S|=21 to q^3=27.'
        ),
        'claim_boundary': (
            'This proves residue-class balance in the Eisenstein prime split/inert sense. It does not assign the six leak primes to individual G2 roots.'
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
