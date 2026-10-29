"""Independent thermodynamic, causal, spectral and realization controls."""
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_pass12340_causal_harmonic_response as core


def test_exact_operator_spectrum_and_metric():
    r = core.exact_identities()
    M = s.Matrix(r['metric']).applyfunc(s.Rational)
    assert M == s.Matrix([[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]])
    K, _, _, _, _ = core.operators()
    assert (K+10*s.eye(27))*(K+s.eye(27))*(K-5*s.eye(27)) == s.zeros(27)
    assert M.det() > 0


def test_grand_potential_curvature_includes_thermal_static_jump():
    """Differentiate actual Peierls free energy, independently of Kubo weights."""
    K, _, _, M, h = core.operators()
    K = np.array(K, float)
    direction = np.array([1.,-.4,.3,.2])
    edges = list(zip(*np.where(np.triu(K) != 0)))
    # h's rows have native edge order, so reconstruct phase derivatives via J.
    J = sum(a*np.array(X,complex) for a,X in zip(direction,core.operators()[1]))
    T, mu = .25, -1.
    def free_energy(t):
        H = K.astype(complex)
        for a,b in edges:
            # K_ab exp(i t alpha_ab), J_ab = i alpha_ab K_ab.
            alpha = (J[a,b]/(1j*K[a,b])).real
            H[a,b] = K[a,b]*np.exp(1j*t*alpha)
            H[b,a] = H[a,b].conjugate()
        E = eigh(H,eigvals_only=True)
        return -T*np.logaddexp(0,(mu-E)/T).sum()
    eps = .0005
    fd = (free_energy(eps)+free_energy(-eps)-2*free_energy(0))/eps**2
    expected = core.coefficients(T,mu)['isothermal']*float(direction@np.array(M,float)@direction)
    assert abs(fd-expected) < 2e-4
    assert expected < 0 < core.coefficients(T,mu)['adiabatic']


def test_dense_response_all_complex_frequencies_and_populations():
    rows = core.numerical_controls()
    assert max(r['maximum_dense_Lehmann_error'] for r in rows) < 2e-10
    assert rows[0]['static_jump'] == 0


def test_causal_time_kernel_laplace_transform():
    """Numerical time-domain integral checks analytic continuation and sign."""
    z = .7+1.1j
    delta = core.coefficients(1.,2.)['population_difference']
    integral = quad(lambda t: (np.exp(1j*z*t)*np.sin(6*t)).real,0,np.inf)[0]
    integral += 1j*quad(lambda t: (np.exp(1j*z*t)*np.sin(6*t)).imag,0,np.inf)[0]
    result = core.coefficients(1.,2.)['contact']-delta*integral/3
    assert abs(result-core.retarded_coefficient(z,1.,2.)) < 1e-9


def test_residues_sum_rule_and_minimal_auxiliary_dimension():
    core.symbolic_completion()
    z = s.Symbol('z')
    R = s.Rational(2,9)-2/(36-z*z)
    assert s.residue(s.I*R/z,z,0) == s.I/6
    assert s.residue(s.I*R/z,z,6) == s.I/36
    assert s.Rational(1,6)+2*s.Rational(1,36) == s.Rational(2,9)
    M = core.operators()[3]
    assert (M/6).rank() == 4
    nu = s.Rational(3,7)
    # Independent exact full block determinant / Schur complement test.
    block = (s.Rational(2,9)*M).row_join(M).col_join(M.row_join((36+nu*nu)*M/2))
    effective = (s.Rational(2,9)-2/(36+nu*nu))*M
    assert block.det() == ((36+nu*nu)*M/2).det()*effective.det()


def test_second_period_basis_and_vertex_gauge_leave_tensor_law_covariant():
    K,J,D,M,_ = core.operators()
    H = np.array(K,complex)
    U = np.diag(np.exp(1j*np.linspace(-.7,.9,27)))
    T = np.array([[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1]])
    changedJ = [U@sum(T[i,j]*np.array(J[i],complex) for i in range(4))@U.conj().T for j in range(4)]
    changedD = [[U@sum(T[a,i]*T[b,j]*np.array(D[a][b],complex)
                          for a in range(4) for b in range(4))@U.conj().T
                 for j in range(4)] for i in range(4)]
    E,Q = eigh(U@H@U.conj().T)
    f = (E < 2).astype(float)
    rho = (Q*f)@Q.conj().T
    A = [Q.conj().T@X@Q for X in changedJ]
    gap = E[:,None]-E[None,:]
    df = f[:,None]-f[None,:]
    df[abs(gap)<1e-9] = 0
    z = 3.+.4j
    result = np.array([[np.trace(rho@changedD[i][j])+np.sum(df/(gap+z)*A[i]*A[j].T)
                        for j in range(4)] for i in range(4)])
    assert np.max(abs(result-core.retarded_coefficient(z,0.,2.)*(T.T@np.array(M,float)@T))) < 1e-11


def test_slater_fidelity_from_occupied_wavefunctions():
    """No spectral Kubo formula: overlap determinants of actual Slater states."""
    K,J,_,M,_ = core.operators()
    K = np.array(K,float)
    d = np.array([.3,-.8,.4,1.])
    vertex = sum(a*np.array(X,complex) for a,X in zip(d,J))
    _,Q0 = eigh(K)
    E0 = Q0[:,:21]
    def fidelity(eps):
        H = K.astype(complex)
        for a,b in zip(*np.where(np.triu(K) != 0)):
            alpha = (vertex[a,b]/(1j*K[a,b])).real
            H[a,b] *= np.exp(1j*eps*alpha)
            H[b,a] = H[a,b].conjugate()
        _,Q = eigh(H)
        return abs(np.linalg.det(E0.conj().T@Q[:,:21]))**2
    expected = d@np.array(M,float)@d/216
    estimate = (2-fidelity(.001)-fidelity(-.001))/(2*.001**2)
    assert abs(estimate-expected) < 2e-7
