from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcc_holonomy_active_column_basis_frontier_bridge import build_bridge


def test_dcc_summary_matches_active_basis_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["active_column_count"] == 36
    assert summary["active_restricted_rank"] == 36
    assert summary["inert_column_count"] == 9
    assert summary["inert_triple_count"] == 3


def test_dcc_basis_data_matches_inert_complement_structure() -> None:
    payload = build_bridge()
    basis_data = payload["basis_data"]

    assert basis_data["off_diagonal_curvature_rank"] == 36
    assert basis_data["inactive_column_complement_triples"] == [[36, 40, 44], [37, 41, 42], [38, 39, 43]]
    assert basis_data["fixed_host_plane"] == "U1"
    assert basis_data["fixed_shell"] == [81, 162, 81]


def test_dcc_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())