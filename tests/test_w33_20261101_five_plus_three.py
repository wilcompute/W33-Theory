"""Independent regression for five W33 frontiers and three falsifiers."""
import sys,math,json,itertools
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261101_five_plus_three as M
import w33_20261031_eight_front_server_campaign as old

@pytest.fixture(scope='module')
def results():
    return M.build()['results']

def test_01_exact_girth_eight_and_81_independent_cycle_mesh(results):
    d=results['01_optical_81_shortest_cycles_sparse_compiler']
    assert d['logical_modes']==81 and d['girth']==8
    assert d['number_independent_girth_cycles']==81
    assert d['fundamental_cycle_supports']==648
    assert d['gate_count']==5346<d['prior_gate_count']==8416
    assert 0.36<d['improvement_fraction']<0.37
    assert d['reconstruction_error']<1e-10
    assert len(d['gate_list_SHA256'])==64

def test_02_optical_subspace_unchanged_even_when_basis_changes():
    D,C=old.projector_exact()
    from scipy.linalg import null_space
    Q=null_space(D.astype(float))
    assert np.linalg.norm(C/320-Q@Q.T)<1e-10
    assert np.all(C.diagonal()==162)

def test_03_magic_four_stabilizer_measurement_fidelity(results):
    d=results['02_QND_strange_fidelity_stabilizer_tomography']
    assert d['number_stabilizer_basis_settings']==4
    assert d['total_shots']==24000
    assert abs(d['true_Strange_fidelity']-.93)<1e-12
    assert d['raw_uncalibrated_fidelity']<d['readout_corrected_fidelity']
    assert abs(d['readout_corrected_fidelity']-.93)<d['conservative_99pct_Hoeffding_halfwidth']
    assert 0<d['conservative_99pct_Hoeffding_halfwidth']<.03

def test_04_120_local_states_and_actual_third_site_sparse_lanczos(results):
    d=results['03_full_120_tick_three_site_quantum_chain']
    a,b=d['rows'];assert (a['Hilbert_dimension'],b['Hilbert_dimension'])==(14400,1728000)
    assert a['local_dimension']==b['local_dimension']==120
    assert abs(a['ground_energy']+1.414609029)<2e-5
    assert abs(b['ground_energy']+2.350555852)<2e-5
    assert 0.28<b['excitation_gap']<0.29
    assert b['excitation_gap']<a['excitation_gap']

def test_05_exact_burst_erasure_advantage_threshold(results):
    d=results['04_Floquet_correlated_burst_erasure']
    assert len(d['rows'])==18
    for row in d['rows']:
        q=row['per_active_rail_erasure']; b=row['adjacent_pair_burst']
        theory=(1-b)*(1-3*q*q+2*q**3)
        bare=(1-2*b/3)*(1-q)
        assert abs(row['erasure_code_success']-theory)<1e-12
        assert abs(row['bare_uniform_rail_success']-bare)<1e-12
    a=d['advantage_loss_thresholds']
    assert abs(a[0]['critical_burst_probability']-.068100186477)<1e-10
    assert abs(a[1]['critical_burst_probability']-.216907861232)<1e-10
    assert abs(a[2]['critical_burst_probability']-.271450129487)<1e-10
    assert d['rows'][5]['encoded_gain']<0

def test_06_actual_nonabelian_Lorentz_curvature_Ward(results):
    d=results['05_Lorentz_nonAbelian_curvature_gauge_and_stability']
    assert d['spatial_lattice']==[2,2,2]
    assert d['gauge_plaquette_covariance_max_error']<1e-11
    assert d['gauge_trace_max_error']<1e-11
    assert d['gauge_matter_action_error']<1e-11
    assert d['lie_bracket_closure_error']<1e-12

def test_07_Wilson_lorentz_boost_unbounded_negative(results):
    d=results['05_Lorentz_nonAbelian_curvature_gauge_and_stability']
    values=d['Wilson_energy_boost_sequence']
    for row in values:
        theta=row['rapidity'];weight=row['noncompact_Wilson_weight']
        assert abs(weight-(4-4*math.cosh(theta)))<1e-8*max(1,abs(weight))
    assert values[-1]['noncompact_Wilson_weight'] < values[-2]['noncompact_Wilson_weight'] < -100

def test_08_single_photon_rail_loss_code_no_go(results):
    d=results['06_outside_single_photon_rail_loss_KL_nogo']
    assert abs(d['loss_probability_max']-81/160)<1e-12
    assert d['loss_probability_min']<1e-20
    assert d['restricted_loss_observable_rank']==1

def test_09_120_tick_residual_entropy_and_exact_colorings(results):
    d=results['07_outside_full120_zero_temperature_entropy']
    assert d['noncommuting_graph_spectrum']=={'81':1,'-9':24,'9':15,'0':80}
    assert d['rings'][0]['exact_ground_configurations']==9720
    assert d['rings'][1]['exact_ground_configurations']==524880
    for row in d['rings']:
        n=row['ring_sites']; assert row['exact_ground_configurations']==81**n+24*(-9)**n+15*9**n
    assert abs(math.log(81)-4.39444915467)<1e-10

def test_10_eight_producers_all_distinct_and_passing(results):
    assert len(results)==8
    assert len({x['status']for x in results.values()})==8
    assert all(d['status'].startswith('PASS')for d in results.values())

def test_11_full_frozen_json_source_alignment(results):
    frozen=json.loads(M.OUT.read_text())['results']
    assert set(frozen)==set(results)
    for k,v in results.items():assert frozen[k]['status']==v['status']

def test_12_inference_boundaries_visible(results):
    assert 'no_QND' not in results['02_QND_strange_fidelity_stabilizer_tomography']['status']
    assert 'not an MPS thermodynamic limit' in results['03_full_120_tick_three_site_quantum_chain']['scope']
    assert 'No invertible tetrad' in results['05_Lorentz_nonAbelian_curvature_gauge_and_stability']['scope']

def test_13_line_correlated_phase_noise_exact_universal_formula(results):
    d=results['08_outside_line_correlated_phase_noise']
    assert d['number_line_blocks']==40
    assert d['block_code_eigenvalue']=='27/40'
    for row in d['rows']:
        s=row['sigma']
        expected=math.exp(-s*s)+(1-math.exp(-s*s))*27/40
        iid=math.exp(-s*s)+(1-math.exp(-s*s))*81/160
        assert abs(row['exact_line_correlated_survival']-expected)<1e-12
        assert abs(row['independent_rail_survival']-iid)<1e-12
        assert abs(row['MonteCarlo_survival']-expected)<.025
        assert row['exact_line_correlated_survival']>=row['independent_rail_survival']-1e-12
