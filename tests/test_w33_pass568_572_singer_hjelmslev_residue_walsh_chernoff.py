from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_pass568_intersection_design():
 p=load('w33_pass568_singer_intersection_design.json')
 assert p['status']=='PASS'
 assert p['ambient']['Singer_normalizer_conjugates']==336
 assert p['incidence_summary']['witting_orbit_count']==10
 assert p['families']['Witting_fixed_16_line_stabilizer']['intersection_signature_census']=={'1|1^1':240,'2|1^1,2^1':72,'4|1^1,2^1,4^2':24}

def test_pass569_full_f3_13_image():
 p=load('w33_pass569_z9_coupled_affine_radial_quadratic.json')
 f=p['layers'][-1]
 assert p['status']=='PASS' and p['family']['parameter_space']=='F3^13'
 assert f['sections']==3**13 and f['distinct_charpolys']==221451
 assert f['projective_parameter_words']==797162
 assert f['projective_injectivity_ratio']<0.28

def test_pass570_residue_formal_boundary():
 p=load('w33_pass570_cyclotomic_residue_formal.json')
 assert p['status']=='PASS'
 assert p['checks']['reduction_mod5_is_x4']
 assert p['checks']['quotient_by_lambda_has_residue_F5']
 assert len(p['remaining_completion_obligations'])==4

def test_pass571_character_decomposition():
 p=load('w33_pass571_twisted_walsh_representation.json')
 assert p['status']=='PASS'
 assert p['group']['irreducible_degrees']==[1]*8+[2]*8
 assert p['signed_walsh_representation']['irreducible_multiplicities']==[104]*8+[204]*8
 assert len(p['formula_signatures'])==6

def test_pass572_chernoff_boundary():
 p=load('w33_pass572_analytic_sequential_bound.json')
 assert p['status']=='PASS'
 assert p['checks']['joint_bottleneck_is_orientation_pair']
 assert p['checks']['coarse_union_bound_does_not_certify_empirical_gain']
 assert all(r['analytic_relative_reduction']<0 for r in p['results'].values())

def test_release_lock():
 p=load('w33_pass568_572_singer_hjelmslev_residue_walsh_chernoff_release.json')
 assert p['status']=='PASS'
 assert p['owner_check_total']==53
 assert all(p['release_checks'].values())
