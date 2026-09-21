from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_physical_a2_clifford648_w33_stabilizer_bridge.py"
    s=importlib.util.spec_from_file_location("c648bridge",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_physical_a2_clifford648_matches_w33_point_stabilizer():
    o=load().main(False)
    assert o["status"]=="PASS_PHYSICAL_A2_H27_NORMALIZER_EQUALS_W33_CLIFFORD648_AT_QUOTIENT_ACTION_LEVEL"
    assert o["physical_E8_side"]["normalizer_order"]==648
    assert o["W33_side"]["quotient_matrix_count"]==24
    assert o["W33_side"]["quotient_matrix_set_equals_physical_SL23"] is True
    assert o["generator_relations"]["F_order"]==4
    assert o["generator_relations"]["P_order"]==3
