#!/usr/bin/env python3
"""PART CCCLXXVII -- Quotient SNF H1 Engine.

Computes the quotient presentation for H1 of the W33 triangle complex.

For a connected graph, choose a spanning tree.  The 201 non-tree edges give an
integral fundamental-cycle basis for ker(d1).  Every triangle boundary is a
cycle, so it has coordinates in this Z^201 basis.  Let

    R : Z^160 -> Z^201

be the matrix of triangle-boundary coordinates in this fundamental-cycle basis.
Then

    H1 = Z^201 / im(R).

The free rank is 201-rank(R)=81.  A full torsion certificate is the Smith normal
form of R.  This compiler constructs R exactly and computes:

- exact rational rank of R,
- sampled modular ranks,
- optional Smith-normal-form invariants if SymPy normal forms are available.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from collections import deque
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
PRIMES=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
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
    # edge orientation is low->high. Boundary [j,k]-[i,k]+[i,j].
    return {(j,k):1,(i,k):-1,(i,j):1}
def quotient_matrix_R(adj):
    E=edges(adj); Tri=triangles(adj); tree,parent=spanning_tree(adj); tree_set=set(tree)
    non_tree=[e for e in E if e not in tree_set]
    non_index={e:i for i,e in enumerate(non_tree)}
    # R is 201 x 160. Coordinate of a cycle in fundamental-cycle basis is its coefficient on non-tree edges.
    R=[[0 for _ in Tri] for _ in non_tree]
    for c,tri in enumerate(Tri):
        bd=triangle_boundary_edges(tri)
        for e,coef in bd.items():
            e=tuple(sorted(e))
            if e in non_index:
                R[non_index[e]][c]=coef
    return R,non_tree,Tri,tree
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
def optional_snf(M):
    try:
        from sympy import Matrix, ZZ
        from sympy.matrices.normalforms import smith_normal_form
        D=smith_normal_form(Matrix(M), domain=ZZ)
        rows,cols=D.shape; diag=[]
        for i in range(min(rows,cols)):
            val=abs(int(D[i,i]))
            if val: diag.append(val)
        return {"available":True,"status":"computed","rank_from_snf":len(diag),"unit_count":sum(1 for d in diag if d==1),"nonunit_invariants":[d for d in diag if d!=1],"torsion_free_if_no_nonunits":len([d for d in diag if d!=1])==0}
    except Exception as exc:
        return {"available":False,"status":"not_computed","reason":str(exc)}
def build_results():
    pts,adj=build_graph(); R,non_tree,Tri,tree=quotient_matrix_R(adj); rankQ=rank_rational(R); free_rank=len(non_tree)-rankQ; mod_ranks={p:rank_mod(R,p) for p in PRIMES}; snf=optional_snf(R); checks=[]
    checks.append(ok('non-tree cycle basis size = 201',len(non_tree)==201,len(non_tree)))
    checks.append(ok('triangle count = 160',len(Tri)==160,len(Tri)))
    checks.append(ok('R shape = 201 x 160',len(R)==201 and len(R[0])==160,[len(R),len(R[0])]))
    checks.append(ok('rank_Q R = 120',rankQ==120,rankQ))
    checks.append(ok('free rank = 81',free_rank==81,free_rank))
    checks.append(ok('sampled modular ranks agree',all(v==rankQ for v in mod_ranks.values()),mod_ranks))
    checks.append(ok('SNF status recorded',snf['status'] in ('computed','not_computed'),snf))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXVII","title":"Quotient SNF H1 Engine","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"presentation":"H1 = Z^201 / im(R), where R is the 201 x 160 triangle-boundary matrix in fundamental-cycle coordinates","R_shape":[len(R),len(R[0])],"rank_Q_R":rankQ,"free_rank":free_rank,"sampled_primes":PRIMES,"modular_ranks":mod_ranks,"optional_snf":snf,"architecture_upgrade":"CCCLXXIII added a general SNF audit path. CCCLXXVII constructs the actual quotient presentation H1=Z^201/im(R), making the torsion problem a Smith-normal-form problem for the 201 x 160 relation matrix R.","theorem":"Choosing a spanning tree identifies ker(d1) with Z^201 via fundamental cycles. Triangle boundaries define a relation matrix R:Z^160->Z^201. The quotient H1 is Z^201/im(R), with rank_Q(R)=120 and free rank 81. If the Smith invariants of R are all unit on the nonzero diagonal, this presentation proves H1 is torsion-free of rank 81.","honesty_boundary":"The quotient presentation is exact. Full torsion-freeness depends on computing or certifying the Smith invariants of R; if optional_snf is unavailable, only rank and sampled-prime checks are reported.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXVII_quotient_snf_h1_engine_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"snf_status":r['optional_snf']['status'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
