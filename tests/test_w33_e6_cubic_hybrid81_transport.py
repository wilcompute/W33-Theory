from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_e6_cubic_hybrid81_transport.py"
DATA=ROOT/"data/w33_e6_cubic_hybrid81_transport.json"
def load():
    s=importlib.util.spec_from_file_location("cubic_hybrid",SCRIPT);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())
def test_exact_transport_and_tangent_boundary():
    o=json.loads(DATA.read_text())
    assert o["root_tensor"]["signed_E6_triads"]==45
    assert o["root_tensor"]["nonzero_unordered_channels"]==810
    assert o["root_tensor"]["firewall_bad_channels"]==162
    assert o["root_tensor"]["root_output_span_dimension"]==81
    assert o["jacobian"]["root_basis_background_rank_set"]==[20]
    assert o["jacobian"]["collective_image_span_dimension"]==81
    assert o["jacobian"]["collectively_reaches_all_54_retyped_slots"] is True
    assert o["jacobian"]["single_root_background_rank54"] is False
    assert all(o["checks"].values())
