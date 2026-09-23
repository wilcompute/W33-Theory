from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_fiber54_vs_equivariance54_no_go.py"
DATA=ROOT/"data/w33_fiber54_vs_equivariance54_no_go.json"
def load():
    s=importlib.util.spec_from_file_location("f54",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_no_go():
    o=json.loads(DATA.read_text())
    assert o["fiber_sector"]["dimension"]==54
    assert o["equivariance_deficit_sector"]["dimension"]==54
    assert o["comparison"]["isomorphic_as_K_modules"] is False
    assert o["comparison"]["maximum_common_equivariant_rank"]==27
    assert o["comparison"]["unmatched_dimensions_each_side"]==27
    assert all(o["checks"].values())
