"""Exact conditional tests: twisted flat geometry, full E8, Higgs branches and noise.

Known geometric framework: Barbosa 1910.10742; Acharya--Baldwin 2312.12311.
No compact G2 vacuum or physical chiral spectrum is claimed.
"""
from itertools import combinations, product
from functools import reduce
from operator import xor
from pathlib import Path
import json
import math
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261119_twisted_flat_E8_higgs_and_noise.json'


def char(c, g):
    return (-1) ** ((int(c) & int(g)).bit_count() % 2)


def form_characters(p):
    return [reduce(xor, I, 0) for I in combinations((1, 2, 3), p)]


def twisted_flat_geometry():
    # Affine maps on the unit torus; translations retained exactly on R^3.
    A = sp.diag(1, -1, -1)
    B = sp.diag(-1, 1, -1)
    a = (A, sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), 0]))
    b = (B, sp.Matrix([0, sp.Rational(1, 2), sp.Rational(1, 2)]))

    def compose(f, g):
        return f[0]*g[0], f[0]*g[1]+f[1]

    ab = compose(a, b)
    squares = [compose(g, g)[1] for g in (a, b, ab)]
    free_witnesses = []
    for R, t in (a, b, ab):
        axis = next(i for i in range(3) if R[i, i] == 1)
        assert t[axis] % 1 == sp.Rational(1, 2)
        free_witnesses.append({'fixed_axis': axis, 'translation_mod_one': str(t[axis] % 1)})
    betti = {str(c): [sum(d == c for d in form_characters(p)) for p in range(4)]
             for c in range(4)}
    assert betti['0'] == [1, 0, 0, 1]
    assert all(betti[str(c)] == [0, 1, 1, 0] for c in (1, 2, 3))
    assert 1 ^ 2 ^ 3 == 0
    # Spin lifts square to -1 on each of the three unit translations.
    I = sp.I
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -I], [I, 0]])
    assert (I*sx)**2 == (I*sy)**2 == ((I*sx)*(I*sy))**2 == -sp.eye(2)
    return {'free_affine_witnesses': free_witnesses,
            'a2_b2_ab2_translations': [[str(v) for v in t] for t in squares],
            'twisted_betti_by_character': betti,
            'triple_twisted_cup_integral_unit_cover': '1/4',
            'unit_L2_normalized_triple': '2',
            'ordinary_parallel_spinors': 0,
            'cover_spin_translation_signs': [-1, -1, -1],
            'ordinary_Dirac_squared_cover_lower_bound_unit_lengths': '3*pi**2',
            'scope': 'Closed flat Hantzsche-Wendt manifold; coefficients factor through V4. Twisted de Rham modes require the gauge-theory twist; ordinary spinors are different.'}


def full_e8_centralizer():
    # Standard E8 roots in R^8: first five coordinates Spin10, last three Spin6.
    roots = []
    for i, j in combinations(range(8), 2):
        for u, v in product((-1, 1), repeat=2):
            r = [sp.Rational(0)]*8
            r[i], r[j] = sp.Rational(u), sp.Rational(v)
            roots.append(tuple(r))
    roots += [tuple(sp.Rational(s, 2) for s in signs)
              for signs in product((-1, 1), repeat=8) if math.prod(signs) == 1]
    t1 = sp.Matrix([0]*5+[sp.Rational(1, 2), sp.Rational(1, 2), 0])
    t2 = sp.Matrix([0]*5+[sp.Rational(1, 2), 0, sp.Rational(1, 2)])
    fixed = [r for r in roots if (sp.Matrix(r).dot(t1)).q == 1
             and (sp.Matrix(r).dot(t2)).q == 1]
    rank = sp.Matrix(fixed).rank()
    neighbors = sorted(set(sum(sum(x*y for x, y in zip(r, s)) == 1
                               for s in fixed) for r in fixed))
    assert len(roots) == 240 and len(fixed) == 72 and rank == 6
    assert neighbors == [20]
    return {'E8_roots': len(roots), 'fixed_roots': len(fixed), 'fixed_root_rank': rank,
            'root_dot_one_neighbor_counts': neighbors,
            'fixed_Lie_algebra': 'e6 + u1 + u1', 'gauge_dimension': 80,
            'warning': 'Counting only Spin10 plus SU4 Cartan misses 32 extra invariant spinor gauge generators. Lie algebra does not specify the global gauge group.'}


