"""Native north-pole W33 triplet masses and an exact rephasing obstruction."""

import json
from itertools import permutations

import numpy as np
import sympy as sp

import toe_20261113_canonical_strong_cp as strong
import toe_20261113_monopole_adjoint_phase as adjoint_phase


flavor = strong.flavor
flat = flavor.flat
neutral = adjoint_phase.neutral
OUT = flat.ROOT / 'data/toe_20261113_monopole_triplet_mass.json'
WEIGHTS = ((0, 1, 0, -2), (0, 0, 1, 3))


def exact_power_sums(base, change, inverse_rows, inverse_cols):
    fixed = base-change
    pencil = {
        -1: inverse_rows*fixed*inverse_cols*change.T,
        0: inverse_rows*(fixed*inverse_cols*fixed.T+change*inverse_cols*change.T),
        1: inverse_rows*change*inverse_cols*fixed.T,
    }
    powers = {0: sp.eye(base.rows)}
    result = []
    for _ in range(4):
        product = {}
        for i, first in powers.items():
            for j, second in pencil.items():
                exponent = i+j
                value = first*second
                product[exponent] = product[exponent]+value if exponent in product else value
        powers = {key: value for key, value in product.items() if any(value)}
        traces = {key: sp.trace(value) for key, value in sorted(powers.items())}
        result.append({key: value for key, value in traces.items() if value})
    return result


def directions(indices, adjoint):
    matter = np.zeros((len(indices), 405), dtype=adjoint.dtype)
    internal = np.zeros((len(indices), 27, 27), dtype=adjoint.dtype)
    slots = np.flatnonzero(indices < 405)
    matter[slots, indices[slots]] = 1
    adjoint_slots = np.flatnonzero(indices >= 405)
    internal[adjoint_slots] = adjoint[indices[adjoint_slots]-405]
    return matter.reshape(-1, 5, 27, 3), internal


def omega_hessian(background, left, right, records):
    """Second jet of a cubic whose background legs lie in the neutral plane."""
    indices, signs = records[:, :3], records[:, 3]
    result = np.zeros((len(left[0]), len(right[0])), dtype=np.result_type(*background))
    for i, j, k in permutations(range(3)):
        vector = background[k].ravel()[indices[:, k]]*signs
        support = vector != 0
        row = left[i].reshape(len(left[i]), 81)[:, indices[support, i]]
        col = right[j].reshape(len(right[j]), 81)[:, indices[support, j]]
        result += (row*vector[support]) @ col.T
    return result


def omega_value(legs, records):
    indices, signs = records[:, :3], records[:, 3]
    return np.sum(signs * np.prod([leg.ravel()[indices[:, i]] for i, leg in enumerate(legs)], axis=0))


def mesons(matter):
    return [matter[k].T @ matter[3+j] for j in range(2) for k in range(3)]


def assert_neutral_legs(records):
    # A pair of neutral internal indices never occurs in the native cubic.
    assert np.max(np.sum(records[:, :3] < 6, axis=1)) == 1


def split_mass(a, matter, meson, zero_charge, left, right, records):
    polynomial = a @ a-zero_charge**2*np.eye(27, dtype=a.dtype)

    def jet(direction):
        fields, delta = direction
        return (fields[:, 0], fields[:, 1],
                ((a @ delta+delta @ a) @ matter[0]+polynomial @ fields[:, 0]) @ meson.T)

    third = polynomial @ matter[0] @ meson.T
    return -omega_hessian((matter[0], matter[1], third), jet(left), jet(right), records)


