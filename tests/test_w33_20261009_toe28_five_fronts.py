"""Round28 five independently runnable tests."""
from pathlib import Path
import sys,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe28_qutrit_noisy_extraction as circuit
import w33_20261009_toe28_hypergraph_product_rate_distance as product
import w33_20261009_toe28_exceptional_e8_branch_screen as e8
import w33_20261009_toe28_wave_geometry_comparison as wave
import w33_20261009_toe28_c8_ramsey_control_spec as c8
def test_qutrit_sum_extraction_faults_cause_logical_failures():
 result=circuit.run(160)
 assert result['code']=='[[160,1,8]]_3'
 assert result['physical_SUM_gates_per_full_round']==956
 assert result['maximum_single_ancilla_Z_hook_on_Wilson_data_Z']==7
 assert result['maximum_single_ancilla_X_hook_on_Gauss_data_X']==3
 stats=result['simulation']
 assert stats['g0_p0']['failures']==0
 assert stats['g0.001_p0.001']['failures']>stats['g0.0001_p0.0001']['failures']
def test_hypergraph_product_commutation_positive_rate_but_fixed_distance():
 result=product.run()
 assert result['status']=='PASS'
 small=result['small_explicit_sparse_stabilizers']
 assert [x['exact_code_parameters'] for x in small]==['[[2866,256,8]]_3','[[31841,6561,8]]_3']
 assert all(x['logical_Z_weight_eight_witness'] for x in small)
 assert result['analytic_q_family'][-1]['rate']>.95
def test_e8_exceptional_factor_only_screen():
 result=e8.run()
 assert result['no_go_F4_only'] and result['no_go_G2_only']
 assert result['F4_only_largest_G_invariant_block']==52
 assert result['E7_factor_only_invariant_block_dimensions']==[133,56,56,1,1,1]
 assert '133' in result['necessary_host_for_St81_in_E7xA1']
def test_wave_graph_cone_is_not_lorentzian_limit():
 result=wave.run()
 assert result['W33_diameter']==4 and sum(result['graph_distance_shells'])==80
 assert len(result['leapfrog_graph_locality_verified_for_times'])==7
 errors=[abs(x['relative_error']) for x in result['external_three_dimensional_spatial_lattice']]
 assert all(errors[i+1]<errors[i] for i in range(len(errors)-1))
def test_C8_complex_ramsey_synthetic_five_bands():
 result=c8.run()
 assert result['n_physical_sites']==8 and result['two_boson_Fock_dimension']==36
 assert result['max_abs_recovery_error_MHz']<.015
 assert len(result['recovered_synthetic_five_band_freq_MHz'])==5
 assert result['first_gap_MHz']>.17
 assert len(result['control_sequence'])==9
