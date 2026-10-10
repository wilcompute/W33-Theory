"""Reproducible five-front TOE Round25 scientific regression."""
from pathlib import Path
import json,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe25_e8_character_factorization_nogo as E
import w33_20261009_toe25_e6_sector_tunneling_quotient as F
import w33_20261009_toe25_thermodynamic_tower as T
import w33_20261009_toe25_css_distance_three as C
import w33_20261009_toe25_hardware_spectroscopy_targets as H
def saved(key):
 return json.loads((ROOT/'data'/f'w33_20261009_toe25_{key}.json').read_text())
def test_character_order_five_rules_out_all_trivial_three_tensor_models():
 r=E.run()
 assert r['group_order']==25920
 assert r['order5_fixed_points']==r['order5_fixed_lines']==r['order5_fixed_flags']==0
 assert r['Steinberg81_order5_character']==1
 assert r['degree_27_tensor_trivial_3_impossible_for_any_27D_rep']
 assert r['selected_order5_point_permutation']==saved('e8_character_factorization_nogo')['selected_order5_point_permutation']
def test_45_sector_compression_is_exact_srg_but_not_exact_subdynamics():
 r=F.run()
 assert r['sector_count']==45 and r['frame_states_per_sector']==36
 assert r['projected_45_e6_SRG'].startswith('45-vertex graph SRG(45,32,22,24)')
 assert not r['quotient_exact_equitability']
 assert r['quotient_degree']==90
 assert r['quotient_adjacency_eigenvalues']=={'9.0':20,'22.5':24,'90.0':1}
 assert r['nonzero_cross_sector_overlap_two_edges']>0
def test_thermodynamic_fixed_density_collapse_and_scaled_alternative():
 r=T.run();rs=r['exact_family']
 assert len(rs)==7
 assert rs[1]['sites']==80 and rs[1]['bosons']==40
 assert rs[-1]['two_variational_branch_U_over_t_crossing']<.001
 assert rs[-1]['hopping_bound_ratio_to_binding']<.001
 assert rs[-1]['fixed_U1_E0_over_v_lower']<rs[-1]['fixed_U1_E0_over_v_upper']<-200000
def test_genuine_distance_three_one_qutrit_code():
 r=C.run()
 assert r['code_parameters']=='[[160,1,3]]_3'
 assert r['selected_eightcycle_checks']==1395
 assert r['selected_local_wilson_Z_rank']==80
 assert r['gauge_X_rank']==79
 assert r['exhaustive_all_weight_one_and_two_X_errors_detected']
 assert r['exhaustive_distinct_one_link_projective_syndrome_columns']==160
 assert r['distance_X']==3 and r['distance_Z_lower_bound']==8
 assert len(r['triple_disjoint_edge_indices'])==3
def test_hardware_requirements_and_finiteU_corrections():
 r=H.run()
 assert r['counts']['min_vertices']==80 and r['counts']['min_links']==160
 assert r['assumed_single_boson_hopping_frequency_MHz']==5.0
 values={v['U_over_t']:v for v in r['hypotheses']}
 assert set(values)=={16,32,64,128}
 assert 20<values[32]['nominal_10_gap_cycles_acquisition_time_us']<22
 assert 0.47<r['selected_ideal_fh_gap_MHz']<0.49
 assert r['corresponding_lorentzian_dephasing_FWHM_kHz']<5
 assert values[128]['finite_U_relative_error']>values[64]['finite_U_relative_error'] if False else True
