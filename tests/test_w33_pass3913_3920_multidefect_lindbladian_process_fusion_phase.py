import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'analysis'/'w33_pass3913_3920_multidefect_lindbladian_process_fusion_phase.py'

@pytest.fixture(scope='session')
def result():
    spec=importlib.util.spec_from_file_location('pass3913_3920',SRC)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.build_result()

def test_semantic_certificate(result):
    assert result['semantic_sha256']=='019183d46768ff68a5f57676540d8aefd853010614545fd834656b69c4c7eb15'

def test_multidefect_decoder(result):
    p=result['passes']['3913_multidefect_topology_immune_system']
    assert p['all_two_flip_syndromes']==303810 and p['all_two_flip_syndromes_distinct']
    assert p['all_three_edge_deletion_syndromes']==2275280 and p['all_three_edge_deletion_syndromes_distinct']

def test_lindbladian_fixed_algebra(result):
    p=result['passes']['3914_symmetry_lindbladian']
    assert p['fixed_algebra_dimension']==3
    assert abs(p['continuous_time_gap_at_unit_rate']-0.06329071414775411)<1e-11

def test_process_and_fusion(result):
    c=result['passes']['3915_partially_observed_process_controller']
    f=result['passes']['3916_correlated_fusion_compiler']
    assert c['partially_observed_optimal_cost']<c['best_static_cost']
    assert 0.9158<f['threshold_for_99_percent_complete_epoch']<0.9160

def test_phase_dna_and_dual_scheduler(result):
    p=result['passes']['3917_architecture_phase_diagram']
    d=result['passes']['3918_bonkers_topology_dna']
    s=result['passes']['3919_bonkers_dual_geometry_all_to_all_scheduler']
    assert sum(p['winner_counts'].values())==500
    assert d['group_order']==25920 and d['edge_orbit_size']==480
    assert s['complete_graph_rounds']==39 and s['all_to_all_edges']==780

def test_compressed_sensor(result):
    p=result['passes']['3920_bonkers_compressed_multidefect_sensor']
    assert p['measured_residual_entries']==192
    assert p['all_two_flip_syndromes_distinguished']==303810
