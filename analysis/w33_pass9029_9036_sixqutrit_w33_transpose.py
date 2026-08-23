#!/usr/bin/env python3
"""Pass9029-9036: inverse/transpose involution on the 31 W33-slice double cosets."""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9029_9036_SIXQUTRIT_W33_TRANSPOSE.json'
J=np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]],dtype=int)
std=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
allvec=[np.array(v,dtype=int) for v in itertools.product(range(3),repeat=4)]
def rref(A,ncols=4):
    A=np.array(A,dtype=int)%3
    if A.size==0:return np.zeros((0,ncols),dtype=int),()
    if A.ndim==1:A=A.reshape(1,-1)
    m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-int(A[i,c])*A[r])%3
        piv.append(c);r+=1
        if r==m:break
    return A[:r],tuple(piv)
def skey(A):return tuple(map(tuple,rref(A)[0].tolist()))
def rank(A):return len(rref(A)[0])
def inv(M):
    A=np.c_[M%3,np.eye(4,dtype=int)];r=0
    for c in range(4):
        z=next(i for i in range(r,4) if A[i,c]);A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(4):
            if i!=r and A[i,c]:A[i]=(A[i]-int(A[i,c])*A[r])%3
        r+=1
    return A[:,4:]%3
def nullrows(A):
    B=[]
    for v in itertools.product(range(3),repeat=4):
        if not any(v) or np.any((np.array(v)@A)%3):continue
        if rank(B+[v])>len(B):B.append(v)
    return skey(B)
def contained(K,R):return rank(list(R)+list(K))==len(R)
def trans_sub(K,M):return () if not K else skey((np.array(K,dtype=int)@M)%3)
subs={()};changed=True
while changed:
    changed=False
    for S in list(subs):
        for v in itertools.product(range(3),repeat=4):
            T=skey(list(S)+[v])
            if T not in subs:subs.add(T);changed=True
bydim=defaultdict(list)
for S in subs:bydim[len(S)].append(S)
assert {d:len(x) for d,x in bydim.items()}=={0:1,1:40,2:130,3:40,4:1}
Ps=[]
for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
    Ps.append(np.array([[0,a,b,c],[-a,0,d,e],[-b,-d,0,f],[-c,-e,-f,0]],int)%3)
pk={tuple(P.ravel()):i for i,P in enumerate(Ps)}
def allowed_A(dim,r):return (dim,r) in {(4,4),(3,2),(2,2),(2,0),(1,0),(0,0)}
def allowed_B(dim,r):return r<=dim and r%2==0
states=[]
for pi,P in enumerate(Ps):
    Q=(J-P)%3;rp=rank(P);rq=rank(Q);radP=nullrows(P);radQ=nullrows(Q)
    for KA in subs:
        if not allowed_A(4-len(KA),rp) or not contained(KA,radP):continue
        for KB in subs:
            if not allowed_B(4-len(KB),rq) or not contained(KB,radQ):continue
            if rank(list(KA)+list(KB))!=len(KA)+len(KB):continue
            states.append((pi,KA,KB))
states=sorted(states,key=repr);si={s:i for i,s in enumerate(states)};assert len(states)==5250
gens=[np.array(x,int)%3 for x in [
[[1,0,0,0],[2,1,0,0],[0,0,1,0],[0,0,0,1]],[[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,2,1]],[[1,0,0,0],[0,1,0,0],[0,0,1,1],[0,0,0,1]],
[[1,0,0,0],[2,1,2,0],[0,0,1,0],[2,0,2,1]]]]
assert all(np.array_equal((g@J@g.T)%3,J) for g in gens)
I=np.eye(4,dtype=int)%3;mkey=lambda M:tuple(map(int,M.ravel()));seen={mkey(I)};dq=deque([I])
while dq:
    x=dq.popleft()
    for g in gens:
        y=(g@x)%3;k=mkey(y)
        if k not in seen:seen.add(k);dq.append(y)
assert len(seen)==51840
def act(s,g):
    pi,KA,KB=s;P=Ps[pi];gi=inv(g);P2=(g@P@g.T)%3
    return (pk[tuple(P2.ravel())],trans_sub(KA,gi),trans_sub(KB,gi))
