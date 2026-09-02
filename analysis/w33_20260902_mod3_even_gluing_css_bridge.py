#!/usr/bin/env python3
"""Tighten the characteristic-3 collapse: identify the glued even channel.

Previous exact certificates established:
  * St81^3 over Q has global PGSp outer multiplicity action diag(1,1,-1);
  * the three integral W33-building injection numerators reduce mod 3 to ranks
    81,81,81 with combined rank 162;
  * images 0 and 1 intersect in dimension 81, while image 2 is disjoint.

Thus the two outer-even rational channels have the same modular image.  Here we
reconstruct the maps, solve the exact source-coordinate intertwiner F over F3
between channel 0 and channel 1, and tie the common 81-space to the canonical
[[240,81,3]]_3 CSS logical Steinberg through their common W33 building-cycle
basis.  The outer-odd channel is checked to remain an independent 81-space.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260901_packet48_bt796_crossid as shell
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import mulvec
from w33_20260901_building_chain_injections import integer_cycle_basis, rank_mod, lcm_den

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_MOD3_EVEN_GLUING_CSS_BRIDGE.json'
P=3


def inv_mod(A,p):
    A=np.asarray(A,dtype=np.int64)%p;n=A.shape[0]; assert A.shape==(n,n)
    X=np.concatenate([A,np.eye(n,dtype=np.int64)],axis=1)%p;r=0
    for c in range(n):
        z=next(i for i in range(r,n) if X[i,c]%p)
        if z!=r:X[[r,z]]=X[[z,r]]
        X[r]=(X[r]*pow(int(X[r,c]),-1,p))%p
        for i in range(n):
            if i!=r and X[i,c]:X[i]=(X[i]-int(X[i,c])*X[r])%p
        r+=1
    assert np.array_equal(X[:,:n]%p,np.eye(n,dtype=np.int64)%p)
    return X[:,n:]%p


def independent_rows(A,p):
    B=np.asarray(A,dtype=np.int64).T.copy()%p;m,n=B.shape;r=0;piv=[]
    for c in range(n):
        z=next((i for i in range(r,m) if B[i,c]),None)
        if z is None:continue
        if z!=r:B[[r,z]]=B[[z,r]]
        B[r]=(B[r]*pow(int(B[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and B[i,c]:B[i]=(B[i]-int(B[i,c])*B[r])%p
        piv.append(c);r+=1
        if r==m:break
    return piv


def main():
    D=shell.build(); pts,wlines,charts,G=D['pts'],D['wlines'],D['charts'],D['G']
    F0=build_frame(); acts,rel,T,frame=F0['acts'],F0['rel'],F0['T'],list(F0['frame'])
    li={frozenset(L):i for i,L in enumerate(wlines)}
    @lru_cache(maxsize=None)
    def line_perm(gi):
        p=G[gi][0];return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def target_one(gi,y):
        c,e=divmod(y,40);return G[gi][2][c]*40+line_perm(gi)[e]
    gen_indices=[]
    for a in acts:
        hit=next(gi for gi in range(len(G)) if all(target_one(gi,y)==a[y] for y in (0,1,39,40,217,1079)))
        assert all(target_one(hit,y)==a[y] for y in range(1080));gen_indices.append(hit)

    chambers=[(p,e) for e,L in enumerate(wlines) for p in L];ci={x:i for i,x in enumerate(chambers)}
    Z,zden=integer_cycle_basis(40,40,chambers);assert zden==1 and Z.shape==(160,81)
    def source_one(gi,s):
        p,e=chambers[s];return ci[(G[gi][0][p],line_perm(gi)[e])]
    transport=[None]*160;H=[]
    for gi in range(len(G)):
        s=source_one(gi,0)
        if transport[s] is None:transport[s]=gi
        if s==0:H.append(gi)
    unseen=set(range(1080));orbits=[]
    while unseen:
        y=min(unseen);O={target_one(gi,y) for gi in H};unseen-=O;orbits.append(tuple(sorted(O)))
    orbits.sort(key=lambda O:(len(O),O[0]))
    zero=sp.zeros(59,1)
    def columns(O):return [tuple(sorted(target_one(transport[s],y) for y in O)) for s in range(160)]
    def selfgram(C):
        row=np.zeros(1080,dtype=np.int64)
        for col in C:
            if 0 in col:row[list(col)]+=1
        v=[None]*59
        for y,x in enumerate(row.tolist()):
            r=int(rel[0,y]);
            if v[r] is None:v[r]=x
            else:assert v[r]==x
        return sp.Matrix(v)
    Ys=[];meta=[]
    for k,Pj in enumerate(frame):
        found=None
        for oi,O in enumerate(orbits):
            C=columns(O);V=selfgram(C)
            if mulvec(Pj,mulvec(V,Pj,T),T)!=zero:found=(oi,C);break
        assert found is not None
        oi,C=found;den=lcm_den(Pj);coeff=np.array([int(den*q) for q in Pj],dtype=np.int64)
        Pnum=coeff[np.asarray(rel,dtype=np.int64)]
        A=np.zeros((1080,160),dtype=np.int64)
        for s,col in enumerate(C):A[:,s]=Pnum[:,list(col)].sum(axis=1)
        Y=(A@Z)%P;assert rank_mod(Y,P)==81
        Ys.append(Y);meta.append({'primitive':k,'sourceOrbit':oi,'denominator':int(den)})
    Y0,Y1,Y2=Ys
    assert rank_mod(np.concatenate([Y0,Y1],axis=1),P)==81
    assert rank_mod(np.concatenate([Y0,Y2],axis=1),P)==162

    rows=independent_rows(Y0,P);assert len(rows)==81
    S=Y0[rows,:]%P;Sinv=inv_mod(S,P)
    F=(Sinv@Y1[rows,:])%P
    assert np.array_equal((Y0@F)%P,Y1%P)
    scalar=next((a for a in (1,2) if np.array_equal(F%P,(a*np.eye(81,dtype=np.int64))%P)),None)
    # Endomorphism order on source coordinates.
    X=np.eye(81,dtype=np.int64)%P;order=None
    for n in range(1,100):
        X=(X@F)%P
        if np.array_equal(X,np.eye(81,dtype=np.int64)%P):order=n;break

    # Build the canonical CSS logical image on the exact same building cycle basis.
    edges=sorted({tuple(sorted((a,b))) for L in wlines for a,b in itertools.combinations(L,2)});ei={e:i for i,e in enumerate(edges)}
    Phi=np.zeros((240,160),dtype=np.int64)
    for s,(p,e) in enumerate(chambers):
        for q in wlines[e]:
            if q==p:continue
            edge=tuple(sorted((p,q)));Phi[ei[edge],s]+=1 if p<q else -1
    CSS=(Phi@Z)%P;assert rank_mod(CSS,P)==81

    out={'schema':'w33.20260902.mod3-even-gluing-css-bridge.v1','status':'PASS','field':'F3',
         'outerParityOverQ':{'evenPrimitiveIndices':[0,1],'oddPrimitiveIndex':2,'J':'diag(1,1,-1)'},
         'integralInjectionMetadata':meta,
         'mod3':{'rankEven0':81,'rankEven1':81,'rankOdd':81,'combinedEvenRank':81,
                 'evenOddCombinedRank':162,'evenImagesEqual':True,
                 'sourceCoordinateIntertwinerF_SHA256':hashlib.sha256(np.asarray(F,dtype=np.int8).tobytes()).hexdigest(),
                 'FIsScalar':scalar is not None,'FScalar':scalar,'FOrder':order,
                 'FTraceMod3':int(np.trace(F)%P)},
         'cssBridge':{'buildingCycleCoordinates':'shared 81-column basis Z',
                      'CSSLogicalBasisShape':[240,81],'obstructionEvenBasisShape':[1080,81],
                      'CSSLogicalBasisSHA256':hashlib.sha256(np.asarray(CSS,dtype=np.int8).tobytes()).hexdigest(),
                      'obstructionEvenBasisSHA256':hashlib.sha256(np.asarray(Y0,dtype=np.int8).tobytes()).hexdigest(),
                      'definition':'CSS* h <-> Y_even * h for h in F3^81',
                      'bothRanks':81},
         'theorem':('The two rational outer-even St81 channels reduce to exactly the same 81-dimensional obstruction submodule over F3, while the rational outer-odd channel reduces to a disjoint 81-dimensional submodule. The exact source-coordinate intertwiner between the two even maps is frozen. The common even submodule and the canonical CSS logical Steinberg are explicitly identified through the same W33 building-cycle coordinates.'),
         'boundary':('The common-source bridge is an exact PSp-module isomorphism between two finite modular images. It does not identify their physical carriers or attach continuum dynamics.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','scalar':scalar,'order':order,'evenRank':81,'evenOddRank':162},sort_keys=True))

if __name__=='__main__':main()
