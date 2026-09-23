from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_scheduler_operator_k81_intertwiner_obstruction.py"
DATA=ROOT/"data/w33_scheduler_operator_k81_intertwiner_obstruction.json"

def load():
    s=importlib.util.spec_from_file_location("k81_obstruction",SCRIPT)
    assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def test_replay_matches_frozen_certificate():
    assert load().main(write=False)==json.loads(DATA.read_text())

def test_full_81_rank_ceiling():
    out=json.loads(DATA.read_text())
    assert out["group"]["K_order"]==81
    assert out["group"]["derived_subgroup_order"]==3
    assert out["group"]["derived_subgroup_characteristic"] is True
    assert out["address_module"]["derived_center_spectrum"]=={"1":27,"omega":27,"omega^2":27}
    assert out["operator_module"]["derived_center_spectrum"]=={"omega":81}
    assert out["intertwiner"]["Hom_dimension"]==81
    assert out["intertwiner"]["maximum_rank"]==27
    assert out["intertwiner"]["invertible_equivariant_compiler_exists"] is False
    assert out["intertwiner"]["automorphism_twist_can_remove_obstruction"] is False
