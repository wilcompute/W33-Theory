from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_latin288_w33_central_quotient_bridge import build_result  # noqa: E402


def test_latin_even_stabilizer_is_explicit_w33_288_quotient_model() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())

    latin = data["latin_stabilizers"]
    assert latin["full_stabilizer_order"] == 576
    assert latin["full_structure"] == "C2^4 semidirect (S3 x S3)"
    assert latin["full_center_order"] == 1
    assert latin["full_derived_order"] == 144
    assert latin["orientation_even_stabilizer_order"] == 288
    assert latin["orientation_even_structure"] == "C2^4 semidirect (S3 x C3)"
    assert latin["orientation_even_center_order"] == 1
    assert latin["orientation_even_derived_order"] == 48
    assert latin["orientation_even_element_order_census"] == {
        "1": 1,
        "2": 27,
        "3": 80,
        "4": 36,
        "6": 144,
    }

    common = data["common_288"]
    assert common["standard_model"] == "A4 wr C2 = (A4 x A4) semidirect C2"
    assert common["W33_model"] == "H576/Z(H576)"
    assert common["affine_group_order"] == 288
    assert common["linear_complement_orders"] == {"latin": 18, "wreath": 18}
    assert common["explicit_GL4_conjugator"] == [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 0],
    ]


def test_plus_quadratic_geometry_and_extraspecial_lift() -> None:
    data = build_result()
    q = data["plus_quadratic_geometry"]
    assert q["carrier"] == "N=C2^4=F2^2 tensor F2^2=M2(F2)"
    assert q["q_value_histogram"] == {"0": 10, "1": 6}
    assert q["nonzero_singular_points"] == 9
    assert q["nonsingular_points"] == 6
    assert q["generator_lines"] == 6
    assert q["ruling_preserving_group"] == "S3 x S3, order 36"
    assert q["full_orthogonal_group"] == "O^+(4,2) = (S3 x S3) : C2, order 72"

    extra = data["extraspecial_plus_lift"]
    assert extra["order"] == 32
    assert extra["center_order"] == 2
    assert extra["derived_order"] == 2
    assert extra["abelianization"] == "C2^4"
    assert extra["element_order_census"] == {"1": 1, "2": 19, "4": 12}
    assert extra["isomorphism_class"] == "2^{1+4}_+"


def test_crossed_576_completions_and_144_torsor_boundary() -> None:
    data = build_result()
    crossed = data["crossed_576_completions"]
    assert crossed["common_core"] == "B288 ~= A4 wr C2 ~= C2^4:(S3 x C3)"
    assert "split index-two" in crossed["Latin"]
    assert crossed["W33"].startswith("1 -> C2 -> H576")
    assert "nonsplit" in crossed["W33_extension_nonsplit"]

    small = data["latin_144_resolution"]
    assert small["main_class_size"] == 144
    assert small["orbit_size"] == 144
    assert small["regular"] is True
    assert small["regular_torsor_group"] == "S4 x S3"
    assert "order 36" in small["not_A4xA4_by_derived_order"]
    assert "order 16" in small["not_A4xA4_by_derived_order"]
