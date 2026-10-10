"""Round30 five research-front and single-fault extraction regressions."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe30_explicit_cover_girth10 as cover
import w33_20261009_toe30_cat_prep_faults as rawcat
import w33_20261009_toe30_verified_cat_CZ as cat
import w33_20261009_toe30_G2_full_subgroup_nogo as g2
import w33_20261009_toe30_finite_ads_Z_clock as clock
import w33_20261009_toe30_C8_readout_feasibility as c8
def check_frozen(result,name):
 expected=json.loads((ROOT/'data'/f'w33_20261009_toe30_{name}.json').read_text())
 assert json.loads(json.dumps(result))==expected
def test_explicit_connected_83_fold_girth10_W33_cover_hgp():
 r=cover.build()
 check_frozen(r,'explicit_girth10_cover')
 assert r['prime_degree']==83 and r['certified_girth']==10
 assert r['zero_holonomy_base_eight_cycles']==0
 assert len(r['voltages'])==160 and len(r['length10_witness_vertex_indices'])==10
 assert r['connected_lift_vertices']==6640
 assert r['HGP_parameters']=='[[220434721,44102881,10]]_3'
 assert r['HGP_max_check_weight']==6
def test_GHZ_fanout_single_fault_data_hook_support_before_verification():
 r=rawcat.run()
 check_frozen(r,'cat_prep_singlefault')
 assert r['exhaustive_Pauli_fault_enumeration']['WilsonZ']['max_logical_equivalent_data_weight']['fanout']<=2
def test_full_verified_GHZ_CZ_single_faults_all_stabilizers():
 r=cat.run()
 check_frozen(r,'verified_cat_CZ')
 assert r['total_two_qutrit_ops']==3347
 assert r['total_verified_cat_ancillas']==1753
 assert all(q['maximum_data_error_weight_modulo_measured_stabilizer']<=1 for q in r['details'].values())
 assert sum(q['accepted_single_faults']+q['rejected_single_faults'] for q in r['details'].values())==275408
def test_no_PSp4_3_homomorphism_to_complex_G2_and_E8_mixed_branch():
 r=g2.run()
 check_frozen(r,'G2_full_subgroup_nogo')
 assert r['no_nontrivial_G_homomorphism_to_G2C']
 assert r['Steinberg81_multiplicity_through_any_F4xG2_embedding']==0
 assert r['all_seven_dimension_sum_candidates']==[[1]*7,[1,1,5],[1,6]]
def test_finite_ads_external_time_has_no_expanding_lightcone():
 r=clock.run()
 check_frozen(r,'finite_ads_Z_clock')
 assert r['future_support_size_after_exact_steps'][1]==20
 assert r['future_support_size_after_exact_steps'][2]==81
 assert r['exact_two_step_path_counts']=={'diagonal':20,'lightlike':1,'nonlightlike':6}
 assert r['random_walk_mixing_and_return'][-1]['square_L2_dist_from_uniform']<1e-9
def test_C8_readout_preference_can_invert_under_contrast_and_reset():
 r=c8.run()
 check_frozen(r,'C8_readout_feasibility')
 assert len(r['scenario_grid'])==27
 assert any(q['faster_protocol']=='IQ' for q in r['scenario_grid'])
 assert any(q['faster_protocol']=='direct' for q in r['scenario_grid'])
 assert r['idealized_first_gap_MHz']>.17
