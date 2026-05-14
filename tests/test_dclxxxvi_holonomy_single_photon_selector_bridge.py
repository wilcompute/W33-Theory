from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxvi_holonomy_single_photon_selector_bridge import build_bridge


def test_dclxxxvi_summary_matches_expected_selector_scales() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["branch_count"] == 3
    assert summary["local_selector_group_order"] == 6
    assert summary["affine_bulk_count"] == 27
    assert summary["ordered_adjacent_pair_count"] == 60
    assert summary["global_selector_carrier"] == 1620


def test_dclxxxvi_local_relations_are_s3() -> None:
    payload = build_bridge()
    group = payload["local_selector_group"]

    assert group["translation"] == [1, 2, 0]
    assert group["reflection"] == [0, 2, 1]
    assert group["translation_inverse"] == [2, 0, 1]
    assert len(group["elements"]) == 6


def test_dclxxxvi_affine_bulk_scales_exactly_to_the_1620_selector_carrier() -> None:
    payload = build_bridge()
    scaling = payload["carrier_scaling"]

    assert scaling["affine_bulk_count"] == scaling["quadrangles_per_pair"] == 27
    assert scaling["ordered_adjacent_pair_count"] * scaling["affine_bulk_count"] == scaling["global_selector_carrier"] == 1620


def test_dclxxxvi_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())