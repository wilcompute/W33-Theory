"""Exact tree-level Weinberg coefficient of the canonical W33 light vacuum."""

from itertools import permutations
import json

import numpy as np
import sympy as sp
from scipy.linalg import eigvalsh

import toe_20261110_light_yukawa_completion as flavor

flat = flavor.flat
OUT = 'data/toe_20261110_neutrino_matching.json'


def add(left, right):
    result = left.copy()
    for key, value in right.items():
        result[key] = result.get(key, 0) + value
    return result


def scale(jet, factor):
    return {key: factor * value for key, value in jet.items()}


def multiply(left, right, operation=np.matmul, maximum=None):
    """Multiply in the algebra with square-zero direction variables."""
    result = {}
    for i, u in left.items():
        if not np.any(u):
            continue
        for j, v in right.items():
            if i & j or (maximum is not None and (i | j).bit_count() > maximum) or not np.any(v):
                continue
            result[i | j] = result.get(i | j, 0) + operation(u, v)
    return result


def transpose(jet):
    return {key: value.T for key, value in jet.items()}


def trace(jet):
    return {key: np.trace(value) for key, value in jet.items()}


def word(mesons, letters, maximum):
    result = mesons[letters[0]]
    for letter in letters[1:]:
        result = multiply(result, mesons[letter], maximum=maximum)
    return result


def jets_at_vev(vectors, x, dual, y, adjoint):
    matter = [{0: value.reshape(27, 3).astype(object)} for value in x]
    conjugate = [{0: value.reshape(27, 3).astype(object)} for value in dual]
    a = {0: np.diag(y).astype(object)}
    for i, direction in enumerate(vectors):
        key = 1 << i
        for j, jet in enumerate(matter + conjugate):
            value = direction[81 * j:81 * (j + 1)].reshape(27, 3)
            if value.any():
                jet[key] = value
        if direction[405:].any():
            a[key] = np.einsum('i,ijk->jk', np.asarray(direction[405:], dtype=np.int64), adjoint).astype(object)
    # The adjoint-only potential contributes to these jets only if at
    # least two directions have adjoint components.
    assert len(a) <= 2
    return matter, conjugate, a


