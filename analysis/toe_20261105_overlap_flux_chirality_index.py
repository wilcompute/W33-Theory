#!/usr/bin/env python3
"""Two-dimensional overlap-Dirac topological index, flux and mass-branch guard.

Computes the exact finite-matrix sign of Hermitian Wilson-Dirac, checks
Ginsparg-Wilson, explicit plaquette winding, and topological index
opposition under flux reversal. Demonstrates why an external flux and
regulator-mass branch are extra physical inputs, not TOE chirality selected.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_overlap_dirac_2d_chirality_index.json"
sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1.,-1.])
I2=np.eye(2,dtype=complex)
def links(L,Q):
    ux=np.empty((L,L),complex)
    uy=np.ones((L,L),complex)
    for x in range(L):
        for y in range(L):
            ux[x,y]=np.exp(-2j*np.pi*Q*y/L**2)
            if y==L-1:uy[x,y]=np.exp(2j*np.pi*Q*x/L)
    phases=[]
    for x in range(L):
        for y in range(L):
            product=ux[x,y]*uy[(x+1)%L,y]*np.conj(ux[x,(y+1)%L])*np.conj(uy[x,y])
            phases.append(float(np.angle(product)))
    plaquette_Q=round(sum(phases)/(2*math.pi))
    assert abs(sum(phases)-2*math.pi*Q)<1e-10
    assert plaquette_Q==Q
    return (ux,uy),max(abs(p) for p in phases)

def wilson_hermitian(L,Q,mass):
    uu,maxplaq=links(L,Q)
    N=L*L
    T=[]
    for mu in (0,1):
        mat=np.zeros((N,N),complex)
        for x in range(L):
            for y in range(L):
                xx,yy=((x+1)%L,y) if mu==0 else (x,(y+1)%L)
                mat[x*L+y,xx*L+yy]=uu[mu][x,y]
        T.append(mat)
    DW=(2-mass)*np.eye(2*N,dtype=complex)
    for gamma,A in zip((sx,sy),T):
        DW-=.5*(np.kron(A,I2-gamma)+
                np.kron(A.conj().T,I2+gamma))
    gamma5=np.kron(np.eye(N),sz)
    H=gamma5@DW
    assert np.max(abs(H-H.conj().T))<2e-13
    return H,gamma5,maxplaq
def check(L,Q,m,compute_overlap=False):
    H,gamma,maxplaq=wilson_hermitian(L,Q,m)
    e,v=np.linalg.eigh(H)
    gap=float(min(abs(e)))
    assert gap>0.1,(L,Q,m,gap)
    asym=int(round(np.sign(e).sum()))
    assert asym%2==0
    index=-asym//2
    assert index==(-Q if m<2 else Q),(L,Q,m,index)
    record={"L":L,"topological_flux_Q":Q,"Wilson_regulator_mass":m,
            "index_minus_half_eta":index,
            "minimum_abs_Wilson_eigenvalue":gap,
            "maximum_plaquette_phase":maxplaq}
    if compute_overlap:
        signH=(v*np.sign(e))@v.conj().T
        D=np.eye(2*L*L)+gamma@signH
        GW=gamma@D+D@gamma-D@gamma@D
        error=float(np.max(abs(GW)))
        assert error<1e-12,(L,Q,m,error)
        record["Ginsparg_Wilson_error"]=error
        record["overlap_zero_mode_count"]=int(sum(abs(np.linalg.eigvals(D))<1e-8))
        assert record["overlap_zero_mode_count"]>=abs(index)
    return record
def main():
    rows=[]
    for L in (4,6,8):
        for Q in (-2,-1,0,1,2):
            for m in (1.,2.5):
                rows.append(check(L,Q,m,compute_overlap=(L==6 and abs(Q)<=1)))
    assert len(rows)==30
    out={"status":"PASS_OVERLAP_DIRAC_FLUX_INDEX_GINSparg_WILSON_REGULATOR_BRANCH",
         "spacetime_dimensions":2,
         "chirality_index_sign_convention":"Index = -flux Q for Wilson mass 1; regulator branch mass 2.5 flips the sign",
         "uniform_plaquette_flux_verified":True,
         "fermi_index_relation":"index D_ov = -1/2 Tr(sign[gamma5 D_W(-m)])",
         "Ginsparg_Wilson_relation":"gamma5 D + D gamma5 = D gamma5 D for D=1+gamma5 signH, lattice units",
         "records":rows,
         "limitation":"This is a standard 2D overlap index in externally imposed flux; neither sign of Q nor Wilson mass branch is selected by W33 geometry. No 3+1D single chiral SM family, anomaly cancellation or flavour dynamics derived.",
         "prior_art":"Neuberger overlap fermions, Kurokawa-Fujiwara uniform-field Wilson-Dirac, and lattice index theorem are established."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS overlap index 30 scans, GW checks; certificate",OUT)
    return out
if __name__=="__main__":main()