def ordinary_mass(a, matter, left, right, records, words):
    dl, al = left
    dr, ar = right
    result = -omega_hessian(matter[:3], dl.transpose(1, 0, 2, 3)[:3],
                            dr.transpose(1, 0, 2, 3)[:3], records)
    for j, k in neutral.trial.MIXED:
        pairs = ((dl[:, 3+j], a @ dr[:, k]), (a @ dl[:, k], dr[:, 3+j]),
                 (dl[:, 3+j], ar @ matter[k]), (al @ matter[k], dr[:, 3+j]),
                 (al.transpose(0, 2, 1) @ matter[3+j], dr[:, k]),
                 (dl[:, k], ar.transpose(0, 2, 1) @ matter[3+j]))
        for row, col in pairs:
            result += np.einsum('ria,cia->rc', row, col)
    for i in np.flatnonzero(np.any(ar, axis=(1, 2))):
        derivative = adjoint_phase.trace_derivative(a, ar[i])
        result[:, i] += np.einsum('rij,ji->r', al, derivative)
    ms = mesons(matter)
    for term in words:
        word = term['meson_trace']
        product = np.eye(3, dtype=a.dtype)
        for label in word:
            product = product @ ms[label]
        shift = np.trace(product)-term['center']
        for index, label in enumerate(word):
            j, k = divmod(label, 3)
            cyclic = np.eye(3, dtype=a.dtype)
            for other in word[index+1:]+word[:index]:
                cyclic = cyclic @ ms[other]
            result += shift*(np.einsum('ab,rib,cia->rc', cyclic, dl[:, k], dr[:, 3+j])
                             + np.einsum('ab,cib,ria->rc', cyclic, dr[:, k], dl[:, 3+j]))
    return result


def tensor_and_rules(fixture):
    cubic = flat.vacuum.cubic
    tensor = np.zeros((27, 27, 27), dtype=np.int64)
    for triple, sign in cubic.signed_terms(cubic.CUBIC).items():
        for indices in permutations(triple):
            tensor[indices] = sign
    units = {key: [(term['word'], float(sp.Rational(term['coefficient']))) for term in terms]
             for key, terms in fixture['family_matrix_unit_words'].items()}
    filters = {tuple(entry['target']): entry['monomials'] for entry in fixture['charge_filters']}
    operators = []
    for legs in fixture['completion']['operator_legs']:
        rules = filters[tuple(leg[0] for leg in legs)]
        for term in rules:
            powers = (term['first_A_power'], term['second_A_power'], term['third_A_power'])
            keys = tuple((index, leg[1], leg[2], p) for index, (leg, p) in enumerate(zip(legs, powers)))
            operators.append((float(sp.Rational(term['coefficient'])), keys))
    return tensor, units, operators


def dressed_background(a, matter, rules):
    tensor, units, operators = rules
    ms = mesons(matter)
    family = {}
    for key, terms in units.items():
        value = np.zeros((3, 3), dtype=a.dtype)
        for word, coefficient in terms:
            product = np.eye(3, dtype=a.dtype)
            for letter in word:
                product = product @ ms[letter]
            value += coefficient*product
        family[key] = value
    cross_family = family['1,0']
    identity = np.eye(27, dtype=a.dtype)
    d = np.einsum('vwj,wa->vja', tensor, matter[0], optimize=True)
    dd = np.einsum('iuv,ua->iva', tensor, matter[3], optimize=True)
    exotic = contract_internal(dd, d)
    cross = contract_internal(dd, d @ cross_family.T)
    maps = {'I': identity, 'E': exotic, 'O': identity-exotic, 'C': cross}
    keys = set(key for _, group in operators for key in group)
    max_power = max(key[-1] for key in keys)
    background = [matter[0]]
    for _ in range(max_power):
        background.append(a @ background[-1])
    base = {key: maps[mode] @ background[p] @ family[f'{index},{source}'].T
            for key in keys for index, mode, source, p in (key,)}
    return family, maps, keys, background, base, d, dd


def contract_internal(dual_tensor, fundamental_tensor):
    leading = fundamental_tensor.shape[:-3]
    dual = dual_tensor.reshape(dual_tensor.shape[:-3]+(27, 81))
    fundamental = fundamental_tensor.swapaxes(-1, -2).reshape(leading+(81, 27))
    return dual @ fundamental


