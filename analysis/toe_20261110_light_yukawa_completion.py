"""Exact light cubic obstruction and covariant Yukawa completion."""

from itertools import permutations, product
import json

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import toe_20261109_canonical_sm_flatness as flat

OUT = 'data/toe_20261110_light_yukawa_completion.json'


def projected_space(gauge, internal, color, weak, y, records):
    x, dual = flat.repair_vevs()
    orbit = flat.repair_orbit(x, dual, gauge, internal, y)
    repair = flat.read(flat.OUT)['repair']
    terms = [tuple(pair) for pair in repair['allowed_mixed_cubic_indices_zero_based']]
    hessian = flat.holomorphic_hessian(x, dual, internal, y, records, terms)
    hessian[405:, 405:] += flat.sextic_adjoint_hessian(internal, y)
    mesons = flat.family_mesons(x, dual)
    hessian += flat.split_exotic_hessian(x, y, mesons, records, orbit)
    trace_hessian, trace_terms = flat.meson_trace_mass(x, dual, mesons, orbit)
    assert trace_terms == repair['centered_trace_squared_terms']
    hessian += trace_hessian
    assert not (orbit @ hessian).any()
    roots = [color[0], color[1], weak]
    coroots = [(root @ root.T - root.T @ root).diagonal() for root in roots]
    fundamental = np.stack([*coroots, y], axis=1)
    weights = np.stack([flat.field_charges(internal, h) for h in fundamental.T], axis=1)
    spaces = {}
    for weight in sorted(set(map(tuple, weights))):
        cols = np.flatnonzero((weights == weight).all(axis=1))
        opposite = (weights == -np.array(weight)).all(axis=1)
        kernel = sp.Matrix(hessian[opposite, :][:, cols]).nullspace()
        gauge_basis = sp.Matrix(orbit[:, cols]).rowspace()
        if not kernel:
            continue
        columns = sp.Matrix.hstack(*[v.T for v in gauge_basis], *kernel)
        lifts = []
        for i in columns.rref()[1]:
            if i < len(gauge_basis):
                continue
            v = kernel[i - len(gauge_basis)]
            lift = np.zeros(483, dtype=object)
            denominator = sp.ilcm(1, *[entry.q for entry in v])
            lift[cols] = [int(entry * denominator) for entry in v]
            lifts.append(lift)
        if lifts:
            spaces[weight] = lifts
    assert sum(map(len, spaces.values())) == 49
    return x, dual, mesons, fundamental, spaces, (hessian, orbit, weights)


def check_old_cubic(spaces):
    """All charged representatives live in X1=-X0, X2=0 with A fixed."""
    for weight, lifts in spaces.items():
        assert weight[-1] != 0
        for vector in lifts:
            assert np.array_equal(vector[:81], -vector[81:162])
            assert not vector[162:243].any() and not vector[405:].any()
            matter = vector[:405].reshape(5, 27, 3)
            assert not matter[:, :2, :].any()


def family_units(mesons):
    """Express every family matrix unit as a polynomial in the mesons."""
    words, matrices = [], []
    for length in range(1, 4):
        for word in product(range(6), repeat=length):
            matrix = np.eye(3, dtype=np.int64)
            for letter in word:
                matrix = matrix @ mesons[letter]
            trial = np.stack([*matrices, matrix.reshape(9)])
            if flat.vacuum.rank(trial) > len(matrices):
                matrices.append(matrix.reshape(9))
                words.append(word)
            if len(matrices) == 9:
                break
        if len(matrices) == 9:
            break
    assert len(matrices) == 9
    units = np.eye(9, dtype=np.int64)
    coefficients = sp.Matrix(np.stack(matrices).T).inv()
    rules = {}
    for target in range(9):
        output, source = divmod(target, 3)
        rules[f'{output},{source}'] = [
            dict(word=list(word), coefficient=str(coefficient))
            for word, coefficient in zip(words, coefficients[:, target]) if coefficient
        ]
        assert np.array_equal(np.stack(matrices).T @ np.array(coefficients[:, target]).ravel(),
                              units[target])
    return rules