def wedge_generator(T):
    pairs = list(combinations(range(4), 2))
    W = sp.zeros(6)
    for col, (i, j) in enumerate(pairs):
        for k in range(4):
            for (a, b), v in (((k, j), T[k, i]), ((i, k), T[k, j])):
                if a != b:
                    W[pairs.index(tuple(sorted((a, b)))), col] += v*(1 if a < b else -1)
    return W


def end_generator(T):
    columns = []
    for i, j in product(range(4), repeat=2):
        E = sp.zeros(4)
        E[i, j] = 1
        columns.append(sp.Matrix(list(T*E-E*T)))
    return sp.Matrix.hstack(*columns)


def invariant_kernel_betti(Ts, characters, active):
    n = len(characters)
    K = (sp.Matrix.vstack(*(Ts[i] for i in active)).nullspace()
         if active else list(sp.eye(n).columnspace()))
    if not K:
        return [0]*4
    K = sp.Matrix.hstack(*K)
    projector = K*(K.T*K).inv()*K.T
    traces = [(projector*sp.diag(*(char(c, g) for c in characters))).trace()
              for g in range(4)]
    counts = [sum(traces[g]*sum(char(c, g) for c in form_characters(p))
                  for g in range(4))/4 for p in range(4)]
    assert all(v.q == 1 and v >= 0 for v in counts)
    return list(map(int, counts))


def higgs_branch_census():
    # Fourier-dual V4 bases: diagonal unitary rho and Hermitian XOR shifts P_i.
    P = [sp.Matrix(4, 4, lambda i, j: int(i == (j ^ k))) for k in (1, 2, 3)]
    for g in range(4):
        rho = sp.diag(*(char(c, g) for c in range(4)))
        assert rho.det() == 1
        for i in range(3):
            assert rho*P[i]*rho == char(i+1, g)*P[i]
    assert all(T.T == T and T.trace() == 0 and T*T == sp.eye(4) for T in P)
    assert all(T*U == U*T for T, U in product(P, repeat=2))
    assert P[0]*P[1] == P[2]
    W = [wedge_generator(T) for T in P]
    E = [end_generator(T) for T in P]
    rows = []
    for mask in range(8):
        active = [i for i in range(3) if mask >> i & 1]
        f = invariant_kernel_betti(P, list(range(4)), active)
        w = invariant_kernel_betti(W, [i ^ j for i, j in combinations(range(4), 2)], active)
        e = invariant_kernel_betti(E, [i ^ j for i, j in product(range(4), repeat=2)], active)
        # Remove the identity from End(4), which is an always-trivial coefficient.
        adj = [v-u for v, u in zip(e, (1, 0, 0, 1))]
        total = [45*u+32*v+10*z+t for u, v, z, t in zip((1, 0, 0, 1), f, w, adj)]
        assert total[0] == total[3] and total[1] == total[2]
        rows.append({'active_axes': active, 'fundamental_4_betti': f,
                     'wedge_6_betti': w, 'adjoint_15_betti': adj,
                     'full_E8_betti': total})
    assert rows[0]['full_E8_betti'] == [80, 168, 168, 80]
    assert rows[-1]['full_E8_betti'] == [45, 3, 3, 45]
    assert all(r['fundamental_4_betti'] == [0]*4 for r in rows[1:])
    return {'parallel_BPS_Higgs': 'phi=sum_i a_i dx_i P_i; d_A phi=d_A* phi=[phi wedge phi]=0',
            'SU4_embedding': 'rho(g)=diag(chi_0,chi_1,chi_2,chi_3)',
            'rows': rows,
            'zero_Higgs_Spin10_content_H1': {'16': 3, '16bar': 3, '10': 6, '1': 12},
            'net_chirality': 0,
            'derivation': 'On the torus cover, Hermitian commuting constant Higgs generators give a positive sum of squared momenta and squared Higgs generators. Only constant forms in their joint kernel survive; average these over V4. Nonzero real a_i has no translation monodromy of unit modulus in the fundamental.',
            'scope': 'Twisted gauge-theory cohomology on one smooth closed base. Three spinor family labels have mirrors at a=0; ANY nonzero real axis Higgs gaps all these spinors. Generic three-axis branch has only three singlet H1 modes. No Standard Model vacuum or compact ADE realization is supplied.'}


