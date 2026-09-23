from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_dark_strange_golay11_ft_lane.py"
DATA=ROOT/"data/w33_dark_strange_golay11_ft_lane.json"
def load():
    s=importlib.util.spec_from_file_location("golay11_ft",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_code_closed_hardware_open():
    o=json.loads(DATA.read_text())
    assert o["w33_code"]["quantum_CSS"]=="[[11,1,5]]_3"
    assert o["w33_code"]["dual_contained_in_G11"] is True
    assert o["w33_code"]["logical_distance"]==5
    assert o["admission_rule"]["published_depolarizing_threshold_approx"]==0.38715
    assert o["physical_fault_tolerant_lane_enabled"] is False
    assert all(o["checks"].values())
