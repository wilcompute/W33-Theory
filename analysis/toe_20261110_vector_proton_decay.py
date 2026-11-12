"""Exact tree-level massive-vector exchange in the W33 light vacuum."""

from itertools import product
import json

import numpy as np
import sympy as sp

import toe_20261110_light_yukawa_completion as flavor

flat = flavor.flat
OUT = 'data/toe_20261110_vector_proton_decay.json'


def weight_lifts(weights, orbit, adjoint_gram, weight, vectors, scale):
    cols = np.flatnonzero((weights == weight).all(axis=1))
    matter_count = sum(cols < 405)
    a = cols[matter_count:] - 405
    metric = sp.diag(sp.eye(int(matter_count)), scale * sp.Matrix(adjoint_gram[np.ix_(a, a)]))
    lift = sp.Matrix(np.stack(vectors, axis=1)[cols, :])
    basis = sp.Matrix.vstack(*sp.Matrix(orbit[:, cols]).rowspace())
    projection = lift - basis.T * (basis * metric * basis.T).inv() * basis * metric * lift
    projection = projection.applyfunc(sp.cancel)
    assert (basis * metric * projection).applyfunc(sp.cancel) == sp.zeros(basis.rows, lift.cols)
    return (cols, projection), (projection.T * metric * projection).applyfunc(sp.cancel)


def current(generator, outgoing, incoming, adjoint, scale):
    """Matrix of <physical outgoing | T | physical incoming>."""
    out_cols, out_vectors = outgoing
    in_cols, in_vectors = incoming
    chart = np.kron(generator, np.eye(3, dtype=np.int64))
    op = sp.zeros(len(out_cols), len(in_cols))
    for i, row in enumerate(out_cols):
        for j, col in enumerate(in_cols):
            if row < 405 and col < 405 and row // 81 == col // 81:
                matrix = chart if row < 243 else -chart.T
                op[i, j] = int(matrix[row % 81, col % 81])
            if row >= 405 and col >= 405:
                right = adjoint[col - 405]
                value = np.sum(adjoint[row - 405] * (generator @ right - right @ generator))
                op[i, j] = int(value) * scale
    return (out_vectors.T * op * in_vectors).applyfunc(sp.cancel)


def mass_kernel(indices, orbit, adjoint_gram, scale):
    v = orbit[indices, :]
    matter = v[:, :405]
    a = v[:, 405:]
    gram = sp.Matrix(matter @ matter.T) + scale * sp.Matrix(a @ adjoint_gram @ a.T)
    assert gram.det() != 0
    return gram


def positive_rational_on_ray(expression, scale):
    numerator, denominator = [sp.Poly(part, scale) for part in sp.fraction(sp.cancel(expression))]
    # All nonzero coefficients have one sign, with numerator and
    # denominator having the same sign. This is an exact ray certificate.
    return (all(c > 0 for c in numerator.coeffs()) and all(c > 0 for c in denominator.coeffs())
            or all(c < 0 for c in numerator.coeffs()) and all(c < 0 for c in denominator.coeffs()))


def exact_rows(matrix):
    return [[str(value) for value in row] for row in matrix.tolist()]


