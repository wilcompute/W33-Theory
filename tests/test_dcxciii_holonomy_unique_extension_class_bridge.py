from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxciii_holonomy_unique_extension_class_bridge import build_bridge


def test_dcxciii_summary_matches_two_class_reduction() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["trivial_class_count"] == 1
    assert summary["nontrivial_class_count"] == 1
    assert summary["total_class_count"] == 2
    assert summary["matter_extension_dimension"] == 162


def test_dcxciii_nonzero_orbit_is_the_unique_nontrivial_class() -> None:
    payload = build_bridge()
    class_data = payload["class_data"]

    assert class_data["trivial_representative"] == [[0, 0], [0, 0]]
    assert class_data["nontrivial_representatives"] == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
    assert class_data["short_exact_sequence_dimensions"] == [81, 162, 81]
    assert class_data["cocycle_is_not_a_coboundary"] is True


def test_dcxciii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())