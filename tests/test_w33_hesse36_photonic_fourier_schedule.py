from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse36_photonic_fourier_schedule.py"
DATA=ROOT/"data/w33_hesse36_photonic_fourier_schedule.json"
def load():
    s=importlib.util.spec_from_file_location("photo",SCRIPT); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_schedule():
    o=json.loads(DATA.read_text())
    assert o["schedule"]["fiber_count"]==12
    assert list(map(len,o["schedule"]["waves"]))==[9,3]
    assert o["schedule"]["active_mixer_depth_per_channel"]==1
    assert o["optical_budget"]["process_fidelity_min"] is None
    assert o["magic_boundary"]["M36_injection_enabled"] is False
