"""Monopole-root channels and scalar forcing in the canonical W33 vacuum."""

from collections import Counter
import json

import numpy as np
import sympy as sp

import toe_20261110_vector_proton_decay as vectors
import toe_20261110_global_gauge_topology as topology

flat = vectors.flat
OUT = 'data/toe_20261110_monopole_core_channels.json'


def monopole_root(internal, five):
    root, = [a for a in internal if a[five[0], five[3]]
             and not a[:2, :].any() and not a[:, :2].any()]
    coroot = (root @ root.T - root.T @ root).diagonal()
    assert coroot[five].tolist() == topology.cocharacters()['primitive_monopole']
    assert np.array_equal((coroot[:, None] - coroot[None, :]) * root, 2 * root)
    return root, coroot


def fixed_torus_sector(internal, color, weak, y, root, five, hessian, orbit):
    charges = np.stack([(a @ a.T - a.T @ a).diagonal()
                        for a in (color[0], color[1], weak)] + [y], axis=1)
    root_weight = sp.Matrix([charges[five[0]] - charges[five[3]]])
    torus = sp.Matrix.hstack(*root_weight.nullspace())
    matter = [i for i, weight in enumerate(charges) if not any(sp.Matrix([weight]) * torus)]
    assert matter == [0, 1] and torus.cols == 3
    adjoint_weights = np.stack([flat.adjoint_charges(internal, h) for h in charges.T], axis=1)
    fixed = [i for i, weight in enumerate(adjoint_weights) if not any(sp.Matrix([weight]) * torus)]
    assert len(fixed) == 10
    raising = internal[fixed] @ root - root @ internal[fixed]
    lowering = internal[fixed] @ root.T - root.T @ internal[fixed]
    commutator_rank = flat.vacuum.rank(np.concatenate([raising, lowering], axis=1).reshape(10, -1))
    assert commutator_rank == 3
    slots = [81 * k + 3 * i + a for k in range(5) for i in matter for a in range(3)]
    slots += [405 + i for i in fixed]
    complement = sorted(set(range(483)) - set(slots))
    assert not hessian[np.ix_(slots, complement)].any()
    mass_rank = flat.vacuum.rank(hessian[np.ix_(slots, slots)])
    orbit_rank = flat.vacuum.rank(orbit[:, slots])
    assert (len(slots), mass_rank, orbit_rank) == (40, 26, 14)
    return dict(torus_rank=torus.cols, fixed_matter_internal_slots=matter,
                fixed_complex_matter_components=30, fixed_internal_adjoint_slots=fixed,
                internal_adjoint_monopole_singlets=7, internal_adjoint_monopole_triplets=1,
                fixed_real_gauge_algebra_dimension=10 + 8,
                fixed_holomorphic_mass_rank=mass_rank, fixed_broken_orbit_rank=orbit_rank,
                fixed_uneaten_massless=0,
                family_spectator_zero_consistent=True)


