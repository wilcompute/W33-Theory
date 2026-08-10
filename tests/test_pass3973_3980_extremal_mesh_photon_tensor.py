from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3973_3980_extremal_mesh_photon_tensor.py"
FROZEN = ROOT / "data" / "PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_results.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass3973_3980", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quick_exact_packet():
    module = load_module()
    result = module.build_result(False)
    assert result["status"] == module.STATUS
    assert result["pass3973_code57_geometry"]["component_identifications"] == [
        "T(10)=L(K10)", "T(4)=L(K4)", "T(4)=L(K4)"
    ]
    assert result["pass3973_enumerator_rigidity"]["t57_evaluation"]["B18"] == 233472
    mesh = result["pass3974_mesh_radius_one"]
    assert mesh["base"] == {"rotations": 398, "exact_zeros": 232, "layers": 69}
    assert mesh["minimum_rotations"] == 398
    assert result["pass3976_rank48_tensor"]["dimension"] == 48
    assert result["pass3976_rank48_tensor"]["nonzero_structure_constants"] == 178
    assert result["pass3977_monster_gate"]["promoted_embedding"] is False


def test_frozen_full_transposition_audit():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    mesh = frozen["pass3974_mesh_radius_one"]
    assert mesh["tested"] == 630
    assert sum(mesh["rotation_histogram"].values()) == 630
    assert mesh["minimum_rotations"] == 398
    assert mesh["ties_at_398"] == 22
    assert mesh["all_layers"] == 69
    assert mesh["sha256"] == "d0e4b57c47e8db57def844d9d9da63b3e7cda0652b05473fcebc5884fbd8d80f"
    assert frozen["semantic_sha256"] == "769f2f1b29e832050fbf148f38ab64acd992766d5dc758a525b3f97e6e77d44e"
