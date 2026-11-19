#!/usr/bin/env python3
"""Independent 4D overlap-Dirac flux/index resolution benchmark.
A smooth-enough externally chosen abelian T4 flux background recovers the
integer index Q12*Q34; coarse lattices need NOT match the continuum value.
This is an established index-theory regulator diagnostic, not emergent 4D,
a derived fermion family or a quantum-gravity calculation.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_fourD_overlap_regulator_flux_threshold.json"
I2=np.eye(2,dtype=complex)
SX=np.array([[0,1],[1,0]],complex)
SY=np.array([[0,-1j],[1j,0]],complex)
SZ=np.diag([1,-1]).astype(complex)
G=[np.kron(SX,SX),np.kron(SX,SY),np.kron(SX,SZ),np.kron(SY,I2)]
G5=np.kron(SZ,I2)
I4=np.eye(4,dtype=complex)


def gamma_relations():
    return float(max(np.linalg.norm(G[i]@G[j]+G[j]@G[i]-
                     (2*I4 if i==j else 0)) for i in range(4) for j in range(4)))


def fourD_links(L,q12,q34):
    coords=list(itertools.product(range(L),repeat=4))
    U=np.ones((L**4,4),complex)
    for n,(x1,x2,x3,x4) in enumerate(coords):
        U[n,0]=np.exp(-2j*np.pi*q12*x2/(L*L))
        if x2==L-1:U[n,1]=np.exp(2j*np.pi*q12*x1/L)
        U[n,2]=np.exp(-2j*np.pi*q34*x4/(L*L))
        if x4==L-1:U[n,3]=np.exp(2j*np.pi*q34*x3/L)
    return coords,U


def fourD_wilson_kernel(L,q12,q34,m0=1.):
    coords,U=fourD_links(L,q12,q34)
    lookup={coord:n for n,coord in enumerate(coords)}
    dim=4*len(coords)
    DW=np.zeros((dim,dim),complex)
    for n,x in enumerate(coords):
        a=4*n
        DW[a:a+4,a:a+4]+=4*I4
        for mu in range(4):
            xp=list(x);xm=list(x)
            xp[mu]=(xp[mu]+1)%L;xm[mu]=(xm[mu]-1)%L
            np_=lookup[tuple(xp)];nm_=lookup[tuple(xm)]
            DW[a:a+4,4*np_:4*np_+4]+=-.5*(I4-G[mu])*U[n,mu]
            DW[a:a+4,4*nm_:4*nm_+4]+=-.5*(I4+G[mu])*np.conj(U[nm_,mu])
    gamma5=np.kron(np.eye(L**4),G5)
    H=gamma5@(DW-m0*np.eye(dim))
    assert np.linalg.norm(H-H.conj().T)<1e-11
    return H,gamma5


def flux_phase_checks(L,q12,q34):
    coords,U=fourD_links(L,q12,q34)
    lookup={c:i for i,c in enumerate(coords)}
    out={}
    for mu,nu,label in [(0,1,"12"),(2,3,"34"),(0,2,"13"),(0,3,"14"),(1,2,"23"),(1,3,"24")]:
        phases=[]
        for n,x in enumerate(coords):
            xp=list(x);yp=list(x)
            xp[mu]=(xp[mu]+1)%L
            yp[nu]=(yp[nu]+1)%L
            nmu=lookup[tuple(xp)];nnu=lookup[tuple(yp)]
            p=U[n,mu]*U[nmu,nu]*np.conj(U[nnu,mu])*np.conj(U[n,nu])
            phases.append(np.angle(p))
        phases=np.asarray(phases)
        target=(q12 if label=="12" else q34 if label=="34" else 0)*2*np.pi/L**2
        assert np.max(abs(phases-target))<1e-11
        out[label]=float(phases.mean())
    return out


def sector(L,q12,q34,full_operator=False):
    H,gamma5=fourD_wilson_kernel(L,q12,q34)
    if full_operator:
        eig,V=eigh(H)
        S=(V*np.sign(eig))@V.conj().T
        D=np.eye(len(H))+gamma5@S
        gw=float(np.linalg.norm(gamma5@D+D@gamma5-D@gamma5@D))
        zero=int(np.sum(np.linalg.svd(D,compute_uv=False)<1e-8))
        assert gw<1e-10
    else:
        eig=np.linalg.eigvalsh(H);gw=None;zero=None
    idx=int(round(-.5*np.sum(np.sign(eig))))
    return {"L":L,"Q12":q12,"Q34":q34,
            "continuum_Chern_character_Q12_times_Q34":q12*q34,
            "finite_overlap_index":idx,
            "finite_index_matches_continuum":idx==q12*q34,
            "kernel_gap":float(np.min(np.abs(eig))),
            "Ginsparg_Wilson_residual_when_full_operator":gw,
            "overlap_zero_mode_count_when_full_operator":zero,
            "mean_plaquette_flux_angles":flux_phase_checks(L,q12,q34)}


def run_all():
    assert gamma_relations()<1e-12
    cases=[
        sector(2,1,1),
        sector(3,0,0),
        sector(3,1,0),
        sector(3,1,1,True),
        sector(3,1,-1),
        sector(3,-1,-1),
        sector(3,1,2),
    ]
    by={(r["L"],r["Q12"],r["Q34"]):r for r in cases}
    assert by[(2,1,1)]["finite_overlap_index"]==0
    assert by[(3,1,1)]["finite_overlap_index"]==1
    assert by[(3,1,-1)]["finite_overlap_index"]==-1
    assert by[(3,1,0)]["finite_overlap_index"]==0
    assert by[(3,-1,-1)]["finite_overlap_index"]==1
    assert by[(3,1,2)]["finite_overlap_index"]!=2
    return {
      "status":"PASS — conditional known topology and regulator-resolution sensitivity",
      "TOE_solved":False,"dynamical_4D_spacetime_derived":False,
      "physical_SM_chiral_gauge_theory_constructed":False,
      "known_continuum_relation":"For U1 field strengths on flat T4 with flux only in 12 and 34 planes, (1/8pi²) integral F wedge F = Q12*Q34; with our gamma orientation overlap index agrees at sufficiently resolved tests.",
      "field_and_fourD_torus_inserted_as_inputs":True,
      "gamma_Clifford_residual":gamma_relations(),
      "cases":cases,
      "observed_coarse_regulator_breakdown":"With Wilson mass m0=1 the L=2 background (Q12,Q34)=(1,1) has continuum charge 1 but overlap index 0 despite nonzero kernel gap; the finer L=3 background gives index 1. L=3 Q34=2 also fails to give 2. Finite resolution and kernel mass/admissibility matter; no universal finite-L index theorem is claimed.",
      "sources":[
        "https://doi.org/10.1007/s11005-026-02080-w",
        "https://arxiv.org/abs/hep-lat/0111060",
        "https://doi.org/10.1016/S0550-3213(99)00115-7"
      ]}


def main():
    r=run_all()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2),encoding="utf8")
    print(json.dumps({"status":"PASS","cases":[(x["L"],x["Q12"],x["Q34"],x["finite_overlap_index"],x["continuum_Chern_character_Q12_times_Q34"]) for x in r["cases"]],
       "full_GW_residual":r["cases"][3]["Ginsparg_Wilson_residual_when_full_operator"],
       "output":str(OUT)}))

if __name__=="__main__":main()
