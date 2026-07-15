"""Focused regression for the GAP-owned Pass 345 spectral-code retraction."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAP_WITNESS = ROOT / "analysis" / "w33_pass345_pass70_spectral_code_retraction.g"
GAP_CERTIFICATE = ROOT / "data" / "w33_pass345_pass70_spectral_code_retraction.json"
LEGACY_WITNESS = ROOT / "w33_pass70_trackB_qec.py"
LEGACY_CERTIFICATE = ROOT / "w33_pass70_trackB_qec.json"


def test_pass345_gap_retracts_the_spectral_code_reading() -> None:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 345"
    result = subprocess.run(
        [gap, "-q", str(GAP_WITNESS)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass345 status=PASS" in result.stdout

    cert = json.loads(GAP_CERTIFICATE.read_text(encoding="utf-8"))
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 12 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["multiplicity_sum"] == 360
    assert cert["distinguished_multiplicity"] == 9
    assert cert["largest_multiplicity"] == 250
    assert cert["literal_ceiling_ratio"] == 2
    assert cert["stabilizer_matrices_constructed"] is False
    assert cert["distance_computed"] is False
    assert cert["claimed_code"] is None


def test_legacy_track_b_agrees_with_the_gap_retraction() -> None:
    subprocess.run(
        [sys.executable, str(LEGACY_WITNESS)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    gap_cert = json.loads(GAP_CERTIFICATE.read_text(encoding="utf-8"))
    legacy = json.loads(LEGACY_CERTIFICATE.read_text(encoding="utf-8"))
    assert legacy["length_n"] == gap_cert["multiplicity_sum"]
    assert legacy["distinguished_multiplicity"] == gap_cert["distinguished_multiplicity"]
    assert legacy["largest_nonlogical_eigenspace"] == gap_cert["largest_multiplicity"]
    assert legacy["heuristic_ceil_ratio"] == gap_cert["literal_ceiling_ratio"]
    assert legacy["stabilizer_matrices_constructed"] is False
    assert legacy["distance_computed"] is False
    assert legacy["claimed_code"] is None
    assert legacy["audit_pass"] is True
