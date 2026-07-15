"""Focused regression for the GAP-owned Pass 343 CSS obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAP_WITNESS = ROOT / "analysis" / "w33_pass343_pass71_css_obstruction.g"
GAP_CERTIFICATE = ROOT / "data" / "w33_pass343_pass71_css_obstruction.json"
LEGACY_WITNESS = ROOT / "w33_pass71_trackD_css_matrices.py"
LEGACY_CERTIFICATE = ROOT / "w33_pass71_trackD_css_matrices.json"


def test_pass343_gap_refutes_the_pass71_css_pair() -> None:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 343"
    result = subprocess.run(
        [gap, "-q", str(GAP_WITNESS)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass343 status=PASS" in result.stdout

    cert = json.loads(GAP_CERTIFICATE.read_text(encoding="utf-8"))
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 12 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["matrix_identity"] == "H_X H_Z^T = A"
    assert cert["css_condition_satisfied"] is False
    assert cert["css_product_rank"] == 16
    assert cert["css_product_weight"] == 480


def test_legacy_track_d_agrees_with_the_gap_certificate() -> None:
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
    assert legacy["audit_pass"] is True
    assert legacy["css_condition_satisfied"] is False
    assert legacy["css_product_equals_adjacency"] is True
    assert legacy["css_product_rank"] == gap_cert["css_product_rank"]
    assert legacy["css_product_weight"] == gap_cert["css_product_weight"]
    assert legacy["claimed_code"] is None
