"""Vacuum mass spectrum and linear exterior for the real W33 radial core."""

import json

import numpy as np
from scipy.interpolate import PchipInterpolator

import toe_20261111_monopole_neutral_core as core

OUT = 'data/toe_20261111_monopole_neutral_tail.json'


def calculate():
    vacuum, _, _, residual, generators = core.model()
    directions = np.eye(len(vacuum))[1:]
    jacobian = np.column_stack([residual(vacuum[None] + 1e-24j*direction)[0].imag / 1e-24
                                for direction in directions])
    _, masses, right = np.linalg.svd(jacobian, full_matrices=False)
    gauge = masses < 1e-8
    assert gauge.sum() == 4
    np.testing.assert_allclose(jacobian @ generators(vacuum[None])[0, :, 1:].T, 0, atol=1e-9)
    masses[gauge] = 0

    previous = core.trial.flat.read(core.OUT)
    probes = np.array(previous['probe_radii'])
    fields = np.array(previous['normalized_profile_samples'])
    amplitude = (right @ (fields[-1, 1:] - vacuum[1:]))**2
    light = np.flatnonzero((masses > 0) & (masses < .03))
    assert len(light) == 4
    fraction = amplitude[light[0]] / amplitude.sum()
    assert fraction > .9

    start = PchipInterpolator(np.r_[0., probes, 5., 9.],
                             np.vstack([fields[0], fields, vacuum, vacuum]), axis=0)
    results = []
    for outer, count in [(5., 160), (9., 185)]:
        endpoints = np.r_[0., np.geomspace(1e-4, outer, count)]
        grid = np.empty(2*count+1)
        grid[::2] = endpoints
        grid[1::2] = (endpoints[:-1] + endpoints[1:]) / 2
        profile = start(grid)
        profile[0, :2] = [core.SQRT6, 0.]
        profile[-1, 0] = 0.
        # For a mode with mass m the exact linear exterior contributes
        # (R + m R^2) times the squared boundary amplitude to E/(4 pi).
        boundary = np.sqrt(outer + outer**2*masses)[:, None] * right
        profile, info = core.minimize(residual, grid, profile, (vacuum[1:], boundary))
        info['outer_radius'] = outer
        info['boundary_scalar_deviation_norm'] = float(np.linalg.norm(profile[-1, 1:] - vacuum[1:]))
        results.append(info)
        print(info, flush=True)
    return dict(status='PASS', linear_massless_gauge_directions=int(gauge.sum()),
                lightest_physical_radial_masses=sorted(masses[light].tolist()),
                prior_tail_fraction_in_0p0275_mode=float(fraction), linear_exterior=results)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (core.trial.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
