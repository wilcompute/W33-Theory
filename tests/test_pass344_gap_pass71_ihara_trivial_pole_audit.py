"""Focused regression for the GAP-owned Pass 344 Ihara classification audit."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAP_WITNESS = ROOT / "analysis" / "w33_pass344_pass71_ihara_trivial_pole_audit.g"
GAP_CERTIFICATE = ROOT / "data" / "w33_pass344_pass71_ihara_trivial_pole_audit.json"
LEGACY_WITNESS = ROOT / "w33_pass71_trackE_ihara_zeta.py"
LEGACY_CERTIFICATE = ROOT / "w33_pass71_trackE_ihara_zeta_poles.json"


def test_pass344_gap_separates_perron_and_nontrivial_poles() -> None:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 344"
    result = subprocess.run(
        [gap, "-q", str(GAP_WITNESS)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass344 status=PASS" in result.stdout

    cert = json.loads(GAP_CERTIFICATE.read_text(encoding="utf-8"))
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 14 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["perron_trivial_poles"] == ["1", "1/11"]
    assert cert["nontrivial_discriminants"] == [-40, -28]
    assert cert["nontrivial_root_modulus_squared"] == "1/11"
    assert cert["nontrivial_root_count"] == 78
    assert cert["vertex_factor_root_count"] == 80
    assert cert["graph_rh_satisfied"] is True


def test_legacy_track_e_agrees_with_the_gap_certificate() -> None:
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
    assert legacy["pole_classification_audit_pass"] is True
    assert legacy["perron_trivial_poles"] == [1.0, 1.0 / 11.0]
    assert legacy["nontrivial_vertex_factor_root_count"] == gap_cert["nontrivial_root_count"]
    assert abs(legacy["nontrivial_root_modulus_squared"] - 1.0 / 11.0) < 1e-12
    assert legacy["grh_violations"] == 0
    assert legacy["grh_satisfied"] is gap_cert["graph_rh_satisfied"]
