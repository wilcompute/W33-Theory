from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_physical_fi_matter_parity_z6_quotient.py"
def load():
    spec=importlib.util.spec_from_file_location("z6q",SRC);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def test_physical_fi_matter_parity_z6_quotient():
    out=load().main(False)
    assert out["status"]=="PASS_PHYSICAL_FI_MATTER_PARITY_Z6_QUOTIENT_WITH_HOLONOMY_FIREWALL"
    assert out["joint_Z2xZ3_dimensions"]["table"]==[[54,33,33],[32,48,48]]
    assert out["Z6"]["dimensions"]==[54,48,33,32,33,48]
    assert out["Z6"]["trace_powers_m0_to_m5"]==[248,37,5,-8,5,37]
    assert out["Z6"]["fixed_reductive_algebra"]=="so(10)+sl(3)+u(1)"
    assert out["physical_flagship_C6_firewall"]["same_order6_element"] is False