def dressed_mass(a, matter, left, right, records, rules):
    tensor, _, operators = rules
    family, maps, keys, background, base, d, dd = dressed_background(a, matter, rules)
    cross_family = family['1,0']
    zero = np.zeros((27, 27), dtype=a.dtype)
    max_power = len(background)-1

    def jets(direction):
        fields, delta = direction
        d1 = np.einsum('vwj,nwa->nvja', tensor, fields[:, 0], optimize=True)
        dd1 = np.einsum('iuv,nua->niva', tensor, fields[:, 3], optimize=True)
        e1 = contract_internal(dd1, d)+contract_internal(dd, d1)
        c1 = (contract_internal(dd1, d @ cross_family.T)
              + contract_internal(dd, d1 @ cross_family.T))
        derivatives = {'I': zero, 'E': e1, 'O': -e1, 'C': c1}
        powers = [fields[:, 0]]
        for p in range(max_power):
            powers.append(a @ powers[-1]+delta @ background[p])
        return {key: (maps[mode] @ powers[p]+derivatives[mode] @ background[p])
                @ family[f'{index},{source}'].T for key in keys for index, mode, source, p in (key,)}

    assert all(not leg[2:].any() for leg in base.values())
    jl, jr = jets(left), jets(right)
    result = np.zeros((len(left[0]), len(right[0])), dtype=a.dtype)
    for coefficient, group in operators:
        result += coefficient*omega_hessian([base[key] for key in group],
                                            [jl[key] for key in group],
                                            [jr[key] for key in group], records)
    return result


def direct_superpotential(a, matter, records, words, rules):
    a2 = a @ a
    a4 = a2 @ a2
    fixed = np.trace(a4 @ a2)/6-3*np.trace(a4 @ a)/5-283*np.trace(a2)/2
    fixed -= omega_value(matter[:3], records)
    for j, k in neutral.trial.MIXED:
        fixed += np.sum(matter[3+j]*(a @ matter[k]))
    family = mesons(matter)
    for term in words:
        word = np.eye(3, dtype=a.dtype)
        for label in term['meson_trace']:
            word = word @ family[label]
        fixed += (np.trace(word)-term['center'])**2/2
    identity = np.eye(27, dtype=a.dtype)
    fixed -= omega_value((matter[0], matter[1], (a2-4*identity) @ matter[0] @ family[1].T), records)
    varying = -omega_value((matter[0], matter[1], (a2-9*identity) @ matter[0] @ family[5].T), records)
    _, _, _, _, legs, _, _ = dressed_background(a, matter, rules)
    dressed = sum(coefficient*omega_value([legs[key] for key in keys], records)
                  for coefficient, keys in rules[2])
    return np.array([fixed, varying, dressed])


def check_directional_jet(a, matter, left, right, records, words, rules):
    rng = np.random.default_rng(774)
    row = rng.normal(size=len(left[0]))
    col = rng.normal(size=len(right[0]))
    row /= np.linalg.norm(row)
    col /= np.linalg.norm(col)
    lm, la = (np.tensordot(row, data, axes=1) for data in left)
    rm, ra = (np.tensordot(col, data, axes=1) for data in right)
    fixed, varying, dressed = holomorphic_masses(a, matter, left, right, records, words, rules)
    expected = np.array([row @ matrix @ col for matrix in (fixed-dressed, varying, dressed)])
    eps = 3e-4
    measured = sum(i*j*direct_superpotential(a+eps*(i*la+j*ra), matter+eps*(i*lm+j*rm),
                                             records, words, rules)
                   for i in (1, -1) for j in (1, -1))/(4*eps**2)
    np.testing.assert_allclose(measured, expected, atol=2e-4, rtol=2e-5)
    return float(np.max(np.abs(measured-expected)))


def holomorphic_masses(a, matter, left, right, records, words, rules):
    assert not np.any(matter[:, 2:]) and not np.any(a[:2, 2:]) and not np.any(a[2:, :2])
    family = mesons(matter)
    phase_piece = split_mass(a, matter, family[5], 3, left, right, records)
    fixed = ordinary_mass(a, matter, left, right, records, words)
    fixed += split_mass(a, matter, family[1], 2, left, right, records)
    dressed = dressed_mass(a, matter, left, right, records, rules)
    return fixed+dressed, phase_piece, dressed


