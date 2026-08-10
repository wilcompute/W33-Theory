#!/usr/bin/env python3
"""Pass 4753 — exact Wedderburn closure of the 270-residue orbital algebra.

Rebuild the 270 four-line kernel residues and the PSp(4,3) action.  The
centralizer/orbital algebra has dimension 12 and center dimension 9.  An exact
central element has algebra characteristic polynomial

 (x-616)^4 (x-436)(x+68)(x+74)(x+500)(x+578)(x+584)
 ((x-154)^2+108).

The rank-40 central block contains a rational rank-20 idempotent, proving that
it is split M_2(Q), not a quaternion division block.  Hence

 A_Q = Q^6 x Q(sqrt(-3)) x M_2(Q),
 A_C = C^8 x M_2(C).

The script also freezes the primitive rank-24 projector used by Passes 4755
and 4759.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4753_ORBITAL_WEDDERBURN.json'

def mask(S): return sum(1<<i for i in S)

def main():
    pts,pidx,lines,A,apartments,_,_=geometry(); A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1): residues.append(tuple(C))
    assert len(residues)==270
    ridx={r:i for i,r in enumerate(residues)}
    _,G,_=build_groups(pts,pidx,lines); assert len(G)==25920
    def act(i,g): return ridx[tuple(sorted(g[x] for x in residues[i]))]
    H=[g for g in G if act(0,g)==0]; assert len(H)==96
    unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({act(x,h) for h in H});orbs.append(O);unseen-=set(O)
    assert [len(O) for O in orbs]==[1,12,16,48,16,6,24,96,12,12,24,3]
    oi={x:k for k,O in enumerate(orbs) for x in O}
    trans={}
    for g in G:
        x=act(0,g)
        if x not in trans:trans[x]=g
    def inv(p):
        q=[0]*len(p)
        for i,j in enumerate(p):q[j]=i
        return tuple(q)
    def rel(a,b):return oi[act(b,inv(trans[a]))]

    P=np.zeros((12,12,12),dtype=int)
    for k,O in enumerate(orbs):
        y=O[0]
        for z in range(270):P[rel(0,z),rel(z,y),k]+=1
    eq=[]
    for j in range(12):
        for k in range(12):eq.append([int(P[i,j,k]-P[j,i,k]) for i in range(12)])
    center_dim=12-sp.Matrix(eq).rank();assert center_dim==9

    def mul(a,b):
        out=[Fraction(0)]*12
        for i,ai in enumerate(a):
            if not ai:continue
            for j,bj in enumerate(b):
                if not bj:continue
                for k in range(12):
                    if P[i,j,k]:out[k]+=ai*bj*int(P[i,j,k])
        return out
    def add(a,b):return [x+y for x,y in zip(a,b)]
    def scale(a,s):return [s*x for x in a]
    def central(a):return all(mul(a,[Fraction(int(i==j)) for i in range(12)])==mul([Fraction(int(i==j)) for i in range(12)],a) for j in range(12))

    t=[Fraction(x) for x in [2,1,3,-40,5,7,11,19,13,34,19,46]]
    assert central(t)
    LT=sp.zeros(12)
    for j in range(12):
        e=[Fraction(0)]*12;e[j]=1
        y=mul(t,e)
        for k,c in enumerate(y):LT[k,j]=sp.Rational(c.numerator,c.denominator)
    x=sp.symbols('x')
    cp=sp.factor(LT.charpoly(x).as_expr())
    expected=(x-616)**4*(x-436)*(x+68)*(x+74)*(x+500)*(x+578)*(x+584)*(x*x-308*x+23824)
    assert sp.expand(cp-expected)==0

    E40=[Fraction(4,27),Fraction(1,81),Fraction(1,54),Fraction(-11,324),Fraction(1,36),Fraction(-1,324),Fraction(1,81),Fraction(0),Fraction(1,81),Fraction(7,81),Fraction(0),Fraction(2,81)]
    assert central(E40) and mul(E40,E40)==E40 and 270*E40[0]==40
    A11=[Fraction(0)]*12;A11[11]=1
    F20=scale(mul(E40,add(A11,scale(E40,Fraction(2)))),Fraction(1,5))
    assert mul(F20,F20)==F20 and 270*F20[0]==20 and F20!=E40

    E24=[Fraction(4,45),Fraction(2,135),Fraction(1,30),Fraction(2,135),Fraction(-1,45),Fraction(-1,270),Fraction(2,135),Fraction(-1,45),Fraction(2,135),Fraction(2,135),Fraction(-1,45),Fraction(-8,135)]
    assert central(E24) and mul(E24,E24)==E24 and 270*E24[0]==24
    ratios=[c/E24[0] for c in E24]
    assert ratios==[Fraction(1),Fraction(1,6),Fraction(3,8),Fraction(1,6),Fraction(-1,4),Fraction(-1,24),Fraction(1,6),Fraction(-1,4),Fraction(1,6),Fraction(1,6),Fraction(-1,4),Fraction(-2,3)]

    out={'pass':4753,'action':{'degree':270,'rank':12,'subdegrees':[len(O) for O in orbs]},
      'orbital_algebra':{'dimension_Q':12,'center_dimension_Q':9,
        'generic_central_charpoly':'(x-616)^4 (x-436)(x+68)(x+74)(x+500)(x+578)(x+584)(x^2-308x+23824)',
        'quadratic_center_field':'Q(sqrt(-3))','wedderburn_Q':'Q^6 x Q(sqrt(-3)) x M2(Q)','wedderburn_C':'C^8 x M2(C)',
        'matrix_block_split_witness':{'central_rank':40,'rational_noncentral_idempotent_rank':20}},
      'rank24_projector':{'orbital_coefficients':[str(c) for c in E24],
        'normalized_orbit_inner_products':[str(c) for c in ratios]},
      'theorem':'The complete rational residue orbital algebra is Q^6 x Q(sqrt(-3)) x M2(Q). The unique noncommutative simple block is the multiplicity-two degree-20 constituent; the two conjugate scalar constituents form the Eisenstein quadratic center field. A canonical rational primitive rank-24 projector is frozen for the non-coordinate lattice continuation.',
      'boundary':'Exact finite semisimple algebra statement. The Q(sqrt(-3)) factor is a character field, not by itself a physical phase.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
