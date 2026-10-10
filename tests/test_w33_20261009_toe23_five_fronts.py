"""Regression coverage for the five TOE Round23 executions and prior papers."""
from pathlib import Path
import json,sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe23_e8_sector_leakage as E
import w33_20261009_toe23_three_boson_vacuum as Q
import w33_20261009_toe23_dynamic_apartment_frame as F
import w33_20261009_toe23_partial_flatness as G
import w33_20261009_toe23_universal_pair_ratios as S
def saved(name):
 return json.loads((ROOT/'data'/f'w33_20261009_toe23_{name}.json').read_text())
def test_E8_81_naive_truncation_3_channel_leakage_and_full_sl9():
 x=E.run()
 assert x==saved('e8_sector_leakage')
 assert x['source_grade_dimensions']==[80,84,84]
 assert x['naive_target_dimensions']==[86,81,81]
 assert x['grade_plus_plus_output_rank']==84
 assert len(x['excluded_dual_grade_witnesses'])==3
 assert x['mixed_to_sl9_offdiagonal_channels']==72
 assert x['mixed_to_sl9_diagonal_full_rank']==9
def test_exact_88560_state_three_boson_quantum_vacuum():
 x=Q.run()
 assert x['Fock_dimension']==88560 and x['particle_number']==3
 assert x['hopping_sparse_nnz']==1036800
 assert abs(x['computed']['0']['E0']+12)<1e-5
 assert x['computed']['8']['triple_onsite_probability']>.94
 assert all(p['max_density_deviation']<1e-6 for p in x['computed'].values())
 assert all(p['gap']>0 for p in x['computed'].values())
def test_apartment_frame_45_components_are_not_tunneling_protected():
 x=F.run()
 assert x['frame_count']==1620
 assert x['overlap_3_connected_components']==45 and x['component_size']==36
 assert x['overlap_3_degree']==8 and x['overlap_2_degree']==90
 assert x['overlap_2_connected_components']==1
 assert x['component_spectrum']=={'-4.0':4,'-2.0':12,'0.0':9,'2.0':4,'4.0':6,'8.0':1}
 assert x['component_triangles']==96
 assert abs(x['component_36_spectral_gap']-4)<1e-8
 assert x['tunneling_gaps']['0.01']['gap']>0
 assert x['torus_heat']['81'][2]['running_spectral_dimension']>3.9
 assert x['torus_heat']['3'][2]['running_spectral_dimension']<.01
def test_all_160_incidence_edges_have_81_cycle_basis():
 x=G.run()
 assert x['all_160_edge_checks']=={'eightcycles_through_each_edge':81,
  'rank_through_each_edge':81,'rank_avoiding_each_edge':80,
  'independently_checked_edges':160}
 result={p['selector']:p for p in x['selector_profiles']}
 assert result['cycles avoiding point 0']['encoded_logical_qutrits']==3
 assert result['cycles avoiding incidence edge']['encoded_logical_qutrits']==1
 assert x['full_flatness']['encoded_logical_qutrits']==0
 assert result['cycles touching point 0 AND nonincident line']['encoded_logical_qutrits']==72
def test_asymptotic_universal_w33_pair_excitation_ratios():
 x=S.run()
 assert x['exact_second_order_Schrieffer_Wolff_numerator']=='K=P H_hop (1-P) H_hop P = 8 I_80 + 2 A_Levi as an integer matrix'
 assert x['nonzero_adj_eigenvalue_multiplicities']=={'-4':1,'-sqrt6':24,'0':30,'sqrt6':24,'4':1}
 assert math.isclose(x['universal_band_gap_ratio_from_ground']['band_0'],4/(4-math.sqrt(6)),rel_tol=1e-12)
 assert abs(x['finite_U_numeric']['128']['relative_error'])<.001
