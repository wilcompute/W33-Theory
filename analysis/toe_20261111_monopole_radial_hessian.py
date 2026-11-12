"""Static second variation of the real W33 radial monopole energy."""

import json

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.linalg import cholesky_banded
from scipy.sparse import coo_matrix, diags

import toe_20261111_monopole_neutral_core as core

OUT = 'data/toe_20261111_monopole_radial_hessian.json'


def potential_half_hessian(residual, state, step, curvature_sign=1):
    """Half the local potential Hessian, including the residual curvature."""
    count, dimension = state.shape
    basis = np.eye(dimension)
    base = residual(state)
    jacobian = np.stack([residual(state + 1e-24j*v).imag / 1e-24 for v in basis[1:]], axis=-1)
    hessian = np.zeros((count, dimension, dimension))
    hessian[:, 1:, 1:] = jacobian.transpose(0, 2, 1) @ jacobian
    single = [residual(state + 1j*step*v).real - base for v in basis[1:]]
    for i, curvature in enumerate(single, 1):
        hessian[:, i, i] -= curvature_sign * 2 * np.sum(base * curvature, axis=1) / step**2
        for j in range(1, i):
            mixed = residual(state + 1j*step*(basis[i] + basis[j])).real - base
            correction = np.sum(base * (mixed - single[i-1] - single[j-1]), axis=1) / step**2
            hessian[:, i, j] -= curvature_sign * correction
            hessian[:, j, i] -= curvature_sign * correction
    return hessian


def half_hessian(residual, state, radius, step):
    hessian = potential_half_hessian(residual, state, step) * radius[:, None, None]**2

    # Gauge angular potential 3(1-K^2)^2/r^2 + 2 K^2 H^2.
    k, h = state[:, 0] / core.SQRT6, state[:, 1]
    hessian[:, 0, 0] = (3*k*k - 1)/radius**2 + h*h/3
    hessian[:, 0, 1] = hessian[:, 1, 0] = 4*k*h/core.SQRT6
    hessian[:, 1, 1] += 2*k*k
    return hessian


def quadratic_elements(grid):
    count = (len(grid)-1)//2
    nodes, weights = np.polynomial.legendre.leggauss(5)
    x = (1 + nodes)/2
    shape = np.column_stack([(1-x)*(1-2*x), 4*x*(1-x), x*(2*x-1)])
    derivatives = np.column_stack([4*x-3, 4-8*x, 4*x-1])
    indices = 2*np.arange(count)[:, None] + np.arange(3)
    width = grid[indices[:, 2]] - grid[indices[:, 0]]
    radii = grid[indices[:, 0], None] + width[:, None]*x
    quadrature = width[:, None] * weights/2
    differential = derivatives[None] / width[:, None, None]
    return indices, radii, shape, differential, quadrature


def assemble(residual, grid, state, boundary, step, local_form=half_hessian):
    indices, radii, shape, differential, quadrature = quadratic_elements(grid)
    count, order = radii.shape
    dimension = state.shape[1]
    mid = np.einsum('qn,cna->cqa', shape, state[indices])
    local = local_form(residual, mid.reshape(-1, dimension), radii.ravel(), step)
    local = local.reshape(count, order, dimension, dimension)

    # Both K and M are in the kinetic coordinates of the radial energy.
    kinetic = np.broadcast_to(radii[:, :, None]**2, (count, order, dimension)).copy()
    kinetic[:, :, 0] = 1
    form = np.einsum('cq,qi,cqab,qj->ciajb', quadrature, shape, local, shape, optimize=True)
    mass = np.zeros_like(form)
    diagonal = np.arange(dimension)
    form[:, :, diagonal, :, diagonal] += np.einsum(
        'cq,cqi,cqa,cqj->acij', quadrature, differential, kinetic, differential, optimize=True)
    mass[:, :, diagonal, :, diagonal] = np.einsum(
        'cq,qi,cqa,qj->acij', quadrature, shape, kinetic, shape, optimize=True)
    cols = (indices[:, :, None]*dimension + diagonal).reshape(count, 3*dimension)
    row = np.broadcast_to(cols[:, :, None], (count, 3*dimension, 3*dimension)).ravel()
    col = np.broadcast_to(cols[:, None, :], (count, 3*dimension, 3*dimension)).ravel()
    matrix_shape = (state.size, state.size)
    stiffness = coo_matrix((form.ravel(), (row, col)), shape=matrix_shape).tocsc()
    norm = coo_matrix((mass.ravel(), (row, col)), shape=matrix_shape).tocsc()
    free = np.arange(state.size)[2:-dimension]
    if boundary is not None:
        trace = np.arange(state.size-dimension+1, state.size)
        extra = boundary.T @ boundary
        stiffness += coo_matrix((extra.ravel(), (np.repeat(trace, len(trace)), np.tile(trace, len(trace)))),
                               shape=matrix_shape).tocsc()
        free = np.r_[free, trace]
    return stiffness[free][:, free], norm[free][:, free]


