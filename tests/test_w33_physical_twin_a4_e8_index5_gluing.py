from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_physical_twin_a4_e8_index5_gluing.py"
def load():
    spec=importlib.util.spec_from_file_location("twin_a4",SRC);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def test_physical_twin_a4_index5_gluing():
    out=load().main(False)
    assert out["status"]=="PASS_PHYSICAL_TWIN_A4_INDEX5_E8_GLUING"
    assert out["physical_A4s"]["combined_rank"]==8
    assert out["physical_A4s"]["index_in_E8"]==5
    assert out["gluing"]["law"]=="c_gauge = 3*c_center (mod 5)"
    assert sum(r["count"] for r in out["root_projection_census"])==240
    assert sorted(out["branching"]["mixed_rep_dimensions"].values())==[50,50,50,50]
