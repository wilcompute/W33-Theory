from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_dark8_g2_branching_shadow.py"
DATA=ROOT/"data/w33_dark8_g2_branching_shadow.json"
def load():
    s=importlib.util.spec_from_file_location("g2shadow",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_branching():
    o=json.loads(DATA.read_text())
    assert o["A2_adjoint_test"]["matches_dark8"] is False
    assert o["G2_shadow"]["matches_dark8_after_H27_restriction"] is True
    assert o["G2_shadow"]["constructed_G2_action"] is False
    assert o["dark8_restricted_to_H27"]["H27_center_trace"]==-1
    assert all(o["checks"].values())