def bottom(stiffness, norm):
    # Congruence scaling makes the r=0 volume factors harmless for the inertia test.
    scale = diags(1 / np.sqrt(norm.diagonal()))
    stiffness = scale @ stiffness @ scale
    norm = scale @ norm @ scale
    width = 3*38
    def band(matrix):
        result = np.zeros((width, matrix.shape[0]))
        lower = matrix.tocoo()
        mask = lower.row >= lower.col
        assert np.max(lower.row[mask]-lower.col[mask]) < width
        result[lower.row[mask]-lower.col[mask], lower.col[mask]] = lower.data[mask]
        return result
    k, m = band(stiffness), band(norm)

    def positive(shift):
        try:
            cholesky_banded(k-shift*m, lower=True, check_finite=False)
            return True
        except np.linalg.LinAlgError:
            return False
    low, high = -1., 1.
    while not positive(low):
        low *= 10
    while positive(high):
        high *= 10
    for _ in range(34):
        middle = (low+high)/2
        if positive(middle):
            low = middle
        else:
            high = middle
    return dict(lowest_half_hessian_bracket=[low, high], positive_at_zero=positive(0))


def calculate():
    vacuum, _, _, residual, _ = core.model()
    ref = core.trial.flat.read(core.OUT)
    radii = np.array(ref['probe_radii'])
    fields = np.array(ref['normalized_profile_samples'])
    start = PchipInterpolator(np.r_[0., radii, 5., 9.],
                             np.vstack([fields[0], fields, vacuum, vacuum]), axis=0)
    jac = np.column_stack([residual(vacuum[None] + 1e-24j*d)[0].imag/1e-24
                           for d in np.eye(len(vacuum))[1:]])
    _, masses, right = np.linalg.svd(jac, full_matrices=False)
    masses[masses < 1e-8] = 0
    result = []
    for outer, count in [(5., 55), (9., 70)]:
        endpoints = np.r_[0., np.geomspace(1e-4, outer, count)]
        grid = np.empty(2*count+1)
        grid[::2] = endpoints
        grid[1::2] = (endpoints[:-1] + endpoints[1:])/2
        state = start(grid)
        state[0, :2], state[-1, 0] = [core.SQRT6, 0.], 0.
        boundary = np.sqrt(outer + outer**2*masses)[:, None]*right
        state, profile = core.minimize(residual, grid, state, (vacuum[1:], boundary))
        print('Hessian setup', outer, profile, flush=True)
        spectra = []
        for step in [1e-3, 5e-4]:
            k, m = assemble(residual, grid, state, boundary, step)
            data = bottom(k, m)
            spectra.append(dict(step=step, **data))
            print('Hessian result', outer, spectra[-1], flush=True)
        result.append(dict(outer_radius=outer, background=profile, spectra=spectra))
    return dict(status='PASS', static_radial_results=result)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (core.trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
