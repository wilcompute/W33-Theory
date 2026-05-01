from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import tools.s12_universal_algebra as s12


def test_analyze_s12_jacobi_failure_pattern_cli_smoke(tmp_path: Path) -> None:
    s12_report_path = tmp_path / "s12_universalization_report.json"
    s12_report = s12.build_s12_universal_report(jordan_sample_limit=120)
    s12_report_path.write_text(json.dumps(s12_report, indent=2), encoding="utf-8")

    out_json = tmp_path / "jacobi_pattern.json"
    out_md = tmp_path / "jacobi_pattern.md"
    cmd = [
        sys.executable,
        "tools/analyze_s12_jacobi_failure_pattern.py",
        "--s12-report-json",
        str(s12_report_path),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    assert out_json.exists()
    assert out_md.exists()

    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["jacobi_failure_count_reported"] == 6
    assert payload["jacobi_failure_count_observed"] == 6
    assert payload["pattern_match"] is True
    assert payload["two_of_one_one_of_other_match"] is True
    assert payload["s3_orbit_count"] == 2
    assert payload["claim_holds"] is True

    text = out_md.read_text(encoding="utf-8")
    assert "# s12 Jacobi Failure Pattern" in text
    assert "predicate match" in text
    assert "S3 Orbits" in text

    # Explicit algebra bridge: the missing Jacobi phase is a Weyl–Heisenberg cocycle,
    # and the same phase threads through the E8 Z3 / L-infinity firewall via CE2.
    fw_path = Path("artifacts") / "firewall_bad_triads_mapping.json"
    if not fw_path.exists():
        pytest.skip(
            "firewall_bad_triads_mapping.json is an ignored heavy artifact; "
            "run tools/map_firewall_bad_triangles_to_cubic_triads.py to materialize the bridge input"
        )
    e6_basis_path = Path("artifacts") / "e6_27rep_basis_export" / "E6_basis_78.npy"
    if not e6_basis_path.exists():
        pytest.skip(
            "E6_basis_78.npy is an ignored E6 basis export; "
            "run tools/build_e6_27rep_minuscule.py --export-basis78 to materialize the bridge input"
        )
    cmd2 = [sys.executable, "-X", "utf8", "scripts/w33_s12_linfty_phase_bridge.py"]
    run2 = subprocess.run(
        cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert run2.returncode == 0, run2.stderr
    # recent script prints improved confirmation line
    assert "Global predictor reproduces CE2 sparse entry exactly" in run2.stdout
