"""Focused regression for the GAP-owned Pass 378 C3 factorization obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
STRESS_FLAGS = [159, 83, 84, 22, 13, 144, 135, 134, 58, 63, 112, 113, 44, 37, 73, 180]


def _scheduler_stress_load_flags() -> list[int]:
    scheduler = json.loads(
        (ROOT / "data" / "bt1406_tomotope_body_edge_pulse_scheduler.json").read_text(
            encoding="utf-8"
        )
    )
    stress = next(
        schedule
        for schedule in scheduler["schedules"]
        if schedule["program"] == "six_digit_stress"
    )
    return [
        pulse["tomotope_flag"]
        for pulse in stress["pulses"]
        if pulse["pulse_op"] == "LOAD_FLAG"
    ]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 378")
def test_pass378_constructs_the_header_scheduler_c3_obstruction() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass378_header_scheduler_c3_obstruction.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass378 status=PASS" in result.stdout

    certificate = json.loads(
        (ROOT / "data" / "w33_pass378_header_scheduler_c3_obstruction.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 13 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["header_clock"] == {
        "toggle_events": 360,
        "flags": 48,
        "free_c3_orbits": 16,
        "shift": "flag -> flag+64 mod 192",
    }
    assert certificate["scheduler"]["stress_flags"] == STRESS_FLAGS
    assert certificate["comparison"] == {
        "bare_c3_set_type": "16*C3",
        "equivariant_bijection_count": "900657498850357248000",
        "header_scheduler_flag_intersection": [112, 144],
        "header_cycle_stress_hit_profile": {"0": 14, "1": 2},
    }
    assert "no C3-equivariant map" in certificate["obstruction"]


def test_pass378_stress_flag_provenance_matches_the_live_bt1406_scheduler() -> None:
    assert _scheduler_stress_load_flags() == STRESS_FLAGS
