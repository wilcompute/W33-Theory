"""Focused regression for Pass 104's W33 axis/glue/E8 lift."""

from __future__ import annotations

import json
from pathlib import Path

import w33_pass123_axis_glue_e8_lift as pass104

ROOT = Path(__file__).resolve().parents[1]


def test_pass104_regenerates_complete_axis_root_lift() -> None:
    assert pass104.main() == 0
    data = json.loads(
        (ROOT / "w33_pass123_axis_glue_e8_lift.json").read_text(encoding="utf-8")
    )

    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["intrinsic_axis_map"]["axes"] == 120
    assert data["intrinsic_axis_map"]["axis_endpoints"] == 240
    assert data["intrinsic_axis_map"]["distinct_anisotropic_cosets"] == 120
    assert data["quadratic_isometry"]["quadratic_failures"] == 0
    assert data["quadratic_isometry"]["bilinear_failures"] == 0
    assert data["e8_lift"]["root_lines"] == 120
    assert data["e8_lift"]["signed_roots"] == 240
    assert len(data["axis_root_table"]) == 120


def test_pass104_axis_endpoints_are_opposite_weight_six_representatives() -> None:
    data = pass104.build_code_and_quotient()
    records = pass104.axis_glue_records(data)

    assert len(records) == 120
    assert len({record["quotient_coordinate"] for record in records}) == 120
    for record in records:
        first, second = record["endpoint_words"]
        assert first.bit_count() == second.bit_count() == 6
        assert first ^ second == data["neighborhood_words"][record["point"]]
        assert pass104.reduce_mod_basis(first, data["code_basis"]) == (
            pass104.reduce_mod_basis(second, data["code_basis"])
        )


def test_pass104_keeps_edge_root_no_go_boundary() -> None:
    data = json.loads(
        (ROOT / "w33_pass123_axis_glue_e8_lift.json").read_text(encoding="utf-8")
    )

    boundary = data["claim_boundary"]
    assert "does not identify the 240 global W33 edges with roots" in boundary
    assert "axis" in boundary
