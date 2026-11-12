"""Native adjoint radial mass blocks and the fixed-profile phase symmetry."""

import json
from pathlib import Path

import numpy as np

import toe_20261110_monopole_core_channels as core
import toe_20261111_monopole_neutral_core as neutral


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261113_monopole_adjoint_phase.json'


def trace_gradient(a):
    a2 = a @ a
    a4 = a2 @ a2
    return a4 @ a - 3 * a4 - 283 * a


def trace_derivative(a, variation):
    powers = [np.eye(len(a), dtype=a.dtype)]
    for _ in range(4):
        powers.append(powers[-1] @ a)
    return (-283 * variation
            - 3 * sum(powers[k] @ variation @ powers[3-k] for k in range(4))
            + sum(powers[k] @ variation @ powers[4-k] for k in range(5)))


def mass_blocks(a, left, right):
    holomorphic = np.array([[np.trace(x @ trace_derivative(a, y))
                             for y in right] for x in left])
    gauge_left = np.array([[np.trace(x @ (y @ a.T - a.T @ y))
                            for y in right] for x in left])
    gauge_right = np.array([[np.trace(y @ (x @ a.T - a.T @ x))
                             for y in right] for x in left])
    return holomorphic, gauge_left, gauge_right


def native_sectors():
    flat = core.flat
    _, adjoint, cartan, color, weak, y = flat.compact_chart()
    five = core.topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    step, magnetic = core.monopole_root(adjoint, five)
    weights = np.stack([(g @ g.T - g.T @ g).diagonal()
                        for g in (color[0], color[1], weak)] + [y], axis=1)
    alpha = weights[five[0]] - weights[five[3]]
    adjoint_weights = np.stack([flat.adjoint_charges(adjoint, h) for h in weights.T], axis=1)
    adjoint_flux = flat.adjoint_charges(adjoint, magnetic)
    ledger = flat.read('data/toe_20261113_monopole_grand_spin.json')
    sectors = []
    for entry in ledger['winding_charge_blocks']['adjoint']:
        q = np.array(entry['doubled_perpendicular_weight'])
        pair = []
        for flux in (1, -1):
            twice_weight = q + flux * alpha
            assert not np.any(twice_weight % 2)
            weight = twice_weight // 2
            for sign in (1, -1):
                assert not np.any(np.all(sign * weights == weight, axis=1))
            index, = np.flatnonzero(np.all(adjoint_weights == weight, axis=1))
            assert adjoint_flux[index] == flux
            pair.append(adjoint[index])
        left = np.array(pair)
        assert not left[:, :2, :].any() and not left[:, :, :2].any()
        assert np.array_equal(step.T @ left[0] - left[0] @ step.T, left[1]) or np.array_equal(
            step.T @ left[0] - left[0] @ step.T, -left[1])
        sectors.append((q, left))
    return np.diag(y), sectors


