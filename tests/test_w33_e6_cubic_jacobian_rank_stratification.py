from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e6_cubic_jacobian_rank_stratification.py"
DATA=ROOT/"data/w33_e6_cubic_jacobian_rank_stratification.json"
def load():
    s=importlib.util.spec_from_file_location("cubic_rank_strata",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_rank_strata_and_firewall():
    o=json.loads(DATA.read_text())
    r=o["exact_rank_strata"]
    assert [r[k]["rank"] for k in ("root0","uniform","linear","quadratic")]==[20,54,54,78]
    assert r["quadratic"]["kernel_dimension"]==3
    assert o["compiler_consequence"]["rank_capacity_margin"]==24
    assert o["compiler_consequence"]["specific_54_coordinate_alignment_proved"] is False
    assert all(o["checks"].values())
