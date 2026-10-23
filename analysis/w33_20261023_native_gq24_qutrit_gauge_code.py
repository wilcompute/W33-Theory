#!/usr/bin/env python3
"""Native H27 GQ(2,4) triangle complex as a qutrit CSS/gauge system.

135 physical link qutrits; 27 X-star Gauss generators; 45 Z-face fluxes.
All commutations, ranks and a weight-two nontrivial logical are certified
without materializing the Hilbert space of dimension 3^135.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
try:
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
 from analysis.w33_20261023_native_plaquette_ward import build
except ImportError:
 from w33_pass12189_12193_five_bridges import graph_inputs
 from w33_20261023_native_plaquette_ward import build

def rank_p(rows,p=3):
    piv={}
    for row in rows:
        x=np.asarray(row,dtype=np.int64).copy()%p
        while True:
            nonzero=np.flatnonzero(x)
            if not len(nonzero):break
            j=int(nonzero[0])
            if j in piv:x=(x-int(x[j])*piv[j])%p
            else:
                piv[j]=(x*pow(int(x[j]),-1,p))%p
                break
    return len(piv)

def run():
    d,B,V,G,aa,bb=graph_inputs()
    cert=build()
    faces=cert["closed_cycles"]
    n=135
    Hx=np.rint(B.T).astype(np.int64)%3
    Hz=np.zeros((len(faces),n),dtype=np.int64)
    for i,face in enumerate(faces):
        for e,s in zip(face["edge_ids"],face["orientation_signs"]):
            Hz[i,e]=s%3
    assert np.all((Hx@Hz.T)%3==0)
    rx=rank_p(Hx);rz=rank_p(Hz)
    assert rx==26 and rz==45
    k=n-rx-rz
    assert k==64
    # No weight-1 Pauli X, Z or their products commute with both
    # check sets: every edge belongs to exactly one face and has two endpoints.
    assert np.all((Hz!=0).sum(axis=0)==1)
    assert np.all((Hx!=0).sum(axis=0)==2)
    # Explicit nontrivial X logical of weight two, living inside a single
    # plaquette and therefore invisible to its single face check.
    f=faces[0]; e1,e2=f["edge_ids"][:2]; s1,s2=f["orientation_signs"][:2]
    x=np.zeros(n,dtype=np.int64)
    x[e1]=s2%3; x[e2]=(-s1)%3
    assert int(np.count_nonzero(x))==2
    assert np.all((Hz@x)%3==0)
    assert rank_p(list(Hx)+[x])==rx+1
    # Single electric X link does not commute with its magnetic face Z,
    # but it commutes with every X-star Gauss operator. Every B_face
    # commutes with every X-star by the CSS identity above.
    ecount=int(np.count_nonzero((Hz@x)%3))
    assert ecount==0
    return {"status":"NATIVE_H27_GQ24_QUTRIT_CSS_135_64_2_AND_GAUGE_ALGEBRA",
        "geometry":"27 vertices, 135 edges, 45 zero-voltage triangular faces, native GQ(2,4)",
        "physical_link_qutrits":135,
        "Gauss_X_star_generators":27,"rank_HX":rx,
        "magnetic_Z_face_generators":45,"rank_HZ":rz,
        "HX_HZ_commute_mod3":True,
        "CSS_parameters":"[[135,64,2]]_3",
        "logical_qutrits":k,"distance":2,
        "logical_X_weight2_witness":[{"edge":int(j),"x_exponent_mod3":int(x[j])} for j in np.flatnonzero(x)],
        "single_link_Pauli_syndrome_detected":True,
        "gauge_Hamiltonian":"H=-gE sum_e Re(X_e)-gB sum_f Re(prod_{e in face(f)} Z_e^{sign_{fe}})",
        "Gauss_generators":"G_v=prod_e X_e^{Hx[v,e]}; [G_v,H]=0 exactly for every vertex",
        "Hamiltonian_noncommuting_terms":"Individual electric X_e fails to commute with its unique magnetic Z_face; interactions are genuine quantum, not diagonal commuting stabilizer Hamiltonian.",
        "Hilbert_dimension_symbolic":"3^135",
        "topological_origin":"k=b1=64 of finite GQ(2,4) triangle 2-complex over F3",
        "limitation":"Distance TWO is not robust fault tolerance. Hilbert dynamics, physical link realization, gauge coupling, Gauss-sector state preparation, four-dimensional continuum and Lorentzian propagation are NOT demonstrated."}

if __name__=="__main__":
 out=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(out,encoding="utf8")
 else:print(out)
