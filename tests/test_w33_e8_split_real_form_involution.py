from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e8_split_real_form_involution.py"
DATA=ROOT/"data/w33_e8_split_real_form_involution.json"

def load():
    s=importlib.util.spec_from_file_location("e8_split_real_form",SCRIPT)
    assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())

def test_split_signature_and_hybrid_correction():
    o=json.loads(DATA.read_text())
    assert o["source_involution"]["unordered_basis_pairs_checked"]==30628
    assert o["source_involution"]["all_brackets_preserved"] is True
    assert o["killing_form"]["fixed_real_form_inertia"]=={"positive":128,"negative":120,"zero":0}
    assert o["killing_form"]["signature_difference"]==8
    assert o["killing_form"]["real_form"]=="E8(8), split real form"
    assert o["hybrid_transport"]["row_sign_ratio_minus"]==39
    assert o["hybrid_transport"]["matter_identity_swap_is_exact"] is False
    assert all(o["checks"].values())
