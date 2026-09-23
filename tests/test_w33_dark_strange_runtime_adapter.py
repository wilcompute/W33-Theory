from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_dark_strange_runtime_adapter.py"
DATA=ROOT/"data/w33_dark_strange_runtime_adapter.json"
def load():
    s=importlib.util.spec_from_file_location("dark_runtime",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_fail_closed():
    o=json.loads(DATA.read_text())
    assert o["exact_handoff"]["decode_word"]=="X Z^2"
    assert o["exact_handoff"]["Clifford_only"] is True
    assert o["packet"]["ticks"]==72
    assert o["fail_closed"]["can_reserve_as_HESSE_T_RAW"] is False
    assert o["fail_closed"]["can_cast_to_M36_Q4_RAW"] is False
    assert o["fail_closed"]["fault_tolerant_injection_enabled"] is False
    assert all(o["checks"].values())
