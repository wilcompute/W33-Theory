"""TOE61: six independent W33 mathematics/physics producers, regression checked.

Regenerate exact integer polynomial theorem, manifold incidence no-go,
full native Gauss operator audit, charged flux-gap enclosures, gap stability,
and staggered mass extension. Preserve parallel repo data.
"""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
NAMES=("det_poly","regular3_no_go","charge_gap","full_gauss_audit",
       "staggered_flux","overlap_time")
@pytest.fixture(scope="module")
def certs():
 for name in NAMES:
  p=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe61_{name}.py")],
    cwd=R,capture_output=True,text=True,timeout=180)
  assert p.returncode==0,(name,p.stdout[-800:],p.stderr[-2200:])
 return {name:json.loads((R/"data"/f"w33_20261013_toe61_{name}.json").read_text())
         for name in NAMES}

def test_exact_all_beta_pi_corner_dominance(certs):
 x=certs['det_poly'];rows=x['Z2_character_polynomials']
 assert len(rows)==8 and x['number_three_pi_dominates']==7
 assert len(x['coefficientwise_partial_order'])>=14
 for r in rows:
  assert len(r['full_det_coefficients_decimal'])==41
  assert len(r['full_difference_from_zero_decimal'])==41
  assert all(int(v)>=0 for v in r['full_difference_from_zero_decimal'])
  if r['corner']!=[0,0,0]:
   assert r['first_nonzero_difference_degree']==4
   assert r['negative_coefficient_count']==0
 assert all(any(int(v)>0 for v in r['full_difference_from_zero_decimal']) for r in rows[1:])

def test_exact_Newton_identity_matches_prior_W33_octagon_moment(certs):
 x=certs['det_poly']
 bridges=x['exact_Newton_bridge_to_TOE59_octagon_H8']
 assert len(bridges)==7
 for r in bridges:
  assert r['delta_e4_exact']==-r['delta_trH8_exact']//8
 assert next(r['delta_e4_exact'] for r in bridges if r['corner']==[1,1,1])==932

def test_coefficientwise_three_pi_dominates_every_corner(certs):
 x=certs['det_poly']
 domin=[tuple(q['dominated']) for q in x['coefficientwise_partial_order']
        if q['dominating']==[1,1,1]]
 assert len(domin)==7 and len(set(domin))==7
 assert 'ALL beta>0' in x['theorem']

def test_native_regular_three_manifold_cell_incidence_no_go(certs):
 x=certs['regular3_no_go'];f=x['actual_cell_counts'];m=x['conditional_manifold_target']
 assert f['regular_octagon_faces']==1382 and f['formal_zero_boundary_commutator_faces_excluded']==3
 assert f['unique_signed_face_boundaries_up_to_orientation']==1382
 assert f['all_declared_face_length_counts']=={'0':3,'8':1382}
 assert f['two_skeleton_rational_betti']==[1,3,1304,0]
 assert m['required_3cells_if_closed_3manifold_no_higher_cells']==1302
 assert m['required_3boundary_rank_for_T3_homology']==1301
 assert m['max_3cells_by_double_counting']==921
 assert m['minimum_octagon_faces_to_discard_under_these_conditions']==1142
 assert 'NOT prohibit' in x['limitations']

def test_full_Gauss_operator_audit_zero_rows_and_fermion_hops(certs):
 x=certs['full_gauss_audit']
 assert x['declared_wilson_rows']==1385
 assert x['nonidentity_native_wilson_flux_shifts']==1382
 assert x['exact_identity_rows']==[1382,1383,1384]
 assert x['pairwise_unique_active_plaquette_shifts_up_to_sign']==1382
 assert x['tested_nonzero_fermion_hops']==160
 assert x['exact_gauss_invariance_of_all_plaquette_shifts']
 assert x['exact_local_gauss_invariance_of_all_160_fermion_hops']

def test_charged_infinite_three_loop_schur_intervals_positive(certs):
 x=certs['charge_gap']
 assert x['native_3_loop_Gram']==[[8,-4,-4],[-4,8,4],[-4,4,8]]
 for record in x['cases']:
  assert [q['states'] for q in record['neutral']]==[729,1331,2197]
  assert [q['states'] for q in record['charged']]==[729,1331,2197]
  assert record['charge_excitation_gap_numeric_interval'][0]>0
  assert record['charge_excitation_gap_numeric_interval'][1]>record['E_q_minus_E_zero_at_N6']>record['charge_excitation_gap_numeric_interval'][0]
  assert all(q['ground_eigenvector_residual']<1e-8 for q in record['charged'])
 assert x['cases'][0]['charge_excitation_gap_numeric_interval'][0]>.12
 assert x['cases'][1]['charge_excitation_gap_numeric_interval'][0]>.59
 assert 'not outward-rounded' in x['precision'].lower()

def test_uniform_staggered_mass_extends_exact_all_beta_ordering(certs):
 x=certs['staggered_flux']
 assert x['numeric_test_count']==20
 assert all(q['three_pi_minus_second_best']<0 for q in x['samples'])
 assert 'ANY real staggered mass m' in x['conditional_exact_theorem']
 assert 'continuous U1' in x['physics_limits']

def test_native_overlap_static_time_slices_have_zero_index(certs):
 x=certs['overlap_time'];rows=x['rows']
 assert x['actual_W33_spinor_band_count']==320
 assert len(rows)==12
 assert all(r['local_signature']==0 and r['Hermitian_gap']>.45 for r in rows)
 assert max(r['reflection_pairing_error'] for r in rows)<1e-10
 assert 'NOT a Dirac index' in x['physics_boundary']

def test_scope_no_claim_of_solved_toe(certs):
 assert 'physical CP' in certs['det_poly']['novelty_limit']
 assert 'not a full' in certs['charge_gap']['physics_scope'].lower() or 'no full' in certs['charge_gap']['physics_scope'].lower()
 assert 'does NOT prove' in certs['regular3_no_go']['limitations']
