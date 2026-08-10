#!/usr/bin/env python3
"""Pass 4777 — explicit matrix units in the unique M2(Q) residue block.

This refines Pass4753 from an abstract Wedderburn factor to literal matrix units.
The cold orbital supplies the off-diagonal intertwiners between the two rank-20
minimal idempotents.  The PGSp/PSp outer involution fixes the entire M2 block
pointwise; its nontrivial orbital action is the transposition of orbitals 8 and 9.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4777_MATRIX_UNITS_OUTER.json'

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    ridx={r:i for i,r in enumerate(residues)}
    _,G,F=build_groups(pts,pidx,lines);assert (len(G),len(F))==(25920,51840)
    def act(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    H=[g for g in G if act(0,g)==0];assert len(H)==96
    unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({act(x,h) for h in H});orbs.append(O);unseen-=set(O)
    assert [len(O) for O in orbs]==[1,12,16,48,16,6,24,96,12,12,24,3]
    oi={x:k for k,O in enumerate(orbs) for x in O};trans={}
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
    def basis(k):return [Fraction(int(i==k)) for i in range(12)]
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
    Z=[Fraction(0)]*12
    E40=[Fraction(4,27),Fraction(1,81),Fraction(1,54),Fraction(-11,324),Fraction(1,36),Fraction(-1,324),Fraction(1,81),Fraction(0),Fraction(1,81),Fraction(7,81),Fraction(0),Fraction(2,81)]
    Ahot=basis(11);Acold=basis(1)
    e11=scale(mul(E40,add(Ahot,scale(E40,Fraction(2)))),Fraction(1,5))
    e22=add(E40,scale(e11,Fraction(-1)))
    e12=mul(mul(e11,Acold),e22)
    raw21=mul(mul(e22,Acold),e11)
    assert mul(e12,raw21)==scale(e11,Fraction(324,25))
    assert mul(raw21,e12)==scale(e22,Fraction(324,25))
    e21=scale(raw21,Fraction(25,324))
    U=[[e11,e12],[e21,e22]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    got=mul(U[i][j],U[k][l]);want=U[i][l] if j==k else Z
                    assert got==want
    assert add(e11,e22)==E40

    # Any element of the outer PGSp coset induces the same permutation of G-orbitals.
    outer=next(iter(set(F)-set(G)))
    operm=[]
    for k,O in enumerate(orbs):
        a,b=act(0,outer),act(O[0],outer)
        operm.append(rel(a,b))
    assert operm==[0,1,2,3,4,5,6,7,9,8,10,11]
    def outer_alg(x):
        y=[Fraction(0)]*12
        for k,c in enumerate(x):y[operm[k]]+=c
        return y
    assert all(outer_alg(x)==x for row in U for x in row)

    out={'pass':4777,'matrix_block':{'central_rank':40,'minimal_ranks':[20,20],
      'matrix_units':{'e11':[str(x) for x in e11],'e12':[str(x) for x in e12],
                      'e21':[str(x) for x in e21],'e22':[str(x) for x in e22]},
      'offdiagonal_normalization':'e12=e11*A_cold*e22; e21=(25/324)e22*A_cold*e11',
      'relations':'e_ij e_kl = delta_jk e_il'},
      'outer_action':{'orbital_permutation':operm,'swapped_orbitals':[8,9],
        'matrix_units_fixed_pointwise':True,
        'conclusion':'the PGSp/PSp outer twist is not carried by the multiplicity-two M2(Q) block'},
      'theorem':'The unique noncommutative factor of the 270-residue orbital algebra is exhibited by literal rational matrix units. The outer involution fixes this M2(Q) factor pointwise and acts nontrivially elsewhere by transposing the paired orbitals 8 and 9.',
      'boundary':'Exact rational orbital-algebra statement.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
