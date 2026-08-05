import json
import math
import runpy
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3743_3750_symmetry_os_spacetime_factory_tournament.py"
FROZEN = ROOT / "data" / "PART_3743_3750_SYMMETRY_OS_SPACETIME_FACTORY_TOURNAMENT_results.json"


@lru_cache(maxsize=1)
def build():
    return runpy.run_path(str(SOURCE))["build_certificate"]()


def test_frozen_and_semantic():
    got = build()
    old = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert got == old
    assert got["semantic_sha256"] == "67ce2d0ab105d8809dd6ae1af60381e1181d9a08c9032ce1dad1130f7bb8ff62"


def test_symmetry_os_and_twirl_cost():
    p = build()["passes"]
    assert p["3743_symmetry_operating_system"]["group_order"] == 25920
    assert p["3743_symmetry_operating_system"]["macro_diameter"] == 11
    assert p["3743_symmetry_operating_system"]["macro_total_generator_pulses_for_full_group_sweep"] == 211898
    twirl = p["3749_bonkers_exact_twirl_cost_firewall"]
    assert twirl["necessary_unweighted_exact_twirl_size_divisibility_lower_bound"] == 4320
    assert twirl["hashed_prefix_coverage"]["25920"]["nonadjacent"]["minimum_count_including_zeros"] == 24


def test_correlated_decoder_and_factory():
    p = build()["passes"]
    decoder = p["3744_correlated_spacetime_decoder"]
    assert decoder["MAP_error_ratio_interleaved_to_consecutive"] < 0.057
    factory = p["3745_hybrid_resource_factory"]
    assert factory["logical_nodes"] == 81
    assert factory["logical_links"] == 240
    assert factory["minimum_physical_controlled_phase_terms_per_logical_CZ"] == 3
    assert factory["physical_controlled_phase_terms_for_all_logical_links"] == 720


def test_grand_tournament_and_preregistration():
    p = build()["passes"]
    tournament = p["3746_geometry_advantage_grand_tournament"]
    assert tournament["degree12_generator_sets"] == 167356
    assert tournament["connected_graphs"] == 165984
    assert tournament["best_noncyclic_spectral_gap"] < 10
    assert tournament["best_noncyclic_minimum_two_hop_routes"] == 4
    assert tournament["best_noncyclic_minroute_metrics"]["nonedge_common_variance"] > 0
    prereg = p["3747_preregistered_hardware_challenge"]
    assert prereg["shots_per_tomography_setting"] == 81825
    assert len(prereg["falsification_conditions"]) == 4


def test_floquet_holonomy_is_s40():
    holonomy = build()["passes"]["3748_bonkers_floquet_incidence_holonomy"]
    assert holonomy["generated_permutation_group"] == "S40"
    assert holonomy["generated_group_order"] == math.factorial(40)
    assert holonomy["relative_round_generators"] == 3


def test_control_port_firewall():
    controls = build()["passes"]["3750_bonkers_minimum_symmetry_breaking_control_ports"]
    assert controls["fixed_passive_adjacency_algebra_dimension"] == 3
    assert controls["certified_control_port_interval"] == [24, 29]
    assert len(controls["force_chain"]) == 11
