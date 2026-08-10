from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_pass3965_3972_topology_control_causal_density.py"
spec=importlib.util.spec_from_file_location("p3965",SCRIPT)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

@pytest.fixture(scope="session")
def frozen():
    return json.loads((ROOT/"data"/"PART_3965_3972_TOPOLOGY_CONTROL_CAUSAL_DENSITY_results.json").read_text(encoding="utf-8"))

@pytest.fixture(scope="session")
def quick(frozen):
    return m.quick_verify(frozen)

def test_semantic_certificate(frozen):
    assert m.canonical_json_sha(frozen)==frozen["semantic_sha256"]==m.SEMANTIC

def test_w33_srg():
    _,A=m.build_w33()
    m.verify_srg(A)

def test_weight_two_ledger(quick):
    assert quick["weight2"]==303810

def test_symmetry_orbits(quick):
    assert quick["group_order"]==25920
    assert quick["pair_orbits"]==[40,480,1080]

def test_minimum_port_certificate(quick):
    assert quick["port_ranks"]=={"5":279,"7":279,"101":279}

def test_photon_causal_density_and_router(frozen):
    p=frozen["passes"]
    assert p["3970_bonkers_photon_causal_density"]["serial_depth_bound"]=="N_serial <= 4 E L/(h c)=4 L/lambda"
    assert p["3972_bonkers_self_similar_causal_router"]["table"][3]["diameter"]==8