def profile_fields(state, embedding):
    a = np.einsum('a,aij->ij', state[1:8], embedding)
    np.testing.assert_allclose(a[:2, 2:], 0., atol=1e-12)
    np.testing.assert_allclose(a[2:, :2], 0., atol=1e-12)
    a[:2, 2:] = a[2:, :2] = 0.
    matter = np.zeros((5, 27, 3), dtype=a.dtype)
    matter[:, :2] = np.array(state[8:]).reshape(5, 2, 3)
    return a, matter


def normalize_rows(data):
    gram = data @ data.T
    return np.linalg.solve(np.linalg.cholesky(gram), data)


def normalize_chiral(direction):
    matter, adjoint = direction
    data = normalize_rows(np.column_stack((matter.reshape(-1, 405), adjoint.reshape(-1, 729))))
    return data[:, :405].reshape(-1, 5, 27, 3), data[:, 405:].reshape(-1, 27, 27)


def chiral_action(generator, direction):
    matter, a = direction
    transform = np.empty_like(matter)
    transform[:, :3] = generator @ matter[:, :3]
    transform[:, 3:] = -generator.T @ matter[:, 3:]
    return transform, generator @ a-a @ generator


def adjoint_action(generator, directions):
    return generator @ directions-directions @ generator


def gauge_mass(a, matter, chiral, gauginos):
    fields, internal = chiral
    result = np.zeros((len(fields), len(gauginos)), dtype=a.dtype)
    adjoint = a.conj().T
    for j, generator in enumerate(gauginos):
        result[:, j] = -np.einsum('tia,ntia->n', matter[:3].conj(), generator @ fields[:, :3])
        result[:, j] += np.einsum('tia,ntia->n', matter[3:].conj(), generator.T @ fields[:, 3:])
        result[:, j] += np.einsum('nij,ji->n', internal, generator @ adjoint-adjoint @ generator)
    return result


def mass_evaluator(left, right, gaugino_left, gaugino_right, records, words, rules):
    def evaluate(a, matter):
        fixed, change, _ = holomorphic_masses(a, matter, left, right, records, words, rules)
        gauge_right = gauge_mass(a, matter, left, gaugino_right)
        gauge_left = gauge_mass(a, matter, right, gaugino_left)
        zeros = np.zeros((len(gaugino_left), len(gaugino_right)), dtype=a.dtype)
        return (np.block([[fixed, gauge_right], [gauge_left.T, zeros]]),
                np.pad(change, ((0, len(gaugino_left)), (0, len(gaugino_right)))))
    return evaluate


def doublet_frames(adjoint, weights, step):
    w = np.array(WEIGHTS[0])

    def bases(weight):
        chiral = normalize_chiral(directions(np.flatnonzero((weights == weight).all(axis=1)), adjoint))
        roots = adjoint[(weights[405:] == weight).all(axis=1)]
        gaugino = normalize_rows(roots.reshape(-1, 729)).reshape(-1, 27, 27)
        return chiral, gaugino

    left, gleft = bases(-w)
    right, gright = bases(w)
    left_lower = chiral_action(-step, left)
    right_lower = chiral_action(step.T, right)
    gleft_lower = adjoint_action(-step, gleft)
    gright_lower = adjoint_action(step.T, gright)
    for matter, internal in (left_lower, right_lower):
        gram = np.einsum('ntia,mtia->nm', matter, matter)+np.einsum('nij,mij->nm', internal, internal)
        np.testing.assert_allclose(gram, np.eye(len(matter)), atol=1e-12)
    for internal in (gleft_lower, gright_lower):
        np.testing.assert_allclose(np.einsum('nij,mij->nm', internal, internal),
                                   np.eye(len(internal)), atol=1e-12)
    shape = (len(left[0])+len(gleft), len(right[0])+len(gright))
    assert sum(shape) == 49
    return ((left, right, gleft, gright), (left_lower, right_lower, gleft_lower, gright_lower)), shape


def doublet_evaluators(adjoint, weights, step, records, words, rules):
    (plus, minus), shape = doublet_frames(adjoint, weights, step)
    return (mass_evaluator(*plus, records, words, rules),
            mass_evaluator(*minus, records, words, rules), shape)


