"""Two-sided reference scattering for the native W33 adjoint doublets."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

import toe_20261113_monopole_adjoint_phase as phase


OUT = phase.ROOT / 'data/toe_20261113_monopole_adjoint_shooting.json'
MESH = phase.ROOT / 'data/toe_20261113_monopole_adjoint_shooting_mesh.json'
SIGMA1 = np.array([[0, 1], [1, 0]])
ANGULAR = np.kron(SIGMA1, np.eye(2))
FLUX = np.block([[-ANGULAR, np.zeros((4, 4))],
                 [np.zeros((4, 4)), ANGULAR]])
GAUGE = np.diag([1, -1])
GAUGE = 1j * np.kron(GAUGE, np.kron([[0, 1], [-1, 0]], np.eye(2)))
REAL_FORM = np.diag([1] * 4 + [1j] * 4)
REGULAR = np.eye(8, dtype=complex)[:, [0, 1, 4, 5]]
LIGHT_IN = np.array([0, 0, 0, 0, 0, 1, 0, -1], dtype=complex) / np.sqrt(2)
LIGHT_OUT = np.array([0, 1, 0, -1, 0, 0, 0, 0], dtype=complex) / np.sqrt(2)


def coefficients(a, roots):
    h, yl, yr = phase.mass_blocks(a, roots, roots.transpose(0, 2, 1))
    return np.array([[h[k, k], yl[k, k], yr[k, k]] for k in range(2)]) / 6


def potential(k_over_r, coeff, z, gauge_yukawa):
    masses = [np.array([[z * h, gauge_yukawa * yl], [gauge_yukawa * yr, 0]])
              for h, yl, yr in coeff]
    m = np.kron(np.eye(2), (masses[0] + masses[1]) / 2)
    m -= np.kron(SIGMA1, (masses[0] - masses[1]) / 2)
    return k_over_r * GAUGE + np.block([
        [np.zeros((4, 4)), m.conj().T], [m, np.zeros((4, 4))],
    ])


def move(generator, start, stop, basis, tolerance, light=None):
    """Short transfers with QR resets, preserving light vectors modulo the basis."""
    count = max(1, int(np.ceil(abs(stop - start) / .035)))
    nodes = np.linspace(start, stop, count + 1)
    dimension = basis.shape[1]
    columns = basis if light is None else np.column_stack((basis, light))
    shape = columns.shape
    for a, b in zip(nodes[:-1], nodes[1:]):
        def rhs(radius, vector):
            return (generator(radius) @ vector.reshape(shape)).ravel()

        result = solve_ivp(rhs, (a, b), columns.ravel(), method='DOP853',
                           rtol=tolerance, atol=tolerance / 30)
        assert result.success
        columns = result.y[:, -1].reshape(shape)
        basis = np.linalg.qr(columns[:, :dimension])[0]
        if light is None:
            columns = basis
        else:
            light = columns[:, dimension:]
            light = light - basis @ (basis.conj().T @ light)
            columns = np.column_stack((basis, light))
    return basis, light


def match(profile, asymptotic, outer, inner, middle, z, gauge_yukawa, tolerance):
    def generator(radius):
        k, coeff = profile(radius)
        return -1j * FLUX @ potential(k / radius, coeff, z, gauge_yukawa)

    if z == 1:
        real_form = REAL_FORM.conj().T @ generator(middle) @ REAL_FORM
        np.testing.assert_allclose(real_form.imag, 0., atol=1e-13)
    exterior = potential(0., asymptotic, z, gauge_yukawa)
    transfer = -1j * FLUX @ exterior
    np.testing.assert_allclose(transfer, transfer.conj().T, atol=1e-11)
    eigenvalues, eigenvectors = np.linalg.eigh(transfer)
    stable = eigenvectors[:, eigenvalues < -1e-8]
    assert stable.shape == (8, 3) and sum(abs(eigenvalues) < 1e-8) == 2
    light = np.column_stack((LIGHT_IN, LIGHT_OUT))
    np.testing.assert_allclose(transfer @ light, 0., atol=1e-11)
    regular, _ = move(generator, inner, middle, REGULAR, tolerance)
    stable, light = move(generator, outer, middle, stable, tolerance, light)
    for basis in (regular, stable):
        np.testing.assert_allclose(basis.conj().T @ FLUX @ basis, 0., atol=2e-6)
    np.testing.assert_allclose(stable.conj().T @ FLUX @ light, 0., atol=2e-6)
    np.testing.assert_allclose(light.conj().T @ FLUX @ light, np.diag([-1, 1]), atol=2e-6)
    localized = np.column_stack((regular, -stable))
    gap = np.linalg.svd(localized, compute_uv=False)[-1]
    overlap = np.linalg.norm(regular.conj().T @ stable, ord=2)
    np.testing.assert_allclose(gap**2, 1 - overlap, atol=1e-13)
    matching = np.column_stack((localized, -light[:, 1]))
    reflection = np.linalg.solve(matching, light[:, 0])[-1]
    return gap, reflection


def reference_profiles(mesh):
    neutral = phase.neutral
    embedding, _, _, y = neutral.geometry()
    if mesh is not None:
        return embedding, json.loads(mesh.read_text(encoding='utf-8'))
    frozen = phase.core.flat.read(neutral.OUT)
    states = np.array(frozen['normalized_profile_samples'])
    origin = states[0].copy()
    origin[:2] = [neutral.SQRT6, 0.]
    vacuum = origin.copy()
    vacuum[0] = 0
    vacuum[1:8] = np.einsum('aii,i->a', embedding, y)
    return embedding, [dict(count=0, grid=[0.] + frozen['probe_radii'] + [5.],
                            state=np.vstack((origin, states, vacuum)).tolist())]


def calculate(mesh):
    a0, sectors = phase.native_sectors()
    embedding, profiles = reference_profiles(mesh)
    rows = []
    for source in profiles:
        grid = np.array(source['grid'])
        state = np.array(source['state'])[:, :8]
        scalar = CubicSpline(grid, state, bc_type=((1, np.r_[0., np.diff(state[:2, 1])[0] / grid[1],
                                                                np.zeros(6)]), 'not-a-knot'))
        # Evaluate the polynomial mass on a refined mesh. The integration
        # samples a cubic interpolant of these values.
        fine = np.unique(np.r_[grid, np.geomspace(1e-6, grid[-1], 660)])
        dense = scalar(fine)
        matrices = np.einsum('na,aij->nij', dense[:, 1:8], embedding)
        for weight, roots in sectors:
            asymptotic = coefficients(a0, roots)
            mass = CubicSpline(fine, np.array([coefficients(a, roots) for a in matrices]))

            def profile(radius):
                return scalar(radius)[0] / phase.neutral.SQRT6, mass(radius)

            variants = []
            for middle, inner, tolerance, yukawa, angle in (
                (.14, 1e-5, 1e-8, 1., 0.),
                (.21, 1e-7, 3e-10, 1., 0.),
                (.14, 1e-5, 1e-8, 1., .71),
                (.14, 1e-5, 1e-8, np.sqrt(2), 0.),
            ):
                z = np.exp(1j * angle)
                gap, reflection = match(profile, asymptotic, grid[-1], inner, middle,
                                        z, yukawa, tolerance)
                assert abs(abs(reflection) - 1) < 2e-6
                if angle == 0.:
                    assert abs(reflection.real) < 2e-6
                assert gap > 1e-4
                variants.append(dict(matching_radius=middle, origin_cutoff=inner,
                                     gauge_yukawa=yukawa, phase=angle, matching_sigma_min=gap,
                                     reflection=[reflection.real, reflection.imag]))
            baseline, changed_radius, changed_phase, _ = variants
            r0 = complex(*baseline['reflection'])
            assert abs(complex(*changed_radius['reflection']) - r0) < 1e-4
            assert abs(complex(*changed_phase['reflection']) - np.exp(.71j) * r0) < 1e-6
            rows.append(dict(mesh=source['count'], weight=weight.tolist(), variants=variants))
    return dict(status='PASS', scope='numerical fixed real profile with vacuum exterior at radius 5',
                profiles='reconstructed finite-element mesh' if mesh else 'interpolated nine frozen samples',
                sectors=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--mesh', type=Path, default=MESH, help='JSON of converged scalar profile meshes')
    source.add_argument('--sampled', action='store_true', help='Print the nine-sample control')
    arguments = parser.parse_args()
    result = json.dumps(calculate(None if arguments.sampled else arguments.mesh), indent=2) + '\n'
    if not arguments.sampled:
        OUT.write_text(result, encoding='utf-8')
    print(result)
