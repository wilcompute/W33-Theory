#!/usr/bin/env python3
"""Executable control completion of the certified Reye Pauli normal form.

Prior geometry: data/w33_e7_d4_presymplectic_reye_normal_form.json.
Control assumptions: independently switchable signed continuous Pauli rotations.
This is an ideal three-qubit control model, not a physical Holonet implementation.
Lie rank and symmetry tests follow the standard framework of arXiv:1012.5256.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LETTERS = 'IXZY'
WORDS = tuple(''.join(x) for x in product(LETTERS, repeat=3))
BASE = tuple(''.join(x) for x in product('XYZ', 'IZ', 'IX'))
EXTRA = ('IXI', 'IIZ', 'IZI')
SINGLE = {'I': np.eye(2, dtype=complex),
          'X': np.array([[0, 1], [1, 0]], complex),
          'Z': np.diag([1, -1]).astype(complex),
          'Y': np.array([[0, -1j], [1j, 0]], complex)}


def matrix(w):
    return np.kron(np.kron(SINGLE[w[0]], SINGLE[w[1]]), SINGLE[w[2]])


MATS = {w: matrix(w) for w in WORDS}
EYE = MATS['III']


def anticommutes(a, b):
    return sum(x != y and x != 'I' and y != 'I' for x, y in zip(a, b)) % 2


def xor(a, b):
    return ''.join(LETTERS[LETTERS.index(x) ^ LETTERS.index(y)] for x, y in zip(a, b))


def closure(generators):
    """Exact Pauli support closure, retaining a topologically ordered proof DAG."""
    proof = {w: None for w in sorted(set(generators) - {'III'})}
    pending = list(proof)
    while pending:
        a = pending.pop(0)
        for b in tuple(proof):
            c = xor(a, b)
            if anticommutes(a, b) and c not in proof:
                proof[c] = (a, b)
                pending.append(c)
    return proof


def commutant(generators):
    # Pauli conjugation is diagonal on the full operator basis, so this spans
    # the entire complex commutant, not merely its Pauli-valued elements.
    return [w for w in WORDS if all(not anticommutes(w, g) for g in generators)]


def rotation(w, theta):
    return np.cos(theta) * EYE - 1j * np.sin(theta) * MATS[w]


def pulses(w, theta, proof):
    """Product-order pulse list implementing exp(-i theta P_w), no approximation."""
    parents = proof[w]
    if parents is None:
        return [(w, theta)]
    a, b = parents
    # R_a(pi/4) P_b R_a(-pi/4) = -i P_a P_b = sign P_w.
    conjugate = -1j * MATS[a] @ MATS[b]
    sign = 1 if np.array_equal(conjugate, MATS[w]) else -1
    assert np.array_equal(conjugate, sign * MATS[w])
    return (pulses(a, np.pi / 4, proof) + pulses(b, sign * theta, proof)
            + pulses(a, -np.pi / 4, proof))


def sector_pulses(role, s, t, theta):
    """SELROT: rotate qubit 1 only in sector (Z2=s, X3=t)."""
    if role not in 'XYZ' or len(role) != 1 or s not in (-1, 1) or t not in (-1, 1):
        raise ValueError('expected Pauli axis and two eigenvalue signs')
    return [(role+'II', theta/4), (role+'ZI', s*theta/4),
            (role+'IX', t*theta/4), (role+'ZX', s*t*theta/4)]


def audit():
    source = ROOT / 'data/w33_e7_d4_presymplectic_reye_normal_form.json'
    prior = json.loads(source.read_text())
    assert prior['status'] == 'PASS'
    assert set(prior['normal_form']['selected_words']) == set(BASE)
    # Independent dense Gaussian-integer matrix check of every support bracket.
    for a, b in combinations(WORDS, 2):
        bracket = MATS[a] @ MATS[b] - MATS[b] @ MATS[a]
        if anticommutes(a, b):
            c = xor(a, b)
            assert any(np.array_equal(bracket, s * 2j * MATS[c]) for s in (-1, 1))
        else:
            assert not np.any(bracket)

    stages = [closure(BASE + EXTRA[:i]) for i in range(4)]
    dimensions = list(map(len, stages))
    assert dimensions == [12, 20, 36, 63]
    assert commutant(BASE) == ['III', 'IIX', 'IZI', 'IZX']
    assert commutant(BASE + EXTRA[:2]) == ['III']
    J = MATS['YZX']
    assert np.array_equal(J.T, -J) and np.array_equal(J @ J, EYE)
    symplectic_basis = {w for w in WORDS if not np.any(MATS[w].T @ J + J @ MATS[w])}
    assert symplectic_basis == set(stages[2]) and len(symplectic_basis) == 36
    assert np.any(MATS['IZI'].T @ J + J @ MATS['IZI'])

    # Four exact rank-two central projectors; inverse Walsh transform supplies
    # independently addressable SU(2) operations within each sector.
    projectors = []
    for s, t in product((-1, 1), repeat=2):
        Q = (EYE + s * MATS['IZI']) @ (EYE + t * MATS['IIX']) / 4
        assert np.array_equal(Q @ Q, Q) and np.trace(Q) == 2
        for role in 'XYZ':
            expansion = (MATS[role+'II'] + s*MATS[role+'ZI']
                         + t*MATS[role+'IX'] + s*t*MATS[role+'ZX']) / 4
            assert np.array_equal(MATS[role+'II'] @ Q, expansion)
            theta = np.pi / 7
            target = EYE + (np.cos(theta)-1)*Q - 1j*np.sin(theta)*expansion
            actual = EYE.copy()
            for g, angle in sector_pulses(role, s, t, theta):
                actual = actual @ rotation(g, angle)
            assert np.max(np.abs(actual-target)) < 1e-14
        projectors.append(Q)
    assert np.array_equal(sum(projectors), EYE)
    assert all(not np.any(a @ b) for a, b in combinations(projectors, 2))

    # Exhaustive minimality relative to additional individual Pauli controls.
    outside = sorted(set(WORDS) - set(BASE) - {'III'})
    single_hist = Counter(len(closure(BASE + (w,))) for w in outside)
    pair_hist = Counter(len(closure(BASE + pair)) for pair in combinations(outside, 2))
    assert len(outside) == 51 and sum(pair_hist.values()) == 1275
    assert max(pair_hist) == 36 and max(single_hist) == 20

    # Concrete pulse compilation of EVERY nonidentity Pauli rotation.
    full = stages[3]
    pulse_counts = {}; max_error = 0.0
    for w in sorted(full):
        program = pulses(w, np.pi / 7, full)
        assert all(g in BASE + EXTRA for g, _ in program)
        U = EYE.copy()
        for g, angle in program:
            U = U @ rotation(g, angle)
        err = float(np.max(np.abs(U - rotation(w, np.pi / 7))))
        assert err < 1e-11
        max_error = max(max_error, err); pulse_counts[w] = len(program)

    # Second realization: Hadamard on the third qubit swaps X/Z and negates Y.
    # The induced signed permutation must preserve the complete bracket algebra.
    H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    U = np.kron(np.eye(4), H)
    mapping = {}
    for w in WORDS:
        transformed = U @ MATS[w] @ U.conj().T
        target = w[:2] + {'I':'I', 'X':'Z', 'Z':'X', 'Y':'Y'}[w[2]]
        sign = -1 if w[2] == 'Y' else 1
        assert np.max(np.abs(transformed - sign*MATS[target])) < 1e-14
        mapping[w] = target
    assert [len(closure(tuple(mapping[w] for w in BASE + EXTRA[:i])))
            for i in range(4)] == dimensions

    return {
        'schema': 'w33.reye-sector-control.v1', 'status': 'PASS',
        'prior_geometry': str(source.relative_to(ROOT)),
        'base_controls': list(BASE), 'additional_controls': list(EXTRA),
        'lie_dimensions': dimensions,
        'base_lie_algebra': 'su(2) direct-sum su(2) direct-sum su(2) direct-sum su(2)',
        'base_associative_algebra': 'M2(C) tensor C^4',
        'base_commutant_basis': commutant(BASE),
        'two_bridge_commutant_basis': commutant(BASE + EXTRA[:2]),
        'two_bridge_skew_form': 'YZX',
        'two_bridge_lie_algebra': 'compact sp(4) on C^8 (dimension 36)',
        'full_lie_algebra': 'su(8)',
        'single_extra_dimension_histogram': dict(sorted(single_hist.items())),
        'two_extra_dimension_histogram': dict(sorted(pair_hist.items())),
        'minimum_additional_individual_pauli_controls': 3,
        'proof_dag': {w: list(p) if p else None for w,p in full.items()},
        'sector_instruction': 'SELROT(axis, Z2_sign, X3_sign, angle): four commuting pulses',
        'sector_instruction_matrix_checks': 12,
        'compiled_rotation_count': len(pulse_counts),
        'compiled_pulse_counts': pulse_counts,
        'max_compilation_matrix_error': max_error,
        'second_realization': 'Hadamard conjugation on qubit 3 verified',
        'boundary': ('Ideal independently switchable signed continuous controls. '
                     'Three is minimal for additional individual Pauli Hamiltonians, '
                     'not for arbitrary linear-combination controls. No pulse-time '
                     'optimality, noise threshold, physical implementation, or scalable '
                     'universal machine is established.'),
        'references': ['https://arxiv.org/abs/1012.5256',
                       'https://arxiv.org/abs/quant-ph/0010100'],
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = audit()
    if args.write:
        Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'lie_dimensions',
        'two_extra_dimension_histogram', 'minimum_additional_individual_pauli_controls',
        'compiled_rotation_count', 'max_compilation_matrix_error')}, indent=2))
