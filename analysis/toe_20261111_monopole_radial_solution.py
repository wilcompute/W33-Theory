"""Radial Euler–Lagrange solution on the canonical W33 D-flat trial manifold."""

import json

import numpy as np
import sympy as sp
from scipy.integrate import quad_vec, solve_bvp
from scipy.interpolate import CubicSpline
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve

import toe_20261111_monopole_variational_core as trial

OUT = 'data/toe_20261111_monopole_radial_solution.json'
NORMALIZATION = np.array([6**0.5, 75**0.5, 1, 1, 1, 1, 2**0.5])
VACUUM = np.array([0, 75**0.5, 0, 0, 0, 0, 0])


def potential():
    y, m, singlets, projector, _ = trial.sector_and_geometry()
    orthogonal, _ = np.linalg.qr(np.asarray(singlets, dtype=float))
    background = np.asarray(y, dtype=float).ravel()
    coroot = np.asarray(m, dtype=float).ravel()
    projector = np.asarray(projector, dtype=float)
    embedding = np.column_stack([-2.5 * coroot / NORMALIZATION[1], orthogonal, np.zeros(27)])
    source = np.zeros(29)
    source[[0, 27, 28]] = 2, 1, 1
    a0, a1, u = sp.symbols('a0 a1 u', real=True)
    x, z, gradients = trial.matter_data(u)
    matter = trial.matter_f(a0, a1, x, z, gradients)
    variables = (a0, a1, u)
    matter_jacobian = matter.jacobian(variables)
    evaluate_matter = sp.lambdify(variables, list(matter) + list(matter_jacobian), 'numpy', cse=True)
    chain = np.vstack([embedding[:2], [0, 0, 0, 0, 0, 1 / NORMALIZATION[-1]]])
    f_vacuum = background**5 - 3 * background**4 - 283 * background

    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    keep = eigenvalues > 1e-12
    square_root = np.sqrt(eigenvalues[keep])[:, None] * eigenvectors[:, keep].T

    def potential_residuals(fields):
        """The potential and its gradient on the six scalar coordinates."""
        adjoint = background[:, None] + embedding @ (fields - VACUUM[1:, None])
        matter_u = fields[-1] / NORMALIZATION[-1]
        f_adj = adjoint**5 - 3 * adjoint**4 - 283 * adjoint - f_vacuum[:, None]
        full_covector = np.pad(f_adj, ((0, 2), (0, 0))) + source[:, None] * matter_u
        result = evaluate_matter(adjoint[0], adjoint[1], matter_u)
        arrays = np.stack([np.broadcast_to(item, matter_u.shape) for item in result])
        f_matter, jacobian = arrays[:30], arrays[30:].reshape(30, 3, -1)
        curvature = 5 * adjoint**4 - 12 * adjoint**3 - 283
        adjoint_jacobian = np.pad(curvature[:, None] * embedding[:, :, None], ((0, 2), (0, 0), (0, 0)))
        adjoint_jacobian[:, -1] += source[:, None] / NORMALIZATION[-1]
        f = np.vstack([square_root @ full_covector, f_matter])
        df = np.concatenate([np.einsum('ij,jkn->ikn', square_root, adjoint_jacobian),
                             np.einsum('ijn,jk->ikn', jacobian, chain)])
        return f, df

    def value_and_gradient(fields):
        f, df = potential_residuals(fields)
        return np.sum(f**2, axis=0), 2 * np.einsum('im,ikm->km', f, df)

    w = sp.Symbol('w', real=True)
    varied_z = [z[0] + sp.Matrix([[0, 0, w], [0, 0, 0]]), z[1]]
    varied_f = trial.matter_f(a0, a1, x, varied_z, trial.centered_gradient(x, varied_z))
    assert varied_f.subs(w, 0) == matter
    normal_matter = sp.lambdify(variables, list(varied_f.diff(w).subs(w, 0)), 'numpy', cse=True)
    changed_source = np.zeros(29)
    changed_source[[0, 27]] = 1

    def transverse_force(fields):
        """Force along the unit variation with delta Z0 opposite to delta X0."""
        f, df = potential_residuals(fields)
        adjoint = background[:, None] + embedding @ (fields - VACUUM[1:, None])
        matter_u = fields[-1] / NORMALIZATION[-1]
        varied = normal_matter(adjoint[0], adjoint[1], matter_u)
        varied = np.stack([np.broadcast_to(item, matter_u.shape) for item in varied])
        adjoint_rows = square_root.shape[0]
        only_z = (square_root @ changed_source) @ f[:adjoint_rows]
        only_z += np.sum(varied * f[adjoint_rows:], axis=0)
        both = np.sum(f * df[:, -1], axis=0)
        return 2 * (np.sqrt(2) * only_z - both)

    amplitudes = np.array([2718, 5209, -4512, -4398, -989]) / 10000
    normal = orthogonal.T @ np.asarray(singlets, dtype=float) @ amplitudes[:4]
    initial_singlets = np.r_[normal, amplitudes[-1] * NORMALIZATION[-1]]
    return value_and_gradient, potential_residuals, transverse_force, initial_singlets


