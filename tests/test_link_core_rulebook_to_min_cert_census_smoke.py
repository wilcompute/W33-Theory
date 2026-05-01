from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.link_core_rulebook_to_min_cert_census import build_report

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
    reason="core rulebook census link requires optional min-cert census artifacts",
)


def test_build_report_flags_and_counts() -> None:
    payload = build_report()
    assert payload["status"] == "ok"
    assert payload["core_motif_count"] == 13

    flags = payload["theorem_flags"]
    assert flags["agl_exact_has_zero_core_overlap"] is True
    assert flags["hessian_exact_has_positive_core_overlap"] is True
    assert flags["hessian_exhaustive_has_positive_core_overlap"] is True
    assert flags["dominant_overlap_motif_is_x_110"] is True

    summary = payload["dataset_summary"]
    assert summary["agl_exact_full"]["distinct_representatives"] == 7
    assert summary["agl_exact_full"]["reps_with_core_overlap"] == 0
    assert summary["hessian_exact_full"]["reps_with_core_overlap"] > 0
    assert summary["hessian_exhaustive2"]["reps_with_core_overlap"] > 0


def test_cli_smoke(tmp_path: Path) -> None:
    if not Path("artifacts/nontrivial_core_rulebook_2026_02_11.json").exists():
        pytest.skip(
            "Missing artifacts/nontrivial_core_rulebook_2026_02_11.json (integration-only)"
        )
    out_json = tmp_path / "core_rulebook_link.json"
    out_md = tmp_path / "core_rulebook_link.md"
    cmd = [
        sys.executable,
        "tools/link_core_rulebook_to_min_cert_census.py",
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