def internal_maps(x, dual, y):
    """The cross map converts the exotic down anti-triplet to its ordinary slot."""
    native = flat.vacuum.cubic
    tensor = np.zeros((27, 27, 27), dtype=np.int64)
    for triple, sign in native.signed_terms(native.CUBIC).items():
        for indices in permutations(triple):
            tensor[indices] = sign
    identity = np.eye(27, dtype=np.int64)
    # E is the contraction of d(X0) and its dual with identity family transport.
    # C uses the family unit sending f0 to f1 on X0 before contraction with Z0.
    matter, conjugate = x[0].reshape(27, 3), dual[0].reshape(27, 3)
    d = np.einsum('vwj,wa->vja', tensor, matter)
    dual_d = np.einsum('iuv,ua->iva', tensor, conjugate)
    exotic = np.einsum('iva,vja->ij', dual_d, d)
    cross = dual_d[:, :, 1] @ d[:, :, 0]
    expected = flat.read(flat.SM)['exotic_mass_support']
    assert np.array_equal(exotic, np.diag([int(i in expected) for i in range(27)]))
    assert abs(cross[8, 17]) == 1 and not cross[:, 8].any()
    maps = {'I': identity, 'E': exotic, 'O': identity - exotic, 'C': cross}
    assert all(not (matrix * (y[:, None] - y[None, :])).any() for matrix in maps.values())
    return maps


def lower_doublet(vector, weak):
    result = np.zeros_like(vector)
    matter = vector[:243].reshape(3, 27, 3)
    dual = vector[243:405].reshape(2, 27, 3)
    result[:243] = (weak.T @ matter).ravel()
    result[243:405] = (-weak @ dual).ravel()
    return result


def covectors(lifts, internal, index, modes):
    available = [(mode, source) for mode in modes for source in range(3)]
    rows = [[int((internal[mode] @ v[:81].reshape(27, 3))[index, source]) for v in lifts]
            for mode, source in available]
    pivots = sp.Matrix(rows).T.rref()[1]
    return [available[i] for i in pivots], [rows[i] for i in pivots]


def repaired_cubic(records, y, internal, terms, vectors):
    """Third jet of the added operators, with all three legs zero at the VEV."""
    total = 0
    for term in terms:
        for order in permutations(vectors):
            legs = []
            for output, ((charge, mode, source), (weight, vector)) in enumerate(zip(term, order)):
                if charge != weight:
                    break
                selected = (y == charge).astype(int)[:, None] * vector[:81].reshape(27, 3)
                leg = np.zeros((27, 3), dtype=object)
                leg[:, output] = (internal[mode] @ selected)[:, source]
                legs.append(leg.ravel())
            if len(legs) == 3:
                total += flat.vacuum.bracket(legs[0], legs[1], records) @ legs[2]
    return total


def charge_filters(charges, targets):
    """Separate the charged cubic channels including the heavy triplet charge."""
    triples = [t for t in product(charges, repeat=3) if sum(t) == 0]
    # The fourth-order filter varies one internal covariant and depends
    # only on the first two external charges, since the third is linear.
    triples += [(-4, -4, 1), (2, 6, 1), (6, 2, 1)]
    powers = [(a, degree - a) for degree in range(8) for a in range(degree + 1)]
    matrix = sp.Matrix([[q * r * t * q**a * r**b for a, b in powers] for q, r, t in triples])
    pivots = DomainMatrix.from_Matrix(matrix).to_field().rref()[1]
    assert len(pivots) == len(triples) == 30
    inverse = matrix[:, list(pivots)].inv()
    filters = []
    for target in targets:
        index = triples.index(target)
        assert matrix[:, list(pivots)] * inverse[:, index] == sp.eye(len(triples))[:, index]
        filters.append(dict(target=list(target), monomials=[
            dict(first_A_power=powers[pivot][0] + 1, second_A_power=powers[pivot][1] + 1,
                 third_A_power=1, coefficient=str(value))
            for pivot, value in zip(pivots, inverse[:, index]) if value
        ]))
        for external in ((1, 1, 1, -3), (-4, -4, 2, 6)):
            for q, r, t, _ in set(permutations(external)):
                assert sum(value * q**(powers[pivot][0] + 1) * r**(powers[pivot][1] + 1) * t
                           for pivot, value in zip(pivots, inverse[:, index])) == 0
    return filters


