from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass453_cyclotomic_covariance as p453
import w33_pass454_q7_field_falsifier as p454
import w33_pass455_frobenius_schur_indicators as p455
import w33_pass456_q5_collision_anatomy as p456
import w33_pass457_formal_perp_audit as p457

def test_pass453_cyclotomic_fields():
    p=p453.build_payload();assert p['status']=='PASS';assert p['q5']['number_field_discriminant']==5;assert p['q7']['number_field_discriminant']==49

def test_pass454_q7_falsifier():
    p=p454.build_payload();assert p['status']=='PASS';assert p['distinct_spectra']==80;assert p['quadratic_field_kernels']=={}

def test_pass455_fs_profiles():
    p=p455.build_payload();assert p['status']=='PASS';assert {(v['ordinary'],v['twisted_tau']) for v in p['results'].values()}=={(0.0,1.0)}

def test_pass456_genuine_collision():
    p=p456.build_payload();assert p['status']=='PASS';g=[r for r in p['collisions'] if not r['affine_aut_equivalent']];assert len(g)==1;assert not g[0]['graph_isomorphic'];assert g[0]['critical_groups_equal']

def test_pass457_formal_audit():
    p=p457.build_payload();assert p['status']=='PASS';assert p['checks']['uses_mathlib_orthogonal_le'];assert p['checks']['no_sorry']
