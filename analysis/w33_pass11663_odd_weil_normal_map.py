"""Pass11663: the odd Weil sector's Coble normal map and a conditional mass phase.

Prior2448 owns9=5+4;11651/11657 own the even Hesse/Burkhardt dictionary.
The Pfaffian covariant is the CLASSICAL Maschke parametrization, identified
against Bruin--Filatov2207.04393 section3.1, not a new Burkhardt map.
New packet: explicit normal derivative in the committed qutrit coordinates,
40-ray rank-two alignment and its exact finite-shell Dirac competition.
The action, fields and dimensional coefficients below are supplied EFT data.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/w33_pass11663_odd_weil_normal_map.json'
PTS = list(itertools.product(range(3), repeat=2))
DIRS = [(0, 1), (1, 0), (1, 1), (1, 2)]
W = s.Symbol('w')
FVAR = s.symbols('f0:4')
G = s.diag(1, 2, 2, 2, 2)


def neg(a):
    return tuple((-x) % 3 for x in a)


def reduce_w(z):
    return s.rem(s.Poly(s.expand(z), W), s.Poly(W * W + W + 1, W)).as_expr()


def parity_bases():
    """Unnormalized even columns have metric G; odd columns have metric2I."""
    E, O = s.zeros(9, 5), s.zeros(9, 4)
    E[0, 0] = 1
    for i, a in enumerate(DIRS):
        E[PTS.index(a), i + 1] = E[PTS.index(neg(a)), i + 1] = 1
        O[PTS.index(a), i] = 1
        O[PTS.index(neg(a)), i] = -1
    return E, O


def cubic_normal_map():
    b = s.symbols('b0:5')
    p = {(0, 0): b[0]}
    for i, a in enumerate(DIRS):
        p[a], p[neg(a)] = b[i + 1] + FVAR[i], b[i + 1] - FVAR[i]
    cs = [sum(z ** 3 for z in p.values()) / 6]
    for d in DIRS:
        lines = {tuple(sorted((a, tuple((a[i] + d[i]) % 3 for i in range(2)),
                               tuple((a[i] - d[i]) % 3 for i in range(2))))) for a in PTS}
        cs.append(sum(s.prod(p[a] for a in line) for line in lines))
    K = s.Matrix([[s.diff(c, z).subs(dict.fromkeys(b, 0)).expand() for z in b] for c in cs])
    assert K + K.T == s.zeros(5)
    assert all(s.expand(c.subs(dict.fromkeys(b, 0))) == 0 for c in cs)
    return b, cs, K


def pfaffian_vector(K):
    def pf4(A):
        return A[0, 1] * A[2, 3] - A[0, 2] * A[1, 3] + A[0, 3] * A[1, 2]
    return s.Matrix([s.expand((-1) ** i * pf4(K.minor_submatrix(i, i))) for i in range(5)])


def canonical_mass(f):
    """Actual derivative of11651's normalized cubic at the normalized odd state."""
    a, b, c, d = f
    K = np.array([[0, a*a, b*b, c*c, d*d],
                  [-a*a, 0, 2*c*d, 2*b*d, 2*b*c],
                  [-b*b, -2*c*d, 0, -2*a*d, 2*a*c],
                  [-c*c, -2*b*d, 2*a*d, 0, -2*a*b],
                  [-d*d, -2*b*c, -2*a*c, 2*a*b, 0]], dtype=complex)
    D = np.diag([1, *([1 / np.sqrt(2)] * 4)])
    return D @ K @ D


def quartic(f):
    a, b, c, d = f
    return np.array([-12*a*b*c*d, 2*a*(b**3+c**3+d**3),
                     2*b*(-a**3-c**3+d**3), 2*c*(-a**3+b**3-d**3),
                     2*d*(-a**3-b**3+c**3)], dtype=complex)


def order_parameter(f):
    q = quartic(f)
    return float(abs(q[0])**2 + 2*np.vdot(q[1:], q[1:]).real)


