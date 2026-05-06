#!/usr/bin/env python3
"""PART CCCLXXII -- Integral Homology / Torsion Audit.

Audits the integral H1 claim for the W33 triangle complex.

For the chain complex C2 -> C1 -> C0 with 160 triangles, 240 edges, 40 vertices,
we compute exact rational ranks of integer boundary matrices:

    rank(d1) = 39,
    rank(d2) = 120,
    beta1 = 240 - rank(d1) - rank(d2) = 81.

To test for torsion in H1 = ker(d1) / im(d2), we use a standard criterion:
if rank(d2 over Q) equals rank(d2 modulo p) for several primes and the gcd of
maximal minors is consistent with 1, then torsion is ruled out for those primes.
A complete Smith normal form is expensive without dependencies, so this audit
performs deterministic modular-rank checks across many primes and reports a
conditional torsion-free certificate.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]
PRIMES=[2,3,5,7,11,13,17,19,23,29,31,37]
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
def d1_matrix(E,nv=40):
    # oriented edge i<j: boundary = j - i
    M=[[0]*len(E) for _ in range(nv)]
    for col,(i,j) in enumerate(E): M[i][col]=-1; M[j][col]=1
    return M
def d2_matrix(Tri,edge_index):
    # oriented triangle i<j<k: boundary (j,k) - (i,k) + (i,j)
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
    rows=len(d1); cols=len(d2[0]); mid=len(d2)
    for i in range(rows):
        for j in range(cols):
            if sum(d1[i][k]*d2[k][j] for k in range(mid))!=0: return False
    return True
def build_results():
    pts,adj=build_graph(); E=edges(adj); edge_index={e:i for i,e in enumerate(E)}; Tri=triangles(adj); D1=d1_matrix(E); D2=d2_matrix(Tri,edge_index); r1=rank_rational(D1); r2=rank_rational(D2); beta1=len(E)-r1-r2; mod_ranks={p:{"rank_d1":rank_mod(D1,p),"rank_d2":rank_mod(D2,p)} for p in PRIMES}; checks=[]
    checks.append(ok('chain counts',len(pts)==40 and len(E)==240 and len(Tri)==160,{"V":len(pts),"E":len(E),"T":len(Tri)}))
    checks.append(ok('boundary composition d1*d2=0',compose_zero(D1,D2),True))
    checks.append(ok('rank_Q d1=39',r1==39,r1))
    checks.append(ok('rank_Q d2=120',r2==120,r2))
    checks.append(ok('beta1=81',beta1==81,beta1))
    checks.append(ok('modular ranks match rational ranks for sampled primes',all(v['rank_d1']==r1 and v['rank_d2']==r2 for v in mod_ranks.values()),mod_ranks))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXII","title":"Integral Homology / Torsion Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"chain_counts":{"vertices":40,"edges":240,"triangles":160},"rational_ranks":{"rank_d1":r1,"rank_d2":r2,"beta1":beta1},"modular_rank_checks":mod_ranks,"torsion_audit":"No torsion detected at sampled primes because ranks over F_p match Q-ranks for all sampled primes. Full Smith normal form remains the definitive certificate.","architecture_upgrade":"CCCLXXI produced a GF2 81-cycle basis. CCCLXXII lifts the audit to integer boundary matrices, verifies rank_Q(d1)=39, rank_Q(d2)=120, beta1=81, and checks sampled-prime torsion obstructions by modular rank agreement.","theorem":"The W33 triangle chain complex over Q has beta1=81. The integer boundary matrices satisfy d1*d2=0, rank_Q(d1)=39, and rank_Q(d2)=120. Modular ranks agree with these rational ranks for sampled primes, giving a strong torsion audit consistent with H1 being free of rank 81, pending full Smith normal form for a complete integral certificate.","honesty_boundary":"This is not a full Smith normal form proof. It certifies the free rank exactly over Q and rules out sampled-prime rank drops, but a complete torsion-free proof should compute SNF or gcd of maximal minors.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXII_integral_homology_torsion_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
