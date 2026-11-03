#!/usr/bin/env python3
"""4D overlap lattice resolution and topology-sector stress test for exotic
Q=3(B-L) chiral charges, not a completed interacting Weyl measure.

For uniform U(1) flux 1 in planes 12 and 34, a charge q sees plaquette
phase q*(2pi/L²). Chosen conservative |phase|<pi/3 requires L²>6|q|.
Anomaly-canceling sum q^3=0 does NOT imply vanishing index q² on flux.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
def main():
 src=json.loads((ROOT/'data/toe_20261103_sterile_anomaly_operators.json').read_text())
 qex=[-15,12,12]
 assert qex in src['all_quark_normalized_integer_sectors']
 assert sum(qex)==9 and sum(q**3 for q in qex)==81
 assert src['three_generation_SM_linear_and_cubic'] if 'three_generation_SM_linear_and_cubic' in src else True
 qall=[1,3,9,12,15,18]
 rows=[]
 for q in qall:
  L=2
  while L*L<=6*q:L+=1
  dim=4*L**4
  gib=dim*dim*16/2**30
  maxangle=2*math.pi*q/(L*L)
  assert maxangle<math.pi/3 and 2*math.pi*q/((L-1)**2)>=math.pi/3
  rows.append({'absolute_charge_Q':q,'minimum_L_for_charge_plaquette_angle_below_pi_over_3':L,
    '4D_site_count':L**4,'overlap_spinor_dimension_4L4':dim,
    'dense_complex128_kernel_GiB':gib,'charged_plaquette_angle_radians':maxangle,
    'index_magnitude_on_flux_1_times_1_continuum':q*q})
 assert rows[4]['minimum_L_for_charge_plaquette_angle_below_pi_over_3']==10
 assert rows[5]['minimum_L_for_charge_plaquette_angle_below_pi_over_3']==11
 assert sum(q*q for q in qex)==513
 # distinct anomaly invariants, cannot infer topology index from q³ cancellation.
 out={'status':'PASS_EXACT_EXOTIC_CHARGE_LATTICE_RESOLUTION_AND_TOPOLOGY_FIREWALL',
 'old_fixture':'data/toe_20261103_sterile_anomaly_operators.json',
 'exotic_sterile_Q3BL':qex,'exotic_sterile_charge_sums':
  {'linear':sum(qex),'cubic':sum(x**3 for x in qex),
   'quadratic':sum(x*x for x in qex)},
 'charge_resolution_rows':rows,
 'admissibility_requirement_input':'For benchmark homogeneous flux 1 in a plaquette plane, require |q|*2pi/L²<pi/3 on the unwrapped flux branch, a chosen conservative phase control rather than a universal necessary and sufficient Luescher condition.',
 'zero_mode_index_law':'For a smooth 4D U(1) bundle with c1 = n12 dx12 +n34 dx34, charge q Dirac index = +/-q²*n12*n34, sign depends on conventions. One chirality acquires this index contribution; in an index-nonzero gauge sector a massless square Weyl determinant cannot generically be treated as a nonzero scalar with a fixed basis and no insertions.',
 'doubled_charge_index':'The index is quadratic in representation charge, while the local 4D cubic abelian gauge anomaly is cubic. Anomaly cancellation sum_i q_i³=0 does not remove individual q_i² flux zero-mode multiplicities.',
 'resource_constraint':'Dense 4L^4 by 4L^4 overlap kernel stores O(L^8) complex numbers; achieving stable admissibility for q>=15 exceeds 40,000 spinor dimensions and a 20 GiB dense Hermitian kernel. Sparse Krylov/rational-sign algorithms, sector-aware Weyl bases, and gauge-invariant measure remain needed.',
 'scope':'Exact finite charge sums, chosen angle-bound combinatorics, and standard topological index expectation. We did NOT numerically compute the L10 overlap index (too costly for dense eigensolve), construct a nonperturbative Weyl measure, or settle admissibility of arbitrary gauge backgrounds.',
 'source_prior':['https://arxiv.org/abs/2610.09093',
                 'https://link.springer.com/article/10.1007/JHEP07%282026%29271']}
 (ROOT/'data/toe_20261103_chiral_topological_resolution_guard.json').write_text(json.dumps(out,indent=2)+'\n')
 print('CHIRAL_TOPOLOGY',json.dumps({'quadratic_index_sum':out['exotic_sterile_charge_sums']['quadratic'],
   'rows':rows}),flush=True)
if __name__=='__main__':main()
