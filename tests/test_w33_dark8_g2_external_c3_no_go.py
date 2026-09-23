from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_dark8_g2_external_c3_no_go.py"
DATA=ROOT/"data/w33_dark8_g2_external_c3_no_go.json"
def load():
    s=importlib.util.spec_from_file_location("g2_c3_no_go",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_strict_extension_killed():
    o=json.loads(DATA.read_text())
    assert o["dark_K_module"]["C3_ext_exponent_multiplicities"]=={"0":6,"1":1,"2":1}
    assert o["candidate_G2_branching"]["C3_scalar_on_seven"] is False
    assert o["obstruction"]["strict_G2_x_C3_extension_exists"] is False
    assert o["what_survives"]["noncommuting_larger_envelope_ruled_out"] is False
    assert all(o["checks"].values())
