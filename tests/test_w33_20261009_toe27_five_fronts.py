"""Round27 independent five-front scientific regression tests."""
from pathlib import Path
import sys,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe27_qutrit_ideal_decoder as dec
import w33_20261009_toe27_gq_family_code_theorem as gq
import w33_20261009_toe27_e8_reducible_sl9_no_steinberg as e8
import w33_20261009_toe27_heat_spectral_dim_and_sector_no_go as heat
import w33_20261009_toe27_c8_spectroscopy_noise_calibration as c8
def frozen(name):
 return json.loads((ROOT/'data'/f'w33_20261009_toe27_{name}.json').read_text())

def test_160_link_ternary_CSS_decoder_recovers_all_sampled_weight_leq_three():
 r=dec.run(trials=500)
 assert r==frozen('qutrit_ideal_decoder')
 assert r['code']=='[[160,1,8]]_3'
 assert r['check_matrix_dimensions']=={'X_error_Wilson_H':[80,160],'Z_error_Gauss_H':[79,160]}
 assert r['syndrome_columns_nonzero_and_unique_X']
 assert r['syndrome_columns_nonzero_and_unique_Z']
 assert all(x['recovered_all'] for x in r['exact_radius_tests'])
 assert all(x['trials']==500 for x in r['iid_depolarizing_8_Paulis_samples'].values())

def test_infinite_q_exact_local16_generator_CSS_family():
 r=gq.run();assert r==frozen('gq_q_family_code_theorem')
 assert 'q^4' in r['proof']
 cases={x['q']:x for x in r['checks']}
 assert cases[2]['total_eight_cycle_apartments']==90
 assert cases[3]['total_eight_cycle_apartments']==1620
 assert cases[3]['cycle_space_rank']==81
 assert cases[16]['certified_one_logical_qutrit_code']=='[[74273,1,8]]_3'
 assert all(x['Gauss_generator_count']+x['Wilson_generator_count']==x['incidence_link_qutrits']-1 for x in cases.values())

def test_E8_reducible_nineD_complete_partition_block_bound():
 r=e8.run();assert r==frozen('e8_reducible_sl9_no_steinberg')
 assert r['total_reducible_nine_partitions']==29
 assert r['maximum_invariant_block_dim_over_ALL_reducible_carriers']==63
 assert r['Steinberg81_multiplicity_for_any_reducible_9D_carrier']==0
 assert all(x['max_G_invariant_block_dimension']<=63 for x in r['cases'])

def test_normalized_Levi_no_four_dim_diffusion_plateau():
 r=heat.run();assert r==frozen('heat_spectral_dim_and_sector_no_go')
 assert r['graph_diameter']==4
 assert r['spectral_dimension_limit']=='d_s(t)=-2d(log H)/d(log t) -> 2t'
 last=r['data']['1009']
 assert abs(last[2]['discrete_spectral_dimension']-4)<.05
 assert last[3]['discrete_spectral_dimension']>7.5
 assert last[1]['discrete_spectral_dimension']<2.1

def test_exact_c8_boson_noise_and_complex_vs_probability_spectroscopy():
 r=c8.run();assert r==frozen('c8_spectroscopy_noise_calibration')
 assert r['H_two_boson_dim']==36
 assert r['U_over_t']==32
 assert abs(r['ideal_C8_five_band_spectrum']['first_gap']-0.03634944022361708)<1e-8
 assert 50<r['min_ten_gap_cycles_coherent_acquisition_us']<60
 assert r['synthetic_bounded_independent_onsite_link_noise_in_t_units']['0.005']['max_abs_first_gap_relative_shift']>.02
 assert 'PAIRWISE' in r['important_readout_correction']
