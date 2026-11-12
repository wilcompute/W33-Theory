"""Finite-radius zero-energy shooting for the 98-component triplet operator."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import expm

import toe_20261113_monopole_triplet_mass as triplet
import toe_20261113_monopole_adjoint_shooting as adjoint


OUT = triplet.flat.ROOT / 'data/toe_20261113_monopole_triplet_shooting.json'


def local_operators(count, inner):
    embedding, evaluators, vacuum = triplet.radial_model()
    source = json.loads(adjoint.MESH.read_text(encoding='utf-8'))[-1]
    fields = np.array(source['state'])
    origin_slopes = np.zeros(fields.shape[1])
    origin_slopes[1] = fields[1, 1]/source['grid'][1]
    profile = CubicSpline(source['grid'], fields, bc_type=((1, origin_slopes), 'not-a-knot'))
    outer = source['grid'][-1]
    middle = .14
    inner_grid = np.geomspace(inner, middle, count+1)
    outer_grid = np.geomspace(middle, outer, count+1)
    grid = np.r_[inner_grid, outer_grid[1:]]
    midpoints = np.sqrt(grid[:-1]*grid[1:])
    widths = np.log(grid[1:]/grid[:-1])
    data = []
    for radius, state in zip(midpoints, profile(midpoints)):
        a, matter = triplet.profile_fields(state, embedding)
        masses = tuple(evaluate(a, matter) for evaluate in evaluators)
        data.append((masses, state[0]/triplet.neutral.SQRT6, radius))
    return data, widths, tuple(evaluate(*vacuum) for evaluate in evaluators)


def exterior_spaces(exterior, phase, light=None):
    masses = [fixed+phase*change for fixed, change in exterior]
    flux, potential = triplet.radial_hamiltonian(*masses, 0.)
    generator = -1j * flux @ potential
    np.testing.assert_allclose(generator, generator.conj().T, atol=1e-12)
    values, vectors = np.linalg.eigh(generator)
    stable = vectors[:, values < -1e-8]
    assert stable.shape == (98, 45)
    if light is None:
        zero = vectors[:, abs(values) < 1e-8]
        velocities, basis = np.linalg.eigh(zero.conj().T @ flux @ zero)
        np.testing.assert_allclose(velocities, [-1]*4+[1]*4, atol=1e-12)
        light = zero @ basis
    np.testing.assert_allclose(generator @ light, 0., atol=1e-11)
    return flux, stable, light


def match(data, widths, exterior, phase, light):
    flux, stable, light = exterior_spaces(exterior, phase, light)
    zero_plus = np.zeros_like(exterior[0][0])
    _, angular = triplet.radial_hamiltonian(zero_plus, zero_plus, 1.)
    origin = -1j * flux @ angular
    assert np.array_equal(origin, np.diag(origin.diagonal()))
    regular = np.eye(98, dtype=complex)[:, origin.diagonal().real > 0]
    middle = len(data)//2

    def transfer(index, sign):
        masses, k, radius = data[index]
        local = [fixed+phase*change for fixed, change in masses]
        _, potential = triplet.radial_hamiltonian(*local, k/radius)
        return expm((-1j * flux @ potential)*(sign*widths[index]*radius))

    for index in range(middle):
        regular = np.linalg.qr(transfer(index, 1) @ regular)[0]
    for index in range(len(data)-1, middle-1, -1):
        matrix = transfer(index, -1)
        stable = np.linalg.qr(matrix @ stable)[0]
        light = matrix @ light
        light -= stable @ (stable.conj().T @ light)
    localized = np.column_stack((regular, -stable))
    gap = float(np.linalg.svd(localized, compute_uv=False)[-1])
    matching = np.column_stack((localized, -light[:, 4:]))
    reflection = np.linalg.solve(matching, light[:, :4])[-4:]
    error = float(np.linalg.norm(reflection.conj().T @ reflection-np.eye(4), ord=2))
    assert error < 1e-5
    return gap, reflection, error


def calculate(counts, angles, inner=1e-6):
    output = []
    for count in counts:
        data, widths, exterior = local_operators(count, inner)
        _, _, light = exterior_spaces(exterior, 1.)
        rows = []
        for angle in angles:
            gap, reflection, error = match(data, widths, exterior, np.exp(1j*angle), light)
            determinant = np.linalg.det(reflection)
            result = dict(angle=angle, matching_sigma_min=gap,
                          reflection_determinant=[determinant.real, determinant.imag],
                          reflection_unitarity_error=error)
            rows.append(result)
            print(dict(radial_cells=2*count, **result), flush=True)
        uniform_loop = np.linspace(0., 2*np.pi, len(angles), endpoint=False)
        if len(rows) > 4 and np.allclose(angles, uniform_loop, rtol=0, atol=1e-12):
            phases = np.array([complex(*row['reflection_determinant']) for row in rows])
            changes = np.angle(np.roll(phases, -1)/phases)
            sampled_winding = float(sum(changes)/(2*np.pi))
            maximum_increment = float(max(abs(changes)))
        else:
            sampled_winding = maximum_increment = None
        output.append(dict(radial_cells=2*count, phases=rows, sampled_winding=sampled_winding,
                           maximum_sampled_phase_increment=maximum_increment))
    return dict(status='PASS', scope='fixed real radius-five core with piecewise exponential transfer',
                origin_cutoff=inner,
                meshes=output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--counts', type=int, nargs='+', default=[60, 120])
    phase_grid = parser.add_mutually_exclusive_group()
    phase_grid.add_argument('--phase-count', type=int, default=1)
    phase_grid.add_argument('--angles', type=float, nargs='+')
    parser.add_argument('--inner', type=float, default=1e-6)
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    if min(args.counts) < 8 or args.phase_count < 1 or not 0 < args.inner < .14:
        parser.error('invalid radial or phase grid')
    phases = args.angles or np.linspace(0., 2*np.pi, args.phase_count, endpoint=False).tolist()
    result = calculate(args.counts, phases, args.inner)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
