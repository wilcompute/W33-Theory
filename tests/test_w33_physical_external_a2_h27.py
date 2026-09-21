from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_physical_external_a2_h27.py"
    s=importlib.util.spec_from_file_location("physical_a2_h27",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_physical_external_a2_h27():
    o=load().main(False)
    assert o["status"]=="PASS_EXPLICIT_PHYSICAL_EXTERNAL_A2_HEISENBERG_27_IN_E8"
    assert o["frozen_root_gauge"]["canonical_clock_character_mod3"]==[0,0,0,0,2,2,0,0]
    assert o["clock_uniqueness"]["number_of_solutions"]==3
    assert o["spectra"]["clock_adjoint_eigendimensions"]==[134,57,57]
    assert o["spectra"]["FI_grade_by_clock_grade_root_counts"]["1"]=={"0":27,"1":27,"2":27}
    assert o["H27"]["order"]==27
    assert o["checks"]["rootwise_Heisenberg_commutator"] is True
