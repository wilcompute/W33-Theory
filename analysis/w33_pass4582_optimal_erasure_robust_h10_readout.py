#!/usr/bin/env python3
"""Pass 4582 -- exact minimum erasure-robust H10 carrier readouts.

Allowed readout carriers are the 40 line-stars A_*e_i and 240 protected edge
vectors A_*(e_i+e_j).  A selected set survives t arbitrary erased channels iff
every nonzero linear functional on H10 is nonzero on at least t+1 selected
carriers.  Equivalently its 10-dimensional binary row code has distance >=t+1.

Frozen witnesses attain the exact minima 11 for t=1 and 14 for t=2.  The lower
bound 11 is dimensional.  For t=2, n=12,13 are impossible by the binary Hamming
bound 2^10(1+n)<=2^n, while the 14-channel witness has minimum functional support 3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4582_OPTIMAL_ERASURE_ROBUST_H10_READOUT.json'

def rank_basis(vecs):
    piv={}
    for x in map(int,vecs):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())

def coord_solver(basis):
    d={}
    for i,v in enumerate(basis):
        y=int(v);c=1<<i
        while y:
            p=y.bit_length()-1
            if p in d:y^=d[p][0];c^=d[p][1]
            else:d[p]=(y,c);break
    def solve(v):
        y=int(v);c=0
        while y:
            p=y.bit_length()-1
            if p not in d:raise ValueError('outside span')
            y^=d[p][0];c^=d[p][1]
        return c
    return solve

def main()->int:
    vals=build_geometry();A=np.asarray(vals[5],dtype=np.uint8)
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]]
    edgev=[cols[i]^cols[j] for i,j in edges]
    carriers=cols+edgev
    labels=[('star',i) for i in range(40)]+[('edge',e) for e in edges]
    assert len(carriers)==len(set(carriers))==280
    # Deterministic H10 coordinate basis from line-stars.
    B=[];bidx=[]
    for i,v in enumerate(cols):
        if len(rank_basis(B+[v]))>len(B):B.append(v);bidx.append(i)
        if len(B)==10:break
    assert bidx==[0,1,2,3,4,5,7,8,10,11]
    solve=coord_solver(B);coords=[solve(v) for v in carriers]
    lookup={lab:i for i,lab in enumerate(labels)}
    W1=[('star',8),('star',12),('star',20),('star',38),('edge',(3,31)),('edge',(4,12)),('edge',(9,24)),('edge',(9,26)),('edge',(19,21)),('edge',(25,28)),('edge',(28,32))]
    W2=[('star',3),('star',7),('star',10),('star',13),('star',16),('star',19),('star',38),('edge',(3,17)),('edge',(4,5)),('edge',(9,14)),('edge',(11,12)),('edge',(17,18)),('edge',(18,27)),('edge',(37,38))]
    def verify(W,t):
        idx=[lookup[x] for x in W];assert len(rank_basis([carriers[i] for i in idx]))==10
        prof=Counter()
        for f in range(1,1<<10):
            wt=sum(((f&coords[i]).bit_count()&1) for i in idx);prof[wt]+=1
        assert min(prof)>=t+1
        # Direct deletion regression.
        for D in itertools.combinations(range(len(idx)),t):
            assert len(rank_basis([carriers[idx[k]] for k in range(len(idx)) if k not in D]))==10
        return prof
    p1=verify(W1,1);p2=verify(W2,2)
    assert 11-1>=10
    assert (1<<10)*(1+12)>(1<<12) and (1<<10)*(1+13)>(1<<13)
    assert (1<<10)*(1+14)<=(1<<14)
    out={'pass':4582,'allowed_carriers':{'line_stars':40,'protected_edges':240,'total_distinct':280},
      'one_erasure':{'exact_minimum_channels':11,'lower_bound':'n-1>=10','witness':W1,'minimum_nonzero_functional_support':2,'functional_weight_profile':dict(sorted(p1.items()))},
      'two_erasures':{'exact_minimum_channels':14,'lower_bound':'[n,10,d>=3] plus Hamming bound excludes n=12,13','witness':W2,'minimum_nonzero_functional_support':3,'functional_weight_profile':dict(sorted(p2.items()))},
      'interpretation':'Parity anchoring is distributed across several line-stars and edge carriers; no single center line-star is a coloop of the robust readout.',
      'theorem':'Within the 280 natural protected carriers, 11 channels are necessary and sufficient to survive any one loss, and 14 are necessary and sufficient to survive any two arbitrary losses.',
      'boundary':'These are exact binary carrier/readout erasure bounds, not hardware fault-tolerance thresholds.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
