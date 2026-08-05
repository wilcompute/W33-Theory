from __future__ import annotations

import importlib.util
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_pass3821_3828_maxcode_mesh_scheme_ovoid.py"
FROZEN = ROOT / "data" / "PART_3821_3828_MAXCODE_MESH_SCHEME_OVOID_results.json"

spec = importlib.util.spec_from_file_location("pass3821", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    return module.build_certificate()


def test_frozen_certificate_and_component_hashes() -> None:
    generated = certificate()
    frozen = json.loads(FROZEN.read_text())
    assert generated == frozen
    assert generated["semantic_sha256"] == "b141dd0f82e4a6b1ee62d1c57f0e92bdfc9f58d3b32515f9521a0175fdca88a1"
    import hashlib
    for name in ("maxcode", "mesh", "monster", "ovoid", "scheme"):
        path = ROOT / "data" / f"PART_3821_3828_COMPONENT_{name.upper()}.json"
        payload = json.loads(path.read_text())
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        assert hashlib.sha256(canonical.encode()).hexdigest() == generated["component_sha256"][name]


def test_eight_front_invariants() -> None:
    c = certificate()
    maxcode = c["maximal_code_extensions"]
    assert maxcode["complete_census"]["number_of_maximal_doubly_even_extensions"] == 240137905387279785868125
    assert maxcode["complete_census"]["u42d2_orbit_count_lower_bound"] == 4632289841575613440
    assert maxcode["maximal_extension"]["u42d2_stabilizer_order"] == 1

    mesh = c["exact_adjacent_multiport"]
    assert (mesh["exact_adjacent_givens_rotations"], mesh["adjacent_layers"]) == (418, 69)
    assert mesh["parameter_sha256"] == "5c933cc2e6d2484e97894f3ca1f71627214238e41a68cd59b7527993d2b06b6b"

    scheme = c["holonomy_association_scheme"]
    assert scheme["q_polynomial_orderings"] == []
    assert len(scheme["fusion_schemes"]) == 4
    assert (scheme["terwilliger_dimension_over_Q"], scheme["terwilliger_center_dimension_over_Q"]) == (79, 10)

    monster = c["monster_internal_standard_pairs"]
    assert monster["centralizer_orbits"] == [576, 576]
    assert monster["total_ordered_standard_pairs"] == 51840
    assert monster["generated_group_orders"] == [25920, 25920]

    ovoid = c["quadratic_parent_ovoid_fusion"]
    assert ovoid["ovoid_orbits"] == {"plane_ovoids": 40, "tripods": 160}
    assert ovoid["combined_264_object_orbital_coherent_configuration"]["orbital_rank"] == 48
    assert ovoid["objectwise_dictionary"]["checks"] == {"all_points": 40, "all_lines": 40, "all_flags": 160}
