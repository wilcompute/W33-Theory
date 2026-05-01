from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.search_core_motif_anchor_sets import build_report

REQUIRED_INPUTS = [
    Path("artifacts/nontrivial_core_rulebook_2026_02_11.json"),
    Path("artifacts/e6_f3_trilinear_min_cert_exact_hessian_full_with_geotypes.json"),
    Path(
        "artifacts/e6_f3_trilinear_min_cert_enumeration_hessian_exhaustive2_with_geotypes.json"
    ),
]

pytestmark = pytest.mark.skipif(
    not all(path.exists() for path in REQUIRED_INPUTS),
    reason="core motif anchor search requires optional min-cert census artifacts",
)


def test_build_report_has_better_coverage_than_fixed_anchor() -> None:
    payload = build_report()
    assert payload["status"] == "ok"
    assert payload["candidate_count"] > 0

    baseline = payload["fixed_anchor_baseline"]["metrics"]
    best = payload["best_candidate"]
    assert best is not None
    metrics = best["metrics"]

    assert float(metrics["precision_when_fired"]) >= 0.90
    assert float(metrics["coverage"]) >= float(baseline["coverage"])
    assert int(metrics["conflict_count"]) == 0
    assert "x:1-1-0" in set(best["full_anchors"])
    assert "x:2-2-1" in set(best["reduced_anchors"])

    flags = payload["theorem_flags"]
    assert flags["has_feasible_candidate"] is True
    assert flags["best_coverage_ge_fixed_coverage"] is True
    assert flags["best_precision_ge_precision_min"] is True


def test_cli_smoke(tmp_path: Path) -> None:
    out_json = tmp_path / "core_motif_anchor_search.json"
    out_md = tmp_path / "core_motif_anchor_search.md"
    cmd = [
        sys.executable,
        "tools/search_core_motif_anchor_sets.py",
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
