"""A different field-lattice Z2 action removes the previous Higgs locking.

Exhaust all4^9 characters with fixed candidate family/Higgs charges, then
construct a canonical D-flat two-hidden-doublet-flavor branch. Its gauge
mass Gram leaves only hypercharge among U1^9 plus hidden su2. No F-flatness
or global gauge/axion completion is claimed.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from math import gcd, prod
import gzip, hashlib, json
import numpy as np
import sympy as S
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/w33_pass11796_parity_complete_abelian_higgs.json'


def inputs():
    w = json.loads((ROOT / 'data/w33_20261009_corrected_assignment_dflat_certificate.json').read_text())
    prior = json.loads((ROOT / 'data/w33_pass11793_order_four_matter_action.json').read_text())
    fields = {r['name']: r for r in json.loads(gzip.decompress(
        (ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))[w['model']]['left']}
    q = {n: S.Matrix(r['q']).applyfunc(S.Rational) for n, r in fields.items()}
    inverse = S.Matrix(prior['integral_charge_lattice_basis']).applyfunc(S.Rational).inv()
    coords = {n: inverse * v * prior['lattice_denominator'] for n, v in q.items()}
    assert all(z.q == 1 for v in coords.values() for z in v)
    roles = {n: (0 if role.startswith('H') else 2)
             for role, fs in prior['candidate_three_family_Higgs_basis'].items() for n in fs}
    roles.update({n: 2 for n in w['physical_family_constraints']})
    return w, prior, fields, q, coords, roles


def character_census(fields, q, coords, roles):
    matrix = np.array([list(map(int, coords[n])) for n in roles], dtype=np.int64)
    targets = np.array(list(roles.values()), dtype=np.int64)
    hits = []
    # Complete radix-four universe, with bounded memory; all arithmetic
    # entries are integers well inside int64, before exact mod4 reduction.
    for prefix in product(range(4), repeat=3):
        candidates = np.array([prefix + tail for tail in product(range(4), repeat=6)], dtype=np.int64)
        good = np.all((candidates @ matrix.T) % 4 == targets, axis=1)
        hits.extend(candidates[good].tolist())
    assert len(hits) == 64
    smith = smith_normal_form(S.Matrix(matrix.tolist()), domain=S.ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(9)]
    assert np.prod([gcd(z, 4) for z in diagonal]) == 64
    singlets = [n for n, f in fields.items() if f['dim'] == '1,1,1,1' and q[n][1] == 0]
    classes = {}
    for char in hits:
        fixed = tuple(n for n in singlets if sum(a * b for a, b in zip(char, coords[n])) % 4 == 0)
        classes.setdefault(fixed, []).append(char)
    rows = []
    for fixed, chars in classes.items():
        mat = S.Matrix.hstack(*(q[n] for n in fixed))
        null = mat.T.nullspace()
        obstruction = next((v / v[0] for v in null if v[0] != 0), None)
        fi_possible = obstruction is None
        if obstruction is not None:
            assert obstruction[0] == 1 and mat.T * obstruction == S.zeros(len(fixed), 1)
        positive = None
        if fi_possible:
            positive = {'n_17': S.Rational(9, 74), 'n_47': S.Rational(9, 74),
                        'n_50': S.Rational(9, 37), 'n_80': S.Rational(9, 37), 'n_82': S.Rational(9, 37)}
            assert set(positive) <= set(fixed)
            assert sum((v * q[n] for n, v in positive.items()), S.zeros(9, 1)) == S.Matrix([-1] + [0] * 8)
        rows.append(dict(characters=chars, fixed_singlets=list(fixed), charge_rank=mat.rank(),
                         FI_vector_in_charge_span=fi_possible,
                         positive_FI_witness=None if positive is None else {n: str(z) for n, z in positive.items()},
                         exact_FI_annihilator=None if obstruction is None else [str(z) for z in obstruction]))
    assert len(rows) == 4 and sorted(r['charge_rank'] for r in rows) == [6, 6, 7, 7]
    return dict(universe=4**9, matching_characters=len(hits),
                full_field_action_orders=dict(Counter(4 // gcd(4, *c) for c in hits)),
                smith_diagonal=diagonal, fixed_singlet_classes=rows)


def vevs(s, u, t):
    return {'n_17': S.Rational(9, 74), 'n_47': S.Rational(9, 74),
            'n_50': S.Rational(9, 37), 'n_80': S.Rational(9, 37), 'n_82': S.Rational(9, 37),
            'n_9': s, 'n_54': s, 'n_37': u, 'n_38': u,
            'n_35': t, 'n_36': t, 'n_39': t, 'n_40': t}


PAULI = [S.Matrix([[0, 1], [1, 0]]), S.Matrix([[0, -S.I], [S.I, 0]]), S.diag(1, -1)]
ORIENTATION = {'n_35': 0, 'n_36': 1, 'n_39': 1, 'n_40': 0}


def mass_gram(q, norms, rotation=None):
    gram = S.zeros(12)
    rotation = S.eye(2) if rotation is None else rotation
    for n, norm in norms.items():
        if n in ORIENTATION:
            vec = rotation[:, ORIENTATION[n]]
            action = S.Matrix.hstack(*[z * vec for z in q[n]], *[a * vec for a in PAULI])
        else:
            action = S.Matrix([[*q[n], 0, 0, 0]])
        gram += norm * (action.conjugate().T * action).applyfunc(S.re)
    return gram


def certificate():
    w, prior, fields, q, coords, roles = inputs()
    census = character_census(fields, q, coords, roles)
    eps2 = [0, 0, 1, 0, 1, 0, 0, 0, 0]
    parity = {n: int(sum(a * b for a, b in zip(eps2, coords[n]))) % 2 for n in fields}
    assert set(parity.values()) == {0, 1}
    odd_components, instantons = 0, [0] * 4
    for n, field in fields.items():
        ds = [abs(int(z)) for z in field['dim'].split(',')]
        odd_components += parity[n] * prod(ds)
        for i, dim in enumerate(ds):
            if dim != 1:
                assert dim == [3, 2, 4, 2][i]  # all nontrivial irreps here are fundamental
                instantons[i] += parity[n] * prod(ds[:i] + ds[i + 1:])
    assert instantons == [14, 18, 6, 10] and odd_components == 144
    assert all(parity[n] == z // 2 for n, z in roles.items())
    s, u, t = S.symbols('s u t', nonnegative=True)
    norms = vevs(s, u, t)
    assert all(parity[n] == 0 and q[n][1] == 0 for n in norms)
    assert all(fields[n]['dim'] == ('1,1,1,2' if n in ORIENTATION else '1,1,1,1') for n in norms)
    balance = sum((z * q[n] for n, z in norms.items()), S.zeros(9, 1)).applyfunc(S.simplify)
    assert balance == S.Matrix([-1] + [0] * 8)
    moment = sum((t * S.eye(2)[:, i] * S.eye(2)[:, i].T for i in ORIENTATION.values()), S.zeros(2))
    assert moment == 2 * t * S.eye(2)
    assert q['n_35'] + q['n_36'] == S.zeros(9, 1)
    assert q['n_39'] == q['n_35'] and q['n_40'] == q['n_36']
    neutral = [n for n in norms if n not in ORIENTATION]
    assert S.Matrix.hstack(*(q[n] for n in neutral)).rank() == 7
    assert S.Matrix.hstack(*(q[n] for n in norms)).rank() == 8
    sample = vevs(S.Rational(1, 10), S.Rational(1, 10), S.Rational(1, 10))
    gram = mass_gram(q, sample)
    assert gram.rank() == 11 and gram.nullspace() == [S.Matrix([0, 1] + [0] * 10)]
    onepair = {n: z for n, z in sample.items() if n not in ('n_39', 'n_40')}
    assert mass_gram(q, onepair).rank() == 10
    r = S.Matrix([[S.Rational(3, 5), 4 * S.I / 5], [4 * S.I / 5, S.Rational(3, 5)]])
    assert r.conjugate().T * r == S.eye(2) and r.det() == 1
    assert mass_gram(q, sample, r).rank() == 11
    # Strict principal minor is an exact independent positivity/rank witness:
    # the Gram is a sum of squared actions with positive weights.
    massive = [i for i in range(12) if i != 1]
    det = gram.extract(massive, massive).det()
    assert det > 0
    singlet_q = S.Matrix.hstack(*(q[n] for n in neutral))
    chi = singlet_q.T.nullspace()[1] * S.Rational(5, 36)
    assert (chi.T * q['q_1'])[0] == -1 and (chi.T * q['n_35'])[0] == -5
    chi_roles = {n: str((chi.T * q[n])[0]) for n in roles}
    legacy_conflict = {n: parity[n] for n in w['positive_support']}
    assert legacy_conflict['n_19'] == legacy_conflict['n_56'] == 1
    family = prior['candidate_three_family_Higgs_basis']
    operators = {'Yukawa_u': ['Q', 'u_c', 'H_u'], 'Yukawa_d': ['Q', 'd_c', 'H_d'],
                 'Yukawa_e': ['L', 'e_c', 'H_d'], 'mu': ['H_u', 'H_d'],
                 'udd': ['u_c', 'd_c', 'd_c'], 'LQd': ['L', 'Q', 'd_c'],
                 'LLe': ['L', 'L', 'e_c'], 'LHu': ['L', 'H_u'],
                 'QQQL': ['Q', 'Q', 'Q', 'L'], 'uude': ['u_c', 'u_c', 'd_c', 'e_c']}
    selection = {name: sum(parity[family[role][0]] for role in rs) % 2 for name, rs in operators.items()}
    return dict(schema='w33.pass11796.parity_higgs.v1', status='PASS', model=w['model'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
        input_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n') if p.suffix == '.json' else p.read_bytes()).hexdigest() for p in
                      [ROOT / 'data/w33_20261009_corrected_assignment_dflat_certificate.json',
                       ROOT / 'data/w33_pass11793_order_four_matter_action.json',
                       ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz']},
        census=census, primitive_order_two_character=eps2, all176_field_parities=parity,
        field_parity_counts=dict(Counter(parity.values())), selected_light_field_parities={n: parity[n] for n in roles},
        nonabelian_fundamental_instanton_odd_zero_mode_counts=instantons,
        odd_chiral_component_count=odd_components,
        anomaly_boundary='All four nonabelian unit-instanton parity phases are+1 on the176field spectrum. Even total odd-component count is recorded only; global mixed Abelian/discrete/axion and gravitational completion is not inferred.',
        legacy_six_support_parities=legacy_conflict,
        prior='Parallel3fdef4a22 owns assignment-aware ledger/BL. Pass11793 owns field charge lattice and proves no matching order2 with its fixed six VEVs. This chooses another character AND another support; no prior certificate is contradicted.',
        symbolic_squared_VEV_norms={n: str(z) for n, z in norms.items()},
        parameter_domain='s,u,t>0; FI-normalized canonical kinetic convention',
        hidden_doublet_orientations=ORIENTATION,
        FI_balance=[str(z) for z in balance], SU2_moment_matrix='2*t*I2, hence all three traceless D terms zero',
        neutral_singlet_charge_rank=7, all_support_abelian_charge_rank=8,
        full_gauge_mass_Gram=[[str(z) for z in row] for row in gram.tolist()],
        gauge_mass_rank=11, gauge_Lie_dimension=12,
        massive_principal_minor_determinant=str(det),
        gauge_kernel=['hypercharge'], one_doublet_pair_mass_rank=10,
        second_complex_SU2_realization_mass_rank=11,
        connected_unbroken_Lie_algebra='visible su3+su2+u1Y and hidden su4; no additional Abelian Lie generator in this canonical Higgs calculation',
        pre_doublet_visible_chi_covector=[str(z) for z in chi], pre_doublet_visible_chi_charges=chi_roles,
        mechanism='One pair of chi-opposite doublets permits a locked continuous chi/hidden Cartan. Two negative-chi doublets occupy both hidden colors; cancellation would require a nonzero scalar traceless su2 matrix. The second independent pair removes that locking. Exact full mass Gram proves it.',
        operator_parities=selection,
        F_term_boundary='The doublet meson n35*n36 is gauge-neutral and has twist sum0; symmetry does not prove a zero coefficient. The enlarged support requires actual worldsheet/R/oscillator and coefficient/cancellation analysis. No F-flatness or supersymmetric vacuum is certified.',
        scope='Exact full176field-lattice order2 representation, canonical classical D-flat branch and Higgs kernel. This is not yet a globally consistent discrete gauge symmetry with axion/Stueckelberg/anomaly completion or a physical MSSM vacuum. Hidden su4 remains, exotic mass ranks and Yukawa coefficients uncomputed; QQQL/uude allowed. No physical scales, gravity or TOE claimed.',
        literature=['https://arxiv.org/abs/0708.2691', 'https://arxiv.org/abs/hep-th/9506098'])


if __name__ == '__main__':
    result = certificate()
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print('11796 PASS64 characters in4^9; full-field Z2 and13field D-flat support; rank11/12 mass Gram leaves onlyY')
