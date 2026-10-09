"""Independent finite-character and actual Higgs-kernel regression audits."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import gzip, hashlib, json, sys
import numpy as np
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import w33_pass11796_parity_complete_abelian_higgs as p


def frozen():
    return json.loads(p.OUT.read_text())


def test_independent_lattice_basis_and_all_order_two_actions():
    w, prior, fields, q, _, roles = p.inputs()
    den = prior['lattice_denominator']
    integral = S.Matrix.hstack(*(den * v for v in q.values()))
    assert all(z.q == 1 for z in integral)
    basis = hermite_normal_form(integral.applyfunc(int))
    assert basis == S.Matrix(prior['integral_charge_lattice_basis']).applyfunc(S.Rational)
    coords = {n: basis.inv() * den * v for n, v in q.items()}
    matches = []
    for bits in product(range(2), repeat=9):
        if all(sum(a * b for a, b in zip(bits, coords[n])) % 2 == z // 2 for n, z in roles.items()):
            matches.append(bits)
    assert len(matches) == 8
    eps = tuple(frozen()['primitive_order_two_character'])
    assert eps in matches
    charge = {n: int(sum(a * b for a, b in zip(eps, coords[n]))) % 2 for n in fields}
    assert charge == frozen()['all176_field_parities']
    assert list(charge.values()).count(1) == 76
    assert charge['n_19'] == charge['n_56'] == 1
    assert all(charge[n] == 0 for n in frozen()['symbolic_squared_VEV_norms'])


def test_independent_binary_lifting_counts_all_mod_four_solutions():
    _, _, _, _, coords, roles = p.inputs()
    # Enumerate epsilon=l+2h; l,h are binary, an independent enumeration
    # from the producer's radix-four prefix blocks.
    bits = np.array(list(product(range(2), repeat=9)), dtype=np.int64)
    matrix = np.array([list(map(int, coords[n])) for n in roles], dtype=np.int64)
    target = np.array(list(roles.values()), dtype=np.int64)
    high = (2 * bits @ matrix.T) % 4
    found = set()
    for low in bits:
        residue = (target - low @ matrix.T) % 4
        for h in bits[np.all(high == residue, axis=1)]:
            found.add(tuple(map(int, low + 2 * h)))
    j = frozen()['census']
    assert len(found) == 64 and j['universe'] == 262144
    stored = {tuple(v) for row in j['fixed_singlet_classes'] for v in row['characters']}
    assert found == stored
    assert sum(all(z % 2 == 0 for z in v) for v in found) == 8


def test_exact_FI_and_nonabelian_cancellation_in_raw_ledger():
    w, _, _, _, _, _ = p.inputs()
    rows = json.loads(gzip.decompress((ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))[w['model']]['left']
    fs = {r['name']: r for r in rows}
    for a, b, c in [(F(1, 10), F(1, 10), F(1, 10)), (F(2, 7), F(11, 19), F(3, 5))]:
        norms = {'n_17': F(9, 74), 'n_47': F(9, 74), 'n_50': F(9, 37),
                 'n_80': F(9, 37), 'n_82': F(9, 37), 'n_9': a, 'n_54': a,
                 'n_37': b, 'n_38': b, 'n_35': c, 'n_36': c, 'n_39': c, 'n_40': c}
        assert [sum(z * F(fs[n]['q'][i]) for n, z in norms.items()) for i in range(9)] == [-1] + [0] * 8
        assert all(F(fs[n]['q'][1]) == 0 for n in norms)
        assert all(fs[n]['dim'] == '1,1,1,2' for n in ['n_35', 'n_36', 'n_39', 'n_40'])
        v = [S.Matrix([1, 0]), S.Matrix([0, 1]), S.Matrix([0, 1]), S.Matrix([1, 0])]
        moment = sum((S.Rational(c.numerator, c.denominator) * x * x.T for x in v), S.zeros(2))
        assert moment - S.trace(moment) * S.eye(2) / 2 == S.zeros(2)


def test_independent_complexified_stabilizer_has_only_hypercharge():
    _, _, _, q, _, _ = p.inputs()
    # Use E12,E21,H, independent of the Hermitian Pauli mass basis.
    generators = [S.Matrix([[0, 1], [0, 0]]), S.Matrix([[0, 0], [1, 0]]), S.diag(1, -1)]
    rows = []
    for n in frozen()['symbolic_squared_VEV_norms']:
        if n in p.ORIENTATION:
            v = S.eye(2)[:, p.ORIENTATION[n]]
            action = S.Matrix.hstack(*(z * v for z in q[n]), *(a * v for a in generators))
            rows.extend(action.tolist())
        else:
            rows.append([*q[n], 0, 0, 0])
    matrix = S.Matrix(rows)
    assert matrix.rank() == 11
    assert matrix.nullspace() == [S.Matrix([0, 1] + [0] * 10)]
    gram = S.Matrix(frozen()['full_gauge_mass_Gram']).applyfunc(S.Rational)
    assert gram.rank() == 11 and gram.nullspace() == matrix.nullspace()
    assert gram.extract([0] + list(range(2, 12)), [0] + list(range(2, 12))).det() == S.Rational(frozen()['massive_principal_minor_determinant']) > 0


def test_one_pair_control_and_rotated_full_flavor_frame():
    _, _, _, q, _, _ = p.inputs()
    norms = p.vevs(S.Rational(1, 7), S.Rational(2, 11), S.Rational(3, 13))
    single = {n: z for n, z in norms.items() if n not in ('n_39', 'n_40')}
    assert p.mass_gram(q, single).rank() == 10
    # Another SU2 matrix, distinct from the producer's complex rotation.
    rot = S.Matrix([[S.Rational(5, 13), S.Rational(12, 13)], [-S.Rational(12, 13), S.Rational(5, 13)]])
    assert rot.T * rot == S.eye(2) and rot.det() == 1
    assert p.mass_gram(q, norms, rot).nullspace() == [S.Matrix([0, 1] + [0] * 10)]


def test_exact_singlet_span_and_FI_obstruction_certificates():
    _, _, _, q, _, _ = p.inputs()
    classes = frozen()['census']['fixed_singlet_classes']
    assert sorted(len(row['fixed_singlets']) for row in classes) == [28, 34, 36, 42]
    assert sorted(row['charge_rank'] for row in classes) == [6, 6, 7, 7]
    for row in classes:
        matrix = S.Matrix.hstack(*(q[n] for n in row['fixed_singlets']))
        assert matrix.rank() == row['charge_rank'] < 8
        if row['exact_FI_annihilator'] is not None:
            v = S.Matrix(row['exact_FI_annihilator']).applyfunc(S.Rational)
            assert v[0] == 1 and matrix.T * v == S.zeros(matrix.cols, 1)


def test_operator_selection_and_unproved_F_terms():
    j = frozen()
    assert all(j['operator_parities'][n] == 0 for n in ['Yukawa_u', 'Yukawa_d', 'Yukawa_e', 'mu', 'QQQL', 'uude'])
    assert all(j['operator_parities'][n] == 1 for n in ['udd', 'LQd', 'LLe', 'LHu'])
    _, _, fs, q, _, _ = p.inputs()
    assert q['n_35'] + q['n_36'] == S.zeros(9, 1)
    assert (int(fs['n_35']['k']) + int(fs['n_36']['k'])) % 6 == 0
    assert 'No F-flatness' in j['F_term_boundary'] and 'Stueckelberg' in j['scope']


def test_nonabelian_instanton_parity_phases_from_all_chiral_components():
    from math import prod
    _, _, fs, _, _, _ = p.inputs()
    j = frozen()
    counts = [0] * 4
    components = 0
    for n, f in fs.items():
        dimensions = [abs(int(z)) for z in f['dim'].split(',')]
        odd = j['all176_field_parities'][n]
        components += odd * prod(dimensions)
        for i, dim in enumerate(dimensions):
            if dim != 1:
                assert dim == [3, 2, 4, 2][i]
                counts[i] += odd * prod(dimensions[:i] + dimensions[i + 1:])
    assert counts == [14, 18, 6, 10] and all(z % 2 == 0 for z in counts)
    assert components == 144
    assert j['nonabelian_fundamental_instanton_odd_zero_mode_counts'] == counts


def test_normalized_source_and_input_provenance():
    j = frozen()
    assert j['source_sha256'] == hashlib.sha256(Path(p.__file__).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    for path, digest in j['input_sha256'].items():
        file = ROOT / path
        raw = file.read_bytes().replace(b'\r\n', b'\n') if file.suffix == '.json' else file.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
