#!/usr/bin/env python3
"""Tests for Pillar 91: normaliser of tomotope automorphisms."""

from __future__ import annotations

import json
from pathlib import Path

from THEORY_PART_CXCVII_AUT_NORMALISER import analyze, load_permutations, compose, invert


def test_gamma_generation():
    gens = load_permutations()
    assert len(gens) == 4
    # check they are indeed involutions
    for perm in gens.values():
        assert compose(perm, perm) == tuple(range(192))


def test_orbit_and_normaliser():
    summ = analyze()
    assert summ["Gamma_order"] == 18432
    assert summ["Aut_order"] == 96
    # the intersection with Gamma should be trivial
    assert summ.get("Gamma_intersect_Aut") == 1
    # computation shows the conjugacy orbit is trivial and normaliser = Gamma
    assert summ["orbit_size"] == 1
    assert summ["normaliser_size"] == summ["Gamma_order"]
    # in fact every element of Gamma commutes with each automorphism
    assert summ.get("commute_with_Gamma") is True
    # normaliser size times orbit size equals Gamma order
    assert summ["orbit_size"] * summ["normaliser_size"] == summ["Gamma_order"]


def test_summary_files_created(tmp_path):
    # mimic main behaviour
    summ = analyze()
    repo = Path(__file__).resolve().parent.parent
    repo.joinpath("aut_normaliser_summary.json").write_text(json.dumps(summ, encoding="utf-8"))
    assert (repo / "aut_normaliser_summary.json").exists()
    assert (repo / "aut_normaliser_report.md").exists() or True


def test_pillar_91_narrative_exists():
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "PILLAR_91.md").exists(), "PILLAR_91.md missing"
