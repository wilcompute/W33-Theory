"""Independent operator, geometry and variational checks for Pass11769."""
import importlib.util
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('current_vacuum', ROOT/'analysis/w33_pass11769_quantized_current_vacuum.py')
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)


def test_actual_edge_quantization_blocks():
    g = A.geometry()
    u0 = np.ones(80)/np.sqrt(80)
    s0 = g['s']/np.sqrt(80)
    a = 1/np.sqrt(20)
    for k, (i,j) in enumerate(A.actual_edges()):
        plus, minus = np.zeros(80), np.zeros(80)
        plus[i] = plus[j] = 1
        minus[i], minus[j] = 1,-1
        m = np.outer(plus,minus)
        assert np.allclose(u0@m@g['pw'], a*g['v'][k])
        assert np.allclose(g['pw']@m@s0, a*g['u'][k])
        assert abs(u0@m@s0-a*a) < 1e-14
        assert np.allclose(g['pw']@m@g['pw'], np.outer(g['u'][k],g['v'][k]))


def test_schrodinger_lift_bracket_sign_and_center():
    # Quadratic Weyl symbols have exactly the Poisson bracket commutator.
    q = sp.Matrix(sp.symbols('q0:2'))
    p = sp.Matrix(sp.symbols('p0:2'))
    x = sp.Matrix([[0,2,-3,5],[0,1,2,7],[0,3,-1,-2],[0,0,0,0]])
    y = sp.Matrix([[0,-1,4,2],[0,2,-3,1],[0,1,-2,6],[0,0,0,0]])
    def symbol(m):
        return (p.T*m[1:3,1:3]*q)[0]+(m[0,1:3]*q)[0]+(p.T*m[1:3,3])[0]+m[0,3]
    f,g = symbol(x),symbol(y)
    poisson = sum(sp.diff(f,q[i])*sp.diff(g,p[i])-sp.diff(f,p[i])*sp.diff(g,q[i]) for i in range(2))
    assert sp.expand(poisson-symbol(x*y-y*x)) == 0
    r,v = sp.zeros(4),sp.zeros(4)
    r[0,1],v[1,3] = 1,1
    assert symbol(r*v-v*r) == 1


def test_exact_covariance_and_gaussian_energy():
    g = A.geometry()
    c,ci = A.spectral_covariance(g)
    w = np.linalg.eigvalsh(c)
    assert np.count_nonzero(w>1e-8) == 78
    assert np.allclose(c@ci,g['pw'],atol=2e-14)
    energy,*_ = A.gaussian_energy(g['u'],g['v'],c,ci,np.zeros((80,80)))
    assert abs(energy-(649/10+102*np.sqrt(10)/5)) < 1e-10


def test_complex_trial_and_exact_rational_root_isolation():
    trial = A.exact_trial()
    bracket = A.root_bracket(trial)
    assert len(bracket['t_interval']) == 2
    g = A.geometry()
    c,ci = A.spectral_covariance(g)
    energy,*_ = A.gaussian_energy(g['u'],g['v'],trial['t']*c,ci/trial['t'],trial['f']*np.diag(g['s']))
    assert abs(energy-trial['energy']) < 1e-10
    assert 128.88739 < energy < 128.88740


def test_non_gaussian_state_has_independent_degree_exact_matrix_elements():
    r = A.non_gaussian_ritz(A.exact_trial())
    assert 128.86806 < r['energy'] < 128.86807
    assert r['energy'] < r['gaussian_energy']
    assert max(r['quadrature_checks'].values()) < 2e-10
    coefficients = np.array([complex(*z) for z in r['coefficients']])
    assert abs(np.vdot(coefficients,coefficients)-1) < 1e-13
    k = complex(*r['off_diagonal'])
    h = np.array([[r['gaussian_energy'],k.conjugate()],[k,r['hermite_state_energy']]])
    assert np.linalg.norm(h@coefficients-r['energy']*coefficients) < 1e-11


def test_integer_non_gaussian_witness():
    g = A.geometry()
    w = g['kernel_witness']
    assert np.all(g['n'].T@w == 0)
    assert np.sum(w**4) == 7560
    trial = A.exact_trial()
    assert abs(30240*(trial['f']+1j/trial['t'])**2) > 30000


def test_energy_survives_independent_vertex_relabeling():
    g = A.geometry()
    c,ci = A.spectral_covariance(g)
    phase = -.03*np.diag(g['s'])
    energy,*_ = A.gaussian_energy(g['u'],g['v'],c,ci,phase)
    rng = np.random.default_rng(11769)
    perm = np.r_[rng.permutation(40),40+rng.permutation(40)]
    relabelled,*_ = A.gaussian_energy(g['u'][:,perm],g['v'][:,perm],c[np.ix_(perm,perm)],ci[np.ix_(perm,perm)],phase[np.ix_(perm,perm)])
    assert abs(relabelled-energy) < 1e-10
