from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccliv_octahedral_commute_hitting_time_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert s["edge_count"] == 12
    assert abs(s["adjacent_commute_time"] - 10.0) < 1e-9
    assert abs(s["antipodal_commute_time"] - 12.0) < 1e-9
    assert abs(s["adjacent_hitting_time"] - 5.0) < 1e-9
    assert abs(s["antipodal_hitting_time"] - 6.0) < 1e-9
    assert abs(s["kemeny_constant"] - (13.0 / 3.0)) < 1e-9


def test_commute_matrix_symmetry() -> None:
    payload = build_bridge()
    C = payload["operators"]["commute_times"]
    n = len(C)
    for i in range(n):
        assert abs(C[i][i]) < 1e-9
        for j in range(n):
            assert abs(C[i][j] - C[j][i]) < 1e-9


def test_resistance_commute_match() -> None:
    payload = build_bridge()
    C = payload["operators"]["commute_times"]
    RC = payload["operators"]["resistance_commute_from_2mR"]
    n = len(C)
    for i in range(n):
        for j in range(n):
            assert abs(C[i][j] - RC[i][j]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