def coefficient(vectors, x, dual, y, adjoint, records, specification):
    """Return the fully polarized derivative in the supplied directions."""
    order = len(vectors)
    mask = (1 << order) - 1
    matter, conjugate, a = jets_at_vev(vectors, x, dual, y, adjoint)
    mesons = [multiply(transpose(f), z, maximum=order) for z in conjugate for f in matter]
    left, mid, right, sign = records

    def omega(f, g, h):
        total = 0
        for i, u in f.items():
            if not u.any():
                continue
            for j, v in g.items():
                if i & j or not v.any():
                    continue
                k = mask ^ (i | j)
                if k in h and h[k].any():
                    total += sum(sign * u.ravel()[left] * v.ravel()[mid] * h[k].ravel()[right])
        return total

    def pair(z, f):
        return multiply(z, f, lambda u, v: (u * v).sum()).get(mask, 0)

    total = -omega(*matter)
    for z, f in specification['mixed']:
        total += pair(conjugate[z], multiply(a, matter[f]))
    a2 = multiply(a, a)
    for term in specification['split']:
        z, f = term['meson']
        r = term['projector_zero_six_Y']
        p = add(a2, {0: -r**2 * np.eye(27, dtype=object)})
        total -= omega(matter[0], matter[1],
                       multiply(multiply(p, matter[0]), transpose(mesons[3 * z + f])))
    for term in specification['trace']:
        invariant = add(trace(word(mesons, term['meson_trace'], order)), {0: -term['center']})
        assert invariant[0] == 0
        total += sp.Rational(1, 2) * multiply(invariant, invariant, lambda u, v: u * v).get(mask, 0)
    if order == 2:
        return total

    # Each dressed leg vanishes at the VEV. To obtain an order-three
    # or order-four term it therefore needs at most a second-order jet.
    covariant_order = order - 3
    family = {}
    for unit, recipe in specification['family'].items():
        result = {}
        for term in recipe:
            result = add(result, scale(word(mesons, term['word'], covariant_order),
                                       sp.Rational(term['coefficient'])))
        family[unit] = result

    d0, d1, d2, dsign = specification['tensor']

    def contract(field):
        answer = {}
        for key, value in field.items():
            if key.bit_count() > covariant_order or not value.any():
                continue
            matrix = np.zeros((3, 27, 27), dtype=object)
            matrix[:, d0, d1] = value[d2, :].T * dsign
            answer[key] = matrix
        return answer

    def covariant(transport):
        seed = multiply(matter[0], transpose(transport), maximum=covariant_order)
        return multiply(contract(conjugate[0]), contract(seed), lambda u, v: (u @ v).sum(axis=0),
                        covariant_order)

    identity = {0: np.eye(27, dtype=object)}
    exotic = covariant({0: np.eye(3, dtype=object)})
    maps = {'I': identity, 'E': exotic, 'O': add(identity, scale(exotic, -1)),
            'C': covariant(family['1,0'])}
    # The order-four jet uses only charged light directions, so its
    # adjoint is fixed. At order three, only the linear power is needed.
    assert order == 3 or len(a) == 1
    powers = [matter[0], multiply(a, matter[0], maximum=1)]
    assert not powers[1].get(0, np.zeros(1)).any()
    highest = specification['highest']
    for _ in range(2, highest + 1):
        powers.append({key: y[:, None] * value for key, value in powers[-1].items() if key})
    legs = {}
    for recipe in specification['operators']:
        target = tuple(leg[0] for leg in recipe)
        for term in specification['filters'][target]:
            placed = []
            for i, (mode, source) in enumerate((leg[1:] for leg in recipe)):
                power = term[('first_A_power', 'second_A_power', 'third_A_power')[i]]
                key = (power, mode, i, source)
                if key not in legs:
                    internal = multiply(maps[mode], powers[power], maximum=order - 2)
                    legs[key] = multiply(internal, transpose(family[f'{i},{source}']), maximum=order - 2)
                placed.append(legs[key])
            value = omega(*placed)
            if value:
                total += sp.Rational(term['coefficient']) * value
    return total


def matching_data():
    gauge, adjoint, _, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    x, dual, _, fundamental, spaces, quadratic = flavor.projected_space(
        gauge, adjoint, color, weak, y, records)
    previous = flat.read(flavor.OUT)
    base = flat.read(flat.OUT)['repair']
    tensor = [(i, j, k, sign) for triple, sign in flat.vacuum.cubic.signed_terms(flat.vacuum.cubic.CUBIC).items()
              for i, j, k in permutations(triple)]
    assert len({(i, j) for i, j, _, _ in tensor}) == len(tensor)
    filters = {tuple(row['target']): row['monomials'] for row in previous['charge_filters']}
    highest = max(max(row['first_A_power'], row['second_A_power'])
                  for monomials in filters.values() for row in monomials)
    spec = dict(mixed=base['allowed_mixed_cubic_indices_zero_based'], split=base['split_exotic_terms'],
                trace=base['centered_trace_squared_terms'], family=previous['family_matrix_unit_words'],
                filters=filters, highest=highest, tensor=np.array(tensor).T,
                operators=previous['completion']['operator_legs'])
    args = (x, dual, y, adjoint, np.array(records).T, spec)
    hessian, orbit, weights = quadratic
    plus = fundamental[15]
    minus = fundamental[23]
    assert np.array_equal(plus, -minus)
    assert not (weights == 2 * plus).all(axis=1).any()
    assert not (weights == 2 * minus).all(axis=1).any()
    down = spaces[tuple(plus)]
    hu, = spaces[tuple(minus)]
    h_row = sp.Matrix([previous['completion']['down_higgs_covector']])
    leptons = [sum((v * c for v, c in zip(down, mix)), np.zeros(483, dtype=object))
               for mix in h_row.nullspace()]
    q, u = (spaces[tuple(fundamental[i])][0] for i in (9, 7))
    assert coefficient([q, u, hu], *args) == previous['completion']['up_matrix'][0][0]
    # Replay one nonzero Hessian entry from each tested field-sector pair.
    units = np.eye(483, dtype=object)
    for left, right in [(slice(0, 243), slice(0, 243)),
                        (slice(0, 243), slice(243, 405)),
                        (slice(0, 243), slice(405, 483)),
                        (slice(243, 405), slice(405, 483))]:
        i, j = np.argwhere(hessian[left, right])[0]
        i, j = int(i) + left.start, int(j) + right.start
        assert coefficient([units[i], units[j]], *args) == hessian[i, j]
    return args, hessian, orbit, weights, leptons, hu


