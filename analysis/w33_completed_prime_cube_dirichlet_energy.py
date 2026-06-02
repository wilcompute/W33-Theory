from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from analysis.w33_completed_prime_cube_mod12_lift import main as mod12_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXX_COMPLETED_PRIME_CUBE_DIRICHLET_ENERGY_results.json'

UNIT_CLASSES = [1, 5, 7, 11]
CHARACTERS = {
    'principal': {1: 1, 5: 1, 7: 1, 11: 1},
    'chi4': {1: 1, 5: 1, 7: -1, 11: -1},
    'chi3': {1: 1, 5: -1, 7: 1, 11: -1},
    'chi12': {1: 1, 5: -1, 7: -1, 11: 1},
}


def profile_mod12(xs):
    return Counter(p % 12 for p in xs if p % 12 in UNIT_CLASSES)


def moments(xs):
    prof = profile_mod12(xs)
    return {name: sum(vals[a] * prof[a] for a in UNIT_CLASSES) for name, vals in CHARACTERS.items()}


def nontrivial_energy(m):
    return m['chi4'] ** 2 + m['chi3'] ** 2 + m['chi12'] ** 2


def dot_nontrivial(a, b):
    return a['chi4'] * b['chi4'] + a['chi3'] * b['chi3'] + a['chi12'] * b['chi12']


def invert_moments(m):
    M0, M4, M3, M12 = m['principal'], m['chi4'], m['chi3'], m['chi12']
    return {
        1: (M0 + M4 + M3 + M12) // 4,
        5: (M0 + M4 - M3 - M12) // 4,
        7: (M0 - M4 + M3 - M12) // 4,
        11: (M0 - M4 - M3 + M12) // 4,
    }


def main():
    prev = mod12_main()

    q = 3
    r = 2
    chi = 4
    k = 12
    phi3 = 13
    heegner6 = 19
    dim_f4 = 52
    q4_edges = 32
    packet_residual_gap = 152
    d4 = r ** q

    completed = sorted(
        prev['sets']['class_1_mod12'] +
        prev['sets']['class_5_mod12'] +
        prev['sets']['class_7_mod12'] +
        prev['sets']['class_11_mod12'] +
        prev['sets']['special_primes_mod12']
    )
    first_leak = [53, 61, 73, 79, 83, 97]
    transition_substrate = [59, 67, 71, 89]
    transition_all = sorted(first_leak + transition_substrate)
    substrate = sorted(set(completed) - set(first_leak))

    M_completed = moments(completed)
    M_substrate = moments(substrate)
    M_leak = moments(first_leak)
    M_transition_substrate = moments(transition_substrate)
    M_transition = moments(transition_all)

    E_completed = nontrivial_energy(M_completed)
    E_substrate = nontrivial_energy(M_substrate)
    E_leak = nontrivial_energy(M_leak)
    E_transition_substrate = nontrivial_energy(M_transition_substrate)
    E_transition = nontrivial_energy(M_transition)
    cross_transition = dot_nontrivial(M_transition_substrate, M_leak)

    checks = {
        'inherits_mod12_lift': prev['n_verified'] == prev['n_checks'] == 27,
        'completed_unit_count_25': M_completed['principal'] == 25,
        'completed_character_moments': M_completed == {'principal': 25, 'chi4': -3, 'chi3': 1, 'chi12': -3},
        'completed_energy_heegner6': E_completed == heegner6 == 19,
        'completed_energy_packet_residual_over_D4': E_completed * d4 == packet_residual_gap == 152,
        'completed_hadamard_inversion': invert_moments(M_completed) == {1: 5, 5: 6, 7: 8, 11: 6},
        'substrate_unit_count_19': M_substrate['principal'] == 19,
        'substrate_character_moments': M_substrate == {'principal': 19, 'chi4': -5, 'chi3': -1, 'chi12': -5},
        'substrate_energy_F4_minus_one': E_substrate == dim_f4 - 1 == 51,
        'leak_unit_count_positive_g2': M_leak['principal'] == 6,
        'leak_character_moments_all_two': M_leak == {'principal': 6, 'chi4': 2, 'chi3': 2, 'chi12': 2},
        'leak_energy_k': E_leak == k == 12,
        'substrate_plus_leak_moments_completed': {name: M_substrate[name] + M_leak[name] for name in CHARACTERS} == M_completed,
        'anisotropy_reduction_is_Q4_edges': E_substrate - E_completed == q4_edges,
        'transition_substrate_moments': M_transition_substrate == {'principal': 4, 'chi4': -2, 'chi3': -2, 'chi12': 0},
        'transition_substrate_energy_D4': E_transition_substrate == d4 == 8,
        'transition_all_moments': M_transition == {'principal': 10, 'chi4': 0, 'chi3': 0, 'chi12': 2},
        'transition_energy_chi': E_transition == chi == 4,
        'transition_cross_term_minus_D4': cross_transition == -d4,
        'transition_energy_by_cross_formula': E_transition == E_transition_substrate + E_leak + 2 * cross_transition,
        'transition_hadamard_inversion': invert_moments(M_transition) == {1: 3, 5: 2, 7: 2, 11: 3},
        'leak_hadamard_inversion': invert_moments(M_leak) == {1: 3, 5: 1, 7: 1, 11: 1},
        'unit_shell_balance_phi3': prev['counts']['mod12_profile'][1] + prev['counts']['mod12_profile'][7] == phi3,
        'q_cube_mean_preserved': sum(completed) == 1350 and len(completed) == q ** q,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXX',
        'theorem': 'Completed prime cube Dirichlet energy theorem',
        'moments': {
            'completed_units': M_completed,
            'substrate_units': M_substrate,
            'first_leak_units': M_leak,
            'transition_substrate': M_transition_substrate,
            'transition_all': M_transition,
        },
        'energies': {
            'completed_nontrivial_character_energy': E_completed,
            'substrate_nontrivial_character_energy': E_substrate,
            'first_leak_nontrivial_character_energy': E_leak,
            'transition_substrate_energy': E_transition_substrate,
            'transition_all_energy': E_transition,
            'transition_cross_term': cross_transition,
        },
        'identities': {
            'completed_character_vector': '(25,-3,1,-3) over (1,chi4,chi3,chi12)',
            'heegner_energy': '(-3)^2 + 1^2 + (-3)^2 = 19 = Heegner6',
            'packet_residual': '19*8 = 152 = packet residual gap',
            'substrate_energy': '(-5)^2 + (-1)^2 + (-5)^2 = 51 = dim(F4)-1',
            'leak_energy': '2^2 + 2^2 + 2^2 = 12 = k',
            'anisotropy_reduction': '51 - 19 = 32 = |E(Q4)|',
            'transition_cancellation': '8 + 12 + 2*(-8) = 4 = chi',
        },
        'interpretation': (
            'The mod-12 completed prime cube has a genuine Dirichlet-character shadow.  Its unit-shell character vector is (25,-3,1,-3), '
            'and the squared nontrivial character energy is exactly 19, the Heegner-6 prime and the packet residual gap divided by the D4 orientation count. '
            'The substrate alone has energy 51=dim(F4)-1; adding the six-prime G2 leak reduces this anisotropy by 32, the Q4 edge count, down to 19.'
        ),
        'claim_boundary': (
            'This constructs character moments and energies for the finite completed prime cube. It is not yet an analytic Dirichlet L-function theorem.'
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
    print(r['moments'])
    print(r['energies'])
