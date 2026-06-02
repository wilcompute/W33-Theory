from __future__ import annotations

import json
from pathlib import Path

from analysis.w33_completed_prime_cube_dirichlet_energy import main as prior_main

OUT = Path(__file__).resolve().parents[1] / 'data' / 'PART_MMCCCLXXXI_PRIME_CUBE_UNIT_PARSEVAL_results.json'
UNITS = [1, 5, 7, 11]
CH = {
    'principal': {1: 1, 5: 1, 7: 1, 11: 1},
    'chi4': {1: 1, 5: 1, 7: -1, 11: -1},
    'chi3': {1: 1, 5: -1, 7: 1, 11: -1},
    'chi12': {1: 1, 5: -1, 7: -1, 11: 1},
}


def mom(prof):
    return {name: sum(vals[a] * prof.get(a, 0) for a in UNITS) for name, vals in CH.items()}


def echi(m):
    return m['chi4']**2 + m['chi3']**2 + m['chi12']**2


def eprof(prof):
    n = sum(prof.values())
    return 4 * sum(x*x for x in prof.values()) - n*n


def inv(m):
    a, b, c, d = m['principal'], m['chi4'], m['chi3'], m['chi12']
    return {1:(a+b+c+d)//4, 5:(a+b-c-d)//4, 7:(a-b+c-d)//4, 11:(a-b-c+d)//4}


def main():
    prev = prior_main()
    r, k, chi, heegner6, dim_f4, q4_edges = 2, 12, 4, 19, 52, 32
    d4 = r**3
    profs = {
        'completed': {1:5, 5:6, 7:8, 11:6},
        'substrate': {1:2, 5:5, 7:7, 11:5},
        'first_leak': {1:3, 5:1, 7:1, 11:1},
        'transition_substrate': {1:0, 5:1, 7:1, 11:2},
        'transition_all': {1:3, 5:2, 7:2, 11:3},
    }
    M = {x: mom(y) for x, y in profs.items()}
    E = {x: echi(y) for x, y in M.items()}
    P = {x: eprof(y) for x, y in profs.items()}
    Q = {x: sum(v*v for v in y.values()) for x, y in profs.items()}

    checks = {
        'inherits_previous': prev['n_verified'] == prev['n_checks'] == 24,
        'moments_completed': M['completed'] == prev['moments']['completed_units'],
        'moments_substrate': M['substrate'] == prev['moments']['substrate_units'],
        'moments_leak': M['first_leak'] == prev['moments']['first_leak_units'],
        'parseval_all': all(E[x] == P[x] for x in profs),
        'completed_energy_19': E['completed'] == heegner6 == 19,
        'completed_pair_square_sum_161': Q['completed'] == 161,
        'completed_formula': 4*Q['completed'] - 25*25 == 19,
        'packet_residual': E['completed'] * d4 == 152,
        'substrate_energy_51': E['substrate'] == dim_f4 - 1 == 51,
        'substrate_pair_square_sum_103': Q['substrate'] == 103,
        'leak_energy_k': E['first_leak'] == k == 12,
        'transition_substrate_energy_d4': E['transition_substrate'] == d4 == 8,
        'transition_all_energy_chi': E['transition_all'] == chi == 4,
        'drop_is_q4_edges': E['substrate'] - E['completed'] == q4_edges,
        'inverse_completed': inv(M['completed']) == profs['completed'],
        'inverse_substrate': inv(M['substrate']) == profs['substrate'],
        'inverse_leak': inv(M['first_leak']) == profs['first_leak'],
        'hadamard_norm_completed': sum(v*v for v in M['completed'].values()) == 4*Q['completed'] == 644,
        'hadamard_norm_substrate': sum(v*v for v in M['substrate'].values()) == 4*Q['substrate'] == 412,
        'completed_energy_norm_minus_main': sum(v*v for v in M['completed'].values()) - M['completed']['principal']**2 == 19,
    }
    assert all(checks.values()), checks
    out = {
        'part': 'MMCCCLXXXI',
        'theorem': 'Prime cube unit Parseval theorem',
        'profiles': profs,
        'moments': M,
        'unit_square_sums': Q,
        'energies': E,
        'identities': {
            'parseval': 'E = chi4^2+chi3^2+chi12^2 = 4*sum(n_a^2)-N^2',
            'completed': '4*(5^2+6^2+8^2+6^2)-25^2 = 19',
            'residual': '19*8=152',
            'substrate': '4*(2^2+5^2+7^2+5^2)-19^2 = 51',
            'leak': '4*(3^2+1^2+1^2+1^2)-6^2 = 12',
            'drop': '51-19=32'
        },
        'claim_boundary': 'Finite unit-residue Parseval identity only; not an analytic prime-distribution theorem.',
        'checks': checks,
        'n_verified': sum(checks.values()),
        'n_checks': len(checks),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    return out

if __name__ == '__main__':
    r = main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['energies'])
