from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_hesse_pappus_45_270_instruction_compiler.py"
DATA=ROOT/"data/w33_hesse_pappus_45_270_instruction_compiler.json"
def load():
    s=importlib.util.spec_from_file_location("c270",SCRIPT); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_270_contract():
    o=json.loads(DATA.read_text())
    assert o["base_layer"]["tritangents"]==45
    assert o["instruction_layer"]["total"]==270
    assert o["instruction_layer"]["ordinary"]==216
    assert o["instruction_layer"]["fiber"]==54
    assert o["compiler"]["full_rank"]==270
    assert o["compiler"]["full_nonzeros"]==702
    assert o["pappus_lift"]["decorated_components"]==24
