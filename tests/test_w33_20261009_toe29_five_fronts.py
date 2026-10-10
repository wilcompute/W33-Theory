"""Round29 regression of five executed fronts and new parallel finite AdS4."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe29_cat_hook_certificate as hook
import w33_20261009_toe29_cover_hgp_growth as cover
import w33_20261009_toe29_e7_branch_obstructions as e8
import w33_20261009_toe29_ads_causality as ads
import w33_20261009_toe29_c8_spectroscopy_comparator as spec
def frozen(name):
 return json.loads((ROOT/'data'/f'w33_20261009_toe29_{name}.json').read_text())
def test_transversal_ancilla_single_data_coupling_fault():
 r=hook.run();assert r==frozen('hook_cat_layer')
 assert r['exhaustive_single_after_SUM_Pauli_faults']==76480
 assert r['naive_sequential_data_error_max']==8
 assert r['independent_cat_transversal_data_error_max']==1
 assert r['cat_data_layer_ancilla_count']==956
def test_W33_normal_finite_cover_hgp_rate_one_fifth_unbounded_girth_existence():
 r=cover.run();assert r==frozen('graph_cover_hgp_family')
 assert r['cycle_group']=='pi1(G) is free group F_(e-v+1)=F_81'
 assert r['explicit_parameters'][0]['HGP_k']==6561
 assert r['explicit_parameters'][-1]['rate']>.199
 assert all(x['girth']==8 for group in r['random_cyclic_cover_samples'].values() for x in group)
def test_E7_three_major_subgroup_hosts_obstruct_steinberg81():
 r=e8.run();assert r==frozen('e7_exceptional_character_screen')
 assert [x['largest_block'] for x in r['full_E8_branching_tests'].values()]==[78,70,66]
 assert all(x['Steinberg81_multiplicity']==0 for x in r['full_E8_branching_tests'].values())
def test_parallel_finite_AdS_81_tangent_time_orientation_nogo():
 r=ads.run();assert r==frozen('finite_ads_causality_test')
 assert r['exact_reconstructed_graph']=='SRG(81,20,1,6)'
 assert r['adjacency_spectrum']=={'20':1,'2':60,'-7':20}
 assert r['graph_diameter']==2
 assert r['heat_spectral_dimension_samples'][-1]['spectral_dimension']<1e-3
def test_C8_synthetic_direct_spectroscopy_vs_cube():
 r=spec.run();assert r==frozen('c8_experiment_decision')
 assert r['C8']['eigenvalue_band_multiplicities']==[1,2,2,2,1]
 assert r['eight_site_cube_Q3_competitor']['eigenvalue_band_multiplicities']==[1,3,3,1]
 assert r['direct_scan']['max_abs_peak_error_MHz']<.01
 assert r['shot_ratio_direct_to_Ramsey']<.31
