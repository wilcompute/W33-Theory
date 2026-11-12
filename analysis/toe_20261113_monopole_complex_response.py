"""Linearized complex stationary monopole response to the adjoint phase."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import null_space
from scipy.sparse import bmat, csc_matrix, diags
from scipy.sparse.linalg import spsolve

import toe_20261111_monopole_phase_hessian as odd
import toe_20261113_monopole_adjoint_phase as phase


OUT = phase.ROOT / 'data/toe_20261113_monopole_complex_response.json'
MESH = phase.ROOT / 'data/toe_20261113_monopole_adjoint_shooting_mesh.json'


def adjoint_field(embedding, fields):
    return np.einsum('...a,aij->...ij', fields[..., 1:8], embedding)


def peak_meson_trace_slopes(fields, eta):
    matter = fields[:, 8:].reshape(-1, 5, 2, 3)
    tangent = eta[:, 8:].reshape(-1, 5, 2, 3)
    slopes = (np.einsum('nzia,nxia->nzx', matter[:, 3:], tangent[:, :3])
              + np.einsum('nzia,nxia->nzx', tangent[:, 3:], matter[:, :3]))
    return np.max(np.abs(slopes), axis=0).tolist()


def solve(source, model, step):
    vacuum, embedding, _, residual, _ = model
    grid = np.array(source['grid'])
    fields = np.array(source['state'])
    assert fields.shape == (len(grid), 38)
    assert np.linalg.norm(fields[-1] - vacuum) < 1e-10
    indices, radii, shape, differential, quadrature = odd.real.quadratic_elements(grid)
    values = np.einsum('qi,cia->cqa', shape, fields[indices])
    slopes = np.einsum('cqi,cia->cqa', differential, fields[indices])
    weights = quadrature * radii**2
    _, _, _, y = odd.core.geometry()
    reference_trace = phase.trace_gradient(np.diag(y))
    matter = values[..., 8:].reshape(radii.shape + (5, 2, 3))
    source_a, source_m, overlap = phase.odd_force(
        embedding, adjoint_field(embedding, values), matter, reference_trace)
    forcing = np.concatenate((np.zeros_like(values[..., :1]), source_a,
                              source_m.reshape(radii.shape + (30,))), axis=-1)
    load = np.zeros_like(fields)
    np.add.at(load, indices, np.einsum('cq,qi,cqa->cia', weights, shape, forcing))

    action = odd.imaginary_gauge_action(embedding)
    tangent_values = action(values[..., 1:])
    np.testing.assert_allclose(np.einsum('...ag,...a->...g', tangent_values, forcing[..., 1:]),
                               0., atol=1e-8)
    gauge_stabilizer = null_space(action(vacuum[1:]), rcond=1e-10)
    assert gauge_stabilizer.shape == (10, 2)
    gauge_tangents = action(fields[:, 1:]) @ gauge_stabilizer
    gauge_tangents = np.pad(gauge_tangents, ((0, 0), (1, 0), (0, 0)))

    form, _ = odd.phase_form(embedding)
    stiffness, norm = odd.real.assemble(residual, grid, fields, None, step, form)
    free = np.arange(fields.size)[2:-fields.shape[1]]
    source_vector = load.ravel()[free]
    gauge_vectors = gauge_tangents.reshape(fields.size, 2)[free]
    gauge_gram = gauge_vectors.T @ norm @ gauge_vectors
    g_values, g_basis = np.linalg.eigh(gauge_gram)
    active = g_values > 1e-16
    gauge_vectors = (gauge_vectors @ g_basis[:, active]) / np.sqrt(g_values[active])
    constraint = norm @ gauge_vectors
    scale = diags(1 / np.sqrt(norm.diagonal()))
    scaled_force = scale @ source_vector
    if np.any(active):
        scaled_constraint = csc_matrix(scale @ constraint)
        system = bmat([[scale @ stiffness @ scale, scaled_constraint],
                       [scaled_constraint.T, None]], format='csc')
        solution = spsolve(system, np.r_[-scaled_force/2, np.zeros(active.sum())])
        response = scale @ solution[:len(free)]
        multipliers = solution[len(free):]
    else:
        response = scale @ spsolve(scale @ stiffness @ scale, -scaled_force/2)
        multipliers = np.empty(0)
    stationarity = stiffness @ response + source_vector/2 + constraint @ multipliers
    residual_relative = np.linalg.norm(scale @ stationarity) / np.linalg.norm(scaled_force)
    assert residual_relative < 1e-8
    np.testing.assert_allclose(constraint.T @ response, 0., atol=1e-9)
    eta = np.zeros(fields.size)
    eta[free] = response
    eta = eta.reshape(fields.shape)
    assert np.max(np.abs(eta[:, 0])) < 1e-10
    local_eta = np.einsum('qi,cia->cqa', shape, eta[indices])
    slope_eta = np.einsum('cqi,cia->cqa', differential, eta[indices])
    currents = np.einsum('...ag,...a->...g', tangent_values, slope_eta[..., 1:])
    currents -= np.einsum('...ag,...a->...g', action(local_eta[..., 1:]), slopes[..., 1:])
    max_current = float(np.max(np.abs(currents) * radii[..., None]**2))
    frozen = float(-2 * np.sum(weights * overlap))
    relaxation = float(source_vector @ response)

    def energy(angle, response_scale):
        field = (values + 1j * angle * response_scale * local_eta).reshape(-1, 38)
        slope = slopes + 1j * angle * response_scale * slope_eta
        trace = phase.trace_f_residual(embedding, adjoint_field(embedding, field), reference_trace)
        local = odd.odd_local_energy(residual, embedding, field, radii.ravel(),
                                     (np.exp(1j*angle)-1) * trace).reshape(radii.shape)
        kinetic = np.sum(np.abs(slope[..., 1:])**2, axis=-1) * radii**2
        kinetic += np.abs(slope[..., 0])**2
        return float(np.sum(quadrature * (local + kinetic)))

    base = energy(0., 0.)
    np.testing.assert_allclose(4*np.pi*(base+3/grid[-1]), source['record']['energy'], atol=2e-8)
    differences = []
    for angle in (.002, .001):
        curves = [(energy(angle, t) + energy(-angle, t) - 2*base)/angle**2 for t in (0, 1)]
        np.testing.assert_allclose(curves, [frozen, frozen+relaxation], rtol=2e-3, atol=2e-5)
        differences.append(dict(angle=angle, frozen=4*np.pi*curves[0], relaxed=4*np.pi*curves[1]))
    return dict(
        elements=source['count'], difference_step=step,
        active_vacuum_stabilizer_directions=int(active.sum()),
        stabilizer_gram_eigenvalues=g_values.tolist(),
        gauge_multiplier_norm=float(np.linalg.norm(multipliers)),
        relative_linear_residual=float(residual_relative),
        maximum_weighted_odd_radial_current=max_current,
        frozen_energy_curvature=4*np.pi*frozen,
        scalar_relaxation_curvature=4*np.pi*relaxation,
        relaxed_energy_curvature=4*np.pi*(frozen+relaxation),
        energy_finite_differences=differences,
        peak_adjoint_response=float(np.max(np.linalg.norm(eta[:, 1:8], axis=1))),
        peak_matter_response=float(np.max(np.linalg.norm(eta[:, 8:], axis=1))),
        peak_invariant_meson_trace_slope=peak_meson_trace_slopes(fields, eta),
        response_at_nodes=eta.tolist(),
    )


def calculate(mesh, sizes):
    model = odd.core.model()
    profiles = json.loads(mesh.read_text(encoding='utf-8'))
    rows = []
    for source in profiles:
        if source['count'] in sizes:
            result = solve(source, model, 5e-4)
            print({k: v for k, v in result.items() if k != 'response_at_nodes'}, flush=True)
            rows.append(result)
    assert len(rows) == len(sizes)
    return dict(status='PASS', scope='first-order response of the finite-radius stationary branch',
                profiles=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, default=MESH)
    parser.add_argument('--sizes', type=int, nargs='+', default=[60, 100, 160])
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    result = json.dumps(calculate(args.mesh, args.sizes), separators=(',', ':')) + '\n'
    args.output.write_text(result, encoding='utf-8')
