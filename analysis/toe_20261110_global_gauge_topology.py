"""Exact representation and cocharacter checks for the W33 global gauge group."""

import json

import numpy as np
import sympy as sp

import toe_20261109_canonical_sm_flatness as flat

OUT = 'data/toe_20261110_global_gauge_topology.json'


def root_component(roots, start):
    supports = np.any(np.stack(roots), axis=0)
    neighbors = supports | supports.T
    component = {start}
    while True:
        reached = set(map(int, np.flatnonzero(neighbors[sorted(component)].any(axis=0))))
        if reached <= component:
            return component
        component |= reached


def representation_check(internal, cartan, weak, y):
    vacuum_pair = [0, 1]
    vector10 = flat.read(flat.SM)['exotic_mass_support']
    spinor16 = sorted(set(range(27)) - {0, *vector10})
    assert len(vector10) == 10 and len(spinor16) == 16 and 1 in spinor16
    charges = np.ones(27, dtype=np.int64)
    charges[0], charges[vector10] = 4, -2
    coefficients = sp.Matrix(cartan.T).gauss_jordan_solve(sp.Matrix(charges))[0]
    assert np.array_equal(np.array(coefficients).ravel() @ cartan, charges)
    # In the trace metric the moment of the first weight ray is H/18.
    assert all(np.dot(charges, a.diagonal()) == 18 * a[0, 0] for a in internal)
    d5_roots = [a for a in internal if not np.array_equal(a, np.diag(a.diagonal()))
                and not (a * (charges[:, None] - charges[None, :])).any()]
    assert len(d5_roots) == 40 and all(not a[:, 0].any() for a in d5_roots)
    assert root_component(d5_roots, vector10[0]) == set(vector10)
    assert root_component(d5_roots, 1) == set(spinor16)
    assert np.gcd.reduce(np.abs(charges)) == 1
    assert np.all(charges % 3 == 1)
    assert [int(value % 4) for value in (charges[0], charges[vector10[0]], charges[1])] == [0, 2, 1]

    roots = [a for a in internal if not np.array_equal(a, np.diag(a.diagonal()))
             and not a[:, vacuum_pair].any() and not a[vacuum_pair, :].any()]
    assert len(roots) == 20
    component = root_component(roots, 21)
    ordered = sorted(component, key=lambda i: (y[i], i))
    assert ordered == [24, 25, 26, 21, 23]
    assert y[ordered].tolist() == [-2, -2, -2, 3, 3]
    weak_weight = (weak @ weak.T - weak.T @ weak).diagonal()
    assert weak_weight[ordered].tolist() == [0, 0, 0, 1, -1]
    return dict(circle_charges=dict(singlet=4, vector10=-2, spinor16=1),
                circle_cartan_coefficients=[str(c) for c in coefficients],
                d5_line_roots=len(d5_roots), spinor_slot=1,
                su5_roots=len(roots), fundamental5_chart=ordered)


def cocharacters():
    # Lie algebra generators are written as real diagonal Hermitian arrays.
    hypercharge = sp.Matrix([-sp.Rational(1, 3)] * 3 + [sp.Rational(1, 2)] * 2)
    electric = hypercharge + sp.Matrix([0, 0, 0, sp.Rational(1, 2), -sp.Rational(1, 2)])
    monopole = sp.Matrix([1, 0, 0, -1, 0])
    assert sum(monopole) == 0 and sum(monopole[:3]) == 1 and monopole[4] == 0
    assert monopole.dot(hypercharge) / hypercharge.dot(hypercharge) == -1
    assert monopole.dot(electric) / electric.dot(electric) == -1
    color_compensation = monopole + electric
    assert list(color_compensation) == [sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3), 0, 0]
    # Fractions in the two covering-kernel representatives are phases
    # measured in turns. Color and weak center elements cancel the U(1).
    sm_center = sp.Matrix([sp.Rational(1, 3)] * 3 + [sp.Rational(1, 2)] * 2)
    sm_identity = sm_center + hypercharge
    em_center = sp.Matrix([sp.Rational(1, 3)] * 3 + [0, 0])
    em_identity = em_center + electric
    assert all(value.q == 1 for value in sm_identity)
    assert all(value.q == 1 for value in em_identity)
    return dict(primitive_monopole=list(map(int, monopole)),
                hypercharge_projection=-1, electromagnetic_projection=-1,
                color_compensation=[str(value) for value in color_compensation],
                primitive_sm_u1_kernel_angle='pi/3', primitive_em_u1_kernel_angle='2*pi/3',
                common_color_determinant_winding=1)


def calculate():
    _, internal, cartan, _, weak, y = flat.compact_chart()
    return dict(status='PASS', representation=representation_check(internal, cartan, weak, y),
                cocharacters=cocharacters(),
                conditional_global_groups=dict(
                    faithful_parent='(E6_sc x SU(3))/Z3',
                    faithful_stabilizer='S(U(3) x U(2))',
                    cover_stabilizer='S(U(3) x U(2)) x Z3',
                    electroweak_stabilizer='(SU(3) x U(1)_em)/Z3'),
                vacuum_homotopy=dict(pi2='Z', pi1='Z3',
                                    electroweak_pi2=0, electroweak_pi1=0,
                                    E8_parent_monopole_to_string_boundary='isomorphism Z3 to Z3'))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
