from __future__ import annotations

import json
from pathlib import Path

from analysis.w33_prime_cube_unit_parseval import main as parseval_main

OUT = Path(__file__).resolve().parents[1] / 'data' / 'PART_MMCCCLXXXII_PRIME_CUBE_UNIT_CONVOLUTION_results.json'
UNITS = [1, 5, 7, 11]
CH = {
    'principal': {1: 1, 5: 1, 7: 1, 11: 1},
    'chi4': {1: 1, 5: 1, 7: -1, 11: -1},
    'chi3': {1: 1, 5: -1, 7: 1, 11: -1},
    'chi12': {1: 1, 5: -1, 7: -1, 11: 1},
}


def convolve(a, b):
    out = {u: 0 for u in UNITS}
    for x, nx in a.items():
        for y, ny in b.items():
            out[(x * y) % 12] += nx * ny
    return out


def moments(prof):
    return {name: sum(vals[u] * prof.get(u, 0) for u in UNITS) for name, vals in CH.items()}


def inv_from_moments(m):
    a, b, c, d = m['principal'], m['chi4'], m['chi3'], m['chi12']
    return {1:(a+b+c+d)//4, 5:(a+b-c-d)//4, 7:(a-b+c-d)//4, 11:(a-b-c+d)//4}


def main():
    prev = parseval_main()
    q, k, phi3, heegner6, d4, x_min, residual = 3, 12, 13, 19, 8, 160, 152
    profiles = prev['profiles']
    completed = profiles['completed']
    substrate = profiles['substrate']
    leak = profiles['first_leak']
    transition = profiles['transition_all']

    conv_completed = convolve(completed, completed)
    conv_substrate = convolve(substrate, substrate)
    conv_leak = convolve(leak, leak)
    conv_transition = convolve(transition, transition)
    cross_sl = {u: conv_completed[u] - conv_substrate[u] - conv_leak[u] for u in UNITS}

    M_completed = moments(completed)
    M_conv_completed = moments(conv_completed)
    M_substrate = moments(substrate)
    M_conv_substrate = moments(conv_substrate)
    M_leak = moments(leak)
    M_conv_leak = moments(conv_leak)

    checks = {
        'inherits_parseval': prev['n_verified'] == prev['n_checks'] == 21,
        'completed_convolution_profile': conv_completed == {1:161, 5:156, 7:152, 11:156},
        'completed_product_sum_25_squared': sum(conv_completed.values()) == 25**2 == 625,
        'identity_class_is_min_x_plus_one': conv_completed[1] == x_min + 1 == 161,
        'class_7_is_packet_residual': conv_completed[7] == residual == heegner6 * d4 == 152,
        'classes_5_11_are_k_phi3': conv_completed[5] == conv_completed[11] == k * phi3 == 156,
        'identity_minus_class7_is_q_squared': conv_completed[1] - conv_completed[7] == q**2 == 9,
        'fourier_square_completed': M_conv_completed == {name: M_completed[name] ** 2 for name in M_completed},
        'hadamard_inverse_completed_convolution': inv_from_moments(M_conv_completed) == conv_completed,
        'substrate_convolution_profile': conv_substrate == {1:103, 5:90, 7:78, 11:90},
        'substrate_fourier_square': M_conv_substrate == {name: M_substrate[name] ** 2 for name in M_substrate},
        'leak_convolution_profile': conv_leak == {1:12, 5:8, 7:8, 11:8},
        'leak_identity_is_k': conv_leak[1] == k == 12,
        'leak_nonidentity_are_d4': conv_leak[5] == conv_leak[7] == conv_leak[11] == d4 == 8,
        'leak_fourier_square': M_conv_leak == {name: M_leak[name] ** 2 for name in M_leak},
        'transition_convolution_profile': conv_transition == {1:26, 5:24, 7:24, 11:26},
        'transition_opposite_classes_26_24': conv_transition[1] == conv_transition[11] == 26 and conv_transition[5] == conv_transition[7] == 24,
        'cross_substrate_leak_profile': cross_sl == {1:46, 5:58, 7:66, 11:58},
        'cross_even_profile': all(v % 2 == 0 for v in cross_sl.values()),
        'cross_unordered_half': {u: cross_sl[u]//2 for u in UNITS} == {1:23, 5:29, 7:33, 11:29},
        'completed_profile_symmetric_5_11': conv_completed[5] == conv_completed[11],
        'completed_nonidentity_sum': conv_completed[5] + conv_completed[7] + conv_completed[11] == 464,
        'completed_identity_plus_residual': conv_completed[1] + conv_completed[7] == 313,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXXII',
        'theorem': 'Prime cube unit convolution theorem',
        'profiles': {
            'completed': completed,
            'completed_convolution': conv_completed,
            'substrate_convolution': conv_substrate,
            'first_leak_convolution': conv_leak,
            'transition_convolution': conv_transition,
            'substrate_leak_cross_terms': cross_sl,
        },
        'moments': {
            'completed': M_completed,
            'completed_convolution': M_conv_completed,
        },
        'identities': {
            'completed_product': '(5,6,8,6)*(5,6,8,6) = (161,156,152,156)',
            'identity_class': '161 = 160 + 1 = X_min_supports + 1',
            'side_classes': '156 = 12*13 = k*Phi3 for both 5 and 11 classes',
            'class_7': '152 = 19*8 = Heegner6*D4 = packet residual gap',
            'gap': '161 - 152 = 9 = q^2',
            'leak_product': '(3,1,1,1)^2 = (12,8,8,8) = (k,D4,D4,D4)',
            'fourier_rule': 'Hadamard moments of a convolution are pointwise squares of Hadamard moments',
        },
        'interpretation': 'The completed prime cube unit shell has a multiplicative residue convolution whose four classes recover X_min+1, two k*Phi3 shells, and the packet residual 152.  This is the finite group-algebra upgrade of the Parseval theorem: the same Hadamard transform that produced character energy now diagonalizes the ordered unit-product table.',
        'claim_boundary': 'This is a finite convolution theorem in the unit group modulo 12.  It is not a proof of multiplicative closure of the prime set itself.',
        'checks': checks,
        'n_verified': sum(checks.values()),
        'n_checks': len(checks),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result

if __name__ == '__main__':
    r = main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['profiles']['completed_convolution'])
