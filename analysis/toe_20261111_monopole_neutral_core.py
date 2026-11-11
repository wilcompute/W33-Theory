"""Real color-invariant W33 radial profiles in radial gauge."""

import json
from itertools import combinations

import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.sparse import coo_matrix, diags, vstack
from scipy.sparse.linalg import spsolve

import toe_20261111_monopole_radial_solution as paired

trial = paired.trial
OUT = 'data/toe_20261111_monopole_neutral_core.json'
SQRT6 = np.sqrt(6)
SQRT75 = np.sqrt(75)


def geometry():
    _, internal, cartan, color, weak, y = trial.flat.compact_chart()
    five = trial.core.topology.representation_check(
        internal, cartan, weak, y)['fundamental5_chart']
    root, m = trial.core.monopole_root(internal, five)
    # The torus-fixed indices are certified by the previous exact weight ledger.
    fixed = trial.flat.read(trial.core.OUT)['fixed_torus_sector']['fixed_internal_adjoint_slots']
    selected = internal[fixed]
    constraints = np.concatenate([(selected @ g - g @ selected).reshape(len(fixed), -1)
                                  for g in (color[0], color[0].T, root, root.T)], axis=1)
    coefficients = sp.Matrix(constraints.T).nullspace()
    assert len(coefficients) == 6
    singlets = np.asarray(sp.Matrix.hstack(*coefficients).T, dtype=float) @ selected.reshape(len(fixed), -1)
    basis = np.linalg.qr(singlets.T)[0].T.reshape(6, 27, 27)
    m_unit = -np.diag(m) / np.sqrt(np.dot(m, m))
    embedding = np.concatenate([m_unit[None], basis])
    assert np.allclose(embedding.reshape(7, -1) @ embedding.reshape(7, -1).T, np.eye(7))
    assert np.allclose(np.einsum('aij,ij->a', embedding, np.diag(y)) @ embedding.reshape(7, -1),
                       np.diag(y).ravel())
    support = np.any(np.abs(embedding) > 1e-12, axis=0)
    assert np.all(support.sum(axis=1) <= 2)
    assert np.all(support == support.T)
    p, q = np.where(np.triu(support, 1))
    assert len(set(p) | set(q)) == 2 * len(p)
    root_pairs = (p, q)

    # The omitted raising and lowering adjoint directions carry monopole weight.
    # The diagonal-gauge F and D covectors are weight zero.
    assert not np.any(root[:2]) and not np.any(root[:, :2])
    assert np.allclose(embedding[:, :2, 2:], 0) and np.allclose(embedding[:, 2:, :2], 0)
    matrices = [sp.Matrix(selected.reshape(len(fixed), -1)).T * c for c in coefficients]
    matrices = [a.reshape(27, 27) for a in matrices]
    antisymmetric, = sp.Matrix.hstack(*[(a + a.T).reshape(729, 1) for a in matrices]).nullspace()
    internal_rotation = np.array(sum((c * a for c, a in zip(antisymmetric, matrices)),
                                     sp.zeros(27)), dtype=float)
    internal_rotation /= internal_rotation[1, 0]
    np.testing.assert_allclose(internal_rotation[:2, :2], [[0, -1], [1, 0]])
    return embedding, root_pairs, internal_rotation, y


