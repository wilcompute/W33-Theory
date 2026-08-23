#!/usr/bin/env python3
"""Pass7941-7948: sharpen the Leech/E8 A2 controller comparison.

Pass7917 gives the Leech projective linking-similitude group G_L of order 46656
on 234 W33 polarities, with four orbits 36,36,81,81.  The overlap-60 graph on a
36-orbit is 3 K_{3,3,3,3}.  This pass uses those three connected components as a
canonical S3 quotient and compares it to the W(A2)=S3 factor in the current
projective E8 A2 stabilizer S3 x W(E6), order 311040.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7941_7948_LEECH_E8_S3_KERNEL_BRIDGE.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError
def rank(A):
    M=np.asarray(A,dtype=int).copy()%3;r=0
    for c in range(M.shape[1]):
        z=next((i for i in range(r,len(M)) if M[i,c]),None)
        if z is None:continue
        M[[r,z]]=M[[z,r]];M[r]=(M[r]*pow(int(M[r,c]),-1,3))%3
        for i in range(len(M)):
            if i!=r and M[i,c]:M[i]=(M[i]-int(M[i,c])*M[r])%3
        r+=1
    return r
def fkey(M):
    M=np.asarray(M,dtype=int)%3;z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    if next(x for x in z if x)==2:M=(-M)%3;z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    return tuple(z)
def pf(k):
    a,b,c,d,e,f=k;return (a*f-b*e+c*d)%3

def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    forms={}
    for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
        M=np.array([[0,a,b,c],[-a,0,d,e],[-b,-d,0,f],[-c,-e,-f,0]],dtype=int)%3
        if rank(M)==4:forms[fkey(M)]=M if fkey(M)==(a,b,c,d,e,f) else (-M)%3
    keys=sorted(forms);ki={k:i for i,k in enumerate(keys)};assert len(keys)==234
    s1=np.array([[1,1],[0,1]],int)%3;s2=np.array([[0,2],[1,0]],int)%3;flip=np.array([[2,0],[0,1]],int)%3;I=np.eye(2,dtype=int)%3
    mats=[]
    for A in (s1,s2):mats.append(np.block([[A,np.zeros((2,2),int)],[np.zeros((2,2),int),I]])%3)
    for D in (s1,s2):mats.append(np.block([[I,np.zeros((2,2),int)],[np.zeros((2,2),int),D]])%3)
    mats.append(np.block([[flip,np.zeros((2,2),int)],[np.zeros((2,2),int),flip]])%3)
    for i in range(2):
      for j in range(2):
        C=np.zeros((2,2),int);C[i,j]=1;mats.append(np.block([[I,np.zeros((2,2),int)],[C,I]])%3)
    perms=[[ki[fkey((g.T@forms[k]@g)%3)] for k in keys] for g in mats]
    G=PermutationGroup([Permutation(p) for p in perms]);assert int(G.order())==46656
    orbs=sorted([sorted(map(int,o)) for o in G.orbits()],key=lambda O:(len(O),pf(keys[O[0]])))
    assert [len(O) for O in orbs]==[36,36,81,81]

    edges=[]
    for k in keys:
        M=forms[k];E=set()
        for i,u in enumerate(P):
          U=np.array(u,dtype=int)
          for j in range(i+1,40):
            if int(U@M@np.array(P[j],dtype=int))%3==0:E.add((i,j))
        edges.append(frozenset(E))
    O=orbs[0];A=np.zeros((36,36),dtype=np.int8)
    for i,j in itertools.combinations(range(36),2):
        if len(edges[O[i]]&edges[O[j]])==60:A[i,j]=A[j,i]=1
    comps=[];seen=set()
    for s in range(36):
        if s in seen:continue
        C={s};q=[s];seen.add(s)
        while q:
            u=q.pop()
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if v not in C:C.add(v);seen.add(v);q.append(v)
        comps.append(frozenset(O[i] for i in C))
    assert sorted(map(len,comps))==[12,12,12]
    cp={S:i for i,S in enumerate(comps)};cperms=[]
    for p in perms:
        cperms.append(tuple(cp[frozenset(p[x] for x in S)] for S in comps))
    Q=PermutationGroup([Permutation(list(p)) for p in cperms]);assert int(Q.order())==6
    kernel_order=46656//6;assert kernel_order==7776
    component_stabilizer_order=46656//3;assert component_stabilizer_order==15552

    # There is no canonical normal C3 inside the normal tensor 3^4 layer:
    # SL2(3)xSL2(3) acts on M2(F3) by D C A^-1.  Its projective orbits have
    # sizes 16 (rank one) and 24 (invertible), so no 1D subspace is invariant.
    mats2=[]
    for z in itertools.product(range(3),repeat=4):
        X=np.array(z,dtype=int).reshape(2,2)%3
        if round(np.linalg.det(X))%3:mats2.append(X)
    assert len(mats2)==48
    SL=[X for X in mats2 if round(np.linalg.det(X))%3==1];assert len(SL)==24
    pts=sorted({canon(z) for z in itertools.product(range(3),repeat=4) if any(z)})
    pidx={x:i for i,x in enumerate(pts)}
    action=[]
    for A0,D0 in ((s1,I),(s2,I),(I,s1),(I,s2)):
        Ai=np.array([[A0[1,1],-A0[0,1]],[-A0[1,0],A0[0,0]]],dtype=int)%3
        action.append(tuple(pidx[canon(tuple(int(x) for x in (D0@np.array(v).reshape(2,2)@Ai).reshape(-1)%3))] for v in pts))
    U=PermutationGroup([Permutation(list(p)) for p in action]);
    assert sorted(len(o) for o in U.orbits())==[16,24]

    e8_stab=311040;e6=51840
    assert e8_stab==6*e6
    common_full=math.gcd(46656,e8_stab);common_kernel=math.gcd(kernel_order,e6)
    assert common_full==15552 and common_kernel==2592 and kernel_order==3*common_kernel and e6==20*common_kernel
    out={
      'schema':'w33.pass7941_7948.leech_e8_s3_kernel_bridge.v1','status':'PASS','passes':'7941-7948',
      'Leech_controller_order':46656,'canonical_three_component_quotient':'S3','Leech_S3_kernel_order':kernel_order,
      'component_stabilizer_order':component_stabilizer_order,
      'E8_A2_stabilizer':{'order':e8_stab,'structure':'S3 x W(E6)','W_E6_order':e6},
      'largest_order_dividing_both_full_controllers':common_full,
      'after_aligning_S3':{'kernel_gcd':common_kernel,'Leech_kernel':'3 x 2592','E8_kernel':'20 x 2592'},
      'normal_C3_no_go':'The normal 3^4 tensor layer M2(F3) has projective Levi orbits 16+24, so it has no invariant 1D subspace; a canonical normal C3 quotient is unavailable.',
      'next_exact_target':'construct an actual order-2592 subgroup/action on both kernels; order arithmetic alone does not establish that subgroup weld.',
      'theorem':'The natural Leech symmetry reduction is controlled by a canonical S3 quotient, not by arbitrarily dividing out C3. Aligning this S3 with W(A2) isolates 2592 as the exact common-order kernel target; equivalently the stabilizer of one Leech three-component block has order 15552, the gcd of the two full controller orders.',
      'claim_boundary':'The S3 quotients and order obstructions are exact. An objectwise common 2592 subgroup is not yet constructed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','S3_kernel':7776,'common_kernel':2592,'component_stabilizer':15552}))
if __name__=='__main__':main()
