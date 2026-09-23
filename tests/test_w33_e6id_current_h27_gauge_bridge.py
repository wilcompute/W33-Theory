from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e6id_current_h27_gauge_bridge.py"
DATA=ROOT/"data/w33_e6id_current_h27_gauge_bridge.json"
def load():
    s=importlib.util.spec_from_file_location("e6_current_h27_bridge",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_full_incidence_bridge():
    o=json.loads(DATA.read_text())
    assert o["search"]["search_nodes"]==27
    assert o["maps"]["e6id_to_current_H27_address"]["0"]==[0,0,0]
    assert o["incidence"]["mapped_full45_equal"] is True
    assert o["incidence"]["mapped_bad9_equal"] is True
    assert all(o["checks"].values())