def exact_base_rays():
    rays = [s.eye(4)[:, i] for i in range(4)]
    for i, j in itertools.product(range(3), repeat=2):
        rays.extend([s.Matrix([0, 1, W**i, W**j]),
                     s.Matrix([1, 0, W**i, -W**j]),
                     s.Matrix([1, -W**i, 0, W**j]),
                     s.Matrix([1, W**i, -W**j, 0])])
    return rays


def canonical_generators():
    """Determinant-one Weil phases, not raw Fourier projective phases."""
    F = s.Matrix(3, 3, lambda i, j: -(1 + 2*W) * W**((i*j) % 3) / 3)
    D = s.diag(*[W**((2*j*j) % 3) for j in range(3)])
    return {'F0': s.kronecker_product(F, s.eye(3)),
            'F1': s.kronecker_product(s.eye(3), F),
            'D0': s.kronecker_product(D, s.eye(3)),
            'D1': s.kronecker_product(s.eye(3), D),
            'CZ': s.diag(*[W**((a[0]*a[1]) % 3) for a in PTS])}


def exact_covariance(K, P):
    E, O = parity_bases()
    rows = []
    for name, gate in canonical_generators().items():
        ge = (G.inv() * E.T * gate * E).applyfunc(reduce_w)
        go = (O.T * gate * O / 2).applyfunc(reduce_w)
        sub = dict(zip(FVAR, go * s.Matrix(FVAR)))
        fp = P.subs(sub, simultaneous=True)
        kp = K.subs(sub, simultaneous=True)
        conjugate = ge.subs(W, W**2).applyfunc(reduce_w)
        inv = (G.inv() * conjugate.T * G).applyfunc(reduce_w)
        assert all(reduce_w(z) == 0 for z in fp - ge * P)
        assert all(reduce_w(z) == 0 for z in kp - inv.T * K * inv)
        assert reduce_w(ge.det()) == 1
        rows.append(dict(generator=name, quartic_covariance=True, mass_covariance=True,
                         even_matrix=[[str(x) for x in row] for row in ge.tolist()],
                         odd_matrix=[[str(x) for x in row] for row in go.tolist()]))
    return rows


def witting_pauli_dictionary(rays):
    w = np.exp(2j*np.pi/3)
    E, O = parity_bases()
    en = np.array(E, dtype=complex) @ np.diag([1, *([1/np.sqrt(2)]*4)])
    on = np.array(O, dtype=complex) / np.sqrt(2)
    rr = [np.array(r.subs(W, w), dtype=complex).ravel() for r in rays]
    rr = [r/np.linalg.norm(r) for r in rr]
    X, Z = np.roll(np.eye(3), 1, axis=0), np.diag([1, w, w*w])
    labels = [v for v in itertools.product(range(3), repeat=4) if any(v) and v < neg(v)]
    ps, qs, matches, match_errors = [], [], [], []
    for v in labels:
        factors = [w**((2*v[j]*v[j+1]) % 3) *
                   np.linalg.matrix_power(X, v[j]) @ np.linalg.matrix_power(Z, v[j+1]) for j in (0, 2)]
        D = np.kron(*factors)
        L = (np.eye(9) + D + D.conj().T) / 3
        p, q = on.conj().T @ L @ on, en.conj().T @ L @ en
        errs = [np.linalg.norm(p-np.outer(r,r.conj())) for r in rr]
        k = int(np.argmin(errs))
        assert errs[k] < 1e-12
        assert np.linalg.matrix_rank(p, tol=1e-10) == 1
        assert np.linalg.matrix_rank(q, tol=1e-10) == 2
        ps.append(p); qs.append(q); matches.append(k); match_errors.append(float(errs[k]))
    A = np.array([[int(i != j and sum(v[t]*u[t+1]-v[t+1]*u[t] for t in (0,2)) % 3 == 0)
                   for j,u in enumerate(labels)] for i,v in enumerate(labels)])
    I, J = np.eye(40), np.ones((40,40))
    gp = np.array([[np.trace(p@q).real for q in ps] for p in ps])
    gq = np.array([[np.trace(p@q).real for q in qs] for p in qs])
    assert np.allclose(3*gp, 2*I-A+J) and np.allclose(3*gq, 4*I+A+2*J)
    assert len(set(matches)) == 40
    return dict(labels=labels, base_ray_indices=matches, maximum_match_error=max(match_errors),
                odd_gram='(2I-A+J)/3', even_gram='(4I+A+2J)/3',
                odd_operator_rank=int(np.linalg.matrix_rank(gp, tol=1e-10)),
                even_operator_rank=int(np.linalg.matrix_rank(gq, tol=1e-10)),
                point_graph_degree=sorted(set(A.sum(1).tolist()))), rr


