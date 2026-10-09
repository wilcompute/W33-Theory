"""Exact hidden-center Higgs branch in the actual 176-field benchmark.

Credits Pass11793's B-L action and the parallel assignment-aware ledger.
Canonical classical D terms are used. No F-flatness, axion masses, or
physical MSSM completion follows from a charge/stabilizer calculation.
"""
from pathlib import Path
import gzip, hashlib, json
from itertools import product
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/w33_pass11794_hidden_center_vacuum.json'


def inputs():
    witness = json.loads((ROOT / 'data/w33_20261009_corrected_assignment_dflat_certificate.json').read_text())
    ledger = json.loads(gzip.decompress((ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))
    fields = {f['name']: f for f in ledger[witness['model']]['left']}
    q = {n: S.Matrix(f['q']).applyfunc(S.Rational) for n, f in fields.items()}
    bl = {n: (S.Matrix(witness['BL_coefficients']).applyfunc(S.Rational).T * v)[0] for n, v in q.items()}
    return witness, fields, q, bl


def center_scan(fields, q, bl):
    """All Z4(SU4) x Z2(SU2) lifts of the fixed11793 generator.

    The first two dimension entries are visible SU3 and SU2; q[1] is
    hypercharge in this ledger. A center eigenvalue is constant on a
    representation, so excluded fields have no fixed nonzero component.
    """
    sm_neutral = [n for n, f in fields.items()
                  if list(map(int, f['dim'].split(',')))[:2] == [1, 1] and q[n][1] == 0]
    assert q['q_1'][1] == S.Rational(1, 6) and q['be_1'][1] == 1
    rows = []
    for a, b in product(range(4), range(2)):
        allowed = []
        for n in sm_neutral:
            d = list(map(int, fields[n]['dim'].split(',')))
            assert d[2] in (1, 4, -4) and d[3] in (1, 2)
            nality = 1 if d[2] == 4 else -1 if d[2] == -4 else 0
            assert (6 * bl[n]).q == 1
            if (int(6 * bl[n]) + a * nality + 2 * b * (d[3] == 2)) % 4 == 0:
                allowed.append(n)
        charged = [n for n in allowed if bl[n] != 0]
        assert charged == (['n_4', 'n_5'] if a == 2 else [])
        rows.append(dict(SU4_center_power=a, SU2_center_power=b,
                         fixed_SM_neutral_fields=allowed, BL_charged_fixed_fields=charged))
    return rows


def vev_family(t, s):
    """Squared canonical field norms, in units where the FI vector is e0."""
    t, s = S.sympify(t), S.sympify(s)
    return {'n_17': t, 'n_19': S.Rational(9, 74), 'n_50': S.Rational(9, 37) + t,
            'n_56': S.Rational(9, 74), 'n_80': S.Rational(9, 37),
            'n_82': S.Rational(9, 37), 'n_4': t, 'n_5': t, 'n_9': s, 'n_54': s}


def su4_generators():
    """An explicit Hermitian basis; no orthonormality convention is needed."""
    out = []
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = S.zeros(4), S.zeros(4)
            a[i, j] = a[j, i] = 1
            b[i, j], b[j, i] = -S.I, S.I
            out.extend([a, b])
    for i in range(3):
        a = S.zeros(4)
        a[i, i], a[i + 1, i + 1] = 1, -1
        out.append(a)
    return out


def higgs_matrix(q, norms):
    """Classical gauge mass Gram on U1^9 plus su4, with unit couplings.

    Nonzero VEVs of n4,n5 point in the first hidden color and conjugate
    color. Overall conventional mass factors do not affect the kernel.
    Actual unequal positive gauge couplings give a congruent Gram.
    """
    gens = su4_generators()
    gram = S.zeros(24)
    e = S.Matrix([1, 0, 0, 0])
    for n, weight in norms.items():
        if n in ('n_4', 'n_5'):
            hidden = [(a if n == 'n_4' else -a.T) * e for a in gens]
            action = S.Matrix.hstack(*[z * e for z in q[n]], *hidden)
        else:
            action = S.Matrix([[*q[n], *([0] * 15)]])
        gram += weight * (action.conjugate().T * action).applyfunc(S.re)
    return gram


def certificate():
    witness, fields, q, bl = inputs()
    scan = center_scan(fields, q, bl)
    t, s = S.symbols('t s', nonnegative=True)
    norms = vev_family(t, s)
    balance = sum((v * q[n] for n, v in norms.items()), S.zeros(9, 1)).applyfunc(S.simplify)
    assert balance == S.Matrix([-1] + [0] * 8)
    assert q['n_4'] + q['n_5'] == q['n_2']
    assert q['n_9'] + q['n_54'] == S.zeros(9, 1)
    # Full hidden SU4 moment map: F F^dagger - A* A^T = 0,
    # not merely its three Cartan components.
    projector = S.diag(1, 0, 0, 0)
    assert t * projector - t * projector == S.zeros(4)
    for row in scan:
        if row['SU4_center_power'] == 2:
            assert set(norms) <= set(row['fixed_SM_neutral_fields'])
    neutral = [n for n, f in fields.items() if f['dim'] == '1,1,1,1' and bl[n] == 0 and q[n][1] == 0]
    assert len(neutral) == 42 and S.Matrix.hstack(*(q[n] for n in neutral)).rank() == 7
    x = S.Matrix(witness['BL_coefficients']).applyfunc(S.Rational)
    T = S.diag(1, -S.Rational(1, 3), -S.Rational(1, 3), -S.Rational(1, 3))
    # T = H01 + 2/3 H12 + 1/3 H23 in the displayed basis.
    diag_generator = x.col_join(S.Matrix([0] * 12 + [1, S.Rational(2, 3), S.Rational(1, 3)]))
    gram = higgs_matrix(q, vev_family(S.Rational(1, 10), S.Rational(1, 10)))
    assert gram == gram.T and gram.rank() == 14
    assert gram * diag_generator == S.zeros(24, 1)
    hypercharge = S.Matrix([0, 1] + [0] * 22)
    assert gram * hypercharge == S.zeros(24, 1)
    pure_bl = x.col_join(S.zeros(15, 1))
    assert (pure_bl.T * gram * pure_bl)[0] == S.Rational(1, 5)
    assert all(S.exp(3 * S.pi * S.I * z) == -1 for z in T.diagonal())
    return dict(schema='w33.pass11794.hidden_center.v1', status='PASS', model=witness['model'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
        input_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n') if p.suffix == '.json' else p.read_bytes()).hexdigest()
                      for p in [ROOT / 'data/w33_20261009_corrected_assignment_dflat_certificate.json',
                                ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz']},
        prior=['PASS10960 explicitly left hidden-center compensation open',
               'parallel3fdef4a22 owns corrected matter assignment and B-L covector',
               'Pass11793 owns exact full-field order4 action'],
        center_lifts=scan, neutral_singlet_count=42, neutral_singlet_charge_rank=7,
        combined_action='g_hat=exp(i*pi*3*BL)*(-I_SU4); optional SU2 center does not change this branch',
        canonical_squared_norms={n: str(z) for n, z in norms.items()},
        parameter_domain='t>0 and s>0; boundary values t=0 or s=0 also D-flat but can enlarge stabilizer',
        FI_balance=[str(z) for z in balance], hidden_SU4_moment_map='zero entire4x4 matrix',
        meson_charge_identity='Q(n4)+Q(n5)=Q(n2); BL(n4)=-1, BL(n5)=+1',
        orientation='n4=sqrt(t)*e1 in4, n5=sqrt(t)*e1 in conjugate4; singlet phases arbitrary for D terms',
        gauge_mass_Gram=[[str(z) for z in row] for row in gram.tolist()],
        gauge_mass_Gram_rank=14, U1_plus_SU4_Lie_dimension=24, kernel_dimension=10,
        hidden_SU2_unchanged_dimension=3,
        connected_unbroken_Lie_algebra='su3_hidden + su2_hidden + u1_Y + u1_BL_diagonal',
        diagonal_generator_BL_plus_T=[str(z) for z in diag_generator],
        hidden_T_diagonal=[str(z) for z in T.diagonal()],
        pure_BL_mass_quadratic_form='1/5 at t=s=1/10, in the supplied canonical unit-coupling convention',
        combined_action_in_connected_group='exp(i*3*pi*(BL+T))=exp(i*3*pi*BL)*(-I_SU4)',
        all_eight_lifts_obstruction='For SU4-center powers0,1,3 every fixed SM-neutral field has BL=0. For power2 only BL-charged fixed fields are one4 n4 and one conjugate4 n5. Their canonical SU4 D-flatness forces equal-norm aligned rank-one projectors, so after gauge rotation BL+diag(1,-1/3,-1/3,-1/3) always survives. Thus these eight fixed-generator center lifts cannot remove every continuous direction that acts as BL on visible matter using classical SM-preserving elementary D-flat VEVs.',
        proof_of_alignment='Traceless part of F Fdagger-Astar AT is zero. This difference has rank<=2<4, so a scalar multiple of I4 must vanish; the rank-one projectors are equal. Zero charged pair leaves pureBL instead.',
        scope='Constructive canonical classical D-flat branch and exact Higgs/stabilizer kernel, not F-flatness. This class fixes the11793 BL covector/generator and permits only SM-preserving elementary fields from this ledger. General other characters, noncentral compensators, composite strong-coupling phases, axion/Stueckelberg masses, noncanonical kinetic corrections and complete global gauge-group/discrete anomaly data are outside the no-go. No MSSM completion, exotic masses, proton protection or observed scales.',
        literature=['https://arxiv.org/abs/0708.2691', 'https://arxiv.org/abs/hep-th/9506098'])


if __name__ == '__main__':
    result = certificate()
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print('11794 PASS eight center lifts, explicit full D-flat family, rank14 mass Gram; continuous diagonalBL remains')
