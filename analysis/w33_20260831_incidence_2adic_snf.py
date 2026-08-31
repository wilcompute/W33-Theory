#!/usr/bin/env python3
"""Complete the Smith normal forms of M, M+, M- at the only possible prime 2.

Prior exact work proves:
  * all three 216x540 matrices have rational row rank 216;
  * rank_2(M)=156 and rank_2(M+)=rank_2(M-)=201;
  * every nonunit Smith invariant is a power of 2 (odd candidate primes are
    excluded by full modular row rank).

Therefore it suffices to compute the exact 2-adic invariant exponents.  This
script diagonalizes over Z/2^K using only invertible row/column operations:
at each stage select an entry of minimum 2-adic valuation, normalize its odd
unit, and clear its row and column.  If every recovered exponent is <K, these
are the integral Smith exponents, not merely truncated data.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, deque
from pathlib import Path
import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import rank_mod

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_INCIDENCE_2ADIC_SNF.json'


def smith2_exponents(A: np.ndarray, K: int=24) -> list[int]:
    mod=1<<K
    B=np.array(A,dtype=np.int64,copy=True)%mod
    m,n=B.shape
    exps=[]
    for i in range(m):
        sub=B[i:,i:]
        found=None
        for e in range(K):
            mask=(sub % (1<<(e+1))) != 0
            if np.any(mask):
                rr,cc=np.argwhere(mask)[0]
                found=(e,i+int(rr),i+int(cc)); break
        if found is None:
            exps.extend([K]*(m-i)); break
        e,r,c=found
        if r!=i: B[[i,r],:]=B[[r,i],:]
        if c!=i: B[:,[i,c]]=B[:,[c,i]]
        a=int(B[i,i]); assert a and a%(1<<e)==0 and a%(1<<(e+1))==(1<<e)
        unit=a>>e
        inv=pow(unit,-1,mod)
        B[i,:]=(B[i,:]*inv)%mod
        assert int(B[i,i])==(1<<e)

        # Clear the pivot column below i.  Minimality of e guarantees exact
        # divisibility by 2^e for every remaining entry.
        for r2 in range(i+1,m):
            val=int(B[r2,i])
            if val:
                assert val%(1<<e)==0
                q=val>>e
                B[r2,:]=(B[r2,:]-q*B[i,:])%mod
                assert int(B[r2,i])==0

        # Clear the pivot row to the right.  The pivot column is already zero
        # below i, so these column operations cannot reintroduce entries there.
        for c2 in range(i+1,n):
            val=int(B[i,c2])
            if val:
                assert val%(1<<e)==0
                q=val>>e
                B[:,c2]=(B[:,c2]-q*B[:,i])%mod
                assert int(B[i,c2])==0
        exps.append(e)
    assert len(exps)==m
    assert exps==sorted(exps)
    return exps


def histogram(exps):
    return {str(k):int(v) for k,v in sorted(Counter(exps).items())}


def main():
    # Sanity test the local algorithm on a known rectangular diagonal form.
    D=np.zeros((5,8),dtype=np.int64)
    for i,e in enumerate([0,1,2,4,7]): D[i,i]=1<<e
    assert smith2_exponents(D,12)==[0,1,2,4,7]

    pts,idx,_lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: c5.append(C)
    c6=six_circuits(masks); i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for q in pts:
                z=alpha*base.form(q,v)%3
                y=base.norm(tuple((q[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[q] for q in S)] for S in supports) for p in gens40]
    gg=[gens45[i] for i in (18,62,77,10)]
    act5=[tuple(i5[tuple(sorted(g[q] for q in C))] for C in c5) for g in gg]
    act6=[tuple(i6[tuple(sorted(g[q] for q in C))] for C in c6) for g in gg]
    s5=[set(C) for C in c5]; s6=[set(C) for C in c6]
    M=np.zeros((216,540),dtype=np.int64)
    for a in range(216):
        for b in range(540):
            if len(s5[a]&s6[b])==3: M[a,b]=1
    seed=next(a*540+b for a in range(216) for b in range(540) if M[a,b])
    O={seed}; Q=deque([seed])
    while Q:
        z=Q.popleft(); a,b=divmod(z,540)
        for p5,p6 in zip(act5,act6):
            nz=p5[a]*540+p6[b]
            if nz not in O: O.add(nz); Q.append(nz)
    Mp=np.zeros_like(M)
    for z in O:
        a,b=divmod(z,540); Mp[a,b]=1
    Mm=M-Mp

    K=24
    rows=[]
    for name,A,rank2 in [('M',M,156),('Mplus',Mp,201),('Mminus',Mm,201)]:
        assert rank_mod(A,1000003)==216 and rank_mod(A,2)==rank2
        exps=smith2_exponents(A,K)
        assert max(exps)<K
        assert exps.count(0)==rank2
        rows.append({'matrix':name,'rows':216,'columns':540,'rank':216,
                     'unitInvariantFactors':exps.count(0),'positive2PowerInvariantFactors':216-exps.count(0),
                     'max2AdicExponent':max(exps),'sum2AdicExponents':sum(exps),
                     'exponentHistogram':histogram(exps),
                     'nonzeroSmithForm':' '.join(f"2^{e}^{histogram(exps)[str(e)]}" for e in sorted(set(exps)))})

    out={'schema':'w33.20260831.incidence-2adic-snf.v1','status':'PASS','modulusExponent':K,
         'matrices':rows,
         'theorem':'Because prior certificates exclude all odd Smith primes, these recovered sub-K 2-adic exponents are the complete nonzero integral Smith normal forms of M, M+, and M-.',
         'boundary':'The 324 zero diagonal entries from the rectangular 216x540 presentation are omitted from the nonzero Smith lists.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rows':[{k:r[k] for k in ('matrix','exponentHistogram','max2AdicExponent','sum2AdicExponents')} for r in rows]},sort_keys=True))

if __name__=='__main__': main()