def radial_hamiltonian(plus, minus, k_over_r):
    row_dim, col_dim = plus.shape
    exchange = np.array([[0, 1], [1, 0]])
    skew = np.array([[0, 1], [-1, 0]])
    flux_left = -np.kron(exchange, np.eye(col_dim))
    flux_right = np.kron(exchange, np.eye(row_dim))
    gauge_left = 1j*k_over_r*np.kron(skew, np.eye(col_dim))
    gauge_right = -1j*k_over_r*np.kron(skew, np.eye(row_dim))
    mass = np.kron(np.eye(2), (plus+minus)/2)-np.kron(exchange, (plus-minus)/2)
    flux = np.block([[flux_left, np.zeros_like(mass.T)], [np.zeros_like(mass), flux_right]])
    potential = np.block([[gauge_left, mass.conj().T], [mass, gauge_right]])
    return flux, potential


def radial_model():
    _, adjoint, cartan, color, weak, y = flat.compact_chart()
    roots = (color[0], color[1], weak)
    charges = [(root @ root.T-root.T @ root).diagonal() for root in roots]+[y]
    weights = np.stack([flat.field_charges(adjoint, h) for h in charges], axis=1)
    core = adjoint_phase.core
    five = core.topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    step, _ = core.monopole_root(adjoint, five)
    records = np.array(flat.vacuum.native.build_records())
    words = flat.read(flat.OUT)['repair']['centered_trace_squared_terms']
    rules = tensor_and_rules(flat.read(flavor.OUT))
    plus, minus, _ = doublet_evaluators(adjoint, weights, step, records, words, rules)
    embedding = neutral.geometry()[0]
    matter = np.concatenate(flat.repair_vevs()).reshape(5, 27, 3).astype(float)
    return embedding, (plus, minus), (np.diag(y).astype(float), matter)