def hollow_yukawa_probe():
    rng = np.random.default_rng(20261119)
    residual = 0.0
    for _ in range(256):
        z = rng.normal(size=3)+1j*rng.normal(size=3)
        Y = np.array([[0, z[0], z[1]], [z[0], 0, z[2]], [z[1], z[2], 0]])
        s = np.linalg.svd(Y, compute_uv=False)
        residual = max(residual, abs(s[0]-s[1]-s[2])/s[0])
    assert residual < 3e-15
    return {'random_complex_cases': 256, 'max_relative_sum_rule_error': residual,
            'exact_sum_rule': 's1=s2+s3 for complex symmetric hollow 3x3 matrices',
            'proof': 'Three diagonal rephasings remove all three off-diagonal phases. The resulting real nonnegative symmetric zero-diagonal matrix has trace zero and one positive/two negative eigenvalues (or a limiting zero-edge case). Perron-Frobenius makes its positive eigenvalue largest in modulus, hence the singular-value equality.',
            'canonical_normalization_necessary_bound': 's1(Yphys)/s2(Yphys) <= 2*sqrt(kappa(KL)*kappa(KR))',
            'same_K_metric_required_condition_number_for_ratio_1e5': 50000,
            'scope': 'Bound applies to invertible positive kinetic metrics with Yphys=KL^(-1/2) Y KR^(-1/2); new diagonal operators change the premise. Strengthens the repo inequality, not a newly discovered general matrix theorem.'}


def poisson_factorial_variance(coefficients, lam, a):
    """Exact Poisson variance of sum c_n a^n (N)_n, with rational inputs."""
    x = sp.Symbol('x')
    f = sum(c*x**i for i, c in enumerate(coefficients))
    return sp.expand(sum((a*a*lam)**r/sp.factorial(r)*sp.diff(f, x, r).subs(x, a*lam)**2
                         for r in range(1, len(coefficients))))


def poisson_noise_probe():
    # Independent factorial-product contraction, rather than implementation echo.
    coeff = [sp.Rational(1), sp.Rational(-2), sp.Rational(3, 5), sp.Rational(1, 7)]
    lam, a = sp.Rational(7, 3), sp.Rational(2, 5)
    second = sum(c*d*a**(i+j)*sum(sp.binomial(i, r)*sp.binomial(j, r)*sp.factorial(r)*lam**(i+j-r)
                 for r in range(min(i, j)+1)) for i, c in enumerate(coeff) for j, d in enumerate(coeff))
    mean = sum(c*(a*lam)**i for i, c in enumerate(coeff))
    var = poisson_factorial_variance(coeff, lam, a)
    assert sp.cancel(second-mean**2-var) == 0
    from scipy.special import j0, j1
    # Score/Cauchy bound for ANY square-integrable count-only estimator unbiased
    # for all diamond volumes, not just a chosen polynomial truncation.
    # Cov(fhat,N)=lambda*d E[fhat]/d lambda=lambda*a*f'(s).
    s, qe = 4., 1.
    derivative = -qe*j1(qe*s/4)/4
    mean_bessel = j0(qe*s/4)
    noise_rows = [{'rho': rho, 'variance_lower_bound': float(2*s*derivative**2/rho),
                   'coefficient_of_variation_lower_bound': float(math.sqrt(2*s*derivative**2/rho)/abs(mean_bessel))}
                  for rho in (0.001, 0.01, 0.1, 1., 10., 100.)]
    # Density convention of the repo causal exchange: lambda=rho*s/2, a=2/rho.
    # For f(s)=s the estimator is 2N/rho, exactly unbiased and Var=2s/rho.
    return {'exact_cubic_variance_crosscheck': str(var), 'independent_moment_residual': '0',
            'finite_polynomial_identity': 'Var[fhat]=sum_{r>=1} (2*s/rho)^r/r! * (f^(r)(s))^2',
            'linear_kernel_at_s_1_variances': {'rho_1': '2', 'rho_10': '1/5', 'rho_100': '1/50'},
            'Bessel_full_estimator_score_bound': {'s': s, 'qE': qe, 'mean_J0': float(mean_bessel),
                'variance_bound_formula': 'Var >= (2*s/rho)*[f_prime(s)]**2', 'rows': noise_rows,
                'assumptions': 'Count-only estimator is unbiased for all positive volumes at fixed rho; square integrability and regular Poisson score identity. Infinite variance also cannot evade the lower bound. Does not assume convergence of the higher chaos terms.'},
            'proof': '(N)_i (N)_j=sum_r binom(i,r)binom(j,r)r!(N)_(i+j-r); Poisson factorial means are lambda^k. The r=0 term is the squared mean.',
            'scope': 'Real polynomial factorial estimator, exact finite identity. Infinite analytic/Bessel extensions require L2 convergence, not assumed here. Sprinkling estimator noise is NOT a quantum Wightman state or a fluctuation-dissipation derivation.'}


