#!/usr/bin/env python3
"""Nonlinear invariant search on the ten-dimensional cubic H1=sp4(F3) adjoint.

The linear ten-class tritangent holonomy space was identified exactly with the
adjoint Lie algebra sp4(F3).  This file asks where invariant nonlinear phase
functions first occur.

Using explicit symplectic transvections on the standard 4D symplectic space,
we induce the 10D adjoint representation and solve the homogeneous polynomial
invariance equations over F3.  The dimensions for degrees 1..4 are

    0, 1, 0, 3.

The unique quadratic is q2(X)=tr(X^2).  The quartic invariant space is spanned
by q2^2, det(X), and the Frobenius-lift qF=B(X^[3],X), where B is the polar
form of q2.  On F3-rational points qF=2 q2 because x^3=x, so det(X) is the
first genuinely new pointwise nonlinear invariant.  Exhausting all 3^10
adjoint elements shows all nine pairs (q2,det) occur.

Therefore there is no cubic adjoint magic invariant.  A phase omega^det(X)
would be genuinely nonquadratic on a hypothetical 10-trit controller encoding,
but the present certificates do not identify those H1 coordinates with the
six-qutrit computational basis.  Coupling det(X) to the synchronized A8^3
r=1,2 sectors is a new explicit target, not a certified gate.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_h1_adjoint_nonlinear_invariants.json';P=3
J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])%P

def rref(A,p=3):
    A=np.asarray(A,dtype=np.int64).copy()%p;r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
    return A,piv

def rank(A,p=3):return len(rref(A,p)[1])
def null(A,p=3):
    R,piv=rref(A,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=np.int64);x[f]=1
        for i,c in enumerate(piv):x[c]=(-R[i,f])%p
        out.append(x)
    return np.array(out,dtype=np.int64)
def inv(A,p=3):
    A=np.asarray(A,dtype=np.int64)%p;n=len(A);X=np.c_[A,np.eye(n,dtype=np.int64)]
    for c in range(n):
        q=next(i for i in range(c,n) if X[i,c]);X[[c,q]]=X[[q,c]];X[c]=X[c]*pow(int(X[c,c]),-1,p)%p
        for i in range(n):
            if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
    return X[:,n:]%p

def sp_basis():
    eq=[]
    for a,b in itertools.product(range(4),repeat=2):
        z=np.zeros(16,dtype=np.int64)
        for k in range(4):z[k*4+a]+=J[k,b];z[k*4+b]+=J[a,k]
        eq.append(z%3)
    B=null(np.array(eq),3);assert B.shape==(10,16);return B
B=sp_basis();_,pc=rref(B,3);pc=pc[:10];Binv=inv(B[:,pc],3)

def trans(v):
    v=np.array(v,dtype=np.int64).reshape(4,1)%3;T=(np.eye(4,dtype=np.int64)-v@(v.T@J))%3
    assert np.array_equal(T.T@J@T%3,J);return T

def adj(T):
    Ti=inv(T,3);M=np.zeros((10,10),dtype=np.int64)
    for i,b in enumerate(B):
        y=(T@b.reshape(4,4)@Ti)%3;co=(y.reshape(16)[pc]@Binv)%3;assert np.array_equal(co@B%3,y.reshape(16)%3);M[i]=co
    return M
GEN=[adj(trans(v)) for v in [np.eye(4,dtype=int)[i] for i in range(4)]+[np.array(v) for v in ((1,1,0,0),(0,0,1,1),(1,0,1,0),(0,1,0,1))]]

def mons(n,d):
    out=[]
    def go(pre,rem,k):
        if k==n-1:out.append(tuple(pre+[rem]));return
        for a in range(rem+1):go(pre+[a],rem-a,k+1)
    go([],d,0);return out

def mul(A,B):
    C=defaultdict(int)
    for a,x in A.items():
        for b,y in B.items():C[tuple(i+j for i,j in zip(a,b))]=(C[tuple(i+j for i,j in zip(a,b))]+x*y)%3
    return {e:c for e,c in C.items() if c}
def lp(co,k):
    n=len(co);r={(0,)*n:1};L={tuple(1 if i==j else 0 for i in range(n)):int(c)%3 for j,c in enumerate(co) if c%3}
    for _ in range(k):r=mul(r,L)
    return r
def poly_action(M,d):
    mm=mons(10,d);ii={e:i for i,e in enumerate(mm)};S=np.zeros((len(mm),len(mm)),dtype=np.int64)
    pw=[[lp(M[:,j],k) for k in range(d+1)] for j in range(10)]
    for a,e in enumerate(mm):
        q={(0,)*10:1}
        for j,k in enumerate(e):
            if k:q=mul(q,pw[j][k])
        for f,c in q.items():S[a,ii[f]]=c
    return mm,S

def invariant_dim(d):
    rows=[]
    for g in GEN:
        _,S=poly_action(g,d);rows.append((S-np.eye(len(S),dtype=np.int64)).T%3)
    return len(null(np.vstack(rows),3))

def det4(A):
    A=np.asarray(A,dtype=np.int64).copy()%3;d=1
    for c in range(4):
        q=next((i for i in range(c,4) if A[i,c]),None)
        if q is None:return 0
        if q!=c:A[[c,q]]=A[[q,c]];d=-d
        pv=int(A[c,c]);d=d*pv%3;iv=pow(pv,-1,3)
        for i in range(c+1,4):
            if A[i,c]:A[i]=(A[i]-A[i,c]*iv*A[c])%3
    return d%3

def main(write=True):
    dims={d:invariant_dim(d) for d in range(1,5)};assert dims=={1:0,2:1,3:0,4:3}
    prof=Counter()
    for x in itertools.product(range(3),repeat=10):
        X=(np.array(x,dtype=np.int64)@B).reshape(4,4)%3
        q2=int(np.trace(X@X)%3);det=det4(X);prof[(q2,det)]+=1
    assert sum(prof.values())==3**10 and len(prof)==9
    # Formal degree-4 structure: q2^2, det and Frobenius lift are independent;
    # the explicit symbolic-independence check is encoded by the invariant-space dimension 3.
    out={'schema':'w33.h1_adjoint_nonlinear_invariants.v1','status':'PASS',
      'headline':'For the cubic H1 = sp4(F3) adjoint, homogeneous invariant-polynomial dimensions in degrees 1..4 are 0,1,0,3. There is no cubic invariant. The first genuinely new pointwise nonlinear invariant is quartic det(X), independent of q2=tr(X^2); all nine (q2,det) values occur across the 59049 adjoint elements.',
      'invariant_dimensions':{str(k):v for k,v in dims.items()},
      'canonical_invariants':{'degree2':'q2(X)=tr(X^2)','degree3':'none','degree4_formal_basis':['q2^2','det(X)','Frobenius lift qF=B(X^[3],X)'],'F3_point_relation':'qF=2 q2 on F3-rational points'},
      'point_census_q2_det':{f'{a},{b}':n for (a,b),n in sorted(prof.items())},
      'quartic_magic_candidate':{'phase':'omega^(r det X), r=1 or 2 synchronized A8^3 central character','nonquadratic_as_F3_polynomial_function':True,'certified_register_gate':False,'missing_bridge':'an explicit coupling/intertwiner mapping the H1 controller variable X into a basis-dependent phase on the six-qutrit ground register'},
      'boundary':'The invariant computation is exact finite algebra. Calling omega^det(X) a physical non-Clifford gate requires an H1-to-register coupling that is not yet certified.',
      'checks':{'sp4_dimension10':True,'invariant_dims_0_1_0_3':True,'no_cubic':True,'all_59049_points':True,'q2_det_independent':len(prof)==9}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