orbof={};orbits=[]
for i,s in enumerate(states):
    if i in orbof:continue
    O={i};q=deque([i]);oi=len(orbits);orbof[i]=oi
    while q:
        u=q.popleft()
        for g in gens:
            v=si[act(states[u],g)]
            if v not in O:O.add(v);orbof[v]=oi;q.append(v)
    orbits.append(sorted(O))
assert len(orbits)==31
assert sorted(map(len,orbits))==[1,1,1,1,40,40,40,40,40,72,72,72,80,80,80,80,90,90,90,90,90,90,90,320,320,360,360,360,360,360,1440]
def complement_before(K):
    C=[];base=list(K);r0=rank(base)
    for e in std:
        if rank(base+C+[e])>r0+len(C):C.append(e)
        if len(C)==4-len(K):break
    T=np.array(C+list(K),int)%3;assert rank(T)==4;return T
def find_vectors_gram(R):
    r=R.shape[0]
    if r==0:return np.zeros((0,4),int)
    chosen=[]
    def rec(i):
        if i==r:return np.array(chosen,int).reshape(r,4)
        for v in allvec:
            if not np.any(v):continue
            if any(int(v@J@u)%3!=int(R[i,j]) for j,u in enumerate(chosen)):continue
            if rank(chosen+[tuple(v)])<i+1:continue
            chosen.append(v.copy());z=rec(i+1)
            if z is not None:return z
            chosen.pop()
        return None
    return rec(0)
def construct_A(P,KA):
    r=4-len(KA);T=complement_before(KA);Pt=(T@P@T.T)%3
    assert not np.any(Pt[r:,:]) and not np.any(Pt[:,r:]);Y=find_vectors_gram(Pt[:r,:r]);assert Y is not None
    Ap=np.zeros((4,4),int)
    if r:Ap[:r]=Y
    A=(inv(T)@Ap)%3;assert np.array_equal((A@J@A.T)%3,P) and nullrows(A)==KA;return A
def transpose_state(s):
    pi,KA,KB=s;P=Ps[pi];A=construct_A(P,KA);C=(-J@A.T@J)%3;Pr=(C@J@C.T)%3
    KAr=nullrows(C);KBr=() if not KB else skey((np.array(KB,int)@A)%3);z=(pk[tuple(Pr.ravel())],KAr,KBr);assert z in si;return z
tr={oi:orbof[si[transpose_state(states[O[0]])]] for oi,O in enumerate(orbits)}
assert all(tr[tr[i]]==i for i in tr);pairs=sorted(set(tuple(sorted((i,j))) for i,j in tr.items() if i!=j));assert len(pairs)==1
a,b=pairs[0]
def sig(s):
    pi,KA,KB=s;P=Ps[pi];Q=(J-P)%3;return (len(KB),len(KA),rank(P),rank(Q),4-rank(P),4-rank(Q))
sa=sig(states[orbits[a][0]]);sb=sig(states[orbits[b][0]])
assert {sa,sb}=={(0,2,0,4,4,0),(0,2,2,4,2,0)}
actual=8459973849600
out={'schema':'w33.pass9029_9036.sixqutrit_w33_transpose.v1','status':'PASS','passes':'9029-9036','finite_states':5250,'Sp4_order':51840,'double_cosets':31,'self_inverse_double_cosets':29,'unique_inverse_pair':{'signatures':[list(sa),list(sb)],'finite_orbit_sizes':[len(orbits[a]),len(orbits[b])],'actual_slice_orbital_sizes':[actual,actual]},'transpose_formula':'For A:X->U with P=A J A^T, the reversed projection is C=-J A^T J; K_A reverses to ker(C), while K_B=X cap U maps to rowspace(K_B A).','theorem':'The rank-31 relative-position geometry of W33 slices in W(11,3) has exactly one non-self-inverse double-coset pair; the other 29 double cosets are self-inverse. The unique pair has signatures (0,2,0,4,4,0) and (0,2,2,4,2,0), and both actual orbitals have valency 8,459,973,849,600.','claim_boundary':'Exact finite symplectic transpose/inversion computation. A unique nonsymmetric pair does not by itself decide whether the full Hecke algebra is commutative.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','double_cosets':31,'self_inverse':29,'pair':out['unique_inverse_pair']}))
