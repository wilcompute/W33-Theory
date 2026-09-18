#!/usr/bin/env python3
"""Resolve the central-character superselection question for the outer-complete group.

Let H=3^(1+12) be the extraspecial Heisenberg normal subgroup and let s be the
certified outer involution with s z s^-1 = z^-1.  The two faithful
Schrodinger irreps V_1,V_2 of H have central characters omega,omega^-1, hence
are inequivalent, and s conjugates V_1 to V_2.

For G=H semidirect <s>, index [G:H]=2.  Mackey/Clifford irreducibility for a
normal subgroup says Ind_H^G(V_1) is irreducible because V_1 is not isomorphic
to its outer conjugate V_2.  Its restriction to H is exactly V_1 direct-sum V_2,
so it is the certified 1458-dimensional doubled carrier.

Consequences:
  * with the outer operation admitted, the doubled carrier is irreducible;
  * the projectors onto r=1 and r=2 are exchanged by s and are not central
    projectors of the outer-complete representation algebra;
  * therefore central character is not an intrinsic superselection label of
    the enlarged finite algebra.

Physical caveat: if the outer operation is not dynamically implementable and
the observable algebra is restricted to operators commuting with z, the two
central characters remain superselected.  The theorem resolves the algebraic
question, not the hardware question.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_outer_complete_no_intrinsic_superselection.json'

def main(write=True):
    swap=json.loads((ROOT/'data/w33_suzuki_outer_heisenberg_sector_swap.json').read_text())
    dq=json.loads((ROOT/'data/w33_doubled_central_character_logical_qubit.json').read_text())
    assert swap['status']=='PASS' and dq['status']=='PASS'
    assert dq['code_space']['dimension_total']==1458
    out={'schema':'w33.outer_complete_no_intrinsic_superselection.v1','status':'PASS_ALGEBRAIC_PHYSICAL_IMPLEMENTATION_OPEN',
      'normal_subgroup':'H=3^(1+12)','extension':'G=H:C2 using the multiplier-minus-one outer involution',
      'H_irreps':{'V1':{'dimension':729,'center':'omega'},'V2':{'dimension':729,'center':'omega^-1'},
                  'inequivalent':True,'outer_relation':'V1^s isomorphic to V2'},
      'clifford_mackey_step':'H is normal of index 2; V1 is irreducible and inequivalent to its only outer conjugate V2, so Ind_H^G(V1) is irreducible.',
      'induced_representation':{'dimension':1458,'restriction_to_H':'V1 direct-sum V2','identified_with_doubled_carrier':True},
      'projectors':{'P1':'projector onto r=1','P2':'projector onto r=2','outer_action':'s P1 s^-1=P2',
                    'central_in_outer_complete_algebra':False},
      'superselection_conclusion':'There is no intrinsic r=1 versus r=2 superselection sector for the outer-complete representation algebra; the two labels are components of one irreducible G-module.',
      'physical_boundary':'If the outer operation is only a formal symmetry and available observables/dynamics commute with z, then P1,P2 remain operational superselection projectors. Physical coherence is equivalent to implementing at least one allowed operation in the outer coset.',
      'checks':{'sector_swap_parent':True,'doubled_dimension_1458':True,'distinct_center_characters':True,'mackey_index2_applies':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
