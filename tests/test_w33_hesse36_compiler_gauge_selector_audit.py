from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_compiler_gauge_selector_audit.py"
DATA=ROOT/"data/w33_hesse36_compiler_gauge_selector_audit.json"
def load():
    s=importlib.util.spec_from_file_location("selector",SCRIPT); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_selector_boundary():
    o=json.loads(DATA.read_text())
    assert o["reduction"]["Q8_equivariant_gauges"]==1179648
    assert o["reduction"]["full_Clifford_character_assignments"]==6
    assert o["reduction"]["neutral_beta0_trivial_survivors"]==2
    assert o["canonical_cubic_signs"]["ordinary36"]=={"plus":20,"minus":16}
    assert o["selector_verdict"]["real_E6_cubic_signs_select_unique_orientation"] is False
