#!/usr/bin/env python3
"""Exact Ledger audit-completeness stress test at qubit and qutrit dimension.

Reproduces the published qubit controls, then tests the W33-native q=3 case
over F_65537.  Three qutrits have rank(A2)=649/729 despite noncommuting books;
word depth three closes 729/729 across five independent exact witnesses.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
P=65537; I=256
assert (I*I)%P==P-1

def digits(i,n,q):
    out=[0]*n
    for k in range(n-1,-1,-1): out[k]=i%q; i//=q
    return out
def idx(ds,q):
    z=0
    for a in ds:z=z*q+a
    return z
def witness_state_num(n,q,seed):
    d=q**n; rng=np.random.default_rng(seed)
    A=rng.integers(0,P,size=(d,d),dtype=np.int64); B=rng.integers(0,P,size=(d,d),dtype=np.int64)
    X=(A+I*B)%P; Xc=(A-I*B)%P
    return (X@Xc.T+np.eye(d,dtype=np.int64))%P
def regional_bases(n,q,seed):
    d=q**n; rho=witness_state_num(n,q,seed); bs=[digits(i,n,q) for i in range(d)]
    def partial_trace(R):
        R=tuple(sorted(R)); C=tuple(i for i in range(n) if i not in R); dr=q**len(R)
        out=np.zeros((dr,dr),dtype=np.int64)
        for i,di in enumerate(bs):
            ri=idx([di[r] for r in R],q)
            for j,dj in enumerate(bs):
                if all(di[c]==dj[c] for c in C):
                    rj=idx([dj[r] for r in R],q); out[ri,rj]=(out[ri,rj]+rho[i,j])%P
        return out
    def embed(op,R):
        R=tuple(sorted(R)); C=tuple(i for i in range(n) if i not in R); out=np.zeros((d,d),dtype=np.int64)
        for i,di in enumerate(bs):
            for j,dj in enumerate(bs):
                if all(di[c]==dj[c] for c in C):
                    out[i,j]=op[idx([di[r] for r in R],q),idx([dj[r] for r in R],q)]
        return out
    regions=[frozenset(s) for k in range(1,n) for s in itertools.combinations(range(n),k)]
    bases={}
    for R in regions:
        a=partial_trace(R); cur=np.eye(a.shape[0],dtype=np.int64); local=[]
        for _ in range(a.shape[0]):
            local.append(embed(cur,R)%P); cur=(cur@a)%P
        bases[R]=local
    return regions,bases
class Span:
    def __init__(self,dim): self.dim=dim; self.pivots={}
    def add(self,mat):
        r=mat.reshape(-1).copy()%P
        while True:
            nz=np.flatnonzero(r)
            if len(nz)==0:return False
            c=int(nz[0])
            if c not in self.pivots:
                r=(r*pow(int(r[c]),P-2,P))%P; self.pivots[c]=r; return True
            r=(r-int(r[c])*self.pivots[c])%P
    @property
    def rank(self): return len(self.pivots)
    def matrices(self,d): return [r.reshape(d,d).copy() for r in self.pivots.values()]
def matrix_rank_mod(a):
    a=a.copy()%P; m,n=a.shape; r=0
    for c in range(n):
        nz=np.flatnonzero(a[r:,c])
        if not len(nz):continue
        j=r+int(nz[0]); a[[r,j]]=a[[j,r]]; a[r]=(a[r]*pow(int(a[r,c]),P-2,P))%P
        for i in range(m):
            if i!=r and a[i,c]: a[i]=(a[i]-int(a[i,c])*a[r])%P
        r+=1
        if r==m:break
    return r
def word_ranks(n,q,seed,depth3=False):
    d=q**n; regions,bases=regional_bases(n,q,seed); gens=[x for R in regions for x in bases[R]]
    span=Span(d*d)
    for g in gens:span.add(g)
    r1=span.rank
    for a in gens:
        for b in gens:span.add((b@a)%P)
    r2=span.rank; r3=None; examined=0
    if depth3:
        basis2=span.matrices(d)
        for g in gens:
            for b in basis2:
                examined+=1; span.add((g@b)%P)
                if span.rank==d*d:break
            if span.rank==d*d:break
        r3=span.rank
    best=(0,None,None)
    for A in regions:
        for B in regions:
            C=(bases[A][1]@bases[B][1]-bases[B][1]@bases[A][1])%P; rr=matrix_rank_mod(C)
            if rr>best[0]:best=(rr,A,B)
    return {"n":n,"q":q,"hilbert_dimension":d,"operator_dimension":d*d,"regions":len(regions),
      "generator_count":len(gens),"rank_depth1":r1,"rank_depth2":r2,"rank_depth3":r3,
      "depth3_products_examined_until_closure":examined,"max_commutator_rank":best[0],
      "max_commutator_regions":[sorted(best[1]) if best[1] is not None else None,sorted(best[2]) if best[2] is not None else None]}
def main():
    q2=word_ranks(2,2,20260920); q3=word_ranks(3,2,20260920); t2=word_ranks(2,3,20260920)
    trials=[word_ranks(3,3,20260920+i,True) for i in range(5)]
    r1={x["rank_depth1"] for x in trials}; r2={x["rank_depth2"] for x in trials}; r3={x["rank_depth3"] for x in trials}
    checks={"two_qubit_control_rank_4_of_16":q2["rank_depth2"]==4 and q2["operator_dimension"]==16,
      "three_qubit_control_rank_64_of_64":q3["rank_depth2"]==64 and q3["operator_dimension"]==64,
      "two_qutrit_rank_9_of_81":t2["rank_depth2"]==9 and t2["operator_dimension"]==81,
      "three_qutrit_depth1_rank_31":r1=={31},"three_qutrit_depth2_rank_649":r2=={649},
      "three_qutrit_depth2_deficiency_80":729-next(iter(r2))==80,
      "three_qutrit_noncommuting_books":all(x["max_commutator_rank"]>0 for x in trials),
      "three_qutrit_depth3_full_729":r3=={729},"five_independent_exact_witnesses":len(trials)==5}
    checks={k:bool(v) for k,v in checks.items()}; assert all(checks.values()),checks
    out={"schema":"w33.ledger.audit-completeness-qutrit.v1","status":"CORRECTION_DEPTH2_FAILS_Q3_DEPTH3_CLOSES",
      "field":{"prime":P,"sqrt_minus_one":I,"reason":"exact Gaussian-integer witness arithmetic"},
      "controls":{"n2_q2":q2,"n3_q2":q3,"n2_q3":t2},"qutrit_trials":trials,
      "theorem_boundary":{"published_depth2_equivalence":"noncommuting regional generators => A2=B(H)",
        "q3_counter_witness":"noncommuting regional books coexist with rank(A2)=649<729",
        "minimal_tested_repair":"allow products of three regional book functions; A3 reaches 729/729",
        "w33_resonance_only":"depth-two deficiency 80 equals the 80 point+line vertices of the W33 Tits building; no causal identification is claimed"},
      "checks":checks}
    p=Path("data/PART_LEDGER_QUTRIT_AUDIT_COMPLETENESS.json"); p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); print(json.dumps(out,indent=2,sort_keys=True)); return out
if __name__=="__main__":main()
