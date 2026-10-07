"""Independent metric, curvature, full-grid heat and rank-four regressions."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import iv
import sympy as s

ROOT=Path(__file__).resolve().parents[1]


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def certificate():
    return json.loads((ROOT/'data/w33_pass11601_matched_metric_dirac.json').read_text())


def test_portable_source_binding_and_preserved_firewall():
    d=certificate()
    for path,want in d['source_sha256'].items():
        p=ROOT/path
        raw=json.dumps(json.loads(p.read_text()),sort_keys=True,separators=(',',':')).encode() if p.suffix=='.json' else p.read_bytes().replace(b'\r\n',b'\n')
        assert hashlib.sha256(raw).hexdigest()==want
    raw=(ROOT/'analysis/w33_pass11601_matched_metric_dirac.py').read_bytes().replace(b'\r\n',b'\n')
    assert hashlib.sha256(raw).hexdigest()==d['producer_sha256']
    old=json.loads((ROOT/'data/PART_W33_PASS11594_REFINED_GRAVITY_FIREWALL.json').read_text())
    assert old['status'].startswith('FIREWALL') and old['rows'][-1]['ratio']['1.0']<0


def test_actual_native_symbol_in_two_coframe_realizations():
    native=module('analysis/w33_pass11557_pin_equivariant_event_dirac.py','native11601')
    gam,_=native.small_clifford();gam=[np.array(a,complex) for a in gam]
    E=np.array([[2.,1,0],[0,1,1],[0,0,1]])
    R=np.array([[0.,-1,0],[1,0,0],[0,0,1]])
    rng=np.random.default_rng(11601)
    for F in [E,R@E]:
        g=F.T@F
        for p in rng.normal(size=(8,3)):
            q=np.linalg.inv(F).T@p
            Q=sum(a*v for a,v in zip(gam,q))
            assert np.linalg.norm(Q@Q-(p@np.linalg.inv(g)@p)*np.eye(4))<1e-12
    p=np.array([1.,0,0]);wrong=sum(a*v for a,v in zip(gam,E@p))
    assert np.linalg.norm(wrong@wrong-(p@np.linalg.inv(E.T@E)@p)*np.eye(4))>1


def test_old_density_formula_and_strict_spectral_volume_gap():
    eps=.12;rng=np.random.default_rng(63)
    for a,b,c in rng.uniform(0,2*np.pi,size=(12,3)):
        E=np.diag(np.exp(eps*np.array([np.sin(a),np.cos(b),np.sin(c)])))
        E[0,1]=.35*eps*np.sin(c);E[1,2]=.25*eps*np.cos(a);E[2,0]=.2*eps*np.sin(b)
        formula=np.exp(eps*(np.sin(a)+np.cos(b)+np.sin(c)))+.35*.25*.2*eps**3*np.sin(c)*np.cos(a)*np.sin(b)
        assert abs(np.linalg.det(E)-formula)<1e-14
    rows=certificate()['old_volume']['rows']
    assert abs(rows[-1]['unmatched_volume']-5.411249214347)<1e-10
    assert max(r['spectral_volume'] for r in rows)-min(r['spectral_volume'] for r in rows)<1e-10
    # A positive nonconstant normalized density must increase its inverse mean.
    J=np.array([.5,1,1.5]);assert J.mean()==1 and np.mean(1/J)>1


def test_conformal_curvature_from_independent_christoffels_and_quadrature():
    geom=module('analysis/w33_einstein_field_equations_from_spectral_action.py','geom11601')
    x,y,z=s.symbols('x y z');sigma=s.Function('sigma')(x);scale=s.symbols('scale',positive=True)
    _,_,R,_,_=geom.einstein_tensor(scale**2*s.exp(2*sigma)*s.eye(3),[x,y,z])
    assert s.simplify(R*scale**2*s.exp(2*sigma)+4*s.diff(sigma,x,2)+2*s.diff(sigma,x)**2)==0
    for eps in [.12,.2]:
        a=iv(0,3*eps)**(-1/3)
        integral=(2*np.pi)**2*a*quad(lambda t:np.exp(eps*np.cos(t))*(4*eps*np.cos(t)-2*eps**2*np.sin(t)**2),0,2*np.pi,epsabs=1e-12)[0]
        row=next(r for r in certificate()['conformal_rows'] if r['eps']==eps)
        assert abs(integral-row['integrated_R'])<1e-11


def test_small_full_three_dimensional_operator_matches_shell_reduction():
    m=module('analysis/w33_pass11601_matched_metric_dirac.py','matched11601')
    L=5;eps=.12;x,k,P=m.circle_momentum(L);I=np.eye(L)
    momenta=[np.kron(np.kron(P,I),I),np.kron(np.kron(I,P),I),np.kron(np.kron(I,I),P)]
    f=np.repeat(np.exp(-eps*np.cos(x))/iv(0,3*eps)**(-1/3),L*L)
    gam,_=m.native.small_clifford();D=np.zeros((4*L**3,4*L**3),complex)
    for g,p in zip(gam,momenta):
        D+=np.kron(np.array(g,complex),.5*(f[:,None]*p+p*f[None,:]))
    ev=np.linalg.eigvalsh(D);times=np.array([.2,.1])
    actual=np.exp(-times[:,None]*ev[None,:]**2).sum(axis=1)
    reduced=m.conformal_heat(eps,L,K=2,times=times)
    assert np.max(np.abs(actual-np.array(reduced['heat'])))<1e-10


def test_rank_four_curvature_coefficient_without_fitting():
    d=certificate();c=-4/(12*(4*np.pi)**1.5)
    assert c==d['expected_a2_rank4_d3']
    for eps in [.12,.2]:
        rows=[r for r in d['conformal_rows'] if r['eps']==eps]
        fine=rows[-1]
        assert abs(fine['normalized_a2'][-1]/c-1)<.002
        assert abs(rows[-2]['normalized_a2'][-1]-fine['normalized_a2'][-1])<1e-5
        # The time correction decreases after the spatial cutoff is resolved.
        assert abs(fine['normalized_a2'][-1]-c)<abs(fine['normalized_a2'][0]-c)
    assert 'nonlocal' in d['scope'] and 'supplied external smooth metrics' in d['scope']


def test_nonconformal_warped_metric_has_no_integrated_curvature_term():
    x=s.symbols('x');f=s.Function('f')(x);scale=s.symbols('scale',positive=True)
    y,z=s.symbols('y z')
    geom=module('analysis/w33_einstein_field_equations_from_spectral_action.py','warpgeom11601')
    _,_,R,_,_=geom.einstein_tensor(scale**2*s.diag(1,f*f,1),[x,y,z])
    assert s.simplify(R*scale**2*f+2*s.diff(f,x,2))==0
    row=certificate()['warped_rows'][-1]
    assert row['integrated_R']==0 and abs(row['sqrt_t_delta'][-1])<.001
    assert .45<row['sqrt_t_delta'][-1]/row['sqrt_t_delta'][-2]<.55


def test_four_dimensional_clifford_factor_and_coefficient():
    X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    gam=[s.kronecker_product(X,a) for a in [X,Y,Z]]
    gt=s.kronecker_product(Y,s.eye(2));p=s.symbols('p0:4')
    D3=sum((a*b for a,b in zip(gam,p)),s.zeros(4))
    assert s.simplify((D3+gt*p[3])**2-D3**2-p[3]**2*s.eye(4))==s.zeros(4)
    d=certificate()['four_dimensional'];c=-4/(12*(4*np.pi)**2)
    assert d['expected_a2']==c and abs(d['normalized_a2'][-1]/c-1)<.002
    assert 'not generic4D dynamics' in d['boundary']


def test_independent_spin_curvature_trace_and_unfitted_a4_correction():
    native=module('analysis/w33_pass11557_pin_equivariant_event_dirac.py','spinR11601')
    gam=[np.array(a,complex) for a in native.small_clifford()[0]]
    Ric=np.diag([-.46,-.2589,-.2589]);R=np.trace(Ric);I=np.eye(3)
    T=np.zeros((3,3,3,3))
    for a,b,c,d in itertools.product(range(3),repeat=4):
        T[a,b,c,d]=I[a,c]*Ric[b,d]+I[b,d]*Ric[a,c]-I[a,d]*Ric[b,c]-I[b,c]*Ric[a,d]-R*(I[a,c]*I[b,d]-I[a,d]*I[b,c])/2
    omega_trace=0j
    for i,j in itertools.product(range(3),repeat=2):
        Om=sum(T[a,b,i,j]*(gam[a]@gam[b])/4 for a,b in itertools.product(range(3),repeat=2))
        omega_trace+=np.trace(Om@Om)
    assert abs(omega_trace+4*np.sum(T*T)/8)<1e-12
    total=4*(5*R*R-2*np.sum(Ric*Ric)+2*np.sum(T*T)-15*R*R+180*R*R/16)+30*omega_trace
    assert abs(total/360-4*(R*R-3*np.sum(Ric*Ric))/120)<1e-12
    for row in certificate()['conformal_rows']:
        if row['L']!=161:continue
        eps=row['eps'];scale=iv(0,3*eps)**(-1/3)
        integral=-2*(2*np.pi)**2/scale*quad(lambda x:np.exp(-eps*np.cos(x))*(-eps*np.cos(x)-eps**2*np.sin(x)**2)**2,0,2*np.pi)[0]
        a4=integral/(30*(4*np.pi)**1.5)
        assert abs(a4-row['curvature_squared_prediction']['predicted_a4'])<1e-12
        corrected=np.array(row['normalized_a2'])-np.array(certificate()['times'])*a4/row['integrated_R']
        assert abs(corrected[-1]/certificate()['expected_a2_rank4_d3']-1)<1e-5
