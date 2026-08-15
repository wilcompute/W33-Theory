#!/usr/bin/env python3
"""Pass5359: prime-anchor Wedderburn census for the canonical PSL2(q) pair Hecke algebra.

Pass5357 proves the all-odd orbital rank of the canonical pair space.  This pass
computes the *full intersection tensor* at prime anchors q=3,5,7,11,13,17,19,23.
It extracts center and commutator dimensions of the orbital algebra and infers
the unique complex matrix-block sizes from semisimplicity.

This is a finite anchor census, not an all-q decomposition theorem.  The observed
number of M2 blocks is floor((q+3)/8) at these anchors; that pattern is emitted as
a conjectural continuation only.
"""
from __future__ import annotations
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5359_PRIME_PAIR_HECKE_WEDDERBURN_CENSUS.json'
INF=-1

def canonical_pm(M,p):
    M=tuple(x%p for x in M); n=tuple((-x)%p for x in M); return min(M,n)

def mobius(M,x,p):
    a,b,c,d=M; X,Y=(a,c) if x==INF else ((a*x+b)%p,(c*x+d)%p)
    return INF if Y%p==0 else X*pow(Y,-1,p)%p

def psl2(p):
    pts=list(range(p))+[INF]; idx={x:i for i,x in enumerate(pts)}; mats=set()
    for a in range(p):
      for b in range(p):
       for c in range(p):
        if a:
            mats.add(canonical_pm((a,b,c,(1+b*c)*pow(a,-1,p)%p),p))
        elif b and c and (-b*c)%p==1:
            for d in range(p):mats.add(canonical_pm((a,b,c,d),p))
    G={tuple(idx[mobius(M,x,p)] for x in pts) for M in mats}
    assert len(G)==p*(p*p-1)//2
    return sorted(G)

def rank_q(rows):
    A=[[Fraction(x) for x in row] for row in rows if any(row)]
    if not A:return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]; z=A[r][c]; A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]; A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
        if r==m:break
    return r

def matmul(A,B):
    n=len(A); return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def block_partitions(total,blocks,minsize=1):
    ans=[]
    def rec(left,k,lo,cur):
        if k==0:
            if left==0:ans.append(cur[:])
            return
        for s in range(lo,int(left**0.5)+1):
            rec(left-s*s,k-1,s,cur+[s])
    rec(total,blocks,minsize,[]); return ans

def analyze(p):
    G=psl2(p); n=p+1; pairs=list(combinations(range(n),2)); pi={x:i for i,x in enumerate(pairs)}
    H=[tuple(pi[tuple(sorted((g[a],g[b])))] for a,b in pairs) for g in G]
    St=[g for g in H if g[0]==0]; assert len(St)==p-1
    unseen=set(range(len(pairs))); orbs=[]
    while unseen:
        x=min(unseen); O={g[x] for g in St}; orbs.append(sorted(O)); unseen-=O
    orbs.sort(key=lambda O:(len(O),O[0])); sub={x:i for i,O in enumerate(orbs) for x in O}
    to0=[next(g for g in H if g[x]==0) for x in range(len(pairs))]
    R=[[sub[to0[x][y]] for y in range(len(pairs))] for x in range(len(pairs))]
    r=len(orbs); P=[[[0]*r for _ in range(r)] for __ in range(r)]
    for k,O in enumerate(orbs):
        y=O[0]
        for z in range(len(pairs)):P[k][R[0][z]][R[z][y]]+=1
    L=[]
    for i in range(r):
        M=[[0]*r for _ in range(r)]
        for j in range(r):
            for k in range(r):M[k][j]=P[k][i][j]
        L.append(M)
    center_eq=[]
    for j in range(r):
        commmats=[]
        for i in range(r):
            AB=matmul(L[i],L[j]); BA=matmul(L[j],L[i])
            commmats.append([[AB[a][b]-BA[a][b] for b in range(r)] for a in range(r)])
        for a in range(r):
            for b in range(r):
                row=[commmats[i][a][b] for i in range(r)]
                if any(row):center_eq.append(row)
    center=r-rank_q(center_eq)
    comm=rank_q([[P[k][i][j]-P[k][j][i] for k in range(r)] for i in range(r) for j in range(r)])
    assert comm==r-center
    transpose=[R[orbs[i][0]][0] for i in range(r)]
    symmetric=sum(i==t for i,t in enumerate(transpose))
    parts=block_partitions(r,center); assert len(parts)==1
    blocks=parts[0]
    return {'q':p,'group_order':len(G),'fiber_size':len(pairs),'pair_stabilizer_order':len(St),
      'orbital_rank':r,'subdegrees':[len(O) for O in orbs],
      'symmetric_orbitals':symmetric,'directed_orbitals':r-symmetric,
      'center_dimension':center,'commutator_dimension':comm,'complex_block_sizes':blocks,
      'M2_block_count':blocks.count(2)}

def main():
    anchors={str(q):analyze(q) for q in (3,5,7,11,13,17,19,23)}
    for q,row in [(int(q),r) for q,r in anchors.items()]:
        assert row['M2_block_count']==(q+3)//8
    out={'pass':5359,'status':'THEOREM_PRIME_ANCHOR_PAIR_HECKE_WEDDERBURN_CENSUS',
      'anchors':anchors,
      'q5_recovery':'q=5 gives block sizes [1,1,2], i.e. C^2 + M2(C), exactly Pass5336.',
      'observed_pattern':'At all eight prime anchors the algebra contains only scalar and M2 blocks, with M2 count floor((q+3)/8).',
      'pattern_status':'CONJECTURAL_ALL_Q; exact only at the displayed prime anchors.',
      'boundary':'Pass5357 proves orbital rank for every odd prime power. This pass does not prove the displayed Wedderburn pattern for arbitrary q and does not identify any characteristic-2 footprint module.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
