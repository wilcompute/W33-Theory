from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxvii_closure_geodesic_refinement_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["total_proper_time_span"] == 5
    assert s["canonical_step_count"] == 5
    assert s["canonical_refinement_action"] == 5
    assert s["coarse_one_jump_action"] == 25
    assert s["extremal_gap"] == 20


def test_canonical_and_coarse_refinements() -> None:
    payload = build_bridge()
    fam = payload["refinement_family"]
    assert fam["canonical_minimizer"]["partition"] == [1, 1, 1, 1, 1]
    assert fam["coarse_maximizer_example"]["partition"] == [5]
    assert fam["canonical_minimizer"]["weight_denominator"] == 32
    assert fam["coarse_maximizer_example"]["weight_denominator"] == 32


def test_all_refinements_preserve_linear_action_and_weight() -> None:
    payload = build_bridge()
    for item in payload["refinement_family"]["all_refinements"]:
        assert item["linear_action"] == 5
        assert item["weight_denominator"] == 32


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