def loop_energy(S, y, A=.01, B=.25):
    """One five-species Dirac matrix: four spin degrees per singular mass."""
    return -quad(lambda x: x*np.log1p(y*y/(2*x)+y**4*S/(16*x*x)), A, B,
                 epsabs=1e-14, epsrel=1e-12)[0]/(4*np.pi*np.pi)


def loop_slope(S, y, A=.01, B=.25):
    return -y**4*quad(lambda x: x/(x*x+y*y*x/2+y**4*S/16), A, B,
                     epsabs=1e-13, epsrel=1e-12)[0]/(64*np.pi*np.pi)


def phase_thresholds(y, A=.01, B=.25):
    c, d = y*y/2, y*y/4
    scale = y**4/(64*np.pi*np.pi)
    high = scale*np.log((B+c)/(A+c))
    low = scale*(np.log((B+d)/(A+d))+d/(B+d)-d/(A+d))
    return dict(Witting_threshold=float(high), balanced_threshold=float(low))


def main():
    b, cs, K = cubic_normal_map()
    P = pfaffian_vector(K)
    assert (K*P).applyfunc(s.expand) == s.zeros(5,1)
    yy = [P[0]/4, *[z/2 for z in P[1:]]]
    assert s.expand(yy[0]*(yy[0]**3+sum(z**3 for z in yy[1:]))+3*s.prod(yy[1:])) == 0
    cov = exact_covariance(K, P)
    rays = exact_base_rays()
    for r in rays:
        sub = dict(zip(FVAR, r))
        assert all(reduce_w(z) == 0 for z in P.subs(sub, simultaneous=True))
        kr = K.subs(sub, simultaneous=True).applyfunc(reduce_w)
        assert any(z != 0 for z in kr)  # skew + zero4x4 Pfaffians => rank2
    dictionary, normalized = witting_pauli_dictionary(rays)
    # Independent scalar derivatives in all8 real coordinates.
    x = s.symbols('x0:8', real=True)
    sub = dict(zip(FVAR, [x[2*i]+s.I*x[2*i+1] for i in range(4)]))
    pr = P.subs(sub, simultaneous=True)
    S = s.expand((s.conjugate(pr).T*G*pr)[0])
    norm = sum(z*z for z in x)
    potential = (norm-1)**2+S
    H = s.hessian(potential, x)
    axis = {z: 0 for z in x}; axis[x[0]] = 1
    assert H.subs(axis) == s.diag(8, 0, 16, 16, 16, 16, 16, 16)
    hf = s.lambdify([x], H, 'numpy')
    maxerr = 0.
    for r in normalized:
        ev = np.linalg.eigvalsh(np.asarray(hf(np.array([[z.real,z.imag] for z in r]).ravel()), dtype=float))
        maxerr = max(maxerr, float(np.max(abs(ev-np.array([0,8,16,16,16,16,16,16])))))
    assert maxerr < 1e-10
    # Exact orientation-independent second mass moment; numerical higher check.
    Dc = s.diag(1,*([1/s.sqrt(2)]*4))
    M = (Dc*K*Dc).subs(sub, simultaneous=True)
    HH = s.conjugate(M).T*M
    assert s.expand(s.trace(HH)-norm**2) == 0
    assert s.expand(s.trace(HH*HH)-norm**4/2+S/4) == 0
    rng = np.random.default_rng(11663)
    err = 0.
    for _ in range(100):
        f = rng.normal(size=4)+1j*rng.normal(size=4); f/=np.linalg.norm(f)
        ev = np.linalg.eigvalsh(canonical_mass(f).conj().T@canonical_mass(f))
        SS = order_parameter(f)
        root = np.sqrt(max(0.,1-SS))
        want = [0,(1-root)/4,(1-root)/4,(1+root)/4,(1+root)/4]
        err = max(err, float(np.max(abs(ev-want))))
    assert err < 1e-11
    y=.2; thresholds=phase_thresholds(y)
    assert abs(loop_slope(0,y)+thresholds['Witting_threshold']) < 1e-15
    assert abs(loop_slope(1,y)+thresholds['balanced_threshold']) < 1e-15
    cases=[]
    for selected in [0.,.5,1.]:
        kap = (1.1*thresholds['Witting_threshold'] if selected==0 else
               .9*thresholds['balanced_threshold'] if selected==1 else -loop_slope(.5,y))
        grid=np.linspace(0,1,101); energies=[kap*z+loop_energy(z,y) for z in grid]
        assert abs(grid[np.argmin(energies)]-selected) < 1e-12
        cases.append(dict(kappa=kap, selected_S=selected,
                          squared_masses=[0,*([(1-np.sqrt(1-selected))/4]*2),
                                          *([(1+np.sqrt(1-selected))/4]*2)]))
    out=dict(status='PASS',reservation='48ef215c6',
             producer_sha256=hashlib.sha256(Path(__file__).read_text().encode()).hexdigest(),
             prior_owners=['analysis/w33_pass2448_2453_where_the_phase_lives.md',
                           'analysis/PASS11651_N_QUTRIT_HESSE_SPACE.md',
                           'analysis/PASS11657_HESSE_SPACE_GEOMETRISES_W33.md',
                           'analysis/PASS11659_BURKHARDT_NODES_ARE_CONCURRENCES.md',
                           'analysis/PASS20260918_physical_e8_holonomy_insert.tex'],
             classical_source='https://arxiv.org/html/2207.04393v1#S3.SS1',
             cubic_odd_restriction='identically zero',
             normal_matrix=[[str(z) for z in row] for row in K.tolist()],
             quartic_kernel=[str(z) for z in P],
             Burkhardt_coordinates=['F0/4','F1/2','F2/2','F3/2','F4/2'],
             Bruin_Filatov_source_coordinates=['f0','f1','f2','-f3'],
             covariance=cov,base_ray_count=40,
             exact_base_rays=[[str(reduce_w(z)) for z in r] for r in rays],
             dictionary=dictionary,
             canonical_normal_mass='G^(-1/2) K G^(-1/2)',
             scalar_potential='lambda (||f||^2-1)^2 + kappa Fdag G F',
             alignment_Hessian=[0,8,16,16,16,16,16,16],
             all40_Hessian_error=maxerr,
             mass_trace_identity='Tr(Mdag M)=||f||^4',
             exact_fourth_moment='Tr((Mdag M)^2)=||f||^8/2-S/4',
             unit_sphere_order_parameter_bound=[0,1],
             mass_squared_formula='0,(1-sqrt(1-S))/4 twice,(1+sqrt(1-S))/4 twice',
             maximum_spectrum_error=err,
             benchmark=dict(y=y,shell=[.01,.25],thresholds=thresholds,cases=cases),
             loop_scope='fixed unit norm; one supplied five-species Dirac matrix; finite normalized Landau shell; scalar/gauge loops omitted',
             physical_boundary='Three zero Dirac singular masses at a selected Witting ray are not three chiral SM generations. A skew matrix is not an identical-Weyl Majorana mass. Scales, couplings, radial quantum relaxation, chirality, observed masses and spacetime remain open.')
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',base_rays=40,alignment_Hessian=out['alignment_Hessian'],
                         thresholds=thresholds,mass_spectrum_error=err),indent=2))
    return out


if __name__ == '__main__':
    main()