def model():
    embedding, pairs, internal_rotation, y = geometry()
    p, q = pairs
    diagonal = np.diagonal(embedding, axis1=1, axis2=2)
    off_left, off_right = embedding[:, p, q], embedding[:, q, p]
    neutral = embedding[:, :2, :2]
    x0, z0, terms = trial.centered_terms()
    matter0 = np.concatenate([x0.reshape(3, 27, 3)[:, :2], z0.reshape(2, 27, 3)[:, :2]])
    adjoint0 = diagonal @ y
    vacuum = np.r_[0., adjoint0, matter0.ravel()]
    trace_vacuum = y**5 - 3 * y**4 - 283 * y
    words = [term['meson_trace'] for term in terms]
    centers = [term['center'] for term in terms]

    def fields(state):
        coordinates = state[:, 1:8]
        matter = state[:, 8:].reshape(-1, 5, 2, 3)
        return coordinates, matter

    def residual(state):
        coordinates, matter = fields(state)
        x, z = matter[:, :3], matter[:, 3:]
        ad = coordinates @ diagonal
        left, right = coordinates @ off_left, coordinates @ off_right
        blocks = np.stack([ad[:, p], left, right, ad[:, q]], axis=-1).reshape(-1, len(p), 2, 2)
        fourth = blocks @ blocks
        fourth = fourth @ fourth
        polynomials = fourth @ blocks - 3 * fourth - 283 * blocks
        derivatives = ad**5 - 3 * ad**4 - 283 * ad
        derivatives[:, p], derivatives[:, q] = polynomials[:, :, 0, 0], polynomials[:, :, 1, 1]
        f_adj = (derivatives - trace_vacuum) @ diagonal.T
        f_adj += polynomials[:, :, 1, 0] @ off_left.T + polynomials[:, :, 0, 1] @ off_right.T
        a = np.einsum('na,aij->nij', coordinates, neutral)
        f_x, f_z = np.zeros_like(x), np.zeros_like(z)
        for j, k in trial.MIXED:
            f_x[:, k] += a.transpose(0, 2, 1) @ z[:, j]
            f_z[:, j] += a @ x[:, k]
            f_adj += np.einsum('nij,aij->na', z[:, j] @ x[:, k].transpose(0, 2, 1), neutral)

        mesons = np.einsum('nkia,njib->njkab', x, z).reshape(-1, 6, 3, 3)
        for word, center in zip(words, centers):
            value = mesons[:, word[0]]
            for letter in word[1:]:
                value = value @ mesons[:, letter]
            shift = np.trace(value, axis1=1, axis2=2) - center
            for position, letter in enumerate(word):
                j, k = divmod(letter, 3)
                cycle = word[position + 1:] + word[:position]
                if cycle:
                    factor = mesons[:, cycle[0]]
                    for other in cycle[1:]:
                        factor = factor @ mesons[:, other]
                else:
                    factor = np.eye(3)
                f_x[:, k] += (z[:, j] @ factor) * shift[:, None, None]
                f_z[:, j] += (x[:, k] @ np.swapaxes(factor, -1, -2)) * shift[:, None, None]

        delta = ad[:, p] - ad[:, q]
        d_diag = np.zeros_like(ad)
        d_diag[:, p], d_diag[:, q] = left**2 - right**2, right**2 - left**2
        d_off = delta * (right - left)
        d_adj = d_diag @ diagonal.T + d_off @ (off_left + off_right).T
        d_matter = (np.einsum('nkia,nkja->nij', x, x)
                    - np.einsum('nkia,nkja->nij', z, z))
        d_adj += np.einsum('nij,aij->na', d_matter, neutral)
        d_family = np.einsum('nkia,nkib->nab', x, x) - np.einsum('nkia,nkib->nab', z, z)
        d_family -= np.trace(d_family, axis1=1, axis2=2)[:, None, None] * np.eye(3) / 3
        return np.column_stack([f_adj, f_x.reshape(-1, 18), f_z.reshape(-1, 12),
                                d_adj / 2, d_family.reshape(-1, 9) / 2])

    def generators(state):
        coordinates, matter = fields(state)
        adjoint = np.einsum('na,aij->nij', coordinates, embedding)
        variations = np.zeros((len(state), 4, state.shape[1]))
        adjoint_variation = internal_rotation @ adjoint - adjoint @ internal_rotation
        variations[:, 0, 1:8] = np.einsum('nij,aij->na', adjoint_variation, embedding)
        variations[:, 0, 8:] = (internal_rotation[:2, :2] @ matter).reshape(-1, 30)
        for j, (left, right) in enumerate(combinations(range(3), 2), 1):
            generator = np.zeros((3, 3))
            generator[right, left], generator[left, right] = 1, -1
            variations[:, j, 8:] = (matter @ generator.T).reshape(-1, 30)
        return variations

    assert np.linalg.norm(residual(vacuum[None])) < 1e-8
    assert np.linalg.matrix_rank(generators(vacuum[None])[0]) == 4
    # Compare the complete D-flat reference potential and the gauge Ward identity.
    probe = initial_profile(np.array([.02, .1, .2]), vacuum, embedding, matter0)
    prior = trial.flat.read(paired.OUT)
    rows = [prior['probe_radii'].index(float(r)) for r in (.02, .1, .2)]
    prior_fields = np.array(prior['profile_samples'])[rows, 1:].T
    evaluate, _, _, _ = paired.potential()
    np.testing.assert_allclose(np.sum(residual(probe)**2, axis=1), evaluate(prior_fields)[0],
                               rtol=1e-9, atol=1e-8)
    perturbed = probe + np.random.default_rng(724).normal(0, .05, probe.shape)
    base = residual(perturbed)
    for tangent in generators(perturbed).transpose(1, 0, 2):
        slope = residual(perturbed + 1e-24j*tangent).imag / 1e-24
        assert np.max(np.abs(np.sum(base * slope, axis=1))) < 2e-6
    return vacuum, embedding, matter0, residual, generators


