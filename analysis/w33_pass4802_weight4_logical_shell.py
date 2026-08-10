#!/usr/bin/env python3
"""Pass 4802 — complete weight-4 logical shell of the intrinsic qutrit CSS code.

For the GQ(4,2) point/triangle incidence matrix B, Pass4800 proved
C=row_3(B)=[270,44,18]_3 and d(C^perp)=4.  This producer classifies every
projective weight-4 word of C^perp.  Pair-sum hashing enumerates all four-column
relations over F3 exactly; no group-orbit assumption is used.

The shell is entirely local to the 27 maximal K5 lines.  Each ten-triangle
fiber has 30 projective minimum relations (60 nonzero codewords), split under
the displayed geometric S5 action as 5+10+15.  Globally this is 135+270+405
projective words, 810 in total (1620 including nonzero scalar multiples).
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4802_WEIGHT4_LOGICAL_SHELL.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x): return tuple((x>>i)&1 for i in range(6))

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

def geometry():
    qp=[x for x in range(1,64) if Qm(bits(x))==0];assert len(qp)==27
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(ql)==45
    K5=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];assert len(set(K5))==27 and {len(C) for C in K5}=={5}
    triangles=sorted({tuple(sorted(T)) for C in K5 for T in itertools.combinations(C,3)});assert len(triangles)==270
    parent={tuple(sorted(T)):i for i,C in enumerate(K5) for T in itertools.combinations(C,3)}
    B=np.zeros((45,270),dtype=int)
    for j,T in enumerate(triangles):B[list(T),j]=1
    assert rank_mod(B,3)==44 and not np.any((B@B.T)%3)
    return K5,triangles,parent,B

def main()->int:
    K5,T,parent,B=geometry();cols=[tuple(int(x) for x in B[:,j]) for j in range(270)]
    pair=defaultdict(list)
    for i,j in itertools.combinations(range(270),2):
        ci,cj=cols[i],cols[j]
        for a in (1,2):
            for b in (1,2):
                key=tuple((a*ci[t]+b*cj[t])%3 for t in range(45))
                pair[key].append((i,j,a,b))
    rels=set()
    for key,A in pair.items():
        neg=tuple((-x)%3 for x in key)
        if neg not in pair:continue
        for i,j,a,b in A:
            for k,l,c,d in pair[neg]:
                if len({i,j,k,l})!=4:continue
                co={i:a,j:b,k:c,l:d};idx=tuple(sorted(co));v=tuple(co[x] for x in idx)
                if v[0]==2:v=tuple((2*x)%3 for x in v)
                rels.add((idx,v))
    assert len(rels)==810
    classes=Counter();local_counts=Counter()
    for idx,v in rels:
        tris=[set(T[i]) for i in idx];pids={parent[T[i]] for i in idx};assert len(pids)==1
        union=set().union(*tris);deg=Counter(x for S in tris for x in S)
        n1=v.count(1);n2=4-n1;split=tuple(sorted((n1,n2)))
        feature=(split,len(union),tuple(sorted(Counter(deg.values()).items())))
        classes[feature]+=1;local_counts[next(iter(pids))]+=1
    assert set(local_counts.values())=={30}
    # The three geometric classes are independent of coordinate ordering.
    wanted={
      ((0,4),4,((3,4),)):135,
      ((1,3),5,((2,3),(3,2))):270,
      ((2,2),5,((2,4),(4,1))):405,
    }
    assert classes==wanted
    # Verify the complete local [10,6,4]_3 kernel enumerator on one K5.
    C=K5[0];ids=[T.index(tuple(sorted(t))) for t in itertools.combinations(C,3)]
    Bloc=B[list(C)][:,ids];assert rank_mod(Bloc,3)==4
    wd=Counter()
    for x in itertools.product(range(3),repeat=10):
        a=np.array(x,dtype=int)
        if np.all((Bloc@a)%3==0):wd[int(np.count_nonzero(a))]+=1
    assert wd==Counter({0:1,4:60,5:144,6:60,7:240,8:180,9:20,10:24})
    out={
      'pass':4802,'quantum_code':'[[270,182,4]]_3','projective_weight4_logicals':810,
      'nonzero_scalar_weight4_logicals':1620,'all_weight4_words_are_single_K5_local':True,
      'projective_shell_split':{'four_points_all_same':135,'five_points_3plus1':270,'five_points_2plus2':405},
      'per_K5_projective_minimum_words':30,'K5_count':27,
      'local_kernel':'[10,6,4]_3','local_weight_enumerator':dict(sorted(wd.items())),
      'theorem':'Every minimum logical operator of the intrinsic qutrit CSS code is supported inside exactly one GQ(4,2) K5 fiber. The 810 projective weight-4 words split 135+270+405, i.e. 5+10+15 per K5; including scalar multiples gives 1620 nonzero weight-4 dual words.',
      'boundary':'The 5+10+15 split is the explicit geometric S5 split of the displayed K5 model. Identification of the local [10,6,4]_3 code with punctured ternary Golay is handled separately in Pass4806, not inferred from parameters alone.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
