#!/usr/bin/env python3
"""Pass10049-10056: exhaustive order-13 test against the canonical Leech V2.

This is the decisive version of the Pass9985 gate.  It works in the actual
24-dimensional mod-2 Co1 representation already stored in the repository.

1. Reconstruct the embedded 3.Suz:2 from the ATLAS standard-generator words
   in the Co1 standard generators.
2. Reconstruct Suz and its embedded G2(4) from the ATLAS words.  Standard
   G2(4) generators have product of order 13.
3. Build the canonical V2 = im((I-M)^2) from the repository's unique pure
   order-8 matrix M and test the explicit 13-element directly.
4. More importantly, enumerate *all* 4097 irreducible 12-spaces invariant
   under this Co1 class-13A representative.  (Phi_13 is irreducible over F2,
   ord_13(2)=12, and the 24-space is two copies of that irreducible module.)
5. Filter them for maximal total singularity and then count Leech type-4
   classes in each by regenerating the 98280-class minimal-vector orbit from
   the actual mod-2 Co1 generators.

Because Co1 has a single order-13 class 13A, the distribution of Leech type on
13A-invariant generators is conjugacy invariant.  If none is type-4-free, then
NO order-13 element of Co1 can stabilize canonical V2, which is type-4-free.

External structural inputs are only ATLAS words/class uniqueness; every module,
subspace, quadratic and type census statement is recomputed from repo matrices.
"""
from __future__ import annotations
from collections import Counter, deque
import json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
OUT=ROOT/'data/PART_W33_PASS10049_10056_CO1_C13_V2_EXHAUSTIVE.json'
P=2
N=24


def mm(A,B): return (A@B)&1

def eye(): return np.eye(N,dtype=np.uint8)

def inv2(A):
    A=np.array(A,dtype=np.uint8)&1
    X=np.concatenate([A,eye()],axis=1)
    r=0
    for c in range(N):
        q=next((i for i in range(r,N) if X[i,c]),None)
        if q is None: raise ValueError('singular')
        X[[r,q]]=X[[q,r]]
        for i in range(N):
            if i!=r and X[i,c]: X[i]^=X[r]
        r+=1
    return X[:,N:]

def pw(A,n):
    if n<0:return pw(inv2(A),-n)
    R=eye();B=A.copy()
    while n:
        if n&1:R=mm(R,B)
        B=mm(B,B);n//=2
    return R

def word(seq,mp):
    R=eye()
    for ch in seq:R=mm(R,mp[ch])
    return R

def order(A,limit=1000):
    R=eye()
    for k in range(1,limit+1):
        R=mm(R,A)
        if np.array_equal(R,eye()):return k
    return None

def conj_power(base_word, exp, mp): return pw(word(base_word,mp),exp)

def rref_cols(B):
    A=np.array(B,dtype=np.uint8)&1
    # return independent columns via row reduction on transpose
    R=A.T.copy();m,n=R.shape;r=0;p=[]
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        p.append(q);r+=1
        if r==m:break
    # easier: derive original independent columns incrementally
    cols=[];rank=0
    for j in range(A.shape[1]):
        T=np.column_stack(cols+[A[:,j]]) if cols else A[:,j:j+1]
        rr=rank2(T)
        if rr>rank:cols.append(A[:,j]);rank=rr
    return np.column_stack(cols) if cols else np.zeros((N,0),dtype=np.uint8)

def rank2(A):
    R=np.array(A,dtype=np.uint8)&1;m,n=R.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        r+=1
        if r==m:break
    return r

def cyclic_basis(z,v):
    cols=[];x=np.array(v,dtype=np.uint8)&1
    for _ in range(12):
        cols.append(x.copy());x=(z@x)&1
    B=np.column_stack(cols)
    assert rank2(B)==12
    return B

def same_space(A,B): return rank2(np.column_stack([A,B]))==rank2(A)==rank2(B)

def vecint(v):
    x=0
    for i,b in enumerate(np.array(v,dtype=np.uint8).tolist()):
        if b:x|=1<<i
    return x

def all_span_ints(B):
    bs=[vecint(B[:,j]) for j in range(B.shape[1])]
    vals=[0]
    for b in bs: vals += [x^b for x in vals]
    return vals

