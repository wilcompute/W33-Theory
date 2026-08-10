from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[
 ('w33_pass651_closed_form_2adic_tree.py','w33_pass651_closed_form_2adic_tree.json'),
 ('w33_pass652_d8_descent_defect_signature.py','w33_pass652_d8_descent_defect_signature.json'),
 ('w33_pass653_gauge_complete_optical_tomography.py','w33_pass653_gauge_complete_optical_tomography.json'),
 ('w33_pass654_correlated_dropout_matrix_eprocess.py','w33_pass654_correlated_dropout_matrix_eprocess.json'),
 ('w33_pass655_minimax_policy_stability.py','w33_pass655_minimax_policy_stability.json'),
]

def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_certificates_are_reproducible():
    for script,_ in CASES:
        subprocess.run([sys.executable,str(ROOT/'analysis'/script),'--check'],check=True,cwd=ROOT)

def test_all_pass_and_checks_true():
    for _,ledger in CASES:
        data=load(ledger);assert data['status']=='PASS';assert all(data['checks'].values())

def test_closed_form_and_defect_signature():
    p651=load(CASES[0][1]);assert p651['closed_form']['stable_cardinality']==8;assert p651['closed_form']['infinite_compatible_branches']==[0,4]
    assert p651['finite_phantom_barcode']['maximum_extra_persistence_edges']==1
    p652=load(CASES[1][1]);assert p652['defect_histogram']=={'0':1,'1':2,'2':1,'3':4};assert p652['defect_sum']==16

def test_optical_and_dropout_corrections():
    p653=load(CASES[2][1]);assert p653['calibration_budget']['total_settings']==286;assert p653['phase_lock_stage']['reconstruction_frobenius_error']<1e-10
    p654=load(CASES[3][1]);assert abs(p654['missingness_model']['exact_offdiagonal_inflation']-10/9)<1e-12
    assert p654['replay']['whitened_true_covariance_max_eigenvalue']<1

def test_policy_nonuniqueness_and_margin():
    p=load(CASES[4][1]);assert p['nominal']['minimax_value']==12
    assert p['nominal']['optimal_root_actions']==['trace1_guard_tagged','trace2_covariance_tagged']
    assert p['nominal']['optimality_margin']==1;assert p['integer_cost_robustness']['all_pair_only']
