from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_difference_R_so14_u1_five_grading():
    p=ROOT/"analysis/w33_difference_R_so14_u1_five_grading.py"
    s=importlib.util.spec_from_file_location("so14r",p);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);o=m.main(False)
    assert o["status"]=="PASS_INTERNAL_SO14_U1_FIVE_GRADING_WITH_HIGHEST_WEIGHTS"
    assert o["root_charge_histogram"]=={"-2":14,"-1":64,"0":84,"1":64,"2":14}
    assert o["neutral"]["root_system"]=="D7"
    assert o["cube_parity"]["fixed_lie_dimension"]==120
    assert all(v["weyl_orbit_size"] in (14,64) for v in o["charged_sectors"].values())
