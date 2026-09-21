from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_physical_fi_factor_routing_e6_a2.py"
def load():
    spec=importlib.util.spec_from_file_location("routing",SRC);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def test_physical_fi_factor_routing():
    out=load().main(False)
    assert out["status"]=="PASS_PHYSICAL_FI_FACTOR_ROUTING"
    r=out["exact_set_relations"]
    assert all(r.values())
    assert out["counts"]["external_A2_roots"]==6
    assert out["counts"]["physical_gauge_A4_roots"]==20
