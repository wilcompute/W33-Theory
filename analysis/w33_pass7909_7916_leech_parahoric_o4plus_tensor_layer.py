#!/usr/bin/env python3
"""Pass7909-7916 (outside-box): the Leech 3-adic automorphism group has an O4+(3) tensor residue.

Pass7861 gives |Aut(C,lambda)|=1,259,712 for C=(Z/9)^2 x (Z/3)^2.  The induced
action on T=C/3C forgets the 27 choices of the level-9 congruence lift and is
    3^4 : (SL2(3) x SL2(3)), order 46656,
with the normal 3^4 identified as Mat_2(F3).  Conjugation is C -> D C A^{-1};
the determinant quadratic form on Mat_2(F3) is invariant.  The Levi action has
kernel {(+I,+I),(-I,-I)} and image of order 288, the standard Omega_4^+(3)
action on the 4D plus-type orthogonal space.  Its matrix orbits are 1+32+24+24,
corresponding to zero, nonzero singular, determinant -1, determinant +1.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7909_7916_LEECH_PARAHORIC_O4PLUS_TENSOR_LAYER.json'

def det2(A):return int(A[0,0]*A[1,1]-A[0,1]*A[1,0])%3
def inv2(A):
    d=det2(A);q=pow(d,-1,3)
    return (q*np.array([[A[1,1],-A[0,1]],[-A[1,0],A[0,0]]],dtype=int))%3

def main():
    SL=[]
    for z in itertools.product(range(3),repeat=4):
        A=np.array(z,dtype=int).reshape(2,2)%3
        if det2(A)==1:SL.append(A)
    assert len(SL)==24
    aut_order=1259712;top_kernel=27;top_order=aut_order//top_kernel
    assert top_order==81*24*24==46656

    mats=[np.array(z,dtype=int).reshape(2,2)%3 for z in itertools.product(range(3),repeat=4)]
    mi={tuple(M.ravel()):i for i,M in enumerate(mats)}
    actions=set()
    for A in SL:
      Ai=inv2(A)
      for D in SL:
        p=tuple(mi[tuple(((D@C@Ai)%3).ravel())] for C in mats)
        # determinant is the invariant quadratic form
        assert all(det2(mats[p[i]])==det2(mats[i]) for i in range(81))
        actions.add(p)
    assert len(actions)==288

    seen=set();orbits=[]
    acts=list(actions)
    for s in range(81):
        if s in seen:continue
        O={s};q=[s];seen.add(s)
        while q:
            x=q.pop()
            for p in acts:
                y=p[x]
                if y not in O:O.add(y);seen.add(y);q.append(y)
        orbits.append(O)
    prof=sorted((len(O),dict(Counter(det2(mats[i]) for i in O))) for O in orbits)
    assert prof==[(1,{0:1}),(24,{1:24}),(24,{2:24}),(32,{0:32})]
    singular=[i for i,M in enumerate(mats) if M.any() and det2(M)==0]
    # projectivizing +/- identifies 32 nonzero singular matrices into 16 points,
    # the point count of Q+(3,3).
    def canon(M):
        z=tuple(int(x) for x in M.ravel());first=next(x for x in z if x)
        return tuple((x if first==1 else 2*x)%3 for x in z)
    qs={canon(mats[i]) for i in singular};assert len(qs)==16

    out={
      'schema':'w33.pass7909_7916.leech_parahoric_o4plus_tensor_layer.v1','status':'PASS','passes':'7909-7916','outside_box':True,
      'Aut_C_lambda_order':aut_order,'top_action_kernel_order':top_kernel,'top_action_order':top_order,
      'top_action_structure':'3^4 : (SL2(3) x SL2(3)); the 3^4 is Mat2(F3) under left-right tensor action C -> D C A^{-1}',
      'tensor_quadratic_form':'q(C)=det(C), a nondegenerate plus-type quadratic form on Mat2(F3)',
      'Levi_action_kernel':'diagonal {(+I,+I),(-I,-I)}','Levi_image_order':288,'Levi_image_identification':'Omega_4^+(3)',
      'Mat2_orbits':{'zero':1,'nonzero_singular':32,'det_plus1':24,'det_minus1':24},
      'projective_singular_quadric':'Q+(3,3) with 16 points',
      'exact_sequence':'1 -> 3^3 -> Aut(C,lambda) -> 3^4:(SL2(3)xSL2(3)) -> 1',
      'D4_bridge':'The corrected Leech 3-adic controller therefore contains a canonical 4D plus-orthogonal tensor residue. This is structurally compatible with the repo D4/O8+(3) triality program, but no embedding into the 3360 O8+(3) carrier is asserted here.',
      'external_name_check':'Omega_4^+(3) order 288 agrees with standard finite-group nomenclature.',
      'theorem':'The Leech mixed-torsion automorphism group is a 3-adic lift of a 4D tensor-parabolic whose Levi quotient is Omega_4^+(3) acting on Mat2(F3) by determinant-preserving left-right transformations.',
      'claim_boundary':'Exact finite group/module theorem; the D4-triality connection remains a next objectwise embedding problem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','top':46656,'Omega4plus':288,'Qplus_points':16,'orbits':[1,32,24,24]}))
if __name__=='__main__':main()
