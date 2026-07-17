"""Focused regression for the GAP-owned Pass 385 orbit-anchor obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
CERTIFICATE = (
    ROOT / "data" / "w33_pass385_header_stress_orbit_anchor_obstruction.json"
)


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 385")
def test_pass385_gap_proves_the_header_stress_orbit_anchor_obstruction() -> None:
    result = subprocess.run(
        [
            GAP,
            "-q",
            str(
                ROOT
                / "analysis"
                / "w33_pass385_header_stress_orbit_anchor_obstruction.g"
            ),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    stdout = result.stdout.replace("\n", "")
    assert "Pass385 status=PASS checks=31" in stdout
    assert (
        "header_aut=C2xD8 header_orbits=8+8 "
        "stress_stabilizers=1/1 anchors=cross"
    ) in stdout

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 31 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["search_signature"] == (
        "48/16/8/8/16/96/1/46080/1/2/orbit-anchor"
    )


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 385")
def test_pass385_classifies_both_intrinsic_carriers_exactly() -> None:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["header_quotient"] == {
        "toggle_events": 360,
        "flags": 48,
        "c3_cycles": 16,
        "cycle_representatives": [
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
        ],
        "directed_q3_toggles": 24,
        "class_size_profile": {"1": 8, "2": 8},
        "event_fiber_profile": {"5": 8, "10": 8},
        "named_axis_profile": [8, 4, 4],
        "ambient_aut_q3_order": 48,
        "partition_preserver_order": 16,
        "induced_group": "C2 x D8",
        "induced_orbits": [8, 8],
        "point_stabilizer_order": 2,
    }
    assert certificate["stress_path"] == {
        "flags": [159, 83, 84, 22, 13, 144, 135, 134, 58, 63, 112, 113, 44, 37, 73, 180],
        "q6_edges": 16,
        "vertices": 17,
        "abstract_path_aut": "C2",
        "metadata_aut_order": 1,
        "bt1371_group_order": 96,
        "bt1371_orbit_profile": [8, 8],
        "setwise_stabilizer_in_bt1371_group": 1,
        "full_q6_aut_order": 46080,
        "setwise_stabilizer_in_full_q6": 1,
        "edge_kind_profile": {"packet": 6, "connector": 10},
        "direction_profile": [2, 4, 3, 2, 2, 3],
    }


def test_pass385_reads_the_live_bt1371_and_bt1407_tables() -> None:
    address_table = json.loads(
        (
            ROOT / "data" / "bt1371_q6_tomotope_explicit_orbit_address_table.json"
        ).read_text(encoding="utf-8")
    )["address_table"]
    body = json.loads(
        (ROOT / "data" / "bt1407_microframe_transaction_composer.json").read_text(
            encoding="utf-8"
        )
    )["body_ticks"]

    stress = body[0::3]
    assert len(body) == 48
    assert [row["edge_step"] for row in stress] == list(range(16))
    assert [row["tomotope_flag"] for row in stress] == [
        159,
        83,
        84,
        22,
        13,
        144,
        135,
        134,
        58,
        63,
        112,
        113,
        44,
        37,
        73,
        180,
    ]
    assert [row["tomotope_flag"] for row in address_table] == list(range(192))
    for row in stress:
        address = address_table[row["tomotope_flag"]]
        assert address["q6_edge_index"] == row["q6_edge_index"]
        assert address["q6_direction"] == row["q6_direction"]
        assert {address["q6_endpoint_a"], address["q6_endpoint_b"]} == {
            row["source"],
            row["target"],
        }


def test_pass385_pins_the_anchor_cross_and_scopes_the_no_go() -> None:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["anchors"] == [
        {
            "scheduler_flag": 144,
            "header_cycle_rep": 16,
            "header_cycle": [16, 80, 144],
            "header_aut_orbit": 0,
            "bt1371_orbit": 0,
        },
        {
            "scheduler_flag": 112,
            "header_cycle_rep": 48,
            "header_cycle": [48, 112, 176],
            "header_aut_orbit": 0,
            "bt1371_orbit": 1,
        },
    ]
    assert certificate["binding_space"] == {
        "partition_respecting_cycle_bijections": "3251404800",
        "with_independent_c3_phase_offsets": "139962315283660800",
        "both_canonical_anchors_compatible": False,
    }
    assert "no orbit-respecting binding retains both anchors" in certificate[
        "obstruction"
    ]
    assert "necessary ABI input" in certificate["conclusion"]
    assert "finite control-plane obstruction" in certificate["conclusion"]
    assert "not a Q6 hardware or oscillator no-go" in certificate["conclusion"]


def test_pass385_synthesis_states_the_precise_boundary() -> None:
    synthesis = (
        ROOT / "PASS385_HEADER_STRESS_ORBIT_ANCHOR_OBSTRUCTION.md"
    ).read_text(encoding="utf-8")
    assert "C_2\\times D_8" in synthesis
    assert "3,251,404,800" in synthesis
    assert "139,962,315,283,660,800" in synthesis
    assert "necessary ABI input" in synthesis
    assert "does not say" in synthesis
    assert "48/16/8/8/16/96/1/46080/1/2/orbit-anchor" in synthesis
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `48/16/8/8/16/96/1/46080/1/2/orbit-anchor` |" in index
    assert "analysis/w33_pass385_header_stress_orbit_anchor_obstruction.g" in index
