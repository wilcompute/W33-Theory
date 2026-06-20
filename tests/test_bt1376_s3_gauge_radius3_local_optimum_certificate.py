#!/usr/bin/env python3
"""Regression tests for BT1376."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1376_radius3_local_optimum_certificate() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis/bt1376_s3_gauge_radius3_local_optimum_certificate.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (
            ROOT / "data/bt1376_s3_gauge_radius3_local_optimum_certificate.json"
        ).read_text(encoding="utf-8")
    )

    assert data["verified"] is True
    assert data["base_witness"]["identity_edges"] == 210
    assert data["base_witness"]["nonidentity_corrections"] == 330
    assert data["local_certificate"]["total_candidate_relabels_checked"] == 1991015

    radii = {row["radius"]: row for row in data["local_certificate"]["radii"]}
    assert radii[1]["candidate_relabels_checked"] == 195
    assert radii[2]["candidate_relabels_checked"] == 25935
    assert radii[3]["candidate_relabels_checked"] == 1964885
    assert {radii[radius]["best_delta"] for radius in (1, 2, 3)} == {-5}
    assert {
        radii[radius]["best_alternative_identity_edges"] for radius in (1, 2, 3)
    } == {205}


def test_bt1376_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "BT1376: radius-3 local optimum certificate for the S3 gauge" in text
    assert "BT1376_s3_gauge_radius3_local_optimum_certificate.md" in text
    assert "1,991,015" in text
    assert "best delta <code>-5</code>" in text


if __name__ == "__main__":
    test_bt1376_radius3_local_optimum_certificate()
    test_bt1376_docs_index_card_present()
    print("BT1376 focused tests passed")