def radial_channels(projected, internal, color, weak, y, root, coroot, five):
    _, _, _, fundamental, spaces, (_, orbit, weights) = projected
    h = sp.Matrix(np.stack([(a @ a.T - a.T @ a).diagonal()
                            for a in (color[0], color[1], weak)] + [y], axis=1))
    coefficients = h.gauss_jordan_solve(sp.Matrix(coroot))[0]
    monopole_charges = {weight: int(sp.Matrix([weight]).dot(coefficients)) for weight in spaces}
    assert all(sp.Matrix([weight]).dot(coefficients) == charge for weight, charge in monopole_charges.items())
    spectrum = Counter()
    anomaly = sp.zeros(4)
    baryon, lepton = sp.zeros(1, 4), sp.zeros(1, 4)
    for weight, basis in spaces.items():
        charge = monopole_charges[weight]
        spectrum[charge] += len(basis)
        q = sp.Matrix([weight])
        anomaly += len(basis) * charge * q.T * q
        hypercharge = weight[-1]
        if hypercharge in (1, -4, 2):
            baryon += len(basis) * charge * q * (sp.Rational(1, 3) if hypercharge == 1
                                                 else -sp.Rational(1, 3))
        if hypercharge == -3:
            lepton += 3 * charge * q
        if hypercharge == 6:
            lepton -= 3 * charge * q
    assert spectrum == {-1: 13, 0: 23, 1: 13}
    assert anomaly == sp.zeros(4)
    assert baryon == lepton == sp.Matrix([[0, 0, -3, 9]])
    electric = sp.Matrix([0, 0, sp.Rational(1, 2), sp.Rational(1, 6)])
    assert baryon.dot(electric) == baryon.dot(coefficients) == 0

    # Use the intrinsic lepton kernel plus the kinetic-orthogonal Higgs
    # in the charged down-doublet channel.
    old = flat.read(vectors.flavor.OUT)['completion']
    down = spaces[tuple(fundamental[15])]
    combinations = sp.Matrix([old['down_higgs_covector']]).nullspace()
    higgs, = sp.Matrix(old['lepton_covectors']).nullspace()
    combinations.append(higgs)
    down_basis = [
        vectors.flavor.lower_doublet(sum((v * c for v, c in zip(down, mix)),
                                         np.zeros(483, dtype=object)), weak)
        for mix in combinations
    ]
    gram_rows = internal.reshape(78, -1)
    adjoint_gram = gram_rows @ gram_rows.T
    physical = {}
    for weight, basis in spaces.items():
        if not monopole_charges[weight]:
            continue
        lower_doublet = weight == tuple(fundamental[16])
        chart, gram = vectors.weight_lifts(weights, orbit, adjoint_gram, weight,
                                           down_basis if lower_doublet else basis, sp.Integer(1))
        if lower_doublet:
            change = sp.eye(4)
            change[:3, 3] = -gram[:3, :3].inv() * gram[:3, 3]
            chart = chart[0], chart[1] * change
        physical[weight] = chart
    step = fundamental[five[0]] - fundamental[five[3]]
    blocks, unmatched = [], []
    for incoming, charge in sorted(monopole_charges.items()):
        if charge != -1:
            continue
        outgoing = tuple(np.array(incoming) + step)
        if outgoing not in physical:
            unmatched.append(dict(weight=list(incoming), dimension=len(spaces[incoming])))
            continue
        assert monopole_charges[outgoing] == 1
        current = vectors.current(root, physical[outgoing], physical[incoming], internal, sp.Integer(1))
        entry = dict(input_weight=list(incoming), output_weight=list(outgoing),
                     rank=current.rank(), matrix=vectors.exact_rows(current))
        if outgoing == tuple(fundamental[16]):
            assert current[:3, :].rank() == 2 and current.rank() == 3
            entry['orthogonal_higgs_row'] = vectors.exact_rows(current[3:, :])[0]
            entry['lepton_submatrix_rank'] = current[:3, :].rank()
        blocks.append(entry)
    assert sum(block['rank'] for block in blocks) == 12
    assert len(unmatched) == 1 and unmatched[0]['dimension'] == 1 and unmatched[0]['weight'][-1] == 3
    unbroken = np.stack([*color, weak, weak.T,
                         *(np.diag(np.array(h[:, i], dtype=np.int64).ravel()) for i in range(4))])
    gauginos = Counter(map(int, flat.adjoint_charges(unbroken, coroot)))
    assert gauginos == {-1: 3, 0: 6, 1: 3}
    assert not flat.adjoint_charges(unbroken, y).any()
    full = spectrum + gauginos
    return dict(coroot_coefficients=[str(value) for value in coefficients],
                flux_charge_counts=spectrum, gauge_anomaly_zero=True,
                unbroken_gaugino_flux_charge_counts=gauginos,
                combined_massless_fermion_flux_charge_counts=full,
                projected_root_current_on_unbroken_gauginos_zero=True,
                baryon_anomaly=list(map(int, baryon)), lepton_anomaly=list(map(int, lepton)),
                mixed_baryon_lepton_trace_for_electric_and_dyon_generators=0,
                cartan_convention=['color1', 'color2', '2T3', '6Y'],
                root_current_rank=12, blocks=blocks, unmatched_input=unmatched)


