import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"w33_pass3829_3836_adaptive_virtual_autonomous_thermo_substrate.py"
spec=importlib.util.spec_from_file_location("p3829",SRC)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def cert(): return mod.certificate()

def test_semantic_hash_and_front_count():
    c=cert()
    assert c["semantic_sha256"]=="d924764ba5d64326fbdc8d7a6bbd8bcdff2fd08fb2a4c6560f29c53a71c29fe4"
    assert len(c["passes"])==8

def test_adaptive_policy_beats_every_static_policy():
    p=cert()["passes"]["3829_noise_adaptive_geometry_hypervisor"]
    assert p["uniform_initial_noise_previous_direct_score"] < min(p["best_static_scores"].values())
    assert p["optimal_policy_by_state_and_previous_action"][0]==["local_ring"]*5
    assert p["optimal_policy_by_state_and_previous_action"][1]==["floquet"]*5
    assert p["optimal_policy_by_state_and_previous_action"][2]==["w33"]*5

def test_virtual_topology_is_a_minimum_twelve_round_factorization():
    p=cert()["passes"]["3830_measurement_only_virtual_w33_topology"]
    assert p["perfect_matching_rounds"]==p["minimum_rounds"]==12
    assert p["total_heralded_edge_tokens"]==240

def test_attractor_and_thermodynamic_transition():
    c=cert()["passes"]
    assert c["3831_autonomous_association_scheme_attractor"]["exact_deviation_contraction_factor"]=="1/2"
    t=c["3832_thermodynamic_geometry_tournament"]
    assert 0.795 < t["break_even_edge_success"] < 0.797

def test_checksum_localizes_every_single_edge_flip():
    p=cert()["passes"]["3834_bonkers_srg_digital_twin_checksum"]
    assert p["single_edge_deletion"]["count"]==240
    assert p["single_edge_insertion"]["count"]==540
    assert p["single_edge_deletion"]["rank"]==p["single_edge_insertion"]["rank"]==4

def test_heralding_and_symmetry_bath():
    c=cert()["passes"]
    h=c["3835_bonkers_heralded_topology_distillation"]["thresholds"]
    assert h["0.999"]["nonedge_four_two_hop_threshold"] < h["0.999"]["adjacent_direct_plus_two_detours_threshold"]
    b=c["3836_bonkers_transvection_symmetry_bath"]
    assert b["one_percent_total_variation_bound_steps"]==89
    assert 0.0632 < b["spectral_gap"] < 0.0634
