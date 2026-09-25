import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
    "w33_20260924_common_winding_relative_h2.py",
    "w33_20260924_fano_seven_qutrit_vm_fabric.py",
    "w33_20260924_leaf_fibre_fano_vm_bridge.py",
    "w33_20260924_e8_metric_fano_latch_orbits.py",
    "w33_20260924_m36_temporal_triangle_dictionary.py",
    "w33_20260924_temporal_e6_dual_residue_firewall.py",
    "w33_20260924_temporal_e6_aut_group_firewall.py",
    "w33_20260924_m36_null_line_atlas.py",
    "w33_20260924_bt1348_bt1349_errata.py",
]

@pytest.mark.parametrize("name",SCRIPTS)
def test_new_producers_replay(name):
    subprocess.run(
        [sys.executable,str(ROOT/"analysis"/name)],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=80,
    )

def load(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))

def test_common_winding_relative_h2_exact_sequence():
    x=load("w33_20260924_common_winding_relative_h2.json")
    assert x["status"]=="PASS_COMMON_WINDING_IS_DISTINGUISHED_RELATIVE_H2_BOUNDARY_CLASS"
    assert x["complex"]["H1_one_skeleton_dimension"]==82
    assert x["complex"]["H1_filled_dimension"]==46
    assert x["complex"]["H2_filled_dimension"]==0
    assert x["relative_pair"]["H2_KG_dimension"]==36
    assert x["relative_pair"]["connecting_map_rank"]==36
    assert x["relative_pair"]["connecting_map_kernel_dimension"]==0
    assert x["relative_pair"]["exact_sequence_dimensions"]=="0 -> 36 -> 82 -> 46 -> 0"
    assert x["distinguished_class"]["boundary_support_edges"]==108
    assert x["distinguished_class"]["boundary_equals_unique_invariant_orientation_cycle"] is True

def test_fano_seven_qutrit_vm_fabric():
    x=load("w33_20260924_fano_seven_qutrit_vm_fabric.json")
    assert x["status"]=="PASS_SEVEN_QUTRIT_VM_IS_FANO_INDEXED_K7_CSASZAR_FABRIC"
    assert x["symmetry"]["GL3_2_order"]==168
    assert x["symmetry"]["embedded_in_Sp14_3_as_mode_permutations"] is True
    assert x["coupler_fabric"]["undirected_CZ_pairs"]==21
    assert x["coupler_fabric"]["directed_pair_latches"]==42
    assert x["coupler_fabric"]["Euler_characteristic"]==0
    assert x["Pass10941_VM"]["existing_pair_coupler_count"]==6
    assert x["Pass10941_VM"]["full_K7_pair_coupler_count"]==21
def test_leaf_fibre_and_vm_share_f2_3_codec():
    x=load("w33_20260924_leaf_fibre_fano_vm_bridge.json")
    assert x["status"]=="PASS_EIGHT_LEAF_TORSOR_AND_SEVEN_QUTRIT_FANO_MODES_SHARE_ONE_F2_3_CODEC"
    assert x["objectwise_dictionary"]["leaf_states"]==8
    assert x["objectwise_dictionary"]["VM_modes"]==7
    assert x["objectwise_dictionary"]["verified_for_all_base_leaves"] is True
    assert x["E8_metric_on_VM_modes"]["13_overlap_modes"]==[0,1,2,5]
    assert x["E8_metric_on_VM_modes"]["4_overlap_modes"]==[3,4,6]
    assert x["E8_metric_on_VM_modes"]["line_sum_zero"] is True
    s=x["symmetry_reduction"]
    assert s["full_Fano_linear_order"]==168
    assert s["distinguished_line_stabilizer_order"]==24
    assert s["affine_metric_group_order"]==192
    assert s["matches_Pass7409_WD4"] is True

def test_bt1349_fano_point_graph_erratum_is_frozen():
    src=(ROOT/"proofs/bt1349_multi_photon_toroidal_scaling.py").read_text(encoding="utf-8")
    assert "degrees == 6" in src
    assert "len(seen_edges) == 21" in src
    assert "eigenvalues[0] - 6.0" in src
    assert "diameter == 1" in src
    assert "degrees == 3" not in src
    assert "eigenvalues[0] - 3.0" not in src


def test_bt1348_bt1349_errata_and_later_code_firewall():
    x=load("w33_20260924_bt1348_bt1349_errata.json")
    assert x["status"]=="PASS_BT1348_BT1349_LEGACY_WITNESSES_REPAIRED_WITH_FIREWALLS"
    a=x["BT1348"]
    assert a["full_quantum_code_claim"] is False
    assert a["routing_preserves_repetition_subspace"] is False
    assert a["routing_repetition_subspace_weight"]=="2/3"
    assert a["contextual_36_equals_12_plus_27"] is False
    assert a["no_factory_inference_from_shell_counts"] is False
    b=x["BT1349"]
    assert b["point_graph"]=="K7"
    assert b["degree"]==6 and b["diameter"]==1
    assert b["pair_channels"]==21
    assert x["later_code_boundary"]["knill_laflamme_checks"]==27

    summary=(ROOT/"papers/BT1348_BT1349_summary.md").read_text(encoding="utf-8")
    assert "3-regular toroidal topology" not in summary
    assert "no separate magic-state factory is needed" not in summary


