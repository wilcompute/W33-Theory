"""Independent charge, full moment-map and gauge-locking controls."""
from pathlib import Path
import gzip, json, sys
from fractions import Fraction as F
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import w33_pass11794_hidden_center_vacuum as p


def raw():
    w = json.loads((ROOT / 'data/w33_20261009_corrected_assignment_dflat_certificate.json').read_text())
    fs = json.loads(gzip.decompress((ROOT / 'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz').read_bytes()))[w['model']]['left']
    return w, {f['name']: f for f in fs}


def test_exact_FI_family_in_original_Fraction_charges():
    _, f = raw()
    for t, s in [(F(1, 10), F(1, 10)), (F(7, 19), F(3, 11)), (F(0), F(0))]:
        v = {'n_17': t, 'n_19': F(9, 74), 'n_50': F(9, 37) + t,
             'n_56': F(9, 74), 'n_80': F(9, 37), 'n_82': F(9, 37),
             'n_4': t, 'n_5': t, 'n_9': s, 'n_54': s}
        assert all(z >= 0 for z in v.values())
        assert [sum(z * F(f[n]['q'][i]) for n, z in v.items()) for i in range(9)] == [-1] + [0] * 8
        assert all(f[n]['dim'].startswith('1,1,') and F(f[n]['q'][1]) == 0 for n in v)


def test_every_hidden_center_lift_from_raw_fields():
    w, fs = raw()
    x = list(map(F, w['BL_coefficients']))
    for a in range(4):
        for b in range(2):
            charged = []
            for n, f in fs.items():
                ds = list(map(int, f['dim'].split(',')))
                if ds[:2] != [1, 1] or F(f['q'][1]) != 0:
                    continue
                bl = sum(y * F(z) for y, z in zip(x, f['q']))
                c4 = {1: 0, 4: 1, -4: -1}[ds[2]]
                phase = 6 * bl + a * c4 + 2 * b * int(ds[3] == 2)
                assert phase.denominator == 1
                if phase % 4 == 0 and bl != 0:
                    charged.append(n)
            assert charged == (['n_4', 'n_5'] if a == 2 else [])
    # Half-BL hidden fundamentals suggested by labels carry hypercharge;
    # they cannot be used as SM-preserving VEVs.
    assert fs['v_2']['dim'] == '1,1,-4,1' and F(fs['v_2']['q'][1]) == -F(1, 2)


def test_complex_rotated_nonabelian_D_terms_and_locked_generator():
    h = S.Matrix([[1, 1, 1, 1], [1, -1, 1, -1],
                  [1, 1, -1, -1], [1, -1, -1, 1]]) / 2
    u = S.diag(1, S.I, -1, -S.I) * h
    assert u.conjugate().T * u == S.eye(4)
    v = u[:, 0]
    anti = v.conjugate()
    assert v * v.conjugate().T - anti.conjugate() * anti.T == S.zeros(4)
    T = u * S.diag(1, -S.Rational(1, 3), -S.Rational(1, 3), -S.Rational(1, 3)) * u.conjugate().T
    assert S.trace(T) == 0 and T == T.conjugate().T
    assert -v + T * v == S.zeros(4, 1)
    assert anti - T.T * anti == S.zeros(4, 1)
    # An equal-norm orthogonal pair cancels neither the full moment map
    # nor merely the three diagonal components in this orientation.
    e0, e1 = S.eye(4)[:, 0], S.eye(4)[:, 1]
    assert e0 * e0.T - e1 * e1.T != S.zeros(4)


def test_full_gauge_mass_kernel_under_independent_Abelian_basis_change():
    _, _, q, _ = p.inputs()
    norms = p.vev_family(S.Rational(1, 10), S.Rational(1, 10))
    gram = p.higgs_matrix(q, norms)
    frozen = json.loads(p.OUT.read_text())
    locked = S.Matrix(frozen['diagonal_generator_BL_plus_T']).applyfunc(S.Rational)
    assert gram.rank() == 14 and gram * locked == S.zeros(24, 1)
    # Arbitrary unimodular change of gauge-coordinate basis transforms
    # both the Gram and the generator, preserving masslessness.
    change = S.eye(24)
    change[2, 5], change[6, 1] = 3, -2
    other = change.T * gram * change
    assert other.rank() == 14 and other * (change.inv() * locked) == S.zeros(24, 1)
    assert S.Matrix(frozen['gauge_mass_Gram']).applyfunc(S.Rational) == gram


def test_residual_SU3_generators_and_visible_BL_action():
    _, _, q, _ = p.inputs()
    gram = p.higgs_matrix(q, p.vev_family(S.Rational(1, 10), S.Rational(1, 10)))
    generators = p.su4_generators()
    # Six off-diagonal generators inside the three unoccupied colors.
    indices = [i for i, a in enumerate(generators[:12]) if a[:, 0] == S.zeros(4, 1)]
    assert len(indices) == 6
    for j in indices + [13, 14]:
        assert gram[:, 9 + j] == S.zeros(24, 1)
    assert gram.nullspace().__len__() == 8 + 2
    assert gram[1, :] == S.zeros(1, 24)
    w, fs = raw()
    x = list(map(F, w['BL_coefficients']))
    assert all(fs[n]['dim'].split(',')[2:] == ['1', '1'] for n in w['physical_family_constraints'])
    assert sum(y * F(z) for y, z in zip(x, fs['q_1']['q'])) == F(1, 3)


def test_continuous_embedding_of_discrete_action_and_scope():
    T = [S.Integer(1)] + [-S.Rational(1, 3)] * 3
    assert all(S.exp(3 * S.pi * S.I * z) == -1 for z in T)
    j = json.loads(p.OUT.read_text())
    assert j['status'] == 'PASS' and len(j['center_lifts']) == 8
    assert 'F-flatness' in j['scope'] and 'Stueckelberg' in j['scope']
