#!/usr/bin/env python3
"""Pass 4584 (outside box) -- the 135x120 O8+ cross-shell incidence is a [120,9,56] code.

Rows are singular protected classes, columns anisotropic classes, and entry 1
means polar orthogonality.  The binary row code is self-orthogonal of dimension
9 with enumerator 1+255 z^56+255 z^64+z^120; its all-one quotient is another
8-dimensional realization of the protected orthogonal geometry.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4584_CROSS_SHELL_INCIDENCE_CODE.json'

def rbasis(vecs):
    piv={}
    for x in map(int,vecs):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())
def span(B):
    S=[0]
    for b in B:S += [x^b for x in list(S)]
    return S

def main()->int:
    vals=build_geometry();A=np.asarray(vals[5],dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if A[i,k]]
    B9=rbasis([cols[i]^cols[k] for i,k in edges]);assert len(B9)==9
    V=[0]
    for b in B9:V += [x^b for x in list(V)]
    reps=sorted({min(x,x^j) for x in V})
    def rep(x):return min(int(x),int(x)^j)
    def q(x):return (rep(x).bit_count()//4)&1
    def polar(x,y):return q(x)^q(y)^q(rep(x)^rep(y))
    sing=[x for x in reps if x and q(x)==0];anis=[x for x in reps if x and q(x)==1]
    assert (len(sing),len(anis))==(135,120)
    R=np.zeros((135,120),dtype=np.uint8)
    for i,s in enumerate(sing):
        for k,a in enumerate(anis):R[i,k]=polar(s,a)==0
    assert set(map(int,R.sum(1)))=={56} and set(map(int,R.sum(0)))=={63}
    rowints=Counter();colints=Counter()
    for i,k in itertools.combinations(range(135),2):rowints[(polar(sing[i],sing[k]),int(np.dot(R[i],R[k])))] += 1
    for i,k in itertools.combinations(range(120),2):colints[(polar(anis[i],anis[k]),int(np.dot(R[:,i],R[:,k])))] += 1
    assert rowints==Counter({(0,24):4725,(1,28):4320})
    assert colints==Counter({(0,31):3780,(1,27):3360})
    RR=(R@R.T)%2;CC=(R.T@R)%2
    assert not RR.any() and np.array_equal(CC,np.ones((120,120),dtype=np.uint8))
    rows=[]
    for row in R:
        m=0
        for k,b in enumerate(row):
            if b:m|=1<<k
        rows.append(m)
    B=rbasis(rows);assert len(B)==9
    C=span(B);wd=Counter(x.bit_count() for x in C)
    assert wd==Counter({0:1,56:255,64:255,120:1}) and (1<<120)-1 in C
    out={'pass':4584,'incidence':{'shape':[135,120],'row_weight':56,'column_weight':63,
      'row_pair_intersections':{'polar0':24,'polar1':28},'column_pair_intersections':{'polar0':31,'polar1':27}},
      'binary':{'rank':9,'RRt':'zero','RtR':'all-ones J120','row_code':'[120,9,56] self-orthogonal','weight_enumerator':'1 + 255 z^56 + 255 z^64 + z^120','contains_all_ones':True,'all_ones_quotient_dimension':8},
      'theorem':'Singular-anisotropic orthogonality in the W33-derived O+(8,2) shell produces a new self-orthogonal [120,9,56] binary code whose fixed-word quotient is 8-dimensional.',
      'boundary':'This is an incidence-code realization, not a physical measurement code or an identification with the apartment code.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
