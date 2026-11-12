"""Exact Higgs–lepton alignment test for the W33 neutral quartic."""

import json

import numpy as np
import sympy as sp

import toe_20261110_neutrino_matching as neutrino

flat = neutrino.flat
OUT = 'data/toe_20261110_neutral_higgs_alignment.json'


def adapted_basis(adjoint, orbit, weights, doublets):
    """Keep the intrinsic lepton kernel and orthogonalize only the Higgs."""
    columns = np.flatnonzero((weights == [0, 0, 1, -3]).all(axis=1))
    lifts = sp.Matrix(np.stack(doublets, axis=1)[columns, :])
    adjoint_cols = [i - 405 for i in columns if i >= 405]
    generators = adjoint[adjoint_cols].reshape(len(adjoint_cols), -1)
    t = sp.Symbol('t', positive=True)
    metric = sp.diag(sp.eye(len(columns) - len(adjoint_cols)),
                     t * sp.Matrix(generators @ generators.T))
    varying = neutrino.quotient_metric(lifts, sp.Matrix(orbit[:, columns]), metric).applyfunc(sp.cancel)
    expected = sp.diag(19, 19, (1080 * t + 71) / (54 * t + 4), 19)
    expected[2, 3] = expected[3, 2] = 1
    assert (varying - expected).applyfunc(sp.cancel) == sp.zeros(4)
    gram = varying.subs(t, 1)
    assert gram.is_positive_definite
    shift = gram[:3, :3].inv() * gram[:3, 3]
    change = sp.eye(4)
    change[:3, 3] = -shift
    adapted = change.T * gram * change
    assert adapted == sp.diag(*adapted.diagonal())
    return gram, change, adapted, varying


def neutral_currents(args, doublets, hu, neutral_cols, mass, solution):
    """Four gauge-covariant currents and their neutral mass pairings."""
    x, dual, y, *_ = args
    trace_pairs = [(0, 0), (0, 1), (0, 2), (1, 0)]
    gradients = np.zeros((483, 4), dtype=np.int64)
    direct = sp.zeros(4)
    for i, (j, k) in enumerate(trace_pairs):
        z_slice = slice(243 + 81 * j, 324 + 81 * j)
        x_slice = slice(81 * k, 81 * (k + 1))
        gradients[x_slice, i] = dual[j]
        gradients[z_slice, i] = x[k]
        for f, vector in enumerate(doublets):
            direct[i, f] = hu[z_slice] @ vector[x_slice] + vector[z_slice] @ hu[x_slice]
    grad = sp.Matrix(gradients[neutral_cols, :])
    assert grad.T * mass.gauss_jordan_solve(grad)[0] == sp.eye(4)
    alignment = direct - grad.T * solution
    assert not alignment.free_symbols

    internal = neutrino.flavor.internal_maps(x, dual, y)
    recipes = [('O', 0, 2, f) for f in range(3)] + [('E', 1, 1, 0)]
    currents = sp.zeros(4)
    for i, (mode, j, output, family) in enumerate(recipes):
        selector = internal[mode] @ np.diag(y * y * (y - 3))
        z_slice = slice(243 + 81 * j, 324 + 81 * j)
        for f, vector in enumerate(doublets):
            currents[i, f] = (
                hu[z_slice].reshape(27, 3)[:, output] @ (selector @ vector[:81].reshape(27, 3))[:, family]
                + vector[z_slice].reshape(27, 3)[:, output] @ (selector @ hu[:81].reshape(27, 3))[:, family]
            )
    assert currents[:3, 3] == sp.zeros(3, 1) and currents[3, :3] == sp.zeros(1, 3)
    assert currents.det() != 0
    return trace_pairs, recipes, currents, alignment


