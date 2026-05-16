from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxii_octahedral_fundamental_matrix_hitting_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["kemeny_constant"] - (13.0 / 3.0)) < 1e-10
    assert abs(s["trace_z_minus_one"] - (13.0 / 3.0)) < 1e-10
    assert abs(s["adjacent_hitting_time"] - 5.0) < 1e-10
    assert abs(s["antipodal_hitting_time"] - 6.0) < 1e-10


def test_hitting_matrices_match() -> None:
    payload = build_bridge()
    Hf = payload["operators"]["H_fundamental"]
    Hd = payload["operators"]["H_direct"]
    n = len(Hf)
    for i in range(n):
        for j in range(n):
            assert abs(Hf[i][j] - Hd[i][j]) < 1e-9


def test_kemeny_rows_constant() -> None:
    payload = build_bridge()
    rows = payload["kemeny_rows"]
    for x in rows:
        assert abs(x - rows[0]) < 1e-9


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
