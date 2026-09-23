from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e8_hybrid_charge_conjugation.py"
DATA=ROOT/"data/w33_e8_hybrid_charge_conjugation.json"
def load():
    s=importlib.util.spec_from_file_location("charge_conj",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_involution():
    o=json.loads(DATA.read_text())
    assert o["involution"]["carrier_dimension"]==248
    assert o["involution"]["fixed_basis_labels"]==86
    assert o["involution"]["exchanged_basis_pairs"]==81
    assert o["FI_center"]["law"]=="C Z_FI C^-1 = Z_FI"
    assert o["compiler_orientation"]["C_exchanges_them"] is True
    assert all(o["checks"].values())