def neutral_matching(args, hessian, orbit, weights, leptons, hu):
    cols = np.flatnonzero(~weights.any(axis=1))
    mass = sp.Matrix(hessian[np.ix_(cols, cols)])
    assert mass.rows == 38 and mass.rank() == 26
    assert sp.Matrix(orbit[:, cols]).rank() == 12
    sources = []
    for index in cols:
        unit = np.zeros(483, dtype=object)
        unit[index] = 1
        sources.append([coefficient([lepton, hu, unit], *args) for lepton in leptons])
    source = sp.Matrix(sources)
    assert source.rank() == 3
    assert sp.Matrix(orbit[:, cols]) * source == sp.zeros(len(orbit), 3)
    solution = mass.gauss_jordan_solve(source)[0]
    exchange = -source.T * solution
    assert not exchange.free_symbols
    direct = sp.Matrix(3, 3, lambda i, j: coefficient([leptons[i], hu, leptons[j], hu], *args) / sp.Integer(2))
    kappa = direct + exchange
    assert kappa == kappa.T
    return mass, source, direct, exchange, kappa, cols, solution


def exact_rows(matrix):
    return [[str(value) for value in row] for row in matrix.tolist()]


def inertia_count(matrix):
    _, diagonal = matrix.LDLdecomposition(hermitian=False)
    pivots = list(diagonal.diagonal())
    assert all(pivots)
    return sum(bool(value > 0) for value in pivots)


def kinetic_comparison(adjoint, orbit, weights, leptons, kappa):
    """Bound the mass hierarchy for any positive adjoint kinetic scale."""
    cols = np.flatnonzero((weights == [0, 0, 1, -3]).all(axis=1))
    orbit = sp.Matrix(orbit[:, cols])
    representatives = sp.Matrix(np.stack(leptons, axis=1)[cols, :])
    matter = [j for j, i in enumerate(cols) if i < 405]
    adjoint_cols = [i - 405 for i in cols if i >= 405]
    assert matter == list(range(len(matter)))
    lift = representatives[matter, :]
    assert representatives[len(matter):, :] == sp.zeros(len(adjoint_cols), 3)

    def quotient(v, orbit_vectors, metric):
        basis = sp.Matrix.vstack(*orbit_vectors.rowspace())
        coupling = basis * metric * v
        return v.T * metric * v - coupling.T * (basis * metric * basis.T).inv() * coupling

    lower = quotient(lift, orbit[:, matter], sp.eye(len(matter)))
    upper = lift.T * lift
    generators = adjoint[adjoint_cols].reshape(len(adjoint_cols), -1)
    unit_metric = sp.diag(sp.eye(len(matter)), sp.Matrix(generators @ generators.T))
    unit = quotient(representatives, orbit, unit_metric)
    positive_mass = -kappa
    assert positive_mass.is_positive_definite and lower.is_positive_definite
    for target in (270 * lower - positive_mass, 48000 * upper - positive_mass):
        assert inertia_count(target) == 2
    upper_ratio = sp.Rational(270**2, 48000**2 - 270**2)
    assert upper_ratio < sp.Rational(1, 30000)
    masses = eigvalsh(np.array(positive_mass, dtype=float), np.array(unit, dtype=float))
    squared = masses * masses
    ratio = (squared[1] - squared[0]) / (squared[2] - squared[0])
    result = dict(assumptions='unit matter kinetic matrices and positive relative adjoint normalization',
                gram_lower=exact_rows(lower), gram_unit_adjoint=exact_rows(unit), gram_upper=exact_rows(upper),
                masses_up_to_common_factor=masses.tolist(), squared_gap_ratio=float(ratio),
                squared_gap_ratio_upper_for_all_positive_adjoint_scales=str(upper_ratio))
    return result, unit


