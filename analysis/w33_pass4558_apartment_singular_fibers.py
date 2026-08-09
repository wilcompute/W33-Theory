#!/usr/bin/env python3
"""Pass 4558 (outside box) -- apartments are a uniform 12-fold lift of O+(8,2) singular classes.

Project every one of the 1620 W33 apartments through b -> A_* b.  Exactly 135
distinct protected vectors occur, all of ambient weight 16, each with twelve
apartment preimages.  Under Pass4553's quotient V8=V9/<j> and q8=wt/4 mod2,
these are precisely the 135 nonzero singular classes of O^+(8,2).

Inside each 12-apartment fiber, connect two apartments when they share one line.
Every fiber is K_{4,4,4}; disjointness partitions it into three groups of four.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4558_APARTMENT_SINGULAR_FIBERS.json'
def vm(v):return sum(int(b)<<i for i,b in enumerate(v) if b)
def main():
    vals=build_geometry();A=vals[5];aps=vals[7];assert len(aps)==1620
    fibers=defaultdict(list)
    for ap in aps:
        y=np.zeros(40,dtype=np.uint8)
        for i in ap:y^=A[:,i]
        assert int(y.sum())==16
        fibers[vm(y)].append(tuple(ap))
    assert len(fibers)==135 and Counter(map(len,fibers.values()))==Counter({12:135})
    profile=Counter()
    for F in fibers.values():
        G=np.zeros((12,12),dtype=np.uint8);ints=Counter()
        for i,j in itertools.combinations(range(12),2):
            z=len(set(F[i])&set(F[j]));ints[z]+=1
            if z==1:G[i,j]=G[j,i]=1
        assert ints==Counter({1:48,0:18}) and set(map(int,G.sum(1)))=={8}
        # complement graph has exactly three K4 components -> G=K4,4,4.
        C=(np.ones((12,12),dtype=np.uint8)^np.eye(12,dtype=np.uint8)^G)
        unseen=set(range(12));comps=[]
        while unseen:
            s=min(unseen);Q=[s];S={s};unseen.remove(s)
            while Q:
                u=Q.pop()
                for v in list(unseen):
                    if C[u,v]:unseen.remove(v);S.add(v);Q.append(v)
            comps.append(S)
        assert sorted(map(len,comps))==[4,4,4]
        assert all(C[i,j] for S in comps for i,j in itertools.combinations(S,2))
        profile['K4,4,4']+=1
    c4553=json.loads((ROOT/'data/PART_W33_PASS4553_CANONICAL_H10_WEIGHT_QUADRATIC.json').read_text())
    assert c4553['middle_quotient']['singular_including_zero']==136
    out={'pass':4558,'apartments':1620,'protected_images':135,'image_weight':16,'uniform_fiber_size':12,
      'O8plus_identification':'The 135 weight-16 images give exactly one representative of every nonzero singular class in V8=V9/<j>; q8=16/4=0 mod2.',
      'fiber_graph':{'vertices':12,'adjacency':'apartments share exactly one line','graph':'K_{4,4,4}','degree':8,'edges':48,'disjoint_pairs':18,'complement_components':[4,4,4]},
      'all_fibers_same_type':profile['K4,4,4']==135,
      'theorem':'The 1620 apartments form a uniform 12-to-1 lift of the 135 nonzero O+(8,2) singular protected classes, and every lift fiber has intrinsic K4,4,4 intersection geometry.',
      'boundary':'This is a finite quotient/fiber theorem. The 12-fold lift is not a physical degeneracy or microscopic state count.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
