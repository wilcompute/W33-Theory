"""Independent invariance, spectral and stochastic checks for the conditional model."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import toe_20261119_twisted_flat_E8_higgs_and_noise as m


def test_free_affine_generators_and_twisted_betti():
    d = m.twisted_flat_geometry()
    assert d['a2_b2_ab2_translations'] == [['1', '0', '0'], ['0', '1', '0'], ['0', '0', '-1']]
    assert d['twisted_betti_by_character']['0'] == [1, 0, 0, 1]
    assert all(d['twisted_betti_by_character'][str(c)] == [0, 1, 1, 0] for c in (1, 2, 3))


def test_twisted_cup_survives_although_no_ordinary_one_form():
    # Explicit transformed dx,dy,dz: product of three signs equals +1.
    signs = np.array([[1, -1, -1], [-1, 1, -1]])
    assert np.all(np.prod(signs, axis=1) == 1)
    assert not np.any(np.all(signs == 1, axis=0))
    # Four-sheeted unit cover: integral 1/4, three normalized forms each 2 dx.
    assert sp.Rational(1, 4)*2**3 == 2


def test_actual_E8_roots_include_enhanced_gauge_algebra():
    d = m.full_e8_centralizer()
    assert (d['fixed_roots'], d['fixed_root_rank'], d['gauge_dimension']) == (72, 6, 80)
    assert d['root_dot_one_neighbor_counts'] == [20]


def test_Higgs_census_all_active_subsets():
    for row in m.higgs_branch_census()['rows']:
        n = len(row['active_axes'])
        assert row['full_E8_betti'] == {0: [80, 168, 168, 80], 1: [46]*4,
                                      2: [45, 23, 23, 45], 3: [45, 3, 3, 45]}[n]


def test_joint_Higgs_weights_independent_Fourier_basis():
    # Walsh eigenvectors diagonalize XOR shifts with tetrahedral sign triples.
    H = sp.Matrix(4, 4, lambda i, j: m.char(i, j))/2
    assert H.T*H == sp.eye(4)
    weights = []
    for k in (1, 2, 3):
        P = sp.Matrix(4, 4, lambda i, j: int(i == (j ^ k)))
        D = H.T*P*H
        assert D.is_diagonal()
        weights.append(list(D.diagonal()))
    tetra = list(zip(*weights))
    assert set(tetra) == {(1, 1, 1), (-1, 1, -1), (1, -1, -1), (-1, -1, 1)}
    # Independent pair-sum kernel count for the 6, no projector calculation.
    for mask in range(8):
        n = sum(all(tetra[i][k]+tetra[j][k] == 0 for k in range(3) if mask >> k & 1)
                for i in range(4) for j in range(i+1, 4))
        assert n == 6-2*mask.bit_count()


def test_no_branch_keeps_three_spinors_without_mirrors():
    d = m.higgs_branch_census()
    assert d['zero_Higgs_Spin10_content_H1']['16'] == d['zero_Higgs_Spin10_content_H1']['16bar'] == 3
    assert all(row['fundamental_4_betti'] == [0]*4 for row in d['rows'][1:])


def test_ordinary_spinor_gap_is_not_twisted_form_count():
    d = m.twisted_flat_geometry()
    assert d['ordinary_parallel_spinors'] == 0
    assert d['cover_spin_translation_signs'] == [-1]*3
    # Smallest half-integer Fourier lattice norm: sum (2*pi*(1/2))^2.
    assert sum((2*sp.pi*sp.Rational(1, 2))**2 for _ in range(3)) == 3*sp.pi**2


def test_hollow_sum_rule_and_zero_edge_limits():
    assert m.hollow_yukawa_probe()['max_relative_sum_rule_error'] < 3e-15
    for z in ((0, 0, 0), (1j, 0, 0), (1j, 7, 0), (1+2j, -2+4j, 3j)):
        Y = np.array([[0, z[0], z[1]], [z[0], 0, z[2]], [z[1], z[2], 0]], complex)
        s = np.linalg.svd(Y, compute_uv=False)
        assert abs(s[0]-s[1]-s[2]) < 1e-13


def test_noncanonical_metric_bound_for_nondiagonal_metrics():
    rng = np.random.default_rng(44)
    Y = np.array([[0, 1j, 2], [1j, 0, 3j], [2, 3j, 0]], complex)
    for _ in range(12):
        transforms, cond = [], []
        for __ in range(2):
            X = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
            K = X.conj().T@X+np.eye(3)
            w, U = np.linalg.eigh(K)
            transforms.append((U/np.sqrt(w))@U.conj().T)
            cond.append(w[-1]/w[0])
        s = np.linalg.svd(transforms[0]@Y@transforms[1], compute_uv=False)
        assert s[0]/s[1] <= 2*np.sqrt(cond[0]*cond[1])+1e-12


def test_exact_Poisson_factorial_second_moment_and_linear_case():
    assert m.poisson_noise_probe()['exact_cubic_variance_crosscheck'] == '32144/84375'
    assert m.poisson_factorial_variance([0, 1], sp.Rational(7, 3), sp.Rational(2, 5)) == sp.Rational(28, 75)
    assert m.poisson_factorial_variance([3], sp.Rational(7, 3), sp.Rational(2, 5)) == 0


def test_full_Bessel_score_noise_bound():
    d = m.poisson_noise_probe()['Bessel_full_estimator_score_bound']
    assert 0.765 < d['mean_J0'] < 0.766
    assert d['rows'][0]['coefficient_of_variation_lower_bound'] > 12
    assert all(abs(r['rho']*r['variance_lower_bound']-0.0968222596) < 1e-8 for r in d['rows'])


def test_frozen_certificate_matches_recomputed_exact_sections():
    frozen = json.loads(m.OUT.read_text(encoding='utf-8'))
    fresh = m.build()
    for key in ('geometry', 'full_E8_centralizer', 'Higgs_branches', 'causal_estimator_noise', 'axion_shift_lattice'):
        assert frozen[key] == fresh[key]


def test_axion_lattice_saturation_is_not_unimodular():
    d = m.axion_shift_lattice_probe()
    assert d['original_Smith_nonzero_factors'] == [1, 2]
    assert d['saturated_Smith_nonzero_factors'] == [1, 1]
    S = sp.Matrix(d['original_shift_matrix'])
    T = sp.Matrix(d['saturated_shift_matrix'])
    # Greatest common divisor of maximal minors is independent of SNF routine.
    minors = lambda M: [abs(M[:, cols].det()) for cols in ((0, 1), (0, 2), (1, 2))]
    assert sp.gcd_list(minors(S)) == 2 and sp.gcd_list(minors(T)) == 1
    assert T*sp.Matrix([-3, 5, 1]) == sp.zeros(2, 1)


def test_axion_integer_rebasis_and_original_charge_polynomial():
    from toe_20261119_balanced_source_E8_cup_gate import sector_census
    _, fields, _ = sector_census()
    a, b, c = sp.symbols('a b c')
    P = sp.expand(sum(d*(q[0]*a+q[1]*b+q[2]*c)**3 for d, q, _ in fields))
    d = m.axion_shift_lattice_probe()
    R1, R2 = map(sp.sympify, d['integer_quadratic_coefficients'])
    assert sp.expand(P-(a+3*c)*R1-(b-5*c)*R2) == 0
    assert sp.expand(P.subs({a: -3*c, b: 5*c})) == 0
