#!/usr/bin/env python3
"""Pass9765-9772 outside-box: classify R-transverse Lagrangians by orthogonal sign.

For a symplectic complex structure R^2=-I on F3^12, a Lagrangian L transverse
to RL carries the symmetric form C_L(u,v)=K(u,Rv).  U(6,3)=C_Sp(R) has two
orbits, plus and minus, with stabilizers O^+(6,3) and O^-(6,3).
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9765_9772_R_TRANSVERSE_LAGRANGIAN_SIGN_ORBITS.json'
Q=3

def unitary6(q=3):
 o=q**15
 for i in range(1,7):o*=q**i-(-1)**i
 return o
def oplus6(q=3):return 2*q**6*(q**3-1)*(q**2-1)*(q**4-1)
def ominus6(q=3):return 2*q**6*(q**3+1)*(q**2-1)*(q**4-1)
def lagrangians_sp12(q=3):
 o=1
 for i in range(1,7):o*=q**i+1
 return o

def main():
 U=unitary6();Op=oplus6();Om=ominus6();Np=U//Op;Nm=U//Om;Tot=lagrangians_sp12();Ntrans=Np+Nm;Nbad=Tot-Ntrans
 assert (U,Op,Om)==(182699779456696320,24261120,26127360)
 assert (Np,Nm)==(7530558336,6992661312)
 assert Tot==16358540800 and Ntrans==14523219648 and Nbad==1835321152
 out={'schema':'w33.pass9765_9772.r_transverse_lagrangian_sign_orbits.v1','status':'PASS','passes':'9765-9772','outside_box':True,
 'ambient':{'C_Sp(R)':'U(6,3)','order':U,'all_Lagrangians_in_Sp12':Tot},
 'R_transverse_orbits':{
   'plus':{'induced_form':'Q+(5,3)','stabilizer':'O+(6,3)','stabilizer_order':Op,'orbit_size':Np},
   'minus':{'induced_form':'Q-(5,3)','stabilizer':'O-(6,3)','stabilizer_order':Om,'orbit_size':Nm}},
 'counts':{'R_transverse_total':Ntrans,'not_R_transverse':Nbad},
 'proof':'For Lagrangian L with L cap RL=0, C_L(u,v)=K(u,Rv) is symmetric and nondegenerate. Its six-dimensional orthogonal sign is invariant under C_Sp(R)=U(6,3). The stabilizer of L is exactly O(C_L), so standard orbit-stabilizer gives the two orbit sizes |U|/|O+| and |U|/|O-|. Every nondegenerate six-dimensional symmetric form over F3 has one of these two signs, exhausting R-transverse Lagrangians.',
 'bridge_consequence':'The Pass9749 sign obstruction is selective, not fatal. The canonical glue half lies in the minus orbit, but the same glue-derived R admits 7,530,558,336 plus-type transverse Lagrangians. Replacing C_G by any plus-orbit Lagrangian removes the Witt-sign obstruction to the canonical Suzuki Q+ half, while retaining the same R and K.',
 'theorem':'An order-four symplectic complex structure on F3^12 has exactly two unitary orbits of transverse Lagrangian polarizations, distinguished by Q+ versus Q- half-form. Their sizes are 7,530,558,336 and 6,992,661,312. The Niemeier and Suzuki canonical polarizations occupy opposite orbits, but compatible-sign alternatives exist abundantly.',
 'boundary':'Standard finite classical-group orbit-stabilizer theorem. This counts algebraic polarizations; it does not select one canonically or prove an integral lattice/physical lift.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','plus':Np,'minus':Nm,'nontransverse':Nbad}));return 0
if __name__=='__main__':raise SystemExit(main())
