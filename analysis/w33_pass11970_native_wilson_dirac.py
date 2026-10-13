"""A local Wilson Hamiltonian on the actual marked 80-site Levi cover.

Prior11956 owns harmonic-period data;11566 owns an external Hamming Wilson
regulator. This construction uses the native links, not a tensor torus stencil.
Continuous time and the three-deck marking are inputs. Free, vectorlike only.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import sys
import numpy as np
import sympy as sp
from scipy.linalg import eigvalsh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep


@lru_cache(None)
def construction():
    ed,volts,*_=prep()
    old=json.loads((ROOT/'data/w33_pass11956_local_electric_metric.json').read_text())
    h=sp.Matrix(old['harmonic_period_basis'])
    B=sp.zeros(160,80)
    for e,(a,b) in enumerate(ed):B[e,a]=-1;B[e,b]=1
    assert B.T*h==sp.zeros(80,3)
    G=h.T*h
    assert h.T*sp.Matrix(volts)==G and G.det()>0
    # Normalize the three first derivatives EXACTLY, with rational currents.
    J=80*h*G.inv()
    assert B.T*J==sp.zeros(80,3)
    assert J.T*sp.Matrix(volts)==80*sp.eye(3)
    sigma=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    alpha=[np.kron(np.array([[0,1],[1,0]]),s) for s in sigma]
    beta=np.diag([1,1,-1,-1])
    return ed,volts,np.asarray(J,float),alpha,beta,G


def operators(k):
    ed,volts,J,alpha,beta,_=construction()
    phase=np.exp(1j*(volts@np.asarray(k)))
    B=np.zeros((160,80),complex);C=np.zeros_like(B)
    for e,(a,b) in enumerate(ed):
        B[e,a]=-1;B[e,b]=phase[e]
        C[e,a]=.5;C[e,b]=.5*phase[e]
    L=B.conj().T@B
    K=[-1j*C.conj().T@(J[:,i,None]*B) for i in range(3)]
    assert max(np.max(abs(x-x.conj().T)) for x in K)<1e-12
    return K,L


def Hamiltonian(k,r=10.,velocity=1.):
    _,_,_,alpha,beta,_=construction()
    K,L=operators(k)
    return velocity*sum(np.kron(a,d) for a,d in zip(alpha,K))+r*np.kron(beta,L)


def payload():
    ed,volts,J,alpha,beta,G=construction()
    u=np.ones(80)/np.sqrt(80)
    K0,L0=operators([0,0,0])
    assert max(np.linalg.norm(K@u) for K in K0)<1e-12
    e0=eigvalsh(Hamiltonian([0,0,0]))
    assert sum(abs(e0)<1e-10)==4
    gap0=float(min(abs(e0[abs(e0)>1e-10])))
    rows=[]
    for direction in ([1,0,0],[1,1,1],[2,-1,3]):
        p=np.asarray(direction,float);p/=np.linalg.norm(p)
        for a in (.02,.01,.005,.0025):
            ev=eigvalsh(Hamiltonian(a*p))
            low=np.sort(ev[np.argsort(abs(ev))[:4]])/a
            error=float(max(abs(low-np.array([-1,-1,1,1]))))
            rows.append(dict(direction=p.tolist(),spacing=a,low_scaled=low.tolist(),error=error))
    # A finite sample is an audit, not the no-doubling proof.
    audits=[]
    for k in ([np.pi,0,0],[np.pi,np.pi,np.pi],[.7,-1.2,2.1]):
        _,L=operators(k);ev=eigvalsh(Hamiltonian(k))
        audits.append(dict(k=list(k),L_min=float(eigvalsh(L)[0]),H_min_abs=float(min(abs(ev)))))
        assert audits[-1]['L_min']>0 and audits[-1]['H_min_abs']>0
    assert all(rows[4*i+3]['error']<rows[4*i]['error']/4 for i in range(3))
    prior=['analysis/w33_pass11956_local_electric_metric.py',
           'data/w33_pass11956_local_electric_metric.json',
           'analysis/w33_pass11562_11569_canonical_spin_gauge_frontier.py',
           'analysis/w33_20261010_toe38_local_maxwell_2complex.py']
    return dict(status='PASS',sites=80,links=160,spinor_bands=320,
        rational_period_Gram=[[str(z) for z in row] for row in G.tolist()],
        exact_current_normalization='J=80 h(h.T h)^-1; B0.T J=0; J.T volts=80 I3',
        operator='H(k)=v sum_i alpha_i tensor [-i C(k).dag diag(J_i) B(k)] + r beta tensor [B(k).dag B(k)]; C has midpoint endpoint weights1/2.',
        locality='Onsite and the same160 native links only, on the infinite80-site Z3 deck cover. J is a fixed coefficient choice computed globally; no nonlocal runtime stencil.',
        no_doubling_proof='L(k) is positive definite off k=0 modulo2pi: its zero would be a covariantly constant scalar, whose three unit deck-loop holonomies force exp(i k_i)=1. Write H=[[rL,S],[S,-rL]], S Hermitian. A zero vector obeys r(psi.dag L psi+chi.dag L chi)=0 by taking real parts of both block equations. Off origin it vanishes; at origin both spinors are constant and S kills them. Thus exactly4 zero modes, all at origin, for every r>0.',
        origin_zero_modes=4,origin_heavy_gap=gap0,
        refinement='For spacing a=1/N, take the periodic native cover with vertices(v,n), n in (Z/N)^3 and edges(a,n)->(b,n+volts_e). H_a=H(a p)/a, continuous time. The four isolated low bands at each fixed physical p approach eigenvalues(-v|p|,-v|p|,v|p|,v|p|); all316 internal bands diverge as1/a. This is a fixed-momentum free spectral limit, not an interacting norm-resolvent theorem.',
        derivation='P H(0) P=0; P dH/dk_i P=v alpha_i since J.T volts/80=I3 and P dL/dk P=0. Analytic finite-matrix perturbation about the isolated four-dimensional kernel gives low effective H=v alpha.p+O(a |p|^2). Compactness away from origin plus the zero-mode proof excludes hidden low species.',
        finite_refinement_checks=rows,off_origin_checks=audits,
        scope='Native free single Dirac species in3+1 dimensions with supplied continuous time, deck marking, Wilson coefficient and current normalization. Vectorlike. No selected spacetime dimension, chiral Standard Model, interacting4D limit, nonlinear gravity or physical speed prediction. Choosing v=sqrt(2) matches the leading11956 photon cone by hand.',
        prior=prior,input_sha256_lf={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in prior},
        primary='https://arxiv.org/abs/2306.14180')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11970_native_wilson_dirac.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['origin_heavy_gap'],[x['error'] for x in d['finite_refinement_checks']])
