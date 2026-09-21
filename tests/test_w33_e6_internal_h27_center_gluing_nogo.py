from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_e6_internal_h27_center_gluing_nogo.py"
    s=importlib.util.spec_from_file_location("h27nog",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_pass369_center_cannot_glue_to_e6_center():
    o=load().main(False)
    assert o["status"]=="PASS_PASS369_CENTER_CANNOT_GLUE_TO_E6_CENTER"
    assert o["obstruction"]["Pass369_center_equals_ZE6"] is False
    assert o["obstruction"]["central_product_243_via_this_H27"] is False
    assert o["conditional_lift_consequence"]["generated_commuting_product_order_in_E6xSU3_mod_Z3"]==729
    assert o["hostile_control"]["correct_conditional_order"]=="27*27=729"