def flavor_operators(spaces, fundamental, y, internal, weak, records):
    at = lambda index: spaces[tuple(fundamental[index])]
    q, u, d, e = [at(i) for i in (9, 7, 8, 2)]
    doublets, hu = at(15), at(23)
    down_doublets = [lower_doublet(v, weak) for v in doublets]
    d_select, d_rows = covectors(d, internal, 8, ['O', 'C'])
    hu_select, _ = covectors(hu, internal, 23, ['E'])
    h_select, h_rows = covectors(doublets, internal, 20, ['E'])
    l_select, l_rows = covectors(doublets, internal, 15, ['O'])
    assert len(d_select) == 3 and len(hu_select) == len(h_select) == 1
    assert len(l_select) == 3 and sp.Matrix(h_rows + l_rows).det() != 0
    for fields, index in [(q, 9), (u, 7), (e, 2)]:
        assert len(covectors(fields, internal, index, ['I'])[0]) == 3

    up = [[(1, 'I', i), (-4, 'I', i), (3, *hu_select[0])] for i in range(3)]
    down = [[(1, 'I', i), (2, *d_select[i]), (-3, *h_select[0])] for i in range(3)]
    lepton = [[(6, 'I', i), (-3, *l_select[i]), (-3, *h_select[0])] for i in range(3)]
    terms = up + down + lepton

    def cubic(a, b, c):
        return repaired_cubic(records, y, internal, terms, [a, b, c])

    up_matrix = sp.Matrix([[cubic((1, a), (-4, b), (3, hu[0])) for b in u] for a in q])
    down_matrices = [
        sp.Matrix([[cubic((1, a), (2, b), (-3, h)) for b in d] for a in q])
        for h in down_doublets
    ]
    charged_lepton = [
        sp.Matrix([[cubic((6, a), (-3, b), (-3, h)) for h in down_doublets] for b in doublets])
        for a in e
    ]
    h_row = sp.Matrix(h_rows)
    leptons = sp.Matrix.hstack(*h_row.nullspace())
    higgs, = sp.Matrix(l_rows).nullspace()
    assert (h_row * higgs)[0] != 0
    assert up_matrix.rank() == 3
    assert sp.Matrix([list(m) for m in down_matrices]).rank() == 1
    assert all(sum((m * v[i] for i, m in enumerate(down_matrices)), sp.zeros(3)) == sp.zeros(3)
               for v in h_row.nullspace())
    down_matrix = sum((m * higgs[i] for i, m in enumerate(down_matrices)), sp.zeros(3))
    assert down_matrix.rank() == 3
    assert all(m == -m.T and leptons.T * m * leptons == sp.zeros(3) for m in charged_lepton)
    lepton_matrix = sp.Matrix.vstack(*[(leptons.T * m * higgs).T for m in charged_lepton])
    assert lepton_matrix.rank() == 3
    assert not any(cubic((-4, a), (2, b), (2, c))
                   for a, b, c in product(u, at(12), at(14)))

    return dict(operator_legs=terms, down_higgs_covector=h_rows[0],
                down_quark_covectors=d_rows, lepton_covectors=l_rows,
                up_matrix=up_matrix.tolist(), down_matrix=down_matrix.tolist(),
                lepton_matrix=lepton_matrix.tolist(),
                ranks=dict(up=3, down=3, charged_lepton=3),
                lepton_number_violating_cubics=0, baryon_number_violating_cubic=0)


