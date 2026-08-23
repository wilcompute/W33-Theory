#!/usr/bin/env python3
"""Pass8417-8424: exact F2-module structure of the C2^8 normal subgroup in the 64-leaf residue controller.

Pass8301 proves 1 -> C2^8 -> G64 -> S3^3 -> 1.  This pass freezes a generating
set for the actual conjugation image of G64/C2^8 on C2^8 and analyzes the module
without rebuilding the 64-leaf geometry.

The six 8x8 binary matrices below were extracted from the exact Pass8301 action.
They generate the order-216 quotient and are a compact reproducible certificate.
"""
from __future__ import annotations
import collections,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8417_8424_64LEAF_BINARY_MODULE.json'
GENS=[
[[1,1,0,0,0,1,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,1,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]],
[[0,1,0,0,0,1,0,0],[1,0,1,0,0,1,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,1,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]],
[[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,1],[0,0,0,1,1,0,1,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,1]],
[[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,0,1,0,1,1],[0,0,0,1,0,0,0,1],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1]],
[[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,0,0],[1,1,0,0,0,1,0,0],[0,0,0,0,1,0,1,1],[0,0,0,1,1,0,1,0],[0,1,0,0,0,1,0,0],[0,0,0,1,1,0,0,1],[0,0,0,1,0,0,1,1]],
[[1,0,1,0,0,1,0,0],[0,1,0,0,0,1,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,1],[0,0,0,0,1,0,1,1],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]]
GENS=[np.array(x,dtype=np.uint8) for x in GENS]
def k(M):return bytes(np.asarray(M,dtype=np.uint8).ravel())
def closure(gens):
    I=np.eye(8,dtype=np.uint8);D={k(I):I};q=collections.deque([I])
    while q:
        A=q.popleft()
        for B in gens:
            C=(A@B)%2;z=k(C)
            if z not in D:D[z]=C;q.append(C)
    return list(D.values())
def vint(n):return np.array([(n>>i)&1 for i in range(8)],dtype=np.uint8)
def vkey(v):return sum(int(v[i])<<i for i in range(8))
def span_basis(vecs):
    rows=[]
    for vv in vecs:
        x=vv.copy()
        for b in rows:
            p=int(np.flatnonzero(b)[0])
            if x[p]:x^=b
        if x.any():
            p=int(np.flatnonzero(x)[0])
            for i,b in enumerate(rows):
                if b[p]:rows[i]=b^x
            rows.append(x);rows.sort(key=lambda z:int(np.flatnonzero(z)[0]))
    return tuple(vkey(x) for x in rows)
def order(M):
    I=np.eye(len(M),dtype=np.uint8);X=I.copy()
    for n in range(1,25):
        X=(X@M)%2
        if np.array_equal(X,I):return n
    raise AssertionError

def main():
    G=closure(GENS);assert len(G)==216
    oc=collections.Counter(order(x) for x in G)
    assert oc==collections.Counter({6:126,2:63,3:26,1:1})
    mods={}
    for n in range(1,256):
        b=span_basis([(g@vint(n))%2 for g in G]);mods[b]=mods.get(b,0)+1
    proper=[b for b in mods if len(b)<8]
    assert len(proper)==2 and sorted(len(b) for b in proper)==[4,4]
    assert sorted(mods[b] for b in proper)==[15,15] and next(v for b,v in mods.items() if len(b)==8)==225
    # In the frozen basis the two modules are coordinate blocks.
    blocks=[[0,1,2,5],[3,4,6,7]]
    assert {frozenset(1<<i for i in B) for B in blocks}=={frozenset(b) for b in proper}
    kernels=[];images=[]
    for B in blocks:
        C=[i for i in range(8) if i not in B];im={};ker=[]
        for g in G:
            assert not g[np.ix_(C,B)].any()
            r=g[np.ix_(B,B)];im[k(r)]=r
            if np.array_equal(r,np.eye(4,dtype=np.uint8)):ker.append(g)
        assert len(im)==36 and len(ker)==6
        assert collections.Counter(order(x) for x in im.values())==collections.Counter({2:15,6:12,3:8,1:1})
        assert collections.Counter(order(x) for x in ker)==collections.Counter({2:3,3:2,1:1})
        kernels.append(ker);images.append(im)
    K0={k(x) for x in kernels[0]};K1={k(x) for x in kernels[1]}
    assert len(K0&K1)==1
    assert all(np.array_equal((a@b)%2,(b@a)%2) for a in kernels[0] for b in kernels[1])
    product=[(a@b)%2 for a in kernels[0] for b in kernels[1]];assert len({k(x) for x in product})==36
    K2=[g for g in G if all(np.array_equal((g@h)%2,(h@g)%2) for h in product)]
    assert len(K2)==6 and collections.Counter(order(x) for x in K2)==collections.Counter({2:3,3:2,1:1})
    out={
      'schema':'w33.pass8417_8424.64leaf_binary_module.v1','status':'PASS','passes':'8417-8424',
      'quotient_order':216,'quotient_identification':'S3^3','conjugation_module':'F2^8 = C2^8',
      'proper_nonzero_submodules':2,'decomposition_dimensions':[4,4],'irreducible':True,
      'frozen_coordinate_blocks':blocks,
      'each_4D_module':{'image_order':36,'image_identification':'S3 x S3','kernel_order':6,'kernel_identification':'S3'},
      'three_factor_recovery':'the two module kernels are disjoint commuting S3 factors; the centralizer of their product is the third S3 factor',
      'tensor_description':'after labeling the kernel factors S3_1,S3_2 and the common active factor S3_3, M4 ~= V2(S3_2) tensor V2(S3_3) and M4_prime ~= V2(S3_1) tensor V2(S3_3)',
      'theorem':'The C2^8 residue layer is two irreducible four-dimensional tensor channels sharing one S3 triality factor. It is not a sum of four natural two-dimensional S3 modules.',
      'claim_boundary':'Exact binary representation theorem for the finite 64-leaf residue controller; the shared S3 is an algebraic coupling channel, not a physical interaction claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','module':'4+4','shared_factor':'S3'}))
if __name__=='__main__':main()
