#!/usr/bin/env python3
"""4D overlap Dirac index on U(1) flux and reducible SU(2) Cartan background.

The SU2 links diag(u,u^-1) are genuinely SU(2)-valued but mutually
commute: a reducible Abelian Cartan embedding, not a non-Abelian instanton.
Four-dimensional Chern number is Q_01*Q_23. Lattice Wilson-mass branches
can change the overlap index and thus cannot be presumed dynamically chosen.
"""
from __future__ import annotations
from itertools import product
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_overlap_4d_su2_cartan_index.json"

I2=np.eye(2,dtype=complex)
sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1.,-1.])
gamma=[np.kron(sx,sx),np.kron(sx,sy),
       np.kron(sx,sz),np.kron(sy,I2)]
g5=np.kron(sz,I2)
I4=np.eye(4,dtype=complex)
for mu in range(4):
    assert np.max(abs(gamma[mu]@gamma[mu]-I4))<1e-12
    assert np.max(abs(gamma[mu]@g5+g5@gamma[mu]))<1e-12
    for nu in range(mu):
        assert np.max(abs(gamma[mu]@gamma[nu]+gamma[nu]@gamma[mu]))<1e-12

def link_phases(L,Q01,Q23):
    # A uniform integer-flux gauge for two orthogonal coordinate tori.
    q=[Q01,Q23]
    N=L**4
    coords=list(product(range(L),repeat=4))
    indices={p:i for i,p in enumerate(coords)}
    T=[np.zeros((N,N),complex) for _ in range(4)]
    for i,x in enumerate(coords):
        for mu in range(4):
            j=list(x);j[mu]=(j[mu]+1)%L
            block=mu//2;Q=q[block]
            if mu%2==0:
                phase=np.exp(-2j*np.pi*Q*x[mu+1]/L**2)
            else:
                phase=np.exp(2j*np.pi*Q*x[mu-1]/L) if x[mu]==L-1 else 1.+0j
            T[mu][i,indices[tuple(j)]]=phase
    for t in T:
        assert np.max(abs(t.conj().T@t-np.eye(N)))<1e-13
    # Local oriented U01 and U23 plaquette holonomy:
    # for each fixed orthogonal coordinate set, Q flux quanta.
    for block,Q in enumerate(q):
        mu=2*block;nu=mu+1
        plaquette=T[mu]@T[nu]@T[mu].conj().T@T[nu].conj().T
        diag=np.diag(plaquette)
        assert np.max(abs(diag-np.exp(2j*np.pi*Q/L**2)))<2e-12
        assert np.max(abs(plaquette-np.diag(diag)))<2e-12
    return T

def wilson_hermitian(L,Q01,Q23,m):
    T=link_phases(L,Q01,Q23)
    N=L**4
    W=(4-m)*np.eye(4*N,dtype=complex)
    for mu,t in enumerate(T):
        W-=.5*(np.kron(t,I4-gamma[mu])+
                np.kron(t.conj().T,I4+gamma[mu]))
    H=np.kron(np.eye(N),g5)@W
    assert np.max(abs(H-H.conj().T))<3e-13
    return H

def scan(L,q1,q2,m,overlap_check=False):
    H=wilson_hermitian(L,q1,q2,m)
    w=eigvalsh(H,check_finite=False)
    minimum=float(min(abs(w)))
    assert minimum>1e-6,(L,q1,q2,m,minimum)
    asym=int(round(np.sign(w).sum()))
    assert asym%2==0
    index= -asym//2
    r={"L":L,"Q01":q1,"Q23":q2,"ch2_abelian":q1*q2,
       "Wilson_negative_mass_parameter":m,"overlap_index":index,
       "Wilson_H_minimum_abs_eigenvalue":minimum}
    if overlap_check:
        s,V=np.linalg.eigh(H)
        signH=(V*np.sign(s))@V.conj().T
        gamma5=np.kron(np.eye(L**4),g5)
        D=np.eye(len(H))+gamma5@signH
        gw=float(np.max(abs(gamma5@D+D@gamma5-D@gamma5@D)))
        assert gw<4e-12
        r["Ginsparg_Wilson_max_residual"]=gw
        r["exact_nearzero_modes"]=int(sum(abs(np.linalg.eigvals(D))<1e-8))
        assert r["exact_nearzero_modes"]>=abs(index)
    return r

def main():
    configs=[
       (2,1,1,1),(2,1,-1,1),(2,0,1,1),(2,0,0,1),
       (3,1,1,1),(3,1,-1,1),(3,-1,1,1),(3,-1,-1,1),
       (3,0,1,1),(3,0,0,1),
       (3,1,1,3),(3,1,-1,3),(3,1,1,5),(3,1,1,7)]
    rows=[]
    for cfg in configs:
        r=scan(*cfg,overlap_check=(cfg in ((2,1,1,1),(3,1,1,1))))
        rows.append(r)
        print("4D INDEX",cfg,r["overlap_index"],"gap",round(r["Wilson_H_minimum_abs_eigenvalue"],4),flush=True)
    by={(x["L"],x["Q01"],x["Q23"],x["Wilson_negative_mass_parameter"]):x["overlap_index"] for x in rows}
    sign=by[(3,1,1,1)]
    assert abs(sign)==1,sign
    assert by[(3,1,-1,1)]==-sign
    assert by[(3,-1,1,1)]==-sign
    assert by[(3,-1,-1,1)]==sign
    assert by[(3,0,1,1)]==by[(3,0,0,1)]==0
    for mass,coeff in ((3,-3),(5,3),(7,-1)):
        assert by[(3,1,1,mass)]==coeff*sign,(mass,by[(3,1,1,mass)])
    # Coarse 2^4 lattice fails to resolve even unit topological charge:
    # this is a cutoff-dependent index failure, not a physical Q=0.
    assert by[(2,1,1,1)]==0
    assert by[(2,1,-1,1)]==0
    su2_doublet_index=by[(3,1,1,1)]+by[(3,-1,-1,1)]
    assert su2_doublet_index==2*sign
    out={"status":"PASS_4D_OVERLAP_ABSOLUTE_INDEX_AND_REDUCIBLE_SU2_CARTAN",
         "representation":"Euclidean 4D Wilson Dirac with four 4x4 Clifford gamma matrices",
         "lattice_hilbert_spinor_dimension_L3":4*3**4,
         "flux_background":"uniform U(1) Q01 and Q23 on orthogonal two-tori",
         "first_Wilson_branch_index_sign_for_Q01Q23_plusone":sign,
         "coarse_L2_nonzero_flux_index_collapses_to_zero":True,
         "L3_recovers_unit_product_flux_index":True,
         "Wilson_mass_branch_multipliers":{"1":1,"3":-3,"5":3,"7":-1},
         "su2_background":"SU(2) fundamental links diag(u,u^-1), which all lie in the commuting Cartan U(1) subgroup",
         "su2_reducible_fundamental_index":su2_doublet_index,
         "su2_is_truly_noncommuting_gauge_background":False,
         "single_weyl_chiral_anomaly_guard":"A single isolated charged chiral fermion can have gauge anomalies; an overlap Dirac index is not by itself an anomaly-free 4D chiral gauge theory.",
         "scans":rows,
         "boundary":"No noncommuting SU2 instanton; no dynamical flux selection, lattice continuum limit, three families, mass matrices or observed chirality derived. Wilson regulator branch is imposed externally.",
         "prior_art":"4D overlap index, index spectral flow, lattice uniform-field Chern class and reducible SU2 gauge embeddings are established."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 4D overlap topology",sign,"SU2 index",su2_doublet_index,"CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
