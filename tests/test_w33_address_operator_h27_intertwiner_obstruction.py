from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_address_operator_h27_intertwiner_obstruction.py"
DATA=ROOT/"data/w33_address_operator_h27_intertwiner_obstruction.json"

def load():
    spec=importlib.util.spec_from_file_location("h27_intertwiner_obstruction",SCRIPT)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_exact_replay_matches_frozen_certificate():
    out=load().main(write=False)
    assert out==json.loads(DATA.read_text())

def test_rank_obstruction_and_scope():
    out=json.loads(DATA.read_text())
    assert out["status"]=="PASS_ADDRESS_OPERATOR_H27_LINEAR_INTERTWINER_RANK_OBSTRUCTION"
    assert out["address_module"]["center_spectrum"]=={"1":9,"omega":9,"omega^2":9}
    assert out["operator_module"]["center_spectrum"]=={"omega":27}
    assert out["intertwiner"]["Hom_dimension"]==27
    assert out["intertwiner"]["maximum_rank"]==9
    assert out["intertwiner"]["target_dimension"]==27
    assert out["intertwiner"]["invertible_intertwiner_exists"] is False
    assert out["intertwiner"]["rank_bound_sharp"] is True
    assert out["intertwiner"]["automorphism_twist_can_remove_obstruction"] is False
    assert "does not forbid a non-equivariant coordinate dictionary" in out["boundary"]