def colored_exchange(x, mesons, fundamental, spaces, quadratic, adjoint, weak, y,
                     maps, records, completion):
    """Pair exact triplet sources through the heavy holomorphic mass block."""
    hessian, orbit, weights = quadratic
    triplet_weights = {tuple(row) for row in fundamental if abs(row[-1]) == 2}
    assert {tuple(row) for row in weights if abs(row[-1]) == 2} == triplet_weights
    assert len(triplet_weights) == 6 and not (np.abs(weights[:, -1]) == 8).any()
    terms = completion['operator_legs']
    adjoint_vev = np.diag(y).astype(object)
    old_split = [(mesons[5], np.diag(y * y - 9)), (mesons[1], np.diag(y * y - 4))]
    first, second = x[:2].reshape(2, 27, 3)
    left, mid, right, signs = np.array(records).T

    def omega(a, b, c):
        if not a.any() or not b.any() or not c.any():
            return 0
        return sum(signs * a.ravel()[left] * b.ravel()[mid] * c.ravel()[right])

    def cubic(vectors, charges):
        # Each charge is nonzero and no pair has zero charge. Mesons have
        # zero first and second variations on the three inputs.
        assert all(charges) and sum(charges) == 0
        matter = [v[:243].reshape(3, 27, 3) for v in vectors]
        conjugate = [v[243:405].reshape(2, 27, 3) for v in vectors]
        aa = [np.einsum('a,aij->ij', np.array(v[405:], dtype=np.int64), adjoint).astype(object)
              for v in vectors]
        total = 0
        for i, j, k in permutations(range(3)):
            # native.jacobian(v) pairs the last slot against the first
            # Hessian index, giving the minus sign in the base certificate.
            total -= omega(matter[i][0], matter[j][1], matter[k][2])
            for z, t in [(0, 2), (1, 0), (1, 1)]:
                if aa[j].any():
                    total += (conjugate[i][z] * (aa[j] @ matter[k][t])).sum()
            for meson, polynomial in old_split:
                total -= omega(matter[i][0], matter[j][1], polynomial @ matter[k][0] @ meson.T)
                if aa[j].any():
                    derivative = adjoint_vev @ aa[j] + aa[j] @ adjoint_vev
                    value = derivative @ matter[k][0] @ meson.T
                    total -= omega(matter[i][0], second, value) + omega(first, matter[i][1], value)
        dressed = []
        for vector, charge, da in zip(vectors, charges, aa):
            lift = vector.copy()
            if da.any():
                lift[:81] += (da @ first).ravel() * sp.Rational(1, charge)
            dressed.append((charge, lift))
        return total + repaired_cubic(records, y, maps, terms, dressed)

    def sources(indices, first_basis, second_basis):
        w1, w2 = fundamental[list(indices)]
        weight = -w1 - w2
        cols = np.flatnonzero((weights == weight).all(axis=1))
        assert len(cols) and tuple(weight) in triplet_weights
        units = []
        for column in cols:
            unit = np.zeros(483, dtype=object)
            unit[column] = 1
            units.append(unit)
        charges = tuple(map(int, (w1[-1], w2[-1], weight[-1])))
        matrix = sp.Matrix([[cubic([a, b, unit], charges) for a, b in product(first_basis, second_basis)]
                            for unit in units])
        assert sp.Matrix(orbit[:, cols]) * matrix == sp.zeros(len(orbit), matrix.cols)
        return cols, matrix

    def check(first_pair, second_pair, last_basis):
        a, b = first_pair
        c, _ = second_pair
        left_cols, l = sources(first_pair, spaces[tuple(fundamental[a])], spaces[tuple(fundamental[b])])
        right_cols, r = sources(second_pair, spaces[tuple(fundamental[c])], last_basis)
        mass = sp.Matrix(hessian[np.ix_(left_cols, right_cols)])
        solution = mass.gauss_jordan_solve(l)[0]
        mass.T.gauss_jordan_solve(r)
        exchange = r.T * solution
        assert exchange == sp.zeros(r.cols, l.cols)
        return dict(source_ranks=[l.rank(), r.rank()], triplet_mass_rank=mass.rank(),
                    exchange_flavor_shape=list(exchange.shape), exchange_rank=0)

    doublets = spaces[tuple(fundamental[15])]
    h_row = sp.Matrix([completion['down_higgs_covector']])
    leptons = [lower_doublet(sum((v * c for v, c in zip(doublets, coefficients)),
                                np.zeros(483, dtype=object)), weak)
               for coefficients in h_row.nullspace()]
    return dict(QQQL=check((3, 6), (9, 16), leptons),
                UcUcDcEc=check((7, 2), (11, 14), spaces[tuple(fundamental[14])]))


def calculate():
    gauge, internal, _, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    x, dual, mesons, fundamental, spaces, quadratic = projected_space(gauge, internal, color, weak, y, records)
    check_old_cubic(spaces)
    maps = internal_maps(x, dual, y)
    completion = flavor_operators(spaces, fundamental, y, maps, weak, records)
    family = family_units(mesons)
    charges = sorted({int(weight[-1]) for weight in spaces})
    filter_charges = sorted({int(charge) for charge in y if charge})
    targets = sorted({tuple(leg[0] for leg in term) for term in completion['operator_legs']})
    filters = charge_filters(filter_charges, targets)
    family_degrees = {key: 2 * max(len(item['word']) for item in value) for key, value in family.items()}
    internal_degrees = {'I': 0, 'E': 2, 'O': 2, 'C': 2 + family_degrees['1,0']}
    powers = {tuple(item['target']): max(sum(row[key] for key in
              ('first_A_power', 'second_A_power', 'third_A_power')) for row in item['monomials'])
              for item in filters}
    maximum = max(3 + powers[tuple(leg[0] for leg in term)]
                  + sum(internal_degrees[mode] + family_degrees[f'{i},{source}']
                        for i, (_, mode, source) in enumerate(term))
                  for term in completion['operator_legs'])
    assert maximum == 31
    return dict(status='PASS', original_light_cubic='identically zero on 49 uneaten components',
                family_matrix_unit_words=family, light_six_Y=charges,
                filter_six_Y=filter_charges, charge_filters=filters,
                maximum_operator_degree=maximum,
                direct_baryon_quartic_filter=['QQQL', 'QQQH_d', 'U^cU^cD^cE^c'],
                completion=completion,
                heavy_triplet_exchange=colored_exchange(x, mesons, fundamental, spaces, quadratic,
                                                        internal, weak, y, maps, records, completion))


if __name__ == '__main__':
    result = calculate()
    (flat.ROOT / OUT).write_text(json.dumps(result, indent=2, default=int) + '\n', encoding='utf-8')
