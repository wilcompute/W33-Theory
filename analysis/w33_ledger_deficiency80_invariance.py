#!/usr/bin/env python3
"""Exact test of whether the qutrit 80-dimensional A2 deficiency is a W33 module."""
from __future__ import annotations
import json,time
from pathlib import Path
import numpy as np
import w33_ledger_qutrit_audit_completeness as Q
OUT=Path("data/PART_LEDGER_DEFICIENCY80_INVARIANCE.json")
P=Q.P
def reduce_with(pivots,mat):
    r=mat.reshape(-1).copy()%P
    while True:
        nz=np.flatnonzero(r)
        if not len(nz):return r
        c=int(nz[0])
        if c not in pivots:return r
        r=(r-int(r[c])*pivots[c])%P
def add(pivots,mat):
    r=reduce_with(pivots,mat);nz=np.flatnonzero(r)
    if not len(nz):return False
    c=int(nz[0]);r=(r*pow(int(r[c]),P-2,P))%P;pivots[c]=r;return True
def digits(i,n=3,q=3):
    a=[0]*n
    for k in range(n-1,-1,-1):a[k]=i%q;i//=q
    return a
def idx(a,q=3):
    z=0
    for x in a:z=z*q+x
    return z
def sum_perm():
    p=np.empty(27,dtype=int)
    for i in range(27):
        a=digits(i);b=a.copy();b[1]=(b[1]+b[0])%3;p[i]=idx(b)
    return p
def conj(M,p):
    out=np.empty_like(M);out[np.ix_(p,p)]=M;return out
def main():
    t0=time.time();regions,bases=Q.regional_bases(3,3,20260920);gens=[x for R in regions for x in bases[R]]
    S=Q.Span(729)
    for a in gens:
        for b in gens:S.add((b@a)%P)
    basis=S.matrices(27);original={k:v.copy() for k,v in S.pivots.items()};hull={k:v.copy() for k,v in original.items()}
    p=sum_perm();outside=0
    for B in basis:
        T=conj(B,p)
        if len(np.flatnonzero(reduce_with(original,T))):outside+=1
        add(hull,T)
    checks={"A2_rank_649":S.rank==649,"deficiency_80":729-S.rank==80,"building_vertices_80":2*40==80,
            "not_invariant":outside==564,"one_clifford_image_closes_full":len(hull)==729}
    assert all(checks.values()),checks
    out={"schema":"w33.ledger.audit-deficiency80-invariance.v1","status":"DEFICIENCY80_IS_NOT_W33_BUILDING_MODULE",
         "audit":{"A2_rank":S.rank,"deficiency":729-S.rank,"operator_dimension":729},
         "symmetry_test":{"element":"local qutrit SUM |a,b,c> -> |a,a+b,c>","basis_vectors_outside_A2":outside,
                          "rank_A2_plus_conjugate_A2":len(hull)},
         "verdict":{"prerequisite_failure":"A2 is not invariant under one exact Clifford/Sp(4,3) element, so the missing 80 directions are not a canonical PSp(4,3) module.",
                    "intertwiner":"No PSp-equivariant identification with the 40-point+40-line building permutation module exists for this generic audit witness.",
                    "resonance":"729-649=80=40+40 is numerical only; A2 plus one Clifford-conjugate copy already spans all 729 directions."},
         "runtime_seconds":time.time()-t0,"checks":checks}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
