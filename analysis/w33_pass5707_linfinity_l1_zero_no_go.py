#!/usr/bin/env python3
"""Pass5707: correct the firewall L-infinity claim at the arity-3 identity.

The existing builder explicitly declares l_1=0 while using a firewall-filtered
l_2 with nonzero Jacobiator and claiming l_3 repairs it. In an ordinary uncurved
L_infinity algebra the n=3 identity has the schematic form

  l1(l3(x,y,z)) + l2(l2(x,y),z)+cyclic
  + l3(l1(x),y,z)+cyclic = 0.

Consequently, if l1=0 then Jacobi(l2)=0 strictly. A nonzero l3 cannot repair a
nonzero l2 Jacobiator. The repo's later CE-2-cochain solver is a meaningful
bracket-deformation/coboundary calculation, but it is not the advertised minimal
l1=0 L_infinity mechanism.

A valid homotopy repair must introduce a nonzero differential on an extended
degree (so l1*l3 can hit the Jacobiator), use a curved/other higher structure with
its correct identities, or modify l2 itself by a CE coboundary. Until such an l1
is specified, the 'dimension of l3 repair freedom' is not a missing rank: for the
stated l1=0 model the repair set is empty whenever J(l2) != 0.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5707_LINFINITY_L1_ZERO_NO_GO.json'
BUILDER=ROOT/'tools/build_linfty_firewall_extension.py'
WELD=ROOT/'analysis/w33_pass5684_collision_linfinity_support_weld.py'

def main():
    b=BUILDER.read_text(encoding='utf-8');w=WELD.read_text(encoding='utf-8')
    declares_zero=('l_1 = 0' in b or 'l_1=0' in b);assert declares_zero
    claims_anomaly=('Jacobi anomaly' in b or 'Jacobiator' in b) and ('cross-terms' in w or 'Jacobiator' in w);assert claims_anomaly
    claims_l3=('l_3' in b and ('restoring coherence' in b or 'absorbed' in b));assert claims_l3
    # This is the coefficient structure of the standard n=3 L_infinity identity;
    # if every l1 term vanishes, the surviving l2 o l2 sum is exactly Jacobi(l2).
    terms={'l1_l3':1,'l2_l2_cyclic':1,'l3_l1_cyclic':1}
    with_l1_zero={'l1_l3':0,'l2_l2_cyclic':1,'l3_l1_cyclic':0}
    assert sum(with_l1_zero.values())==1
    out={
      'pass':5707,'status':'CORRECTION__NONZERO_FIREWALL_JACOBIATOR_CANNOT_BE_REPAIRED_BY_L3_WHEN_L1_IS_ZERO',
      'repo_evidence':{'builder':'tools/build_linfty_firewall_extension.py','builder_declares_l1_zero':declares_zero,'builder_claims_l3_repair':claims_l3,'firewall_nonjacobi_evidence':'Pass5684 and builder both treat firewall l2 as having a nonzero Jacobi anomaly'},
      'arity3_identity':'l1(l3)+sum_cyclic l2(l2)+sum_cyclic l3(l1,...)=0 (up to convention-dependent signs)',
      'specialization_l1_zero':'sum_cyclic l2(l2)=0; l2 must obey strict Jacobi and l3 drops out of the arity-3 identity',
      'repair_space_in_stated_model':'EMPTY for any triple with J_l2 != 0; there is no l3 coefficient choice to solve 0*l3=-J',
      'required_repair_options':[
        'introduce an extended graded space with nonzero l1 whose image contains the firewall Jacobiator, then solve l1(l3)=-J',
        'modify l2 by a genuine Chevalley-Eilenberg coboundary/deformation so the modified bracket satisfies the intended identity',
        'specify a different curved/higher algebraic structure and verify its actual identities rather than calling the l1=0 object an ordinary L_infinity algebra'
      ],
      'minimal_extension_statement':'If a new differential l1:Y->g is introduced, existence requires im(J) subset im(l1). Any solution l3 is then affine over ker(l1); therefore the repair-freedom dimension cannot be stated until l1 and the exact Jacobiator image are specified.',
      'CE2_reinterpretation':'The later local CE2 alpha machinery computes coboundaries built from l2 and can be useful as a deformation solver. That CE differential is not the unary L_infinity bracket l1, so it does not cure the stated l1=0 arity-3 contradiction.',
      'physics_boundary':'This is an algebraic consistency correction. All confinement/QCD readings attached to the old l1=0 l3 story are unsupported until a valid higher-algebra model is constructed.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
