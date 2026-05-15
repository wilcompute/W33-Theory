from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.PART_CCCCCLXXXVIII_e6_a2_root_refinement import build


def test_root_level_e8_grading_count():
    summary = build()
    assert summary.e6_roots + summary.a2_roots + summary.g1_roots + summary.g2_roots == 240


def test_lie_algebra_dimension_grading_count():
    summary = build()
    assert summary.dim_e6 + summary.dim_a2 + summary.g1_roots + summary.g2_roots == 248


def test_we6_orbits_refine_to_e6_a2_matter():
    summary = build()
    assert summary.e6_roots == 72
    assert summary.a2_roots == 6
    assert summary.g1_roots + summary.g2_roots == 162
    assert summary.e8_root_carrier == 240


def test_six_27_orbits_split_into_two_81_charge_triples():
    summary = build()
    assert summary.g1_roots == 81
    assert summary.g2_roots == 81
    assert summary.g1_roots + summary.g2_roots == 162


def test_a2_root_and_rank_counts():
    summary = build()
    a2_rank = 2
    assert summary.a2_roots + a2_rank == summary.dim_a2


def test_e6_root_and_rank_counts():
    summary = build()
    e6_rank = 6
    assert summary.e6_roots + e6_rank == summary.dim_e6


def test_claim_surface_marks_cover_tower_as_conditional():
    summary = build()
    assert summary.claims["root_refinement"]["status"] == "exact_verified"
    assert summary.claims["cover_tower_continuity_bridge"]["status"] == "conditional_verified"
    assert len(summary.claims["cover_tower_continuity_bridge"]["assumptions"]) >= 1


def test_all_checks_hold():
    summary = build()
    assert all(summary.checks.values())