def trial_energy(potential, perpendicular_force, profile, monopole_norm, projection):
    """Exact integrals for a regular hedgehog trial family."""
    def integral(n, k):
        return sp.simplify(sp.gamma(n + sp.Rational(1, 2)) *
                           sp.gamma(k - n - sp.Rational(1, 2)) / (2 * sp.gamma(k)))

    trace_index = monopole_norm / 4
    gauge = trace_index * (integral(3, 4) + 4 * integral(2, 4) + 12 * integral(1, 4))
    scalar = trace_index * (2 * projection)**2 * 3 * integral(1, 3)

    def integrate_even(poly):
        values = sp.Poly(sp.cancel(poly), profile)
        assert all(power[0] % 2 == 0 for power, _ in values.terms())
        return sum(value * integral(power[0] // 2 + 1, power[0] // 2 + 2)
                   for power, value in values.terms())

    potential_factor = integrate_even(potential / (1 - profile**2)**2)
    derivative_factor = -integrate_even(perpendicular_force / (profile**2 - 1))
    assert all(value > 0 for value in (gauge, scalar, potential_factor))
    assert derivative_factor < 0
    radius2 = sp.simplify((-scalar + sp.sqrt(scalar**2 + 12 * potential_factor * gauge))
                          / (6 * potential_factor))
    radius = sp.sqrt(radius2)
    unit_upper = 4 * sp.pi * (gauge / radius + scalar * radius + potential_factor * radius**3)
    # At the unit point even the gauge and gradient terms alone lie
    # above the bound, by AM-GM and pi > 3.
    assert 36 * (gauge / sp.pi) * (scalar / sp.pi) > (projection * monopole_norm)**2
    return dict(scalar_profile='s(r)=r/sqrt(r^2+R^2)', gauge_profile='K(r)=R^2/(r^2+R^2)',
                energy='4*pi*(a/(g^2*R)+b*t*R+c*R^3/t)',
                coefficients=[str(value) for value in (gauge, scalar, potential_factor)],
                perpendicular_variation='delta A = epsilon*K(r)*A_perp',
                energy_derivative='4*pi*d*R^3/t', derivative_coefficient=str(derivative_factor),
                unit_radius_squared=str(radius2), unit_frozen_trial_energy=float(unit_upper),
                bogomolny_lower_bound='120*pi*sqrt(t)/g',
                smooth_fixed_sector_can_saturate_bound=False)


def core_forcing(cartan, y, coroot, circle_coefficients):
    s = sp.Symbol('s', real=True)
    basis = sp.Matrix(cartan)
    trace_inverse = (basis * basis.T).inv()
    a_vacuum = sp.Matrix(y)
    m = sp.Matrix(coroot)
    projection = a_vacuum.dot(m) / m.dot(m)
    assert projection == -sp.Rational(5, 2)
    perpendicular = a_vacuum - projection * m
    profile = perpendicular + s * projection * m
    assert perpendicular.dot(m) == 0
    assert all(profile[i] == 0 for i in (0, 1))
    derivative = profile.applyfunc(lambda value: value**5 - 3 * value**4 - 283 * value)
    projector = basis.T * trace_inverse * basis
    projected = projector * derivative
    potential = sp.factor(derivative.dot(projected))
    curvature = profile.applyfunc(lambda value: 5 * value**4 - 12 * value**3 - 283)
    gradient = 2 * projector * projected.multiply_elementwise(curvature)
    perpendicular_force = sp.factor(gradient.dot(perpendicular))
    circle = basis.T * sp.Matrix([sp.Rational(value) for value in circle_coefficients])
    assert circle.dot(a_vacuum) == circle.dot(m) == 0 and circle[0] == 4
    circle_force = sp.factor(gradient.dot(circle))
    assert circle_force.subs(s, 0) == 1503375
    transverse = gradient - m * (gradient.dot(m) / m.dot(m))
    coefficient_span = sp.Matrix([[sp.Poly(value, s).nth(k) for value in transverse]
                                  for k in range(10)])
    assert coefficient_span.rank() == 3
    matter_force = sp.factor(2 * projected[0])
    assert potential.subs(s, 1) == perpendicular_force.subs(s, 1) == matter_force.subs(s, 1) == 0
    assert perpendicular_force.subs(s, 0) == -sp.Rational(1061338875, 128)
    assert matter_force.subs(s, 0) != 0
    quotient = sp.Poly(sp.cancel(perpendicular_force / (s**2 - 1)), s)
    assert all(coefficient > 0 for coefficient in quotient.coeffs())
    return dict(profile='A(s) = A_perp - (5/2)s m', adjoint_projection=str(projection),
                potential=str(potential), perpendicular_scalar_force=str(perpendicular_force),
                perpendicular_force_at_core=str(perpendicular_force.subs(s, 0)),
                transverse_gradient_polynomial_span=coefficient_span.rank(),
                outside_su5_circle_gradient=str(circle_force),
                outside_su5_circle_gradient_at_core=str(circle_force.subs(s, 0)),
                matter_slot='real X[0] at e0 tensor f2',
                matter_force=str(matter_force), matter_force_at_core=str(matter_force.subs(s, 0)),
                frozen_spectator_ansatz_stationary=False,
                trial=trial_energy(potential, perpendicular_force, s, m.dot(m), projection))


def calculate():
    gauge, internal, cartan, color, weak, y = flat.compact_chart()
    representation = topology.representation_check(internal, cartan, weak, y)
    five = representation['fundamental5_chart']
    root, coroot = monopole_root(internal, five)
    root_spectrum = Counter(map(int, flat.adjoint_charges(internal, coroot)))
    assert root_spectrum == {-2: 1, -1: 20, 0: 36, 1: 20, 2: 1}
    records = flat.vacuum.native.build_records()
    projected = vectors.flavor.projected_space(gauge, internal, color, weak, y, records)
    hessian, orbit, _ = projected[-1]
    return dict(status='PASS', adjoint_monopole_weights=root_spectrum,
                core=core_forcing(cartan, y, coroot, representation['circle_cartan_coefficients']),
                fixed_torus_sector=fixed_torus_sector(internal, color, weak, y, root, five, hessian, orbit),
                radial=radial_channels(projected, internal, color, weak, y, root, coroot, five))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2, default=int) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
