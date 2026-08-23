#!/usr/bin/env python3
"""Pass8901-8908: the shared S3 in the 64-leaf binary module is literally E8 D4 triality.

Dependencies:
- Pass7949: explicit Q+(3,3) residue inside E8/3E8;
- Pass8301: its 64 W33 leaf lifts and G64 with 1 -> C2^8 -> G64 -> S3^3 -> 1;
- Pass8417: C2^8 splits into two irreducible 4D modules with one common active S3;
- Pass8801 repaired Pass8409: the E8 residue stabilizer is W(F4) x_{S3} W(F4).

This verifier rebuilds the same E8 Schreier generators simultaneously in matrix
space and on the 2240 leaves. The matrix projection gives the D4-triality quotient
W(F4)/W(D4)=S3. The leaf projection gives the faithful S3^3 action on C2^8.
The kernel of the triality map inside that order-216 leaf quotient is exactly the
product of the two order-6 kernels of the two irreducible 4D modules. Hence the
remaining common S3 quotient is precisely the synchronized D4 triality.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS8901_8908_DIAGONAL_TRIALITY_LEAF_COUPLING.json'
P=3
T=np.array([[0,1,2,0],[1,0,0,1],[1,1,1,2],[1,2,2,2]],dtype=np.int64)%3
SIMPLES=E.SIMPLES

def mm(A,B):return (np.asarray(A,dtype=np.int64)@np.asarray(B,dtype=np.int64))%P
def inv(A):
    A=np.array(A,dtype=np.int64)%P;n=len(A);B=np.concatenate([A,np.eye(n,dtype=np.int64)],1)%P;r=0
    for c in range(n):
        z=next(i for i in range(r,n) if B[i,c]);B[[r,z]]=B[[z,r]]
        B[r]=(B[r]*pow(int(B[r,c]),-1,P))%P
        for i in range(n):
            if i!=r and B[i,c]:B[i]=(B[i]-B[i,c]*B[r])%P
        r+=1
    return B[:,n:]%P

def rref(B):
    A=np.array(B,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
        if r==m:break
    return tuple(map(tuple,A.tolist()))
def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError
def qdet(x):return (x[0]*x[3]-x[1]*x[2])%3
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def pinv(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def pkey(g,n):return tuple(int(g(i)) for i in range(n))
def bkey(A):return bytes(np.asarray(A,dtype=np.uint8).ravel())
def b4(k):return np.frombuffer(k,dtype=np.uint8).astype(np.int64).reshape(4,4)
def mul4(k,l):return bkey(mm(b4(k),b4(l)))
def pairkey(A,B):return bkey(A)+bkey(B)

def close_pairs(gens):
    I=np.eye(4,dtype=np.int64);D={pairkey(I,I):(I,I)};q=collections.deque([(I,I)])
    while q:
        A,B=q.popleft()
        for C,D0 in gens:
            X=mm(A,C);Y=mm(B,D0);k=pairkey(X,Y)
            if k not in D:D[k]=(X,Y);q.append((X,Y))
    return D

def v8(n):return np.array([(n>>i)&1 for i in range(8)],dtype=np.uint8)
def vi(v):return sum(int(v[i])<<i for i in range(8))
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
    return tuple(vi(x) for x in rows)

def matperm(M):return Permutation([vi((M@v8(n))%2) for n in range(256)],size=256)

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build()
    radicals=[]
    for S in A2:
        vals=set()
        for i,j in itertools.combinations(sorted(S),2):
            if E.dot(R[i],R[j])==-4:vals.add(E.canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
        assert len(vals)==1;radicals.append(next(iter(vals)))
    ri={v:i for i,v in enumerate(radicals)}
    rank1=sorted({canon(x) for x in itertools.product(range(3),repeat=4) if any(x) and qdet(x)==0})
    U=set()
    for x in rank1:
        y4=tuple(int(z) for z in (T@np.array(x,dtype=np.int64))%3)
        U.add(ri[E.canon3(y4+(0,0,0,0))])
    assert len(U)==16
    selected=[i for i,L in enumerate(leaves) if len(set(L)&U)==4];assert len(selected)==64
    pos={v:i for i,v in enumerate(selected)}

    I8=np.eye(8,dtype=np.int64);mgens=[]
    for r in SIMPLES:
        v=np.array(r,dtype=np.int64).reshape(8,1)%3
        S=(I8-mm(v,v.T))%3;assert np.array_equal(mm(S,S),I8);mgens.append(S)
    W=np.eye(8,dtype=np.int64)[:4,:];k0=rref(W)
    orb=[k0];oi={k0:0};rm=[I8.copy()];rp=[tuple(range(2240))];dq=collections.deque([0]);raw=[]
    while dq:
        i=dq.popleft();tm=rm[i];tp=rp[i]
        for S,gp in zip(mgens,lgens):
            ntm=mm(S,tm);ntp=comp(gp,tp);k=rref(mm(W,ntm.T))
            if k not in oi:oi[k]=len(orb);orb.append(k);rm.append(ntm);rp.append(ntp);dq.append(len(orb)-1)
            j=oi[k];hm=mm(mm(inv(rm[j]),S),tm);hp=comp(pinv(rp[j]),comp(gp,tp))
            assert not np.any(hm[4:,:4]) and not np.any(hm[:4,4:])
            arr=tuple(pos[hp[v]] for v in selected)
            raw.append((hm[:4,:4].copy(),hm[4:,4:].copy(),arr))
    assert len(orb)==3150
    paired=[];seen=set()
    for A,B,p in raw:
        k=(bkey(A),bkey(B),p)
        if k not in seen:seen.add(k);paired.append((A,B,Permutation(list(p),size=64)))
    assert len(paired)==13

    HL=close_pairs([(A,B) for A,B,_ in paired]);assert len(HL)==221184
    I4=bkey(np.eye(4,dtype=np.int64));Aset={k[:16] for k in HL};KA={k[:16] for k in HL if k[16:]==I4}
    assert len(Aset)==1152 and len(KA)==192
    unseen=set(Aset);cos=[];ci={}
    while unseen:
        a=next(iter(unseen));C={mul4(a,k) for k in KA};j=len(cos);cos.append(C)
        for x in C:ci[x]=j
        unseen-=C
    assert len(cos)==6;crep=[next(iter(C)) for C in cos]
    trial=[]
    for A,_,_ in paired:
        ak=bkey(A);trial.append(Permutation([ci[mul4(ak,crep[j])] for j in range(6)],size=6))
    assert int(PermutationGroup(trial).order())==6

    K=PermutationGroup([h for _,_,h in paired]);assert int(K.order())==55296
    D2=K.derived_subgroup().derived_subgroup();assert int(D2.order())==256
    de=list(D2.generate_schreier_sims());id64=Permutation(list(range(64)))
    basis=[];coord={pkey(id64,64):0}
    for d in de:
        kd=pkey(d,64)
        if kd in coord:continue
        old=list(coord.items());bit=1<<len(basis)
        for pk,m in old:
            g=Permutation(list(pk),size=64);coord[pkey(g*d,64)]=m|bit
        basis.append(d)
        if len(basis)==8:break
    assert len(basis)==8 and len(coord)==256
    mats=[]
    for _,_,h in paired:
        hi=~h;cols=[]
        for b in basis:cols.append(v8(coord[pkey(h*b*hi,64)]))
        mats.append(np.column_stack(cols)%2)
    I=np.eye(8,dtype=np.uint8);MD={bkey(I):I};q=collections.deque([I])
    while q:
        A=q.popleft()
        for B in mats:
            C=(A@B)%2;k=bkey(C)
            if k not in MD:MD[k]=C;q.append(C)
    GM=list(MD.values());assert len(GM)==216
    mods={}
    for n in range(1,256):
        b=span_basis([(g@v8(n))%2 for g in GM]);mods[b]=mods.get(b,0)+1
    proper=[b for b in mods if len(b)<8];assert len(proper)==2 and sorted(len(b) for b in proper)==[4,4]
    blocks=[sorted(int(np.log2(x)) for x in b) for b in proper]
    assert sorted(blocks)==[[0,1,2,5],[3,4,6,7]]

    comb=[]
    for M,t in zip(mats,trial):
        pm=matperm(M);ti=~t
        comb.append(Permutation([int(pm(i)) for i in range(256)]+[256+int(ti(i)) for i in range(6)],size=262))
    Q=PermutationGroup(comb);assert int(Q.order())==216
    map_mt={}
    for g in Q.generate_schreier_sims():
        p=tuple(int(g(i)) for i in range(256));tr=tuple(int(g(256+i))-256 for i in range(6));map_mt[p]=tr
    assert len(map_mt)==216 and len(set(map_mt.values()))==6
    allm=[];ktr=[]
    for p,tr in map_mt.items():
        M=np.column_stack([v8(p[1<<i]) for i in range(8)])%2;allm.append(M)
        if tr==tuple(range(6)):ktr.append(M)
    assert len(ktr)==36
    B0=[0,1,2,5];B1=[3,4,6,7];I8b=np.eye(8,dtype=np.uint8)
    ker0=[M for M in allm if all(np.array_equal((M@I8b[:,i])%2,I8b[:,i]) for i in B0)]
    ker1=[M for M in allm if all(np.array_equal((M@I8b[:,i])%2,I8b[:,i]) for i in B1)]
    assert len(ker0)==len(ker1)==6
    product={bkey((A@B)%2) for A in ker0 for B in ker1}
    assert len(product)==36 and product=={bkey(M) for M in ktr}

    out={'schema':'w33.pass8901_8908.diagonal_triality_leaf_coupling.v1','status':'PASS','passes':'8901-8908',
      'paired_Schreier_generators':13,'linear_residue_stabilizer_order':221184,'W_F4_projection_order':1152,'W_D4_kernel_order':192,'triality_quotient':'S3',
      'leaf_controller_order':55296,'leaf_binary_normal':'C2^8','leaf_quotient_order':216,'leaf_quotient':'S3^3','binary_module_dimensions':[4,4],
      'two_module_kernel_orders':[6,6],'triality_kernel_in_leaf_quotient_order':36,'kernel_identity':'ker(triality) = ker(M4) x ker(M4_prime)',
      'shared_quotient':'The quotient by those two module-kernel S3 factors is the same S3=W(F4)/W(D4) triality quotient and acts nontrivially on both irreducible C2^4 channels.',
      'theorem':'The algebraic coupling S3 shared by the two irreducible C2^4 channels in the 64-leaf residue is literally the synchronized D4 triality quotient of the E8 D4+D4 residue stabilizer.',
      'claim_boundary':'Exact generator-level finite-group/representation commuting diagram; no physical coupling is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','paired_generators':13,'leaf_quotient':'S3^3','triality':'shared_S3'}))
if __name__=='__main__':main()
