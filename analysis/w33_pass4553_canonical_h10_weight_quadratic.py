#!/usr/bin/env python3
"""Pass 4553 -- canonical parity/pairing derivation of the H10 1|8|1 filtration.

The previous cyclic-submodule census found 0<1<9<10.  This pass reconstructs
that filtration from intrinsic protected geometry.  Coefficient parity pi gives
V9=ker(pi), Pass 4541 gives pi(x)=B(x,j) for the unique fixed all-ones vector j,
so V9=j^perp.  The quotient V8=V9/<j> carries the explicit quadratic form
    q8([x]) = wt(x)/4 mod 2.
It is well defined under x~x+j and its polarization is exactly B.  Exhausting
V9 gives 136 singular classes (including zero) and 120 anisotropic classes,
hence plus type O^+(8,2).  Middle irreducibility remains inherited from the
independent Pass-4477/4496 certificate; no cyclic census is used to locate the
1 and 9 layers themselves.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4553_CANONICAL_H10_WEIGHT_QUADRATIC.json'
COLS=[0,1,2,3,4,5,7,8,10,11]

def vm(v): return sum(int(b)<<i for i,b in enumerate(v) if b)
def qwt(x): return (int(np.asarray(x,dtype=np.uint8).sum())//4)&1

def main():
    *_x,A=build_geometry()[:6]
    assert rank2(A)==10
    M=A[:,COLS];assert rank2(M)==10
    image={}
    for m in range(1<<10):
        b=np.zeros(40,dtype=np.uint8);x=np.zeros(40,dtype=np.uint8)
        for k,c in enumerate(COLS):
            if (m>>k)&1:b[c]=1;x^=A[:,c]
        image[vm(x)]=b
    assert len(image)==1024
    j=np.ones(40,dtype=np.uint8);jm=vm(j);assert jm in image
    V9=[]
    for xm,b in image.items():
        if int(b.sum())%2==0:
            x=np.array([(xm>>i)&1 for i in range(40)],dtype=np.uint8);V9.append((xm,x,b))
    assert len(V9)==512
    weights=Counter(int(x.sum()) for _,x,_ in V9)
    assert weights==Counter({20:240,16:135,24:135,0:1,40:1})
    # q8 is constant on the j-pairs and polarizes to the protected alternating form b^T A c.
    for xm,x,b in V9:
        assert qwt(x)==qwt(x^j)
    for xm,x,b in V9:
        for ym,y,c in V9:
            lhs=qwt(x^y)^qwt(x)^qwt(y)
            rhs=int((b@(A@c%2))%2)
            assert lhs==rhs
    seen=set();qcount=Counter()
    for xm,x,b in V9:
        if xm in seen:continue
        partner=xm^jm;assert partner in image
        seen|={xm,partner};qcount[qwt(x)]+=1
    assert len(seen)==512 and qcount==Counter({0:136,1:120})
    c4541=json.loads((ROOT/'data/PART_W33_PASS4541_PARITY_FIXED_VECTOR_PAIRING.json').read_text())
    assert c4541['module_chain']=='0 < <1> < 1^perp < H10 with dimensions 0<1<9<10'
    out={'pass':4553,'canonical_chain':'0 < <j> < j^perp=V9 < H10','dimensions':[0,1,9,10],
      'fixed_vector':'j=all-ones; uniqueness inside H10 follows from transitivity of the ambient 40-line permutation action',
      'parity_pairing':'pi(x)=B(x,j), hence V9=ker(pi)=j^perp',
      'middle_quotient':{'space':'V8=V9/<j>','dimension':8,'quadratic_form':'q8([x])=wt(x)/4 mod2','well_defined_under_complement':True,'polar_form':'protected alternating B','type':'O+(8,2)','singular_including_zero':136,'anisotropic':120},
      'V9_ambient_weights':{str(k):v for k,v in sorted(weights.items())},
      'irreducibility_boundary':'The intrinsic construction locates the 1 and 9 layers without cyclic-submodule search. Irreducibility of V8 is inherited from independent Pass 4477/4496 exhaustive certificates.',
      'theorem':'The protected 1|8|1 filtration is canonically the fixed line, its symplectic perpendicular, and the full H10; the middle factor has an explicit plus-type weight quadratic.',
      'boundary':'Finite binary module geometry only; q8 is not a physical energy or charge.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
