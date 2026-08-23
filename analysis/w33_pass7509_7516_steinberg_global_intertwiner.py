#!/usr/bin/env python3
"""Pass7509-7516: global A2 -> W33 Steinberg H1 integral intertwiner and SNF."""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7509_7516_STEINBERG_GLOBAL_INTERTWINER.json'

def build_T():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();AO,C,lab=E.a2_scheme(R,A2);bl=sorted(base);W=AO[np.ix_(bl,bl)]
    edges=[(i,j) for i in range(40) for j in range(i+1,40) if W[i,j]];ei={e:k for k,e in enumerate(edges)}
    tris=[t for t in itertools.combinations(range(40),3) if all(W[a,b] for a,b in itertools.combinations(t,2))]
    assert len(edges)==240 and len(tris)==160
    d0=np.zeros((40,240),dtype=np.int64);d1=np.zeros((240,160),dtype=np.int64)
    for k,(a,b) in enumerate(edges):d0[a,k]=-1;d0[b,k]=1
    for j,(a,b,c) in enumerate(tris):d1[ei[(b,c)],j]=1;d1[ei[(a,c)],j]=-1;d1[ei[(a,b)],j]=1
    L=d0.T@d0+d1@d1.T;I=np.eye(240,dtype=np.int64);P=(4*I-L)@(10*I-L)@(16*I-L)
    assert np.array_equal(P@P,640*P) and np.linalg.matrix_rank(P.astype(float),tol=1e-7)==81
    maps={}
    for a,b in itertools.combinations(range(5),2):
        M=np.zeros((240,1120),dtype=np.int8)
        for k,(u,v) in enumerate(edges):
            ru=lab[:,bl[u]];rv=lab[:,bl[v]];M[k,(ru==a)&(rv==b)]=1;M[k,(ru==b)&(rv==a)]=-1
        X=P@M.astype(np.int64);g=0
        for x in X.ravel():g=math.gcd(g,abs(int(x)))
        maps[(a,b)]=(X//g if g else X,g)
    T=maps[(1,2)][0];assert np.array_equal(T@T.T,240*P)
    signs={(1,2):1,(1,3):-1,(1,4):1,(2,3):1,(2,4):-1}
    for k,s in signs.items():assert np.array_equal(maps[k][0],s*T)
    assert np.count_nonzero(np.any(T!=0,axis=0))==1080 and all(not np.any(T[:,j]) for j in bl)
    return R,A2,J,base,bl,AO,lab,edges,L,P,T,maps

def padic_vals(A,p,K,target=81):
    M=p**K;A=np.asarray(A,dtype=np.int64).copy()%M;m,n=A.shape;r=0;vals=[]
    while r<min(m,n) and r<target:
        B=A[r:,r:];nz=np.argwhere(B%M!=0)
        if len(nz)==0:break
        best=K;bi=bj=0
        for ii,jj in nz:
            x=int(B[ii,jj]);v=0
            while v<K and x%p==0:v+=1;x//=p
            if v<best:best=v;bi=int(ii);bj=int(jj)
            if v==0:break
        i=r+bi;j=r+bj
        if i!=r:A[[r,i],r:]=A[[i,r],r:]
        if j!=r:A[r:,[r,j]]=A[r:,[j,r]]
        pv=p**best;unit=(int(A[r,r])//pv)%(M//pv);A[r,r:]=(A[r,r:]*pow(unit,-1,M))%M
        if r+1<m:
            f=(A[r+1:,r]//pv).astype(np.int64);A[r+1:,r:]=(A[r+1:,r:]-f[:,None]*A[r,r:])%M
        if r+1<n:
            f=(A[r,r+1:]//pv).astype(np.int64);A[r:,r+1:]=(A[r:,r+1:]-A[r:,r,None]*f[None,:])%M
        vals.append(best);r+=1
    return vals

def main():
    R,A2,J,base,bl,AO,lab,edges,L,P,T,maps=build_T();nz=T[:,np.any(T!=0,axis=0)]
    spec=Counter(int(round(x)) for x in np.linalg.eigvalsh(L.astype(float)));assert spec=={0:81,4:120,10:24,16:15}
    mods={str(p):E.rank_mod(T,p) for p in (2,3,5,7,11,13)};assert mods=={'2':14,'3':81,'5':23,'7':81,'11':81,'13':81}
    v2=Counter(padic_vals(nz,2,12));v5=Counter(padic_vals(nz,5,8));assert v2=={0:14,2:1,3:52,4:8,5:6} and v5=={0:23,1:58}
    snf={'1':14,'4':1,'8':8,'40':44,'80':8,'160':6};assert sum(snf.values())==81
    cols={}
    for j in np.flatnonzero(np.any(T!=0,axis=0)):cols.setdefault(tuple(int(x) for x in T[:,j]),[]).append(int(j))
    assert len(cols)==360 and set(map(len,cols.values()))=={3}
    out={'schema':'w33.pass7509_7516.steinberg_global_intertwiner.v1','status':'PASS','passes':'7509-7516',
      'H1_dimension':81,'Hodge_spectrum':{str(k):v for k,v in sorted(spec.items())},'projector_numerator_identity':'P^2=640P',
      'surviving_relation_maps':{'(1,2)':'+T','(1,3)':'-T','(1,4)':'+T','(2,3)':'+T','(2,4)':'-T'},'vanishing_relation_maps':['(0,*)','(3,4)'],
      'tight_frame_identity':'T T^T = 240 P','zero_columns':40,'nonzero_columns':1080,'distinct_nonzero_vectors':360,'multiplicity_each':3,
      'modular_ranks':mods,'F3_full_rank_steinberg':True,'nonzero_Smith_invariants':snf,'determinantal_divisor_81':'2^220 * 5^58',
      'theorem':'The global 1120-A2 permutation lattice has a canonical antisymmetric orbital map onto the unique W33 Steinberg H1. Five orbital constructions collapse to one primitive map up to sign; it has full rank 81 in characteristic 3 and the stated exact Smith invariants.',
      'boundary':'Integral/finite representation theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','rankF3':mods['3'],'SNF':snf,'distinct_vectors':360}))
if __name__=='__main__':main()
