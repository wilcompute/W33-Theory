"""Exact homogenization and independent finite-momentum completion controls."""
import importlib.util,json
from pathlib import Path
import numpy as np
import pytest
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location('invariant_native',ROOT/'analysis/toe_20261108_invariant_magnetic_completion.py')
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
@pytest.fixture(scope='module')
def m():return M.completion()

def test_exact_short_face_projection(m):
    assert m['exact_proof']['normal_equations_exact'] and m['exact_proof']['antisymmetry_exact']
    assert m['chi_exact']==sp.diag(sp.Rational(29857,5775),0,0,0,0,0)
    assert np.max(abs(m['A'].T@m['residual'].reshape(1287,16)))<2e-12

def test_integer_period_cup_rank_and_nonuniform_weight_control(m):
    d=m['topology']
    assert d['polygon_twice_area_mod_optical_exact'] and d['period_cup_image_rank']==1
    assert d['face_cohomology_dimension']==1182
    assert abs(d['weighted_area_coefficient']-float(m['chi_exact'][0,0]))>.01
    assert d['weighted_other_components_max']<1e-12

def test_positive_compensation_boundary(m):
    c=m['chi_exact'];T=m['target'];critical=1/m['relative']
    assert critical==sp.Rational(5775,29857)
    assert (T-critical*c).det()==0
    assert all(m['H'][:i,:i].det()>0 for i in range(1,7))
    assert float(critical)>float(m['alpha'])
    assert np.linalg.eigvalsh(np.array(T-2*critical*c,float)).min()<0
    y=m['overshoot_simple']
    assert (y.T*c*y)[0]>(y.T*T*y)[0]
    assert y[0]*y[5]-y[1]*y[4]+y[2]*y[3]==0

def test_every_mapped_commutator_is_literal_closed_zero_voltage(m):
    for g,block in enumerate(m['blocks']):
        assert len(block)==6
        for face in block:
            assert len(face)==16
            vertex=m['lifts'][g]['vertex'][0];start=vertex;pos=np.zeros(4,int)
            for e,s in face:
                a,b=m['edges'][e] if s==1 else m['edges'][e][::-1]
                assert vertex==a;vertex=b;pos+=s*m['V'][e]
            assert vertex==start and not pos.any()

@pytest.mark.parametrize('n',[[1,0,0,0],[0,0,1,0],[1,2,-1,1]])
def test_exact_leading_common_cone(m,n):
    W=sp.Matrix(M.wedge(n).astype(int).tolist());n=sp.Matrix(n);G=m['M']
    target=((n.T*G*n)[0]*G-G*n*n.T*G)/27
    assert W.T*m['target']*W==target
    assert m['alpha']*m['chi_exact']+m['complement']==m['target']

def test_independent_finite_difference_optical_homogenization(m):
    n=np.array([1.,2.,-1.,1.]);x=np.array([.3,-.2,.7,.9]);errors=[]
    for t in (.004,.002):
        F=M.prior.curl(m['faces'],m['V'],t*n)
        a=F@m['hf']@x;A=F@m['C']
        # Direct complex finite-k least-squares, distinct from analytic derivative.
        y=np.linalg.lstsq(A,-a,rcond=None)[0]
        energy=np.linalg.norm(a+A@y)**2/t**2
        predicted=float((M.wedge(n)@x)@m['chi']@(M.wedge(n)@x))
        errors.append(abs(energy-predicted))
    assert errors[-1]<errors[0] and errors[-1]<2e-4

@pytest.mark.parametrize('g',[3,9,17])
def test_nonzero_momentum_controller_covariance(m,g):
    r=M.covariance(np.array([.17,-.23,.31,.11]),g)
    assert r['gradient_covariance_max']<2e-12 and r['magnetic_covariance_max']<2e-10

def test_propagating_completion_vs_short_only_flat_modes(m):
    k=np.array([.17,-.23,.31,.11]);short=M.spectrum(k,False);full=M.spectrum(k)
    assert max(abs(np.array(short['lowest_squared_frequencies'][:2])))<1e-11
    assert full['lowest_squared_frequencies'][0]>1e-5 and full['Ward_max']<2e-12

def test_numerical_acoustic_limit_and_finite_k_splitting(m):
    n=np.array([1.,2.,-1.,1.]);predicted=n@np.array(m['M'],float)@n/27;errors=[]
    for t in (.02,.005):
        r=M.spectrum(t*n);scaled=np.array(r['lowest_squared_frequencies'][:3])/t**2
        errors.append(max(abs(scaled-predicted)))
    assert errors[-1]<errors[0] and errors[-1]/predicted<.01
    assert np.ptp(scaled)>1e-7  # leading matching is not an exact finite-k cone

def test_actual_server_independent_six_area_control():
    d=json.loads((ROOT/'data/toe_20261108_invariant_magnetic_server.json').read_text())
    assert d['runtime']=='Actual functions.exec V8' and d['Cholesky_max_error']<2e-14
    assert min(d['Cholesky_diagonal'])>0
    for r in d['cases']:
        assert abs(r['transverse'])<3e-13
        assert r['total']==pytest.approx(r['predicted'],rel=2e-14,abs=1e-13)
