from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3751_3768_GQ_VELDKAMP_AXIAL_LATTICE_MONSTER_results.json"
SOURCE = ROOT / "analysis" / "w33_pass3751_3768_gq_veldkamp_axial_lattice_monster.py"
LEDGER = ROOT / "data" / "PART_3751_3768_GQ_VELDKAMP_AXIAL_LATTICE_MONSTER_CLAIMS_LEDGER.json"
EXPECTED = "f401d08e08c1f5898d363e2e371bfffb9ec0227b18486de4e9a4c72109d47b0b"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_certificate_and_source_present():
    assert SOURCE.is_file()
    result = load(RESULT)
    assert result["status"] == "PASS_EXACT_EIGHT_FRONT_SOURCE_MONSTER_AND_ROOTLESS_LEECH_PENDING"
    assert result["semantic_sha256"] == EXPECTED
    assert all(result["checks"].values())


def test_gq_veldkamp_and_w33_closures():
    result = load(RESULT)
    assert result["gq_association_algebra"]["dual_gq_4_2"]["point_graph_srg"] == [45, 12, 3, 3]
    assert result["gq_association_algebra"]["terwilliger_at_vertex"]["dimension"] == 16
    assert result["veldkamp_triality_tower"]["line_type_census"] == {
        "3_singular": 45,
        "2_singular_1_nonsingular": 216,
        "1_singular_2_nonsingular": 270,
        "3_nonsingular": 120,
    }
    assert result["plane_ovoid_W33_bridge"]["graph_srg"] == [40, 12, 2, 4]
    assert result["plane_ovoid_W33_bridge"]["automorphism_orbits"] == [40, 160]


def test_axial_and_lattice_firewalls():
    result = load(RESULT)
    axial = result["gq24_axial_algebra"]
    assert axial["axis_spectrum"] == {"1": 1, "1/7": 14, "-1/3": 9}
    assert axial["multiplication_operator_algebra_dimension_mod_1000003"] == 576
    assert axial["derivation_dimension_over_Q"] == 0
    assert axial["miyamoto_Z2_grading"] is False
    lattice = result["lattice_symmetry_breaking"]
    assert lattice["wd4_obstruction"]["maximum_rank"] == 16
    assert lattice["c2_preserving_child"]["isometry_type"] == "E8^3"
    assert lattice["c2_preserving_child"]["surviving_U4_2_stabilizer_order"] == 2
    assert lattice["rootless_Leech_status"].startswith("PENDING")


def test_claims_ledger_remains_fail_closed():
    result = load(RESULT)
    ledger = load(LEDGER)
    assert ledger["semantic_sha256"] == EXPECTED
    assert result["monster_descent_front"]["status"] == "FAIL_CLOSED_MMgroup_WORDS_PENDING"
    joined = " ".join(ledger["fail_closed"]).lower()
    assert "no serialized mmgroup words" in joined
    assert "no rootless" in joined
    assert "no remote ci" in joined
