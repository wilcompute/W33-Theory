"""Focused regression for the GAP-owned Pass 373 certificate."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 373")
def test_pass373_proves_exact_triangle_boundary_code_and_mlut() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass373_triangle_boundary_mlut.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Pass373 status=PASS" in result.stdout

    certificate = json.loads(
        (ROOT / "data" / "w33_pass373_triangle_boundary_mlut.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 12 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["code"] == {
        "object": "image of the oriented W33 triangle boundary map over GF(3)",
        "parameters": "[240,120,3]_3",
        "length": 240,
        "dimension": 120,
        "minimum_distance": 3,
    }
    assert certificate["parity_certificate"] == {
        "rank": 120,
        "nonzero_columns": 240,
        "projective_column_classes": 240,
    }
    assert certificate["decoder"] == {
        "correction_radius": 1,
        "nonzero_single_error_syndromes": 480,
        "complete_mlut_entries": 481,
    }
    assert "not itself the qutrit CSS code" in certificate["separation"]
    assert "[[240,81,3]]_3" in certificate["separation"]
    assert "analysis/w33_css_exact_audit.py" in certificate["separation"]


def test_short_distance_certificate_covers_one_two_three_and_fallback() -> None:
    from scripts.w33_quantum_error_correction import code_min_distance_from_basis

    assert code_min_distance_from_basis(np.eye(3, dtype=int)) == 1
    assert code_min_distance_from_basis(np.array([[1, 1]], dtype=int)) == 2
    assert code_min_distance_from_basis(np.array([[1, 1, 1]], dtype=int)) == 3
    assert code_min_distance_from_basis(np.array([[1, 1, 1, 1]], dtype=int)) == 4


def test_pass373_is_published_with_the_css_object_boundary() -> None:
    surfaces = {
        "README": (ROOT / "README.md").read_text(encoding="utf-8"),
        "paper": (ROOT / "w33_paper.tex").read_text(encoding="utf-8"),
        "photonic": (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8"),
        "practical": (ROOT / "holonet_practical_implications.tex").read_text(
            encoding="utf-8"
        ),
        "website": (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    }
    for name, surface in surfaces.items():
        assert "[240,120,3]" in surface, name
        assert "481" in surface, name

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `[240,120,3]` |" in index
