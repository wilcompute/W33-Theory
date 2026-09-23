from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_photonic_coherent_retiming.py"
DATA=ROOT/"data/w33_hesse36_photonic_coherent_retiming.json"
def load():
    s=importlib.util.spec_from_file_location("retime",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_retiming():
    o=json.loads(DATA.read_text())
    s=o["schedule"]
    assert s["wave_occupancy"]==[9,3]
    assert s["wave0_channels_postheld"]==27
    assert s["wave1_channels_preheld"]==9
    assert s["F3_traversals_per_channel"]==1
    assert s["HOLD_traversals_per_channel"]==1
    assert o["coherent_optical_budget"]["tritter_process_fidelity_min"] is None
    assert all(o["checks"].values())
