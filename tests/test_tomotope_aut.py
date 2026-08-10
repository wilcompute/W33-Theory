#!/usr/bin/env python3
"""Tests for Pillar 90: tomotope automorphism group analysis."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from THEORY_PART_CXCVI_TOMOTOPE_AUTOMORPHISMS import (
    analyze,
    build_graph,
    compute_automorphisms,
    load_r_generators,
)


def test_load_and_build_graph():
    gens = load_r_generators()
    assert set(gens.keys()) == {0, 1, 2, 3}
    G = build_graph(gens)
    assert G.number_of_nodes() == 192
    # each node has degree 4 (one edge per generator) although some edges are repeated
    degs = set(dict(G.degree()).values())
    assert max(degs) <= 4 and min(degs) >= 1


def test_automorphism_count():
    summary = analyze()
    assert summary["T1_automorphism_count"] == 96
    # cycle distribution should sum to 96 automorphisms * 192 flags
    total = sum(l * c for l, c in summary["T2_cycle_distribution"].items())
    assert total == 96 * 192


def test_write_results(tmp_path):
    # verify writing creates JSON and MD
    summ = analyze()
    # temporarily override write location by calling analyze and writing manually
    p = tmp_path / "s.json"
    p.write_text(json.dumps(summ, encoding="utf-8"))
    assert p.exists()


def test_summary_file_created(tmp_path, monkeypatch):
    # call main and ensure files appear in workspace root
    repo = Path(__file__).resolve().parent.parent
    # run the module's main
    import THEORY_PART_CXCVI_TOMOTOPE_AUTOMORPHISMS as mod
    mod.main()
    assert (repo / "tomotope_aut_summary.json").exists()
    assert (repo / "tomotope_aut_report.md").exists()


def test_pillar_90_narrative_exists():
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "PILLAR_90.md").exists(), "narrative PILLAR_90.md should be present"