def initial_guess(radius, singlets):
    scalar_radius, gauge_radius = 0.0277, 0.2328
    s = radius / np.sqrt(radius**2 + scalar_radius**2)
    k = gauge_radius**2 / (radius**2 + gauge_radius**2)
    ds = scalar_radius**2 / (radius**2 + scalar_radius**2)**1.5
    dk = -2 * radius * k / (radius**2 + gauge_radius**2)
    return np.vstack([NORMALIZATION[0] * k, NORMALIZATION[1] * s,
                      singlets[:, None] * (1 - s**2),
                      NORMALIZATION[0] * dk, NORMALIZATION[1] * ds,
                      -2 * singlets[:, None] * s * ds])


def minimize_profile(potential_residuals, initial_singlets, outer, count):
    """Damped Gauss–Newton on a piecewise-linear radial finite element space."""
    grid = np.r_[0, np.geomspace(2e-5, outer, count)]
    nodes, weights = np.polynomial.legendre.leggauss(3)
    position = np.tile((1 + nodes) / 2, count)
    left = np.repeat(np.arange(count), len(nodes))
    width = np.diff(grid)[left]
    radius = grid[left] + position * width
    quadrature = np.sqrt(np.tile(weights, count) * width / 2)
    state = initial_guess(grid, initial_singlets)[:7].T.copy()
    state[-1] = VACUUM
    free = np.arange(state.size)[2:-7]

    def residuals(state, derivatives=False):
        values = state[left] * (1 - position[:, None]) + state[left + 1] * position[:, None]
        slopes = (state[left + 1] - state[left]) / width[:, None]
        k, h = values[:, 0] / NORMALIZATION[0], values[:, 1]
        f, df = potential_residuals(values[:, 1:].T)
        kinetic_weight = np.column_stack([np.ones_like(radius), np.tile(radius[:, None], (1, 6))])
        result = np.column_stack([kinetic_weight * slopes, np.sqrt(3) * (1 - k**2) / radius,
                                  np.sqrt(2) * k * h, radius[:, None] * f.T])
        result *= quadrature[:, None]
        if not derivatives:
            return result.ravel()
        count_rows = result.shape[1]
        jac = np.zeros((len(radius), count_rows, 7))
        jac[:, 7, 0] = -2 * np.sqrt(3) * k / (NORMALIZATION[0] * radius)
        jac[:, 8, 0] = np.sqrt(2) * h / NORMALIZATION[0]
        jac[:, 8, 1] = np.sqrt(2) * k
        jac[:, 9:, 1:] = radius[:, None, None] * df.transpose(2, 0, 1)
        kinetic = np.zeros_like(jac)
        kinetic[:, np.arange(7), np.arange(7)] = kinetic_weight / width[:, None]
        jac_left = (jac * (1 - position[:, None, None]) - kinetic) * quadrature[:, None, None]
        jac_right = (jac * position[:, None, None] + kinetic) * quadrature[:, None, None]
        row = np.broadcast_to(np.arange(result.size).reshape(-1, count_rows, 1), jac.shape).ravel()
        col = np.broadcast_to((7 * left[:, None, None] + np.arange(7)), jac.shape).ravel()
        sparse = coo_matrix((np.r_[jac_left.ravel(), jac_right.ravel()],
                             (np.r_[row, row], np.r_[col, col + 7])),
                            shape=(result.size, state.size)).tocsc()
        sparse.eliminate_zeros()
        return result.ravel(), sparse[:, free]

    damping = 1e-3
    for iteration in range(170):
        residual, jac = residuals(state, True)
        error = residual @ residual
        gradient = jac.T @ residual
        gram = jac.T @ jac
        scale = gram.diagonal()
        scaled_gradient = np.linalg.norm(gradient / np.sqrt(scale), ord=np.inf)
        if scaled_gradient < 2e-7:
            break
        for attempt in range(12):
            step = spsolve(gram + diags(damping * scale), -gradient)
            candidate = state.copy()
            candidate.flat[free] += step
            candidate_residual = residuals(candidate)
            if candidate_residual @ candidate_residual < error:
                state = candidate
                damping = max(1e-10, damping / 2)
                break
            damping *= 5
        else:
            raise RuntimeError(f'Radial minimization stalled at {scaled_gradient}')
    else:
        raise RuntimeError(f'Radial minimization did not converge: {scaled_gradient}')
    print(f'Finite elements: E={4*np.pi*(error + 3/outer):.9f}, {iteration} iterations', flush=True)
    spline = CubicSpline(grid, state.T, axis=1)

    def interpolate(radius):
        return np.vstack([spline(radius), spline(radius, 1)])

    return interpolate


