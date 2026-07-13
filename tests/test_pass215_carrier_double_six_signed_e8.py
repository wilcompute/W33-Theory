"""Focused regression for the GAP-owned Pass 215 carrier/E8 endpoint lift."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass215_carrier_double_six_signed_e8.g"
CERT = ROOT / "data" / "w33_pass215_carrier_double_six_signed_e8.json"


def run_gap() -> dict:
    subprocess.run(
        ["gap", "-q", str(SCRIPT.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        timeout=300,
    )
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_pass215_gap_certificate() -> None:
    data = run_gap()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())


def test_pass215_exact_fibres_and_sign_cover() -> None:
    data = json.loads(CERT.read_text(encoding="utf-8"))
    lift = data["carrier_lift"]
    assert (lift["sheets"], lift["local_axis_endpoints"], lift["axes"]) == (
        4320,
        240,
        120,
    )
    assert lift["endpoint_fibre"] == 18
    assert lift["axis_fibre"] == 36
    assert data["minimal_phase_sheet"]["cover"] == "C2 -> 240 endpoints -> 120 axes"
    assert data["minimal_phase_sheet"]["fixed_points"] == 0
    assert data["minimal_phase_sheet"]["centralizes_code_action"] is True


def test_pass215_keeps_the_two_we6_embeddings_separate() -> None:
    data = json.loads(CERT.read_text(encoding="utf-8"))
    ledger = data["embedding_ledger"]
    assert ledger["W33_code_embedding_endpoint_orbits"] == [240]
    assert ledger["W33_code_embedding_axis_orbits"] == [120]
    assert ledger["standard_E6_signed_root_orbits"] == [
        1,
        1,
        1,
        1,
        1,
        1,
        27,
        27,
        27,
        27,
        27,
        27,
        72,
    ]
    assert "not equivariant" in ledger["conclusion"]
