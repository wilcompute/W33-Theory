#!/usr/bin/env python3
"""Actual 4D Wilson-overlap spectral-asymmetry test with two U1 flux planes.

A coarse gapped lattice can yield a DIFFERENT integer than continuum q^2 n12 n34.
This is a lattice admissibility/resolution check, not a new index theorem or
a compact singular G2 matter spectrum.
"""
from pathlib import Path
from itertools import product
import json
import numpy as np
from scipy.linalg import eigvalsh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_fourD_overlap_resolution_gate.json"
SX=np.array([[0,1],[1,0]],complex)
SY=np.array([[0,-1j],[1j,0]],complex)
SZ=np.diag([1.,-1.])
I2=np.eye(2)
I4=np.eye(4)
GAMMAS=[np.kron(SX,SX),np.kron(SX,SY),np.kron(SX,SZ),np.kron(SY,I2)]
G5=np.kron(SZ,I2)
assert all(np.max(abs(a@b+b@a-(2*I4 if i==j else 0)))<1e-12
           for i,a in enumerate(GAMMAS) for j,b in enumerate(GAMMAS))
assert all(np.max(abs(a@G5+G5@a))<1e-12 for a in GAMMAS)

def links4(x,mu,L,n12,n34,charge):
    if mu==0:return np.exp(-2j*np.pi*charge*n12*x[1]/L**2)
    if mu==1:return np.exp(2j*np.pi*charge*n12*x[0]/L) if x[1]==L-1 else 1.+0j
    if mu==2:return np.exp(-2j*np.pi*charge*n34*x[3]/L**2)
    return np.exp(2j*np.pi*charge*n34*x[2]/L) if x[3]==L-1 else 1.+0j

def wilson_kernel(L,n12,n34,charge=1,mass=1.,gauge=None):
    coords=list(product(range(L),repeat=4))
    idx={x:i for i,x in enumerate(coords)}
    A=(4-mass)*np.eye(4*L**4,dtype=complex)
    for x in coords:
      p=4*idx[x]
      for mu,gamma in enumerate(GAMMAS):
        y=list(x);y[mu]=(y[mu]+1)%L;y=tuple(y)
        tgt=4*idx[y]
        U=links4(x,mu,L,n12,n34,charge)
        if gauge is not None:U*=gauge[idx[x]]*np.conj(gauge[idx[y]])
        A[p:p+4,tgt:tgt+4]+=-.5*(I4-gamma)*U
        A[tgt:tgt+4,p:p+4]+=-.5*(I4+gamma)*np.conj(U)
    Gamma5=np.kron(np.eye(L**4),G5)
    H=Gamma5@A
    assert np.max(abs(H-H.conj().T))<1e-11
    return H

def index4(L,n12,n34,charge=1,gauge=None):
    ev=eigvalsh(wilson_kernel(L,n12,n34,charge,gauge=gauge),check_finite=False)
    index=int(round(-.5*np.sum(np.sign(ev))))
    return {
      "L":L,"sites":L**4,"spinor_dimension":4*L**4,
      "n12":n12,"n34":n34,"U1_charge":charge,
      "continuum_index_prediction":charge**2*n12*n34,
      "lattice_overlap_index":index,
      "minimum_Wilson_gap":float(np.min(abs(ev))),
      "max_plaquette_phase_abs":float(2*np.pi*abs(charge)*max(abs(n12),abs(n34))/L**2),
      "agrees_with_continuum":index==charge**2*n12*n34
    }

def main(write=True):
    samples=[
       index4(3,0,0),
       index4(3,1,0),
       index4(3,1,1),
       index4(3,2,1),
       index4(3,1,1,charge=2),
       index4(4,1,1),
       index4(4,2,1),
       index4(4,2,2),
       index4(4,1,1,charge=2),
       index4(4,3,1),
       index4(4,3,1,charge=2)
    ]
    actual=[r["lattice_overlap_index"] for r in samples]
    assert actual==[0,0,1,1,0,1,2,4,4,3,0],actual
    assert all(s["minimum_Wilson_gap"]>.02 for s in samples)
    assert samples[3]["agrees_with_continuum"] is False
    assert samples[6]["agrees_with_continuum"] is True
    # Cross-check exact local lattice U(1) gauge covariance at L=3.
    rng=np.random.default_rng(11)
    phase=np.exp(1j*rng.uniform(-np.pi,np.pi,size=3**4))
    Hg=wilson_kernel(3,1,1,gauge=phase)
    H0=wilson_kernel(3,1,1)
    U=np.kron(np.diag(phase),I4)
    covariance=float(np.max(abs(Hg-U@H0@U.conj().T)))
    assert covariance<2e-12
    result={
      "status":"PASS_ACTUAL_4D_WILSON_OVERLAP_FLUX_RESOLUTION_GATE",
      "sources":"Continuum index q^2 n12 n34 on flat torus and overlap spectral asymmetry are established. This executable builds the full 4D 4L^4-by-4L^4 Hermitian Wilson kernel.",
      "samples":samples,
      "random_gauge_covariance_residual_L3":covariance,
      "caution":"A nonzero Wilson gap at a coarse lattice does not alone ensure agreement with the continuum integer. High charge times flux can violate the lattice smooth-field/admissibility domain; no 4D scan to L>=5 is claimed.",
      "E6_relevance":"The q=1 n12=3 n34=1 lattice index is 3 at L=4, but q=2 with same background fails at L=4. It is invalid to use an underresolved finite lattice to assert charge-weighted 3/12/48 families. Continuum theorem remains separate."
    }
    if write:OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":print(json.dumps(main(),indent=2))
