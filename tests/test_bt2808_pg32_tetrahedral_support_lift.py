from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


core = load_module(
    ROOT / "analysis" / "bt2808_pg32_tetrahedral_support_lift.py",
    "bt2808_pg32_tetrahedral_support_lift",
)
freeze = load_module(
    ROOT / "analysis" / "bt2808_freeze.py",
    "bt2808_freeze",
)


def test_exact_certificate_passes_all_checks():
    certificate = core.build_certificate()
    assert certificate["check_count"] == 43
    assert all(certificate["checks"].values())


def test_support_lift_is_tomotope_profile():
    certificate = core.build_certificate()
    lift = certificate["support_lift"]
    assert lift["tomotope_f_vector"] == [4, 12, 16, 8]
    assert [row["fiber_size"] for row in lift["fiber_rows"]] == [
        1, 1, 2, 1, 2, 2, 4, 1, 2, 2, 4, 2, 4, 4, 8
    ]


def test_all_three_support_quotients_have_exact_split():
    certificate = core.build_certificate()
    quotient = certificate["equitable_quotients"]
    assert quotient["matching_count"] == 3
    for row in quotient["matching_results"]:
        assert row["quotient"]["equitable"]
        assert row["quotient"]["eigenvalues"] == {"12": 1, "2": 9, "-4": 5}
        assert row["quotient"]["residual_phase_eigenvalues"] == {
            "2": 15,
            "-4": 10,
        }
        assert row["quotient"]["quadratic_identity"]
        assert row["quotient"]["detailed_balance"]
        assert row["quotient"]["closed_formula_verified"]


def test_s4_d8_pairing_and_type_a_face_bridge():
    certificate = core.build_certificate()
    bridge = certificate["selector_bridge"]
    assert bridge["pairing_orbit_size"] == 3
    assert bridge["pairing_stabilizer_order"] == 8
    assert bridge["pairing_stabilizer_type"] == "D8"
    assert bridge["type_a_face_masks"] == ["0111", "1011", "1101", "1110"]
    assert bridge["face_pairing_chart_count"] == 12


def test_frozen_certificate_is_semantically_exact():
    computed = json.loads(json.dumps(freeze.compact_certificate(core.build_certificate())))
    frozen = json.loads(
        (
            ROOT
            / "data"
            / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"
        ).read_text(encoding="utf-8")
    )
    assert frozen == computed