def initial_profile(grid, vacuum, embedding, matter0):
    old = trial.flat.read(paired.OUT)
    x = np.array(old['probe_radii'])
    data = np.array(old['profile_samples'])
    _, _, singlets, _, _ = trial.sector_and_geometry()
    orthogonal = np.linalg.qr(np.array(singlets, dtype=float))[0]
    transfer = np.einsum('ai,ib->ab', np.diagonal(embedding, axis1=1, axis2=2), orthogonal)
    samples = PchipInterpolator(np.r_[0., x, 5.], np.vstack([
        np.r_[SQRT6, 0., data[0, 2:]], data, paired.VACUUM]), axis=0)(grid)
    result = np.broadcast_to(vacuum, (len(grid), len(vacuum))).copy()
    result[:, 0] = samples[:, 0]
    result[:, 1] = samples[:, 1]
    result[:, 2:8] += (samples[:, 2:6] @ transfer.T)[:, 1:]
    matter = np.broadcast_to(matter0, (len(grid), 5, 2, 3)).copy().astype(float)
    u = samples[:, -1] / np.sqrt(2)
    matter[:, 0, 0, 2] = u
    matter[:, 3, 0, 2] = u
    result[:, 8:] = matter.reshape(-1, 30)
    return result


def minimize(residual, grid, state, boundary=None):
    # Quadratic elements with five Gauss points per element.
    nodes, weights = np.polynomial.legendre.leggauss(5)
    count = (len(grid) - 1) // 2
    position = np.tile((1 + nodes) / 2, count)
    left = np.repeat(np.arange(count), len(nodes))
    endpoints = 2 * left
    width = grid[endpoints+2] - grid[endpoints]
    radius = grid[endpoints] + position * width
    indices = endpoints[:, None] + np.arange(3)
    shape = np.column_stack([(1-position)*(1-2*position), 4*position*(1-position),
                             position*(2*position-1)])
    slope_shape = np.column_stack([4*position-3, 4-8*position, 4*position-1]) / width[:, None]
    quadrature = np.sqrt(np.tile(weights, count) * width / 2)
    dimension = state.shape[1]
    free = np.arange(state.size)[2:-dimension]
    if boundary is not None:
        center, tail_matrix = boundary
        free = np.r_[free, np.arange(state.size-dimension+1, state.size)]
        tail_jacobian = coo_matrix((tail_matrix.ravel(),
                                    (np.repeat(np.arange(dimension-1), dimension-1),
                                     np.tile(np.arange(state.size-dimension+1, state.size), dimension-1))),
                                   shape=(dimension-1, state.size)).tocsc()[:, free]
    kinetic = np.column_stack([np.ones_like(radius), np.broadcast_to(radius[:, None], (len(radius), dimension-1))])
    angular = np.sqrt(2)
    eye = np.eye(dimension)

    def local(fields, derivatives):
        k, h = fields[:, 0] / SQRT6, fields[:, 1]
        f = residual(fields)
        values = np.column_stack([np.sqrt(3) * (1-k**2) / radius, angular * k * h, radius[:, None] * f])
        if not derivatives:
            return values
        jacobian = np.zeros((len(radius), values.shape[1], dimension))
        jacobian[:, 0, 0] = -2 * np.sqrt(3) * k / (SQRT6 * radius)
        jacobian[:, 1, 0] = angular * h / SQRT6
        jacobian[:, 1, 1] = angular * k
        for j in range(1, dimension):
            # Real polynomial continued holomorphically for cancellation-free differentiation.
            jacobian[:, 2:, j] = radius[:, None] * residual(fields + 1e-24j * eye[j]).imag / 1e-24
        return values, jacobian

    def system(fields, derivatives=False):
        element = fields[indices]
        mid = np.einsum('ni,nij->nj', shape, element)
        slope = np.einsum('ni,nij->nj', slope_shape, element)
        result = local(mid, derivatives)
        tail = np.empty(0) if boundary is None else tail_matrix @ (fields[-1, 1:] - center)
        if not derivatives:
            bulk = (quadrature[:, None] * np.column_stack([kinetic*slope, result])).ravel()
            return np.r_[bulk, tail]
        values, jacobian = result
        values = quadrature[:, None] * np.column_stack([kinetic*slope, values])
        total_rows = values.shape[1]
        jacobian = np.pad(jacobian, ((0,0), (dimension,0), (0,0)))
        row = np.broadcast_to(np.arange(values.size).reshape(-1, total_rows, 1), jacobian.shape).ravel()
        entries, columns = [], []
        for node in range(3):
            block = jacobian * shape[:, node, None, None]
            block[:, np.arange(dimension), np.arange(dimension)] += kinetic * slope_shape[:, node, None]
            entries.append((block * quadrature[:, None, None]).ravel())
            columns.append(np.broadcast_to(dimension*indices[:, node, None, None] + np.arange(dimension),
                                           jacobian.shape).ravel())
        sparse = coo_matrix((np.concatenate(entries), (np.tile(row, 3), np.concatenate(columns))),
                            shape=(values.size, fields.size)).tocsc()
        sparse.eliminate_zeros()
        jacobian = sparse[:, free]
        if boundary is not None:
            jacobian = vstack([jacobian, tail_jacobian], format='csc')
        return np.r_[values.ravel(), tail], jacobian

    damping = 1e-3
    for iteration in range(140):
        values, jac = system(state, True)
        cost = values @ values
        force = jac.T @ values
        gram = jac.T @ jac
        scale = gram.diagonal()
        error = np.max(np.abs(force) / np.sqrt(scale))
        if iteration % 10 == 0:
            print(f'n={count} iteration={iteration} energy={4*np.pi*(cost+3/grid[-1]):.9f} residual={error:.3g}',
                  flush=True)
        if error < 2e-7:
            break
        for _ in range(14):
            delta = spsolve(gram + diags(damping*scale), -force)
            updated = state.copy()
            updated.flat[free] += delta
            test = system(updated)
            if test @ test < cost:
                state = updated
                damping = max(1e-10, damping/2)
                break
            damping *= 5
        else:
            raise RuntimeError(f'Neutral radial solve stalled at residual {error}')
    else:
        raise RuntimeError(f'Neutral radial solve exceeded iterations, residual {error}')
    extra = 0 if boundary is None else dimension-1
    tail_energy = 0. if not extra else 4*np.pi*np.sum(values[-extra:]**2)
    blocks = values[:len(values)-extra].reshape(len(radius), -1)**2
    gauge = 4*np.pi*(np.sum(blocks[:, [0, dimension]]) + 3/grid[-1])
    scalar = 4*np.pi*(np.sum(blocks[:, 1:dimension]) + np.sum(blocks[:, dimension+1]))
    potential = 4*np.pi*np.sum(blocks[:, dimension+2:])
    d_energy = 4*np.pi*np.sum(blocks[:, -16:])
    result = dict(energy=float(gauge+scalar+potential+tail_energy), iterations=iteration,
                       scaled_discrete_residual=float(error), elements=count,
                       gauge=float(gauge), scalar_gradient=float(scalar), potential=float(potential),
                       d_energy=float(d_energy), virial_defect=float(gauge-scalar-3*potential))
    if boundary is not None:
        result['linear_scalar_tail_energy'] = float(tail_energy)
    return state, result


