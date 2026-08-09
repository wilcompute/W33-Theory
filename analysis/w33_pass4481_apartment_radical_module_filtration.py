#!/usr/bin/env python3
"""Pass 4481 -- apartment-code radical module filtration.

Renumbering note: first pushed under 4475; canonical ownership moved to 4481
because reservation d300fa184fa5665fd539f39b2d6ab4b23c08a39d predates the
abandoned 4474--4478 reservation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass158_chiral_trade_lattice_two_480s import build_group, build_w33, w33_lines
from w33_pass161_gq42_ihara_inheritance import small_generating_set
from w33_pass187_f2_layer_sandwich import exhaustive_cyclic_irreducible, subquotient_action_matrices
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT=Path(__file__).resolve().parents[1]
def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def inter(A,B):
    A=rref_rows(A); B=rref_rows(B); rel=nullspace_mod2(np.hstack((A.T,B.T))); out=[]
    for z in rel:
        v=(z[:len(A)]@A)%2
        if v.any(): out.append(v)
    return rref_rows(np.asarray(out,dtype=np.uint8)) if out else np.zeros((0,A.shape[1]),dtype=np.uint8)
def contains(big,small):
    big=rref_rows(big); r=len(big)
    return all(rank2(np.vstack((big,v)))==r for v in rref_rows(small))
def main():
    points,A,symp=build_w33(); lines=w33_lines(A); N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines): N[list(L),li]=1
    Ast=(N.T@N)%2; j=np.ones((1,40),dtype=np.uint8)
    R=rref_rows(nullspace_mod2(N)); I=rref_rows(Ast); K=rref_rows(nullspace_mod2(Ast)); U=inter(R,I); S=rref_rows(np.vstack((R,I)))
    checks={
      'dims':(len(R),len(I),len(U),len(S),len(K))==(15,10,9,16,30),
      'J_in_U':contains(U,j),'R_in_K':contains(K,R),'I_in_K':contains(K,I),'Astar_square_zero':not np.any((Ast@Ast)%2),
      'radical_29':len(K)-1==29,'layers_8_7_14':(len(U)-1,len(S)-len(U),len(K)-len(S))==(8,7,14),
      'middle_6_plus_1':(len(R)-len(U),len(I)-len(U))==(6,1)}
    _,group=build_group(points,symp); pg=small_generating_set(group); idx={frozenset(L):i for i,L in enumerate(lines)}
    lg=[tuple(idx[frozenset(g[p] for p in L)] for L in lines) for g in pg]
    a8,d8=subquotient_action_matrices(U,j,lg); a6,d6=subquotient_action_matrices(R,U,lg); a14,d14=subquotient_action_matrices(K,S,lg); a1,d1=subquotient_action_matrices(I,U,lg)
    ir8,o8=exhaustive_cyclic_irreducible(a8,d8); ir6,o6=exhaustive_cyclic_irreducible(a6,d6); ir14,o14=exhaustive_cyclic_irreducible(a14,d14)
    checks.update({'irred8':d8==8 and ir8,'irred6':d6==6 and ir6,'irred14':d14==14 and ir14,'trivial1':d1==1 and all(int(x[0,0])==1 for x in a1)})
    assert all(checks.values()),checks
    out={'pass':4481,'theorem':'W33 apartment-code radical module filtration theorem','exact_sequence':'0 -> K/J (29) -> C_ap (39) -> H10 (10) -> 0',
      'spaces':{'J':1,'R':15,'I':10,'U':9,'S':16,'K':30},'radical_profile':'8 | (6 + 1) | 14','irreducible_factors':[8,6,14],
      'orbit_scans':{'8':o8,'6':o6,'14':o14},'boundary':'Modular representation dimensions only; no particle interpretation or physical radical-discarding measurement is inferred.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4481_APARTMENT_RADICAL_MODULE_FILTRATION.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
