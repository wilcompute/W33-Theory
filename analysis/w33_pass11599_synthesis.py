#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files={
11590:'PART_W33_PASS11590_E8_THREE_SPIN10_FAMILIES.json',
11591:'PART_W33_PASS11591_SPIN10_DELTA54_HESSE_YUKAWA.json',
11592:'PART_W33_PASS11592_Q6_OVERLAP_ADMISSIBILITY.json',
11593:'PART_W33_PASS11593_UNIQUE_WEYL_SELECTOR.json',
11594:'PART_W33_PASS11594_REFINED_GRAVITY_FIREWALL.json',
11595:'PART_W33_PASS11595_NEUTRINO_MAJORANA_CHANNEL.json',
11596:'PART_W33_PASS11596_SPIN10_COUPLING_NORMALIZATION.json',
11597:'PART_W33_PASS11597_FAMILY_CLIFFORD_BREAKING.json',
11598:'PART_W33_PASS11598_CLOCK_FLOQUET_CHIRALITY.json',
}
P={str(k):json.loads((ROOT/'data'/v).read_text()) for k,v in files.items()}
assert P['11590']['chosen_shell_D5_content']['Spin10_16']==48
assert P['11591']['symmetric_family_tensor_dimension']==2
assert P['11592']['scan'][-1]['index']==-36
assert P['11593']['full_Dirac_commutant_dim']==2
assert P['11594']['status'].startswith('FIREWALL_')
assert P['11595']['required_scalar_vev_charges']['sixY']==0
assert P['11596']['TrY2_over_T2']=='5/3'
assert P['11597']['Delta54_invariant_dimension']==2 and P['11597']['Clifford648_invariant_dimension']==0
assert P['11598']['G4_equals_minus_identity_error']<1e-10
out={
 'schema':'w33.pass11590-11599.families-flavor-chirality-gravity.v1',
 'status':'PASS_WITH_CHIRALITY_AND_GRAVITY_FIREWALLS',
 'passes':P,
 '11599':{
   'status':'PASS_SYNTHESIS_THREE_FAMILY_SPIN10_HESSE_FLAVOR_WITH_EXPLICIT_OPEN_BOUNDARIES',
   'architecture':'external A2 family triplet x internal Spin(10) Weyl16 x external 4D overlap spacetime factor',
   'three_family_matter':'one selected E8 (27,3) shell branches to 3*(16+10+1); the three 16s are the exact family candidate',
   'flavor':'Delta(54) permits exactly two symmetric family Yukawa tensors; their Higgs-triplet determinant is a Hesse cubic',
   'flavor_breaking':'full H27:SL(2,3) forbids that cubic Yukawa entirely, so reduction to Delta(54) is necessary',
   'gauge_normalization':'Spin(10) Weyl16 gives TrY^2/T_SU2=5/3 and tree-level unification sin^2(theta_W)=3/8',
   'neutrino':'nu^c Majorana mass requires the unique 126-type symmetric channel with a neutral B-L=-2, T3R=+1 scalar VEV',
   'overlap':'all primitive hypercharge magnitudes 1,2,3,4,6 now have explicitly resolved -q^2 overlap sectors; q=6 is resolved at L=5,m0>=1.7 in the tested background',
   'chirality':'Spin(10)-gauge-invariant selector space is span{I,Chi}; the pure clock cannot select chirality because G^4=-I',
   'gravity':'non-diagonal scalar-curvature integrals become nonzero under refinement, but the spectral heat/curvature coefficient is not yet lattice-size independent',
   'physical_boundary':'The packet does not derive the chiral-shell vacuum choice, the Delta54 breaking potential, measured family Yukawa coefficients/mixings, the 126 VEV scale, RG evolution/thresholds, or an Einstein-Hilbert continuum limit.'
 }
}
(ROOT/'data/PART_W33_PASS11590_11599_FAMILIES_FLAVOR_CHIRALITY_GRAVITY.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out['11599'],indent=2))
