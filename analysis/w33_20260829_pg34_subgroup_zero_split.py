#!/usr/bin/env python3
"""Exact subgroup-breaking hierarchy for the 85-state chiral coupling.

For H <= PSp(4,3), an H-equivariant 40x45 coupling is constant on H-orbits
of cross pairs.  We construct that full orbital matrix space and exhibit exact
finite-field full-rank witnesses whenever possible.  Rank 40 is the absolute
rectangular maximum, hence leaves only the five index-protected zero modes.

The chain is tied to one sentinel five-circuit stabilizer S5 and its natural
subgroups on the five circuit elements.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from collections import deque

from w33_20260829_216_clifford_torsor_nogo import (
    geometry,supports_from_N,closure_paired,norm,form,compose,porder
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_SUBGROUP_ZERO_SPLIT.json'
P=1000003

def rank_mod(A,p=P):
    M=[[x%p for x in r] for r in A];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i][c]),None)
        if q is None:continue
        M[r],M[q]=M[q],M[r];inv=pow(M[r][c],p-2,p);M[r]=[(x*inv)%p for x in M[r]]
        for i in range(m):
            if i==r or not M[i][c]:continue
            a=M[i][c];M[i]=[(M[i][j]-a*M[r][j])%p for j in range(n)]
        r+=1
        if r==m:break
    return r

def parity(p):
    inv=0
    for i in range(len(p)):
        for j in range(i+1,len(p)):inv+=p[i]>p[j]
    return inv&1

def cross_orbit_index(H):
    rem={(i,j) for i in range(40) for j in range(45)};idx={};sizes=[];k=0
    while rem:
        seed=min(rem);O={(h[0][seed[0]],h[1][seed[1]]) for h in H}
        for x in O:idx[x]=k
        sizes.append(len(O));rem-=O;k+=1
    assert len(idx)==1800
    return idx,sorted(sizes)

def witness_rank(idx,norb,seed):
    # Deterministic nonzero coefficients in F_p; the returned matrix itself is
    # an exact witness, while rank=40 proves maximality by the rectangular bound.
    x=(seed*1664525+1013904223)%P;coeff=[]
    for _ in range(norb):
        x=(1664525*x+1013904223)%P;coeff.append(1+x%(P-1))
    M=[[coeff[idx[(i,j)]] for j in range(45)] for i in range(40)]
    return rank_mod(M),coeff

def main():
    pts,idxp,lines,N=geometry();supports,masks=supports_from_N(N)
    circuits=[]
    for cc in itertools.combinations(range(45),5):
        w=0
        for i in cc:w^=masks[i]
        if w==0:circuits.append(cc)
    assert len(circuits)==216

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3;y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idxp[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)};gens45=[]
    for p in gens40:gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen=(18,62,77,10);G=closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    c0=tuple(circuits[0]);cset=set(c0)
    S5=[h for h in G if {h[1][x] for x in cset}==cset];assert len(S5)==120
    pos={x:i for i,x in enumerate(c0)}
    def p5(h):return tuple(pos[h[1][x]] for x in c0)
    A5=[h for h in S5 if parity(p5(h))==0];assert len(A5)==60
    S4=[h for h in S5 if p5(h)[0]==0];assert len(S4)==24
    A4=[h for h in S4 if parity(p5(h))==0];assert len(A4)==12
    V4=[h for h in A4 if porder(p5(h)) in (1,2)];assert len(V4)==4
    e=next(h for h in V4 if porder(p5(h))==1)
    g2=next(h for h in V4 if porder(p5(h))==2);C2=[e,g2]
    chain=[('PSp(4,3)',G),('S5',S5),('A5',A5),('S4',S4),('A4',A4),('V4',V4),('C2',C2),('1',[e])]

    rows=[]
    for name,H in chain:
        oi,sizes=cross_orbit_index(H);norb=1+max(oi.values())
        best=(-1,None)
        for seed in range(1,65):
            r,coef=witness_rank(oi,norb,seed)
            if r>best[0]:best=(r,seed)
            if r==40:break
        r,seed=best
        # PSp upper bound 25 is the established 1+24 common-module theorem.
        if name=='PSp(4,3)': assert r==25
        else: assert r==40, (name,r,norb)
        rows.append({'subgroup':name,'order':len(H),'crossPairOrbits':norb,
          'crossOrbitSizes':sizes,'maxRankWitness':r,'witnessSeed':seed,
          'minimumChiralZeroModes':85-2*r})

    out={'schema':'w33.20260829.pg34-subgroup-zero-split.v1','status':'PASS','chain':rows,
      'theorem':'The extra 30 PSp-protected zero modes are completely lifted already by symmetry breaking to the sentinel-circuit stabilizer S5: an S5-equivariant coupling of full rectangular rank 40 exists. Every subgroup below S5 therefore also permits only the five index-protected zero modes.',
      'boundary':'Exact finite chiral-coupling/intertwiner statement. A permitted perturbation is not asserted to be physically local or dynamically generated.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
