#!/usr/bin/env python3
from __future__ import annotations
import itertools
from collections import deque
import numpy as np

def m36_rays():
    w=np.exp(2j*np.pi/3);rays=[];meta=[]
    for fam in range(4):
        for mu in range(3):
            for nu in range(3):
                raw=[0,1,-w**mu,w**nu] if fam==0 else [1,0,-w**mu,-w**nu] if fam==1 else [1,-w**mu,0,w**nu] if fam==2 else [1,w**mu,w**nu,0]
                rays.append(np.array(raw,dtype=complex)/np.sqrt(3));meta.append((fam,mu,nu))
    return rays,meta
def bxor(a,b):return tuple(x^y for x,y in zip(a,b))
def bsymp(v,w,n):return sum(v[i]*w[n+i]+v[n+i]*w[i] for i in range(n))%2
def bvec(i,n):return tuple((i>>k)&1 for k in range(2*n))
I2=np.eye(2,dtype=complex);X2=np.array([[0,1],[1,0]],complex);Z2=np.array([[1,0],[0,-1]],complex)
def kron_all(ms):
    out=np.array([[1]],complex)
    for m in ms:out=np.kron(out,m)
    return out
def hermitian_pauli(v,n):return kron_all([(1j**(x*z))*np.linalg.matrix_power(X2,x)@np.linalg.matrix_power(Z2,z) for x,z in zip(v[:n],v[n:])])
def stabilizer_states_two_qubits():
    vecs=[bvec(i,2) for i in range(1,16)];planes=set();states=[];I=np.eye(4,dtype=complex)
    for i,u in enumerate(vecs):
        for v in vecs[i+1:]:
            if not bsymp(u,v,2):planes.add(tuple(sorted((u,v,bxor(u,v)))))
    for plane in sorted(planes):
        P,Q=hermitian_pauli(plane[0],2),hermitian_pauli(plane[1],2)
        for s,t in itertools.product((1,-1),repeat=2):
            rho=((I+s*P)@(I+t*Q))/4;vals,vecs_=np.linalg.eigh(rho);psi=vecs_[:,int(np.argmax(vals))];psi/=np.linalg.norm(psi)
            if not any(abs(np.vdot(psi,q))**2>1-1e-9 for q in states):states.append(psi)
    assert len(states)==60;return states
def m36_grade_data():
    rays,meta=m36_rays();stabs=stabilizer_states_two_qubits();groups={}
    for i,r in enumerate(rays):groups.setdefault(round(float(max(abs(np.vdot(r,s))**2 for s in stabs)),12),[]).append(i)
    assert sorted(map(len,groups.values()))==[4,8,24];return rays,meta,groups
Q=3;Mat=tuple[tuple[int,...],...];I4=tuple(tuple(int(i==j) for j in range(4)) for i in range(4));J4=((0,1,0,0),(2,0,0,0),(0,0,0,1),(0,0,2,0));FP=((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1));FF=((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0));SP=((1,0,0,0),(1,1,0,0),(0,0,1,0),(0,0,0,1));SF=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,1));CX=((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1))
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(4))%3 for j in range(4)) for i in range(4))
def inv(a):
    aug=[list(a[i])+[int(i==j) for j in range(4)] for i in range(4)];r=0
    for c in range(4):
        p=next(i for i in range(r,4) if aug[i][c]%3);aug[r],aug[p]=aug[p],aug[r]
        if aug[r][c]==2:aug[r]=[(2*x)%3 for x in aug[r]]
        for i in range(4):
            if i!=r and aug[i][c]:f=aug[i][c];aug[i]=[(aug[i][j]-f*aug[r][j])%3 for j in range(8)]
        r+=1
    return tuple(tuple(row[4:]) for row in aug)
def mpow(a,n):
    out=I4
    while n:
        if n&1:out=mm(out,a)
        a=mm(a,a);n//=2
    return out