def calculate():
    a0, sectors = native_sectors()
    flat = core.flat
    _, adjoint, _, _, _, y = flat.compact_chart()
    embedding, _, _, _ = neutral.geometry()
    profile = flat.read(neutral.OUT)
    canonical_hessian = flat.sextic_adjoint_hessian(adjoint, y)
    np.testing.assert_array_equal(mass_blocks(a0, adjoint, adjoint)[0], canonical_hessian)
    rows = []
    for q, left in sectors:
        exact = mass_blocks(a0, left, left.transpose(0, 2, 1))
        assert np.all(np.array(exact) == np.array([np.diag(np.diag(m)) for m in exact]))
        assert exact[0][0, 0] != 0 and exact[0][1, 1] == 0
        assert exact[1][0, 0] == 0 and exact[1][1, 1] != 0
        assert np.array_equal(exact[1], -exact[2])
        norm = np.sum(left * left, axis=(1, 2))
        assert list(norm) == [6, 6]
        samples = []
        for radius, state in zip(profile['probe_radii'], profile['normalized_profile_samples']):
            a = np.einsum('a,aij->ij', np.array(state[1:8]), embedding)
            h, yl, yr = mass_blocks(a, left, left.transpose(0, 2, 1))
            for i, direction in enumerate(left.transpose(0, 2, 1)):
                derivative = trace_gradient(a + 1e-24j * direction).imag / 1e-24
                np.testing.assert_allclose(h[:, i], np.einsum('aji,ij->a', left, derivative),
                                           atol=1e-9)
            matrices = np.array([h, yl, yr])
            assert np.max(np.abs(matrices - np.array([np.diag(np.diag(m)) for m in matrices]))) < 1e-7
            # Two flavor entries in each flux slot, in chiral, gaugino order.
            # The gauge overall coupling and constant convention phase are omitted.
            t = np.diag(np.exp(0.37j * np.array([1, -1])))
            for k in range(2):
                block = np.array([[h[k, k], yl[k, k]], [yr[k, k], 0]])
                phased = block.astype(complex)
                phased[0, 0] *= np.exp(0.74j)
                np.testing.assert_allclose(t @ block @ t, phased, atol=1e-9)
            samples.append(dict(radius=radius, trace_hessian_diagonal=np.diag(h).tolist(),
                                gauge_commutator_diagonal=np.diag(yl).tolist()))
        rows.append(dict(doubled_perpendicular_weight=q.tolist(),
                         vacuum_integer_trace_hessian=exact[0].tolist(),
                         vacuum_integer_gauge_commutator=exact[1].tolist(),
                         generator_trace_norm_squared=norm.tolist(), samples=samples))

    overlaps = []
    matter_phase_sources = []
    odd_scalar_sources = []
    ward_errors = []
    trace_at_vacuum = trace_gradient(a0)
    for state in profile['normalized_profile_samples']:
        a = np.einsum('a,aij->ij', np.array(state[1:8]), embedding)
        matter = np.array(state[8:]).reshape(5, 2, 3)
        plane = embedding[:, :2, :2]

        def mixed_residual(fields):
            source = sum(fields[3+j] @ fields[k].T for j, k in neutral.trial.MIXED)
            return np.einsum('aij,ij->a', plane, source)

        def trace_residual(adjoint_field):
            return np.einsum('aij,ji->a', embedding,
                             trace_gradient(adjoint_field)-trace_at_vacuum)

        mixed = mixed_residual(matter)
        trace = trace_residual(a)
        overlaps.append(float(np.dot(mixed, trace)))
        trace_plane = np.einsum('a,aij->ij', trace, plane)
        source = np.zeros_like(matter)
        for j, k in neutral.trial.MIXED:
            source[k] += 2 * trace_plane.T @ matter[3+j]
            source[3+j] += 2 * trace_plane @ matter[k]
        magnitude = np.linalg.norm(source)
        matter_phase_sources.append(float(magnitude))
        source_adjoint = -2 * np.array([np.dot(mixed, np.einsum(
            'aij,ji->a', embedding, trace_derivative(a, direction)))
            for direction in embedding])
        scalar_source = np.r_[source_adjoint, source.ravel()]
        total_norm = np.linalg.norm(scalar_source)
        odd_scalar_sources.append(scalar_source.tolist())
        if total_norm > 1e-6:
            z = np.exp(.4j)
            step = 1e-5j / total_norm
            delta_a = step * np.einsum('a,aij->ij', source_adjoint, embedding)
            delta_matter = step * source
            plus = np.linalg.norm(mixed_residual(matter + delta_matter)
                                  + z * trace_residual(a + delta_a))**2
            minus = np.linalg.norm(mixed_residual(matter - delta_matter)
                                   + z * trace_residual(a - delta_a))**2
            np.testing.assert_allclose((plus-minus) / 2e-5, z.imag * total_norm, atol=1e-7)
        dual_sign = np.array([1, 1, 1, -1, -1])[:, None, None]
        ward = []
        for direction in embedding[1:]:
            generator = (direction + direction.T) / 2
            tangent_a = np.einsum('aij,ij->a', embedding, generator @ a-a @ generator)
            tangent_matter = dual_sign * (generator[:2, :2] @ matter)
            ward.append(source_adjoint @ tangent_a + np.sum(source * tangent_matter))
        for i in range(3):
            for j in range(i, 3):
                generator = np.zeros((3, 3))
                generator[i, j] = generator[j, i] = 1
                ward.append(np.sum(source * dual_sign * (matter @ generator)))
        ward_error = max(map(abs, ward))
        assert ward_error < 1e-8
        ward_errors.append(float(ward_error))
    assert max(map(abs, overlaps)) > 1e-6
    assert max(matter_phase_sources) > 1e-6
    return dict(status='PASS', blocks=rows, radial_mass_phase='M(z)=diag(t,1/t) M(1) diag(t,1/t), t^2=z',
                sampled_bosonic_trace_mixed_F_interference=overlaps,
                sampled_imaginary_matter_force_norm_divided_by_sin_phase=matter_phase_sources,
                sampled_odd_scalar_force_divided_by_sin_phase=odd_scalar_sources,
                sampled_odd_force_gauge_ward_max_error=ward_errors,
                scope='canonical two-dual real hedgehog, fixed background, no soft gaugino masses')


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    OUT.write_text(result, encoding='utf-8')
    print(result)
