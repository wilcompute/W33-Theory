#!/usr/bin/env python3
"""Index-vs-symmetry protection for the 85-state PG(3,4) chiral coupling.

This extends w33_20260829_pg34_85_chiral_module.py.  The off-diagonal coupling
B is 40x45 and has rank 25.  Chiral/sub-lattice imbalance alone forces only
|40-45|=5 zero modes for an arbitrary off-diagonal coupling.  The observed
15+20=35 zero modes require the established PSp(4,3) representation split:
40=1+24+15 and 45=1+24+20, so the unmatched 15 and 20 sectors cannot couple
under PSp-equivariant perturbations.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_FLATBAND_INDEX.json'

def norm(v):
    i=next(k for k,x in enumerate(v) if x%3); z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)
def form(u,v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def rank_mod(A,p=1000003):
    M=[[x%p for x in r] for r in A]; m=len(M); n=len(M[0]); r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i][c]),None)
        if q is None: continue
        M[r],M[q]=M[q],M[r]; inv=pow(M[r][c],p-2,p)
        M[r]=[(x*inv)%p for x in M[r]]
        for i in range(m):
            if i==r or not M[i][c]: continue
            a=M[i][c]; M[i]=[(M[i][j]-a*M[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r

def build_B():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4: lines.add(tuple(sorted(S)))
    lines=sorted(lines); N=[[0]*40 for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:N[li][p]=1
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]
    sig=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        z=tuple(sum(cols[p][l] for p in S) for l in range(40)); sig[z].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in sig.values() if len(v)==2)
    assert len(pairs)==45
    B=[[0]*45 for _ in range(40)]
    for m,(u,v) in enumerate(pairs):
        for c in set(u)|set(v):B[c][m]=1
    return B

def add(A,C,sa=1,sc=1): return [[sa*A[i][j]+sc*C[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def main():
    B=build_B(); J=[[1]*45 for _ in range(40)]
    assert rank_mod(B)==25
    # A concrete chiral-symmetry-preserving perturbation reaching maximal
    # rectangular rank.  Full rank mod p proves full rational row rank.
    E=[[1 if i==j else 0 for j in range(45)] for i in range(40)]
    generic=add(B,E); assert rank_mod(generic)==40
    # Natural two-dimensional equivariant family spanned by B and J.
    assert rank_mod(add(B,J))==25
    assert rank_mod(add(B,J,5,-1))==24  # trivial-sector cancellation

    out={
      'schema':'w33.20260829.pg34-flatband-index.v1','status':'PASS',
      'sublattices':[40,45],'incidenceRank':25,'observedZeroModes':35,
      'chiralIndex':-5,
      'arbitraryChiralPerturbation':{
        'exampleRank':40,'zeroModes':5,
        'theorem':'For any 40x45 off-diagonal coupling, nullity(left)-nullity(right)=40-45=-5; hence at least five zero modes survive, but 35 need not.'},
      'PSpEquivariantProtection':{
        'leftModule':'1 + 24 + 15','rightModule':'1 + 24 + 20',
        'unmatchedSectors':[15,20],'protectedZeroModes':35,
        'naturalIntertwinerFamily':'a B + b J; generic rank 25, with rank 24 on the trivial-sector cancellation 9a+45b=0'},
      'reading':'The five-mode residue is index/sublattice-imbalance protected. The full 35-mode flat band is protected only while the PSp(4,3) representation mismatch is respected.',
      'boundary':'Exact finite linear-algebra/representation statement. Flat-band/chiral terminology does not assert a material band structure, fermion species, or measured Hamiltonian.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rankB':25,'genericRank':40,'index':-5,'PSpZeroModes':35}))
if __name__=='__main__':main()
