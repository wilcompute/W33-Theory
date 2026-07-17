"""Focused regression for the GAP-owned Pass 380 minimal scheduler lift."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
STRESS_FLAGS = [159, 83, 84, 22, 13, 144, 135, 134, 58, 63, 112, 113, 44, 37, 73, 180]
PHASE_WORD = ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 380")
def test_pass380_constructs_the_minimal_phase_lift_and_binding_boundary() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass380_minimal_scheduler_phase_lift.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass380 status=PASS" in result.stdout
    assert "lift=48 intersection=6 anchors=2" in result.stdout.replace("\n", "")

    certificate = json.loads(
        (ROOT / "data" / "w33_pass380_minimal_scheduler_phase_lift.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 14 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["scheduler"] == {
        "stress_flags": 16,
        "phase_trits": 3,
        "refined_labels": 48,
        "label": "(tomotope_flag, phase_trit)",
        "phase_word": PHASE_WORD,
    }
    assert certificate["canonical_full_bus_lift"] == {
        "formula": "iota(flag,phase)=flag+64*phase mod 192",
        "image_size": 48,
        "header_intersection_size": 6,
        "aligned_scheduler_flags": [112, 144],
        "aligned_header_cycles": [[16, 80, 144], [48, 112, 176]],
    }
    assert certificate["binding_count"] == {
        "all_bare_equivariant_bijections": "900657498850357248000",
        "after_two_oriented_anchors": "416971064282572800",
        "unanchored_orbits": 14,
    }
    assert certificate["search_signature"] == "48/6/2/14!3^14/minimal-phase-lift"


def test_pass380_provenance_is_the_live_bt1407_body_schedule() -> None:
    transaction = json.loads(
        (ROOT / "data" / "bt1407_microframe_transaction_composer.json").read_text(
            encoding="utf-8"
        )
    )
    body = transaction["body_ticks"]
    assert len(body) == 48
    assert [tick["frame_tick"] for tick in body] == list(range(48))
    assert [tick["edge_step"] for tick in body[0::3]] == list(range(16))
    assert [tick["tomotope_flag"] for tick in body[0::3]] == STRESS_FLAGS
    for offset in range(0, 48, 3):
        triple = body[offset : offset + 3]
        assert [tick["phase_trit"] for tick in triple] == [0, 1, 2]
        assert [tick["op"] for tick in triple] == PHASE_WORD
        assert len({tick["tomotope_flag"] for tick in triple}) == 1
        assert len({tick["q6_edge_index"] for tick in triple}) == 1


def test_pass380_result_is_indexed() -> None:
    synthesis = (ROOT / "PASS380_MINIMAL_SCHEDULER_PHASE_LIFT.md").read_text(
        encoding="utf-8"
    )
    assert "16-row header-orbit binding table" in synthesis
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `48/6/2/14!3^14/minimal-phase-lift` |" in index
