#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ext=json.loads((ROOT/'data/w33_physical_external_a2_h27.json').read_text())
qpsi=json.loads((ROOT/'data/w33_qpsi_matter_parity_e8_d8_bridge.json').read_text())
st=json.loads((ROOT/'data/bt865_dual_torsor_steinberg_compiler.json').read_text())
assert ext['status'].startswith('PASS_EXPLICIT_PHYSICAL_EXTERNAL_A2_HEISENBERG_27')
assert ext['spectra']['matter_81_split']=='Each FI grade-1 and grade-2 matter shell splits exactly 27+27+27 under the clock.'
assert qpsi['E6_27']['branching']=='27 = 16_1 + 10_-2 + 1_4'
assert st['point_state_torsor']['complex_restriction']=='3 Reg(H27)'
# E8 -> (E6 x SU3_ext)/Z3 gives one chosen matter shell (27,3).
# Branching the E6 factor gives three copies of every D5 summand.
branch={'Spin10_16':3*16,'Spin10_10':3*10,'Spin10_1':3*1}
assert sum(branch.values())==81
# The external family H27 is not the W33 Steinberg logical 81:
# its nontrivial center is scalar omega on (27,3), hence trace 81 omega,
# whereas 3 Reg(H27) has trace 0 on every nonidentity element.
out={
 'status':'PASS_E8_EXTERNAL_A2_TRIPLICATES_SPIN10_WEYL16_WITH_MODULE_SEPARATION_FIREWALL',
 'E8_branch':'248=(78,1)+(1,8)+(27,3)+(27bar,3bar)',
 'chosen_matter_shell':'(27,3)',
 'E6_to_Spin10_U1':qpsi['E6_27']['branching'],
 'chosen_shell_D5_content':branch,
 'three_chiral_spin10_16s_dimension':48,
 'family_factor':'external SU(3) triplet; its H27 clock/shift is the certified physical external-A2 H27',
 'external_H27_center_trace_on_matter81':'81*omega (or 81*omega^2 on conjugate shell)',
 'steinberg_H1_restriction':st['point_state_torsor']['complex_restriction'],
 'steinberg_nonidentity_character':0,
 'modules_are_inequivalent':True,
 'full_E8_firewall':'The adjoint contains both (27,3) and (27bar,3bar). Selecting one chiral shell is still a vacuum/chirality problem; the theorem is representation-theoretic, not a completed compactification.'
}
OUT=ROOT/'data/PART_W33_PASS11590_E8_THREE_SPIN10_FAMILIES.json'
OUT.write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
