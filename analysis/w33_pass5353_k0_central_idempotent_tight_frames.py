#!/usr/bin/env python3
"""Pass5353 (bonkers): turn the q=5 K0 rank-21 orbital algebra into seven exact spherical tight-frame embeddings.

For a transitive coherent configuration, every primitive central idempotent E is
an orthogonal projection in the 2340-point permutation module. Normalizing its
rows gives a unit-norm tight frame in rank(E) dimensions. Because E is constant
on orbitals, all inner products are exact rational numbers read directly from
the 21 orbital coefficients. This pass computes those seven Gram spectra and
detects collapse relations (inner product +1), antipodes (-1), and the number of
distinct projected vectors.
"""
from __future__ import annotations
import json
from collections import Counter
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path
import numpy as np
from sympy import Matrix
from analysis.w33_pass5332_q5_k0_orbital_wedderburn import build_action,tensor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5353_K0_CENTRAL_IDEMPOTENT_TIGHT_FRAMES.json'

def fstr(x:Fraction):return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def mul(P,a,b):
    r=len(a);out=[Fraction(0) for _ in range(r)]
    for i,ai in enumerate(a):
        if not ai:continue
        for j,bj in enumerate(b):
            if not bj:continue
            for k,v in enumerate(P[:,i,j]):
                if v:out[k]+=ai*bj*int(v)
    return out

def main():
    garr,orbs=build_action();P,tr=tensor(garr,orbs);r=21
    L=[]
    for i in range(r):
        M=np.zeros((r,r),dtype=int)
        for j in range(r):M[:,j]=P[:,i,j]
        L.append(M)
    rows=[]
    for j in range(r):
        C=[L[i]@L[j]-L[j]@L[i] for i in range(r)]
        for a in range(r):
            for b in range(r):
                v=[int(C[i][a,b]) for i in range(r)]
                if any(v):rows.append(v)
    A=Matrix(rows);ns=A.nullspace();assert len(ns)==7
    Z=[]
    for v in ns:
        den=1
        for x in v:den=np.lcm(den,int(x.q))
        a=np.array([int(x*den) for x in v],dtype=np.int64)
        gg=reduce(gcd,[abs(int(x)) for x in a if x] or [1]);a//=gg
        if next((x for x in a if x),1)<0:a=-a
        Z.append(a)
    c=sum((i+1)*Z[i] for i in range(7));C=sum(int(c[i])*L[i] for i in range(r))
    eig=[9878,1283,998,443,128,-352,-340]
    alg_mult={9878:1,1283:1,998:1,443:1,128:9,-352:4,-340:4}
    one=[Fraction(0) for _ in range(r)];one[0]=1;z=[Fraction(int(x)) for x in c]
    frames=[]
    for lam in eig:
        e=one;den=1
        for mu in eig:
            if mu==lam:continue
            t=z.copy();t[0]-=mu;e=mul(P,e,t);den*=lam-mu
        e=[x/Fraction(den) for x in e];assert mul(P,e,e)==e
        assert all(e[i]==e[tr[i]] for i in range(r))
        rank=Fraction(2340)*e[0];assert rank.denominator==1;rank=int(rank)
        diag=e[0];assert diag>0
        hist=Counter()
        for i,O in enumerate(orbs):
            if i==0:continue
            hist[e[i]/diag]+=len(O)
        assert sum(hist.values())==2339
        dup=1+sum(n for x,n in hist.items() if x==1)
        assert 2340%dup==0
        distinct=2340//dup
        anti=sum(n for x,n in hist.items() if x==-1)
        m=int(round(alg_mult[lam]**0.5));assert m*m==alg_mult[lam]
        irrep=rank//m;assert irrep*m==rank
        frames.append({
          'central_eigenvalue':lam,'isotypic_rank':rank,'multiplicity':m,'irreducible_dimension':irrep,
          'unit_norm_tight_frame':{'vectors_with_multiplicity':2340,'ambient_rank':rank,'frame_constant':fstr(Fraction(2340,rank))},
          'distinct_projected_vectors':distinct,'duplicate_class_size':dup,'antipodal_neighbors_per_row':anti,
          'offdiagonal_inner_product_histogram':{fstr(x):n for x,n in sorted(hist.items(),key=lambda kv:float(kv[0]))},
          'number_of_offdiagonal_inner_products':len(hist)})
    # The unique multiplicity-one 65 block should collapse the 15-point fibers to 156 base points.
    base65=[x for x in frames if x['irreducible_dimension']==65 and x['multiplicity']==1]
    assert len(base65)==1 and base65[0]['duplicate_class_size']==15 and base65[0]['distinct_projected_vectors']==156
    out={'pass':5353,'status':'THEOREM_Q5_K0_CENTRAL_IDEMPOTENTS_GIVE_SEVEN_EXACT_SPHERICAL_TIGHT_FRAMES',
      'source':'rank-21 noncommutative orbital algebra from Pass5332',
      'frames':frames,
      'base_65_detection':'The multiplicity-one 65-dimensional central block has 15 identical shell vectors per W-point fiber, hence exactly156 distinct projected vectors.',
      'boundary':'These are exact representation-theoretic spherical embeddings. Tight-frame structure alone is not a physical state-space claim and does not imply a new code-distance bound without an additional LP/moment argument.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
