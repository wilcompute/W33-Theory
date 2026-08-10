#!/usr/bin/env python3
"""Pass 4778 — minimum line-kernel words are BLT sets; q=5 has two PSp orbits.

Pass4754 proved d=q+1 for odd q.  Equality in that proof is precisely the BLT
condition: q+1 pairwise-skew W(3,q) lines, every external W-line meeting 0 or 2
members.  Here q=3 and q=5 are classified computationally inside PSp.

At q=3 all 270 minima are planar in the Klein/Pluecker model.  At q=5 there
are exactly two PSp orbits, of sizes 6500 (planar) and 13000 (nonplanar).
A final MILP excluding both orbits is infeasible.  The two classes align with
the classical Linear and Fisher (Fi) BLT classes; that naming is prior art, not
a novelty claim.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy import sparse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4778_BLT_MINIMUM_ORBITS.json'

def norm(v,q):
    v=tuple(int(x)%q for x in v)
    for x in v:
        if x:
            z=pow(x,-1,q);return tuple((z*y)%q for y in v)
    raise ValueError('zero')

def geometry(q):
    pts=[]
    for lead in range(4):
        for tail in itertools.product(range(q),repeat=3-lead):pts.append((0,)*lead+(1,)+tail)
    pidx={p:i for i,p in enumerate(pts)}
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%q
    def sy(x,y):return int(np.array(x)@J@np.array(y))%q
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if sy(x,y):continue
            S=set()
            for a,b in itertools.product(range(q),repeat=2):
                if a or b:S.add(pidx[norm(tuple((a*u+b*v)%q for u,v in zip(x,y)),q)])
            if len(S)==q+1:lines.add(frozenset(S))
    lines=sorted(lines,key=lambda S:tuple(sorted(S)));lidx={L:i for i,L in enumerate(lines)}
    A=np.zeros((len(lines),len(lines)),dtype=np.uint8)
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]:A[i,j]=A[j,i]=1
    return pts,pidx,lines,lidx,A,J

def transvection(v,q,J):
    v=np.array(v,dtype=int).reshape(4,1);return (np.eye(4,dtype=int)+v@(J@v).T)%q

def line_perm(M,q,pts,pidx,lines,lidx):
    return tuple(lidx[frozenset(pidx[norm(M@np.array(pts[i]),q)] for i in L)] for L in lines)

def act_support(S,p):return tuple(sorted(p[i] for i in S))
def orbit(S,gens):
    O={tuple(S)};Q=deque([tuple(S)])
    while Q:
        T=Q.popleft()
        for g in gens:
            U=act_support(T,g)
            if U not in O:O.add(U);Q.append(U)
    return O

def kernel_weight6(A,forbid=()):
    n=A.shape[0];rr=[];cc=[];dd=[]
    for i in range(n):
        for j in np.flatnonzero(A[i]):rr.append(i);cc.append(int(j));dd.append(1.)
        rr.append(i);cc.append(n+i);dd.append(-2.)
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(n,2*n)).tocsr()
    cons=[LinearConstraint(M,0,0)]
    wrow=sparse.csr_matrix(([1.]*n,([0]*n,list(range(n)))),shape=(1,2*n));cons.append(LinearConstraint(wrow,6,6))
    if forbid:
        R=[];C=[];D=[]
        for a,S in enumerate(forbid):
            for j in S:R.append(a);C.append(j);D.append(1.)
        X=sparse.coo_matrix((D,(R,C)),shape=(len(forbid),2*n)).tocsr();cons.append(LinearConstraint(X,-np.inf,5))
    lb=np.zeros(2*n);ub=np.ones(2*n);ub[n:]=n
    c=np.zeros(2*n)
    return milp(c,integrality=np.ones(2*n),bounds=Bounds(lb,ub),constraints=cons,options={'presolve':True})

def plucker(L,q,pts):
    a,b=sorted(L)[:2];x=np.array(pts[a]);y=np.array(pts[b]);z=[]
    for i,j in itertools.combinations(range(4),2):z.append(int((x[i]*y[j]-x[j]*y[i])%q))
    return norm(z,q)
def rank_mod(rows,q):
    M=[list(map(lambda x:int(x)%q,r)) for r in rows];r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]),None)
        if p is None:continue
        M[r],M[p]=M[p],M[r];z=pow(M[r][c],-1,q);M[r]=[(z*x)%q for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]:
                z=M[i][c];M[i]=[(a-z*b)%q for a,b in zip(M[i],M[r])]
        r+=1
    return r

def blt_check(S,A,q):
    assert len(S)==q+1
    if any(A[i,j] for i,j in itertools.combinations(S,2)):return False
    return all(sum(int(A[x,j]) for j in S) in (0,2) for x in range(len(A)) if x not in S)

def main()->int:
    out={'pass':4778,'cases':{}}
    # q=3: enumerate all weight-4 kernel words directly.
    pts,pidx,lines,lidx,A,J=geometry(3)
    mins=[]
    for S in itertools.combinations(range(40),4):
        v=np.zeros(40,dtype=np.uint8);v[list(S)]=1
        if not np.any((A@v)&1):mins.append(S)
    assert len(mins)==270 and all(blt_check(S,A,3) for S in mins)
    ranks={rank_mod([plucker(lines[i],3,pts) for i in S],3) for S in mins};assert ranks=={3}
    out['cases']['3']={'minimum_words':270,'PSp_orbits':[270],'plucker_span_ranks':[3],'all_planar':True,'BLT_classes':'Linear only'}

    # q=5: deterministic transvection generating set used only for support orbits.
    pts,pidx,lines,lidx,A,J=geometry(5);idx=[31,6,1,0,56,36,32,11,7,2]
    gens=[line_perm(transvection(pts[i],5,J),5,pts,pidx,lines,lidx) for i in idx]
    R=kernel_weight6(A);assert R.success
    S=tuple(np.flatnonzero(R.x[:156]>.5));Oa=orbit(S,gens);assert len(Oa) in (6500,13000)
    R2=kernel_weight6(A,sorted(Oa));assert R2.success
    T=tuple(np.flatnonzero(R2.x[:156]>.5));Ob=orbit(T,gens);assert len(Ob) in (6500,13000) and len(Ob)!=len(Oa)
    Osmall,Olarge=(Oa,Ob) if len(Oa)==6500 else (Ob,Oa)
    R3=kernel_weight6(A,sorted(Osmall|Olarge));assert R3.status==2  # infeasible
    assert all(blt_check(S,A,5) for S in (next(iter(Osmall)),next(iter(Olarge))))
    rs=rank_mod([plucker(lines[i],5,pts) for i in next(iter(Osmall))],5)
    rl=rank_mod([plucker(lines[i],5,pts) for i in next(iter(Olarge))],5)
    assert (rs,rl)==(3,5)
    psp_order=5**4*(5**4-1)*(5**2-1)//2;assert psp_order==4680000
    out['cases']['5']={'minimum_words':19500,'PSp_orbits':[6500,13000],
      'PSp_stabilizers':[psp_order//6500,psp_order//13000],
      'plucker_span_ranks':[3,5],'planar_orbit':6500,'nonplanar_orbit':13000,
      'MILP_after_excluding_both_orbits':'infeasible','BLT_classes':['Linear','Fisher/Fi']}
    out['identification']='For odd q, equality in the Pass4754 distance bound is exactly the BLT-set condition on q+1 disjoint W(3,q) lines.'
    out['theorem']='At q=3 all 270 minimum words form the planar Linear BLT class. At q=5 the complete minimum shell has two PSp orbits: 6500 planar Linear BLT sets and 13000 nonplanar Fisher BLT sets. Thus all-minima-are-conics already fails at q=5.'
    out['prior_art_boundary']='BLT terminology and the small-q Linear/Fisher classification are classical/known; this pass supplies the explicit code-kernel equivalence and independent PSp/MILP orbit certificate used by the repository.'
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
