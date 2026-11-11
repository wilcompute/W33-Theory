"""An exact D-flat radial trial family for the canonical W33 monopole."""

from itertools import combinations
import json

import numpy as np
import sympy as sp


import toe_20261110_monopole_core_channels as core

OUT = 'data/toe_20261111_monopole_variational_core.json'
flat = core.flat
MIXED = [(0, 2), (1, 0), (1, 1)]


def sector_and_geometry():
    gauge, internal, cartan, color, weak, y = flat.compact_chart()
    five = core.topology.representation_check(internal, cartan, weak, y)['fundamental5_chart']
    root, m = core.monopole_root(internal, five)
    records = flat.vacuum.native.build_records()
    _, _, _, _, _, (hessian, orbit, _) = core.vectors.flavor.projected_space(
        gauge, internal, color, weak, y, records)
    old = core.fixed_torus_sector(internal, color, weak, y, root, five, hessian, orbit)
    fixed = old['fixed_internal_adjoint_slots']
    matrices = internal[fixed]
    constraints = np.concatenate([(matrices @ generator - generator @ matrices).reshape(10, -1)
                                  for generator in (color[0], color[0].T)], axis=1)
    invariant = sp.Matrix(constraints.T).nullspace()
    assert len(invariant) == 9
    lifts = sp.zeros(483, 39)
    neutral = [81 * k + i for k in range(5) for i in range(6)]
    for j, i in enumerate(neutral):
        lifts[i, j] = 1
    for j, coefficients in enumerate(invariant, 30):
        for i, coefficient in zip(fixed, coefficients):
            lifts[405 + i, j] = coefficient
    h_rank = (lifts.T * sp.Matrix(hessian) * lifts).rank()
    orbit_rank = (sp.Matrix(orbit) * lifts).rank()
    assert (h_rank, orbit_rank) == (25, 14)

    # The neutral fundamental plane is pointwise invariant under both SU(2)s.
    assert all(not generator[:, :2].any() for generator in
               (root, root.T, color[0], color[0].T))
    basis = np.eye(81, dtype=np.int64)[:6]
    assert all(not flat.vacuum.bracket(a, b, records).any() for a, b in combinations(basis, 2))
    assert [tuple(pair) for pair in flat.read(flat.OUT)['repair']['allowed_mixed_cubic_indices_zero_based']] == MIXED

    m, y, cartan = sp.Matrix(m), sp.Matrix(y), sp.Matrix(cartan)
    color_step = np.argwhere(color[0] != 0)[0]
    a, b = map(int, color_step)
    conditions = (cartan[:, a] - cartan[:, b]).T.col_join(m.T * cartan.T)
    coefficients = conditions.nullspace()
    assert len(coefficients) == 4
    singlets = cartan.T * sp.Matrix.hstack(*coefficients)
    perpendicular = y + sp.Rational(5, 2) * m
    assert perpendicular.dot(m) == 0
    assert all(not (np.array(singlets[:, j], dtype=object).ravel()[:, None] * root
                    - root * np.array(singlets[:, j], dtype=object).ravel()).any()
               for j in range(singlets.cols))

    # Only diagonal entries and the neutral (0,1),(1,0) entries can source F_A.
    full = sp.Matrix(internal.reshape(78, -1))
    support = [28 * i for i in range(27)] + [1, 27]
    compressed = full[:, support]
    projector = compressed.T * (full * full.T).inv() * compressed
    return y, m, singlets, projector, dict(complex_chiral_fields=39,
                                            adjoint_singlets=6, adjoint_triplets=1,
                                            holomorphic_hessian_rank=h_rank,
                                            broken_complex_orbit_rank=orbit_rank)


def matter_data(u):
    """Return the exact matter VEVs and centered-meson F gradients on the trial."""
    x = [sp.Matrix([[1, 0, u], [0, 0, 0]]),
         sp.Matrix([[0, 0, 0], [0, 1, 0]]),
         sp.Matrix([[0, 0, 1], [0, 0, 1]])]
    z = [x[0] + x[1], x[2]]
    assert sum((v * v.T for v in x), sp.zeros(2)) == sum((v * v.T for v in z), sp.zeros(2))
    assert sum((v.T * v for v in x), sp.zeros(3)) == sum((v.T * v for v in z), sp.zeros(3))
    mesons = [w.T * v for v in z for w in x]
    _, _, terms = centered_terms()
    gradients = [sp.zeros(2, 3) for _ in range(5)]
    for term in terms:
        word = term['meson_trace']
        product = sp.eye(3)
        for label in word:
            product *= mesons[label]
        shift = sp.expand(sp.trace(product) - term['center'])
        for i, label in enumerate(word):
            cyclic = sp.eye(3)
            for other in word[i + 1:] + word[:i]:
                cyclic *= mesons[other]
            j, k = divmod(label, 3)
            gradients[k] += shift * z[j] * cyclic
            gradients[3 + j] += shift * x[k] * cyclic.T
    source = sum((z[j] * x[k].T for j, k in MIXED), sp.zeros(2))
    assert source == sp.Matrix([[2 * u, u], [u, 0]])
    return x, z, [g.applyfunc(sp.expand) for g in gradients]


