#!/usr/bin/env python3
"""Exact odd-qutrit discrete-Wigner and three-qutrit entanglement audit
for the rational chiral cone gate. A mathematical resource witness, not an
experimental universality or distillation claim.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json, math, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as C
OUT=ROOT/"data"/"toe_20261113_chiral_null_wigner_magic.json"
V=C.V
VID=C.VID

def add(a,b):
    return tuple((x+y)%3 for x,y in zip(a,b))

def minus(a,b):
    return tuple((x-y)%3 for x,y in zip(a,b))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))%3

def rational_rank(rows):
    """Exact Gaussian elimination in Q; no floating-point rank threshold."""
    R=[[Fraction(int(x)) for x in row] for row in rows]
    m=len(R); n=len(R[0]); rank=0
    for c in range(n):
        k=next((t for t in range(rank,m) if R[t][c]),None)
        if k is None:
            continue
        R[rank],R[k]=R[k],R[rank]
        pivot=R[rank][c]
        R[rank]=[z/pivot for z in R[rank]]
        for t in range(m):
            if t==rank: continue
            v=R[t][c]
            if v: R[t]=[a-v*b for a,b in zip(R[t],R[rank])]
        rank+=1
        if rank==m: break
    return rank

def verify():
    _,A,D=C.build()
    I=np.eye(27,dtype=np.int64)
    numer=18*I+3*D+D@D
    assert not np.any(numer%2)
    M=numer//2
    assert np.array_equal(M.T@M,81*I)
    # U|0> = M[:,0]/9. In 3-qutrit Wigner convention:
    # W(q,p) = (1/27) sum_x omega^(p.x)
    #            psi(q+x/2) psi*(q-x/2).
    # Over F3, 1/2=2=-1; for real psi, pair x and -x:
    # 2187*W(q,p)=M_q^2+sum_{13 pairs} c_{p.x} M_{q+x}M_{q-x},
    # c_0=2, c_1=c_2=-1.
    representatives=[]
    seen={(0,0,0)}
    for v in V:
        if v in seen: continue
        neg=tuple((-x)%3 for x in v)
        representatives.append(v)
        seen.add(v);seen.add(neg)
    assert len(representatives)==13
    amplitudes=np.asarray(M[:,0],dtype=np.int64)
    W=np.zeros((27,27),dtype=np.int64)
    for qi,q in enumerate(V):
        for pi,p in enumerate(V):
            value=int(amplitudes[qi]**2)
            for v in representatives:
                phase=dot(p,v)
                coefficient=2 if phase==0 else -1
                value+=coefficient*int(amplitudes[VID[add(q,v)]]*
                                        amplitudes[VID[minus(q,v)]])
            W[qi,pi]=value
    histogram=Counter(map(int,W.flatten()))
    assert histogram==Counter({-9:432,18:270,45:27})
    assert int(W.sum())==2187
    assert 27*int((W*W).sum())==2187**2
    total_l1=Fraction(int(np.abs(W).sum()),2187)
    negative_mass=Fraction(-int(W[W<0].sum()),2187)
    assert total_l1==Fraction(41,9)
    assert negative_mass==Fraction(16,9)
    ranks={}
    for j,name in enumerate(("qutrit-1","qutrit-2","qutrit-3")):
        shapes=[]
        for idx in range(27):
            tensor=M[:,idx].reshape((3,3,3))
            mat=np.moveaxis(tensor,j,0).reshape((3,9))
            shapes.append(rational_rank(mat.tolist()))
        assert len(set(shapes))==1
        ranks[name]=shapes[0]
    assert ranks=={"qutrit-1":3,"qutrit-2":2,"qutrit-3":3}
    result={
      "schema":"toe.chiral_null_wigner_magic.v1",
      "status":"PASS_EXACT_3_QUTRIT_NONCLIFFORD_MAGIC_ENTANGLEMENT",
      "input":"computational basis |000>, and all 27 basis inputs via translation covariance",
      "gate":"U=(18I+3D+D^2)/18; U^3=I; U^T U=I",
      "wigner":{"convention":"Gross odd-prime discrete Wigner on F3^3 x F3^3",
        "grid_points":729,"integer_denominator":2187,
        "integer_value_histogram":{"-9":432,"18":270,"45":27},
        "normalized_values":{"-1/243":432,"2/243":270,"5/243":27},
        "normalization":1,"pure_state_identity":"27 sum W^2=1",
        "negative_phase_points":432,
        "total_negative_mass":"16/9",
        "l1_norm":"41/9",
        "mana_exact":"ln(41/9)",
        "mana_numeric":math.log(41/9),
        "gross_hudson_conclusion":"pure output has negative Wigner, hence is not stabilizer; U is not Clifford"},
      "entanglement":{"schmidt_ranks_over_Q_for_each_1_vs_2_cut":ranks,
        "all_27_basis_columns_have_same_cut_ranks":True},
      "scope":"Exact finite-dimensional resource witness. Does not prove gate universality, efficient synthesis, or realizable optical flux."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    a=verify()
    print(json.dumps(a,indent=2))
