"""Independent controls for a declared full-native scalar Wilson potential."""
import importlib.util
import json
import math
from itertools import product
from pathlib import Path
import numpy as np
import pytest
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("native_scalar_wilson",ROOT/"analysis/toe_20261108_native_scalar_wilson.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)


def test_full_native_geometry_and_exact_schur():
    B,V,a,b,h,G=M.geometry()
    assert B.shape==(135,27) and V.shape==(135,4)
    assert np.max(abs(B.T@h))<2e-13
    x=M.exact_normalization()
    assert x["Schur_scalar_kinetic"]=="27/5" and x["inverse_M44"]=="5/27"
    Z=sp.Matrix(G.tolist());u=sp.Matrix(sp.symbols("u:3"));v=sp.Symbol("v")
    w=u+Z[:3,:3].inv()*Z[:3,3]*v
    assert sp.expand((u.col_join(sp.Matrix([v])).T*Z*u.col_join(sp.Matrix([v])))[0]-(w.T*Z[:3,:3]*w)[0]-sp.Rational(27,5)*v*v)==0


def test_actual_incidence_matches_batched_operator():
    _,V,a,b,_,_=M.geometry()
    k=np.array([.17,-.23,.31,.11])
    D=np.zeros((135,27),complex)
    for e,(i,j) in enumerate(zip(a,b)):
        D[e,i]=-1;D[e,j]=np.exp(1j*k@V[e])
    H,_,_=M.matrices(k)
    assert np.max(abs(H[0]-D.conj().T@D))<2e-14
    assert abs(np.linalg.eigvalsh(H[0]).sum()-270)<1e-11


def test_vertex_cell_gauge_changes_preserve_full_band_spectrum():
    B,V,*_=M.geometry()
    shifts=np.random.default_rng(14).integers(-2,3,(27,4))
    k=np.array([.4,-.7,.3,.8])
    H=M.matrices(k)[0][0]
    H2=M.matrices(k,voltages=V+B@shifts)[0][0]
    U=np.diag(np.exp(1j*shifts@k))
    assert np.max(abs(H2-U.conj().T@H@U))<3e-14
    assert np.max(abs(np.linalg.eigvalsh(H)-np.linalg.eigvalsh(H2)))<2e-14


def test_theta_vertices_against_direct_differences():
    k=np.array([.3,.4,-.8,.27]);L=3;q=2;dt=1e-4
    H,Hp,Hpp=[x[0] for x in M.matrices(k,L,q)]
    shifted=[]
    for sign in (-1,1):
        kp=k.copy();kp[3]+=sign*q*dt/L;shifted.append(M.matrices(kp,L,q)[0][0])
    assert np.max(abs((shifted[1]-shifted[0])/(2*dt)-Hp))<2e-8
    assert np.max(abs((shifted[1]-2*H+shifted[0])/dt**2-Hpp))<8e-8


def test_lifted_real_space_and_bloch_spectra_agree():
    sizes=(2,1,1,2);theta=.713
    direct=M.full_cover_spectrum(sizes,theta)
    ks=np.array([[2*np.pi*x[0]/2,0,0,(2*np.pi*x[3]+theta)/2] for x in product(*(range(s) for s in sizes))])
    bloch=np.linalg.eigvalsh(M.matrices(ks)[0]).ravel()
    assert np.max(abs(np.sort(direct)-np.sort(bloch)))<4e-14


@pytest.mark.parametrize("L",[2,3,4])
def test_large_gauge_periodicity_and_charge(L):
    E=M.energy(3,L,.6,.47)
    assert M.energy(3,L,.6,.47+2*np.pi)==pytest.approx(E,abs=2e-12)
    assert M.energy(3,L,.6,-.47)==pytest.approx(E,abs=2e-12)
    assert M.energy(3,L,.6,.235,charge=2)==pytest.approx(E,abs=2e-12)


@pytest.mark.parametrize("L,mass",[(2,.3),(3,.8),(4,.3)])
def test_full_trace_curvature_matches_independent_five_point_energy(L,mass):
    n=3;h=.04
    _,c=M.energy(n,L,mass,0,curvature=True)
    E={i:M.energy(n,L,mass,i*h) for i in (-2,-1,0,1,2)}
    finite=(-E[2]+16*E[1]-30*E[0]+16*E[-1]-E[-2])/(12*h*h)
    assert c>0 and finite==pytest.approx(c,rel=3e-5,abs=4e-9)


def test_degenerate_sqrt_divided_difference_not_singular():
    H=np.zeros((1,3,3),complex);Hp=np.array([[[0,1,0],[1,0,2],[0,2,0]]],complex)
    Hpp=np.zeros_like(H)
    _,c=M.trace_sqrt_curvature(H,Hp,Hpp,2.)
    assert c[0]==pytest.approx(-np.trace(Hp[0]@Hp[0]).real/(4*2**3),abs=1e-14)


def test_complex_scalar_factor_is_two_real_oscillators():
    e=M.energy(2,2,.8,0)
    H=M.matrices(M.grid(2,2,0))[0]
    real_zero_point=.5*np.sqrt(np.linalg.eigvalsh(H)+.8**2).sum()/2**3
    assert e==pytest.approx(2*real_zero_point,abs=1e-12)


def test_literal_closed_walk_has_primitive_fourth_period():
    x=M.literal_winding_path()
    assert x["primitive_period"]==[0,0,0,1] and x["steps"]>0
    _,V,a,b,_,_=M.geometry();v=0;z=np.zeros(4,int)
    for e,s in x["signed_edges"]*3:
        assert v==(a[e] if s==1 else b[e])
        v=b[e] if s==1 else a[e];z+=s*V[e]
    assert v==0 and z.tolist()==[0,0,0,3]


def test_actual_independent_server_matrix_series():
    d=json.loads((ROOT/'data/toe_20261108_native_scalar_wilson_server.json').read_text())
    assert d['runtime']=='Actual functions.exec V8'
    for row in d['rows']:
        assert M.energy(2,2,3,row['theta'])==pytest.approx(row['energy'],abs=2e-11)
    _,c=M.energy(2,2,3,0,curvature=True)
    assert c==pytest.approx(d['five_point_curvature'],abs=3e-9)
    assert all(row['rigorous_series_tail_bound']<1e-17 for row in d['rows'])


def test_positive_walk_bound_matches_independent_gamma_integral():
    import mpmath as mp
    d=M.winding_curvature_lower_bound(2,.8);r=d['walk_length']
    with mp.workdps(40):
        direct=2/mp.sqrt(mp.pi)/mp.factorial(r)*mp.quad(lambda t:t**(r-mp.mpf('1.5'))*mp.exp(-mp.mpf('10.64')*t),[0,1,mp.inf])
        assert float(mp.log10(direct))==pytest.approx(d['log10_numeric_lower_bound'],abs=1e-12)
    _,c=M.energy(3,2,.8,0,curvature=True)
    assert c>math.exp(d['log10_numeric_lower_bound']*math.log(10))>0


@pytest.mark.parametrize('n',[2,3])
def test_divisible_finite_cover_upper_bounds_decrease(n):
    e0,c0=M.energy(n,2,.8,0,curvature=True)
    e1,c1=M.energy(2*n,2,.8,0,curvature=True)
    d0=M.energy(n,2,.8,1.)-e0
    d1=M.energy(2*n,2,.8,1.)-e1
    assert c0>c1>0 and d0>d1>0


@pytest.mark.parametrize("theta",[.3,1.,2.,np.pi])
def test_declared_scalar_global_minimum_numerical_controls(theta):
    assert M.energy(3,3,.4,theta)>M.energy(3,3,.4,0)
