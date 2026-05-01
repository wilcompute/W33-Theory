from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.classify_core_motif_orbit_polarization import build_report

REQUIRED_INPUTS = [
    Path("artifacts/nontrivial_core_rulebook_2026_02_11.json"),
    Path("artifacts/e6_f3_trilinear_min_cert_exact_agl_full_with_geotypes.json"),
    Path("artifacts/e6_f3_trilinear_min_cert_exact_hessian_full_with_geotypes.json"),
    Path(
        "artifacts/e6_f3_trilinear_min_cert_enumeration_hessian_exhaustive2_with_geotypes.json"
    ),
]

pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REQUIRED_INPUTS),
    reason="core motif orbit polarization requires optional min-cert census artifacts",
)


def test_build_report_expected_counts() -> None:
    payload = build_report()
    assert payload["status"] == "ok"
    assert payload["core_motif_count"] == 13

    summary = payload["dataset_summary"]
    assert summary["agl_exact_full"]["overlap_representatives"] == 0
    assert summary["hessian_exact_full"]["overlap_representatives"] == 18
    assert summary["hessian_exact_full"]["overlap_orbit_hist"] == {
        "1296": 2,
        "2592": 16,
    }
    assert summary["hessian_exhaustive2"]["overlap_representatives"] == 30
    assert summary["hessian_exhaustive2"]["overlap_orbit_hist"] == {
        "1296": 4,
        "2592": 26,
    }

    x110 = payload["x110_by_dataset"]
    assert x110["hessian_exact_full"]["support"] == 16
    assert x110["hessian_exact_full"]["orbit_2592_count"] == 15
    assert x110["hessian_exhaustive2"]["support"] == 20
    assert x110["hessian_exhaustive2"]["orbit_2592_count"] == 19

    flags = payload["theorem_flags"]
    assert flags["agl_exact_zero_overlap"] is True
    assert flags["hessian_exact_positive_overlap"] is True
    assert flags["hessian_exhaustive_positive_overlap"] is True
    assert flags["x110_precision_ge_0p90_in_hessian_exact"] is True
    assert flags["x110_precision_ge_0p90_in_hessian_exhaustive"] is True
    assert flags["x110_combined_precision_ge_0p90_in_hessian"] is True


def test_cli_smoke(tmp_path: Path) -> None:
    out_json = tmp_path / "core_motif_orbit_polarization.json"
    out_md = tmp_path / "core_motif_orbit_polarization.md"
    cmd = [
        sys.executable,
        "tools/classify_core_motif_orbit_polarization.py",
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert out_md.exists()