def test_repaired_bt1348_witness_replays():
    env=dict(os.environ)
    env["PYTHONUTF8"]="1"
    proc=subprocess.run(
        [sys.executable,str(ROOT/"proofs/bt1348_gf3_qec_holonet_integration.py")],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=30,env=env,
    )
    assert "PASS FIREWALL: one-site Z is undetected" in proc.stdout
    assert "repetition-subspace weight after routing = 0.666667" in proc.stdout
    assert "Magic/QEC resource claims require independent certificates" in proc.stdout

def test_e8_selected_line_stratifies_hardware_bus():
    x=load("w33_20260924_e8_metric_fano_latch_orbits.json")
    assert x["status"]=="PASS_E8_SELECTED_FANO_LINE_STRATIFIES_HOLONET_21_42_168_192_BUS"
    assert x["K7_pair_orbits"]["orbit_sizes"]==[3,6,12]
    assert x["oriented_latch_orbits"]["orbit_sizes"]==[6,12,12,12]
    assert x["active_detector_refinement"]["active_total"]==168
    assert x["tomotope_bus_refinement"]["total"]==192
    assert x["tomotope_bus_refinement"]["guard_apertures"]==24


def test_m36_temporal_triangle_dictionary():
    x=load("w33_20260924_m36_temporal_triangle_dictionary.json")
    assert x["status"]=="PASS_M36_IS_OBJECTWISE_THE_36_ORIENTED_TEMPORAL_TRIANGLES"
    r=x["residual_geometry"]
    assert r["off_line_points"]==36
    assert r["history_lines_disjoint_from_Bell"]==27
    assert r["incidences"]==108
    assert x["checks"]["all_36_magic_rays_biject_to_off_Bell_points"] is True
    assert x["checks"]["all_36_points_biject_to_temporal_triangles"] is True
    assert len(x["M36_dictionary"]["rows"])==36

def test_temporal_and_e6_36_are_cospectral_but_not_isomorphic():
    x=load("w33_20260924_temporal_e6_dual_residue_firewall.json")
    assert x["status"]=="PASS_TEMPORAL_36_AND_E6_AFFINE_36_ARE_COSPECTRAL_NONISOMORPHIC_DUAL_RESIDUES"
    assert x["shared_shadow"]["spectrum"]=={"8":1,"2":12,"-1":8,"-4":6}
    assert x["temporal_line_side"]["diameter"]==2
    assert x["E6_point_side"]["diameter"]==3
    assert x["temporal_line_side"]["nonedge_common_neighbor_histogram"]=={"2":162,"4":81}
    assert x["E6_point_side"]["nonedge_common_neighbor_histogram"]=={"0":27,"3":216}
    assert x["firewall_completion"]["fiber_pairs_equal_all_zero_CN_nonedges"] is True
    assert x["firewall_completion"]["completed_graph"]=="SRG(27,10,1,5)"


def test_temporal_and_e6_1296_groups_are_nonisomorphic():
    x=load("w33_20260924_temporal_e6_aut_group_firewall.json")
    assert x["status"]=="PASS_SAME_1296_AUT_ORDER_SPLITS_ABELIAN_VS_HEISENBERG_AND_SPLIT_VS_NONSPLIT_48"
    assert x["temporal"]["full_automorphism_order"]==1296
    assert x["E6_H27"]["full_automorphism_order"]==1296
    assert x["temporal"]["translation_group_abelian"] is True
    assert x["E6_H27"]["translation_group_abelian"] is False
    assert x["separators"]["full_group_order8_elements"]=={"temporal":0,"E6_H27":324}
    assert x["separators"]["groups_isomorphic"] is False

def test_m36_is_null_line_atlas():
    x=load("w33_20260924_m36_null_line_atlas.json")
    assert x["status"]=="PASS_M36_IS_THE_36_AFFINE_NULL_LINES_OF_THE_HISTORY_LIGHT_CONE"
    h=x["history_geometry"]
    assert h["projective_null_directions"]==4
    assert h["affine_lines_per_direction"]==9
    assert h["selected_null_lines"]==36
    assert h["history_points"]==27
    rows=x["M36_coordinates"]["family_records"]
    assert [r["family_name"] for r in rows]==["A","B","C","D"]
    assert {tuple(r["null_direction"]) for r in rows}=={
        (0,0,1),(1,0,0),(1,1,1),(1,2,1)
    }
    assert all(r["nine_parallel_lines_partition_F3_3"] for r in rows)
    assert all(r["mu_nu_to_quotient_affine"]["det_mod3"] in (1,2) for r in rows)
