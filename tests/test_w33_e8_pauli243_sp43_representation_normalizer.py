from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_e8_pauli243_sp43_representation_normalizer.py"
    s=importlib.util.spec_from_file_location("e8sp43",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_e8_pauli243_sp43_representation_normalizer():
    o=load().main(False)
    assert o["status"]=="PASS_E8_DERIVED_PAULI243_REPRESENTATION_NORMALIZED_BY_FULL_SP43_CLIFFORD"
    assert o["compressed_generators"]["count"]==4
    assert o["compressed_generators"]["generated_Sp43_order"]==51840
    assert o["unitary_lift"]["total_conjugation_checks"]==324
    assert o["normalizer"]["Pauli_order"]==243
    assert o["normalizer"]["Sp43_order"]==51840
    assert o["E8_firewall"]["all_clifford_lifts_proved_inside_compact_E8"] is False
    assert o["E8_firewall"]["N_E8_of_this_specific_Pauli243_identified"] is False
    assert all(o["checks"].values())
