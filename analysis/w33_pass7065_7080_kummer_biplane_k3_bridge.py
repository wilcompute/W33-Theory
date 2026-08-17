#!/usr/bin/env python3
"""Passes 7065--7080: exact abstract Kummer-configuration bridge.

The Pass7001 bent extension D=<RM(1,4),q0> has sixteen minimum supports.
This verifier identifies that biplane explicitly with the classical 4x4
row/column model of the Kummer 16_6 configuration.

Internal proof:
  * q0=x0*x1+x2*x3 has six-point support S;
  * the 16 minimum blocks are the translates S+a;
  * an explicit M in GL(4,2) sends S to the six-point 'cross' consisting of
    the three nonzero points in row 0 and the three nonzero points in column 0;
  * therefore M sends S+a to the row/column cross centred at M a, giving an
    explicit incidence isomorphism to the standard 4x4 Kummer model;
  * the Levi graph is explicitly isomorphic to the antipodal quotient of Q6
    (the folded 6-cube), with a frozen 32-vertex bijection checked edgewise.

Literature is deliberately not encoded as an executable premise.  The report
records the exact combinatorial result; manuscript text separately cites the
primary Kummer/K3 and spinor-tenfold literature.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7065_7080_KUMMER_BIPLANE_K3_BRIDGE.json'

V=[tuple((i>>j)&1 for j in range(4)) for i in range(16)]
VID={x:i for i,x in enumerate(V)}
M=np.array([
 [1,1,0,1],
 [1,1,1,0],
 [1,0,1,1],
 [1,1,0,0],
],dtype=np.uint8)

# Frozen explicit isomorphism from the 32-vertex Levi graph to antipodal
# classes of Q6.  Representatives are integers 0..31; x and x^63 represent
# the same folded-cube vertex.
POINT_TO_FQ6=[0,6,10,12,30,24,20,18,17,23,27,29,15,9,5,3]
BLOCK_TO_FQ6=[13,11,7,1,19,21,25,31,28,26,22,16,2,4,8,14]


def add(a,b): return tuple(int(x)^int(y) for x,y in zip(a,b))

def q0(x): return (x[0]*x[1]+x[2]*x[3])%2

def lin(x):
    y=(M@np.array(x,dtype=np.uint8))%2
    return tuple(int(z) for z in y)

def rank2(A):
    A=np.array(A,dtype=np.uint8).copy(); r=0
    for c in range(A.shape[1]):
        piv=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if piv is None: continue
        A[[r,piv]]=A[[piv,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return r

def cross(center):
    r,c=center[:2],center[2:]
    return frozenset(
        x for x in V
        if x!=center and (x[:2]==r or x[2:]==c)
    )

def folded6_adj(a,b):
    # representatives of antipodal pairs {x,x^63}; adjacency means some
    # representatives are Hamming distance one.
    A=(a,a^63); B=(b,b^63)
    return any((x^y).bit_count()==1 for x in A for y in B)

def main():
    assert rank2(M)==4
    S=frozenset(x for x in V if q0(x)==1)
    X0=cross((0,0,0,0))
    assert len(S)==len(X0)==6
    assert frozenset(lin(x) for x in S)==X0

    qblocks={a:frozenset(x for x in V if q0(add(x,a))==1) for a in V}
    kblocks={a:cross(a) for a in V}
    assert len(set(qblocks.values()))==len(set(kblocks.values()))==16

    # Explicit labelled incidence isomorphism: a block translated by a maps
    # to the row/column cross centred at M a.
    for a,B in qblocks.items():
        assert frozenset(lin(x) for x in B)==kblocks[lin(a)]

    # Biplane checks in the Kummer grid model.
    assert Counter(len(A&B) for A,B in __import__('itertools').combinations(kblocks.values(),2))==Counter({2:120})
    assert set(Counter(x for B in kblocks.values() for x in B).values())=={6}

    # Verify frozen folded-Q6 isomorphism edge by edge, including nonedges.
    assert len(set(POINT_TO_FQ6+BLOCK_TO_FQ6))==32
    for u in POINT_TO_FQ6+BLOCK_TO_FQ6:
        assert 0<=u<32
    for xi,x in enumerate(V):
        for ai,a in enumerate(V):
            incident=x in qblocks[a]
            fq=folded6_adj(POINT_TO_FQ6[xi],BLOCK_TO_FQ6[ai])
            assert incident==fq
    # same-side pairs must be nonadjacent because the folded Q6 stays bipartite
    for arr in (POINT_TO_FQ6,BLOCK_TO_FQ6):
        for i in range(16):
            for j in range(i+1,16):
                assert not folded6_adj(arr[i],arr[j])

    # Folded-Q6 spectrum follows from direct 32x32 adjacency calculation.
    A=np.zeros((32,32),dtype=int)
    reps=POINT_TO_FQ6+BLOCK_TO_FQ6
    for i in range(32):
        for j in range(i+1,32):
            if folded6_adj(reps[i],reps[j]): A[i,j]=A[j,i]=1
    assert np.all(A.sum(axis=1)==6)
    vals=np.linalg.eigvalsh(A)
    spec=Counter(round(float(v),8) for v in vals)
    assert spec==Counter({-2.0:15,2.0:15,-6.0:1,6.0:1})

    report={
      'passes':list(range(7065,7081)),
      'quadratic_model':{
        'q0':'x0*x1+x2*x3',
        'support_size':6,
        'minimum_blocks':'{supp(q0(x+a)): a in F2^4}',
        'block_count':16
      },
      'explicit_GL4_isomorphism':{
        'matrix':M.astype(int).tolist(),
        'target_model':'4x4 row/column cross: for each point, the other 3 points in its row plus the other 3 in its column',
        'verified_all_16_blocks':True
      },
      'kummer_configuration':{
        'abstract_parameters':'16_6 symmetric 2-(16,6,2)',
        'each_two_blocks_intersect':2,
        'each_point_degree':6,
        'aut_group_from_Pass7001':'2^4:Sp(4,2) ~= 2^4:S6, order 11520',
        'status':'EXPLICIT_ABSTRACT_ISOMORPHISM_TO_STANDARD_ROW_COLUMN_KUMMER_MODEL'
      },
      'levi_graph':{
        'model':'folded 6-cube Q6/{x~x+111111}',
        'vertices':32,'degree':6,'edges':96,
        'spectrum':{'6':1,'2':15,'-2':15,'-6':1},
        'frozen_point_representatives':POINT_TO_FQ6,
        'frozen_block_representatives':BLOCK_TO_FQ6,
        'edgewise_isomorphism_verified':True
      },
      'k3_boundary':'The executable theorem is an abstract incidence isomorphism. Primary literature identifies this standard 16_6 configuration as the node/trope Kummer configuration whose quartic minimal resolution is a K3 surface. A specific projective embedding/quartic equation and a chain map into the repo 45-point curvature precomplex are not constructed here.',
      'status':'ABSTRACT_KUMMER_CONFIGURATION_IDENTIFIED__PROJECTIVE_K3_AND_CURVATURE_REALIZATION_OPEN'
    }
    OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__': main()
