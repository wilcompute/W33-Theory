from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[
 ('w33_pass681_h1_cocycle_rigidity_h2_scalar.py','w33_pass681_h1_cocycle_rigidity_h2_scalar.json'),
 ('w33_pass682_flatblock_h1_branch_separation.py','w33_pass682_flatblock_h1_branch_separation.json'),
 ('w33_pass683_waveform_level_optical_memory_falsifier.py','w33_pass683_waveform_level_optical_memory_falsifier.json'),
 ('w33_pass684_open_ended_propensity_confidence_process.py','w33_pass684_open_ended_propensity_confidence_process.json'),
 ('w33_pass685_hybrid_symbolic_controller_complex.py','w33_pass685_hybrid_symbolic_controller_complex.json')]

def checked(i):
    script,ledger=CASES[i]
    subprocess.run([sys.executable,str(ROOT/'analysis'/script),'--check'],check=True,timeout=180,capture_output=True,text=True)
    return json.loads((ROOT/'data'/ledger).read_text(encoding="utf-8"))

def test_pass685_hybrid_symbolic_complex():
    # The workflow runs the Pass 685 --check separately. Read the locked ledger here so
    # the focused pytest suite uses only four child Python processes in constrained CI.
    p=json.loads((ROOT/'data'/CASES[4][1]).read_text(encoding="utf-8"));assert p['status']=='PASS';assert p['hybrid_seven_dimensional_complex']['declared_integer_atlas_cells']==7776;assert p['hybrid_seven_dimensional_complex']['distinct_root_phases']==22;assert p['exact_nominal_science_chamber']['integer_box_mismatches']==0;assert p['calibration_redesign']['tested_coefficients'][-1]['unique_pair']

def test_pass681_h1_rigidity_and_scalar_h2():
    p=checked(0);assert p['status']=='PASS';assert p['degree_one']['H1_dimension']==0;assert p['degree_two']['ambient_lower_bound_dimension']==1;assert p['checks']['selected_relations_sufficient_by_dimension_squeeze']

def test_pass682_one_branch_after_cyclotomic_correction():
    p=checked(1);assert p['status']=='PASS';assert p['chain_operator']['H1_dimension']==81;assert p['flatblock_specialization']['represented_branch']=='M_0';assert p['flatblock_specialization']['pass676_real_cyclotomic_correction']['3_primary_rank']==4

def test_pass683_waveform_falsifier():
    p=checked(2);assert p['status']=='PASS';assert p['scheduling_result']['balanced_interleaved']['maximum_channel_abs_error_q95']<.05;assert p['stress_envelope']['maximum_passing_stress']==1.75;assert p['stress_envelope']['first_failing_stress']==2.0

def test_pass684_open_ended_propensity_process():
    p=checked(3);assert p['status']=='PASS';assert p['alternative_replay']['first_detection']['delay']<8000;assert p['alternative_replay']['average_pilots_after_burnin']<19;assert p['alternative_replay']['covariance']['dynamic_over_frozen_ratio']<.02;assert p['null_replay']['terminal_mixture_log_e']<p['null_replay']['threshold_log_e']
