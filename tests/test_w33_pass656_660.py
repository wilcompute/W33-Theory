from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass656_two_character_ext_kuranishi.py',
 'w33_pass657_d8_torsor_cocycle_minimal_marking.py',
 'w33_pass658_fisher_optimal_flat_probe_tomography.py',
 'w33_pass659_unknown_drifting_propensity_eprocess.py',
 'w33_pass660_continuous_minimax_polyhedral_complex.py']

def load(name):
    path=ROOT/'analysis'/name;spec=importlib.util.spec_from_file_location(path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_pass656_ext_quiver():
    p=load(SCRIPTS[0]).payload();assert p['status']=='PASS';assert p['Ext1_matrix_rows_source_columns_target']==[['0','Z/4'],['Z/4','0']];assert p['direct_sum_deformation_complex']['unobstructed_count']==8

def test_pass657_minimal_marking():
    p=load(SCRIPTS[1]).payload();assert p['status']=='PASS';assert p['minimal_marking']['states']==8;assert p['minimal_marking']['stabilizer']=='trivial'

def test_pass658_flat_probe():
    p=load(SCRIPTS[2]).payload();assert p['status']=='PASS';assert p['flat_probe']['minimum_amplitude']>.249999;assert p['graph_design']['configuration_count']==30

def test_pass659_drifting_propensities():
    p=load(SCRIPTS[3]).payload();assert p['status']=='PASS';assert p['replay']['dynamic_over_frozen_error_ratio']<.2;assert p['replay']['whitened_true_covariance_max_eigenvalue']<1

def test_pass660_continuous_region():
    p=load(SCRIPTS[4]).payload();assert p['status']=='PASS';assert p['parametric_certification']['mismatches']==0;assert p['nominal']['Linf_radius']==1
