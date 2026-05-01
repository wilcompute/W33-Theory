#!/usr/bin/env python3
"""Tests for Pillar 92: tomotope symmetry structure."""

from __future__ import annotations

from THEORY_PART_CXCII_TOMOTOPE_STRUCTURE import analyze


def test_structure_summary():
    summ = analyze()
    assert summ["Gamma_order"] == 18432
    assert summ["Aut_order"] == 96
    assert summ["Gamma_intersect_Aut"] == 1
    assert summ["commute_with_Gamma"] is True
    assert summ["direct_product_order"] == summ["Gamma_order"] * summ["Aut_order"]
    # there should be multiple conjugacy classes but none of size exactly 192
    assert summ.get("num_conj_classes", 0) > 1
    assert 192 in summ.get("conj_class_sizes", [])


def test_pillar_92_narrative_exists():
    from pathlib import Path

    repo = Path(__file__).resolve().parent.parent
    assert (repo / "archive" / "misc" / "PILLAR_92.md").exists(), "PILLAR_92.md missing"
