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
    firewall=o["object_type_firewall"]
    assert firewall["Q8_objectwise_equivariant_bijections"]==1179648
    assert firewall["full_Clifford_intertwiner_space_dimension"]==7
    assert firewall["Q8_bijections_contain_Fourier_assignments_as_subset"] is False
    assert firewall["numeric_collapse_1179648_to_6_claimed"] is False
    selector=o["character_assignment_selector"]
    assert selector["safe_sheet_beta_order"]==[0,1,2]
    assert selector["Fourier_ansatz_character_assignments"]==6
    assert selector["neutral_beta0_trivial_survivors"]==2
    assert o["canonical_cubic_signs"]["ordinary36"]=={"plus":20,"minus":16}
    assert o["selector_verdict"]["real_E6_cubic_signs_select_unique_orientation"] is False
