"""Imaginary radial fluctuations about the real W33 monopole."""

import json

import numpy as np
from scipy.interpolate import PchipInterpolator

import toe_20261111_monopole_radial_hessian as real

core = real.core
OUT = 'data/toe_20261111_monopole_phase_hessian.json'


def phase_form(embedding):
    """Build the conjugation-odd half Hessian in the real kinetic coordinates."""
    # The real chart uses the same Frobenius inner product on Hermitian moments.
    neutral = embedding[:, :2, :2]
    swap = lambda a: np.swapaxes(a, -1, -2)
    pairs = embedding @ swap(embedding[:, None]) - swap(embedding[:, None]) @ embedding
    commutator_gram = (pairs + pairs.swapaxes(0, 1)) / 2

    def d_jacobian(state):
        adj = np.einsum('na,aij->nij', state[:, 1:8], embedding)
        d_a = (embedding[None] @ swap(adj[:, None]) - swap(adj[:, None]) @ embedding[None]
               - adj[:, None] @ swap(embedding[None]) + swap(embedding[None]) @ adj[:, None])
        jac = np.zeros((len(state), 16, state.shape[1]))
        jac[:, :7, 1:8] = np.einsum('naij,bij->nba', d_a, embedding) / 2
        matter = state[:, 8:].reshape(-1, 5, 2, 3)
        for a in range(2):
            for b in range(3):
                variation = np.zeros((2, 3))
                variation[a, b] = 1
                internal = variation @ swap(matter)
                family = variation.T @ matter
                jac[:, :7, 8+3*a+b::6] = np.einsum(
                    'ntij,kij->nkt', internal-swap(internal), neutral) / 2
                jac[:, 7:, 8+3*a+b::6] = (family-swap(family)).reshape(-1, 5, 9).transpose(0, 2, 1)/2
        return jac

    def form(residual, state, radius, step):
        f = lambda values: residual(values)[:, :37]
        result = real.potential_half_hessian(f, state, step, curvature_sign=-1)
        jac = d_jacobian(state)
        result += jac.transpose(0, 2, 1) @ jac
        base = residual(state)
        internal = np.einsum('na,aij->nij', base[:, 37:44], embedding)
        family = base[:, 44:].reshape(-1, 3, 3)
        # D is stored divided by two. This contraction includes the factor
        # of two between the quadratic moment and the energy coefficient.
        result[:, 1:8, 1:8] += np.einsum('nij,abij->nab', internal, commutator_gram)
        block = (np.einsum('nij,ab->niajb', internal[:, :2, :2], np.eye(3))
                 + np.einsum('ij,nab->niajb', np.eye(2), family)).reshape(-1, 6, 6)
        for field in range(5):
            index = slice(8+6*field, 14+6*field)
            result[:, index, index] += block if field < 3 else -block

        result *= radius[:, None, None]**2
        k, h = state[:, 0]/core.SQRT6, state[:, 1]
        result[:, 0, 0] = (k*k-1)/radius**2 + h*h/3
        result[:, 1, 1] += 2*k*k
        return result

    return form, d_jacobian


def vacuum_gauge_tangents(embedding, vacuum):
    """Compact imaginary generators on the seven adjoint and thirty matter slots."""

    symmetric = ((embedding[1:] + embedding[1:].transpose(0, 2, 1))/2).reshape(6, -1)
    _, values, right = np.linalg.svd(symmetric, full_matrices=False)
    assert sum(values > 1e-10) == 5
    internal = right[values > 1e-10].reshape(5, 27, 27)
    adj = np.einsum('a,aij->ij', vacuum[1:8], embedding)
    matter = vacuum[8:].reshape(5, 2, 3)
    dual_sign = np.array([1, 1, 1, -1, -1])[:, None, None]
    tangents = []
    for generator in internal:
        adjoint = np.einsum('aij,ij->a', embedding, generator@adj-adj@generator)
        variations = dual_sign * (generator[:2, :2] @ matter)
        tangents.append(np.r_[adjoint, variations.ravel()])
    family = [np.diag([1., -1., 0.]), np.diag([0., 1., -1.])]
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        symmetric = np.zeros((3, 3))
        symmetric[i, j] = symmetric[j, i] = 1
        family.append(symmetric)
    for generator in family:
        tangents.append(np.r_[np.zeros(7), (dual_sign*(matter @ generator)).ravel()])
    tangents = np.asarray(tangents).T
    assert np.linalg.matrix_rank(tangents) == 8
    return tangents


