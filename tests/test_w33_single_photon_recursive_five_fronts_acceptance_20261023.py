"""Five-track self-recursion acceptance packet with explicit hardware boundaries."""
import math,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_single_photon_recursive_five_fronts_acceptance_20261023 import report
def test_each_of_five_prior_fronts_has_executable_model_and_blocker():
    r=report()
    assert len(r['track_results'])==5
    for name,v in r['track_results'].items():
        assert len(v['executed'])>45 and len(v['barrier'])>45
def test_first_chip_9_mode_experiment_vs_1600_w33_digit_modes():
    a=report()['track_results']['1_foundry_pic']
    assert a['minimum_path_time_qutrit_product_mode_count']==9
    assert a['W33_pairwise_address_mode_count']==1600
    assert a['W33_phase_flipped_ordered_address_pairs']==480
    assert a['W33_undirected_graph_edges']==240
    assert not a['real_DRC_LVS']
def test_eraser_phase_coherent_and_incoherent_counts_differ_at_all_depths():
    a=report()['track_results']['2_noise_lab']['predictions_250k_photon_trials']
    assert len(a)==5
    for v in a:
        assert v['event_difference']>0
        assert v['mode_address_dimension_required']==3**v['fresh_registers']
        assert v['time_fourier_all_plus_probability']==pytest.approx(3**(-v['fresh_registers']))
        assert v['predicted_detections_joint_coherent_no_dark']>v['predicted_detections_joint_incoherent_no_dark']
    assert a[-1]['event_difference']<a[0]['event_difference']
def test_physical_incidence_not_graph_vertex_is_identity():
    a=report()['track_results']['3_interbus_transfer']
    assert a['incidence_rails']==160 and a['line_pairs']==780
    assert a['four_distinct_rail_moves_required_per_pair']==4
    assert a['recursive_entanglement_entropy_bits']==pytest.approx(4.803856189774729)
def test_rtl_storage_obligation_is_not_actual_quantum_memory():
    a=report()['track_results']['4_fpga']
    assert a['cycles']==2000 and a['accepted_commands']==676
    assert a['UP5K_LC']==42 and a['estimated_fmax_MHz']==68.82
    assert not a['quantum_memory_implemented'] and not a['pin_constraints_real']
def test_two_photon_vs_intraparticle_entanglement_types_not_confused():
    a=report()['track_results']['5_two_photons']
    assert a['two_photon_both_code_postselect_probability']==pytest.approx(.5)
    assert a['two_photon_conditional_negativity']==pytest.approx(.25)
    assert a['conditional_state_generator_not_gate']
