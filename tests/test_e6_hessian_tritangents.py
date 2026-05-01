from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.e6_hessian_tritangents import analyze_hessian_tritangent_split

ROOT = Path(__file__).resolve().parents[1]
FIREWALL_BAD_TRIADS = ROOT / "artifacts" / "firewall_bad_triads_mapping.json"
SAGE_TRANSPORT = (
    ROOT / "artifacts" / "sage_h27_to_schlafli_effective_triads_conjugacy.json"
)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _ensure_firewall_bad_triads() -> None:
    if FIREWALL_BAD_TRIADS.exists():
        return

    build_channels = _load_module(
        ROOT / "tools" / "build_channel_dictionary_from_we6_generators.py",
        "build_channel_dictionary_from_we6_generators_for_hessian_test",
    )
    build_channels.main()

    selection_rules = _load_module(
        ROOT / "tools" / "generate_selection_rules_report.py",
        "generate_selection_rules_report_for_hessian_test",
    )
    selection_rules.main()

    map_firewall = _load_module(
        ROOT / "tools" / "map_firewall_bad_triangles_to_cubic_triads.py",
        "map_firewall_bad_triangles_to_cubic_triads_for_hessian_test",
    )
    map_firewall.main()


@lru_cache(maxsize=1)
def _res():
    if not SAGE_TRANSPORT.exists():
        pytest.skip(
            "Sage H27-to-Schlafli transport certificate is absent; "
            "run sage tools/sage_conjugacy_h27_to_schlafli_effective_triads.sage "
            "to materialize this ignored artifact"
        )
    _ensure_firewall_bad_triads()
    return analyze_hessian_tritangent_split()


def test_e6_hessian_tritangents_counts():
    res = _res()
    c = res["counts"]
    assert c["points_total"] == 27
    assert c["triads_total"] == 45
    assert c["fiber_triads"] == 9
    assert c["affine_triads"] == 36
    assert c["u_points"] == 9
    assert c["u_lines"] == 12
    assert c["u_line_directions"] == 4
    assert res["reconstruction"]["fiber_matches"] is True
    assert res["reconstruction"]["affine_matches"] is True
    assert res["reconstruction"]["affine_formula_asserted"] is False
    assert res["hessian_group"]["order"] == 648
    assert res["hessian_group"]["transitive"] is True
    assert res["hessian_group"]["triads_invariant"] is True
    assert res["hessian_group"]["fiber_triads_invariant"] is True
    assert res["hessian_group"]["affine_triads_invariant"] is True
    assert res["hessian_group"]["point_stabilizer_order"] == 24
    assert res["hessian_group"]["transported_from_w33"] is True
    assert res["affine_group"]["order"] == 1296
    assert res["affine_group"]["transitive"] is True
    assert res["affine_group"]["triads_invariant"] is True
    assert res["affine_group"]["fiber_triads_invariant"] is True
    assert res["affine_group"]["affine_triads_invariant"] is True
    assert res["affine_group"]["point_stabilizer_order"] == 48
    assert res["affine_group"]["normal_27_subgroup_structure"] == "(C3 x C3) : C3"
    assert res["affine_group"]["projective_subgroup_order"] == 648
    assert res["affine_group"]["projective_subgroup_index"] == 2
    assert res["affine_group"]["transported_from_w33"] is True
    assert res["affine_group"]["order"] == 2 * res["hessian_group"]["order"]


def test_e6_hessian_tritangents_firewall_bad9_matches_fibers():
    res = _res()
    fiber = {tuple(sorted(t)) for t in res["fiber_triads"]}

    data = json.loads(FIREWALL_BAD_TRIADS.read_text(encoding="utf-8"))
    bad = data["bad_triangles_Schlafli_e6id"]
    bad = {tuple(sorted(map(int, t))) for t in bad}
    assert fiber == bad


def test_e6_hessian_tritangents_ag23_incidence():
    res = _res()
    ag = res["ag23_checks"]

    assert ag["pairs_total"] == 36  # C(9,2)
    assert sorted(set(ag["direction_sizes"].values())) == [
        3
    ]  # 4 directions x 3 parallels
    assert sorted(set(ag["u_point_line_degrees"].values())) == [
        4
    ]  # 4 lines through each u