def calculate():
    gauge, adjoint, cartan, color, weak, y = flat.compact_chart()
    records = np.array(flat.vacuum.native.build_records())
    assert_neutral_legs(records)
    x, dual, ms, _, _, (hessian, orbit, weights) = flavor.projected_space(
        gauge, adjoint, color, weak, y, records.tolist())
    triplet_mesons = list(ms)
    triplet_mesons[1] = np.zeros_like(ms[1])
    split = flat.split_exotic_hessian(x, y, triplet_mesons, records.tolist(), orbit)
    flattened = adjoint.reshape(78, -1)
    metric = sp.diag(sp.eye(405), sp.Matrix(flattened @ flattened.T))
    base, rows, cols = strong.weight_block(hessian, weights, WEIGHTS[0])
    change, _, _ = strong.weight_block(split, weights, WEIGHTS[0])
    r, c = list(map(int, rows)), list(map(int, cols))
    gram_left, gram_right = metric.extract(r, r), metric.extract(c, c)
    traces = exact_power_sums(base, change, gram_left.inv(), gram_right.inv())
    assert traces[:3] == [{0: sp.Rational(1577, 3)}, {0: sp.Rational(634543, 9)},
                          {0: sp.Rational(334701971, 27)}]
    assert traces[3] == {-2: -sp.Rational(200, 3), 0: sp.Rational(191325201055, 81),
                         2: -sp.Rational(200, 3)}
    assert not any(strong.weight_block(split, weights, WEIGHTS[1])[0])
    negative_rows = [44, 59, 125, 140, 204, 220, 315, 316, 398]
    negative_cols = [74, 155, 234, 235, 285, 301, 368, 383, 407]
    assert set(negative_rows) <= set(r) and set(negative_cols) <= set(c)
    sign_left = sp.diag(*(-1 if i in negative_rows else 1 for i in r))
    sign_right = sp.diag(*(-1 if i in negative_cols else 1 for i in c))
    assert sign_left*gram_left*sign_left == gram_left
    assert sign_right*gram_right*sign_right == gram_right
    assert sign_left*(base-change)*sign_right == base-change
    assert sign_left*change*sign_right == -change

    rule = tensor_and_rules(flat.read(flavor.OUT))
    words = flat.read(flat.OUT)['repair']['centered_trace_squared_terms']
    embedding = neutral.geometry()[0]
    profile = flat.read(neutral.OUT)
    vacuum_matter = np.concatenate((x, dual)).reshape(5, 27, 3)
    results = []
    for weight in WEIGHTS:
        expected, rows, cols = strong.weight_block(hessian, weights, weight)
        expected_split, _, _ = strong.weight_block(split, weights, weight)
        left, right = directions(rows, adjoint), directions(cols, adjoint)

        vacuum_fixed, vacuum_phase, _ = holomorphic_masses(
            np.diag(y).astype(float), vacuum_matter.astype(float), left, right, records, words, rule)
        np.testing.assert_allclose(vacuum_fixed+vacuum_phase, np.array(expected, dtype=float), atol=1e-9)
        np.testing.assert_allclose(vacuum_phase, np.array(expected_split, dtype=float), atol=1e-9)
        radial = []
        for radius, state in zip(profile['probe_radii'], profile['normalized_profile_samples']):
            a, matter = profile_fields(state, embedding)
            fixed, phase_piece, dressed = holomorphic_masses(a, matter, left, right, records, words, rule)
            radial.append(dict(radius=radius,
                               phase_piece_rank=int(np.linalg.matrix_rank(phase_piece, tol=1e-8)),
                               phase_piece_frobenius=float(np.linalg.norm(phase_piece)),
                               dressed_frobenius=float(np.linalg.norm(dressed)),
                               fixed_frobenius=float(np.linalg.norm(fixed))))
        probe = profile_fields(profile['normalized_profile_samples'][5], embedding)
        derivative_error = check_directional_jet(*probe, left, right, records, words, rule)
        results.append(dict(weight=list(weight), chiral_shape=list(expected.shape), radial=radial,
                            directional_second_difference_error=derivative_error))

    core = adjoint_phase.core
    five = core.topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    step, _ = core.monopole_root(adjoint, five)
    plus, minus, shape = doublet_evaluators(adjoint, weights, step, records, words, rule)
    real_mesh = flat.read('data/toe_20261113_monopole_adjoint_shooting_mesh.json')[-1]
    origin = profile_fields(real_mesh['state'][0], embedding)
    at_origin = [f(*origin) for f in (plus, minus)]
    np.testing.assert_allclose(at_origin[0], at_origin[1], atol=1e-9)
    vacuum = np.diag(y).astype(float), vacuum_matter.astype(float)
    exterior = [f(*vacuum) for f in (plus, minus)]
    for fixed, change in exterior:
        holomorphic = fixed[:25, :22]+change[:25, :22]
        np.testing.assert_allclose(holomorphic.T @ fixed[:25, 22:], 0., atol=1e-9)
        np.testing.assert_allclose(holomorphic @ fixed[25:, :22].T, 0., atol=1e-9)
    exterior_ranks = [int(np.linalg.matrix_rank(a+b, tol=1e-9)) for a, b in exterior]
    assert sum(exterior_ranks) == 45
    probe = profile_fields(profile['normalized_profile_samples'][3], embedding)
    z = np.exp(.63j)
    local = [a+z*b for a, b in (f(*probe) for f in (plus, minus))]
    flux, potential = radial_hamiltonian(*local, 2.)
    assert flux.shape == (98, 98)
    np.testing.assert_allclose(flux @ flux, np.eye(98), atol=1e-13)
    np.testing.assert_allclose(potential, potential.conj().T, atol=1e-13)
    transfer = -1j * flux @ potential
    np.testing.assert_allclose(transfer.conj().T @ flux + flux @ transfer, 0., atol=1e-13)
    return dict(status='PASS',
                triplet_mass_squared_power_sums=[{str(k): str(v) for k, v in row.items()} for row in traces],
                whole_block_unitary_rephasing_excluded=True, north_pole_holomorphic_blocks=results,
                exterior_phase_sign_symmetry=dict(negative_row_coordinates=negative_rows,
                                                  negative_column_coordinates=negative_cols),
                paired_north_pole_shape=list(shape), angular_radial_dimension=98,
                exterior_mass_ranks=exterior_ranks, regular_origin_flux_slot_mass_agreement=True)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2)+'\n'
    OUT.write_text(result, encoding='utf-8')
    print(result)
