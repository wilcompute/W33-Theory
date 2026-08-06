#!/usr/bin/env python3
"""Pass 3982: ordering-independent Hadamard cut-rank bound plus exact ordering search."""
from __future__ import annotations
import json, random
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=[7,19,9,17,14,25,24,15,10,16,20,6,4,32,31,0,33,3,1,28,5,2,30,26,29,27,35,34,21,22,23,12,11,13,8,18]

def bits(x,n=6): return [(x>>i)&1 for i in range(n)]
def qform(x):
    b=bits(x); return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y): return qform(x^y)^qform(x)^qform(y)
def hadamard():
    xs=[x for x in range(1,64) if qform(x)]; assert len(xs)==36
    A=[[0]*36 for _ in range(36)]
    for i,x in enumerate(xs):
        for j,y in enumerate(xs):
            if i!=j and beta(x,y)==0: A[i][j]=1
    K=[[2*A[i][j]-1 for j in range(36)] for i in range(36)]
    assert all(sum(K[i][t]*K[j][t] for t in range(36))==(36 if i==j else 0) for i in range(36) for j in range(36))
    assert all(K[i][j]==K[j][i] for i in range(36) for j in range(36))
    return K

def max_pm6_multiplicity(k):
    # m eigenvalues are +/-6.  trace(A)=-k and trace(A^2)=k^2.
    best=0
    for m in range(k+1):
        sq=k*k-36*m
        if sq<0: continue
        rem=k-m
        for d in range(-m,m+1,2): # d=m_plus-m_minus
            residual_sum=-k-6*d
            ok=(sq==0 and residual_sum==0) if rem==0 else sq*rem>=residual_sum*residual_sum
            if ok: best=max(best,m)
    return best

def universal_sequence():
    half=[k-max_pm6_multiplicity(k) for k in range(1,19)]
    total=2*sum(half[:-1])+half[-1]
    assert total==229
    return half,total

def rank_mod(rows,p):
    if not rows: return 0
    a=[[x%p for x in row] for row in rows]
    m=len(a); n=len(a[0]); r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if a[i][c]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][c],p-2,p)
        a[r]=[(x*inv)%p for x in a[r]]
        for i in range(m):
            if i!=r and a[i][c]:
                f=a[i][c]; a[i]=[(x-f*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==m: break
    return r

def rank_q(rows):
    if not rows: return 0
    a=[[Fraction(x) for x in row] for row in rows]
    m=len(a); n=len(a[0]); r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if a[i][c]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        q=a[r][c]; a[r]=[x/q for x in a[r]]
        for i in range(r+1,m):
            if a[i][c]:
                f=a[i][c]; a[i]=[x-f*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==m: break
    return r

def cut_rank(K,subset,p=1000003):
    S=[i for i in range(36) if subset>>i&1]; T=[i for i in range(36) if not subset>>i&1]
    if len(S)>len(T): S,T=T,S
    return rank_mod([[K[i][j] for j in T] for i in S],p)

def chain(order,K,cache):
    mask=0; ranks=[]
    for v in order[:-1]:
        mask|=1<<v
        key=min(mask,((1<<36)-1)^mask)
        if key not in cache: cache[key]=cut_rank(K,key)
        ranks.append(cache[key])
    return ranks,sum(ranks)

def search(K):
    rng=random.Random(3982); cache={}
    order=BASE[:]; ranks,score=chain(order,K,cache)
    base_score=score; best=(score,order[:],ranks[:])
    temperature=3.0
    for step in range(30000):
        i,j=sorted(rng.sample(range(36),2)); cand=order[:]; cand[i],cand[j]=cand[j],cand[i]
        cr,cs=chain(cand,K,cache)
        accept=cs<=score or rng.random()<pow(2.718281828,-(cs-score)/max(temperature,1e-9))
        if accept: order,ranks,score=cand,cr,cs
        if score<best[0]: best=(score,order[:],ranks[:])
        temperature*=0.99985
    # deterministic best-improvement cleanup
    changed=True
    while changed:
        changed=False; candidate_best=best
        for i in range(36):
            for j in range(i+1,36):
                cand=best[1][:]; cand[i],cand[j]=cand[j],cand[i]
                cr,cs=chain(cand,K,cache)
                if cs<candidate_best[0]: candidate_best=(cs,cand,cr)
        if candidate_best[0]<best[0]: best=candidate_best; changed=True
    exact=[]; mask=0
    for v in best[1][:-1]:
        mask|=1<<v; S=[i for i in range(36) if mask>>i&1]; T=[i for i in range(36) if not mask>>i&1]
        if len(S)>len(T): S,T=T,S
        rows=[[K[i][j] for j in T] for i in S]
        rq=rank_q(rows); assert rq==rank_mod(rows,1000003)==rank_mod(rows,1000033)
        exact.append(rq)
    assert sum(exact)==best[0]
    return {'base_order':BASE,'base_cut_ranks':chain(BASE,K,cache)[0],'base_bound':base_score,
            'best_order':best[1],'best_cut_ranks':exact,'best_bound':best[0],'cache_entries':len(cache)}

def main():
    K=hadamard(); half,total=universal_sequence(); result=search(K)
    result.update({'schema':'w33.pass3982.global_mesh_bound.v1','status':'PASS',
      'universal_half_cut_rank_lower_bounds':half,'universal_adjacent_factor_lower_bound':total,
      'proof':'For each principal cut A|B of symmetric K with K^2=36I, BB^T=36I-A^2. Cut-rank defect equals the multiplicity of eigenvalues +/-6 of A. trace(A)=-k, trace(A^2)=k^2, and Cauchy bound that multiplicity.',
      'boundary':'229 is ordering-independent. The searched ordering is an exact constructive cut-rank certificate, not a proof that its cut-rank sum or a physical factorization is globally optimal.'})
    (ROOT/'data/PART_3982_GLOBAL_MESH_BOUND.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_GLOBAL_MESH_BOUND',total,result['best_bound'])
if __name__=='__main__': main()
