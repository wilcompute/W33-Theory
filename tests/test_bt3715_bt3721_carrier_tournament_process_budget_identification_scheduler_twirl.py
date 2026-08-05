import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'analysis' / 'bt3715_3721_carrier_tournament_process_budget_identification_scheduler_twirl.py'
FROZEN = ROOT / 'data' / 'PART_BT3715_BT3721_CARRIER_TOURNAMENT_PROCESS_BUDGET_IDENTIFICATION_SCHEDULER_TWIRL_results.json'
spec = importlib.util.spec_from_file_location('bt3715_3721', SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
DATA = mod.build()
OLD = json.loads(FROZEN.read_text())


def test_frozen_semantic_certificate():
    assert DATA == OLD
    assert DATA['semantic_sha256'] == '2f934b56ba757c94c7b1c46396691dbc417a37aa0b5a07cf762067449705d9b1'


def test_minimum_erasure_carrier():
    p = DATA['passes']['3715_minimum_erasure_correcting_carrier']
    assert p['code'] == '[[3,1,2]]_3'
    assert p['knill_laflamme_erasure_checks'] == 27
    assert p['erasure_encoded_physical_qutrits'] == 243
    assert p['triple_rail_modes'] == 729
    assert p['encoded_per_physical_qutrit_loss_threshold'] > 0.04


def test_geometry_tournament():
    p = DATA['passes']['3716_degree_matched_geometry_tournament']
    assert p['circulants']['searched_jump_sets'] == 27132
    assert p['w33']['diameter'] == 2
    assert p['w33']['nonedge_common_neighbor_variance'] == '0'
    assert p['w33']['nonedge_common_neighbor_min'] == 4
    assert p['circulants']['route_optimum_metrics']['nonedge_common_neighbor_min'] == 2
    assert p['w33']['adjacency_spectral_gap'] > p['circulants']['gap_optimum_spectral_gap']


def test_process_budget_and_identification():
    comb = DATA['passes']['3717_causal_process_tensor_memory']
    budget = DATA['passes']['3718_thermodynamic_spacetime_budget']
    ident = DATA['passes']['3719_decisive_system_identification_experiment']
    assert comb['future_retains_past_after_identical_middle_replacement']
    assert not comb['future_to_past_signalling']
    assert comb['process_tensor_memory_bond_dimension'] == 3
    assert budget['feedforward_delay_length_m_by_latency_ns']['10'] > 0.7
    assert ident['transfer_matrix_input_settings'] == 1600
    assert ident['w33_triangle_markers'] == 160


def test_optimal_four_tick_schedule():
    p = DATA['passes']['3720_bonkers_optimal_four_tick_syndrome_plane']
    assert p['round_count'] == p['optimal_depth_lower_bound'] == 4
    assert p['incidence_edges'] == 160
    assert all(len(set(r)) == 40 for r in p['rounds'])
    seen = {(point, line) for r in p['rounds'] for point, line in enumerate(r)}
    assert len(seen) == 160


def test_rank_three_symmetry_twirl():
    p = DATA['passes']['3721_bonkers_rank_three_symmetry_twirl']
    assert p['automorphism_group_order'] == 25920
    assert p['ordered_pair_orbit_sizes'] == [40, 480, 1080]
    assert p['twirled_Hermitian_parameter_count'] == 3
    assert p['cycle40_dihedral_parameter_count'] == 21
    assert p['path40_reversal_parameter_count'] == 800
