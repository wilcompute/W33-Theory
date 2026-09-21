from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_qpsi_mod12_unification.py"
    s=importlib.util.spec_from_file_location("qpsi12",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_single_integer_qpsi_unifies_all_discrete_e8_gradings():
    o=load().main(False)
    assert o["status"]=="PASS_SINGLE_INTEGER_QPSI_UNIFIES_E8_Z2_Z3_Z4_Z6_Z12"
    d=o["residue_dimensions"]
    assert d["mod2_matter_parity"]==[120,128]
    assert d["mod3_CE2_and_physical_FI"]==[86,81,81]
    assert d["mod4_Kummer"]==[60,64,60,64]
    assert d["mod6_FI_x_matter_parity"]==[54,48,33,32,33,48]
    assert d["mod12_common_refinement"]==[54,48,30,16,3,0,0,0,3,16,30,48]
    assert all(x["all_charges_match_grade_mod3"] for x in o["channel_mod3_certificate"].values())
