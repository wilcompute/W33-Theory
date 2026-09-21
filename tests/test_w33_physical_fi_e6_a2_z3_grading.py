from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_physical_fi_e6_a2_z3_grading.py"
def load():
    spec=importlib.util.spec_from_file_location("fi_e6a2",SRC);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def test_physical_fi_realizes_e6_a2_z3_grading():
    out=load().main(False)
    assert out["status"]=="PASS_PHYSICAL_FI_REALIZES_E6_A2_Z3_GRADING"
    assert out["physical_FI_projection"]["three_times_diagonal"]==[-5,3,1,-5,6]
    assert out["organizer_SU5"]["root_grades"]=={"0":8,"1/3":6,"2/3":6}
    assert out["E8"]["root_grades"]=={"0":78,"1/3":81,"2/3":81}
    assert out["E8"]["fixed_lie_algebra"]=="E6 + A2"
