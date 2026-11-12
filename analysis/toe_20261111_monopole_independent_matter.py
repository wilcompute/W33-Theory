"""Release the paired matter mode and eliminate the sourced family connection."""

import json

import numpy as np
import sympy as sp
from scipy.integrate import quad_vec, solve_bvp

import toe_20261111_monopole_radial_solution as paired

trial = paired.trial
OUT = 'data/toe_20261111_monopole_independent_matter.json'
VACUUM = np.r_[paired.VACUUM, 0.]


def metric(u, v):
    gram = 6 + u**2 + v**2
    return 1 - 2 / gram, 4 * u / gram**2, 4 * v / gram**2


def potential():
    y, m, singlets, projector, _ = trial.sector_and_geometry()
    assert projector[0, 0] == sp.Rational(2, 9)
    basis, _ = np.linalg.qr(np.array(singlets, dtype=float))
    background = np.array(y, dtype=float).ravel()
    embedding = np.column_stack([-2.5 * np.array(m, dtype=float).ravel() / np.sqrt(75),
                                 basis, np.zeros((27, 2))])
    projector = np.array(projector, dtype=float)
    a0, a1, u, v = sp.symbols('a0 a1 u v', real=True)
    x, z, _ = trial.matter_data(u)
    bump = sp.Matrix([[0, 0, v / sp.sqrt(2)], [0, 0, 0]])
    x[0] -= bump
    z[0] += bump

    # Both representations restrict to the same real family rotations.
    tensor = sum((f.T * f for f in x + z), sp.zeros(3))
    assert sp.expand(tensor[0, 0] + tensor[2, 2]) == 6 + 2 * u**2 + v**2
    assert tensor[0, 1] == tensor[1, 2] == 0
    du, dv = sp.symbols('du dv', real=True)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        generator = sp.zeros(3)
        generator[j, i], generator[i, j] = 1, -1
        current = sum(sp.trace((f.diff(u) * du + f.diff(v) * dv).T * f * generator.T)
                      for f in x + z)
        assert sp.expand(current) == (2 * du if (i, j) == (0, 2) else 0)
    internal_moment = sum((f * f.T for f in x), sp.zeros(2))
    internal_moment -= sum((f * f.T for f in z), sp.zeros(2))
    assert internal_moment.applyfunc(sp.expand) == sp.diag(-2 * sp.sqrt(2) * u * v, 0)
    family_moment = sum((f.T * f for f in x), sp.zeros(3))
    family_moment -= sum((f.T * f for f in z), sp.zeros(3))
    family_moment -= sp.eye(3) * sp.trace(family_moment) / 3
    d_energy = (internal_moment[0, 0]**2 * sp.Rational(2, 9)
                + sp.trace(family_moment**2)) / 4
    assert sp.expand(d_energy - v**2 * (1 + sp.Rational(16, 9) * u**2)) == 0

    mixed = sum((z[j] * x[k].T for j, k in trial.MIXED), sp.zeros(2))
    entries = sp.zeros(29, 1)
    for index, coordinate in zip((0, 1, 27, 28), ((0, 0), (1, 1), (0, 1), (1, 0))):
        entries[index] = mixed[coordinate]
    source = np.array(entries.jacobian((u, v)), dtype=float)
    assert entries.subs({u: 0, v: 0}) == sp.zeros(29, 1)
    matter = trial.matter_f(a0, a1, x, z, trial.centered_gradient(x, z))
    variables = (a0, a1, u, v)
    evaluate = sp.lambdify(variables, list(matter) + list(matter.jacobian(variables)), 'numpy', cse=True)
    chain = np.vstack([embedding[:2], np.column_stack([np.zeros((2, 5)), np.diag([1 / np.sqrt(2), 1])])])
    f_vacuum = background**5 - 3 * background**4 - 283 * background

    w = sp.Symbol('w', real=True)
    variation = sp.Matrix([[0, 0, 0], [0, 0, w]])
    varied_x, varied_z = [*x[:2], x[2] + variation], [z[0], z[1] + variation]
    varied_matter = trial.matter_f(a0, a1, varied_x, varied_z,
                                  trial.centered_gradient(varied_x, varied_z))
    assert varied_matter.subs(w, 0) == matter
    evaluate_extra = sp.lambdify(variables, list(varied_matter.diff(w).subs(w, 0)), 'numpy', cse=True)

    def calculate(fields, extra=False):
        adj = background[:, None] + embedding @ (fields - VACUUM[1:, None])
        u, v = fields[-2] / np.sqrt(2), fields[-1]
        f_adj = np.pad(adj**5 - 3 * adj**4 - 283 * adj - f_vacuum[:, None], ((0, 2), (0, 0)))
        f_adj += source @ np.vstack([u, v])
        projection = projector @ f_adj
        terms = evaluate(adj[0], adj[1], u, v)
        arrays = np.stack([np.broadcast_to(value, u.shape) for value in terms])
        f, df = arrays[:30], arrays[30:].reshape(30, 4, -1)
        d = v**2 * (1 + 16 / 9 * u**2)
        energy = np.sum(f_adj * projection, axis=0) + np.sum(f**2, axis=0) + d
        curvature = 5 * adj**4 - 12 * adj**3 - 283
        gradient = 2 * embedding.T @ (curvature * projection[:27])
        gradient[-2:] += 2 * source.T @ projection / np.array([[np.sqrt(2)], [1]])
        gradient += 2 * chain.T @ np.einsum('im,ikm->km', f, df)
        gradient[-2] += 32 / (9 * np.sqrt(2)) * u * v**2
        gradient[-1] += 2 * v * (1 + 16 / 9 * u**2)
        if extra:
            variation = np.stack([np.broadcast_to(value, u.shape)
                                  for value in evaluate_extra(adj[0], adj[1], u, v)])
            derivative = (u + v / np.sqrt(2)) * projection[27]
            derivative += (u - v / np.sqrt(2)) * projection[28]
            return 2 * (derivative + np.sum(f * variation, axis=0))
        return energy, gradient, d

    return calculate


