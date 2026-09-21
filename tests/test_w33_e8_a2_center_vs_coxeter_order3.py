from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_e8_a2_center_vs_coxeter_order3.py"
    s=importlib.util.spec_from_file_location("a2z3split",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_physical_a2_center_and_pass1147_coxeter_are_distinct_order3_classes():
    o=load().main(False)
    assert o["status"]=="PASS_PHYSICAL_A2_CENTER_AND_PASS1147_COXETER_ARE_DISTINCT_E8_ORDER3_CLASSES"
    assert len(o["normalized_exact_order3_inner_kac_classes"])==4
    p=o["physical_FI_center_Z3"]
    c=o["pass1147_A2_coxeter_C3"]
    assert p["adjoint_eigendimensions"]==[86,81,81]
    assert p["unique_kac_coordinates"]==[0,0,0,0,0,1,0,0,0]
    assert p["fixed_reductive_algebra"]=="E6+A2"
    assert c["adjoint_eigendimensions"]==[134,57,57]
    assert c["unique_kac_coordinates"]==[1,0,0,0,0,0,1,0,0]
    assert c["fixed_reductive_algebra"]=="E7+u1"
    assert o["separation"]["same_E8_conjugacy_class"] is False
