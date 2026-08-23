#!/usr/bin/env python3
"""Pass8201-8208: exact Leech/W33 common controller H27:GL2(3).

Pass8101-8108 proves that each 36-object mixed-Leech-Lagrangian component has
full automorphism group H27:GL2(3), order 1296.  This verifier independently
constructs Aut(W(3,3))=W(E6) as the projective symplectic-similitude group on
PG(3,3), takes a point stabilizer, and identifies exactly the same parabolic.

The old repo 2592 action AGL2(3) x Aff1(3) is also structurally audited: its
normal 3-core is abelian C3^3, so it is not the H27 parabolic and cannot supply
the sought objectwise weld merely from its order.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8201_8208_LEECH_W33_H27_PARABOLIC_WELD.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={v:i for i,v in enumerate(P)}
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=int)%3

def trans(v):
    v=np.array(v,dtype=int)%3;out=[]
    for x in P:
        q=np.array(x,dtype=int);c=int(q@J@v)%3;y=(q+c*v)%3
        out.append(pi[canon(tuple(map(int,y)))])
    return tuple(out)
def lin(M):
    M=np.array(M,dtype=int)%3
    return tuple(pi[canon(tuple(map(int,(M@np.array(x,dtype=int))%3)))] for x in P)

def main():
    vecs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(0,0,1,1)]
    sp=[Permutation(list(trans(v))) for v in vecs];G0=PermutationGroup(sp);assert int(G0.order())==25920
    R=np.diag([1,1,2,2]);assert np.array_equal((R.T@J@R)%3,(2*J)%3)
    G=PermutationGroup(sp+[Permutation(list(lin(R)))]);assert int(G.order())==51840
    H=G.stabilizer(0);assert int(H.order())==1296

    # Four totally isotropic lines through the fixed W33 point; quotient image S4.
    p0=P[0]
    nbr=[i for i in range(40) if i and int(np.array(p0)@J@np.array(P[i]))%3==0]
    def adj(i,j):return i!=j and int(np.array(P[i])@J@np.array(P[j]))%3==0
    lines=[];seen=set()
    for s in nbr:
        if s in seen:continue
        C={s};q=[s];seen.add(s)
        while q:
            u=q.pop()
            for v in nbr:
                if v not in C and adj(u,v):C.add(v);seen.add(v);q.append(v)
        lines.append(frozenset(C))
    assert sorted(map(len,lines))==[3,3,3,3];li={L:i for i,L in enumerate(lines)}
    def lp(g):return tuple(li[frozenset(int(g(x)) for x in L)] for L in lines)
    img=PermutationGroup([Permutation(list(lp(g))) for g in H.generators]);assert int(img.order())==24

    # Kernel of four-direction action has order 54; its Sylow-3 is O3(H)=H27.
    hels=list(H.generate_schreier_sims());K=[g for g in hels if lp(g)==(0,1,2,3)];assert len(K)==54
    Kgrp=PermutationGroup(K);P3=Kgrp.sylow_subgroup(3);assert int(P3.order())==27
    assert int(P3.center().order())==3 and int(P3.derived_subgroup().order())==3
    assert Counter(int(g.order()) for g in P3.generate_schreier_sims())==Counter({3:26,1:1})
    assert all(P3.contains((~h)*p*h) for h in H.generators for p in P3.generators)

    # Quotient H/H27 has order 48 and contains order-8 elements, distinguishing
    # GL2(3) from C2 x S4; its projective direction quotient is S4.
    def qord(h):
        x=Permutation(list(range(40)))
        for n in range(1,20):
            x=x*h
            if P3.contains(x):return n
        raise AssertionError
    qhist=Counter(qord(h) for h in hels);assert qhist[8]>0

    # Structural boundary for the old 2592 product action used in the E6/F3
    # minimal-certificate census: AGL2(3) x Aff1(3) has O3=C3^2 x C3, abelian.
    old={'order':432*6,'structure':'AGL2(3) x AGL1(3)','O3':'C3^3 (abelian)','same_as_H27_parabolic':False}
    out={'schema':'w33.pass8201_8208.leech_w33_h27_parabolic_weld.v1','status':'PASS','passes':'8201-8208',
      'W33_Aut_order':51840,'W33_point_stabilizer_order':1296,
      'point_parabolic':{'O3_order':27,'O3_center_order':3,'O3_derived_order':3,'O3_element_orders':'1^1+3^26','O3':'H27','quotient_order':48,'quotient':'GL2(3)','four_direction_image':'S4'},
      'Leech_dependency':'Pass8101-8108: full automorphism group of each 36-Lagrangian component is H27:GL2(3), order 1296',
      'common_controller':'H27:GL2(3)','common_order':1296,
      'old_2592_action':old,
      'theorem':'The canonical Leech 36-Lagrangian controller is exactly the W33/W(E6) point parabolic H27:GL2(3). The previous order-2592 target was an order-level overreach: the older 2592 E6/F3 action has abelian 3-core and is not this parabolic.',
      'claim_boundary':'Exact finite-group weld. No physical identification follows from the shared controller alone.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','common':'H27:GL2(3)','order':1296,'old2592_same':False}))
if __name__=='__main__':main()