def alignment_certificate(kappa, gram, currents, difference):
    mixed = kappa[:3, 3]
    assert mixed != sp.zeros(3, 1)
    norm_sq = (mixed.T * gram[:3, :3].inv() * mixed)[0] / gram[3, 3]

    # The single knob in the previous packet uses I_1 J_1. Check the
    # entire polynomial path, including the changed Higgs direction.
    one = sp.zeros(4)
    one[1, 1] = 1
    update = one * currents
    lam = sp.Symbol('lambda')
    path = (kappa + lam * (difference.T * update + update.T * difference)
            - lam**2 * update.T * update)[:3, 3]
    assert path.applyfunc(sp.expand) == mixed

    # Two independent neutral rows suffice. Row 1 cancels b and row 2
    # controls the splitting, with zero alignment-difference on both rows.
    assert difference[1:3, :] == sp.zeros(2, 4)
    align = mixed.T.row_join(sp.Matrix([[1000000]])) / 1000
    second = currents[1, :]
    assert second[3] == 0 and second != sp.zeros(1, 4)
    effective = kappa - align.T * align - lam**2 * second.T * second
    assert effective[:3, 3] == sp.zeros(3, 1)
    lepton_gram = gram[:3, :3]
    left = -effective[:3, :3].subs(lam, sp.Rational(12, 5))
    right = -effective[:3, :3].subs(lam, sp.Rational(5, 2))
    inertia = neutrino.inertia_count
    assert inertia(8300 * lepton_gram - left) == 2 and inertia(49000 * lepton_gram - left) == 2
    assert inertia(300 * lepton_gram - left) == 1 and inertia(300 * lepton_gram - right) == 1
    assert inertia(8800 * lepton_gram - right) == 1 and inertia(49500 * lepton_gram - right) == 3
    upper = sp.Rational(8300**2, 49000**2 - 300**2)
    lower = sp.Rational(8800**2 - 300**2, 49500**2)
    assert upper < sp.Rational(37, 1250) < lower
    first_coupling = align * currents.inv()
    return dict(mixed_coefficient=[str(value) for value in mixed],
                kinetic_normalized_mixed_norm_squared=str(norm_sq),
                previous_single_coupling_path=[str(entry.expand()) for entry in path],
                aligned_rank_two_witness=dict(
                    zero_based_first_row=1, first_row=[str(value) for value in first_coupling],
                    zero_based_variable_entry=[2, 1], variable_interval=['12/5', '5/2'],
                    left_ratio_upper=str(upper), right_ratio_lower=str(lower),
                    isolated_gap_ratio='37/1250'))


def uniform_alignment_bound(kappa, difference, currents):
    """Extend the real rank-one exclusion over all positive adjoint scales."""
    # Only the third lepton is added to Hd, with coefficient -p. The
    # exact quotient metric puts p in [1/20, 4/71] for every scale.
    p = sp.Symbol('p')
    lo, hi = sp.Rational(1, 20), sp.Rational(4, 71)
    shift = sp.Matrix([0, 0, -p, 1])
    assert difference * shift == sp.zeros(4, 1) and (currents * shift)[1] == 0
    b = kappa[:3, :] * shift
    for endpoint in (lo, hi):
        assert b[2].subs(p, endpoint) > 0
    plane = sp.Matrix([[b[2], 0], [0, b[2]], [-b[0], -b[1]]])
    a = -kappa[:3, :3]
    floor = a - difference[:, :3].T * difference[:, :3]
    assert floor.is_positive_definite and floor[2, 2] > 48000 * 20
    lower_metric = sp.diag(19, 19, sp.Rational(71, 4))
    restricted = plane.T * (300 * lower_metric - a) * plane
    for minor in (restricted[0, 0], restricted.det()):
        polynomial = sp.Poly(minor, p)
        assert polynomial.eval(lo) > 0 and polynomial.count_roots(lo, hi) == 0
    ratio_upper = sp.Rational(300**2, 48000**2 - 300**2)
    return dict(adjoint_scale='all positive', higgs_shift_interval=[str(lo), str(hi)],
                nonzero_mixed_column=True, real_aligned_rank_one_gap_ratio_upper=str(ratio_upper))


