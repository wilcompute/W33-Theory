#!/usr/bin/env python3
"""Pass10369-10376: the Gamma16 adjacency rows form an exact binary [16,8,4] self-dual code.

Gamma16 is the canonical 16-point Hermitian-isotropic W33 residue / four-common-line
spread-pair graph from Pass10169-10176 and Pass10321-10328.  In the Cayley coordinates

  V = C4 x C4,
  S = {(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)},

let A be its 16x16 adjacency matrix.  This pass treats A over F2.

Exact facts:
* A^2=0 over F2, hence the row code is self-orthogonal;
* rank_F2(A)=8, so the row code is self-dual [16,8];
* the minimum nonzero weight is 4;
* weight enumerator:
    1 + 12 y^4 + 64 y^6 + 102 y^8 + 64 y^10 + 12 y^12 + y^16.
* the full graph automorphism group S4 x D8 (order 192), acting as arbitrary row-fiber
  permutations and dihedral column permutations, preserves the code.  Weight-6 and
  weight-10 words each split as 16+48 under this group.

The repeated number 64 is recorded as a target for the canonical V2 good-sublattice
profile 64^4095.  No identification of the two 64-sets is made here.
"""
from __future__ import annotations
from collections import Counter
import itertools,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10369_10376_GAMMA16_SELF_DUAL_CODE.json'

VERT=[(r,c) for r in range(4) for c in range(4)]
IDX={v:i for i,v in enumerate(VERT)}
S=[(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)]

def rank2(M):
    M=np.array(M,dtype=np.uint8)&1;r=0
    for c in range(M.shape[1]):
        q=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
        if q is None:continue
        if q!=r:M[[r,q]]=M[[q,r]]
        for i in range(M.shape[0]):
            if i!=r and M[i,c]:M[i]^=M[r]
        r+=1
    return r

def adjacency():
    A=np.zeros((16,16),dtype=np.uint8)
    for v in VERT:
        for s in S:
            w=((v[0]+s[0])%4,(v[1]+s[1])%4)
            A[IDX[v],IDX[w]]=1
    assert np.array_equal(A,A.T) and set(A.sum(axis=1).tolist())=={6}
    return A

def row_basis(A):
    b=[];r=0
    for x in A:
        T=np.vstack(b+[x]) if b else x.reshape(1,-1)
        rr=rank2(T)
        if rr>r:b.append(x.copy());r=rr
    return b

def codewords(basis):
    out=[]
    for mask in range(1<<len(basis)):
        x=np.zeros(16,dtype=np.uint8)
        for j,b in enumerate(basis):
            if (mask>>j)&1:x^=b
        out.append(x)
    return out

def aut_perms():
    # Full Aut(Gamma16)=S4 x D8 in the canonical fiber coordinates.
    perms=[]
    for sigma in itertools.permutations(range(4)):
        for eps in (1,-1):
            for k in range(4):
                p=[]
                for r,c in VERT:p.append(IDX[(sigma[r],(eps*c+k)%4)])
                perms.append(tuple(p))
    assert len(set(perms))==192
    return sorted(set(perms))

def main():
    A=adjacency()
    assert not np.any((A@A)&1)
    rk=rank2(A);assert rk==8
    basis=row_basis(A);assert len(basis)==8
    words=codewords(basis);assert len(words)==256
    hist=Counter(int(w.sum()) for w in words)
    want={0:1,4:12,6:64,8:102,10:64,12:12,16:1};assert dict(sorted(hist.items()))==want
    assert min(k for k in hist if k)>0 and min(k for k in hist if k>0)==4
    # Self-dual because dim=8 in length16 and self-orthogonal.
    assert rank2(A)==16//2

    keys={tuple(w.tolist()):i for i,w in enumerate(words)}
    perms=aut_perms()
    assert all(np.array_equal(A[np.ix_(p,p)],A) for p in perms)
    unseen=set(range(len(words)));orbits=[]
    while unseen:
        seed=next(iter(unseen));w=words[seed];orb=set()
        for p in perms:
            y=np.zeros(16,dtype=np.uint8)
            for i,b in enumerate(w):
                if b:y[p[i]]=1
            orb.add(keys[tuple(y.tolist())])
        unseen-=orb;orbits.append(orb)
    orbit_summary=sorted((int(words[next(iter(o))].sum()),len(o)) for o in orbits)
    assert [s for w,s in orbit_summary if w==6]==[16,48]
    assert [s for w,s in orbit_summary if w==10]==[16,48]
    assert sum(s for w,s in orbit_summary if w==8)==102

    out={
      'schema':'w33.pass10369_10376.gamma16_self_dual_code.v1','status':'PASS','passes':'10369-10376',
      'Gamma16':{'vertices':16,'degree':6,'model':'Cay(C4 x C4,S)','S':[list(x) for x in S],'Aut':'S4 x D8','Aut_order':192},
      'binary_adjacency_code':{'generator':'16 adjacency rows over F2','A_squared_mod2_zero':True,'rank':rk,'parameters':'[16,8,4]','self_orthogonal':True,'self_dual':True,'weight_enumerator':{str(k):v for k,v in sorted(want.items())}},
      'Aut_orbits_on_codewords':{'weight_size_pairs':[[w,s] for w,s in orbit_summary],'weight6':'16+48','weight10':'16+48'},
      '64_target':{'Gamma16_weight6_words':64,'Gamma16_weight10_words':64,'canonical_V2_good_profile':'64^4095','status':'count-pattern target only; no map asserted'},
      'theorem':'The adjacency row space of the canonical 16-point Hermitian/spread-intersection graph Gamma16 is a binary self-dual [16,8,4] code with weight enumerator 1+12y^4+64y^6+102y^8+64y^10+12y^12+y^16. Its full S4 x D8 automorphism group preserves the code and splits both 64-word weight shells into 16+48.',
      'boundary':'Exact finite computation in the canonical Cayley model. The equality 64 with the V2 good-sublattice profile is deliberately not promoted to an objectwise identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','parameters':'[16,8,4]','weights':dict(sorted(hist.items())),'orbits':orbit_summary}))
    return 0
if __name__=='__main__':raise SystemExit(main())
