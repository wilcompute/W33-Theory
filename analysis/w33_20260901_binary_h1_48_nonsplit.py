#!/usr/bin/env python3
"""Resolve the binary H1=48 of the 90-D4 prism.

The doubled prism is a chain complex mod 2:

    F2^36 --N90--> F2^90 --R90--> F2^27,

with H1 dimension 48.  The pair injection J immediately supplies an invariant
45-space S=im(J)=ker(J^T) in characteristic two.  This witness turns that
observation into the exact module filtration

    0 -> A24 -> H1_48 -> B24 -> 0,

where A24=S/im(N90) and B24=ker(R P) on the 45 packet coordinates.  Generator
matrices are built explicitly and the extension splitting equation is solved
over F2.  It has no solution: H1_48 is a nonsplit extension.

The tempting shared 48-dimensional Z12 sector from the independent E8
Z3/Z4 refinement is also tested at object level.  A product of two E6 root
reflections (hence an even W(E6)=PSp(4,3) element) sends a root in that 48-sector
outside it.  Therefore the E8 grading-48 is not a PSp-invariant carrier and
cannot be the binary H1 module.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np

import w33_20260829_216_clifford_torsor_nogo as groupbase
from w33_pass4992_4999_common import build_base
from w33_pass7225_7232_spread_code_doily_puncture import coordinate_isomorphism
from w33_20260901_d4_prism_lift import d4_data
from w33_pass7081_7096_e8_z3_z4_z12_common_refinement import (
    e8_roots_doubled, simple_roots, coeff_map, dot,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_BINARY_H1_48_NONSPLIT.json'


def rref(A):
    A=np.asarray(A,dtype=np.uint8).copy()&1;m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        piv.append(c);r+=1
        if r==m:break
    return A,piv


def rank(A):return len(rref(A)[1])


def col_basis(M):
    _R,p=rref(M);return np.asarray(M,dtype=np.uint8)[:,p]


def nullspace(A):
    R,piv=rref(A);n=R.shape[1];free=[j for j in range(n) if j not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,p in enumerate(piv):x[p]=R[i,f]
        out.append(x)
    return np.stack(out,axis=1) if out else np.zeros((n,0),dtype=np.uint8)


def inv2(A):
    A=np.asarray(A,dtype=np.uint8);n=A.shape[0]
    M=np.concatenate([A.copy(),np.eye(n,dtype=np.uint8)],axis=1);r=0
    for c in range(n):
        z=next(i for i in range(r,n) if M[i,c]);M[[r,z]]=M[[z,r]]
        for i in range(n):
            if i!=r and M[i,c]:M[i]^=M[r]
        r+=1
    assert np.array_equal(M[:,:n],np.eye(n,dtype=np.uint8))
    return M[:,n:]


def coord_solver(B):
    B=np.asarray(B,dtype=np.uint8);_R,rows=rref(B.T);rows=rows[:B.shape[1]]
    I=inv2(B[rows,:])
    return lambda V:(I@np.asarray(V,dtype=np.uint8)[rows,:])&1


def solve_linear(A,b):
    A=np.asarray(A,dtype=np.uint8);b=np.asarray(b,dtype=np.uint8).reshape(-1,1)
    M=np.concatenate([A,b],axis=1);m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=next((i for i in range(r,m) if M[i,c]),None)
        if z is None:continue
        M[[r,z]]=M[[z,r]]
        for i in range(m):
            if i!=r and M[i,c]:M[i]^=M[r]
        piv.append(c);r+=1
    for i in range(r,m):
        if not M[i,:n].any() and M[i,n]:return None,0
    free=[j for j in range(n) if j not in piv]
    x=np.zeros(n,dtype=np.uint8)
    for i,p in enumerate(piv):x[p]=M[i,n]
    return x,len(free)


def act_columns(B,p):
    out=np.zeros_like(B)
    for i,j in enumerate(p):out[j,:]=B[i,:]
    return out


def main():
    b=build_base();T=b['tritangents'];N=(1-np.asarray(b['M'],dtype=np.uint8))&1
    D4,pairs,supports,_packs=d4_data(b['W'])
    packet_to_tri=coordinate_isomorphism(supports,T)
    P=np.zeros((45,45),dtype=np.uint8)
    for s,t in enumerate(packet_to_tri):P[t,s]=1
    R=np.zeros((27,45),dtype=np.uint8)
    for j,t in enumerate(T):R[list(t),j]=1
    J=np.zeros((90,45),dtype=np.uint8)
    for s,(a,c) in enumerate(pairs):J[a,s]=J[c,s]=1
    N90=(J@P.T@N)&1;R90=(R@P@J.T)&1
    assert rank(N90)==rank(R90)==21 and not np.any((R90@N90)&1)

    # Canonical 24+24 filtration.
    I=col_basis(N90);assert I.shape==(90,21)
    S=J.copy();assert rank(S)==45
    cur=I.copy();rr=21;Acols=[]
    for j in range(45):
        z=S[:,j:j+1]
        if rank(np.concatenate([cur,z],axis=1))>rr:
            Acols.append(z[:,0]);cur=np.concatenate([cur,z],axis=1);rr+=1
    assert len(Acols)==24 and rr==45
    A=np.stack(Acols,axis=1)
    K=nullspace(R90);assert K.shape==(90,69)
    cur=np.concatenate([I,A],axis=1);rr=45;Bcols=[]
    for j in range(K.shape[1]):
        z=K[:,j:j+1]
        if rank(np.concatenate([cur,z],axis=1))>rr:
            Bcols.append(z[:,0]);cur=np.concatenate([cur,z],axis=1);rr+=1
    assert len(Bcols)==24 and rr==69
    B=np.stack(Bcols,axis=1);Full=np.concatenate([I,A,B],axis=1)
    solve=coord_solver(Full)

    # PSp generators on the 90 individual D4 coordinates.
    pts=b['P'];idx={v:i for i,v in enumerate(pts)};qidx={q:i for i,q in enumerate(D4)}
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*groupbase.form(x,v)%3
                y=groupbase.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    gens90=[]
    for gi in (18,62,77,10):
        p=gens40[gi]
        gens90.append(tuple(qidx[frozenset(p[x] for x in q)] for q in D4))

    Egens=[]
    for p in gens90:
        C=solve(act_columns(np.concatenate([A,B],axis=1),p))
        E=C[21:,:]&1;assert E.shape==(48,48)
        assert not np.any(E[24:,:24])
        Egens.append(E)
    Ag=[E[:24,:24] for E in Egens]
    Cg=[E[:24,24:] for E in Egens]
    Bg=[E[24:,24:] for E in Egens]

    # Hom_G(B,A) and extension splitting equations A_g F + C_g = F B_g.
    def equations(with_cocycle):
        rows=[];rhs=[]
        for AA,CC,BB in zip(Ag,Cg,Bg):
            for i in range(24):
                for j in range(24):
                    row=np.zeros(576,dtype=np.uint8)
                    for k in np.flatnonzero(AA[i]):row[k+24*j]^=1
                    for k in np.flatnonzero(BB[:,j]):row[i+24*k]^=1
                    rows.append(row);rhs.append(CC[i,j] if with_cocycle else 0)
        return np.stack(rows),np.array(rhs,dtype=np.uint8)
    MH,_=equations(False);Hbasis=nullspace(MH);homdim=Hbasis.shape[1]
    hranks=sorted(rank(Hbasis[:,k].reshape((24,24),order='F')) for k in range(homdim))
    assert homdim==2 and hranks==[1,10]
    MS,bs=equations(True);split,_free=solve_linear(MS,bs)
    assert split is None

    def fixed_dim(gs,n):
        M=np.concatenate([g^np.eye(n,dtype=np.uint8) for g in gs],axis=0)
        return n-rank(M)
    fixed=[fixed_dim(Ag,24),fixed_dim(Bg,24),fixed_dim(Egens,48)]
    assert fixed==[1,0,1]

    # The independent E8 Z12=1 sector of dimension 48 is not PSp invariant.
    roots=e8_roots_doubled();h=(1,3,9,27,81,243,729,2187)
    simp=simple_roots(roots,h);cm=coeff_map(roots,simp)
    Z4_NODE=3;Z3_NODE=4
    shared={r for r in roots if cm[r][Z4_NODE]%4==1 and cm[r][Z3_NODE]%3==1}
    assert len(shared)==48
    neutral=[r for r in roots if cm[r][Z3_NODE]%3==0]
    ns=simple_roots(neutral,h)
    G=nx.Graph();G.add_nodes_from(range(len(ns)))
    for i,j in itertools.combinations(range(len(ns)),2):
        if dot(ns[i],ns[j])==-4:G.add_edge(i,j)
    e6idx=next(C for C in nx.connected_components(G) if len(C)==6)
    e6=[ns[i] for i in e6idx]
    def refl(x,a):
        q=dot(x,a)//4
        return tuple(x[i]-q*a[i] for i in range(8))
    witness=None
    for a,c in itertools.product(e6,e6):
        if a==c:continue
        for r in shared:
            y=refl(refl(r,a),c)
            if y not in shared:
                witness=(a,c,r,y,cm[y][Z4_NODE]%4,cm[y][Z3_NODE]%3);break
        if witness:break
    assert witness is not None and witness[5]==1 and witness[4]!=1

    out={
      'schema':'w33.20260901.binary-h1-48-nonsplit.v1','status':'PASS',
      'binaryH1':{
        'dimension':48,
        'exactSequence':'0 -> A24 -> H1_48 -> B24 -> 0',
        'A24':'im(J) / im(N90)',
        'B24':'ker(R P) via the pair-sum quotient',
        'extensionSplits':False,
        'Hom_B_to_A_dimension':homdim,
        'deterministicHomBasisRanks':hranks,
        'globalFixedDimensions':{'A24':fixed[0],'B24':fixed[1],'H1_48':fixed[2]},
        'generatorCocycleBlockRanks':[rank(C) for C in Cg],
      },
      'e8Shared48Test':{
        'sector':'Z4=1, Z3=1, dimension 48',
        'PSpInvariant':False,
        'witnessType':'product of two E6 root reflections (even Weyl element)',
        'targetJointGrade':[int(witness[4]),int(witness[5])],
        'consequence':'no PSp-equivariant identification with binary H1_48 as this 48-root subset/carrier'},
      'theorem':'The binary D4-prism H1 is a nonsplit extension of two inequivalent 24-dimensional quotient/kernel modules. The independent E8/Kummer shared 48-sector is not invariant under PSp(4,3), so the matching dimension 48 does not define an intertwiner.',
      'boundary':'This is a characteristic-two module theorem plus a root-set invariance no-go. It does not identify the two 24 factors with ordinary characteristic-zero irreducibles by degree alone.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','H1':48,'filtration':[24,24],
      'split':False,'HomDim':2,'E8shared48Invariant':False},sort_keys=True))

if __name__=='__main__':main()