def lightest_family_test(qque, metrics, yukawa, scale):
    """Test an accessible charged-lepton channel in the unit Yukawa chart."""
    q, up, down, charged, lepton = (metrics[i] for i in (3, 7, 8, 2, 16))
    matrices = [sp.Matrix(yukawa[name]) for name in ('up_matrix', 'down_matrix', 'lepton_matrix')]
    up_left, down_left, charged_right = [
        (y * metric.inv() * y.T).applyfunc(sp.cancel)
        for y, metric in zip(matrices, (up, down, lepton))
    ]
    # The third integral basis vector is both the left and the right
    # lightest up-quark direction. The charged singlet is the middle lepton.
    for matrix in (q, up, charged, up_left, charged_right):
        assert matrix[:2, 2] == sp.zeros(2, 1)
    up_third_squared = up_left[2, 2] / q[2, 2]
    up_diff = (up_left - up_third_squared * q)[:2, :2]
    assert positive_rational_on_ray(up_diff[0, 0], scale)
    assert positive_rational_on_ray(up_diff.det(), scale)
    assert matrices[0] == -3 * sp.eye(3)
    muon_squared = charged_right[2, 2] / charged[2, 2]
    charged_diff = (charged_right - muon_squared * charged)[:2, :2]
    assert charged_diff.det().subs(scale, 1) < 0
    # A positive Rayleigh excess makes this direction lighter than at
    # least one charged lepton for every positive adjoint scale.
    assert positive_rational_on_ray(charged_diff[1, 1], scale)

    # If a down-quark eigenvector had vanishing third coordinate, its
    # first two entries would lie in this one-dimensional kernel.
    assert q[:2, 2] == sp.zeros(2, 1)
    possible = sp.Matrix([down_left[2, 1], -down_left[2, 0]])
    residual = (down_left[:2, :2] * possible).row_join(q[:2, :2] * possible)
    numerator, denominator = [sp.Poly(part, scale)
                              for part in sp.fraction(sp.cancel(residual.det()))]
    assert numerator.count_roots(0, sp.oo) == 1 and denominator.count_roots(0, sp.oo) == 0
    critical = (sp.sqrt(89) - 7) / 24
    assert sp.simplify(numerator.eval(critical)) == 0
    v = possible.col_join(sp.zeros(1, 1)).subs(scale, critical).applyfunc(sp.simplify)
    g, mass = q.subs(scale, critical), down_left.subs(scale, critical)
    norm = sp.simplify((v.T * g * v)[0])
    assert norm > 0
    value = sp.simplify((v.T * mass * v)[0] / norm)
    deficit = (value * g - mass).applyfunc(sp.simplify)
    assert (deficit * v).applyfunc(sp.simplify) == sp.zeros(3, 1)
    sub = deficit.extract([0, 2], [0, 2])
    assert sub[0, 0] > 0 and sp.simplify(sub.det()) > 0
    row = qque[8, 6:9]
    assert row == sp.Matrix([[0, 0, -sp.Rational(4, 75) / scale]])
    return dict(scope='all positive adjoint scales with the fixed unit Yukawa matrices',
                lightest_up_direction=2, middle_charged_lepton_direction_at_unit_scale=2,
                third_charged_lepton_direction_always_lighter_than_another=True,
                down_lightest_always_has_nonzero_third_coordinate=True,
                exceptional_scale_for_heaviest_down=str(critical),
                exceptional_squared_yukawa_eigenvalue=str(value),
                reduced_uu_d_charged_lepton_current='(-4/(75*t)) times the third down-left coordinate')


