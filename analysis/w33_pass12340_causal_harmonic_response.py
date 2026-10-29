"""All-frequency harmonic response of the existing 27-site free fermion cell.

Prior owner of the geometry/current trace identities and low-frequency response:
analysis/w33_20261027_acoustic_density_backreaction.py. This is a causal Kubo
completion and input-output identifiability audit, not new Maxwell dynamics.
Standard conductivity/sum-rule conventions: arXiv:2004.04561.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import sympy as s
from scipy.linalg import eigh
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import w33_20261027_native_operator_closure as native


@lru_cache(None)
def operators():
    """Recompute exact harmonic representatives; do not load prior answer JSON."""
    B, V, edges, _ = native.geometry()
    B, V = s.Matrix(B), s.Matrix(V)
    b = B[:, 1:]
    h = V - b * (b.T*b).inv() * b.T * V
    M = h.T*h
    K = s.zeros(27)
    currents = [s.zeros(27) for _ in range(4)]
    second = [[s.zeros(27) for _ in range(4)] for _ in range(4)]
    for e, (a, z) in enumerate(edges):
        K[a, z] = K[z, a] = -1
        for i in range(4):
            currents[i][z, a] = -s.I*h[e, i]
            currents[i][a, z] = s.I*h[e, i]
            for j in range(4):
                second[i][j][a, z] = second[i][j][z, a] = h[e, i]*h[e, j]
    assert B.T*h == s.zeros(27, 4)
    return K, currents, second, M, h


def exact_identities():
    K, currents, second, M, _ = operators()
    I = s.eye(27)
    projectors = [s.ones(27)/27, -(K+10*I)*(K-5*I)/54,
                  (K+10*I)*(K+I)/90]
    energies = [-10, -1, 5]
    multiplicities = [1, 20, 6]
    for P, E, n in zip(projectors, energies, multiplicities):
        assert P*P == P and K*P == E*P and s.trace(P) == n
    assert sum(projectors, s.zeros(27)) == I
    block_coefficients = []
    for a, P in enumerate(projectors):
        row = []
        for b, Q in enumerate(projectors):
            T = s.Matrix(4, 4, lambda i, j: s.trace(P*currents[i]*Q*currents[j]))
            coefficient = T[0, 0]/M[0, 0]
            assert T == coefficient*M
            row.append(coefficient)
        block_coefficients.append(row)
    assert block_coefficients == [[0, 0, 0], [0, s.Rational(5, 3), s.Rational(1, 6)],
                                 [0, s.Rational(1, 6), 0]]
    contacts = []
    for P in projectors:
        T = s.Matrix(4, 4, lambda i, j: s.trace(P*second[i][j]))
        coefficient = T[0, 0]/M[0, 0]
        assert T == coefficient*M
        contacts.append(coefficient)
    assert contacts == [s.Rational(2, 27), s.Rational(4, 27), -s.Rational(2, 9)]
    L, D = M.LDLdecomposition()
    assert L*D*L.T == M and all(x > 0 for x in D.diagonal())
    # The filled21 Slater determinant's Fubini-Study metric is another moment
    # of the same transition tensor, not a spacetime/gravitational metric.
    Pocc = projectors[0]+projectors[1]
    dP = [-(projectors[1]*J*projectors[2]+projectors[2]*J*projectors[1])/6 for J in currents]
    quantum_metric = s.Matrix(4, 4, lambda i,j: s.trace(dP[i]*dP[j])/2)
    berry = s.Matrix(4, 4, lambda i,j: s.I*s.trace(Pocc*(dP[i]*dP[j]-dP[j]*dP[i])))
    assert quantum_metric == M/216 and berry == s.zeros(4)
    return dict(metric=[[str(x) for x in row] for row in M.tolist()],
                metric_determinant=str(M.det()),
                metric_LDL_diagonal=list(map(str, D.diagonal())),
                spectrum=dict(zip(map(str, energies), multiplicities)),
                current_blocks=[[str(x) for x in row] for row in block_coefficients],
                contact_coefficients=list(map(str, contacts)),
                filled21_quantum_geometry=dict(Fubini_Study_metric='M/216', Berry_curvature='zero',
                    metric_to_electric_coefficient_ratio='3',
                    scope='Local occupied-Slater-state parameter geometry at zero holonomy. Not a global band invariant, quantized Chern class, spacetime metric or gravitational field.'))


def occupations(T, mu):
    if T < 0:
        raise ValueError('Only nonnegative temperatures are supported')
    E = np.array([-10., -1., 5.])
    if T == 0:
        if np.min(abs(mu-E)) < 1e-10:
            raise ValueError('T=0 requires chemical potential off the shells')
        return (E < mu).astype(float)
    return expit((mu-E)/T)


def coefficients(T, mu):
    fg, fm, fp = occupations(T, mu)
    contact = (2*fg+4*fm-6*fp)/27
    delta = fm-fp
    adiabatic = contact-delta/18
    thermal = 5*fm*(1-fm)/(3*T) if T else 0.
    return dict(contact=float(contact), population_difference=float(delta),
                adiabatic=float(adiabatic), isothermal=float(adiabatic-thermal),
                static_jump=float(thermal))


def retarded_coefficient(z, T, mu):
    """Analytic in Im(z)>0. Boundary values mean z=omega+i0+."""
    c = coefficients(T, mu)
    return c['contact'] - 2*c['population_difference']/(36-z*z)


def dense_lehmann(z, T, mu):
    """Independent dense spectral evaluation, including contact, at complex z."""
    K, J, second, _, _ = operators()
    H = np.array(K, float)
    E, U = eigh(H)
    f = expit((mu-E)/T) if T else (E < mu).astype(float)
    rho = (U*f)@U.T
    A = [U.conj().T@np.array(X, complex)@U for X in J]
    gap = E[:, None]-E[None, :]
    df = f[:, None]-f[None, :]
    # Suppress numerical splitting of exactly degenerate energy shells.
    df[abs(gap) < 1e-9] = 0.
    W = df/(gap+z)
    return np.array([[np.trace(rho@np.array(second[i][j], float)) +
                      np.sum(W*A[i]*A[j].T) for j in range(4)] for i in range(4)])


def symbolic_completion():
    z, nu, fg, fm, fp = s.symbols('z nu f_g f_m f_p', real=True)
    contact = (2*fg+4*fm-6*fp)/27
    delta = fm-fp
    R = contact-2*delta/(36-z*z)
    R0 = s.factor(R.subs(z, 0))
    assert s.simplify(R0-(4*fg+5*fm-9*fp)/54) == 0
    euclidean = R.subs(z, s.I*nu)
    assert s.simplify((euclidean-R0)/nu**2-delta/(18*(36+nu**2))) == 0
    residue = s.residue(R, z, 6)
    assert residue == delta/6
    sigma = s.I*R/z
    # Re sigma / pi = R0 delta(omega) + delta/36 [delta(omega-6)+delta(omega+6)].
    assert s.simplify(R0+2*delta/36-contact) == 0
    assert s.limit(z*sigma, z, s.oo) == s.I*contact
    # At T=0, mu=2: all 21 low orbitals filled.
    fixed = {fg: 1, fm: 1, fp: 0}
    assert R0.subs(fixed) == s.Rational(1, 6)
    assert contact.subs(fixed) == s.Rational(2, 9)
    # Eliminate four auxiliary harmonic coordinates with Q=M*(36+nu^2)/(2 delta).
    # Their Schur complement is [contact-2delta/(36+nu^2)] M.
    return dict(retarded_kernel_over_M=str(R), euclidean_kernel_over_M=str(euclidean),
                regular_zero_frequency_over_M=str(R0),
                electric_low_frequency_over_M='(f_m-f_p)/648',
                retarded_poles=[-6, 6], positive_pole_residue_over_M=str(residue),
                inverse_transform='K_R(t)=M*[contact*delta(t)-(f_m-f_p)*theta(t)*sin(6*t)/3]',
                formal_conductivity='sigma(z)=i*K_R(z)/z, E=-dA/dt, Fourier convention exp(-i omega t)',
                real_conductivity_over_pi_M='R0*delta(omega)+(f_m-f_p)/36*[delta(omega-6)+delta(omega+6)]',
                full_line_sum_rule='integral Re sigma(omega) d omega = pi*contact*M',
                filled21=dict(contact='2/9', adiabatic='1/6', each_optical_delta='1/36',
                              zero_frequency_weight_fraction='3/4',
                              total_finite_frequency_weight_fraction='1/4'),
                oscillator_equivalence=dict(auxiliary_dimension=4,
                    auxiliary_inverse='(36+nu^2)*M/[2*(f_m-f_p)]', coupling='M', contact='contact*M',
                    minimality='The positive-frequency pole residue is (f_m-f_p)*M/6 of rank4 for f_m>f_p. Four independent scalar harmonic coordinates suffice and fewer cannot realize its residue rank.',
                    boundary='Exact equality only for the collisionless quadratic four-probe response at a chosen T,mu. The oscillator parameters depend on the populations. This is not an equivalence of the fermion Fock space, higher correlators or the separate isothermal zero-Matsubara term.'))


def numerical_controls():
    M = np.array(operators()[3], float)
    values = []
    for T, mu in ((0., 2.), (0., -5.), (.25, -1.), (1., 2.), (2., -10.), (10., 0.)):
        c = coefficients(T, mu)
        errors = []
        for z in (.4+.3j, 5.8+.1j, 8.+.4j, 2j, 30j):
            expected = retarded_coefficient(z, T, mu)*M
            errors.append(float(np.max(abs(dense_lehmann(z, T, mu)-expected))))
        assert max(errors) < 2e-10
        # Oscillator realization checked as a matrix Schur complement.
        if c['population_difference'] > 1e-14:
            nu = .7
            Q = (36+nu*nu)*M/(2*c['population_difference'])
            Kaux = c['contact']*M-M@np.linalg.solve(Q, M)
            assert np.max(abs(Kaux-retarded_coefficient(1j*nu, T, mu)*M)) < 1e-12
        # Formal finite-ring spectral weights are nonnegative at Gibbs populations.
        assert c['population_difference'] >= 0 and c['adiabatic'] >= -1e-14
        values.append(dict(T=T, mu=mu, **c, maximum_dense_Lehmann_error=max(errors)))
    return values


def run():
    return dict(schema='w33.pass12340.causal_harmonic_response.v1',
                base_commit='41b1bb2434034af141500087308cd6084cbe4f10',
                prior_owner='analysis/w33_20261027_acoustic_density_backreaction.py',
                primary_method='https://arxiv.org/abs/2004.04561',
                exact=exact_identities(), completion=symbolic_completion(), controls=numerical_controls(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                units='Nearest-edge hopping amplitude, charge and hbar set to1; harmonic flux response has no spatial-volume normalization.',
                scope='Finite free spinless27-site/135-edge cell and four harmonic holonomy probes. No nonzero spatial momentum, thermodynamic Drude weight, bulk conductor/insulator classification, derived Maxwell photon, universal speed, chiral vacuum or TOE. The existing no-global21-band-gap cover obstruction remains in force.')


if __name__ == '__main__':
    result = run()
    target = ROOT/'data/w33_pass12340_causal_harmonic_response.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', output=str(target),
                         max_dense_error=max(x['maximum_dense_Lehmann_error'] for x in result['controls']))))
