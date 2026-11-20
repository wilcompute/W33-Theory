#!/usr/bin/env python3
"""A falsifiable flux-only chiral-family proposal: E6/Spin10 U1psi on T4.

Continuum index is q^2*n12*n34; independent 2D Wilson-overlap indexes
verify factor values. This is NOT a native 4D Wilson-overlap simulation,
a charged G2 index, or physical anomaly inflow.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.linalg import eigvalsh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_flux_chirality_E6_obstruction.json"
SZ=np.diag([1,-1]).astype(complex)
SX=np.array([[0,1],[1,0]],complex)
SY=np.array([[0,-1j],[1j,0]],complex)
GAMMAS=(SX,SY)

def links_2d(L,charge,flux):
    U=np.ones((2,L,L),dtype=complex)
    for x in range(L):
      for y in range(L):
        U[0,x,y]=np.exp(-2j*np.pi*charge*flux*y/(L*L))
        if y==L-1:U[1,x,y]=np.exp(2j*np.pi*charge*flux*x/L)
    plaquettes=[]
    for x in range(L):
      for y in range(L):
        P=U[0,x,y]*U[1,(x+1)%L,y]*np.conj(U[0,x,(y+1)%L])*np.conj(U[1,x,y])
        plaquettes.append(P)
    target=np.exp(2j*np.pi*charge*flux/L**2)
    assert np.max(np.abs(np.array(plaquettes)-target))<1e-12
    return U

def H_wilson(L,U,mass=1.):
    N=L*L
    W=(2-mass)*np.eye(2*N,dtype=complex)
    for x in range(L):
      for y in range(L):
        p=2*(x*L+y)
        for mu,gamma in enumerate(GAMMAS):
          xx,yy=((x+1)%L,y) if mu==0 else (x,(y+1)%L)
          target=2*(xx*L+yy)
          T=-.5*U[mu,x,y]*(np.eye(2)-gamma)
          W[p:p+2,target:target+2]+=T
          W[target:target+2,p:p+2]+=-.5*np.conj(U[mu,x,y])*(np.eye(2)+gamma)
    gamma5=np.kron(np.eye(N),SZ)
    H=gamma5@W
    assert np.max(abs(H-H.conj().T))<1e-12
    return H

def overlap_index_2d(L,charge,flux,random_gauge=False):
    U=links_2d(L,charge,flux)
    if random_gauge:
        rng=np.random.default_rng(711)
        phase=np.exp(1j*rng.uniform(-np.pi,np.pi,size=(L,L)))
        for x in range(L):
          for y in range(L):
            U[0,x,y]*=phase[x,y]*np.conj(phase[(x+1)%L,y])
            U[1,x,y]*=phase[x,y]*np.conj(phase[x,(y+1)%L])
    ev=eigvalsh(H_wilson(L,U),check_finite=False)
    eta=int(sum(np.sign(ev)))
    assert eta%2==0
    return {"L":L,"charge":charge,"flux":flux,
            "index_from_Hermitian_Wilson_spectral_asymmetry":int(-eta//2),
            "spectral_gap":float(min(abs(ev))),
            "plaquette_angle_magnitude":float(abs(2*np.pi*charge*flux/L**2)),
            "gauged":random_gauge}

def e6_flux_anomaly(n12=3,n34=1,L=11):
    Q=n12*n34
    reps=[
      {"Spin10_rep":"16","dimension":16,"U1psi_charge":1,"T2_index":2},
      {"Spin10_rep":"10","dimension":10,"U1psi_charge":-2,"T2_index":1},
      {"Spin10_rep":"1","dimension":1,"U1psi_charge":4,"T2_index":0}
    ]
    results=[]
    for r in reps:
        charge=r["U1psi_charge"]
        ab=overlap_index_2d(L,charge,n12)
        cd=overlap_index_2d(L,charge,n34)
        assert ab["index_from_Hermitian_Wilson_spectral_asymmetry"]==-charge*n12
        assert cd["index_from_Hermitian_Wilson_spectral_asymmetry"]==-charge*n34
        index=ab["index_from_Hermitian_Wilson_spectral_asymmetry"]*cd["index_from_Hermitian_Wilson_spectral_asymmetry"]
        assert index==charge**2*Q
        results.append({**r,"four_dimensional_continuum_flux_index":index,
                       "two_independent_2D_overlap_index_inputs":[ab,cd]})
    unfluxed_anomalies={
        "U1psi_gravitational":sum(r["dimension"]*r["U1psi_charge"] for r in results),
        "U1psi_cubic":sum(r["dimension"]*r["U1psi_charge"]**3 for r in results),
        "Spin10_squared_U1psi":sum(r["T2_index"]*r["U1psi_charge"] for r in results)
    }
    assert list(unfluxed_anomalies.values())==[0,0,0]
    fluxed_anomalies={
        "U1psi_gravitational":sum(r["dimension"]*r["U1psi_charge"]*r["four_dimensional_continuum_flux_index"] for r in results),
        "U1psi_cubic":sum(r["dimension"]*r["U1psi_charge"]**3*r["four_dimensional_continuum_flux_index"] for r in results),
        "Spin10_squared_U1psi":sum(r["T2_index"]*r["U1psi_charge"]*r["four_dimensional_continuum_flux_index"] for r in results)
    }
    assert fluxed_anomalies=={"U1psi_gravitational":0,"U1psi_cubic":720*Q,"Spin10_squared_U1psi":-6*Q}
    # Gauge transform leaves gauge-invariant overlap index.
    ref=overlap_index_2d(L,1,1)
    transformed=overlap_index_2d(L,1,1,random_gauge=True)
    assert ref["index_from_Hermitian_Wilson_spectral_asymmetry"]==transformed["index_from_Hermitian_Wilson_spectral_asymmetry"]
    assert abs(ref["spectral_gap"]-transformed["spectral_gap"])<1e-11
    opposite=overlap_index_2d(L,1,-1)
    assert opposite["index_from_Hermitian_Wilson_spectral_asymmetry"]==1
    return {
      "background":"Flat T4, c1(L)=n12 e12 + n34 e34, charged rep L^q, zero internal gravitational curvature.",
      "index_theorem":"index(D_q)=integral_T4 (1/2)c1(L^q)^2=q^2*n12*n34.",
      "internal_fluxes":{"n12":n12,"n34":n34,"product":Q},
      "E6_27_branching":results,
      "unfluxed_complete_27_anomalies":unfluxed_anomalies,
      "flux_zero_mode_4D_anomaly_tests":fluxed_anomalies,
      "gauge_rephase_invariance_overlap_index":True,
      "sign_reversal_under_2D_flux_reversal":True,
      "scope":"The 4D index q^2 Q is a CONTINUUM Atiyah-Singer result independently checked by PRODUCT of two 2D overlap indices; we did NOT build an actual 4D overlap kernel. Anomaly sums assume the chirally selected modes alone, without extra bulk/inflow/Green-Schwarz/mass partners.",
      "physical_no_go":"A lone U1psi flux selecting 3 Spin10 spinor copies also yields 12 chiral vector-10 and 48 chiral singlet copies; surviving 4D U1psi^3 and Spin10^2 U1psi anomalies are respectively 2160 and -18 for Q=3. Additional physics is mandatory. Selecting n12=3 by hand does not explain the number three."
    }

def main(write=True):
    data={"status":"PASS_CONTINUUM_INDEX_PLUS_2D_OVERLAP_FLUX_E6_SIEVE",
          "prior_art":"Atiyah-Singer index on a torus and lattice Wilson overlap index known; E6 branching known. The new scoped output is an explicit flux-only anomaly filter for the claimed family mechanism.",
          "flux_model":e6_flux_anomaly()}
    if write:OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    return data

if __name__=="__main__":print(json.dumps(main(),indent=2))
