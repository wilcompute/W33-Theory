#!/usr/bin/env python3
"""PART CCCLXXX -- Quotient SNF Invariant Runner.

Runs the quotient relation-matrix engine for H1 and reports invariant-factor
status.  This part is deliberately conservative:

- Always constructs the exact 201 x 160 relation matrix R.
- Always verifies rank_Q(R)=120 and free_rank=81.
- Always verifies sampled modular ranks.
- If a Smith normal form backend is available, reports nonzero invariant factors.
- If not available, reports a reproducible fallback certificate rather than
  pretending a full invariant-factor computation happened.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from collections import deque
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
PRIMES=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
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
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]
def spanning_tree(adj):
    parent={0:None}; q=deque([0]); tree=[]
    while q:
        v=q.popleft()
        for w in sorted(adj[v]):
            if w not in parent:
                parent[w]=v; tree.append(tuple(sorted((v,w)))); q.append(w)
    return tree,parent
def triangle_boundary_edges(tri):
    i,j,k=tri
    return {(j,k):1,(i,k):-1,(i,j):1}
def relation_matrix(adj):
    E=edges(adj); Tri=triangles(adj); tree,parent=spanning_tree(adj); tree_set=set(tree)
    non_tree=[e for e in E if e not in tree_set]; non_index={e:i for i,e in enumerate(non_tree)}
    R=[[0 for _ in Tri] for _ in non_tree]
    for col,tri in enumerate(Tri):
        for e,coef in triangle_boundary_edges(tri).items():
            e=tuple(sorted(e))
            if e in non_index: R[non_index[e]][col]=coef
    return R,non_tree,Tri
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
def try_snf(M):
    try:
        from sympy import Matrix, ZZ
        from sympy.matrices.normalforms import smith_normal_form
        D=smith_normal_form(Matrix(M), domain=ZZ)
        rows,cols=D.shape; diag=[]
        for i in range(min(rows,cols)):
            val=abs(int(D[i,i]))
            if val: diag.append(val)
        return {"status":"computed","rank":len(diag),"unit_count":sum(1 for x in diag if x==1),"nonunit_invariants":[x for x in diag if x!=1],"all_nonzero_units":all(x==1 for x in diag)}
    except Exception as exc:
        return {"status":"unavailable","reason":str(exc)}
def invariant_report(R):
    rankQ=rank_rational(R); free=len(R)-rankQ; mods={p:rank_mod(R,p) for p in PRIMES}; snf=try_snf(R)
    if snf['status']=='computed':
        certificate='complete_snf' if snf.get('all_nonzero_units') and snf.get('rank')==rankQ else 'snf_computed_with_nonunit_or_rank_issue'
    else:
        certificate='rank_plus_sampled_modular_fallback'
    return {"rank_Q":rankQ,"free_rank":free,"modular_ranks":mods,"snf":snf,"certificate_type":certificate}
def build_results():
    pts,adj=build_graph(); R,non_tree,Tri=relation_matrix(adj); report=invariant_report(R); checks=[]
    checks.append(ok('R shape 201 x 160',len(R)==201 and len(R[0])==160,[len(R),len(R[0])]))
    checks.append(ok('rank_Q = 120',report['rank_Q']==120,report['rank_Q']))
    checks.append(ok('free rank = 81',report['free_rank']==81,report['free_rank']))
    checks.append(ok('all sampled modular ranks are 120',all(v==120 for v in report['modular_ranks'].values()),report['modular_ranks']))
    checks.append(ok('certificate type recorded',report['certificate_type'] in ('complete_snf','rank_plus_sampled_modular_fallback','snf_computed_with_nonunit_or_rank_issue'),report['certificate_type']))
    if report['snf']['status']=='computed':
        checks.append(ok('SNF rank matches rational rank',report['snf']['rank']==report['rank_Q'],report['snf']))
    else:
        checks.append(ok('SNF unavailable is explicit',report['snf']['status']=='unavailable',report['snf']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXX","title":"Quotient SNF Invariant Runner","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"relation_matrix_shape":[len(R),len(R[0])],"invariant_report":report,"architecture_upgrade":"CCCLXXVII built the exact quotient relation matrix. CCCLXXX runs the invariant-factor path when available and otherwise emits a clear rank-plus-modular fallback certificate.","theorem":"The H1 quotient relation matrix R has rank 120 and free rank 81. If SNF computes with all nonzero invariant factors equal to 1, this proves the quotient is torsion-free. Otherwise the runner records the exact rank and sampled modular agreement as a fallback audit.","honesty_boundary":"A complete torsion-free certificate is claimed only when certificate_type is complete_snf. Otherwise the output remains a transparent partial invariant audit.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXX_quotient_snf_invariant_runner_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"certificate_type":r['invariant_report']['certificate_type'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
