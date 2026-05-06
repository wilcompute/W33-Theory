#!/usr/bin/env python3
"""PART CCCLXVII -- Odd-Triple Nullspace Basis Certificate.

CCCLXV proved that the odd-triple operator K=M^T M has rank 40 and nullity
4440.  CCCLXVII makes that nullspace constructive without dumping 4440 huge
vectors into the repository.

Let M be the 40 x 4480 vertex-by-odd-triple incidence matrix.  The compiler:

1. constructs all 4480 odd triples,
2. finds 40 pivot odd triples whose incidence columns form an invertible
   40 x 40 matrix P,
3. proves rank(M)=40 from det(P) != 0,
4. defines a generator for each free odd triple c:

      x_free = 1,
      x_pivot = - P^{-1} c,

   so that M x = 0.

Thus the 4440-dimensional null/gauge space is represented as a reproducible
pivot/free-column basis rule, with sample basis vectors verified exactly over Q.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
P=1000003
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
def edge_count(tri,adj): return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def odd_triples(adj): return [tri for tri in itertools.combinations(range(len(adj)),3) if edge_count(tri,adj)%2==1]
def col_dict(tri,p=P): return {i:1%p for i in tri}
def reduce_mod(vec,basis,p=P):
    vec=dict(vec)
    while vec:
        piv=min(vec)
        coeff=vec[piv]%p
        if coeff==0:
            del vec[piv]; continue
        if piv not in basis: return vec
        prow=basis[piv]
        for k,v in prow.items():
            vec[k]=(vec.get(k,0)-coeff*v)%p
            if vec[k]==0: del vec[k]
    return vec
def pivot_columns(odd):
    basis={}; pivots=[]
    for idx,tri in enumerate(odd):
        vec=reduce_mod(col_dict(tri),basis)
        if vec:
            piv=min(vec); coeff=vec[piv]%P; inv=pow(coeff,P-2,P)
            norm={k:(v*inv)%P for k,v in vec.items() if (v*inv)%P}
            basis[piv]=norm; pivots.append(idx)
            if len(pivots)==40: break
    return pivots
def pivot_matrix(odd,pivots):
    return [[Fraction(1 if r in odd[c] else 0) for c in pivots] for r in range(40)]
def invert_fraction_matrix(A):
    n=len(A); aug=[row[:] + [Fraction(1 if i==j else 0) for j in range(n)] for i,row in enumerate(A)]
    for c in range(n):
        pivot=None
        for r in range(c,n):
            if aug[r][c]!=0:
                pivot=r; break
        if pivot is None: raise ValueError('singular')
        aug[c],aug[pivot]=aug[pivot],aug[c]
        fac=aug[c][c]
        aug[c]=[x/fac for x in aug[c]]
        for r in range(n):
            if r==c: continue
            f=aug[r][c]
            if f:
                aug[r]=[aug[r][j]-f*aug[c][j] for j in range(2*n)]
    return [row[n:] for row in aug]
def mat_vec(A,v): return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]
def column_vector(tri): return [Fraction(1 if r in tri else 0) for r in range(40)]
def null_vector_for_free(odd,pivots,Pinv,free_idx):
    c=column_vector(odd[free_idx]); y=mat_vec(Pinv,c)
    coeffs={pivots[j]:-y[j] for j in range(len(pivots)) if y[j]!=0}
    coeffs[free_idx]=Fraction(1)
    return coeffs
def verify_null_vector(odd,coeffs):
    sums=[Fraction(0) for _ in range(40)]
    for idx,coef in coeffs.items():
        for v in odd[idx]: sums[v]+=coef
    return all(x==0 for x in sums)
def fraction_str(x): return f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator)
def sample_basis_vectors(odd,pivots,Pinv,count=3):
    free=[i for i in range(len(odd)) if i not in set(pivots)]
    out=[]
    for idx in free[:count]:
        coeffs=null_vector_for_free(odd,pivots,Pinv,idx)
        out.append({"free_index":idx,"free_triple":odd[idx],"support_size":len(coeffs),"verified":verify_null_vector(odd,coeffs),"first_coefficients":[[k,fraction_str(v)] for k,v in list(coeffs.items())[:8]]})
    return out
def build_results():
    pts,adj=build_graph(); odd=odd_triples(adj); piv=pivot_columns(odd); Pmat=pivot_matrix(odd,piv); Pinv=invert_fraction_matrix(Pmat); samples=sample_basis_vectors(odd,piv,Pinv,3); checks=[]
    checks.append(ok('odd triples = 4480',len(odd)==4480,len(odd)))
    checks.append(ok('pivot count = 40',len(piv)==40,len(piv)))
    checks.append(ok('free count = 4440',len(odd)-len(piv)==4440,len(odd)-len(piv)))
    checks.append(ok('pivot matrix inverse is 40x40',len(Pinv)==40 and all(len(r)==40 for r in Pinv),[len(Pinv),len(Pinv[0])]))
    checks.append(ok('sample null vectors verified',all(s['verified'] for s in samples),samples))
    checks.append(ok('sample support sizes are finite',all(s['support_size']>=2 for s in samples),[s['support_size'] for s in samples]))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXVII","title":"Odd-Triple Nullspace Basis Certificate","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"matrix":"M is 40 x 4480 vertex-by-odd-triple incidence","rank_certificate":"40 pivot odd-triple columns form an invertible 40 x 40 incidence matrix P","nullity":4440,"basis_rule":"for each free column c, basis vector has x_c=1 and x_pivots=-P^{-1}c, so Mx=0","pivot_indices_first_20":piv[:20],"sample_basis_vectors":samples,"architecture_upgrade":"CCCLXV identified a 4440-dimensional odd-triple null/gauge kernel. CCCLXVII gives a constructive pivot/free-column basis rule and verifies sample basis vectors exactly over Q.","theorem":"Choosing any 40 independent odd-triple incidence columns P gives an explicit basis of ker(M): for every nonpivot column c, the vector e_c - P^{-1}c on pivot coordinates satisfies Mx=0. Since M has 4480 columns and rank 40, these 4440 vectors form a basis for the odd-triple null/gauge space.","honesty_boundary":"The compiler stores the generator rule and sample vectors rather than writing all 4440 basis vectors to the repository.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXVII_odd_triple_nullspace_basis_certificate_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
