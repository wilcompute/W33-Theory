#!/usr/bin/env python3
"""Exact W33 216-route POVM effect spectrum, cross module, and covariance."""
from pathlib import Path
from collections import Counter
import math,sys,json
import numpy as np
from sympy import prevprime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261102_route_216_cubic_tomography as old

def minima(mat,weight):
    a=[sum((int(x)&1)<<j for j,x in enumerate(row)) for row in mat]
    piv={};r=0;n=mat.shape[1]
    for j in range(n):
        k=next((i for i in range(r,len(a)) if a[i]>>j&1),None)
        if k is None:continue
        a[k],a[r]=a[r],a[k]
        for i in range(len(a)):
            if i!=r and a[i]>>j&1:a[i]^=a[r]
        piv[j]=r;r+=1
    free=[j for j in range(n) if j not in piv]
    assert r==25 and len(free)==15
    basis=[(1<<j)|sum((1<<k) for k,i in piv.items() if a[i]>>j&1) for j in free]
    out=[];word=0
    for i in range(1,1<<15):
        word^=basis[(i&-i).bit_length()-1]
        assert word.bit_count()>=weight
        if word.bit_count()==weight:out.append(word)
    return out

def rank_mod(M,p):
    A=M.copy()%p;n=len(A);r=0
    for j in range(n):
        nz=np.flatnonzero(A[r:,j])
        if not len(nz):continue
        k=r+int(nz[0]);A[[r,k]]=A[[k,r]]
        inv=pow(int(A[r,j]),-1,p)
        ids=np.flatnonzero(A[r+1:,j])+r+1
        if len(ids):
            f=(A[ids,j]*inv)%p
            A[ids,j:]=(A[ids,j:]-f[:,None]*A[r,j:][None,:])%p
        r+=1
        if r==n:break
    return r

def main():
    pts,lines,N,idx,norm,symp=old.geometry()
    lid={frozenset(L):i for i,L in enumerate(lines)}
    pg=[];lg=[]
    for a in pts:
        gp=tuple(idx[norm(tuple((x[k]+symp(x,a)*a[k])%3 for k in range(4)))] for x in pts)
        pg.append(gp)
        lg.append(tuple(lid[frozenset(gp[x] for x in L)] for L in lines))
    seed=frozenset(old.SEED);seen={seed};front=[seed]
    while front:
        nxt=[]
        for S in front:
            for g in lg:
                T=frozenset(g[j] for j in S)
                if T not in seen:seen.add(T);nxt.append(T)
        front=nxt
    assert len(seen)==216
    words=sorted(seen,key=lambda x:tuple(sorted(x)))
    B=np.zeros((216,40),dtype=np.int64)
    for i,S in enumerate(words):B[i,list(S)]=1
    cover=B@N.T
    assert np.all((cover==0)|(cover==2))
    H=cover//2;Z=2*H-1
    I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
    A=N@N.T-4*I
    assert np.array_equal(Z.T@Z,240*I+60*A-24*J)
    assert np.array_equal((Z.T@Z)@(Z.T@Z),360*(Z.T@Z))
    # POVM E_s= |u_s><u_s|/9, with u_s in R^24.
    _,sv,Vt=np.linalg.svd(Z.astype(float),full_matrices=False)
    assert np.max(abs(sv[:24]-math.sqrt(360)))<1e-8
    assert np.max(abs(sv[24:]))<1e-8
    u=Z@Vt[:24].T/math.sqrt(40)
    assert np.max(abs(u.T@u-9*np.eye(24)))<1e-10
    assert np.max(abs(np.sum(u*u,axis=1)-1))<1e-10
    # Exact operator-Gram spectrum: CRT modular annihilator plus rank.
    K=(Z@Z.T)**2;Q=np.eye(216,dtype=np.int64)
    assert int(np.trace(K))==345600
    roots=(0,576,768,2304,3168,14400)
    primes=[];p=65521
    for _ in range(8):primes.append(p);p=int(prevprime(p))
    bound=345600**6;crt=math.prod(primes)
    assert crt>2*bound
    for p in primes:
        V=Q.copy()
        for lam in roots:V=(V@((K-lam*Q)%p))%p
        assert not V.any()
    spec={str(l):216-rank_mod(K-l*Q,primes[0]) for l in roots}
    assert spec=={'0':15,'576':15,'768':81,'2304':80,'3168':24,'14400':1}
    # Address vs route: exhaustive binary kernels.
    ad=minima(N.T,8);ro=minima(N,10)
    assert len(ad)==45 and len(ro)==216
    M=np.array([[int(w>>j&1) for j in range(40)] for w in ad],dtype=np.int64)
    cross=M@H.T
    counts=dict(sorted(Counter(map(int,cross.ravel())).items()))
    assert counts=={0:1080,4:6480,6:2160}
    assert np.array_equal(M.T@M,8*I+2*A+J)
    assert set(map(int,cross.sum(1)))=={864}
    assert set(map(int,cross.sum(0)))=={180}
    # Equivariance on all 40 symplectic transvections.
    pos={S:i for i,S in enumerate(words)}
    for gp,gl in zip(pg,lg):
        inv=np.argsort(gp)
        for i,S in enumerate(words):
            assert np.array_equal(H[i,inv],H[pos[frozenset(gl[j] for j in S)]])
    split=Z[Z[:,0]==1].sum(axis=0)
    assert Counter(map(int,split))=={108:1,18:12,-12:27}
    pairs=Counter(int(np.dot(Z[i],Z[j])) for i in range(216) for j in range(i+1,216))
    cubic=216*40**3+2*sum(c*v**3 for v,c in pairs.items())
    assert cubic==27371520
    assert np.array_equal((Z.T@Z)@np.ones(40,dtype=np.int64),np.zeros(40,dtype=np.int64))
    res={'status':'PASS_EXACT_216_OUTCOME_POVM_AND_DUALITY',
      'address_minimum_words':45,'route_minimum_words':216,
      'cross_point_overlap_distribution':counts,
      'address_support_gram':'M.T M=8 I+2 A_point+J',
      'povm':{'dimension':24,'outcomes':216,'effects':'E_s=(1/9)|u_s><u_s|',
         'sum_effects':'I_24','uniform_input_probability':'1/216',
         'naimark_output_dimension':216,'operator_span_exact_rank':201,
         'hermitian_operator_space_dimension':576,
         'informationally_complete':False},
      'effect_squared_gram':{'integer_eigenvalues':spec,
          'modular_primes':primes,'CRT_product':str(crt),
          'max_polynomial_entry_bound':str(bound),
          'method':'annihilator vanishes modulo CRT product greater than twice norm bound; distinct-root mod-p nullities certify multiplicities'},
      'clifford_transvections_checked':40,
      'point_stabilizer_108_split_first_moments':dict(sorted(Counter(map(int,split)).items())),
      'invariant_cubic_frobenius_norm_squared':cubic,
      'equivariant_unital_Jordan_on_24d':False,
      'scope':'Abstract measurement and finite geometry. No specific photonic circuit, arbitrary-state tomography or TOE.'}
    out=ROOT/'data/w33_20261102_povm_spectrum_and_duality.json'
    out.write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8')
    print(res['status'],spec,counts)
    return res
if __name__=='__main__':main()
