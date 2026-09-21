from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_twin_z6_single_node_difference.py"
def load():
    s=importlib.util.spec_from_file_location("z6diff",SRC);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_twin_z6_single_node_difference():
    o=load().main(False)
    assert o["status"]=="PASS_TWIN_Z6_DIFFER_BY_ONE_MARK2_COWEIGHT_PHASE"
    assert o["spectra"]["R"]==[92,64,14,0,14,64]
    assert o["R_power_ladder"]["1"]["semisimple_type"]=="D7"
    assert o["R_power_ladder"]["2"]["fixed_lie_dimension"]==92
    assert o["R_power_ladder"]["3"]["semisimple_type"]=="D8"
    assert o["checks"]["all_240_root_grades_add"] is True
