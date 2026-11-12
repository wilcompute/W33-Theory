"""Finite-element continuation of the complex W33 monopole."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve

import toe_20261111_monopole_phase_hessian as odd
import toe_20261113_monopole_adjoint_phase as phase
from toe_20261113_monopole_complex_response import MESH, OUT as RESPONSE


OUT = phase.ROOT / 'data/toe_20261113_monopole_nonlinear_phase.json'
SCALARS = 37
DIMENSION = 1 + 2*SCALARS


def write_checkpoint(output, result):
    staging = output.with_name(output.name+'.tmp')
    staging.write_text(json.dumps(result, separators=(',', ':'))+'\n', encoding='utf-8')
    staging.replace(output)


def unpack(state):
    return np.column_stack((state[:, 0], state[:, 1:38] + 1j*state[:, 38:]))


def d_components(internal, family):
    family = family - np.trace(family, axis1=1, axis2=2)[:, None, None]*np.eye(3)/3
    return np.column_stack((internal, family.reshape(len(family), 9))) / 2


def potential(model, angle, trace_vacuum):
    _, embedding, _, residual, _ = model
    z_shift = np.exp(1j*angle)-1
    plane = embedding[:, :2, :2]
    basis = np.eye(SCALARS)
    matter_basis = np.eye(6).reshape(6, 2, 3)
    dual = (1, 1, 1, -1, -1)

    def f_terms(fields):
        f = residual(fields, holomorphic_only=True)
        a = np.einsum('na,aij->nij', fields[:, 1:8], embedding)
        f[:, :7] += z_shift * phase.trace_f_residual(embedding, a, trace_vacuum)
        return f

    def local(state, radii, derivatives):
        fields = unpack(state)
        a = np.einsum('na,aij->nij', fields[:, 1:8], embedding)
        adjoint = a.conj().swapaxes(1, 2)
        matter = fields[:, 8:].reshape(-1, 5, 2, 3)
        x, z = matter[:, :3], matter[:, 3:]
        internal = np.einsum('aij,nij->na', embedding, a @ adjoint-adjoint @ a)
        internal += np.einsum('aij,nij->na', plane,
                              np.einsum('nkia,nkja->nij', x, x.conj())
                              - np.einsum('nkia,nkja->nij', z.conj(), z))
        family = (np.einsum('nkia,nkib->nab', x, x.conj())
                  - np.einsum('nkia,nkib->nab', z.conj(), z))
        f, d = f_terms(fields), d_components(internal, family)
        k, h = state[:, 0]/odd.core.SQRT6, fields[:, 1]
        angular = np.sqrt(2)*k*h
        values = np.column_stack((np.sqrt(3)*(1-k*k)/radii, angular.real, angular.imag,
                                  radii[:, None]*np.column_stack((f.real, f.imag, d.real, d.imag))))
        if not derivatives:
            return values

        jac = np.zeros((len(radii), values.shape[1], DIMENSION))
        jac[:, 0, 0] = -2*np.sqrt(3)*k / (odd.core.SQRT6*radii)
        jac[:, 1, 0], jac[:, 2, 0] = np.sqrt(2)*h.real/odd.core.SQRT6, np.sqrt(2)*h.imag/odd.core.SQRT6
        jac[:, 1, 1] = jac[:, 2, 38] = np.sqrt(2)*k
        holomorphic_step = 1e-5
        for j, direction in enumerate(basis):
            perturbation = np.r_[0., holomorphic_step*direction]
            df = (residual(fields+perturbation, holomorphic_only=True)
                  - residual(fields-perturbation, holomorphic_only=True))/(2*holomorphic_step)
            if j < 7:
                df[:, :7] += z_shift * np.einsum(
                    'aij,nji->na', embedding, phase.trace_derivative(a, embedding[j]))
            for part, coefficient in enumerate((1., 1j)):
                df_part = coefficient*df
                if j < 7:
                    delta = coefficient*embedding[j]
                    delta_adjoint = delta.conj().T
                    variation = delta @ adjoint-adjoint @ delta + a @ delta_adjoint-delta_adjoint @ a
                    dd = d_components(np.einsum('aij,nij->na', embedding, variation),
                                      np.zeros_like(family))
                else:
                    field, entry = divmod(j-7, 6)
                    displacement = matter_basis[entry]*coefficient
                    m = matter[:, field]
                    if dual[field] < 0:
                        m, displacement = m.conj(), displacement.conj()
                    dm = displacement @ m.conj().swapaxes(1, 2) + m @ displacement.conj().T
                    d_family = displacement.T @ m.conj() + m.swapaxes(1, 2) @ displacement.conj()
                    dd = d_components(dual[field]*np.einsum('aij,nij->na', plane, dm),
                                      dual[field]*d_family)
                jac[:, 3:, 1+j+part*SCALARS] = radii[:, None]*np.column_stack(
                    (df_part.real, df_part.imag, dd.real, dd.imag))
        return values, jac

    return local


def optimize(grid, start, model, angle, trace_vacuum, tolerance, verify_jacobian=False):
    indices, radii, shape, differential, quadrature = odd.real.quadratic_elements(grid)
    count, order = radii.shape
    local = potential(model, angle, trace_vacuum)
    radius = radii.ravel()
    kinetic = np.broadcast_to(radii[:, :, None]**2, (count, order, DIMENSION)).copy()
    kinetic[:, :, 0] = 1.
    columns = (DIMENSION*indices[:, :, None]+np.arange(DIMENSION)).reshape(count, -1)
    rows = np.broadcast_to(columns[:, :, None], (count, 3*DIMENSION, 3*DIMENSION)).ravel()
    cols = np.broadcast_to(columns[:, None, :], (count, 3*DIMENSION, 3*DIMENSION)).ravel()
    free = np.setdiff1d(np.arange(start.size-DIMENSION), [0, 1, 38])
    kinetic_block = np.einsum('cq,cqi,cqa,cqj->acij', quadrature, differential,
                              kinetic, differential, optimize=True)
    component = np.arange(DIMENSION)

    def sample(state):
        values = np.einsum('qi,cia->cqa', shape, state[indices])
        slopes = np.einsum('cqi,cia->cqa', differential, state[indices])
        return values.reshape(-1, DIMENSION), slopes

    def system(state, derivatives):
        values, slopes = sample(state)
        if derivatives:
            residual, jac = local(values, radius, True)
        else:
            residual = local(values, radius, False)
        cost = float(quadrature.ravel() @ np.sum(residual**2, axis=1)
                     + np.sum(quadrature[:, :, None]*kinetic*slopes**2))
        if not derivatives:
            return cost
        local_force = (jac.transpose(0, 2, 1) @ residual[..., None]).reshape(count, order, DIMENSION)
        element_force = (np.einsum('cq,qi,cqa->cia', quadrature, shape, local_force)
                         + np.einsum('cq,cqi,cqa,cqa->cia', quadrature, differential, kinetic, slopes))
        force = np.zeros_like(state)
        np.add.at(force, indices, element_force)
        metric = (jac.transpose(0, 2, 1) @ jac).reshape(count, order, DIMENSION, DIMENSION)
        block = np.einsum('cq,qi,cqab,qj->ciajb', quadrature, shape, metric, shape, optimize=True)
        block[:, :, component, :, component] += kinetic_block
        gram = coo_matrix((block.ravel(), (rows, cols)), shape=(state.size, state.size)).tocsc()
        return cost, force.ravel()[free], gram[free][:, free]

    if verify_jacobian:
        values, _ = sample(start)
        values = values[::29]
        probe = radius[::29]
        direction = np.random.default_rng(905).normal(size=values.shape)/np.sqrt(DIMENSION)
        _, jac = local(values, probe, True)
        epsilon = 1e-5
        difference = (local(values+epsilon*direction, probe, False)
                      - local(values-epsilon*direction, probe, False))/(2*epsilon)
        np.testing.assert_allclose(np.einsum('nki,ni->nk', jac, direction), difference,
                                   rtol=3e-6, atol=2e-7)

    state = start.copy()
    damping = 1e-6
    for iteration in range(65):
        cost, force, gram = system(state, True)
        scale = gram.diagonal()
        error = float(np.max(np.abs(force)/np.sqrt(scale)))
        if iteration % 10 == 0:
            print(f'phi={angle:.5f} iteration={iteration} residual={error:.4g}', flush=True)
        if error < tolerance:
            break
        for _ in range(12):
            updated = state.copy()
            updated.flat[free] += spsolve(gram+diags(damping*scale), -force)
            if system(updated, False) < cost:
                state = updated
                damping = max(1e-11, damping/2)
                break
            damping *= 5
        else:
            raise RuntimeError(f'Complex core descent stalled at {angle} with residual {error}')
    else:
        raise RuntimeError(f'Complex core iterations exceeded at {angle} with residual {error}')

    vacuum, embedding, _, residual, real_generators = model
    values, slopes = sample(state)
    fields = unpack(values)
    complex_slopes = unpack(slopes.reshape(-1, DIMENSION))
    adjoint = np.einsum('na,aij->nij', fields[:, 1:8], embedding)
    trace = phase.trace_f_residual(embedding, adjoint, trace_vacuum)
    independent_energy = odd.odd_local_energy(
        residual, embedding, fields, radius, (np.exp(1j*angle)-1)*trace)
    independent_energy += np.sum(kinetic.reshape(-1, DIMENSION)*slopes.reshape(-1, DIMENSION)**2, axis=1)
    np.testing.assert_allclose(cost, quadrature.ravel() @ independent_energy, atol=1e-9)
    imaginary_action = odd.imaginary_gauge_action(embedding)
    imag_tangents = 1j*imaginary_action(fields[:, 1:])
    real_tangents = real_generators(fields.real) + 1j*real_generators(fields.imag)
    current_real = np.einsum('nga,na->ng', real_tangents.conj(), complex_slopes).real
    current_imag = np.einsum('nag,na->ng', imag_tangents.conj(), complex_slopes[:, 1:]).real
    current = np.column_stack((current_real, current_imag))*radius[:, None]**2
    np.testing.assert_allclose(unpack(state[-1:])[0], vacuum, atol=1e-10)
    return state, dict(angle=angle, energy=float(4*np.pi*(cost+3/grid[-1])),
                       iterations=iteration, scaled_discrete_residual=error,
                       max_weighted_radial_current=float(np.max(np.abs(current))),
                       max_imaginary_scalar=float(np.max(np.abs(state[:, 38:]))))


def conjugation_predictor(base, history, angle):
    """Extrapolate even and odd profiles in the conjugation-compatible coordinates."""
    coefficients = []
    for row in history[-2:]:
        previous = row['angle']
        state = np.array(row['state'])
        coordinate = 1-np.cos(previous)
        coefficients.append((coordinate, (state[:, :38]-base)/coordinate,
                             state[:, 38:]/np.sin(previous)))
    coordinate, real, imaginary = coefficients[-1]
    target = 1-np.cos(angle)
    if len(coefficients) == 2:
        earlier, real_earlier, imaginary_earlier = coefficients[0]
        ratio = (target-coordinate)/(coordinate-earlier)
        if 0 < ratio < 2:
            real = real + ratio*(real-real_earlier)
            imaginary = imaginary + ratio*(imaginary-imaginary_earlier)
    return np.column_stack((base+target*real, np.sin(angle)*imaginary))


def continuation(mesh, response, elements, angles, output, tolerance, seed_branch=None,
                 resume=False, periodic_predictor=False):
    source, = [row for row in json.loads(mesh.read_text()) if row['count'] == elements]
    start, = [row for row in json.loads(response.read_text())['profiles'] if row['elements'] == elements]
    real = np.array(source['state'])
    grid = np.array(source['grid'])
    derivative = np.zeros((len(real), DIMENSION))
    derivative[:, 38:] = np.array(start['response_at_nodes'])[:, 1:]
    state = np.column_stack((real, np.zeros((len(real), SCALARS))))
    model = odd.core.model()
    trace_vacuum = phase.trace_gradient(np.diag(odd.core.geometry()[3]))
    rows = []
    previous = 0.
    if resume:
        checkpoint = json.loads(output.read_text(encoding='utf-8'))
        rows = checkpoint['profiles']
        assert checkpoint['elements'] == elements and checkpoint['grid'] == grid.tolist()
        assert [row['angle'] for row in rows] == angles[:len(rows)]
        if rows:
            last_state = np.array(rows[-1]['state'])
            previous = rows[-1]['angle']
            if len(rows) == 1:
                derivative = (last_state-state)/previous
            else:
                derivative = (last_state-np.array(rows[-2]['state']))/(previous-rows[-2]['angle'])
            state = last_state
    result = dict(elements=elements, grid=grid.tolist(), profiles=rows)
    seeds = None
    if seed_branch is not None:
        coarse = json.loads(seed_branch.read_text(encoding='utf-8'))
        seeds = {row['angle']: CubicSpline(coarse['grid'], row['state'], axis=0)(grid)
                 for row in coarse['profiles']}
    for angle in angles[len(rows):]:
        if seeds is not None:
            trial = seeds[angle]
        elif periodic_predictor and rows:
            trial = conjugation_predictor(real, rows, angle)
        else:
            trial = state + (angle-previous)*derivative
        trial[0, [0, 1, 38]] = state[0, [0, 1, 38]]
        trial[-1] = state[-1]
        update, record = optimize(grid, trial, model, angle, trace_vacuum, tolerance, not rows)
        derivative = (update-state)/(angle-previous)
        state, previous = update, angle
        rows.append(dict(**record, state=state.tolist()))
        write_checkpoint(output, result)
        print(record, flush=True)


def real_pi_endpoint(mesh, elements, output):
    source, = [row for row in json.loads(mesh.read_text()) if row['count'] == elements]
    grid = np.array(source['grid'])
    model = odd.core.model()
    _, embedding, _, residual, _ = model
    trace_vacuum = phase.trace_gradient(np.diag(odd.core.geometry()[3]))

    def shifted(fields):
        f = residual(fields)
        adjoint = np.einsum('na,aij->nij', fields[:, 1:8], embedding)
        f[:, :7] -= 2 * phase.trace_f_residual(embedding, adjoint, trace_vacuum)
        return f

    real, record = odd.core.minimize(shifted, grid, np.array(source['state']))
    state = np.column_stack((real, np.zeros((len(real), SCALARS))))
    row = dict(angle=np.pi, max_imaginary_scalar=0., **record, state=state.tolist())
    write_checkpoint(output, dict(elements=elements, grid=source['grid'], profiles=[row]))
    print(record, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, default=MESH)
    parser.add_argument('--response', type=Path, default=RESPONSE)
    parser.add_argument('--elements', type=int, default=60)
    parser.add_argument('--angles', type=float, nargs='+', default=[.05, .2, .45, .8, 1.2, 1.65, 2.1, 2.55, 2.9, np.pi])
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--seed-branch', type=Path, help='Use these coarse states as mesh-refinement seeds')
    parser.add_argument('--resume', action='store_true', help='Resume from the verified output prefix')
    parser.add_argument('--real-endpoint', action='store_true', help='Solve the conjugation-fixed pi endpoint')
    parser.add_argument('--periodic-predictor', action='store_true',
                        help='Use cosine and sine coordinates on the positive half-loop')
    parser.add_argument('--tolerance', type=float, default=3e-7)
    args = parser.parse_args()
    if not np.all(np.diff(np.r_[0., args.angles]) > 0):
        parser.error('angles must be increasing and positive')
    if args.periodic_predictor and args.angles[-1] > np.pi:
        parser.error('the periodic predictor is defined up to pi')
    if args.real_endpoint:
        if args.output.resolve() == OUT.resolve():
            parser.error('the real endpoint control needs a distinct output path')
        real_pi_endpoint(args.mesh, args.elements, args.output)
    else:
        continuation(args.mesh, args.response, args.elements, args.angles, args.output, args.tolerance,
                     args.seed_branch, args.resume, args.periodic_predictor)