def calculate():
    gauge, adjoint, _, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    _, _, _, fundamental, spaces, (_, orbit, weights) = flavor.projected_space(
        gauge, adjoint, color, weak, y, records)
    root_cartans = [(g @ g.T - g.T @ g).diagonal() for g in (color[0], color[1], weak)]
    gauge_weights = np.stack([flat.adjoint_charges(adjoint, h) for h in [*root_cartans, y]], axis=1)
    flat_adjoint = adjoint.reshape(78, -1)
    adjoint_gram = flat_adjoint @ flat_adjoint.T
    scale = sp.Symbol('t', positive=True)
    q3, q6, uc, ec, dc = (spaces[tuple(fundamental[i])] for i in (3, 6, 7, 2, 12))
    old = flat.read(flavor.OUT)['completion']
    lepton = [
        flavor.lower_doublet(sum((v * c for v, c in zip(spaces[tuple(fundamental[15])], coefficients)),
                                 np.zeros(483, dtype=object)), weak)
        for coefficients in sp.Matrix([old['down_higgs_covector']]).nullspace()
    ]
    step = next(g for g in color if g[5, 3])
    transport = weak.T @ step
    to_yukawa_q = next(g for g in color if g[9, 3])
    q9 = spaces[tuple(fundamental[9])]
    for v, w in zip(q3, q6):
        assert not v[243:].any() and not w[243:].any()
        assert np.array_equal(transport @ v[:243].reshape(3, 27, 3),
                              -w[:243].reshape(3, 27, 3))
    for v, w in zip(q3, q9):
        assert not w[243:].any()
        assert np.array_equal(to_yukawa_q @ v[:243].reshape(3, 27, 3),
                              int(to_yukawa_q[9, 3]) * w[:243].reshape(3, 27, 3))
    lifts = {
        index: weight_lifts(weights, orbit, adjoint_gram, fundamental[index], vectors, scale)
        for index, vectors in [(3, q3), (6, q6), (7, uc), (2, ec), (12, dc), (16, lepton),
                               (8, spaces[tuple(fundamental[8])])]
    }

    def exchange(a, b, c, d):
        w = fundamental[a] - fundamental[b]
        assert np.array_equal(w, fundamental[d] - fundamental[c])
        indices = np.flatnonzero((gauge_weights == w).all(axis=1)).tolist()
        reverse = []
        signs = []
        for i in indices:
            j, sign = next((j, s) for j, candidate in enumerate(adjoint) for s in (1, -1)
                           if np.array_equal(adjoint[i].T, s * candidate))
            reverse.append(j)
            signs.append(sign)
        gram = mass_kernel(indices, orbit, adjoint_gram, scale)
        sign = sp.diag(*signs)
        assert gram == sign * mass_kernel(reverse, orbit, adjoint_gram, scale) * sign
        left = [current(adjoint[i], lifts[a][0], lifts[b][0], adjoint, scale) for i in indices]
        right = [current(adjoint[i].T, lifts[c][0], lifts[d][0], adjoint, scale) for i in indices]
        inverse = gram.inv()
        tensor = sp.zeros(9)
        for i, j in product(range(len(indices)), repeat=2):
            tensor += inverse[i, j] * sp.kronecker_product(left[i], right[j])
        trace_gram = sp.Matrix(adjoint_gram[np.ix_(indices, indices)])
        masses = (trace_gram.inv() * gram).eigenvals()
        block = dict(generators=indices, vev_gram=exact_rows(gram),
                     trace_normalized_mass_eigenvalues=[str(k) for k in masses])
        return block, tensor.applyfunc(sp.cancel), left, right

    x1, qque_a, up_current, lepton_current = exchange(7, 3, 2, 6)
    x2, qque_b, _, _ = exchange(7, 6, 2, 3)
    # Align row order (Uc,Ec) and columns (Q at weight 3,Q at weight 6).
    permutation = [3 * j + i for i, j in product(range(3), repeat=2)]
    assert qque_a == qque_b
    for matrices in (up_current, lepton_current):
        matrix, = matrices
        det = sp.cancel(matrix.det())
        assert det.subs(scale, 1) != 0
        assert positive_rational_on_ray(sp.sign(det.subs(scale, 1)) * det, scale)
    qque = (qque_a + qque_b[:, permutation]).applyfunc(sp.cancel)
    assert positive_rational_on_ray(-qque[0, 0], scale)
    x3, duql_a, _, _ = exchange(7, 3, 12, 16)
    xp, duql_b, _, _ = exchange(12, 3, 7, 16)
    duql_b = duql_b[permutation, :]
    duql = (duql_a + duql_b).applyfunc(sp.cancel)
    unit_q = qque.subs(scale, 1)
    unit_d = duql.subs(scale, 1)
    assert unit_q.rank() == 6 and unit_d.rank() == 7
    metrics = {index: data[1].subs(scale, 1) for index, data in lifts.items()}
    row_inverse = sp.kronecker_product(metrics[7].inv(), metrics[12].inv())
    col_inverse = sp.kronecker_product(metrics[3].inv(), metrics[16].inv())

    def inner(a, b):
        return sp.trace(row_inverse * a * col_inverse * b.T)

    a, b = duql_a.subs(scale, 1), duql_b.subs(scale, 1)
    normal_a = inner(a, a)
    normal_b = inner(b, b)
    interference = 2 * inner(a, b)
    assert inner(unit_d, unit_d) == normal_a + normal_b + interference
    assert normal_b > normal_a > 0
    return dict(status='PASS', convention='reduced current pairings before common Weyl and action factor',
                su5_channels=[x1, x2, x3], flipped_channel=xp,
                flavor_rows=dict(qque='Uc,Ec', duql='Uc,Dc'),
                flavor_columns=dict(qque='Q at 3,Q at 6', duql='Q at 3,L at 16'),
                qque_unit=exact_rows(unit_q), duql_unit=exact_rows(unit_d),
                qque_rank_at_unit=unit_q.rank(), duql_rank_at_unit=unit_d.rank(),
                qque_rank_all_positive_adjoint_scales=6,
                duql_unit_norm_ratios=dict(flipped_over_su5=str(normal_b / normal_a),
                                           interference_over_su5=str(interference / normal_a)),
                unit_yukawa_accessible_channel=lightest_family_test(
                    qque, {index: data[1] for index, data in lifts.items()}, old, scale),
                first_qque_coefficient=str(sp.factor(qque[0, 0])))


if __name__ == '__main__':
    result = calculate()
    (flat.ROOT / OUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
