"""Focused regression for the GAP-owned Pass 384 Q6/Q3 fold obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")

PROFILE_FOLDS = [
    [1, 1, 2, 1, 3, 2],
    [1, 1, 3, 1, 2, 3],
    [1, 2, 1, 1, 3, 2],
    [1, 2, 2, 1, 3, 1],
    [1, 3, 1, 1, 2, 3],
    [1, 3, 3, 1, 2, 1],
]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 384")
def test_pass384_classifies_strict_q6_to_binary_q3_coordinate_folds() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass384_q6_q3_fold_obstruction.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass384 status=PASS" in result.stdout
    assert (
        "strict=540 profile_folds=6 exact=0 best=22of48 relation=S6"
        in result.stdout.replace("\n", "")
    )

    certificate = json.loads(
        (ROOT / "data" / "w33_pass384_q6_q3_fold_obstruction.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 19 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["map_counts"] == {
        "all_rank_three_linear_maps": 234360,
        "strict_one_bit_surjective_coordinate_folds": 540,
        "strict_affine_coordinate_folds": 4320,
        "all_affine_epimorphisms": 1874880,
    }
    assert certificate["strict_fold_orbits"] == [
        {
            "multiplicities": [1, 1, 4],
            "representative": [1, 1, 1, 1, 2, 3],
            "count": 90,
            "full_action_orbit": 90,
            "stabilizer_order": 48,
        },
        {
            "multiplicities": [1, 2, 3],
            "representative": [1, 1, 1, 2, 2, 3],
            "count": 360,
            "full_action_orbit": 360,
            "stabilizer_order": 12,
        },
        {
            "multiplicities": [2, 2, 2],
            "representative": [1, 1, 2, 2, 3, 3],
            "count": 90,
            "full_action_orbit": 90,
            "stabilizer_order": 48,
        },
    ]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 384")
def test_pass384_fences_the_live_header_binding_claim_precisely() -> None:
    certificate = json.loads(
        (ROOT / "data" / "w33_pass384_q6_q3_fold_obstruction.json").read_text(
            encoding="utf-8"
        )
    )
    profile = certificate["stress_profile"]
    assert profile["walk_axis_usage"] == [3, 2, 2, 3, 4, 2]
    assert profile["header_axis_cycle_profile"] == [8, 4, 4]
    assert profile["nominal_relabelling_order"] == 24
    assert profile["induced_relabelling_order"] == 12
    assert profile["induced_stabilizer_order"] == 2
    assert profile["nominal_stabilizer_order"] == 4
    assert [entry["fold"] for entry in profile["folds"]] == PROFILE_FOLDS
    assert [entry["header_axis_matches"] for entry in profile["folds"]] == [
        21,
        21,
        15,
        22,
        18,
        21,
    ]
    assert certificate["anchor_test"] == {
        "scheduler_flags": [112, 144],
        "walk_coordinates": [1, 4],
        "header_axis": 1,
        "compatible_profile_folds": 6,
        "conclusion": "The two natural anchors do not select a fold.",
    }
    obstruction = certificate["live_table_obstruction"]
    assert obstruction["direction_by_header_axis"] == [
        [6, 2, 4],
        [3, 1, 1],
        [6, 1, 1],
        [1, 4, 2],
        [3, 0, 1],
        [5, 4, 3],
    ]
    assert obstruction["exact_strict_intertwiners"] == 0
    assert obstruction["best_all_fold_match"] == 25
    assert obstruction["best_all_fold_count"] == 4
    assert obstruction["best_profile_fold"] == [1, 2, 2, 1, 3, 1]
    assert obstruction["best_profile_fold_match"] == 22
    assert obstruction["best_profile_fold_count"] == 1
    assert obstruction["diagnostic_only"] is True
    assert certificate["header_c3_direction_relation"] == {
        "group": "S6",
        "order": 720,
        "orbits": [[1, 2, 3, 4, 5, 6]],
        "all_colorings_invariant": 3,
        "strict_surjective_invariant": 0,
        "stress_profile_invariant": 0,
    }
    assert certificate["binding_boundary"] == {
        "axis_respecting_torsor": "S8 x S4 x S4 with independent C3 phase offsets",
        "unanchored_count": "999730823454720",
        "after_two_oriented_anchors": "1983592903680",
        "six_labeled_folds_after_anchors": "11901557422080",
        "unrestricted_to_axis_ratio": 900900,
    }
    assert "not a canonical header-to-scheduler binding" in certificate["conclusion"]
    assert "explicit sixteen-row binding table" in certificate["conclusion"]
    assert certificate["search_signature"] == (
        "234360/540/90+360+90/6/22of48/0exact/S6-direction"
    )


def test_pass384_uses_the_live_bt1371_and_bt1407_inputs() -> None:
    table = json.loads(
        (
            ROOT / "data" / "bt1371_q6_tomotope_explicit_orbit_address_table.json"
        ).read_text(encoding="utf-8")
    )["address_table"]
    body = json.loads(
        (ROOT / "data" / "bt1407_microframe_transaction_composer.json").read_text(
            encoding="utf-8"
        )
    )["body_ticks"]

    assert [row["tomotope_flag"] for row in table] == list(range(192))
    assert len(body) == 48
    assert [row["q6_direction"] for row in body[0::3]] == [
        1,
        4,
        3,
        5,
        1,
        2,
        0,
        1,
        5,
        2,
        5,
        4,
        3,
        1,
        0,
        2,
    ]
    assert [row["tomotope_flag"] for row in body[0::3]][5] == 144
    assert [row["tomotope_flag"] for row in body[0::3]][10] == 112


def test_pass384_synthesis_keeps_the_no_go_scoped() -> None:
    synthesis = (ROOT / "PASS384_Q6_Q3_FOLD_OBSTRUCTION.md").read_text(
        encoding="utf-8"
    )
    assert "strict coordinate fold" in synthesis
    assert "not canonical" in synthesis
    assert "does not rule out" in synthesis
    assert "234360/540/90+360+90/6/22of48/0exact/S6-direction" in synthesis
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `234360/540/90+360+90/6/22of48/0exact/S6-direction` |" in index
    assert "analysis/w33_pass384_q6_q3_fold_obstruction.g" in index
