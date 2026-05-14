from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxiv_holonomy_qutrit_transvection_bridge import build_bridge


def test_dclxiv_summary_matches_expected_shell_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["field_order"] == 3
    assert summary["vertex_count"] == 40
    assert summary["transvection_order"] == 3
    assert summary["fixed_projective_count"] == 13
    assert summary["affine_bulk_count"] == 27
    assert summary["affine_fiber_count"] == 9
    assert summary["affine_fiber_size"] == 3


def test_dclxiv_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxiv_projective_orbit_structure_is_13_plus_9_times_3() -> None:
    payload = build_bridge()
    carrier = payload["carrier_action"]

    assert carrier["projective_orbit_size_counts"] == {1: 13, 3: 9}
    assert len(carrier["fixed_projective_points"]) == 13
    assert len(carrier["affine_fibers"]) == 9
    assert all(fiber["is_translation_fiber"] for fiber in carrier["affine_fibers"])


def test_dclxiv_sample_affine_orbit_is_one_qutrit_fiber() -> None:
    payload = build_bridge()
    sample = payload["carrier_action"]["sample_affine_orbit"]
    assert len(sample) == 3

    a_values = sorted(point[0] for point in sample)
    b_values = {point[1] for point in sample}
    c_values = {point[2] for point in sample}
    d_values = {point[3] for point in sample}

    assert a_values == [0, 1, 2]
    assert b_values == {1}
    assert len(c_values) == 1
    assert len(d_values) == 1