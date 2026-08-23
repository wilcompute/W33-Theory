#!/usr/bin/env python3
"""Pass9397-9404 outside-box: the 16D logical point-star quotient is O^-(16,2).

Pass9037-9044 identifies the nondegenerate point-star quotient with
F_2^40/ker(A_W33), polar form B(x,y)=x^T A_W33 y.  Because A_W33 is the
adjacency matrix of a simple graph, q(x)=sum_{i<j} A_ij x_i x_j polarizes to B.
The decisive check here is that q vanishes on ker(A), so it descends to the
16-dimensional quotient.  Enumeration of a complement determines minus type.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9397_9404_POINTSTAR_ORTHOGONAL_MINUS.json'

def canon3(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError

def rref2(M):
    M=np.asarray(M,dtype=np.uint8).copy();m,n=M.shape;r=0;piv=[]
    for c in range(n):
        z=np.flatnonzero(M[r:,c])
        if not len(z):continue
        i=r+int(z[0]);M[[r,i]]=M[[i,r]]
        for j in np.flatnonzero(M[:,c]):
            if j!=r:M[j]^=M[r]
        piv.append(c);r+=1
        if r==m:break
    return M,piv

def rank2(M):return len(rref2(M)[1])

def null2(M):
    R,piv=rref2(M);n=R.shape[1];free=[j for j in range(n) if j not in piv];B=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,p in enumerate(piv):
            if R[i,f]:x[p]=1
        B.append(x)
    return np.asarray(B,dtype=np.uint8)

P=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
assert len(P)==40
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],int)%3
A=np.zeros((40,40),dtype=np.uint8)
for i,j in itertools.combinations(range(40),2):
    if int(np.array(P[i])@J@np.array(P[j]))%3==0:A[i,j]=A[j,i]=1
assert set(map(int,A.sum(1)))=={12} and rank2(A)==16 and not np.any(np.diag(A))
edges=[tuple(map(int,z)) for z in np.argwhere(np.triu(A,1))]
def q(x):
    x=np.asarray(x,dtype=np.uint8)
    return sum(int(x[i]&x[j]) for i,j in edges)&1
K=null2(A);assert K.shape==(24,40)
# On rad(B)=ker(A), q is linear. Vanishing on a basis proves vanishing identically.
assert all(q(k)==0 for k in K)

# Choose a vector-space complement of ker(A) and enumerate all 2^16 quotient classes.
cur=K.copy();r=rank2(cur);C=[]
for i in range(40):
    e=np.zeros(40,dtype=np.uint8);e[i]=1
    rr=rank2(np.vstack([cur,e]))
    if rr>r:
        C.append(e);cur=np.vstack([cur,e]);r=rr
    if len(C)==16:break
C=np.asarray(C,dtype=np.uint8);assert C.shape==(16,40) and r==40
cnt=Counter()
for mask in range(1<<16):
    x=np.zeros(40,dtype=np.uint8)
    for i in range(16):
        if (mask>>i)&1:x^=C[i]
    cnt[q(x)]+=1
assert cnt==Counter({1:32896,0:32640})
# For 2m=16, minus type has 2^(15)-2^7 zeros including zero.
assert cnt[0]==2**15-2**7
# The forty coordinate classes are singular and span the quotient modulo ker(A).
assert all(q(np.eye(40,dtype=np.uint8)[i])==0 for i in range(40))
assert rank2(np.vstack([K,np.eye(40,dtype=np.uint8)]))==40
# Their polar Gram is A itself: W33 adjacency = nonorthogonality on this singular 40-set.
for i,j in itertools.combinations(range(40),2):
    ei=np.zeros(40,dtype=np.uint8);ej=np.zeros(40,dtype=np.uint8);ei[i]=1;ej[j]=1
    polar=q(ei^ej)^q(ei)^q(ej)
    assert polar==int(A[i,j])

out={
 'schema':'w33.pass9397_9404.pointstar_orthogonal_minus.v1','status':'PASS','passes':'9397-9404','outside_box':True,
 'quotient':'F2^40 / ker(A_W33)','dimension':16,
 'quadratic_refinement':'q(x)=sum_{i<j} A_W33[i,j] x_i x_j',
 'descent':{'ker_A_dimension':24,'q_vanishes_on_ker_A':True,'polar_form':'B(x,y)=x^T A_W33 y'},
 'type':{'orthogonal':'minus','notation':'O^-(16,2) / Q^-(15,2)','zeros_including_zero':32640,'nonsingular_vectors':32896},
 'W33_singular_40_set':{'size':40,'all_singular':True,'spans_quotient':True,'pairing_rule':'B(e_p,e_q)=1 iff p,q are adjacent in W33','interpretation':'W33 is the nonorthogonality graph induced on forty canonical singular point-star classes.'},
 'group_boundary':'W(E6) preserves A_W33 and therefore q, so its 16D logical quotient action lies in O^-(16,2). No assertion that the image is the full orthogonal group is made.',
 'theorem':'The 16-dimensional nondegenerate logical point-star quotient has a canonical W(E6)-invariant minus-type quadratic refinement. Its forty canonical point-star classes are singular and realize W33 exactly as their nonorthogonality graph inside Q^-(15,2).',
 'claim_boundary':'Exact finite characteristic-two quadratic geometry; this is a logical/module quotient, not a claim of a physical 8-qubit subsystem.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','type':'Q-(15,2)','singular':32640,'W33_points':40}))