def total_singular(B,G):
    # B has 0/1 integer representatives as columns.
    Bi=B.astype(np.int64)
    gram=(Bi.T@G@Bi)%2
    if np.any(gram):return False
    for j in range(B.shape[1]):
        x=Bi[:,j]
        if (int(x@G@x)//2)%2:return False
    return True

def orbit_bits(gens,start,cap=200000):
    start=vecint(start);seen={start};Q=deque([start])
    # precompute image of coordinate basis as bit masks for each generator
    maps=[]
    for A in gens:
        maps.append([vecint(A[:,j]) for j in range(N)])
    def act(x,mp):
        y=0;j=0
        while x:
            if x&1:y^=mp[j]
            x>>=1;j+=1
        return y
    while Q:
        x=Q.popleft()
        for mp in maps:
            y=act(x,mp)
            if y not in seen:
                seen.add(y);Q.append(y)
                if len(seen)>cap:raise RuntimeError('orbit cap exceeded')
    return seen

def main():
    mats=load_flat(ROOT/'analysis/_co0_G.txt')
    assert len(mats)==2
    A=np.array(mats[0],dtype=np.uint8)&1; B=np.array(mats[1],dtype=np.uint8)&1
    mp={'a':A,'b':B}
    # Co1 standard checks after reduction mod 2.
    std={'a':order(A),'b':order(B),'ab':order(word('ab',mp)),'ababb':order(word('ababb',mp))}
    assert std=={'a':2,'b':3,'ab':40,'ababb':6}

    # ATLAS: 3.Suz:2 maximal subgroup of Co1.
    C=mm(mm(pw(word('ab',mp),-2),B),mm(A,B)) # (ab)^-2 b a b
    D=mm(mm(pw(word('abb',mp),-2),pw(word('abababbabababbab',mp),8)),word('abbabb',mp))
    cd={'C':C,'D':D}
    # ATLAS maximal Suz inside Suz:2; same projective words apply to the 3-cover mod 2.
    T=word('cdd',{'c':C,'d':D})
    Sa=mm(mm(pw(T,-2),pw(word('cd',{'c':C,'d':D}),14)),pw(T,2))
    Sb=D
    smp={'a':Sa,'b':Sb}
    z_suz=word('ab',smp)
    assert order(z_suz)==13

    # ATLAS standard G2(4) inside Suz; its standard-generator product is order 13.
    Ga=mm(mm(pw(word('ab',smp),-5),pw(word('abababb',smp),6)),pw(word('ab',smp),5))
    Gb=mm(mm(pw(word('abb',smp),-4),pw(word('ababb',smp),3)),pw(word('abb',smp),4))
    gmp={'a':Ga,'b':Gb}
    g2_checks={'a':order(Ga),'b':order(Gb),'ab':order(word('ab',gmp)),'abb':order(word('abb',gmp)),'ababb':order(word('ababb',gmp))}
    assert g2_checks=={'a':2,'b':5,'ab':13,'abb':13,'ababb':15}
    z=word('ab',gmp)

    # Canonical V2 from unique pure order-8 M.
    M=np.array(load_flat(ROOT/'analysis/_co0_M8.txt')[0],dtype=np.int64)
    I=np.eye(N,dtype=np.int64);Nmat=(I-M)%2
    V2=rref_cols((Nmat@Nmat)%2)
    assert V2.shape==(24,12)
    explicit_invariant=rank2(np.column_stack([V2,(z@V2)&1]))==12

    # Invariant module decomposition U1 + U2.
    e=np.eye(N,dtype=np.uint8)
    U1=None
    for i in range(N):
        try:T1=cyclic_basis(z,e[:,i])
        except AssertionError:continue
        U1=T1;break
    assert U1 is not None
    U2=None
    for i in range(N):
        T2=cyclic_basis(z,e[:,i])
        if rank2(np.column_stack([U1,T2]))==24:U2=T2;break
    assert U2 is not None

    # Recover the positive Leech Gram and a norm-4 basis class.
    G0,_=invariant_gram(load_flat(ROOT/'analysis/_co0_G.txt'));G=-np.array(G0,dtype=np.int64)
    idx=next(i for i in range(N) if int(G[i,i])==4)
    type4=orbit_bits([A,B],e[:,idx],cap=120000)
    assert len(type4)==98280

    # 4096 graphs U_t plus U2 at infinity.
    u2vals=all_span_ints(U2)
    # map int back to vector
    def intvec(x):return np.array([(x>>i)&1 for i in range(N)],dtype=np.uint8)
    sing=[];dist=Counter();v2_hit=False
    v=U1[:,0]
    for tcode in u2vals:
        t=intvec(tcode)
        W=cyclic_basis(z,v^t)
        if total_singular(W,G):
            vals=all_span_ints(W)[1:]
            c=sum(x in type4 for x in vals)
            sing.append(c);dist[c]+=1
            if same_space(W,V2):v2_hit=True
    if total_singular(U2,G):
        vals=all_span_ints(U2)[1:];c=sum(x in type4 for x in vals)
        sing.append(c);dist[c]+=1
        if same_space(U2,V2):v2_hit=True

    assert len(sing)>0
    type4_free=dist.get(0,0)
    # If zero, this is an absolute no-go because Co1 has one 13A class.
    theorem = ('NO-GO: no Co1 order-13 element can stabilize canonical V2.' if type4_free==0 else
               'There exist 13A-invariant type-4-free generators; Co1-orbit comparison with canonical V2 remains necessary.')
    out={
      'schema':'w33.pass10049_10056.co1_c13_v2_exhaustive.v1','status':'PASS','passes':'10049-10056',
      'co1_standard_checks':std,
      'atlas_embedded_3Suz2':{'constructed':True,'Suz_order13_word':'a*b after standard Suz recovery','order':order(z_suz)},
      'atlas_embedded_G2_4':{'standard_checks':g2_checks,'order13_word':'ab','order':order(z)},
      'canonical_V2':{'dimension':12,'explicit_G2_order13_stabilizes':bool(explicit_invariant)},
      'class13A_invariant_12spaces':{'all_irreducible_invariant_12spaces':4097,'totally_singular_count':len(sing),'type4_count_distribution':{str(k):v for k,v in sorted(dist.items())},'type4_free_count':type4_free,'canonical_V2_is_one_of_them':bool(v2_hit)},
      'single_class_input':'ATLAS Co1 has exactly one order-13 class 13A, centralizer order 156.',
      'theorem':theorem,
      'boundary':'All 4097 invariant irreducible 12-spaces for one actual Co1 13A representative are exhaustive. Type-4 classes are regenerated as the 98280-element orbit in the actual mod-2 Co1 module. The only external inputs are ATLAS standard-generator words and uniqueness of Co1 class 13A.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
    return 0
if __name__=='__main__':raise SystemExit(main())
