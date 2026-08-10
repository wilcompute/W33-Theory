#!/usr/bin/env python3
"""Pass 4806 bonkers — each GQ K5 fiber is a punctured ternary Golay code.

Pass4802 found the local ten-triangle dual kernel K=[10,6,4]_3 with enumerator
1+60z^4+144z^5+60z^6+240z^7+180z^8+20z^9+24z^10.
This producer does not identify K from those parameters alone.  It constructs a
basis of K, exhausts all 3^6 linear one-coordinate extensions, and proves:
  * exactly four nonzero functionals (two projective directions) raise d to 5;
  * every such extension is [11,6,5]_3 with the perfect ternary Golay enumerator;
  * adjoining representatives of both projective directions gives a self-dual
    [12,6,6]_3 code with the extended ternary Golay enumerator.
Thus the local code is explicitly a puncture of ternary Golay.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4806_LOCAL_TERNARY_GOLAY.json'

def rank_mod(M,p=3):
    A=np.array(M,dtype=int)%p;r=0
    for c in range(A.shape[1]):
        s=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if s is None:continue
        A[[r,s]]=A[[s,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

def nullspace_mod(M,p=3):
    A=np.array(M,dtype=int)%p;m,n=A.shape;r=0;piv=[]
    for c in range(n):
        s=next((i for i in range(r,m) if A[i,c]),None)
        if s is None:continue
        A[[r,s]]=A[[s,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv];B=[]
    for f in free:
        x=np.zeros(n,dtype=int);x[f]=1
        for i,c in enumerate(piv):x[c]=(-A[i,f])%p
        B.append(x)
    return np.array(B,dtype=int)

def main()->int:
    triples=list(itertools.combinations(range(5),3));M=np.zeros((5,10),dtype=int)
    for j,T in enumerate(triples):M[list(T),j]=1
    assert rank_mod(M,3)==4
    G=nullspace_mod(M,3);assert G.shape==(6,10)
    msgs=np.array(list(itertools.product(range(3),repeat=6)),dtype=int)
    C=(msgs@G)%3;basewt=np.count_nonzero(C,axis=1)
    wd=Counter(map(int,basewt));assert wd==Counter({0:1,4:60,5:144,6:60,7:240,8:180,9:20,10:24})
    good=[]
    for a in itertools.product(range(3),repeat=6):
        if not any(a):continue
        aa=np.array(a,dtype=int);ec=(msgs@aa)%3;ew=basewt+(ec!=0)
        if min(ew[1:])>=5:
            ewd=Counter(map(int,ew));assert ewd==Counter({0:1,5:132,6:132,8:330,9:110,11:24})
            good.append(aa)
    assert len(good)==4
    scalar_pairs=[]
    for i,j in itertools.combinations(range(4),2):
        if np.array_equal(good[j],(2*good[i])%3):scalar_pairs.append((i,j))
    assert len(scalar_pairs)==2 and {x for p in scalar_pairs for x in p}==set(range(4))
    # Choose one representative from each projective direction.
    a=good[scalar_pairs[0][0]];b=good[scalar_pairs[1][0]]
    E=np.column_stack([G,a,b])%3;assert rank_mod(E,3)==6 and np.all((E@E.T)%3==0)
    EC=(msgs@E)%3;ewd=Counter(map(int,np.count_nonzero(EC,axis=1)))
    assert ewd==Counter({0:1,6:264,9:440,12:24})
    out={'pass':4806,'local_fiber_code':'[10,6,4]_3','local_weight_enumerator':dict(sorted(wd.items())),
      'distance5_extension_functionals':4,'projective_extension_directions':2,
      'one_coordinate_extension':'[11,6,5]_3 perfect ternary Golay','one_coordinate_weight_enumerator':{'0':1,'5':132,'6':132,'8':330,'9':110,'11':24},
      'two_coordinate_extension':'[12,6,6]_3 extended ternary Golay','two_coordinate_self_dual':True,
      'two_coordinate_weight_enumerator':dict(sorted(ewd.items())),
      'theorem':'The ten triangle coordinates of every GQ(4,2) K5 carry an explicit punctured ternary Golay code G10=[10,6,4]_3. Exactly two projective extension directions recover G11=[11,6,5]_3, and adjoining both yields the self-dual extended ternary Golay G12=[12,6,6]_3.',
      'boundary':'The identification is established by explicit extension and self-duality/weight checks, not by the [10,6,4] parameters or enumerator alone. No Mathieu-group embedding into the global W33 action is claimed here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
