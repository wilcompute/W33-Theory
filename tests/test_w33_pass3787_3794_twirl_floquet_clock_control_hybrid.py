import json
import runpy
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3787_3794_twirl_floquet_clock_control_hybrid.py"
FROZEN = ROOT / "data" / "PART_3787_3794_TWIRL_FLOQUET_CLOCK_CONTROL_HYBRID_results.json"

@lru_cache(maxsize=1)
def cert():
    return runpy.run_path(str(SOURCE))["build_certificate"]()

def test_frozen_semantic_certificate():
    assert cert() == json.loads(FROZEN.read_text())

def test_minimum_observable_twirl():
    p = cert()["passes"]["3787_minimum_exact_observable_twirl_design"]
    assert p["ordered_pair_orbit_sizes"] == [40,480,1080]
    assert p["minimum_unweighted_orbit_estimation_settings"] == 1600
    assert p["shortest_word_total_generator_macros"] == 8934

def test_floquet_and_clock():
    p = cert()["passes"]
    assert p["3788_floquet_diagonal_error_machine"]["relative_group"] == "S40"
    assert p["3788_floquet_diagonal_error_machine"]["traceless_static_diagonal_disorder_cancelled"]
    assert p["3789_optimal_distributed_clock_broadcast"]["optimal_broadcast_ticks"] == 7
    assert p["3789_optimal_distributed_clock_broadcast"]["informed_count_by_tick"] == [1,2,4,8,16,30,54,80]

def test_exact_zero_forcing_number():
    p = cert()["passes"]["3790_exact_zero_forcing_control_ports"]
    assert p["zero_forcing_number"] == 29
    assert p["maximum_reverse_forcing_length"] == 11
    assert p["depth_12_orbits"] == 0
    assert p["reverse_sequence_orbit_counts_by_length"][-1] == 34890

def test_dynamic_hybrid():
    p = cert()["passes"]["3791_dynamic_w33_locality_hybrid"]
    assert p["shared_couplers"] == 128
    assert p["union_coupler_inventory"] == 352
    assert p["cross_phase_two_step_path_minimum"] == 2
    assert p["all_two_phase_two_step_walk_minimum"] == 4

def test_three_bonkers_mechanisms():
    p = cert()["passes"]
    assert p["3792_bonkers_zero_forcing_actuator_virtualization"]["virtualized_unactuated_modes"] == 11
    assert p["3793_bonkers_floquet_fourier_spectrometer"]["independent_traceless_diagonal_modes"] == 39
    assert p["3794_bonkers_reversible_fourteen_tick_all_reduce"]["all_reduce_ticks"] == 14
