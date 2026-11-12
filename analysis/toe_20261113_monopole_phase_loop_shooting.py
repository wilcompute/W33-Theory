"""Match adjoint reflection on the nonlinear finite-radius monopole branch."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

import toe_20261113_monopole_adjoint_shooting as shooting
import toe_20261113_monopole_nonlinear_phase as nonlinear


OUT = shooting.phase.ROOT / 'data/toe_20261113_monopole_phase_loop_shooting.json'


def context():
    vacuum, sectors = shooting.phase.native_sectors()
    embedding = shooting.phase.neutral.geometry()[0]
    return embedding, [(weight, roots, shooting.coefficients(vacuum, roots))
                       for weight, roots in (sectors[0], sectors[-1])]


def scatter(grid, state, angle, inputs):
    embedding, sectors = inputs
    scalar, fine, matrices = shooting.interpolate_scalar(
        grid, nonlinear.unpack(np.array(state))[:, :8], embedding)
    rows = []
    for weight, roots, exterior in sectors:
        mass = CubicSpline(fine, np.array([shooting.coefficients(a, roots) for a in matrices]))

        def profile(radius):
            return scalar(radius)[0].real/shooting.phase.neutral.SQRT6, mass(radius)

        gap, reflection = shooting.match(profile, exterior, grid[-1], 1e-6, .14,
                                         np.exp(1j*angle), 1., 3e-9)
        assert abs(abs(reflection)-1) < 2e-7
        rows.append(dict(weight=weight.tolist(), matching_sigma_min=gap,
                         reflection=[reflection.real, reflection.imag]))
    return dict(angle=angle, sectors=rows)


def summarize(branch, samples):
    result = dict(elements=branch['elements'], samples=samples)
    angles = [row['angle'] for row in samples]
    if len(angles) < 2 or not np.isclose(angles[-1], np.pi, rtol=0, atol=1e-12):
        return result
    endpoint = branch['profiles'][-1]['max_imaginary_scalar']
    result['pi_endpoint_max_imaginary_scalar'] = endpoint
    if endpoint > 1e-4 or max(np.diff(angles)) > .7:
        return result
    # At zero use the established real reference phase. Reflecting a conjugate
    # core takes R to -conj(R) in the fixed left/right light basis.
    winding = []
    for index, reference in enumerate((-1j, 1j)):
        half = np.array([reference]+[complex(*row['sectors'][index]['reflection']) for row in samples])
        full = np.r_[half, -half[-2:0:-1].conj(), reference]
        changes = np.angle(full[1:]/full[:-1])
        adjusted = np.angle(half[1:]*np.exp(-1j*np.array(angles))/reference)
        winding.append(dict(weight=samples[0]['sectors'][index]['weight'],
                            sampled_winding=float(sum(changes)/(2*np.pi)),
                            max_sampled_step=float(max(abs(changes))),
                            max_sampled_phase_correction=float(max(abs(adjusted))),
                            pi_endpoint_reduced_reflection_sign=int(np.sign(
                                (half[-1]*np.exp(-1j*np.pi)/reference).real)),
                            minimum_sampled_matching_gap=min(
                                row['sectors'][index]['matching_sigma_min'] for row in samples)))
    result['conjugated_loop_summary'] = winding
    result['sampled_total_adjoint_winding'] = (2*winding[0]['sampled_winding']
                                                + winding[1]['sampled_winding'])
    return result


def calculate(path):
    branch = json.loads(path.read_text(encoding='utf-8'))
    grid = np.array(branch['grid'])
    inputs = context()
    rows = []
    for profile in branch['profiles']:
        row = scatter(grid, profile['state'], profile['angle'], inputs)
        rows.append(row)
        print(row, flush=True)
    return summarize(branch, rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch', type=Path, default=nonlinear.OUT)
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate(args.branch)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