def centered_terms():
    x, z = flat.repair_vevs()
    mesons = flat.family_mesons(x, z)
    gauge, internal, _, _, _, y = flat.compact_chart()
    orbit = flat.repair_orbit(x, z, gauge, internal, y)
    _, terms = flat.meson_trace_mass(x, z, mesons, orbit)
    return x, z, terms


def matter_f(a0, a1, x, z, gradients):
    diagonal = sp.diag(a0, a1)
    result = [g.copy() for g in gradients]
    for j, k in MIXED:
        result[k] += diagonal * z[j]
        result[3 + j] += diagonal * x[k]
    return sp.Matrix([value for g in result for value in g])


def radius_and_energy(a, b, c):
    radius2 = 2 * a / (b + (b * b + 12 * c * a)**0.5)
    radius = radius2**0.5
    return radius, 4 * np.pi * (a / radius + b * radius + c * radius**3)


def relaxed_gauge_bound(b, c):
    """Vary the gauge profile while keeping the same scalar shapes."""
    s = sp.Symbol('s', real=True)
    amplitude = sp.Rational(4, 3)
    radius = sp.Rational(647, 10000)
    k = (1 - s**2) * (1 + amplitude * s**2)

    def moment(expression):
        polynomial = sp.Poly(sp.cancel(expression), s)
        assert all(power[0] % 2 == 0 for power, _ in polynomial.terms())
        return sum(coefficient * sp.binomial(power[0], power[0] // 2)
                   / 2**(power[0] + 1) for power, coefficient in polynomial.terms())

    a = 3 * moment(2 * sp.diff(k, s)**2 * (1 - s**2)**2 + (1 - k**2)**2 / s**2)
    b += 150 * moment((k**2 - (1 - s**2)**2) * s**2 / (1 - s**2))
    assert a == sp.Rational(1039, 864) and b == sp.Rational(8249503679, 240000000)
    e_over_pi2 = 4 * (a / radius + b * radius + c * radius**3)
    assert e_over_pi2 * sp.Rational(22, 7)**2 < 1038
    return dict(profile='K=(1-s^2)*(1+4*s^2/3)', radius=str(radius),
                coefficients_over_pi=list(map(str, (a, b, c))),
                energy_over_pi_squared=str(e_over_pi2),
                energy=float(e_over_pi2 * sp.pi**2), upper_bound=1038)


def phase_inertia(radius):
    """Solve Gauss's equation for the electric phase on the trial configuration."""
    angle = sp.Symbol('angle', positive=True)
    k = sp.sqrt(3)
    u = k * sp.cos(k * angle) - sp.cot(angle) * sp.sin(k * angle)
    assert sp.trigsimp(sp.diff(u, angle, 2) + (3 - 2 / sp.sin(angle)**2) * u) == 0
    outer = sp.pi / 2
    p = u / (sp.sin(angle) * u.subs(angle, outer))
    assert p.subs(angle, outer) == 1
    assert sp.limit(p / angle, angle, 0, dir='+').is_finite
    boundary_derivative = sp.simplify(sp.diff(p, angle).subs(angle, outer))
    assert sp.simplify(boundary_derivative + 2 * sp.tan(k * outer) / k) == 0
    inertia_times_g2 = sp.simplify(24 * sp.pi * radius * boundary_derivative)
    return dict(gauss_radial='(r^2 p_prime)_prime = 2 K^2 p',
                inertia_times_g_squared=str(inertia_times_g2),
                inertia_at_unit_g=float(inertia_times_g2))


def trial():
    y, m, singlets, projector, sector = sector_and_geometry()
    u, s = sp.symbols('u s', real=True)
    a0, a1 = sp.symbols('a0 a1', real=True)
    x, z, gradients = matter_data(u)
    matter = matter_f(a0, a1, x, z, gradients)
    matter_fun = sp.lambdify((a0, a1, u), list(matter), 'numpy', cse=True)
    source = sp.zeros(29, 1)
    source[0], source[27], source[28] = 2, 1, 1
    y_f, m_f = [np.array(v, dtype=float).ravel() for v in (y, m)]
    singlets_f, projector_f = [np.array(v, dtype=float) for v in (singlets, projector)]
    source_f = np.array(source, dtype=float).ravel()
    f_vacuum = y.applyfunc(lambda value: value**5 - 3 * value**4 - 283 * value)
    f_vacuum = f_vacuum.col_join(sp.zeros(2, 1))
    assert projector * f_vacuum == sp.zeros(29, 1)
    f_vacuum_f = np.array(f_vacuum, dtype=float).ravel()
    nodes, weights = np.polynomial.legendre.leggauss(40)
    angle = np.pi * (nodes + 1) / 4
    sin, cos2 = np.sin(angle), np.cos(angle)**2
    a = 63 * np.pi / 32

    def energy(parameters):
        normal = singlets_f @ parameters[:4]
        adj = y_f + 2.5 * (1 - sin[:, None]) * m_f + cos2[:, None] * normal
        matter_u = cos2 * parameters[4]
        f_adj = np.pad(adj**5 - 3 * adj**4 - 283 * adj, ((0, 0), (0, 2)))
        f_adj += matter_u[:, None] * source_f - f_vacuum_f
        f_matter = np.stack([np.broadcast_to(v, sin.shape)
                             for v in matter_fun(adj[:, 0], adj[:, 1], matter_u)], axis=1)
        potential = np.einsum('ni,ij,nj->n', f_adj, projector_f, f_adj)
        potential += np.sum(f_matter**2, axis=1)
        c = np.pi / 4 * np.dot(weights, sin**2 * potential / cos2**2)
        b = np.pi * (225 / 16 + (normal @ normal + 2 * parameters[4]**2) / 8)
        return radius_and_energy(a, b, c)[1]

    rational = [sp.Rational(value, 10000) for value in (2718, 5209, -4512, -4398, -989)]

    def exact_coefficients(parameters):
        normal = singlets * sp.Matrix(parameters[:4])
        k = 1 - s**2
        adj = y + sp.Rational(5, 2) * (1 - s) * m + k * normal
        f_adj = adj.applyfunc(lambda v: v**5 - 3 * v**4 - 283 * v).col_join(sp.zeros(2, 1))
        f_adj += source * k * parameters[4]
        f_matter = matter.subs({a0: adj[0], a1: adj[1], u: k * parameters[4]}, simultaneous=True)
        adj_poly = [sp.Poly(value, s, domain=sp.QQ) for value in f_adj]
        matter_poly = [sp.Poly(value, s, domain=sp.QQ) for value in f_matter]
        potential = sum(poly**2 for poly in matter_poly)
        potential += sum(projector[i, j] * adj_poly[i] * adj_poly[j]
                         for i in range(29) for j in range(29) if projector[i, j])
        reduced, remainder = potential.div(sp.Poly(k**2, s))
        assert remainder.is_zero and all(power[0] % 2 == 0 for power, _ in reduced.terms())
        c = sum(coefficient * sp.binomial(power[0] + 2, power[0] // 2 + 1)
                / 2**(power[0] + 3) for power, coefficient in reduced.terms())
        b = sp.Rational(225, 16) + (normal.dot(normal) + 2 * parameters[4]**2) / 8
        return b, c

    baseline_b, baseline_c = exact_coefficients([0] * 5)
    assert baseline_b == sp.Rational(225, 16)
    assert baseline_c == sp.Rational(449843766875, 196608)
    b, c = exact_coefficients(rational)
    assert b > baseline_b and c < baseline_c
    # Use a rational trial radius and compare using rational bounds on pi.
    _, value = radius_and_energy(a, float(sp.pi * b), float(sp.pi * c))
    trial_radius = sp.Rational(747, 10000)
    e_over_pi2 = 4 * (sp.Rational(63, 32) / trial_radius + b * trial_radius + c * trial_radius**3)
    assert e_over_pi2 * sp.Rational(22, 7)**2 < 1422
    assert abs(value - energy(np.array(rational, dtype=float))) < 1e-7, (value, energy(np.array(rational, dtype=float)), rational)
    return dict(status='PASS', sector=sector, radius=str(trial_radius),
                singlet_basis_columns=singlets.tolist(), amplitudes=list(map(str, rational)),
                coefficients_over_pi=list(map(str, (sp.Rational(63, 32), b, c))),
                energy_over_pi_squared=str(e_over_pi2), trial_energy=float(e_over_pi2 * sp.pi**2),
                baseline_energy=energy(np.zeros(5)),
                variational_upper_bound=1422, electric_phase=phase_inertia(trial_radius),
                relaxed_gauge=relaxed_gauge_bound(b, c))


if __name__ == '__main__':
    result = json.dumps(trial(), indent=2, default=lambda value: str(value)) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
