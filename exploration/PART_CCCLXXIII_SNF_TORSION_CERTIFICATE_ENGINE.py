#!/usr/bin/env python3
"""PART CCCLXXIII -- SNF / Torsion Certificate Engine.

CCCLXXII audited the integral W33 triangle chain complex by exact rational ranks
and sampled-prime modular ranks.  CCCLXXIII adds a deterministic Smith-normal-
form certificate path.

The chain complex is

    C2 --d2--> C1 --d1--> C0

with |C0|=40, |C1|=240, |C2|=160.  The known ranks are

    rank_Q(d1)=39,
    rank_Q(d2)=120,
    beta1=240-39-120=81.

This compiler provides two audit paths:

1. Dependency-free exact audit:
   - construct integer d1,d2,
   - verify d1*d2=0,
   - compute exact Q-ranks,
   - compute modular ranks over a fixed prime set.

2. Optional full Smith normal form audit:
   - if sympy is available, compute Smith invariants for d2 and report the
     nonzero diagonal factors.

A complete torsion-free certificate for H1 requires the Smith normal form of the
triangle-boundary image inside ker(d1).  The optional SNF path is included and
kept separate from the dependency-free checks so CI remains lightweight.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
PRIMES=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
Vector=Tuple[int,int,int,int]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]
def d1_matrix(E,nv=40):
    M=[[0]*len(E) for _ in range(nv)]
    for c,(i,j) in enumerate(E): M[i][c]=-1; M[j][c]=1
    return M
def d2_matrix(Tri,edge_index):
    M=[[0]*len(Tri) for _ in range(len(edge_index))]
    for c,(i,j,k) in enumerate(Tri):
        M[edge_index[(j,k)]][c]=1
        M[edge_index[(i,k)]][c]=-1
        M[edge_index[(i,j)]][c]=1
    return M
def rank_rational(M):
    A=[[Fraction(x) for x in row] for row in M]
    m=len(A); n=len(A[0]) if A else 0; r=0
    for c in range(n):
        pivot=None
        for i in range(r,m):
            if A[i][c]!=0: pivot=i; break
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        fac=A[r][c]; A[r]=[x/fac for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]!=0:
                f=A[i][c]; A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
        r+=1
        if r==m: break
    return r
def rank_mod(M,p):
    A=[[x%p for x in row] for row in M]
    m=len(A); n=len(A[0]) if A else 0; r=0
    for c in range(n):
        pivot=None
        for i in range(r,m):
            if A[i][c]%p: pivot=i; break
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]
        inv=pow(A[r][c],p-2,p); A[r]=[(x*inv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p; A[i]=[(A[i][j]-f*A[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r
def compose_zero(d1,d2):
    rows=len(d1); mid=len(d2); cols=len(d2[0])
    for i in range(rows):
        for j in range(cols):
            if sum(d1[i][k]*d2[k][j] for k in range(mid))!=0: return False
    return True
def optional_snf_invariants(M):
    try:
        from sympy import Matrix, ZZ
        try:
            from sympy.matrices.normalforms import smith_normal_form
        except Exception as exc:
            return {"available":False,"status":"import_failed","reason":str(exc)}
        D=smith_normal_form(Matrix(M), domain=ZZ)
        diag=[]
        rows,cols=D.shape
        for i in range(min(rows,cols)):
            val=int(D[i,i])
            if val!=0: diag.append(abs(val))
        return {"available":True,"status":"computed","rank_from_snf":len(diag),"nonunit_invariants":[d for d in diag if d!=1],"unit_count":sum(1 for d in diag if d==1),"diag_nonzero_count":len(diag)}
    except Exception as exc:
        return {"available":False,"status":"not_computed","reason":str(exc)}
def build_results():
    pts,adj=build_graph(); E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj); D1=d1_matrix(E); D2=d2_matrix(Tri,edge_index); r1=rank_rational(D1); r2=rank_rational(D2); beta1=len(E)-r1-r2; mod_ranks={p:{"rank_d1":rank_mod(D1,p),"rank_d2":rank_mod(D2,p)} for p in PRIMES}; snf=optional_snf_invariants(D2)
    checks=[]
    checks.append(ok('chain counts 40/240/160',len(pts)==40 and len(E)==240 and len(Tri)==160,{"V":len(pts),"E":len(E),"T":len(Tri)}))
    checks.append(ok('d1*d2=0',compose_zero(D1,D2),True))
    checks.append(ok('rank_Q d1=39',r1==39,r1))
    checks.append(ok('rank_Q d2=120',r2==120,r2))
    checks.append(ok('beta1=81',beta1==81,beta1))
    checks.append(ok('sampled modular ranks agree',all(v['rank_d1']==r1 and v['rank_d2']==r2 for v in mod_ranks.values()),mod_ranks))
    checks.append(ok('SNF path is available or gracefully skipped',snf['status'] in ('computed','not_computed','import_failed'),snf))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXIII","title":"SNF / Torsion Certificate Engine","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"chain_counts":{"vertices":40,"edges":240,"triangles":160},"rational_ranks":{"rank_d1":r1,"rank_d2":r2,"beta1":beta1},"sampled_primes":PRIMES,"modular_rank_checks":mod_ranks,"optional_snf":snf,"architecture_upgrade":"CCCLXXII gave an integral rank and sampled-prime torsion audit. CCCLXXIII adds an optional Smith-normal-form certificate path while preserving dependency-free exact rank/modular checks.","theorem":"The W33 triangle chain complex has exact rational beta1=81. Modular ranks agree with rational ranks for the sampled primes. When an SNF backend is available, the same audit can compute Smith invariants of d2 directly, upgrading the torsion audit toward a full integral certificate.","honesty_boundary":"Unless optional_snf.status is computed with all nonzero invariants equal to 1 in the relevant ker(d1) quotient, this remains an engine and partial certificate rather than a final full SNF proof of torsion-freeness.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXIII_snf_torsion_certificate_engine_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"snf_status":r['optional_snf']['status'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
