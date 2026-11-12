"""Exact superpotential stabilizer and anomalous theta identifications."""

from itertools import permutations
import json

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

import toe_20261109_canonical_sm_flatness as flat


OUT = 'data/toe_20261112_theta_rephasing.json'
CANONICAL = 'data/toe_20261109_canonical_sm_flatness.json'
THETA = 'data/toe_20261112_parent_theta_lattice.json'


def spectator_probe(matrix):
    """Coefficient of S[0,1,2]^2 in the canonical epsilon contraction."""
    epsilon = [(word, flat.vacuum.cubic.parity(word)) for word in permutations(range(3))]
    target = [0, 1, 2]
    return sum(
        sign * other_sign * int(matrix[p, k]) * int(matrix[q, n])
        for (i, j, k), sign in epsilon
        for (l, m, n), other_sign in epsilon
        for p, q in np.ndindex(3, 3)
        if sorted((i, l, p)) == sorted((j, m, q)) == target
    )


def stabilizer_witness(repair):
    mixed = sp.zeros(2, 3)
    for j, k in repair['allowed_mixed_cubic_indices_zero_based']:
        mixed[j, k] = 1
    centers = {tuple(row['meson_trace']): row['center']
               for row in repair['centered_trace_squared_terms']}
    x, z = flat.repair_vevs()
    mesons = flat.family_mesons(x, z)
    for word, center in centers.items():
        matrix = sp.eye(3)
        for label in word:
            matrix *= sp.Matrix(mesons[label])
        assert sp.trace(matrix) == center
    linear = -sp.Matrix(2, 3, [centers.get((label,), 0) for label in range(6)])
    species_basis = sp.Matrix([[0, 1, 1], [0, 1, -1], [1, 0, 0]])
    assert mixed * species_basis == sp.Matrix([[1, 0, 0], [0, 2, 0]])
    assert sorted((mixed.T * mixed).eigenvals()) == [0, 1, 2]
    assert linear * species_basis == sp.Matrix([[0, -2, 0], [-2, 0, 0]])

    field = (x[0] + x[1])
    zero = np.zeros_like(field)
    neutral = flat.family_mesons([field, field, zero], [field, zero])
    odd = flat.family_mesons([field, -field, field], [field, zero])
    assert repair['sextic_spectator_mass']['meson_index_pairs'] == [[0, 0], [0, 2], [3, 4]]
    assert np.array_equal(neutral[0], np.diag([1, 1, 0]))
    assert np.array_equal(odd[0], odd[2])
    assert not neutral[2].any() and not any(matrix.any() for matrix in odd[3:])
    coefficient = spectator_probe(neutral[0])
    assert coefficient == -2 and coefficient == spectator_probe(odd[0])
    # In the odd probe rescale X2 by t. The spectator polynomial is c(1+t).
    # Its constant and linear terms carry species phases -6x and -3x.
    return dict(mixed_singular_values_squared=[2, 1, 0],
                centered_bilinear_matrix=[list(map(int, row)) for row in linear.tolist()],
                spectator_neutral_coefficient=coefficient,
                spectator_mixed_coefficient=coefficient)


def calculate():
    repair = flat.read(CANONICAL)['repair']
    parent = flat.read(THETA)
    witness = stabilizer_witness(repair)
    names = ['A5', 'A6', 'Omega', 'Z0AX2', 'Z1AX0', 'Z1AX1', 'TrM00', 'SS_M00_M00']
    # Scalar phases (X0, X1, X2, Z0, Z1, A, S) and superspace phase.
    rows = sp.Matrix([
        [0, 0, 0, 0, 0, 5, 0, -2],
        [0, 0, 0, 0, 0, 6, 0, -2],
        [1, 1, 1, 0, 0, 0, 0, -2],
        [0, 0, 1, 1, 0, 1, 0, -2],
        [1, 0, 0, 0, 1, 1, 0, -2],
        [0, 1, 0, 0, 1, 1, 0, -2],
        [1, 0, 0, 1, 0, 0, 0, -2],
        [2, 0, 0, 2, 0, 0, 2, -2],
    ])
    smith = [abs(int(d)) for d in smith_normal_form(rows, domain=sp.ZZ).diagonal()]
    assert smith == [1, 1, 1, 1, 1, 1, 2, 6]
    indices = [sp.Matrix(1, 2, entry['basic_trace_indices'])
               for entry in parent['spin_witness']['representations'].values()]
    bifundamental, adjoint, family_adjoint, spectator = indices
    chiral = [bifundamental] * 5 + [adjoint, spectator]
    r_anomaly = adjoint + family_adjoint - sum(chiral, sp.zeros(1, 2))
    gauge = sp.Matrix.vstack(*chiral, r_anomaly).T
    geometric = sp.Matrix(parent['theta_period_generators_in_2pi_units']).T
    character_anomaly = geometric.inv() * gauge
    assert character_anomaly.tolist() == [
        [18, 18, 18, 18, 18, 24, 0, -90],
        [3, 3, 3, 3, 3, -8, 5, -18],
    ]
    center = sp.Matrix([1, 1, 1, -1, -1, 0, 0, 0]) / 3
    spectator_sign = sp.eye(8)[:, 6] / 2
    parity = sp.eye(8)[:, 7] / 2
    for phase in (center, spectator_sign, parity):
        assert all(entry.is_integer for entry in rows * phase)
    assert all(entry.is_integer for entry in character_anomaly * center)
    assert all(entry.is_integer for entry in character_anomaly * parity)
    assert (character_anomaly * spectator_sign).applyfunc(lambda phase: phase % 1) == (
        sp.Matrix([0, sp.Rational(1, 2)])
    )
    invariants = sp.diag(1, 2) * character_anomaly * rows.inv()
    assert all(entry.is_integer for entry in invariants)
    assert any(not entry.is_integer for entry in (character_anomaly * rows.inv())[1, :])
    # The paired cocharacter on S² x S² with c1=x+y has half the
    # Chern–Weil charges of the c1=x+2y witness.
    flux_charges = sp.Matrix(parent['spin_witness']['witness_instanton_numbers']) / 2
    assert flux_charges == sp.Matrix([sp.Rational(4, 3), sp.Rational(2, 3)])
    assert (spectator * flux_charges)[0] == 10
    allowed_characters = sp.diag(1, sp.Rational(1, 2)) * geometric.T
    assert allowed_characters * flux_charges == sp.Matrix([2, 1])
    assert allowed_characters * sp.Matrix([1, 0]) == sp.Matrix([1, 0])
    return dict(
        status='PASS',
        species_witness=witness,
        diagonal_character_smith=smith,
        angle_coefficient_labels=names,
        gauge_anomaly_rows=gauge.tolist(),
        invariant_phase_coefficients=invariants.tolist(),
        theta_period_generators_in_pi_units=[[2, 2], [0, 3]],
        spectator_even_sector_condition='3*Q_family = 0 mod 2',
        fourier_charge_generators=[[1, 0], [2, 1]],
        spin_flux_witness_charges=list(map(str, flux_charges)),
        spin_flux_witness_spectator_index=10,
    )


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2, default=int) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
