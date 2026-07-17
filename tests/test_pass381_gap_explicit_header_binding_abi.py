"""Focused regression for the GAP-owned explicit Pass 381 compiler ABI."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
PHASE_WORD = ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 381")
def test_pass381_compiles_the_explicit_reviewed_binding_abi() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass381_explicit_header_binding_abi.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass381 status=PASS" in result.stdout
    assert "rows=16 trace=48 anchors=2 external=14" in result.stdout.replace("\n", "")

    certificate = json.loads(
        (ROOT / "data" / "w33_pass381_explicit_header_binding_abi.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 14 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["summary"] == {
        "scheduler_pulses": 48,
        "header_flags": 48,
        "canonical_anchors": 2,
        "external_rows": 14,
        "header_clock": "flag -> flag+64 mod 192",
    }
    assert certificate["search_signature"] == "16/48/2+14/external-binding-abi"


def test_pass381_configuration_is_explicit_and_preserves_only_the_known_anchors() -> None:
    config = json.loads(
        (ROOT / "analysis" / "w33_pass381_header_orbit_binding_abi.json").read_text(
            encoding="utf-8"
        )
    )
    rows = config["rows"]
    assert config["kind"] == "explicit reviewed compiler input"
    assert len(rows) == 16
    assert [row["edge_step"] for row in rows] == list(range(16))
    assert len({row["tomotope_flag"] for row in rows}) == 16
    assert len({row["header_cycle_rep"] for row in rows}) == 16
    anchors = [row for row in rows if row["binding_source"] == "canonical_full_bus_anchor"]
    assert anchors == [
        {
            "edge_step": 5,
            "tomotope_flag": 144,
            "header_cycle_rep": 16,
            "phase_offset": 2,
            "binding_source": "canonical_full_bus_anchor",
        },
        {
            "edge_step": 10,
            "tomotope_flag": 112,
            "header_cycle_rep": 48,
            "phase_offset": 1,
            "binding_source": "canonical_full_bus_anchor",
        },
    ]
    assert sum(row["binding_source"] == "reviewed_external_binding" for row in rows) == 14


def test_pass381_trace_is_a_bijective_c3_compiler_trace_for_the_live_body() -> None:
    certificate = json.loads(
        (ROOT / "data" / "w33_pass381_explicit_header_binding_abi.json").read_text(
            encoding="utf-8"
        )
    )
    transaction = json.loads(
        (ROOT / "data" / "bt1407_microframe_transaction_composer.json").read_text(
            encoding="utf-8"
        )
    )
    trace = certificate["compiled_trace"]
    body = transaction["body_ticks"]
    assert len(trace) == len(body) == 48
    assert {row["header_flag"] for row in trace} == {
        1,
        3,
        5,
        10,
        12,
        16,
        18,
        24,
        27,
        33,
        35,
        39,
        41,
        46,
        48,
        50,
        65,
        67,
        69,
        74,
        76,
        80,
        82,
        88,
        91,
        97,
        99,
        103,
        105,
        110,
        112,
        114,
        129,
        131,
        133,
        138,
        140,
        144,
        146,
        152,
        155,
        161,
        163,
        167,
        169,
        174,
        176,
        178,
    }
    for position, (row, tick) in enumerate(zip(trace, body)):
        assert row["inverse_position"] == position
        assert row["edge_step"] == tick["edge_step"]
        assert row["tomotope_flag"] == tick["tomotope_flag"]
        assert row["phase_trit"] == tick["phase_trit"]
        assert row["op"] == tick["op"]
    for start in range(0, 48, 3):
        triple = trace[start : start + 3]
        assert [row["phase_trit"] for row in triple] == [0, 1, 2]
        assert [row["op"] for row in triple] == PHASE_WORD
        assert triple[1]["header_flag"] == (triple[0]["header_flag"] + 64) % 192
        assert triple[2]["header_flag"] == (triple[1]["header_flag"] + 64) % 192
    assert [row["header_flag"] for row in trace[15:18]] == [144, 16, 80]
    assert [row["header_flag"] for row in trace[30:33]] == [112, 176, 48]


def test_pass381_result_is_indexed() -> None:
    synthesis = (ROOT / "PASS381_EXPLICIT_HEADER_BINDING_ABI.md").read_text(
        encoding="utf-8"
    )
    assert "reviewed compiler input" in synthesis
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `16/48/2+14/external-binding-abi` |" in index
