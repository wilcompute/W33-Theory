from __future__ import annotations

import json
from functools import lru_cache

from scripts.e6_hessian_tritangents import analyze_hessian_tritangent_split


@lru_cache(maxsize=1)
def _res():
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

    bad = json.load(open("artifacts/firewall_bad_triads_mapping.json", "r", encoding="utf-8"))[
        "bad_triangles_Schlafli_e6id"
    ]
    bad = {tuple(sorted(map(int, t))) for t in bad}
    assert fiber == bad


def test_e6_hessian_tritangents_ag23_incidence():
    res = _res()
    ag = res["ag23_checks"]

    assert ag["pairs_total"] == 36  # C(9,2)
    assert sorted(set(ag["direction_sizes"].values())) == [3]  # 4 directions x 3 parallels
    assert sorted(set(ag["u_point_line_degrees"].values())) == [4]  # 4 lines through each u
