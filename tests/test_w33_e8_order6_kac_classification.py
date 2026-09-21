from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load():
    p = ROOT / "analysis/w33_e8_order6_kac_classification.py"
    s = importlib.util.spec_from_file_location("order6kac", p)
    assert s and s.loader
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_twin_order6_kac_classes_and_power_ladders():
    o = load().main(False)
    assert o["status"] == "PASS_UNIQUE_TWIN_ORDER6_E8_KAC_CLASSES_AND_POWER_LADDERS"
    assert o["normalized_exact_order6_kac_diagrams_enumerated"] == 20
    s = o["structural_FI_x_matter_parity_Z6"]
    h = o["flagship_holonomy_Z6"]
    assert s["unique_kac_coordinates"] == [2,0,0,0,1,0,0,0,0]
    assert h["unique_kac_coordinates"] == [0,0,0,0,1,0,0,1,0]
    assert s["power_ladder"]["2"]["semisimple_type"] == "A2+E6"
    assert h["power_ladder"]["2"]["semisimple_type"] == "D7"
    assert s["power_ladder"]["3"]["semisimple_type"] == "D8"
    assert h["power_ladder"]["3"]["semisimple_type"] == "D8"
