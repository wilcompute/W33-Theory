from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_e8_z12_clifford_mu12_character_bridge.py"
    s=importlib.util.spec_from_file_location("mu12bridge",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_explicit_e8_z12_to_clifford_mu12_character_bridge():
    o=load().main(False)
    assert o["status"]=="PASS_EXPLICIT_FAITHFUL_Z12_TO_MU12_CHARACTER_BRIDGE"
    assert o["character"]["isomorphism"] is True
    assert o["E8_phase_multiplicities_exponents_0_to_11"]==[54,48,30,16,3,0,0,0,3,16,30,48]
    assert o["cubic_phase_selection"]["total_cubics"]==45
    assert o["cubic_phase_selection"]["all_character_products_trivial"] is True
    assert o["subgroup_character_ladder"]["6"]["generator_order"]==6
    assert o["checks"]["representation_intertwiner_not_claimed"] is True
