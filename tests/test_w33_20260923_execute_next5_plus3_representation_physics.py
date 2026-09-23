from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_20260923_execute_next5_plus3_representation_physics.py"
FROZEN=ROOT/"data/w33_20260923_execute_next5_plus3_representation_physics.json"


def load_module():
    spec=importlib.util.spec_from_file_location("w33_next5_plus3_representation_physics",SCRIPT)
    assert spec and spec.loader
    m=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=m
    spec.loader.exec_module(m)
    return m


def test_dirac_module_and_q3_realification():
    m=load_module()
    a1=m.attack1_dirac_ladder()
    a2=m.attack2_q3_realification()

    assert a1["W33_identity"] == "{24/5,96/5,216/5}=(24/5)*{1^2,2^2,3^2}"
    assert a1["pure_Casimir_explanation_refuted"] is True
    assert a1["weighted_bands"]["0_H1"]["multiplicity"] == 81

    assert a2["single_sector"]["retained_phase_Clifford_order"] == 648
    assert abs(a2["single_sector"]["Frobenius_Schur_indicator"][0]) < 1e-10
    assert a2["full_similitude"]["order"] == 1296
    assert a2["full_similitude"]["conjugacy_class_count"] == 18
    assert abs(a2["full_similitude"]["character_norm"]-1) < 1e-10
    assert abs(a2["full_similitude"]["Frobenius_Schur_indicator"][0]-1) < 1e-10
    assert a2["full_similitude"]["all_determinant_odd_class_traces_zero"] is True
    assert a2["trace_field"]["field"] == "Q"
    assert a2["trace_field"]["order18_elements_absent"] is True


def test_z3_pairing_and_FI_reference_arm():
    m=load_module()
    a3=m.attack3_z3_antiunitary_pairing()
    a4=m.attack4_fi_reference_arm()

    assert a3["synthetic_check"]["max_T2_minus_C2"] < 1e-12
    assert a3["synthetic_check"]["max_HT_minus_TH"] < 1e-12
    assert a3["synthetic_check"]["matter_partner_overlap"] < 1e-12

    abi=a4["existing_Holonet_ABI"]
    assert abi["120deg_Hesse_bins"] == ["H1","H4","H7"]
    assert abi["120deg_probe_opportunities_per_mirror_atlas"] == 180
    assert abi["120deg_probe_opportunities_per_supercycle"] == 4320
    assert a4["fail_closed_admission"]["nominal_visibility_passes_99pct_gate"] is False
    assert a4["shot_budget_Fisher_design"]["supercycles_needed_if_one_detected_event_per_opportunity_at_floor"] == 2


def test_chernoff_nuisance_and_outside_box():
    m=load_module()
    rows=m._chernoff_rows()
    assert rows["9"][0]["optimal_setting_weights"] == [0.0,1.0,0.0]
    assert rows["9"][1]["optimal_setting_weights"] == [1.0,0.0,0.0]
    assert rows["9"][2]["optimal_setting_weights"] == [0.0,0.0,1.0]
    assert rows["9"][3]["optimal_setting_weights"] == [1/3,1/3,1/3]

    # Small deterministic replay: this is a regression, not the frozen 5000-trial study.
    sim=m.nuisance_adaptive_simulation(trials=200,seed=20260923)
    assert sim["results"]["9"]["mean"] < sim["results"]["7"]["mean"]

    frozen=json.loads(FROZEN.read_text())
    assert frozen["status"].startswith("PASS_NEXT5_PLUS3")
    assert all(frozen["checks"].values())
    assert frozen["outside_box"]["A_finite_McKean_Singer_index"]["Euler_characteristic"] == "40-240+160-40=-80"
    assert frozen["outside_box"]["C_distributed_FI_phase_frame"]["optimal_broadcast_ticks"] == 7
