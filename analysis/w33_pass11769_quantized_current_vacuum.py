"""A proposed quantum dynamics for the actual W33 currents, not a TOE claim.

Prior current algebra: w33_pass11767_global_current_algebra.py.
Standard Schrödinger/Heisenberg quantization is prior mathematics. New here is
the explicit edge Hamiltonian and its reproducible restricted vacuum problem.
The finite 78-dimensional configuration carrier is NOT its quantum Hilbert space.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq, minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass11767_global_current_algebra import actual_edges

OUT = ROOT / 'data/w33_pass11769_quantized_current_vacuum.json'


def geometry():
    edges = actual_edges()
    n = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        n[i, j - 40] = 1
    one = np.ones((40, 40), dtype=np.int64)
    # Exact integer identities certify the 24 + 15 spectral subspaces on
    # each 39-dimensional augmentation module; no eigenvalue fit is used.
    t = 5 * n @ n.T - 2 * one
    tl = 5 * n.T @ n - 2 * one
    assert np.array_equal(t @ t, 30 * t)
    assert np.array_equal(tl @ tl, 30 * tl)
    assert np.trace(t) == np.trace(tl) == 720
    assert np.array_equal(n @ tl, t @ n)
    u40 = np.zeros((160, 80), dtype=np.int64)
    v40 = u40.copy()
    s = np.r_[np.ones(40, dtype=np.int64), -np.ones(40, dtype=np.int64)]
    for k, (i, j) in enumerate(edges):
        u40[k, i] = u40[k, j] = 40
        u40[k] -= 1
        v40[k, i], v40[k, j] = 40, -40
        v40[k] -= s
    pw40 = np.block([[40*np.eye(40, dtype=np.int64)-one, np.zeros_like(one)],
                     [np.zeros_like(one), 40*np.eye(40, dtype=np.int64)-one]])
    g10 = np.block([[np.zeros_like(one), 10*n-one],
                    [10*n.T-one, np.zeros_like(one)]])
    assert np.array_equal(g10 @ g10 @ g10, 600*g10)
    assert np.trace(g10 @ g10) == 28800
    assert np.array_equal(u40.T @ u40, 160*(pw40+g10))
    assert np.array_equal(v40.T @ v40, 160*(pw40-g10))
    assert np.all(np.sum(u40*v40, axis=1) == 0)
    assert np.all(np.sum(u40*u40, axis=1) == 3120)
    assert np.all(np.sum(v40*v40, axis=1) == 3120)
    assert np.all(u40.sum(axis=0) == 0) and np.all(v40.sum(axis=0) == 0)
    pairing = u40 @ v40.T
    for k, edge in enumerate(edges):
        for l, other in enumerate(edges):
            if set(edge).isdisjoint(other):
                assert pairing[k,l] == pairing[l,k] == 0
    # The linear sum is a dilation/squeeze generator, not a stable energy.
    # Bsum=D(4P-G), Bsum^2=16P-G^2, with real nonzero eigenvalues.
    bsum = np.diag(s)@(4*pw40-g10*4)/40
    assert np.allclose(bsum@bsum, 16*pw40/40-(g10@g10)/100)
    # A rational direction in the point-side 15-dimensional incidence kernel.
    # Its entries are 9 at a point, -3 at its 12 collinear neighbors, 1 elsewhere.
    witness = (120*np.eye(40, dtype=np.int64)-3*one-4*t)[:, 0] // 5
    assert sorted(witness.tolist()) == [-3]*12 + [1]*27 + [9]
    assert witness.sum() == 0 and np.all(n.T @ witness == 0)
    assert int(np.sum(witness**4)) == 7560
    # A classical zero exists: red (non-star) edges kill the q factor,
    # the four edges at point0 kill the p factor. Quantum central charge
    # prevents simultaneous annihilation by the corresponding operators.
    qscaled = np.r_[np.array([39]+[-1]*39), np.zeros(40,dtype=int)]
    pscaled39 = np.r_[np.array([-39]+[1]*39), np.zeros(40,dtype=int)]
    x40, y1560 = v40@qscaled+40, u40@pscaled39+1560
    assert np.all(x40*y1560 == 0)
    assert np.count_nonzero(x40) == 4
    assert all(qscaled[i:i+40].sum() == pscaled39[i:i+40].sum() == 0 for i in (0,40))
    return dict(n=n, u=u40/40, v=v40/40, pw=pw40/40,
                g=g10/10, s=s, p=t/30, pl=tl/30,
                kernel_witness=witness)


def gaussian_energy(u, v, covariance, inverse, phase):
    """Exact Wick formula, numerically evaluated; no sampling or Fock cutoff.

    psi(q) ∝ exp(-q.C^-1.q/2 + i q.F.q/2), q in W.
    Every edge's x=V.q and y=U.p commute because U.V=0.
    """
    vx = np.einsum('ei,ei->e', v@covariance, v)/2
    vy = np.einsum('ei,ei->e', u@(inverse+phase@covariance@phase), u)/2
    cross = np.einsum('ei,ei->e', v@covariance@phase, u)/2
    b = 1/20
    terms = vx*vy+2*cross**2+b*(vx+vy+4*cross)+b*b
    return float(terms.sum()), vx, vy, cross


def exact_trial():
    m = (6*np.sqrt(10)+15)/40
    b = 1/20
    def derivative(t):
        return 1-1/t**2-4*b*b/(3*m*t+b)**2
    t = brentq(derivative, 1, 2, xtol=1e-14)
    f = -2*b/(3*m*t+b)
    energy = 160*(m*m+b*m*(t+1/t)+b*b-4*b*b*t*m/(3*m*t+b))
    return dict(m=float(m), t=float(t), f=float(f), energy=float(energy),
                root_residual=float(derivative(t)))


def root_bracket(trial):
    """Rational signs isolate the root; decimal floats do not certify it."""
    scale = 10**40
    r = isqrt(10*scale*scale)
    lo, hi = Fraction(r, scale), Fraction(r+1, scale)
    assert lo*lo < 10 < hi*hi
    ml, mh = (6*lo+15)/40, (6*hi+15)/40
    k = int(trial['t']*10**12)
    tl, th = Fraction(k, 10**12), Fraction(k+1, 10**12)
    b = Fraction(1, 20)
    def polynomial(t, m):
        return (t*t-1)*(3*m*t+b)**2-4*b*b*t*t
    assert 1 < tl < th
    assert polynomial(tl, mh) < 0 < polynomial(th, ml)
    return dict(sqrt10_interval=[str(lo), str(hi)],
                t_interval=[str(tl), str(th)],
                proof='F increases with m for t>1; exact rational endpoint signs. The divided stationarity equation has strictly positive derivative for t>0, so there is exactly one positive root.')


def non_gaussian_ritz(trial):
    """Explicit span{psi, He4(Y)psi/sqrt(24)} and independent quadrature.

    Y=(w.q)/sqrt(108t), with the integer point-kernel vector w. Its variance
    is one, so the two states are orthonormal. The formula is algebraic in
    m,t,f; seven-node Gaussian quadrature integrates the degree<=12 products
    exactly in exact arithmetic and checks a separate implementation.
    """
    m, t, f, e = (trial[k] for k in ('m','t','f','energy'))
    diagonal = (21600*f*f*m*m*t**3+4320*f*f*m*t**3+360*f*f*m*t*t
        +525*f*f*t**3+36*f*f*t*t+1440*f*m*t*t+144*f*t*t
        +7200*m*m*t+360*m*t*t+1440*m*t+360*m+36*t*t+193*t+36)/(45*t)
    coupling = 35*np.sqrt(6)*(f*t+1j)**2/108
    matrix = np.array([[e, coupling.conjugate()], [coupling, diagonal]])
    values, vectors = np.linalg.eigh(matrix)
    nodes, weights = np.polynomial.hermite_e.hermegauss(7)
    weights /= np.sqrt(2*np.pi)
    eta = np.array(np.meshgrid(nodes, nodes, nodes, indexing='ij')).reshape(3,-1)
    weight = np.prod(np.array(np.meshgrid(weights, weights, weights,
                                        indexing='ij')), axis=0).ravel()
    dcheck, kcheck, ncheck = 0., 0j, 0.
    b = 1/20
    for w, count in ((9,4),(-3,48),(1,108)):
        vx, vz = t*m, m/t
        sigma = np.sqrt(108*t)
        cx, cz, derivative = t*w/(2*sigma), w/(2*sigma), w/sigma
        x, z = np.sqrt(vx)*eta[0], np.sqrt(vz)*eta[1]
        remainder = 1-cx*cx/vx-cz*cz/vz
        assert remainder > 0
        y = cx/np.sqrt(vx)*eta[0]+cz/np.sqrt(vz)*eta[1]+np.sqrt(remainder)*eta[2]
        h, hp = y**4-6*y*y+3, 4*y**3-12*y
        jpsi = (x+np.sqrt(b))*(f*x+np.sqrt(b)+1j*z)
        jphi = (x+np.sqrt(b))*((f*x+np.sqrt(b)+1j*z)*h-1j*derivative*hp)/np.sqrt(24)
        dcheck += count*float(weight @ np.abs(jphi)**2)
        kcheck += count*(weight @ (jphi.conjugate()*jpsi))
        ncheck = float(weight @ (h*h/24))
    assert abs(dcheck-diagonal) < 2e-10
    assert abs(kcheck-coupling) < 2e-10
    assert abs(ncheck-1) < 2e-13
    assert values[0] < e-0.019
    return dict(energy=float(values[0]),
        gaussian_energy=e, hermite_state_energy=float(diagonal),
        off_diagonal=[float(coupling.real),float(coupling.imag)],
        coefficients=[[float(z.real),float(z.imag)] for z in vectors[:,0]],
        state='c0*psi+c1*He4(Y)*psi/sqrt(24), Y=w.q/sqrt(108t)',
        exact_coupling='35*sqrt(6)*(f*t+i)^2/108',
        exact_diagonal='(21600*f^2*m^2*t^3+4320*f^2*m*t^3+360*f^2*m*t^2+525*f^2*t^3+36*f^2*t^2+1440*f*m*t^2+144*f*t^2+7200*m^2*t+360*m*t^2+1440*m*t+360*m+36*t^2+193*t+36)/(45*t)',
        exact_energy='(E+D-sqrt((D-E)^2+4*abs(K)^2))/2',
        quadrature_checks={'diagonal_error':float(abs(dcheck-diagonal)),
                           'coupling_error':float(abs(kcheck-coupling)),
                           'norm_error':float(abs(ncheck-1))},
        scope='An explicit non-Gaussian variational upper bound; no ground-state attainment or gap claim.')


def spectral_covariance(g):
    pw, a = g['pw'], g['g']
    c = pw+a/np.sqrt(10)+(4/np.sqrt(10)-1)*(a@a)/6
    ci = pw-a/np.sqrt(10)+(4/np.sqrt(10)-1)*(a@a)/6
    assert np.allclose(c@ci, pw, atol=2e-14)
    return c, ci


def invariant_probe(g):
    """Ten supplied Gaussian parameters; optimization is evidence, not proof.

    Two 24-dimensional copies have a real symmetric 2x2 covariance and phase;
    the two 15-dimensional kernels have independent scalar covariances/phases.
    We do not assert this exhausts all invariant or all Gaussian states.
    """
    n, p, pl = g['n'], g['p'], g['pl']
    j = np.ones((40, 40))/40
    k, kl = np.eye(40)-j-p, np.eye(40)-j-pl
    r = (n-4*j)/np.sqrt(6)
    def energy(x):
        a, b, d, e = np.exp(x[[0, 1, 3, 4]])
        c = np.tanh(x[2])*np.sqrt(a*b)
        determinant = a*b-c*c
        cov = np.block([[a*p+d*k, c*r], [c*r.T, b*pl+e*kl]])
        inv = np.block([[b/determinant*p+k/d, -c/determinant*r],
                        [-c/determinant*r.T, a/determinant*pl+kl/e]])
        phase = np.block([[x[5]*p+x[8]*k, x[7]*r],
                          [x[7]*r.T, x[6]*pl+x[9]*kl]])
        return gaussian_energy(g['u'], g['v'], cov, inv, phase)[0]
    initial = np.zeros(10)
    initial[:2] = np.log(4/np.sqrt(10))
    initial[2] = np.arctanh(np.sqrt(6)/4)
    result = minimize(energy, initial, method='BFGS',
                      options={'gtol': 1e-8, 'maxiter': 500})
    return dict(energy=float(result.fun), parameters=result.x.tolist(),
                optimizer_success=bool(result.success), message=str(result.message),
                scope='An exploratory ten-parameter search, not a certified global minimum.')


def payload():
    g = geometry()
    c0, ci0 = spectral_covariance(g)
    trial = exact_trial()
    c, ci = trial['t']*c0, ci0/trial['t']
    phase = trial['f']*np.diag(g['s'])
    e, vx, vy, cross = gaussian_energy(g['u'], g['v'], c, ci, phase)
    assert abs(e-trial['energy']) < 1e-10
    assert all(np.ptp(a) < 1e-12 for a in (vx, vy, cross))
    no_phase = gaussian_energy(g['u'], g['v'], c0, ci0, np.zeros((80,80)))[0]
    isotropic = gaussian_energy(g['u'], g['v'], g['pw'], g['pw'],
                                np.zeros((80,80)))[0]
    assert abs(no_phase-(64.9+20.4*np.sqrt(10))) < 1e-11
    assert abs(isotropic-168.1) < 1e-11
    # At q=lambda*(kernel_witness,0), H psi/psi has this nonzero lambda^4
    # coefficient. Hence this Gaussian is not an eigenstate, even at its
    # exact restricted minimum. Schwartz residual gives strict descent.
    coefficient = 30240*(trial['f']+1j/trial['t'])**2
    assert abs(coefficient) > 30000
    probe = invariant_probe(g)
    source = Path(__file__)
    return dict(schema='w33.pass11769.quantized_current_vacuum.v1', status='PASS',
        source_sha256=hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        prior='analysis/w33_pass11767_global_current_algebra.py; standard Schrodinger representation is prior mathematics.',
        proposed_hamiltonian='H=sum_e J_e^2; J_e=(V_e.q+1/sqrt(20))*(U_e.p+1/sqrt(20)), [q_i,p_j]=i delta_ij on W=(u,s)^perp, dim W=78.',
        rejected_linear_energy='sum_e J_e=p^T Bsum q+8 I, Bsum=D(4P_W-A_W); Bsum^2=16P_W-A_W^2. Eigenvalues +/-sqrt(10), each multiplicity24, and +/-4, each multiplicity15. Coherent-state displacements make this operator unbounded above and below; it is not a stable energy.',
        quantization='For A=[[0,r,z],[0,B,v],[0,0,0]], hat(A)=p^T Bq+r.q+v.p+z I, tr B=0; [hat(A),hat(C)]=i hat([A,C]) on Schwartz space.',
        energy_units='Central charge and overall energy unit are supplied conventions, not predictions for hbar or a physical mass scale.',
        exact_integer_checks='160 actual incidences; T^2=30T, tr T=720 on both sides; G10^3=600G10; exact projected U,V Gram identities; U_e.V_e=0.',
        spectral_inventory={'adjacency_plus_sqrt6':24,'adjacency_minus_sqrt6':24,'adjacency_zero':30},
        isotropic_trial_energy=isotropic,
        real_spectral_trial={'exact_energy':'649/10+(102/5)*sqrt(10)', 'energy':no_phase,
            'scope':'Minimum only in the centered real Gaussian three-spectral-parameter class.',
            'covariance':'C0=P_W+A_W/sqrt(10)+(4/sqrt(10)-1)*A_W^2/6'},
        complex_trial={**trial,
            'state':'psi ∝ exp(-q.C0^-1.q/(2t) + i f q.D.q/2), D=diag(+1 points,-1 lines)|W',
            'root_equation':'(t^2-1)*(3*m*t+b)^2-4*b^2*t^2=0; m=(6sqrt(10)+15)/40, b=1/20; unique positive root t>1.',
            'phase_equation':'f=-2*b/(3*m*t+b)',
            'exact_energy':'160*(m^2+b*m*(t+1/t)+b^2-4*b^2*t*m/(3*m*t+b))',
            'minimum_scope':'Exact minimum within this two-real-parameter family; not all Gaussian states.',
            'edge_moments':dict(q_variance=float(vx[0]), p_variance=float(vy[0]), covariance=float(cross[0]))},
        exact_root_bracket=root_bracket(trial),
        non_gaussian_ritz=non_gaussian_ritz(trial),
        ten_parameter_probe=probe,
        non_gaussian_descent={'point_kernel_direction':g['kernel_witness'].tolist(),
            'sum_fourth_powers':7560,
            'quartic_coefficient':'30240*(f+i/t)^2 != 0',
            'coefficient_real':float(coefficient.real),'coefficient_imag':float(coefficient.imag),
            'consequence':'Trial is not an eigenstate. Taking psi-epsilon*(H-E)psi gives strictly smaller Rayleigh quotient for sufficiently small positive epsilon.'},
        lower_boundary='H has a nonnegative Friedrichs extension and no zero eigenvector: simultaneous current annihilation would annihilate the whole Lie closure, including its represented identity center. No positive gap, compact resolvent or attained ground state is proved.',
        classical_zero='Set a=1/sqrt20; q_point0=39a, q_other_points=-a, q_lines=0; p_point0=-a, p_other_points=a/39, p_lines=0. Both lie in W. Every non-star edge kills the position factor and each of the four star edges kills the momentum factor. Classical sum of squared current symbols is zero, while quantum H has no zero eigenvector; a strictly positive spectral infimum is NOT implied.',
        graph_locality='Disjoint edge currents commute exactly, hence so do their squares. An iterated commutator ad_H^k(J_e) is a sum of current words supported within distance k of e in the line graph. Its commutator with J_f vanishes when distance(e,f)>k+1. This is a formal nested-commutator support theorem, not a Lieb-Robinson bound for these unbounded operators or a continuum causal limit.',
        physical_boundary='An explicit interacting 78-coordinate quantum model, with a proposed energy law. No continuum locality, 3+1 Lorentz symmetry, chiral matter, GR, mass spectrum or cosmological constant is derived. These currents cannot all be anomaly-free gauge constraints at nonzero central charge.',
        literature=['https://arxiv.org/abs/math-ph/0505073'])


if __name__ == '__main__':
    result = payload()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('11769 PASS: positive interacting Hamiltonian; exact Gaussian-family trial',
          result['complex_trial']['energy'], '; non-Gaussian strict descent established')