def neutralino_exchange():
    """Verify the conditional neutralino correction at zero sneutrino VEV."""
    u, d, c, alpha = sp.symbols('u d c alpha', nonzero=True, real=True)
    r = sp.Matrix([2 * u * d, u**2])
    v = sp.Matrix([u, -d])
    higgsino = c * sp.Matrix([[d**2, 2 * u * d], [2 * u * d, u**2]])
    block = higgsino - alpha * v * v.T
    scalar = (r.T * block.inv() * r)[0]
    expected = u**2 / c + alpha * d**2 / (c**2 * (1 - alpha * (v.T * higgsino.inv() * v)[0]))
    assert sp.cancel(scalar - expected) == 0
    return dict(assumptions=['real neutral VEVs u,d', 'zero sneutrino VEV',
                             'no additional mu or bilinear superpotential terms',
                             'invertible heavy block and nonzero gaugino masses'],
                alpha='(gY^2/M1 + g2^2/M2)/2',
                higgsino_after_gaugino_exchange=neutrino.exact_rows(block),
                source_vector=[str(value) for value in r],
                schur_scalar=str(sp.factor(scalar)),
                neutrino_schur_block='u^2 K_LL - schur_scalar * b b^T',
                correction_rank_upper=1)


def calculate():
    data = neutrino.matching_data(include_down_higgs=True)
    args, _, orbit, weights, doublets, hu = data
    mass, source, direct, exchange, kappa, cols, solution = neutrino.neutral_matching(*data)
    previous = flat.read(neutrino.OUT)
    for label, matrix in [('direct', direct), ('exchange', exchange), ('kappa', kappa)]:
        assert neutrino.exact_rows(matrix[:3, :3]) == previous[label]
    assert kappa.det() != 0
    raw_gram, change, gram, varying = adapted_basis(args[3], orbit, weights, doublets)
    adapted = change.T * kappa * change
    up_cols = np.flatnonzero((weights == [0, 0, -1, 3]).all(axis=1))
    up_adj = [i - 405 for i in up_cols if i >= 405]
    generators = args[3][up_adj].reshape(len(up_adj), -1)
    metric = sp.diag(sp.eye(len(up_cols) - len(up_adj)), sp.Matrix(generators @ generators.T))
    up_gram = neutrino.quotient_metric(sp.Matrix(hu[up_cols]), sp.Matrix(orbit[:, up_cols]), metric)
    assert up_gram == sp.Matrix([[21]])
    trace_pairs, recipes, currents, difference = neutral_currents(args, doublets, hu, cols, mass, solution)
    return dict(status='PASS', basis=['L0', 'L1', 'L2', 'Hd'], source_rank=source.rank(),
                direct=neutrino.exact_rows(direct), exchange=neutrino.exact_rows(exchange),
                kappa=neutrino.exact_rows(kappa), rank=kappa.rank(),
                raw_gram=neutrino.exact_rows(raw_gram), gram_all_adjoint_scales=neutrino.exact_rows(varying),
                basis_change=neutrino.exact_rows(change),
                adapted_gram=neutrino.exact_rows(gram), adapted_kappa=neutrino.exact_rows(adapted),
                up_higgs_gram=int(up_gram[0]),
                neutral_susy_EWSB_branch_from_origin=False,
                extension=dict(trace_pairs=trace_pairs, current_recipes=recipes, neutral_mass_pairing='I4',
                               adapted_currents=neutrino.exact_rows(currents * change),
                               adapted_alignment=neutrino.exact_rows(difference * change)),
                alignment=alignment_certificate(adapted, gram, currents * change, difference * change),
                uniform_alignment_bound=uniform_alignment_bound(kappa, difference, currents),
                neutralino_exchange=neutralino_exchange())


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
