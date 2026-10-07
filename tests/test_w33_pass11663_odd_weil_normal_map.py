"""Independent parity, normal-map, rank and quantum-phase controls for11663."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis'))
import w33_pass11663_odd_weil_normal_map as M


def test_certificate_and_exact_classical_identity():
    data=json.loads(M.OUT.read_text())
    assert data['status']=='PASS'
    assert data['producer_sha256']==hashlib.sha256(Path(M.__file__).read_text().encode()).hexdigest()
    _,_,K=M.cubic_normal_map(); F=M.pfaffian_vector(K)
    assert (K*F).applyfunc(s.expand)==s.zeros(5,1)
    y=[F[0]/4,*[z/2 for z in F[1:]]]
    assert s.expand(y[0]**4+y[0]*sum(z**3 for z in y[1:])+3*s.prod(y[1:]))==0
    # A sign or coefficient corruption destroys the quartic identity.
    assert s.expand(y[0]**4-y[0]*sum(z**3 for z in y[1:])+3*s.prod(y[1:]))!=0


def test_normal_map_against_committed_cubic_tensor():
    import w33_pass11651_n_qutrit_hesse_space as H
    _,_,_,B,_=H.setup(2)
    E,O=M.parity_bases()
    en=np.array(E,dtype=complex)@np.diag([1,*([1/np.sqrt(2)]*4)])
    on=np.array(O,dtype=complex)/np.sqrt(2)
    u=lambda p:B.T@np.kron(np.kron(p,p),p)
    rng=np.random.default_rng(3354)
    for _ in range(12):
        f=rng.normal(size=4)+1j*rng.normal(size=4)
        b=rng.normal(size=5)+1j*rng.normal(size=5)
        assert np.linalg.norm(u(on@f))<1e-11
        t=.37
        assert np.allclose(u(on@f+t*en@b),t*M.canonical_mass(f)@b+t**3*u(en@b),atol=1e-10)


def test_all_forty_witting_rays_have_rank_two():
    _,_,K=M.cubic_normal_map();F=M.pfaffian_vector(K)
    rays=M.exact_base_rays()
    assert len(rays)==40
    for ray in rays:
        sub=dict(zip(M.FVAR,ray))
        assert all(M.reduce_w(z)==0 for z in F.subs(sub,simultaneous=True))
        kr=K.subs(sub,simultaneous=True).applyfunc(M.reduce_w)
        assert any(z!=0 for z in kr)
    dictionary, rr=M.witting_pauli_dictionary(rays)
    assert len(set(dictionary['base_ray_indices']))==40
    assert dictionary['point_graph_degree']==[12]
    for ray in rr:
        mm=M.canonical_mass(ray)
        assert np.allclose(np.linalg.eigvalsh(mm.conj().T@mm),[0,0,0,.5,.5])


def test_generic_and_balanced_mass_spectra():
    rng=np.random.default_rng(8440)
    for _ in range(30):
        f=rng.normal(size=4)+1j*rng.normal(size=4);f/=np.linalg.norm(f)
        S=M.order_parameter(f);assert 0<=S<=1+1e-12
        mm=M.canonical_mass(f);ev=np.linalg.eigvalsh(mm.conj().T@mm)
        assert abs(ev.sum()-1)<1e-12
        assert abs(ev[1]*ev[3]-S/16)<1e-12
        assert np.allclose(ev, [0,*([(1-np.sqrt(1-S))/4]*2),*([(1+np.sqrt(1-S))/4]*2)])
    f=np.array([1,1j,0,0])/np.sqrt(2)
    assert abs(M.order_parameter(f)-1)<1e-12
    mm=M.canonical_mass(f)
    assert np.allclose(np.linalg.eigvalsh(mm.conj().T@mm),[0,.25,.25,.25,.25])


def test_actual_dirac_inventory_and_quantum_thresholds():
    A,B,y=.01,.25,.2
    nodes,weights=np.polynomial.legendre.leggauss(128)
    xs=(B+A)/2+(B-A)*nodes/2;ws=(B-A)*weights/2
    for f in [np.array([1,0,0,0]),np.array([1,1j,0,0])/np.sqrt(2),
              np.array([1,2,3j,4])/np.sqrt(30)]:
        mm=M.canonical_mass(f);ev=np.maximum(0,np.linalg.eigvalsh(mm.conj().T@mm))
        # Each Dirac determinant has spin factor -2; Euclidean radial measure is x dx/(16pi^2).
        actual=-2*sum(w*x*np.log1p(y*y*ev/x).sum() for x,w in zip(xs,ws))/(16*np.pi**2)
        assert abs(actual-M.loop_energy(M.order_parameter(f),y,A,B))<1e-14
    th=M.phase_thresholds(y,A,B)
    assert 0<th['balanced_threshold']<th['Witting_threshold']
    assert abs(M.loop_slope(0,y,A,B)+th['Witting_threshold'])<1e-15
    assert abs(M.loop_slope(1,y,A,B)+th['balanced_threshold'])<1e-15
    # Fermions alone favor rank-four balance, not the40 rank-two vacua.
    assert M.loop_energy(1,y)<M.loop_energy(0,y)
    # Strict convexity and the exact intermediate derivative select S=.5.
    k=-M.loop_slope(.5,y)
    energy=lambda z:k*z+M.loop_energy(z,y)
    assert energy(.5)<energy(.4) and energy(.5)<energy(.6)
