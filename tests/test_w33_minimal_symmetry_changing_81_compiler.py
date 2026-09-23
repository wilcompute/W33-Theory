from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_minimal_symmetry_changing_81_compiler.py"
DATA=ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json"
def load():
    s=importlib.util.spec_from_file_location("min81",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_minimality():
    o=json.loads(DATA.read_text())
    c=o["compiler"]
    assert c["unitary"] and c["bijective"]
    assert c["symmetry_preserving_coordinates"]==27
    assert c["symmetry_changing_coordinates"]==54
    assert c["symmetry_change_lower_bound"]==54
    assert c["lower_bound_saturated"] is True
    assert c["mapping_digest"].startswith("sha256:")
    assert all(o["checks"].values())
