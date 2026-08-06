from __future__ import annotations
import base64
import hashlib
import importlib.util
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "data/PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_manifest.json").read_text(encoding="utf-8"))

def unpack(paths, compressed_sha, json_sha):
    encoded = "".join((ROOT / path).read_text(encoding="ascii").strip() for path in paths)
    compressed = base64.b64decode(encoded, validate=True)
    assert hashlib.sha256(compressed).hexdigest() == compressed_sha
    raw = zlib.decompress(compressed)
    assert hashlib.sha256(raw).hexdigest() == json_sha
    return json.loads(raw)

def certificate():
    return unpack(MANIFEST["certificate"]["parts"], MANIFEST["certificate"]["compressed_sha256"], MANIFEST["certificate"]["json_sha256"])

def test_extremal_code_and_mesh():
    frozen = certificate()
    code = frozen["pass3973_extremal_A4_57"]
    assert code["candidate_orbits"] == [135, 810]
    assert code["orbit_maxima"] == [15, 54]
    assert code["global_maximum_A4"] == 57
    assert code["stabilizer_order"] == 192
    assert code["weight4_intersection_graph"]["component_sizes"] == [45, 6, 6]
    mesh = frozen["pass3974_active_mixer_compiler"]
    assert mesh["active_mixer_optimized"]["active_mixers"] == 296
    assert mesh["active_mixer_optimized"]["signed_swaps"] == 105
    assert mesh["fixed_order_cut_rank_lower_bound"]["sum"] == 253

def test_tensor_photon_monster_and_semantic_boundary():
    frozen = certificate()
    tensor = unpack([MANIFEST["rank48_tensor"]["path"]], MANIFEST["rank48_tensor"]["compressed_sha256"], MANIFEST["rank48_tensor"]["json_sha256"])
    assert len(tensor["relation_metadata"]) == 48
    assert len(tensor["tensor_entries"]) == 904
    assert tensor["tensor_sha256"] == frozen["pass3976_rank48_literal_tensor"]["tensor_sha256"]
    assert frozen["pass3975_photon_competing_model_experiment"]["three_axis_protocol"]["W33_spectral_sweep"]["laplacian_eigenvalues"] == [0,10,16]
    assert frozen["pass3977_monster_execution_gate"]["status"].startswith("PENDING")
    spec = importlib.util.spec_from_file_location("pass3973", ROOT / "analysis/w33_pass3973_3980_extremal_mesh_photon_tensor_monster.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.canonical_sha(frozen) == MANIFEST["semantic_sha256"]
