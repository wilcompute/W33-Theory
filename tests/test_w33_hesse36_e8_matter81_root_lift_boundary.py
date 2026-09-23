from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_e8_matter81_root_lift_boundary.py"
DATA=ROOT/"data/w33_hesse36_e8_matter81_root_lift_boundary.json"
def load():
    s=importlib.util.spec_from_file_location("rootlift",SCRIPT); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_ranks_and_firewalls():
    o=json.loads(DATA.read_text())
    assert o["incidence"]["base_27x36_rank"]==21
    assert o["incidence"]["ordinary_81x216_rank"]==73
    assert o["incidence"]["full_81x270_rank"]==73
    assert o["incidence"]["dark_root_dimension"]==8
    assert o["incidence"]["ordinary_cubics_per_root"]==8
    assert o["incidence"]["fiber_cubics_per_root"]==2
    assert o["selection_rules"]["canonical_signs_cannot_change_incidence_rank"] is True
    assert o["pauli243_firewall"]["direct_objectwise_identification"] is False