def expanded_guess(profile):
    def evaluate(radius):
        previous = profile(radius)
        zero = np.zeros_like(radius)
        return np.vstack([previous[:7], zero, previous[7:], zero])
    return evaluate


def solve(evaluate, guess, inner, outer, tolerance, release=True):
    def equation(radius, state):
        fields, velocities = state[:8], state[8:]
        k, h = fields[:2] / paired.NORMALIZATION[:2, None]
        _, force, _ = evaluate(fields[1:])
        g, du, dv = metric(*fields[-2:])
        acceleration = force / 2 - 2 * velocities[1:] / radius
        acceleration[0] += 2 * k**2 * fields[1] / radius**2
        acceleration[-2] += (force[-2] * (1 - g) - du * velocities[-2]**2
                             - 2 * dv * velocities[-2] * velocities[-1]) / (2 * g)
        acceleration[-1] += dv * velocities[-2]**2 / 2
        if not release:
            acceleration[-1] = -2 * velocities[-1] / radius
        gauge = fields[0] * ((k**2 - 1) / radius**2 + 25 * h**2)
        return np.vstack([velocities, gauge, acceleration])

    def conditions(left, right):
        _, force, _ = evaluate(left[1:8, None])
        force[-2] /= metric(*left[6:8])[0]
        if not release:
            force[-1] = 0
        regular = np.r_[left[0] - np.sqrt(6) - inner * left[8] / 2,
                        left[1] - inner * left[9],
                        left[10:] - inner * force[1:, 0] / 6]
        return np.r_[regular, right[:8] - VACUUM]

    mesh = np.geomspace(inner, outer, 400)
    solution = solve_bvp(equation, conditions, mesh, guess(mesh), tol=tolerance, max_nodes=12000)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def energy(evaluate, solution):
    def density(radius):
        state = solution.sol(radius)
        fields, velocities = state[:8], state[8:]
        k = fields[0] / np.sqrt(6)
        v, _, d = evaluate(fields[1:, None])
        g = metric(*fields[-2:])[0]
        kinetic = np.sum(velocities[1:]**2) - (1 - g) * velocities[-2]**2
        gauge = velocities[0]**2 + 3 * (1 - k**2)**2 / radius**2
        return np.array([gauge, radius**2 * kinetic + 2 * k**2 * fields[1]**2,
                         radius**2 * v[0], radius**2 * d[0]])

    inner, outer = solution.x[[0, -1]]
    pieces, _ = quad_vec(density, inner, outer, epsabs=1e-8, epsrel=1e-9,
                        points=[.002, .02, .2, .6, 1.2])
    pieces += density(inner) * inner / 3
    pieces[0] += 3 / outer
    return 4 * np.pi * pieces


