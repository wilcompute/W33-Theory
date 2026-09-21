from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_physical_fi_is_h27_center.py"
    s=importlib.util.spec_from_file_location("fi_h27",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_physical_fi_is_exact_h27_center_character():
    o=load().main(False)
    assert o["status"]=="PASS_PHYSICAL_FI_Z3_EQUALS_QUTRIT_HEISENBERG_CENTER_CHARACTER"
    assert o["H27"]["order"]==27
    assert o["H27"]["center_order"]==3
    assert o["H27"]["commutator"]=="[Z,X]=omega I"
    assert o["E8"]["adjoint_eigendimensions"]==[86,81,81]
    assert o["identity"]["same_central_character"] is True
    assert "Lie su(3)" in o["what_remains_open"]
