import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]

SCRIPTS=[
    "w33_20260924_eight_eisenstein_leaves_objectwise.py",
    "w33_20260924_common_winding_orientation_chain_map.py",
    "w33_20260924_hermitian_s6_tetracode_c3.py",
    "w33_20260924_tetracode_spectral_mu12_clock.py",
    "w33_20260924_temporal_tetracode_adqc_controller.py",
]

@pytest.mark.parametrize("name",SCRIPTS)
def test_all_five_producers_replay(name):
    subprocess.run(
        [sys.executable,str(ROOT/"analysis"/name)],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=70,
    )

def load(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))
def test_eight_leaves_are_literal_e8_objects():
    x=load("w33_20260924_eight_eisenstein_leaves_objectwise.json")
    assert x["status"]=="PASS_OBJECTWISE_COMMON_MODE_TO_EIGHT_EISENSTEIN_W33_LEAVES"
    assert x["leaf_model"]["leaf_count_through_fixed_4A2"]==8
    assert x["leaf_model"]["leaf_points_each"]==40
    assert x["leaf_model"]["all_J_fixed_point_free_on_rank8"] is True
    assert x["leaf_model"]["pairwise_leaf_intersection_histogram"]=={"4":12,"13":16}
    assert len({r["leaf_sha256"] for r in x["dictionary"]})==8
    m=x["F2_3_overlap_metric"]
    assert m["13_overlap_graph"].startswith("K4,4")
    assert m["4_overlap_graph"].startswith("K4 disjoint union K4")
    assert m["13_overlap_degree"]==4

def test_common_winding_is_exact_orientation_boundary():
    x=load("w33_20260924_common_winding_orientation_chain_map.json")
    assert x["status"]=="PASS_COMMON_NULL_WINDING_ORBIT_SUM_EQUALS_GLOBAL_HISTORY_ORIENTATION_CYCLE"
    assert x["chain_map"]["translated_loops"]==27
    assert x["chain_map"]["support_size"]==108
    assert x["chain_map"]["supports_partition_all_108_edges"] is True
    assert x["chain_map"]["equals_preexisting_invariant_orientation_cycle"] is True
    assert x["homology_resolution"]["filled_history_H1_class"]=="zero"
    assert x["homology_resolution"]["global_W33_H1_image_class"].startswith("zero")
def test_tetracode_c3_sits_in_hermitian_s6_after_transport():
    x=load("w33_20260924_hermitian_s6_tetracode_c3.json")
    assert x["status"]=="PASS_TETRACODE_C3_CONJUGATES_INTO_HERMITIAN_SPREAD_S6"
    assert x["groups"]["Hermitian_spread_stabilizer_order"]==720
    assert x["groups"]["C3_fixed_spreads_before_conjugation"]==3
    assert x["embedding"]["orthogonal_multiplier"]==1
    assert x["orbit_decomposition"]["null_QH0_10"]==[1,3,3,3]
    assert x["orbit_decomposition"]["norm1_QH1_15"]==[3,3,3,3,3]
    assert x["orbit_decomposition"]["norm2_QH2_15"]==[1,1,1,3,3,3,3]
    s=x["exceptional_S6_class_fingerprint"]
    assert s["QH2_matches_single_3cycle_class"] is True
    assert s["QH1_matches_double_3cycle_class"] is True

def test_tetracode_clock_duality_and_minimal_mu12_extension():
    x=load("w33_20260924_tetracode_spectral_mu12_clock.json")
    assert x["status"]=="PASS_TETRACODE_CLOCK_DUALITY_FIXED3_WITH_MINIMAL_C3_MU12_EXTENSION"
    assert x["primal_tetracode_plane"]["states"]==9
    assert x["primal_tetracode_plane"]["basis_support_subspace_dynamically_invariant"] is False
    assert x["canonical_fourier_quotient"]["dimension"]==3
    assert x["canonical_fourier_quotient"]["spectral_clock_action"]=="identity at t*=2*pi/9"
    assert x["C3"]["fixes_P_perp_pointwise"] is True
    assert x["C3"]["primal_plane_not_preserved_by_dual_action"] is True
    assert x["minimal_mu12_extension"]["dimension"]==6
    assert x["minimal_mu12_extension"]["phase_dimensions"]=={"1":3,"omega":3,"omega^2":0}
    assert x["minimal_mu12_extension"]["generated_mu12_indices"]==list(range(12))
def test_adqc_controller_abi_and_rtl_surface():
    x=load("w33_20260924_temporal_tetracode_adqc_controller.json")
    assert x["status"]=="PASS_TETRACODE_RELATIVE_MODE_COMPILED_TO_PHOTONIC_ADQC_CONTROLLER"
    assert x["four_channel_abi"]["histories"]==27
    assert x["four_channel_abi"]["representatives_per_history"]==3
    assert x["tetracode_program_plane"]["program_histories"]==9
    assert x["tetracode_program_plane"]["all_standard_tetracode_words_recovered"] is True
    assert x["tetracode_program_plane"]["C3_preserves_plane_and_gauge"] is True
    assert x["analyzer_programs"]["program_id_width"]==2
    assert x["parallel_pass10941_vm_bridge"]["all_25_vm_generators_lowered_exactly_mod3"] is True
    assert x["parallel_pass10941_vm_bridge"]["maximum_clifford_macro_length"]==7
    assert x["parallel_pass10941_vm_bridge"]["same_T_analyzer_Z_orbit"] is True
    assert len(x["rtl"]["truth_table_sha256"])==64
    assert len(x["rtl"]["rtl_source_sha256"])==64
    assert len(x["rtl"]["testbench_source_sha256"])==64
    assert (ROOT/x["rtl"]["testbench"]).exists()

    rtl=(ROOT/"rtl/w33_temporal_tetracode_adqc_controller.v").read_text()
    assert "module w33_temporal_tetracode_adqc_controller" in rtl
    assert "tetracode_plane" in rtl
    assert "common_mode_correction" in rtl
    assert "program_id = 2'd3" in rtl