def calculate():
    restricted, residuals, transverse, initial = paired.potential()
    initial_profile = paired.minimize_profile(residuals, initial, 3, 260)
    reference = paired.solve_profile(restricted, initial, .002, 3, 2e-6, initial_profile)
    guess = expanded_guess(reference.sol)
    evaluate = potential()
    check_radii = np.array([.002, .02, .1, .2, .4])
    sample = reference.sol(check_radii)[1:7]
    potential_values, derivatives, d = evaluate(np.vstack([sample, np.zeros(len(check_radii))]))
    old_values, old_derivatives = restricted(sample)
    np.testing.assert_allclose(potential_values, old_values, rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(derivatives[:-1], old_derivatives, rtol=1e-6, atol=1e-6)
    np.testing.assert_allclose(derivatives[-1], transverse(sample), rtol=1e-8, atol=1e-8)
    assert not np.any(d)
    family_corrected = solve(evaluate, guess, .002, 3, 2e-6, release=False)
    assert np.max(np.abs(family_corrected.y[7])) < 1e-9
    corrected_paired_energy = float(sum(energy(evaluate, family_corrected)[:3]))
    guess = family_corrected.sol
    results = []
    for inner, outer, tolerance in [(.002, 3, 2e-6), (.001, 4, 5e-7), (.0005, 5, 1e-7)]:
        solution = solve(evaluate, guess, inner, outer, tolerance)
        parts = energy(evaluate, solution)
        record = dict(inner=inner, outer=outer, nodes=len(solution.x),
                      max_collocation_residual=float(max(solution.rms_residuals)),
                      energy=float(sum(parts[:3])), gauge=float(parts[0]), scalar_gradient=float(parts[1]),
                      potential=float(parts[2]), d_energy=float(parts[3]),
                      virial_defect=float(parts[0] - parts[1] - 3 * parts[2]))
        results.append(record)
        print(record, flush=True)
        guess = solution.sol
    assert results[-1]['energy'] < corrected_paired_energy < 574.241567
    assert abs(results[-1]['energy'] - results[-2]['energy']) < 1e-4
    assert abs(results[-1]['virial_defect']) < 1e-4
    radii = np.r_[check_radii, .8, 1.6]
    state = solution.sol(radii)
    fields = state[:8]
    connection = -np.sqrt(2) * state[-2] / (6 + fields[-2]**2 + fields[-1]**2)
    extra_force = evaluate(fields[1:], extra=True) + 4 * connection**2
    assert np.max(np.abs(extra_force)) > .1
    assert max(abs(fields[-1])) > .001
    return dict(status='PASS', family_corrected_paired_energy=corrected_paired_energy,
                convergence=results, probe_radii=radii.tolist(),
                independent_matter_samples=fields[-2:].T.tolist(),
                remaining_matter_equation_residual=extra_force.tolist(),
                electric_phase=paired.phase_response(solution))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
