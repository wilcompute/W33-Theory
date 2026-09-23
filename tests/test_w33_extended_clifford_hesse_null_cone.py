from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_extended_clifford_hesse_null_cone.py"
DATA=ROOT/"data/w33_extended_clifford_hesse_null_cone.json"

def load():
    s=importlib.util.spec_from_file_location("extended_clifford_hesse_null",SCRIPT)
    assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_replay():
    assert load().main(write=False)==json.loads(DATA.read_text())

def test_factor_two_and_null_cone():
    o=json.loads(DATA.read_text())
    c=o["clifford_extension"]; q=o["affine_hull_null_cone"]
    assert (c["physical_clifford_lift_order"],c["projective_unitary_order"])==(648,216)
    assert c["extended_projective_order"]==432
    assert c["extended_with_C3_center_order"]==1296
    assert o["four_direction_action"]["unitary_image"]=="A4"
    assert o["four_direction_action"]["extended_image"]=="S4"
    assert o["four_direction_action"]["conjugation_permutation"]==[0,1,3,2]
    assert q["special_orthogonal_group_order"]==24
    assert q["SO_ray_permutation_group"]=="S4"
    assert q["direction_and_null_ray_permutation_sets_equal"] is True
    assert all(o["checks"].values())
