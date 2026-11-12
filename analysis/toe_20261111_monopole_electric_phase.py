"""Electric phase, theta normalization, and light-channel traces of the W33 monopole."""

import json
from types import SimpleNamespace

import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline, PchipInterpolator

import toe_20261110_monopole_color_operators as operators
import toe_20261111_monopole_neutral_core as core

OUT = 'data/toe_20261111_monopole_electric_phase.json'


def exact_phase():
    incoming, outgoing, alpha = operators.flavor_weights()
    _, internal, cartan, _, weak, y = core.trial.flat.compact_chart()
    topology = core.trial.core.topology
    five = topology.representation_check(internal, cartan, weak, y)['fundamental5_chart']
    _, coroot = core.trial.core.monopole_root(internal, five)
    fields = core.trial.flat.read(core.trial.core.OUT)['radial']
    m = sp.Matrix([sp.Rational(value) for value in fields['coroot_coefficients']])
    assert list(coroot[five]) == [1, 0, 0, -1, 0]
    assert sp.Matrix(alpha).dot(m) == 2
    traces = [sum(int(n)**2 for n in coroot),
              sum(int(n)**2 for n in core.trial.flat.adjoint_charges(internal, coroot))]
    assert traces == [12, 48]
    # The basic invariant form is Tr_27/6 on this long-root SU(2).
    assert sp.Rational(traces[0], 6) == 2

    holonomies = []
    pump = sp.zeros(6, 1)
    for weights, expected in [(incoming, -1), (outgoing, 1)]:
        charges = [sp.Matrix(weight[:4]).dot(m) for weight in weights]
        assert charges == [expected]*16
        holonomies.append(int((-1)**expected))
        for weight, charge in zip(weights, charges):
            pump += charge**2 * sp.Matrix(weight)/2
    assert pump == sp.zeros(6, 1)
    assert all(tuple(b-a for a, b in zip(w[:4], v[:4])) == alpha
               for w, v in zip(incoming[:12], outgoing[:12]))
    assert all(tuple(a+b for a, b in zip(w[:4], v[:4])) == (0, 0, 0, 0)
               for w, v in zip(incoming[12:], outgoing[12:]))
    assert sum(sp.Matrix(w[:4]).dot(m)**2 for w in incoming+outgoing)/2 == 16

    return dict(root_step=list(alpha), phase_period_over_pi=2,
                full_lift_endpoint_on_five=[-1, 1, 1, -1, 1],
                holonomy_by_lowest_wave_sign=holonomies,
                bare_kinetic_charge='integer - theta/(2*pi)',
                odd_dressing_momentum_shift='1/2',
                trace_indices_27_and_78=[value//2 for value in traces],
                topological_number_per_full_phase_cycle=1,
                light_occupation_trace=16, chiral_and_gaugino_contributions=[13, 3],
                formal_3B_L_and_Cartan_weighted_traces=list(map(int, pump)),
                one_step_particle_channels=12, zero_step_hole_channels=4)


def core_phase_response():
    vacuum, _, _, residual, _ = core.model()
    previous = core.trial.flat.read(core.OUT)
    radii = np.array(previous['probe_radii'])
    fields = np.array(previous['normalized_profile_samples'])
    start = PchipInterpolator(np.r_[0., radii, 5., 9.],
                             np.vstack([fields[0], fields, vacuum, vacuum]), axis=0)
    jacobian = np.column_stack([residual(vacuum[None]+1e-24j*d)[0].imag/1e-24
                                for d in np.eye(len(vacuum))[1:]])
    _, masses, right = np.linalg.svd(jacobian, full_matrices=False)
    masses[masses < 1e-8] = 0
    result = []
    for outer, count in [(5., 55), (9., 70)]:
        endpoints = np.r_[0., np.geomspace(1e-4, outer, count)]
        grid = np.empty(2*count+1)
        grid[::2], grid[1::2] = endpoints, (endpoints[:-1]+endpoints[1:])/2
        state = start(grid)
        state[0, :2], state[-1, 0] = [core.SQRT6, 0.], 0.
        boundary = np.sqrt(outer + outer**2*masses)[:, None]*right
        state, background = core.minimize(residual, grid, state, (vacuum[1:], boundary))
        spline = CubicSpline(grid, state, axis=0)
        start = spline
        profile = SimpleNamespace(x=np.array([0.0005, outer]), sol=lambda r: spline(r).T)
        phase = core.paired.phase_response(profile)
        result.append(dict(outer_radius=outer, background=background, **phase))
        print('Electric phase', result[-1], flush=True)
    inertia = result[-1]['inertia_at_unit_g']
    assert abs(inertia-result[0]['inertia_at_unit_g']) < .01
    tail = core.trial.flat.read('data/toe_20261111_monopole_neutral_tail.json')
    lightest = min(tail['lightest_physical_radial_masses'])
    gap = 1/(2*inertia)
    assert gap > 30*lightest
    return dict(convergence=result, bare_theta_zero_one_step=gap,
                bare_theta_zero_three_steps=9*gap, lightest_neutral_mass=lightest,
                one_step_to_lightest_mass_ratio=gap/lightest)


if __name__ == '__main__':
    result = dict(status='PASS', exact=exact_phase(), numerical=core_phase_response())
    payload = json.dumps(result, indent=2) + '\n'
    (core.trial.flat.ROOT / OUT).write_text(payload, encoding='utf-8')
    print(payload)
