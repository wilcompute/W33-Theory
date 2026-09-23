from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_h27_cubic_representation_transducer.py"
DATA=ROOT/"data/w33_h27_cubic_representation_transducer.json"
def load():
    s=importlib.util.spec_from_file_location("cubic_transducer",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_rules():
    o=json.loads(DATA.read_text())
    assert o["tensor_rules"]["S2_t_x_S2_u"]=="3 S1_(t+u)"
    assert o["cubic_invariants"]["charge_zero_external_triples_per_central_character"]==9
    assert o["cubic_invariants"]["total_singlet_multiplicity_across_all_cases"]==54
    assert all(o["checks"].values())
