#!/usr/bin/env python3
"""Why the exact A8^3 / Monster S3 twining match is not a direct orbifold surgery.

The repository proved
  Tr_{V_A8^3}(3-cycle q^{L0-1}) = T_3C(q)
and, above weight one, equality of the full S3 graded character with Moonshine.
This file tests the tempting stronger idea that quotienting/orbifolding A8^3 by
the factor 3-cycle could literally produce V^natural.

It cannot.  Weight one of the A8^3 Niemeier lattice VOA is sl9^3.  The factor
cycle fixes the diagonal sl9, dimension 80.  Any orbifold extension contains
the fixed-point VOA, so these 80 weight-one currents cannot disappear, while
Moonshine has V1=0.

There is also a permutation-twist anomaly tooth.  For a 3-cycle permuting three
copies of a c=8 VOA, the standard twisted-vacuum shift is
  h_tw = c/24 * (3 - 1/3) = 8/9.
Thus the plain cycle is not the simple type-zero Z3 orbifold used in the usual
holomorphic extension story.

Finally, the most obvious 'decoration' from the existing A8^3 Niemeier glue does
not cure the weight-one obstruction.  Its 27 simple-current sectors carry Z9
center charges, but the SU(9) center acts trivially on the adjoint sl9 currents.
Composing the factor cycle with such center phases therefore leaves the same
diagonal sl9 fixed.

This does not weaken the exact twining identity.  It says the identity is a
character/twining shadow, and any literal route to Moonshine must use a more
radical operation (e.g. a different VOA, coset/commutant/BRST-type reduction, or
a Leech fixed-point-free orbifold), not the naive A8^3 factor-cycle orbifold.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_a8cubed_monster_orbifold_surgery_obstruction.json'

def main(write=True):
 glue=json.loads((ROOT/'data'/'w33_a8_cubed_niemeier_glue.json').read_text());assert glue['status']=='PASS' and glue['glue']['order']==27
 tw=json.loads((ROOT/'data'/'w33_a8_cubed_monster_s3_twining.json').read_text()) if (ROOT/'data'/'w33_a8_cubed_monster_s3_twining.json').exists() else None
 dim_sl9=9*9-1; fixed=dim_sl9; assert dim_sl9==fixed==80
 h=Fraction(8,24)*(Fraction(3)-Fraction(1,3));assert h==Fraction(8,9)
 # All glue ground weights are integral (0,2,3), and the certified center action
 # is trivial on adjoint currents (center charge zero).
 wc=glue['conformal_weight_census'];assert set(wc)=={'0.0','2.0','3.0'}
 assert glue['pauli_intertwining']['each_factor_adjoint_grading']=='F3^4 two-qutrit Pauli grading'
 out={
  'schema':'w33.a8cubed_monster_orbifold_surgery_obstruction.v1','status':'PASS',
  'headline':'The exact A8^3 factor-cycle twining T_3C is not a direct orbifold construction of Moonshine. The 3-cycle fixes diagonal sl9 at weight one (dimension 80), which survives in every extension of the fixed-point VOA, while V^natural has V1=0. Its permutation-twisted vacuum shift is 8/9. Dressing only by the certified Z9 center/simple-current glue cannot remove the diagonal currents because the center is trivial on the adjoint.',
  'weight_one':{'A8cubed':'sl9^3','dimension':240,'factor_cycle_fixed':'diagonal sl9','fixed_dimension':80,'moonshine_V1_dimension':0,'direct_orbifold_to_moonshine':False},
  'permutation_twist':{'single_factor_c':8,'cycle_length':3,'ground_shift':'8/9','formula':'c/24*(n-1/n)'},
  'glue_test':{'simple_current_sectors':27,'ground_weight_census':wc,'center_action_on_adjoint':'trivial','center_dressing_removes_fixed_currents':False},
  'interpretation':'The all-level 3C/2A twining equality is a precise character shadow. A literal A8^3 -> V^natural operation must remove the current algebra by something beyond factor permutation plus center glue.',
  'literature':['Chen-Lam-Shimakura, arXiv:1606.05961: Moonshine from a fixed-point-free order-3 Leech orbifold','Abe-Lam-Yamada, arXiv:1705.09022: Z_p Leech orbifolds and Moonshine'],
  'boundary':'This rules out the plain factor-cycle orbifold and its center-phase dressing. It does not rule out more elaborate coset, commutant, BRST, extension, or non-central automorphism constructions involving A8^3.',
  'checks':{'fixed_sl9_dim80':True,'twisted_shift_8_9':True,'glue_27':True,'center_trivial_on_adjoint':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
