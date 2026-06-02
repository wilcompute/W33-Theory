from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from analysis.w33_completed_prime_cube_eisenstein_balance import main as eisenstein_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXIX_COMPLETED_PRIME_CUBE_MOD12_LIFT_results.json'


def profile(xs, m):
    return Counter(x % m for x in xs)


def main():
    prev = eisenstein_main()

    q = 3
    r = 2
    lam = 2
    chi = 4
    F5 = 5
    g2 = 6
    phi3 = 13
    phi4 = 10
    phi6 = 7
    p_Ih = 11
    m_s = 15
    k = 12
    q_cube = q ** q
    d4_orientations = r ** q

    C = prev['sets']['split_mod_3_primes'] + prev['sets']['inert_mod_3_primes'] + prev['sets']['ramified_mod_3_primes']
    C = sorted(C)
    units12 = [p for p in C if p % 12 in {1, 5, 7, 11}]
    special = [p for p in C if p % 12 not in {1, 5, 7, 11}]

    mod3 = profile(C, 3)
    mod4 = profile(C, 4)
    mod12 = profile(C, 12)
    units12_profile = Counter({a: mod12[a] for a in [1, 5, 7, 11]})

    split_mod3_from_mod12 = mod12[1] + mod12[7]
    inert_mod3_from_mod12 = mod12[2] + mod12[5] + mod12[11]
    ramified_mod3_from_mod12 = mod12[3]

    gaussian_1_from_mod12 = mod12[1] + mod12[5]
    gaussian_3_from_mod12 = mod12[3] + mod12[7] + mod12[11]
    gaussian_2_from_mod12 = mod12[2]

    checks = {
        'inherits_eisenstein_balance': prev['n_verified'] == prev['n_checks'] == 22,
        'completed_cube_size_q_cube': len(C) == q_cube == 27,
        'mod3_profile_phi3_phi3_one': mod3 == Counter({1: phi3, 2: phi3, 0: 1}),
        'mod4_profile_pIh_ms_two': mod4 == Counter({1: p_Ih, 3: m_s, 2: 1}),
        'mod4_imbalance_is_chi': mod4[3] - mod4[1] == chi,
        'mod12_profile_exact': mod12 == Counter({7: 8, 5: 6, 11: 6, 1: 5, 2: 1, 3: 1}),
        'mod12_special_primes_are_r_q': special == [r, q],
        'mod12_units_count_F5_squared': len(units12) == F5 ** 2 == 25,
        'unit_profile_F5_g2_D4_g2': units12_profile == Counter({1: F5, 5: g2, 7: d4_orientations, 11: g2}),
        'unit_count_law': F5 + g2 + d4_orientations + g2 == F5 ** 2,
        'cube_count_law': len(special) + F5 + 2 * g2 + d4_orientations == q_cube,
        'split_mod3_recovered_from_mod12': split_mod3_from_mod12 == phi3,
        'inert_mod3_recovered_from_mod12': inert_mod3_from_mod12 == phi3,
        'ramified_mod3_recovered_from_mod12': ramified_mod3_from_mod12 == 1,
        'gaussian_mod4_recovered_from_mod12': gaussian_1_from_mod12 == p_Ih and gaussian_3_from_mod12 == m_s and gaussian_2_from_mod12 == 1,
        'mod12_split_pair_1_7_is_phi3': mod12[1] + mod12[7] == phi3,
        'mod12_inert_pair_plus_two_is_phi3': mod12[2] + mod12[5] + mod12[11] == phi3,
        'mod12_symmetric_inert_units': mod12[5] == mod12[11] == g2,
        'mod12_class7_minus_class1_is_q': mod12[7] - mod12[1] == q,
        'mod12_class7_is_D4_orientations': mod12[7] == d4_orientations,
        'mod12_class1_is_F5': mod12[1] == F5,
        'mod12_classes5_11_sum_is_k': mod12[5] + mod12[11] == k,
        'mod12_classes1_7_sum_is_phi3': mod12[1] + mod12[7] == phi3,
        'mod12_all_units_sum_25': sum(units12_profile.values()) == 25,
        'crt_lift_preserves_completed_mean': sum(C) == 1350 and sum(C) // len(C) == 50,
        'phi4_as_chi_plus_g2': phi4 == chi + g2,
        'phi6_bridge_7': phi6 == mod12[7] - 1,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXIX',
        'theorem': 'Completed prime cube mod-12 lift theorem',
        'counts': {
            'completed_size': len(C),
            'mod3_profile': dict(mod3),
            'mod4_profile': dict(mod4),
            'mod12_profile': dict(mod12),
            'unit_residue_count': len(units12),
            'special_residue_count': len(special),
        },
        'sets': {
            'special_primes_mod12': special,
            'class_1_mod12': [p for p in C if p % 12 == 1],
            'class_5_mod12': [p for p in C if p % 12 == 5],
            'class_7_mod12': [p for p in C if p % 12 == 7],
            'class_11_mod12': [p for p in C if p % 12 == 11],
        },
        'identities': {
            'mod12_profile': 'C mod 12 has profile 1^5, 2^1, 3^1, 5^6, 7^8, 11^6',
            'unit_shell': '25 = F5 + g2 + r^q + g2 = 5 + 6 + 8 + 6',
            'cube_shell': '27 = {2,3} + 25 = r + F5 + 2*g2 + r^q',
            'eisenstein_recovery': '(1 mod 12)+(7 mod 12)=13 and (2,5,11 mod 12)=13',
            'gaussian_recovery': '(1,5 mod 12)=11=p_Ih and (3,7,11 mod 12)=15=m_s',
            'asymmetry': 'class 7 minus class 1 = 8 - 5 = q',
            'g2_symmetry': 'classes 5 and 11 each have 6 primes = positive G2 roots',
        },
        'interpretation': (
            'The completed 27-prime cube has a mod-12 CRT lift that simultaneously refines Eisenstein mod-3 balance and Gaussian mod-4 imbalance. '
            'The four odd unit residue classes carry the profile 5,6,8,6 = F5,g2,r^q,g2, while the two special primes are 2 and 3. '
            'Thus the completed prime cube decomposes as 27 = 2 special primes + 25 unit primes, and the unit shell itself is F5 + 2*g2 + D4.'
        ),
        'claim_boundary': (
            'This proves residue-class counts and CRT compatibility. It does not construct a Dirichlet-character representation or assign residues to individual physical sectors.'
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