def calculate():
    vacuum, embedding, matter0, residual, generators = model()
    records = []
    spline = None
    for count in (60, 100, 160):
        endpoints = np.r_[0., np.geomspace(1e-4, 5., count)]
        grid = np.empty(2*count+1)
        grid[::2] = endpoints
        grid[1::2] = (endpoints[:-1] + endpoints[1:]) / 2
        state = initial_profile(grid, vacuum, embedding, matter0) if spline is None else spline(grid)
        state[0, :2] = [SQRT6, 0.]
        state[-1] = vacuum
        state, result = minimize(residual, grid, state)
        spline = CubicSpline(grid, state, axis=0)
        radii = np.geomspace(.002, 4, 180)
        samples = spline(radii)
        currents = np.einsum('ngi,ni->ng', generators(samples), spline(radii, 1))
        result['max_r2_real_radial_current'] = float(np.max(np.abs(currents)*radii[:, None]**2))
        records.append(result)
        print(result, flush=True)
    probes = np.array([.002, .01, .02, .05, .1, .2, .4, .8, 1.6])
    assert records[-1]['energy'] < 574.219849
    assert abs(records[-1]['energy'] - records[-2]['energy']) < .12
    return dict(status='PASS', real_scalar_profiles=37, convergence=records, probe_radii=probes.tolist(),
                normalized_profile_samples=spline(probes).tolist(),
                matter_max_deviation=np.max(np.abs(spline(probes)[:,8:]-vacuum[8:]),axis=1).tolist())


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
