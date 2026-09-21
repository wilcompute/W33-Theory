from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_e8_trinification_two_qutrit_pauli243.py"
    s=importlib.util.spec_from_file_location("pauli243",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_trinification_two_qutrit_pauli243_inside_e8():
    o=load().main(False)
    assert o["status"]=="PASS_E8_CONTAINS_TRINIFICATION_CENTRAL_PRODUCT_TWO_QUTRIT_PAULI243"
    assert o["trinification"]["E6_center_action_on_three_nonets"]==[1,1,1]
    assert o["E8_gluing"]["centers_identified"] is True
    assert o["two_qutrit_pauli"]["order"]==243
    assert o["two_qutrit_pauli"]["exponent"]==3
    assert o["two_qutrit_pauli"]["center_order"]==3
    assert o["two_qutrit_pauli"]["derived_order"]==3
    assert o["two_qutrit_pauli"]["projective_order"]==81
    assert o["checks"]["new_internal_commutator_is_ZE6"] is True
