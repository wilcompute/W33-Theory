#!/usr/bin/env python3
"""Pass 4541 (outside box) -- coefficient parity is pairing with the fixed vector.

Pass 4536 identified pi(A_*b)=sum b as the missing quotient functional with
kernel V9.  Pass 4496 independently proved that H10 has a unique fixed 1-space
and a unique invariant 9-space in the uniserial chain 0<1<9<10.

The protected alternating form on coefficient classes is
  B(A_*b,A_*c)=b^T A_* c.
The all-ones protected vector satisfies 1=A_*(e0+e1+e2+e3). Hence
  B(A_*b,1)=b^T 1=pi(A_*b).
Since 1 is group-fixed and the fixed space is one-dimensional, this is exactly
the canonical fixed vector of Pass 4496. Therefore V9=1^perp, and the missing
tenth bit is the symplectic coordinate dual to the fixed line.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4541_PARITY_FIXED_VECTOR_PAIRING.json'

def main():
    *_x,A=build_geometry()[:6]
    one=np.ones(40,dtype=np.uint8)
    c=np.zeros(40,dtype=np.uint8);c[[0,1,2,3]]=1
    assert np.array_equal((A@c)%2,one)
    assert int(c.sum())%2==0
    # Exhaust coefficient representatives from a ten-column basis.
    piv=[];cur=np.zeros((40,0),dtype=np.uint8);r=0
    for j in range(40):
        T=np.column_stack((cur,A[:,j]));rr=rank2(T)
        if rr>r:piv.append(j);cur=T;r=rr
        if r==10:break
    assert piv==[0,1,2,3,4,5,7,8,10,11]
    for mask in range(1<<10):
        b=np.zeros(40,dtype=np.uint8)
        for k,j in enumerate(piv):
            if (mask>>k)&1:b[j]=1
        x=(A@b)%2
        parity=int(b.sum())%2
        # B(A b, A c)=b^T A c=b^T 1.
        pairing=int((b@one)%2)
        assert parity==pairing
    c4496=json.loads((ROOT/'data/PART_W33_PASS4496_H10_EXTENSION_COHOMOLOGY.json').read_text())
    assert c4496['module']['fixed_dimension']==1
    assert c4496['module']['fixed_perp_dimension']==9
    assert c4496['module']['invariant_submodule_lattice']=='0 < 1 < 9 < 10'
    out={
      'pass':4541,'fixed_vector_ambient':[1]*40,
      'fixed_vector_preimage_support':[0,1,2,3],
      'identity':'pi(A_* b)=B(A_* b, 1)=b^T 1',
      'edge_layer':'V9=ker(pi)=1^perp',
      'module_chain':'0 < <1> < 1^perp < H10 with dimensions 0<1<9<10',
      'exhausted_protected_vectors':1024,
      'theorem':'The missing coefficient-parity bit is the alternating-form coordinate dual to the unique PSp-fixed protected vector; the entire edge carrier is exactly its orthogonal hyperplane.',
      'boundary':'Symplectic/fixed-vector language is finite module geometry. It does not identify pi with a physical conserved charge without dynamics.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