def axion_shift_lattice_probe():
    """Integral refinement of eaedca990's formal two-direction factorization."""
    from sympy.matrices.normalforms import smith_normal_form
    from toe_20261119_two_GS_axions_causal_layer_and_Bell_gates import global_e8_anomaly_two_axions
    previous = global_e8_anomaly_two_axions()
    original = sp.Matrix(previous['two_axion_shift_vectors'])
    saturated = sp.Matrix([[1, 0, 3], [0, 1, -5]])
    transition = sp.Matrix([[2, 1], [0, 1]])
    assert original == transition*saturated
    a, b, c = sp.symbols('a b c')
    P = sp.sympify(previous['Abelian_cubic_polynomial'])
    Q1 = sp.sympify(previous['two_axion_P_decomposition_Q1'])
    Q2 = sp.sympify(previous['two_axion_P_decomposition_Q2'])
    U, V = a+3*c, b-5*c
    R1, R2 = sp.expand(2*Q1), sp.expand(Q1+Q2)
    assert sp.expand(P-U*R1-V*R2) == 0
    assert all(v.q == 1 for R in (R1, R2) for v in sp.Poly(R, a, b, c).coeffs())
    return {'original_shift_matrix': [list(map(int, row)) for row in original.tolist()],
            'saturated_shift_matrix': [list(map(int, row)) for row in saturated.tolist()],
            'original_Smith_nonzero_factors': [abs(int(smith_normal_form(original, domain=sp.ZZ)[i, i])) for i in range(2)],
            'saturated_Smith_nonzero_factors': [abs(int(smith_normal_form(saturated, domain=sp.ZZ)[i, i])) for i in range(2)],
            'lattice_index': int(transition.det()),
            'primitive_continuous_kernel_generator': [-3, 5, 1],
            'integer_quadratic_coefficients': [str(R1), str(R2)],
            'exact_polynomial_residual': '0',
            'linear_mixed_anomaly_rebasis': '2a+b+c=2*(a+3c)+(b-5c)',
            'conditional_torus_kernel_components': {'original': 'Z2', 'saturated': 'trivial'},
            'scope': 'Assumes independent 2pi gauge angles and 2pi axions with integer shifts. Replacing the lattice changes the periodic axion model; it is NOT a unimodular redefinition of the original axions. Formal integer polynomial coefficients do not establish quantized normalized WZ couplings, global E8 quotient, inflow or a physical discrete symmetry.'}


def build():
    return {'geometry': twisted_flat_geometry(), 'full_E8_centralizer': full_e8_centralizer(),
            'Higgs_branches': higgs_branch_census(), 'hollow_Yukawa': hollow_yukawa_probe(),
            'causal_estimator_noise': poisson_noise_probe(),
            'axion_shift_lattice': axion_shift_lattice_probe()}


if __name__ == '__main__':
    data = build()
    OUT.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    for row in data['Higgs_branches']['rows']:
        print(row['active_axes'], row['full_E8_betti'])
    print(OUT)
