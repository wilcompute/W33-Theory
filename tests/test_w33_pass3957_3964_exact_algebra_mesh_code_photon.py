from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis/w33_pass3957_3964_exact_algebra_mesh_code_photon.py"
FROZEN = ROOT / "data/PART_3957_3964_EXACT_ALGEBRA_MESH_CODE_PHOTON_results.json"

def load_module():
    spec = importlib.util.spec_from_file_location("pass3957", SOURCE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_frozen_certificate_reproduces():
    module = load_module()
    generated = json.loads(json.dumps(module.build_certificate(ROOT), sort_keys=True))
    assert generated == json.loads(FROZEN.read_text(encoding="utf-8"))

def test_key_exact_boundaries():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    mesh = frozen["exact_adjacent_mesh"]
    assert (mesh["rotations"], mesh["skipped_exact_zeros"], mesh["layers"]) == (398, 232, 69)
    assert mesh["offdiagonal_nonzeros"] == 0
    assert mesh["max_c2_denominator"] == 441
    code = frozen["maximal_code_stratum_57"]
    assert code["weight4_count"] == 57
    assert code["weight4_intersection2_graph"]["component_sizes"] == [45, 6, 6]
    rank48 = frozen["rank48_coherent_algebra"]
    assert rank48["centralizer_dimension"] == 48
    assert rank48["wedderburn"] == "Q^2 + M2(Q)^3 + M3(Q) + M5(Q)"
    assert frozen["monster_gate"]["status"].startswith("PENDING")
    assert frozen["photon_node_capacity_model"]["quantum_speed_limit"]["overload_factor"] == 10
