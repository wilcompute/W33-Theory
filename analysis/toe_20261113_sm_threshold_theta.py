"""Standard Model bundle and monopole response of the two W33 mass phases."""

import json

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

import toe_20261110_global_gauge_topology as topology
import toe_20261113_canonical_strong_cp as strong_cp


OUT = 'data/toe_20261113_sm_threshold_theta.json'


def anomaly_coefficients():
    flat = topology.flat
    _, adjoint, cartan, color, weak, y = flat.compact_chart()
    five = topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    coroots = [(root @ root.T-root.T @ root).diagonal() for root in (color[0], color[1], weak)]
    for coroot in coroots:
        assert int(coroot @ coroot) == 12
    weights = np.stack([flat.adjoint_charges(adjoint, h) for h in [*coroots, y]], axis=1)
    mass = flat.sextic_adjoint_hessian(adjoint, y)
    affected = weights[np.any(mass, axis=1)]
    weak_roots = affected[affected[:, 2] != 0]
    assert sorted(map(tuple, weak_roots.tolist())) == [(0, 0, -2, 0), (0, 0, 2, 0)]
    color_roots = affected[np.any(affected[:, :2], axis=1)]
    assert len(color_roots) == 6 and not color_roots[:, 2:].any()
    for weight in weak_roots:
        cols = np.flatnonzero((weights == weight).all(axis=1))
        rows = np.flatnonzero((weights == -weight).all(axis=1))
        assert len(cols) == len(rows) == 1 and mass[rows[0], cols[0]] != 0
    reference = flat.read(strong_cp.OUT)
    assert reference['triplet_split_determinant_ratio'] == 'z_T**3'
    assert reference['octet_anomaly_weight'] == 3
    assert any(row == {'weak_and_six_Y': [0, -2], 'rank': 21}
               for row in reference['triplet_weight_blocks'])
    five_color_weights = {tuple(coroots[j][i].item() for j in range(2)) for i in five[:3]}
    assert five_color_weights == {(0, 1), (1, -1), (-1, 0)}
    # Each triplet pair has three states of integer hypercharge -2.
    triplet_phase = sp.Matrix([3, 0, 3*3*4])
    adjoint_phase = sp.Matrix([3, 2, 0])
    parent_phase = sp.Matrix([1, 1, sum(int(n)**2 for n in y[five])])
    assert list(parent_phase) == [1, 1, 30]
    return adjoint_phase, triplet_phase, parent_phase


def calculate():
    adjoint_phase, triplet_phase, parent_phase = anomaly_coefficients()
    q_from_integer = sp.Matrix([
        [1, 0, sp.Rational(2, 3)],
        [0, 1, sp.Rational(1, 2)],
        [0, 0, sp.Rational(1, 36)],
    ])
    periods = q_from_integer.T.inv()
    assert periods == sp.Matrix([[1, 0, 0], [0, 1, 0], [-24, -18, 36]])
    integrated = q_from_integer.T*sp.Matrix.hstack(adjoint_phase, triplet_phase, parent_phase)
    assert integrated == sp.Matrix([[3, 3, 1], [2, 0, 1], [3, 3, 2]])
    smith_two = [abs(int(v)) for v in smith_normal_form(integrated[:, :2], domain=sp.ZZ).diagonal()]
    smith_all = [abs(int(v)) for v in smith_normal_form(integrated, domain=sp.ZZ).diagonal()]
    assert smith_two == [1, 6] and smith_all == [1, 1, 6]
    assert integrated[:, 0]-integrated[:, 1] == sp.Matrix([0, 2, 0])
    assert q_from_integer*sp.Matrix([0, 0, 1]) == sp.Matrix([
        sp.Rational(2, 3), sp.Rational(1, 2), sp.Rational(1, 36),
    ])

    monopole = sp.Matrix(topology.cocharacters()['primitive_monopole'])
    hypercharge = sp.Matrix([-2, -2, -2, 3, 3])
    h = monopole.dot(hypercharge)/hypercharge.dot(hypercharge)
    assert h == -sp.Rational(1, 6)
    m3 = monopole[:3, :]-h*hypercharge[:3, :]
    m2 = monopole[3:, :]-h*hypercharge[3:, :]
    # For a traceless m, choose the hypercharge functional whose dot
    # product with m is the common Abelian coefficient.
    hypercharge_dual = hypercharge / hypercharge.dot(hypercharge)

    def electric_shift(phase):
        return (phase[0]*m3).col_join(phase[1]*m2)+phase[2]*h*hypercharge_dual

    weight_a = electric_shift(adjoint_phase)
    weight_t = electric_shift(triplet_phase)+sp.Rational(3, 5)*sp.ones(5, 1)
    assert weight_a == sp.Matrix([2, -1, -1, -1, 1])
    assert weight_t == sp.Matrix([3, 0, 0, 0, 0])
    assert electric_shift(parent_phase) == monopole
    assert all(weight[1] == weight[2] for weight in (weight_a, weight_t))
    difference = weight_a-weight_t+sp.ones(5, 1)
    assert difference == sp.Matrix([0, 0, 0, 0, 2])
    electric = sp.Matrix([-sp.Rational(1, 3)]*3+[1, 0])
    assert weight_a.dot(electric) == weight_t.dot(electric) == -1
    assert weight_a.dot(monopole)/2 == weight_t.dot(monopole)/2 == sp.Rational(3, 2)
    # Q = Y + T3. The weak coroot coefficient is 1/2 and the
    # integer hypercharge generator 6Y has coefficient 1/6.
    photon = sp.Matrix([0, sp.Rational(1, 2), sp.Rational(1, 36)])
    assert photon.dot(adjoint_phase) == photon.dot(triplet_phase) == 1
    return dict(
        status='PASS', phase_order=['adjoint', 'triplet', 'parent_E6'],
        angle_coefficient_columns=sp.Matrix.hstack(adjoint_phase, triplet_phase, parent_phase).tolist(),
        integral_spin_charge_coefficient_columns=integrated.tolist(),
        angle_period_generators_in_2pi_units=periods.tolist(),
        heavy_phase_smith=smith_two, heavy_and_parent_smith=smith_all,
        pure_determinant_flux_phase_indices=[3, 3, 2],
        monopole_primitive=list(map(int, monopole)),
        monopole_electric_shift_representatives=[list(map(int, w)) for w in (weight_a, weight_t)],
        shift_difference_mod_trivial_character=list(map(int, difference)),
        monopole_electric_Q_shift=-1, m_over_two_pairing='3/2',
        kappa_character_of_both_shifts=-1, electromagnetic_theta_coefficient=1,
        conditional_axion_E_over_N='2/3',
    )


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2, default=int) + '\n'
    (topology.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
