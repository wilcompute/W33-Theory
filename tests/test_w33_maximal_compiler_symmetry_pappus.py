from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_maximal_compiler_symmetry_pappus.py"
DATA = ROOT / "data/w33_maximal_compiler_symmetry_pappus.json"


def load():
    spec = importlib.util.spec_from_file_location("compiler_pappus", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay_matches_frozen_certificate():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_maximal_safe_symmetry_and_pappus_controller():
    out = json.loads(DATA.read_text())
    assert out["restriction_criterion"]["maximal_safe_subgroup_order"] == 9
    assert out["subgroup_census"] == {
        "order3_total": 40,
        "order3_safe": 39,
        "order3_unsafe": 1,
        "order9_total": 49,
        "order9_safe": 36,
        "order9_containing_derived": 13,
        "order27_maximal_total": 13,
        "order27_safe": 0,
    }
    geom = out["safe_plane_geometry"]
    assert geom["count"] == 36
    assert geom["center_sheet_sizes"] == [12, 12, 12]
    assert geom["fixed_center_automorphism_group_order"] == 216
    assert geom["fixed_center_automorphism_orbit_sizes"] == [12, 12, 12]
    assert geom["compiler_plane_order3_intersection_graph_degree"] == 17

    assert out["hesse_duality"]["all_12_lines_recovered"] is True

    pappus = out["pappus_controller"]
    assert pappus["noncentral_C3_points"] == 36
    assert pappus["maximal_safe_planes"] == 36
    assert pappus["connected_components"] == 4
    assert pappus["component_sizes"] == [18, 18, 18, 18]
    assert pappus["all_components_isomorphic_to_Pappus_graph"] is True

    firewall = out["ownership_and_firewalls"]["double_six_firewall"]
    assert "17-regular" in firewall
    assert "SRG(36,20,10,12)" in firewall
