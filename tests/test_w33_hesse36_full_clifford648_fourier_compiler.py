from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_full_clifford648_fourier_compiler.py"
DATA=ROOT/"data/w33_hesse36_full_clifford648_fourier_compiler.json"
def load():
    s=importlib.util.spec_from_file_location("full648",SCRIPT); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_contract():
    o=json.loads(DATA.read_text())
    assert o["group"]["order"]==648
    assert o["group"]["source_stabilizer_order"]==18
    assert o["group"]["target_sheet_stabilizer_order"]==54
    assert o["orbits"]["safe36"]==[12,12,12]
    assert o["compiler"]["rank"]==36
    assert o["compiler"]["nonzero_entries"]==108
    assert o["compiler"]["fiber_count"]==12
    assert o["compiler"]["matrix_digest"].startswith("sha256:")
    assert all(o["checks"].values())
