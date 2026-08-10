from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(n,name):
 p=ROOT/'data'/f'w33_pass{n}_{name}.json'
 d=json.loads(p.read_text(encoding="utf-8"));assert d['status']=='PASS';assert all(d['checks'].values());return d

def test_pass721_formal_rigidity_local_h2():
 d=load(721,'formal_rigidity_local_h2_census')
 assert d['minimal_projective_resolution_over_F2E']['Ext_dimensions_H0_H1_H2']==[441,74,100]
 assert d['degree_two_local_census']['H2_E_traceless_dimension']==90

def test_pass722_cycle_two_branch_order():
 d=load(722,'cycle_lattice_two_branch_order')
 assert d['integral_two_branch_operator']['branch_dimensions']=={'M_0_homology_quotient':81,'M_4_triangle_boundaries':120}
 assert d['extension_and_gluing']['gluing_module']=='(Z/4)^66'

def test_pass723_self_calibrating_waveform():
 d=load(723,'self_calibrating_waveform_identifier')
 assert d['adaptive_schedule_compiler']['selected']=='balanced_g4'
 assert d['heldout_falsifier']['selected_schedule']['maximum_q95']<.05

def test_pass724_nonfactorizable_matrix_cs():
 d=load(724,'nonfactorizable_dropout_matrix_cs')
 assert d['nonparametric_matrix_confidence_sequence']['all_operator_bounds_covered']
 assert d['residual_recovery']['terminal_errors']['sparse_nonzero_offdiag']>0
 assert d['covariance_and_selection']['direct_over_factorized']<.01

def test_pass725_complete_phase_compiler():
 d=load(725,'complete_phase_semilinear_compiler')
 assert d['complete_phase_classification']['distinct_phases']==22
 assert d['complete_phase_classification']['cells']==7776
 assert d['automatic_calibration_credit']['nominal_kappa1_minimum_credit']==2
