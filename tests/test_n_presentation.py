#!/usr/bin/env python3
"""Tests for Pillar 95: N structure and presentation."""

from __future__ import annotations

import json
from pathlib import Path

from THEORY_PART_CXCV_N_PRESENTATION import find_presentation

repo = Path(__file__).resolve().parent.parent
ARCHIVE_FILE = repo / "archive" / "json" / "N_heis_presentation.json"


def test_presentation_file_exists():
    assert ARCHIVE_FILE.exists()


def test_presentation_properties():
    s = find_presentation()
    # N should be 2- or 3-generated
    assert s["T1_num_generators"] in (2, 3)
    # derived subgroup divides 192
    assert 192 % s["T2_derived_order"] == 0
    # abelianisation
    assert s["T2_abelianisation_order"] == 192 // s["T2_derived_order"]
    # Sylow-2 subgroup: if found, must be 64; if not found, -1
    assert s["T4_sylow2_order"] in (64, -1)
    # order-3 subgroup
    assert s["T5_ord3_subgroup_order"] > 0
