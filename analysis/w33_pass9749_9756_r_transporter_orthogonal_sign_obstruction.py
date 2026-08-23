#!/usr/bin/env python3
"""Pass9749-9756: sharpen the Niemeier-to-Suzuki R transporter problem.

Both sides have a 12D symplectic space, an order-four exchanger squaring to -I,
and a 6+6 Lagrangian polarization.  The induced six-dimensional symmetric forms,
however, have opposite orthogonal sign.  This is an exact obstruction to a
transporter preserving the canonical polarizations.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
OUT=ROOT/'data/PART_W33_PASS9749_9756_R_TRANSPORTER_ORTHOGONAL_SIGN_OBSTRUCTION.json'
P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 for x in v:
  if x:
   z=pow(x,-1,P);return tuple(z*y%P for y in v)
 raise ValueError

def main():
 glue=json.loads((ROOT/'data/PART_W33_PASS9505_9512_DOUBLE_MINUS_ORTHOGONAL_POLARIZATION.json').read_text())
 suz=json.loads((ROOT/'data/PART_W33_PASS9093_9100_SUZUKI_QPLUS53_W33_SELECTOR.json').read_text())
 assert glue['bulk']=='(F3^12,B) has orthogonal type O+(12,3)'
 assert glue['each_half_Qminus_census']['singular_projective_points']==112
 assert suz['polarization']['both_Lagrangian'] is True and suz['symmetric_form_C']['singular_projective_points']==130
 # Recheck the Suzuki exchanger x directly: it is symplectic and x^2=-I.
 from scripts.w33_2suz_sp12_embedding import analyze as analyze_2suz
 from scripts.w33_2suz_m12_2_subgroup import build_m12_2_generators_from_suz,_standard_symplectic_form
 rep=analyze_2suz();assert rep.get('available') is True
 std=rep['standardized_generators'];a=np.array(std['A_std_mod3'],dtype=np.int64)%P;b=np.array(std['B_std_mod3'],dtype=np.int64)%P
 J=_standard_symplectic_form(6,p=P);x=build_m12_2_generators_from_suz(a,b,p=P)['x'];I=np.eye(12,dtype=np.int64)%P
 assert np.array_equal(x.T@J@x%P,J) and np.array_equal(x@x%P,(-I)%P)
 out={'schema':'w33.pass9749_9756.r_transporter_orthogonal_sign_obstruction.v1','status':'PASS','passes':'9749-9756',
 'glue_package':{'exchange':'R','R_squared':'-I','canonical_half_form':'Q^-(5,3)','singular_points':112,'both_halves_Lagrangian':True},
 'Suzuki_package':{'exchange':'x','x_squared':'-I (rechecked from vendored ATLAS matrices)','canonical_half_form':'Q^+(5,3)','singular_points':130,'both_halves_Lagrangian':True},
 'obstruction_proof':'Assume a symplectic T sends the glue canonical half C_G to the Suzuki canonical half U and conjugates R to x. The induced form K(g,Rh) is then carried by congruence to J(Tg,xTh). Congruence preserves the projective singular-point count and hence orthogonal sign. But the glue half has 112 singular points (minus type) and the Suzuki half has 130 (plus type), contradiction.',
 'consequence':'There is NO polarization-compatible symplectic transporter (K,R,C_G) -> (J,x,U). Hall-Janko endpoint orientation cannot repair this because it contributes only a C2 orientation quotient, whereas the obstruction is the six-dimensional orthogonal Witt sign. A successful weld must change the selected Lagrangian on at least one side: choose a plus-type R-transverse Lagrangian in the glue space or a minus-type x-transverse Lagrangian in the Suzuki space.',
 'theorem':'The missing R weld is not merely an unconstructed isometry: with the presently canonical polarizations it is impossible. The glue and Suzuki order-four exchangers have the same formal symplectic role, but their distinguished Lagrangians lie in opposite orthogonal-sign orbits, Q^-(5,3) versus Q^+(5,3).',
 'boundary':'This no-go applies to transporters that preserve both the exchanger and the currently distinguished Lagrangian half. It does not rule out conjugating R to x after replacing the polarization on one side.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','glue_singular':112,'Suzuki_singular':130,'compatible_transporter':False}));return 0
if __name__=='__main__':raise SystemExit(main())
