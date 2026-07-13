"""Regression coverage for the GAP-owned Pass 214 certificate."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass214_source_line_v4_torsor.g"
CERTIFICATE = ROOT / "data" / "w33_pass214_source_line_v4_torsor.json"


@lru_cache(maxsize=1)
def _certificate() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 214"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=90,
    )
    assert "Pass 214 source-line V4 torsor: PASS" in result.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_pass214_universal_source_torsor_certificate() -> None:
    cert = _certificate()
    assert cert["schema"] == "w33.pass214.source_line_v4_torsor.gap.v1"
    assert cert["producer"].startswith("GAP ")
    assert cert["status"] == "PASS"
    assert cert["theorem"]["verdict"] == (
        "PROVED for every active pair and every source origin"
    )
    assert cert["counts"] == {
        "active_pairs": 1080,
        "source_origins": 4320,
        "nonidentity_partition_labels": 3240,
        "source_point_partition_incidence_cases": 12960,
        "generator_kernel_covariance_cases": 2160,
        "generator_partition_covariance_cases": 6480,
    }
    assert all(cert["checks"].values())


def test_pass214_identity_and_three_partition_labels() -> None:
    seed = _certificate()["seed"]
    assert seed["active_pair"] == [1, 2]
    assert seed["line_points"] == [1, 14, 15, 16]
    assert seed["sample_source_origin"] == 1
    assert seed["identity_row"] == [
        1,
        "identity fixes the chosen source origin",
    ]
    assert seed["nonidentity_rows_image_point_then_partition"] == [
        [14, [[1, 14], [15, 16]]],
        [15, [[1, 15], [14, 16]]],
        [16, [[1, 16], [14, 15]]],
    ]


def test_pass214_keeps_completion_and_semantic_boundaries() -> None:
    cert = _certificate()
    assert "completion-line points" in cert["compatibility"]["no_contradiction"]
    assert "source line" in cert["compatibility"]["no_contradiction"]
    assert "no assignment" in cert["semantic_boundary"]["not_canonical"]
    assert "external frame or calibration" in (
        cert["semantic_boundary"]["not_canonical"]
    )
