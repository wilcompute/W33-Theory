#!/usr/bin/env python3
"""Search the currently certified Suzuki/cubic/A8^3 layers for a non-Clifford gate.

Result: none of the three obvious candidates is an internal non-Clifford
endomorphism of the fixed six-qutrit register.

(1) Three-W33 refactorization moves generate 2.Suz <= Sp(12,3), hence Clifford.
(2) The ten global cubic holonomy channels are exactly the sp4(F3) adjoint,
    again finite symplectic/Clifford-side data.
(3) The Z9 A8^3 simple-current center acts on Lambda^k(9) by the scalar xi^k.
    A scalar ninth root is computationally trivial under conjugation; it is not
    the qutrit T gate.  Moreover the first glue sectors are inter-sector fields
    such as 9 tensor 9 tensor 126, not endomorphisms of the 9^3 ground register.

Control: the genuine qutrit third-level phase T=diag(1,xi,xi^-1), xi^9=1,
satisfies T^3=Z but T X T^-1 is not proportional to any Pauli X Z^k.  Thus a
ninth root CAN support a non-Clifford operation when its phases depend on the
computational basis; the certified A8^3 center phase does not do that.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_nonclifford_extension_search.json'

def main(write=True):
 ref=json.loads((ROOT/'data'/'w33_suzuki_refactorization_compiler.json').read_text());h1=json.loads((ROOT/'data'/'w33_e6_cubic_h1_is_sp4_adjoint.json').read_text());glue=json.loads((ROOT/'data'/'w33_a8_cubed_niemeier_glue.json').read_text())
 assert ref['status']=='PASS' and h1['status']=='PASS' and glue['status']=='PASS'
 # Exponents mod 9 for T=diag(1,xi,xi^-1).
 t=[0,1,8];conjX=[(t[(j+1)%3]-t[j])%9 for j in range(3)]
 # A Pauli X Z^k has input-dependent phase c+3*k*j (mod 9), up to scalar c.
 pauli=[]
 for c in range(9):
  for k in range(3):pauli.append([(c+3*k*j)%9 for j in range(3)])
 T_nonclifford=conjX not in pauli
 T3=[(3*x)%9 for x in t];assert T3==[0,3,6] and T_nonclifford
 # Scalar xi^q I has constant exponent and conjugates X,Z unchanged.
 scalar_conjugation_trivial=True
 dims=[x['finite_SU9_rep_dimensions'] for x in glue['generator_vertex_operators']]
 assert dims==[[9,9,126],[9,126,9],[126,9,9]]
 out={'schema':'w33.nonclifford_extension_search.v1','status':'PASS',
 'headline':'No internal non-Clifford endomorphism is certified by the current three-W33 refactorization, ten-class cubic holonomy, or A8^3 simple-current center layers. Refactorization is 2.Suz Clifford; cubic H1 is sp4(F3) adjoint; and the Z9 center is a sector scalar, while the first glue fields map between representation sectors rather than acting as endomorphisms of the fixed six-qutrit ground register.',
 'candidate_1_refactorization':{'generated_group':'2.Suz','ambient':'Sp(12,3)','result':'Clifford subgroup, not non-Clifford'},
 'candidate_2_cubic_H1':{'module':'sp4(F3) adjoint','dimension':10,'result':'symplectic-adjoint/Clifford-side controller, not a non-Clifford gate by itself'},
 'candidate_3_A8_glue':{'center':'Z9','action_on_Lambda_k':'scalar xi^k','generator_sector_dimensions':dims,'result':'scalar center phase is conjugation-trivial; weight-two simple currents are inter-sector fields, not certified register endomorphisms'},
 'qutrit_T_control':{'xi_order':9,'T_phase_exponents_mod9':t,'T_cubed_phase_exponents':[0,3,6],'T_cubed':'Z','T_X_Tdagger_phase_exponents':conjX,'is_proportional_to_any_XZk':not T_nonclifford,'T_is_nonClifford':T_nonclifford},
 'missing_datum':'An explicit sector-return intertwiner/endormorphism whose conjugation on Pauli generators leaves the Clifford normalizer, or a certified magic-state injection (the blueprint currently keeps M36 magic as an external handshake).',
 'boundary':'This is a no-go only for the presently certified internal candidates. It does not prove no non-Clifford operation exists anywhere in the full VOA/orbifold theory.',
 'checks':{'refactorization_Clifford':True,'H1_sp4':True,'center_scalar_trivial':scalar_conjugation_trivial,'qutrit_T_control_nonClifford':T_nonclifford,'simple_currents_not_ground_register_endomorphisms':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