def solve_profile(evaluate, initial_singlets, inner, outer, tolerance, previous=None):
    def equation(radius, state):
        fields, derivatives = state[:7], state[7:]
        k, h = fields[:2] / NORMALIZATION[:2, None]
        _, grad = evaluate(fields[1:])
        acceleration = grad / 2 - 2 * derivatives[1:] / radius
        acceleration[0] += 2 * k**2 * fields[1] / radius**2
        gauge = fields[0] * ((k**2 - 1) / radius**2 + 25 * h**2)
        return np.vstack([derivatives, gauge, acceleration])

    def conditions(left, right):
        _, force = evaluate(left[1:7, None])
        origin = np.r_[left[0] - NORMALIZATION[0] - inner * left[7] / 2,
                       left[1] - inner * left[8],
                       left[9:] - inner * force[1:, 0] / 6]
        return np.r_[origin, right[:7] - VACUUM]

    mesh = np.geomspace(inner, outer, 340)
    guess = initial_guess(mesh, initial_singlets) if previous is None else previous(mesh)
    solution = solve_bvp(equation, conditions, mesh, guess, tol=tolerance, max_nodes=12000)
    if not solution.success:
        raise RuntimeError(f'{solution.message} residual {max(solution.rms_residuals)}')
    return solution


def energy(evaluate, solution):
    def density(radius):
        state = solution.sol(radius)
        k = state[0] / NORMALIZATION[0]
        potential, _ = evaluate(state[1:7, None])
        gauge = state[7]**2 + 3 * (1 - k**2)**2 / radius**2
        angular = 2 * k**2 * state[1]**2
        return np.array([gauge, radius**2 * np.sum(state[8:]**2) + angular, radius**2 * potential[0]])

    inner, outer = solution.x[[0, -1]]
    components, error = quad_vec(density, inner, outer, epsabs=1e-8, epsrel=1e-9,
                                 points=[0.002, 0.02, 0.2, 0.6, 1.2])
    components += density(inner) * inner / 3
    components[0] += 3 / outer
    return components * 4 * np.pi, error * 4 * np.pi


def phase_response(solution):
    inner, outer = solution.x[[0, -1]]

    def equation(radius, profile):
        p, dp = profile
        k = solution.sol(radius)[0] / NORMALIZATION[0]
        return np.vstack([dp, 2 * (k**2 * p - radius * dp) / radius**2])

    def conditions(left, right):
        return np.array([left[0] - inner * left[1], right[0] + outer * right[1] - 1])

    mesh = np.geomspace(inner, outer, 350)
    start = np.stack([mesh / (0.2 + mesh), 0.2 / (0.2 + mesh)**2])
    phase = solve_bvp(equation, conditions, mesh, start, tol=1e-8, max_nodes=6000)
    if not phase.success:
        raise RuntimeError(phase.message)
    coulomb_length = outer**2 * phase.y[1, -1]
    return dict(coulomb_length=float(coulomb_length), inertia_at_unit_g=float(24 * np.pi * coulomb_length),
                max_collocation_residual=float(max(phase.rms_residuals)))


def calculate():
    evaluate, residuals, transverse, initial = potential()
    records = []
    previous = minimize_profile(residuals, initial, 3, 260)
    for inner, outer, tolerance in [(0.002, 3, 2e-6), (0.001, 4, 5e-7), (0.0005, 5, 1e-7)]:
        solution = solve_profile(evaluate, initial, inner, outer, tolerance, previous)
        pieces, quadrature_error = energy(evaluate, solution)
        record = dict(inner=inner, outer=outer, nodes=len(solution.x),
                      max_collocation_residual=float(max(solution.rms_residuals)),
                      energy=float(sum(pieces)), quadrature_error=quadrature_error,
                      energy_components=pieces.tolist(),
                      virial_defect=float(pieces[0] - pieces[1] - 3 * pieces[2]))
        records.append(record)
        print(record, flush=True)
        previous = solution.sol
    probes = np.array([0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6])
    samples = solution.sol(probes)
    force = transverse(samples[1:7])
    assert np.max(np.abs(force)) > 0.1
    assert abs(records[-1]['energy'] - records[-2]['energy']) < 0.01
    assert abs(records[-1]['virial_defect']) < 0.01
    assert records[-1]['energy'] < 635
    return dict(probe_radii=probes.tolist(), profile_samples=samples[:7].T.tolist(),
                unit_omitted_matter_force=force.tolist(),
                electric_phase=phase_response(solution), status='PASS', convergence=records)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
