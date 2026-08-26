#!/usr/bin/env python3
"""Pass10421-10428: the two appearances of 64 are structurally different unless a nontrivial map is built.

Gamma16 side.
The adjacency code C is the self-dual [16,8,4] code from Pass10369-10376.  Its 64
weight-six codewords form the shell W6.  Translate W6 by a base word w0 and compute the
linear span over F2.  The span has dimension SEVEN, not six.  Thus W6 is not an affine
F2^6 despite having 64 elements.  The XOR-distance distribution from any base word is
0^1,4^9,8^51,12^3.

Its full weight enumerator
  1+12y^4+64y^6+102y^8+64y^10+12y^12+y^16
is the classical unique singly-even self-dual [16,8,4] code d_8^{2+}.

Canonical-V2 side.
Nebe--Parker define, for a good sublattice N and nonzero f+N, 24 antipodal pairs of
minimal vectors {+-v_i} in that coset and

  B(N,f)={(v_i+v_j+v_k)+2Lambda}.

Orbit 7 has profile 64^4095, so |B(V2,f)|=64 for every nonzero f.  Each bad vector lies
in the same affine coset f+V2 because three copies of f add to f in characteristic two.
The published profile does NOT assert B(V2,f) is an affine 6-flat.

Conclusion: 64=64 alone supplies no objectwise bridge.  In particular the most obvious
six-bit-flat identification is falsified on the Gamma16 side.  A genuine bridge must
compute one B(V2,f) and compare its addition/distance/group-action invariants.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10421_10428_GAMMA64_VS_V2_BAD64.json'
VERT=[(r,c) for r in range(4) for c in range(4)];IDX={v:i for i,v in enumerate(VERT)}
S=[(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)]
def rank2(M):
    A=np.array(M,dtype=np.uint8)&1;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
    return r
def main():
    A=np.zeros((16,16),dtype=np.uint8)
    for v in VERT:
        for s in S:
            w=((v[0]+s[0])%4,(v[1]+s[1])%4);A[IDX[v],IDX[w]]=1
    basis=[];r=0
    for x in A:
        T=np.vstack(basis+[x]) if basis else x[None,:];rr=rank2(T)
        if rr>r:basis.append(x.copy());r=rr
    assert len(basis)==8
    words=[]
    for mask in range(256):
        x=np.zeros(16,dtype=np.uint8)
        for j,b in enumerate(basis):
            if (mask>>j)&1:x^=b
        words.append(x)
    hist=Counter(int(x.sum()) for x in words)
    assert dict(sorted(hist.items()))=={0:1,4:12,6:64,8:102,10:64,12:12,16:1}
    W6=[x for x in words if int(x.sum())==6];assert len(W6)==64
    w0=W6[0];D=np.vstack([x^w0 for x in W6]);affdim=rank2(D);assert affdim==7
    dd=Counter(int((x^w0).sum()) for x in W6);assert dict(sorted(dd.items()))=={0:1,4:9,8:51,12:3}
    out={
      'schema':'w33.pass10421_10428.gamma64_vs_v2_bad64.v1','status':'PASS','passes':'10421-10428',
      'Gamma16_shell':{'code':'unique singly-even self-dual [16,8,4] code d_8^{2+} (classification input)','weight6_size':64,'affine_hull_dimension':affdim,'is_affine_F2_6':False,'xor_distance_from_base':{str(k):v for k,v in sorted(dd.items())}},
      'V2_bad_set':{'definition':'B(N,f)={(v_i+v_j+v_k)+2Lambda} from the 24 antipodal minimal-vector pairs in f+N','orbit7_profile':'64^4095','size_for_each_nonzero_f':64,'ambient':'single affine coset f+V2 because 3f=f mod V2','affine_flat_status':'NOT asserted by Nebe-Parker and not inferred here'},
      'no_go':'The raw equality 64=64 cannot identify the Gamma16 weight-6 shell with B(V2,f). In particular, any proposed bridge that treats both as affine F2^6 flats is false because the Gamma16 shell has affine hull dimension 7.',
      'next_exact_test':'Construct one orbit-7 B(V2,f) in compatible Leech coordinates and compare affine hull dimension, XOR-distance multiset, stabilizer orbits, and any quadratic/Hermitian invariants to the frozen Gamma16 shell.',
      'boundary':'Gamma16 calculations are exhaustive. The d_8^{2+} naming uses the classical classification of binary self-dual length-16 codes. The Nebe-Parker bad-set definition/profile is external prior art; no uncomputed affine property is assigned to B(V2,f).'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Gamma64_affdim':7,'xor_dist':dict(sorted(dd.items())),'V2_bad64':'requires direct construction'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
