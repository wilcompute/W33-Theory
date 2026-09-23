from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e8_full_graded_hybrid_atlas.py"
DATA=ROOT/"data/w33_e8_full_graded_hybrid_atlas.json"
def load():
    s=importlib.util.spec_from_file_location("e8atlas",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_atlas():
    o=json.loads(DATA.read_text())
    assert o["grading"]["dimensions"]=={"g0":86,"g1":81,"g2":81,"total":248}
    assert o["atlas"]["rank"]==248
    assert o["atlas"]["grade1_digest"]!=o["atlas"]["grade2_conjugate_digest"]
    assert o["grading"]["FI_center_trace"]=="5"
    assert all(o["checks"].values())
