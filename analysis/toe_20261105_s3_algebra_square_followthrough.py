#!/usr/bin/env python3
"""S3 exchange-algebra irreducibility probe and mobile spatial square.

The first calculation uses a generic simple-spectrum Hermitian element
and transition-graph connectivity as a finite-dimensional commutant test.
It is numerically conditioned, not an exact algebraic certificate.
The second uses a gauge-fixed square + diagonal (V=4,E=5) containing
two independent Wilson loops and a mobile color-doublet particle.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from toe_20261105_s3_exchange_mobile_obstruction import (
    matrix_family, PERMS,INDEX,TRANS,mul,inv,irrep)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_s3_full_algebra_spatial_square.json"

def exchange_difference():
    D=np.zeros((144,144))
    for i,g in enumerate(PERMS):
        for j,k in enumerate(PERMS):
            sl=slice(4*(6*i+j),4*(6*i+j)+4)
            for t in TRANS:
                ti=INDEX[mul(t,g)];tj=INDEX[mul(t,k)]
                D[sl,slice(4*(6*ti+j),4*(6*ti+j)+4)]-=np.eye(4)/3
                D[sl,slice(4*(6*i+tj),4*(6*i+tj)+4)]+=np.eye(4)/3
    return D

def connected_components(adj):
    visited=set();sizes=[]
    for seed in range(len(adj)):
        if seed in visited:continue
        stack=[seed];visited.add(seed);n=0
        while stack:
            i=stack.pop();n+=1
            for j in np.flatnonzero(adj[i]):
                if int(j) not in visited:
                    visited.add(int(j));stack.append(int(j))
        sizes.append(n)
    return sorted(sizes,reverse=True)

def simple_spectrum_commutant(ops):
    # Hermitian generic Hamiltonian generated from the tested algebra.
    gen=ops+[1j*(ops[0]@ops[1]-ops[1]@ops[0])]
    coeff=[.739,.293,.187,.433,.137][:len(gen)]
    A=sum(c*X for c,X in zip(coeff,gen))
    A=(A+A.conj().T)/2
    eig,V=np.linalg.eigh(A)
    gap=float(np.min(np.diff(eig)))
    mat=[V.conj().T@X@V for X in ops]
    off=np.maximum.reduce([abs(X)-np.diag(abs(np.diag(X))) for X in mat])
    strengths=off[np.triu_indices(len(eig),1)]
    positive=np.sort(strengths[strengths>1e-11])
    sizes=connected_components(off>1e-9)
    return dict(generic_simple_spectral_gap=gap,
       graph_component_sizes=sizes,
       min_nontrivial_transition_magnitude=float(positive[0]) if len(positive) else 0,
       # If simple spectrum AND connected transition graph, common commutant
       # is exactly scalar in exact arithmetic. Float thresholds give evidence.
       scalar_commutant_numerically_supported=gap>1e-8 and sizes==[len(eig)],
       matrix_dimension=len(eig))

def algebra_probe():
    reps,gauge,P,(E,M,C),F=matrix_family("tensor")
    D=exchange_difference()
    assert max(np.max(abs(D@u-u@D)) for u in gauge)<1e-12
    p=lambda X:F.T@X@F
    sym=[p(E),p(M),p(C)]
    broken=sym+[p(D)]
    a=simple_spectrum_commutant(sym)
    b=simple_spectrum_commutant(broken)
    assert a["matrix_dimension"]==27 and b["matrix_dimension"]==27
    assert len(a["graph_component_sizes"])>=2
    return {"original_symmetric_generators":a,"exchange_broken_generators":b,
      "interpretation":"Commutant test of the specified Hermitian matrices only. Full Mat27 if a simple element and connected transitions can be rigorously certified; numerical thresholds are not a formal proof. Neither case supplies a natural H27/Pauli intertwiner."}

def spatial_square():
    reps=irrep(); n=36*8
    U=[]
    for h in PERMS:
        hh=inv(h);R=reps[INDEX[h]];u=np.zeros((n,n))
        color=np.kron(np.eye(4),R)
        for i,g in enumerate(PERMS):
            ni=INDEX[mul(mul(h,g),hh)]
            for j,k in enumerate(PERMS):
                nj=INDEX[mul(mul(h,k),hh)]
                u[8*(6*ni+nj):8*(6*ni+nj)+8,
                  8*(6*i+j):8*(6*i+j)+8]=color
        assert np.max(abs(u.T@u-np.eye(n)))<1e-12
        U.append(u)
    P=sum(U)/6
    assert np.max(abs(P@P-P))<2e-13
    trace=[round(np.trace(u)) for u in U]
    assert sorted(trace)==[-36,-36,0,0,0,288]
    assert abs(np.trace(P)-36)<1e-12
    E=np.zeros((n,n));M=np.zeros((n,n));T=np.zeros((n,n))
    edges=[(0,1,None),(1,2,None),(2,3,None),(3,0,"g0"),(0,2,"g1")]
    for i,g0 in enumerate(PERMS):
        for j,g1 in enumerate(PERMS):
            sl=slice(8*(6*i+j),8*(6*i+j)+8)
            for t in TRANS:
                ni=INDEX[mul(t,g0)]; nj=INDEX[mul(t,g1)]
                E[sl,slice(8*(6*ni+j),8*(6*ni+j)+8)]-=np.eye(8)/3
                E[sl,slice(8*(6*i+nj),8*(6*i+nj)+8)]-=np.eye(8)/3
            # Two elementary triangular Wilson words: g1 and g1*g0;
            # the character is cyclic so tr(g1*g0)=tr(g0*g1).
            w=mul(g0,g1)  # 0->2->3->0 triangular plaquette word
            chi=(np.trace(reps[j])+np.trace(reps[INDEX[w]]))/4
            M[sl,sl]=-chi*np.eye(8)
            hop=np.zeros((8,8))
            for a,b,name in edges:
                R=np.eye(2) if name is None else reps[i if name=="g0" else j]
                hop[2*a:2*a+2,2*b:2*b+2]-=R/5
                hop[2*b:2*b+2,2*a:2*a+2]-=R.T/5
            T[sl,sl]=hop
    for X in (E,M,T):
        assert np.max(abs(X-X.T))<1e-13
        assert max(np.max(abs(X@u-u@X)) for u in U)<1e-12
    eig,V=np.linalg.eigh(P)
    F=V[:,eig>.5]
    assert F.shape==(288,36)
    ops=[F.T@X@F for X in (E,M,T)]
    assert np.linalg.norm(ops[0]@ops[1]-ops[1]@ops[0])>1e-4
    assert np.linalg.norm(ops[0]@ops[2]-ops[2]@ops[0])>1e-4
    rows=[]
    for J,K,g in ((1,0,0),(.5,1,.3),(.5,.5,1),(.1,1,1)):
        hh=J*ops[0]+K*ops[1]+g*ops[2]
        e,v=np.linalg.eigh(hh)
        psi=F@v[:,0]
        gauss=max(np.linalg.norm((u-np.eye(n))@psi) for u in U)
        assert gauss<1e-11
        rows.append({"J":J,"magnetic_K":K,"transport_g":g,
             "ground_energy":float(e[0]),"gap":float(e[1]-e[0]),
             "gauss_error":float(gauss)})
    return {"graph":"4-site square plus diagonal (5 oriented edges, 3 spanning-tree links, 2 independent loops)",
        "raw_unfixed_dimension":6**5*8,"gauge_fixed_dimension":n,
        "invariant_dimension":36,"gauge_trace_census":sorted(trace),
        "Wilson_triangles":2,"matter_transport_edges":5,
        "electric_magnetic_noncommutation":True,
        "electric_transport_noncommutation":True,
        "scans":rows,
        "boundary":"One particle on a finite 4-vertex spatial graph. No thermodynamic phase transition or continuum SU(3) matter spectrum."}

def main():
    out={"status":"NUMERIC_S3_OPERATOR_COMMUTANT_AND_SPATIAL_SQUARE_GAUSS",
         "operator_algebra":algebra_probe(),
         "mobile_square":spatial_square(),
         "prior_art":"Finite-group gauge-invariant Hilbert spaces, Burnside trace rank, irreducibility/commutant tests and gauge-covariant hopping are established."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("ALGEBRA",out["operator_algebra"])
    print("MOBILE",out["mobile_square"]["invariant_dimension"],out["mobile_square"]["scans"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
