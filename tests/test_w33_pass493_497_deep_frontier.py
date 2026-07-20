from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    p=ROOT/'analysis'/name
    s=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_pass493_quick_exact():
    p=load('w33_pass493_mixed_characteristic_falsifiers.py').main_payload(full=False)
    assert p['status']=='PASS'
    assert [r['attained_depth'] for r in p['rings']]==[18,18]

def test_pass494_incidence():
    p=load('w33_pass494_hjelmslev_reduction_incidence.py').main_payload()
    assert p['status']=='PASS'
    assert all(c['gram_is_p_identity'] and c['tower_identity'] for c in p['cases'])

def test_pass495_phase_diagram():
    p=load('w33_pass495_arithmetic_geometric_minimum_law.py').main_payload()
    assert p['status']=='PASS'
    assert len(p['existing_data'])==13
    assert len(p['preregistered_falsifiers'])==8

def test_pass496_symbolic_nogo():
    m=load('w33_pass496_relative_norm_and_different_nogo.py')
    assert m.projective_depth(5,2)==30
    assert m.different_exponent(5,2)==35

def test_pass497_optical_invariants():
    m=load('w33_pass497_optical_depth_observable.py')
    r,_=m.run(m.F9,20,1e-4,497)
    assert r['weyl_frobenius_norm_exact']
    assert abs(r['metrics']['phase_noise_gain']['mean']-1)<0.2
    assert len(m.real_galois_reps(9))==3
    assert len(m.real_galois_reps(25))==10
