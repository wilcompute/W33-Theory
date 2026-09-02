#!/usr/bin/env python3
"""Identify the two mod-3 St81 obstruction images as the two PGSp extensions.

The previous exact chain-level results give:
  * a common outer-even 81-dimensional obstruction image Y+ over F3;
  * a disjoint outer-odd 81-dimensional obstruction image Y- over F3;
  * the CSS logical Steinberg CSS=Phi Z on the same W33 building-cycle basis Z.

Here we include the actual multiplier-minus-one similitude s=diag(1,2,1,2).
It acts on W33 building chambers, on the 1080 obstruction carrier, and as a
signed permutation on the canonically oriented 240 clique edges.  We compute
the induced 81x81 outer matrix S on building H1 and verify exactly

    s Y+  =  Y+ S,
    s Y-  = -Y- S,
    s CSS =  CSS S              over F3.

Thus Y+ and CSS carry the same PGSp extension of the PSp Steinberg, while Y-
carries its tensor product with the nontrivial PGSp/PSp sign character.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260901_packet48_bt796_crossid as shell
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import mulvec
from w33_20260901_building_chain_injections import integer_cycle_basis,lcm_den,rank_mod

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_MOD3_PGSP_EXTENSION_TWIN.json'
P=3


def norm(v):
    i=next(k for k,x in enumerate(v) if x%3);z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)

def inv_mod(A,p):
    A=np.asarray(A,dtype=np.int64)%p;n=A.shape[0];X=np.concatenate([A,np.eye(n,dtype=np.int64)],axis=1)%p;r=0
    for c in range(n):
        z=next(i for i in range(r,n) if X[i,c]);
        if z!=r:X[[r,z]]=X[[z,r]]
        X[r]=(X[r]*pow(int(X[r,c]),-1,p))%p
        for i in range(n):
            if i!=r and X[i,c]:X[i]=(X[i]-int(X[i,c])*X[r])%p
        r+=1
    assert np.array_equal(X[:,:n],np.eye(n,dtype=np.int64)%p);return X[:,n:]%p

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

def permute_rows(A,perm,signs=None,p=3):
    out=np.zeros_like(A,dtype=np.int64)
    if signs is None:
        for i,j in enumerate(perm):out[j]=A[i]
    else:
        for i,j in enumerate(perm):out[j]=(int(signs[i])*A[i])%p
    return out%p


def main():
    D=shell.build();pts,wlines,supports,charts,G=D['pts'],D['wlines'],D['supports'],D['charts'],D['G']
    idx={v:i for i,v in enumerate(pts)};li={frozenset(L):i for i,L in enumerate(wlines)}
    F=build_frame();rel,T,frame=F['rel'],F['T'],list(F['frame'])
    outer40=tuple(idx[norm((v[0],2*v[1],v[2],2*v[3]))] for v in pts)
    outerL=tuple(li[frozenset(outer40[x] for x in L)] for L in wlines)
    si={S:i for i,S in enumerate(supports)};outer45=tuple(si[frozenset(outer40[x] for x in S)] for S in supports)
    ci27={frozenset(C):i for i,C in enumerate(charts)};outer27=tuple(ci27[frozenset(outer45[x] for x in C)] for C in charts)
    outer1080=tuple(outer27[y//40]*40+outerL[y%40] for y in range(1080))

    @lru_cache(maxsize=None)
    def line_perm(gi):
        p=G[gi][0];return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def target_one(gi,y):
        c,e=divmod(y,40);return G[gi][2][c]*40+line_perm(gi)[e]

    chambers=[(p,e) for e,L in enumerate(wlines) for p in L];chi={x:i for i,x in enumerate(chambers)}
    outerCh=tuple(chi[(outer40[p],outerL[e])] for p,e in chambers)
    Z,zden=integer_cycle_basis(40,40,chambers);assert zden==1 and Z.shape==(160,81)
    Z=Z%P;Zout=permute_rows(Z,outerCh,p=P)
    rows=independent_rows(Z,P);assert len(rows)==81
    S=(inv_mod(Z[rows,:],P)@Zout[rows,:])%P
    assert np.array_equal((Z@S)%P,Zout)
    assert np.array_equal((S@S)%P,np.eye(81,dtype=np.int64)%P)

    # Source-to-target orbital maps, exactly as in the frozen injection certificate.
    transport=[None]*160;H=[]
    def source_one(gi,s):
        p,e=chambers[s];return chi[(G[gi][0][p],line_perm(gi)[e])]
    for gi in range(len(G)):
        s=source_one(gi,0)
        if transport[s] is None:transport[s]=gi
        if s==0:H.append(gi)
    unseen=set(range(1080));orbits=[]
    while unseen:
        y=min(unseen);O={target_one(gi,y) for gi in H};unseen-=O;orbits.append(tuple(sorted(O)))
    orbits.sort(key=lambda O:(len(O),O[0]));zero=sp.zeros(59,1)
    def columns(O):return [tuple(sorted(target_one(transport[s],y) for y in O)) for s in range(160)]
    def selfgram(C):
        row=np.zeros(1080,dtype=np.int64)
        for col in C:
            if 0 in col:row[list(col)]+=1
        v=[None]*59
        for y,x in enumerate(row.tolist()):
            r=int(rel[0,y])
            if v[r] is None:v[r]=x
            else:assert v[r]==x
        return sp.Matrix(v)
    Ys=[]
    for Pj in frame:
        found=None
        for O in orbits:
            C=columns(O);V=selfgram(C)
            if mulvec(Pj,mulvec(V,Pj,T),T)!=zero:found=C;break
        assert found is not None
        den=lcm_den(Pj);coeff=np.array([int(den*q) for q in Pj],dtype=np.int64);Pnum=coeff[np.asarray(rel,dtype=np.int64)]
        A=np.zeros((1080,160),dtype=np.int64)
        for s,col in enumerate(found):A[:,s]=Pnum[:,list(col)].sum(axis=1)
        Y=(A@Z)%P;assert rank_mod(Y,P)==81;Ys.append(Y)
    Yplus,Yplus2,Yminus=Ys
    assert np.array_equal(Yplus,Yplus2)
    Tplus=permute_rows(Yplus,outer1080,p=P);Tminus=permute_rows(Yminus,outer1080,p=P)
    rhsPlus=(Yplus@S)%P;rhsMinus=(Yminus@S)%P
    assert np.array_equal(Tplus,rhsPlus)
    assert np.array_equal(Tminus,(-rhsMinus)%P)

    # Canonical oriented clique-edge CSS map and signed outer permutation.
    edges=sorted({tuple(sorted((a,b))) for L in wlines for a,b in itertools.combinations(L,2)});ei={e:i for i,e in enumerate(edges)}
    Phi=np.zeros((240,160),dtype=np.int64)
    for s,(p,e) in enumerate(chambers):
        for q in wlines[e]:
            if q==p:continue
            E=tuple(sorted((p,q)));Phi[ei[E],s]+=1 if p<q else -1
    CSS=(Phi@Z)%P;assert rank_mod(CSS,P)==81
    outerEdge=[];edgeSign=[]
    for a,b in edges:
        aa,bb=outer40[a],outer40[b];outerEdge.append(ei[tuple(sorted((aa,bb)))]);edgeSign.append(1 if aa<bb else -1)
    ToutCSS=permute_rows(CSS,outerEdge,edgeSign,P)
    assert np.array_equal(ToutCSS,(CSS@S)%P)

    out={'schema':'w33.20260902.mod3-pgsp-extension-twin.v1','status':'PASS','field':'F3',
         'outer':{'matrixMod3':'diag(1,2,1,2)','buildingH1MatrixShape':[81,81],
                  'buildingH1MatrixSHA256':hashlib.sha256(np.asarray(S,dtype=np.int8).tobytes()).hexdigest(),
                  'involution':True},
         'covariance':{'CSS':'s CSS = CSS S','obstructionEven':'s Y+ = Y+ S',
                       'obstructionOdd':'s Y- = - Y- S','allVerified':True},
         'modules':{'CSSLogicalExtension':'outer-even','obstructionEvenExtension':'outer-even',
                    'obstructionOddExtension':'outer-odd/sign-twist'},
         'theorem':('Over F3 the common even obstruction Steinberg and the canonical CSS logical Steinberg carry the same extension from PSp4(3) to the explicit PGSp4(3) outer involution. The disjoint odd obstruction Steinberg carries the sign-twisted extension: after transporting the same building H1 coordinates by the outer matrix S, its target chain map acquires exactly a minus sign.'),
         'boundary':('Outer-even and outer-odd here mean the two finite PGSp extensions of the same restricted PSp Steinberg module. This is not a spacetime parity or particle-chirality claim.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','S_involution':True,'CSS':'even','Yplus':'even','Yminus':'odd'},sort_keys=True))

if __name__=='__main__':main()