def order(a,limit=200):
    x=I4
    for n in range(1,limit+1):
        x=mm(x,a)
        if x==I4:return n
    raise ValueError
def generators():
    out=[]
    for g in (FP,FF,SP,SF,CX):out.append(g);gi=inv(g);out.extend([gi] if gi!=g else [])
    return out
def group_closure(with_parent=False):
    gs=generators();parent={I4:(None,None)};q=deque([I4])
    while q:
        x=q.popleft()
        for j,s in enumerate(gs):
            y=mm(x,s)
            if y not in parent:parent[y]=(x,j);q.append(y)
    assert len(parent)==51840;return (list(parent),parent) if with_parent else list(parent)
def centralizer(group,target=CX):return sorted(g for g in group if mm(g,target)==mm(target,g))
def closure(gens):
    out={I4};q=deque([I4]);gens=list(gens)
    while q:
        x=q.popleft()
        for g in gens:
            y=mm(x,g)
            if y not in out:out.add(y);q.append(y)
    return out
def center(group):return {g for g in group if all(mm(g,h)==mm(h,g) for h in group)}
def factor_centralizer(C):
    Z=center(C);z6=next(z for z in sorted(Z) if order(z)==6);z3=next(z for z in sorted(Z) if order(z)==3 and len(closure((z6,z)))==18);S=None
    for a in sorted(C):
        if a in Z or order(a)!=3:continue
        for b in sorted(C):
            if order(b)==2 and mm(mm(b,a),b)==inv(a):
                H=closure((a,b))
                if len(H)==6 and H&Z=={I4} and len({mm(z,h) for z in Z for h in H})==108:S=(a,b,sorted(H));break
        if S:break
    assert S;return z6,z3,S[0],S[1],S[2]
def norm3(v):
    v=tuple(int(x)%3 for x in v);f=next(x for x in v if x);m=1 if f==1 else 2;return tuple(m*x%3 for x in v)
def sp3(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
def w33_lines():
    pts=sorted({norm3(v) for v in itertools.product(range(3),repeat=4) if any(v)});lines=set()
    for u,v in itertools.combinations(pts,2):
        if sp3(u,v):continue
        L=tuple(sorted({norm3(tuple((a*np.array(u)+b*np.array(v))%3)) for a,b in itertools.product(range(3),repeat=2) if a or b}))
        if len(L)==4:lines.add(L)
    assert len(lines)==40;return pts,sorted(lines)
def rank3(A):
    A=np.array(A,dtype=int)%3;r=0
    for c in range(A.shape[1]):
        p=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if p is None:continue
        A[[r,p]]=A[[p,r]]
        if A[r,c]==2:A[r]=2*A[r]%3
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%3
        r+=1
    return r
def inv3(A):
    A=np.array(A,dtype=int)%3;n=A.shape[0];aug=np.concatenate([A,np.eye(n,dtype=int)],axis=1);r=0
    for c in range(n):
        p=next(i for i in range(r,n) if aug[i,c]);aug[[r,p]]=aug[[p,r]]
        if aug[r,c]==2:aug[r]=2*aug[r]%3
        for i in range(n):
            if i!=r and aug[i,c]:aug[i]=(aug[i]-aug[i,c]*aug[r])%3
        r+=1
    return aug[:,n:]%3
def canonical_line_frame(line):
    b1=np.array(line[0],int);B=None
    for p in line[1:]:
        q=np.array(p,int)
        if rank3(np.column_stack([b1,q]))==2:B=np.column_stack([b1,q])%3;break
    J=np.array(J4,int);vecs=[np.array(v,int) for v in itertools.product(range(3),repeat=4)]
    for m1 in vecs:
        if tuple(B.T@J@m1%3)!=(1,0):continue
        for m2 in vecs:
            if tuple(B.T@J@m2%3)==(0,1) and int(m1@J@m2%3)==0:
                M=np.column_stack([m1,m2])%3
                if rank3(np.column_stack([B,M]))==4:return B,M
    raise AssertionError