def verify_local_form(residual, form, embedding, points, radii):
    def energy(state):
        a = np.einsum('na,aij->nij', state[:, 1:8], embedding)
        matter = state[:, 8:].reshape(-1, 5, 2, 3)
        x, z = matter[:, :3], matter[:, 3:]
        adjoint = a.conj().transpose(0, 2, 1)
        moment = a @ adjoint-adjoint @ a
        moment[:, :2, :2] += np.einsum('nkia,nkja->nij', x, x.conj())
        moment[:, :2, :2] -= np.einsum('nkia,nkja->nij', z.conj(), z)
        d_e = np.einsum('nij,aij->na', moment, embedding)
        d_f = np.einsum('nkia,nkib->nab', x, x.conj()) - np.einsum('nkia,nkib->nab', z.conj(), z)
        d_f -= np.trace(d_f, axis1=1, axis2=2)[:, None, None]*np.eye(3)/3
        k = np.abs(state[:, 0]/core.SQRT6)**2
        return (radii**2 * (np.sum(np.abs(residual(state)[:, :37])**2, axis=1)
                            + np.sum(np.abs(d_e)**2, axis=1)/4
                            + np.sum(np.abs(d_f)**2, axis=(1, 2))/4)
                + 3*(1-k)**2/radii**2 + 2*k*np.abs(state[:, 1])**2)

    base = energy(points)
    hessian = form(residual, points, radii, 5e-4)
    for seed in range(3):
        direction = np.random.default_rng(seed).normal(size=points.shape)
        direction /= np.linalg.norm(direction, axis=1)[:, None]
        predicted = np.einsum('ni,nij,nj->n', direction, hessian, direction)
        step = 1e-4
        numeric = (energy(points+1j*step*direction)-base)/step**2
        np.testing.assert_allclose(predicted, numeric, rtol=4e-6, atol=4e-5)


def calculate():
    vacuum, embedding, _, residual, _ = core.model()
    reference = core.trial.flat.read(core.OUT)
    probes = np.array(reference['probe_radii'])
    fields = np.array(reference['normalized_profile_samples'])
    start = PchipInterpolator(np.r_[0., probes, 5., 9.],
                             np.vstack([fields[0], fields, vacuum, vacuum]), axis=0)
    form, d_jacobian = phase_form(embedding)
    verify_local_form(residual, form, embedding, fields[3:6], probes[3:6])
    jac = np.column_stack([residual(vacuum[None]+1e-24j*d)[0].imag/1e-24
                           for d in np.eye(len(vacuum))[1:]])
    phase_jac = np.vstack([jac[:37], d_jacobian(vacuum[None])[0, :, 1:]])
    tangents = vacuum_gauge_tangents(embedding, vacuum)
    np.testing.assert_allclose(phase_jac @ tangents, 0, atol=2e-9)
    _, masses, right = np.linalg.svd(phase_jac, full_matrices=False)
    _, real_masses, real_right = np.linalg.svd(jac, full_matrices=False)
    null = masses < 1e-8
    assert sum(null) == 8
    assert np.linalg.matrix_rank(jac[:37], tol=1e-8) == 25
    masses[null] = 0
    real_masses[real_masses < 1e-8] = 0

    results = []
    for outer, count in [(5., 55), (9., 70)]:
        ends = np.r_[0., np.geomspace(1e-4, outer, count)]
        grid = np.empty(2*count+1)
        grid[::2], grid[1::2] = ends, (ends[:-1]+ends[1:])/2
        state = start(grid)
        state[0, :2], state[-1, 0] = [core.SQRT6, 0.], 0.
        real_boundary = np.sqrt(outer + outer**2*real_masses)[:, None]*real_right
        state, background = core.minimize(residual, grid, state, (vacuum[1:], real_boundary))
        boundary = np.sqrt(outer + outer**2*masses)[:, None]*right
        spectra = []
        for step in (1e-3, 5e-4):
            stiffness, norm = real.assemble(residual, grid, state, boundary, step, form)
            spectra.append(dict(step=step, **real.bottom(stiffness, norm)))
            print('Phase Hessian', outer, spectra[-1], flush=True)
        results.append(dict(outer_radius=outer, background=background, spectra=spectra))
    return dict(status='PASS', odd_vacuum_gauge_nullity=int(sum(null)),
                physical_odd_vacuum_masses=sorted(masses[~null].tolist()),
                static_phase_results=results)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (core.trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
