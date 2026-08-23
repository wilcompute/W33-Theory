#!/usr/bin/env python3
"""Pass8489-8496: E7 root pairs are literally the 63 three-qubit Pauli classes.

Fix one E8 root.  Its 126 orthogonal roots form E7.  Reduce the E7 lattice mod 2:
the Gram has a one-dimensional radical, and the 63 antipodal root pairs occupy all
63 nonzero classes of the six-dimensional symplectic quotient.  Root inner-product
parity is the quotient symplectic form; the 336 nonorthogonal root-pair triangles
are exactly the 336 closed anticommuting Pauli triangles of Pass8241.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np, sympy as sp
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8489_8496_E7_PAULI_ROOTPAIR_BRIDGE.json'
S=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]

def roots():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (2,-2):
            for b in (2,-2):
                v=[0]*8;v[i]=a;v[j]=b;R.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:R.append(tuple(s))
    assert len(R)==240;return R

def rank2(A):
    A=np.array(A,dtype=np.uint8)%2;m,n=A.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
    return r

def key(r):
    r=tuple(map(int,r));return min(r,tuple(-x for x in r))
def refl(x,r):
    q=sum(a*b for a,b in zip(x,r));assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))

def main():
    R=roots();r0=np.array(S[1]);E7=[np.array(r,dtype=int) for r in R if int(np.dot(r,r0))==0];assert len(E7)==126
    A=sp.Matrix(np.array(S,dtype=int).T);G=np.array([[np.dot(x,y)//4 for y in S] for x in S],dtype=int)
    # E7 coefficient lattice: condition 2*c1-c3=0 in these simple-root coordinates.
    B=np.zeros((8,7),dtype=int)
    for j,i in enumerate([0,2,4,5,6,7]):B[i,j]=1
    B[1,6]=1;B[3,6]=2
    GE=B.T@G@B;assert round(np.linalg.det(GE))==2
    Ai=A.inv();mods=defaultdict(list)
    for r in E7:
        c=Ai*sp.Matrix(r.tolist());assert all(x.q==1 for x in c);c=np.array([int(x) for x in c])
        d=np.array([c[0],c[2],c[4],c[5],c[6],c[7],c[1]],dtype=int);assert np.array_equal(B@d,c)
        mods[tuple((d%2).tolist())].append(tuple(map(int,r)))
    assert len(mods)==63 and set(map(len,mods.values()))=={2}
    G2=GE%2;assert rank2(G2)==6 and not np.any(G2[-1])
    rad=np.array([0,0,0,0,0,0,1],np.uint8);assert tuple(rad) not in mods
    assert all(tuple((np.array(v,np.uint8)^rad).tolist()) not in mods for v in mods)
    J=G2[:6,:6].astype(np.uint8);assert rank2(J)==6
    qmap={tuple(v[:6]):v for v in mods};assert len(qmap)==63
    Q=sorted(qmap);rep={q:np.array(mods[qmap[q]][0]) for q in Q}
    tri=set()
    for a,b in itertools.combinations(Q,2):
        av=np.array(a,np.uint8);bv=np.array(b,np.uint8);lhs=(int(np.dot(rep[a],rep[b]))//4)%2;rhs=int(av@J@bv)%2
        assert lhs==rhs
        if rhs:
            c=tuple((av^bv).tolist());assert c in qmap;tri.add(frozenset((a,b,c)))
    assert len(tri)==336 and set(Counter(x for T in tri for x in T).values())=={16}
    pairs=sorted({key(r) for r in E7});pi={p:i for i,p in enumerate(pairs)};gens=[];Gg=PermutationGroup([Permutation(list(range(63)))])
    growth=[]
    for r in E7:
        p=Permutation([pi[key(refl(x,r))] for x in pairs]);H=PermutationGroup(gens+[p])
        if int(H.order())>int(Gg.order()):
            gens.append(p);Gg=H;growth.append(int(H.order()))
            if int(H.order())==1451520:break
    assert int(Gg.order())==1451520 and len(Gg.orbits())==1
    out={'schema':'w33.pass8489_8496.e7_pauli_rootpair_bridge.v1','status':'PASS','passes':'8489-8496',
      'E7_roots':126,'antipodal_root_pairs':63,'E7_mod2_dimension':7,'radical_dimension':1,'symplectic_quotient_dimension':6,
      'root_pairs_cover_all_nonzero_quotient_classes':True,'pairing_identity':'(r.s)/4 mod 2 = omega(q(r),q(s))',
      'closed_nonorthogonal_triangles':336,'triangles_through_each_point':16,
      'reflection_group_on_63_pairs':{'order':1451520,'identification':'Sp6(2)','generator_order_growth':growth},
      'theorem':'The 63 E7 antipodal root pairs are an explicit coordinatization of the 63 nonzero three-qubit Pauli classes. Their 336 nonorthogonal linear triples are exactly the 336 closed anticommuting Pauli triangles / W(3,2) sectors of the Leech W(5,2) carrier.',
      'claim_boundary':'Exact lattice-mod-2/finite-symplectic identification; no physical subsystem claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','points':63,'triangles':336,'group':1451520}))
if __name__=='__main__':main()
