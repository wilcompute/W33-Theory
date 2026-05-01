from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.core_motif_enrichment_stats import build_report

REQUIRED_INPUTS = [
    Path("artifacts/nontrivial_core_rulebook_2026_02_11.json"),
    Path("artifacts/e6_f3_trilinear_min_cert_exact_hessian_full_with_geotypes.json"),
    Path(
        "artifacts/e6_f3_trilinear_min_cert_enumeration_hessian_exhaustive2_with_geotypes.json"
    ),
]

pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REQUIRED_INPUTS),
    reason="core motif enrichment stats require optional min-cert census artifacts",
)


def test_build_report_focus_motifs() -> None:
    payload = build_report()
    assert payload["status"] == "ok"
    assert payload["core_motif_count"] == 13

    focus = payload["focus_motifs"]
    x110 = focus["x_1_1_0"]
    assert x110 is not None
    assert x110["support"] == 36
    assert x110["orbit_2592_count"] == 34
    assert abs(float(x110["precision_2592"]) - (34.0 / 36.0)) < 1e-12
    assert float(x110["pvalue_enrich_2592"]) <= 0.05

    x221 = focus["x_2_2_1"]
    assert x221 is not None
    assert x221["support"] == 2
    assert x221["orbit_2592_count"] == 0
    assert float(x221["pvalue_enrich_1296"]) <= 0.05

    flags = payload["theorem_flags"]
    assert flags["hessian_combined_has_x110"] is True
    assert flags["x110_support_ge_30"] is True
    assert flags["x110_precision_ge_0p90"] is True
    assert flags["x110_enrichment_pvalue_le_0p05"] is True
    assert flags["x221_exists_and_is_pure_1296"] is True


def test_cli_smoke(tmp_path: Path) -> None:
    out_json = tmp_path / "core_motif_enrichment_stats.json"
    out_md = tmp_path / "core_motif_enrichment_stats.md"
    cmd = [
        sys.executable,
        "tools/core_motif_enrichment_stats.py",
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