def single_coupling_bracket(kappa, currents, alignment, gram):
    """A rank-one correction brackets the NuFIT 6.0 gap ratio."""
    assert alignment[1, :] == sp.zeros(1, 3)
    update = currents[1, :].T * currents[1, :]
    left = -kappa + sp.Rational(12, 5)**2 * update
    right = -kappa + sp.Rational(5, 2)**2 * update
    assert inertia_count(8300 * gram - left) == 2 and inertia_count(49000 * gram - left) == 2
    assert inertia_count(300 * gram - left) == 1 and inertia_count(300 * gram - right) == 1
    assert inertia_count(8800 * gram - right) == 1 and inertia_count(49500 * gram - right) == 3
    upper = sp.Rational(8300**2, 49000**2 - 300**2)
    lower = sp.Rational(8800**2 - 300**2, 49500**2)
    target = sp.Rational(37, 1250)
    assert upper < target < lower
    return dict(zero_based_T_index=[1, 1], coupling_interval=['12/5', '5/2'],
                left_ratio_upper=str(upper), right_ratio_lower=str(lower), target=str(target))


def calculate():
    data = matching_data()
    mass, source, direct, exchange, kappa, cols, solution = neutral_matching(*data)
    x, dual, y, adjoint, *_ = data[0]
    leptons, hu = data[-2:]
    gradients = np.zeros((483, 3), dtype=np.int64)
    for k in range(3):
        gradients[81 * k:81 * (k + 1), k] = dual[0]
        gradients[243:324, k] = x[k]
    neutral_gradients = sp.Matrix(gradients[cols, :])
    assert neutral_gradients.T * mass.gauss_jordan_solve(neutral_gradients)[0] == sp.eye(3)
    source_pairing = neutral_gradients.T * solution
    assert not source_pairing.free_symbols
    light_traces = sp.Matrix(3, 3, lambda k, i: (
        hu[243:324] @ leptons[i][81 * k:81 * (k + 1)]
        + leptons[i][243:324] @ hu[81 * k:81 * (k + 1)]
    ))
    # J_f = Z0 : [A O A(A-3I) X0 F[2,f]^T], with both end factors
    # vanishing at the VEV. Its first nonzero light jet is a bilinear.
    ordinary = flavor.internal_maps(x, dual, y)['O']
    select = ordinary @ np.diag(y * y * (y - 3))
    currents = sp.Matrix(3, 3, lambda f, i: (
        hu[243:324].reshape(27, 3)[:, 2] @ (select @ leptons[i][:81].reshape(27, 3))[:, f]
        + leptons[i][243:324].reshape(27, 3)[:, 2] @ (select @ hu[:81].reshape(27, 3))[:, f]
    ))
    assert currents.rank() == 3
    alignment = light_traces - source_pairing
    assert kappa.rank() == 3
    comparison, unit_gram = kinetic_comparison(adjoint, data[2], data[3], leptons, kappa)
    return dict(status='PASS', convention='W = (L Hu)^T kappa (L Hu) / 2',
                neutral_dimension=mass.rows, neutral_hessian_rank=mass.rank(), source_rank=source.rank(),
                direct=exact_rows(direct), exchange=exact_rows(exchange),
                kappa=exact_rows(kappa), rank=kappa.rank(),
                kinetic_comparison=comparison,
                neutral_current_extension=dict(
                    current_matrix=exact_rows(currents), current_determinant=str(currents.det()),
                    centered_trace_mass_pairing='I3',
                    direct_minus_exchange_alignment=exact_rows(alignment),
                    completed_square='kappa(T) = kappa + D^T D - (TJ-D)^T(TJ-D)',
                    image='all complex symmetric 3 by 3 matrices',
                    one_coupling_ratio_bracket=single_coupling_bracket(kappa, currents, alignment, unit_gram)))


if __name__ == '__main__':
    result = calculate()
    print(json.dumps(result, indent=2))
    (flat.ROOT / OUT).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
