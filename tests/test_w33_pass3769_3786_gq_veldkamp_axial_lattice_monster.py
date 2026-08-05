from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3769_3786_GQ_VELDKAMP_AXIAL_LATTICE_MONSTER_results.json"
SOURCE = ROOT / "analysis" / "w33_pass3769_3786_gq_veldkamp_axial_lattice_monster.py"
EXPECTED = "8d3f383e362f30e58d8c482f48e2ac2b77414922366ba8053633859d6206313a"


def result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_collision_safe_certificate():
    r = result()
    assert SOURCE.is_file()
    assert r["schema"] == "w33.pass3769_3786.gq_veldkamp_axial_lattice_monster.v1"
    assert r["semantic_sha256"] == EXPECTED
    assert all(r["checks"].values())


def test_gq_veldkamp_w33_and_axial_closures():
    r = result()
    assert r["gq_association_algebra"]["dual_gq_4_2"]["point_graph_srg"] == [45, 12, 3, 3]
    assert r["gq_association_algebra"]["terwilliger_at_vertex"]["dimension"] == 16
    assert r["veldkamp_triality_tower"]["line_type_census"] == {
        "3_singular": 45,
        "2_singular_1_nonsingular": 216,
        "1_singular_2_nonsingular": 270,
        "3_nonsingular": 120,
    }
    assert r["plane_ovoid_W33_bridge"]["graph_srg"] == [40, 12, 2, 4]
    assert r["gq24_axial_algebra"]["axis_spectrum"] == {"1": 1, "1/7": 14, "-1/3": 9}
    assert r["gq24_axial_algebra"]["multiplication_operator_algebra_dimension_mod_1000003"] == 576
    assert r["gq24_axial_algebra"]["derivation_dimension_over_Q"] == 0


def test_lattice_and_embedding_boundaries():
    r = result()
    lattice = r["lattice_symmetry_breaking"]
    assert lattice["wd4_obstruction"]["maximum_rank"] == 16
    assert lattice["c2_preserving_child"]["isometry_type"] == "E8^3"
    assert lattice["c2_preserving_child"]["surviving_U4_2_stabilizer_order"] == 2
    assert lattice["rootless_Leech_status"].startswith("PENDING")
    assert r["monster_descent_front"]["status"] == "FAIL_CLOSED_MMgroup_WORDS_PENDING"
