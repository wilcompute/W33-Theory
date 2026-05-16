from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccliii_octahedral_effective_resistance_dirichlet_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert s["adjacent_pair_count"] == 12
    assert s["antipodal_pair_count"] == 3
    assert abs(s["adjacent_resistance"] - (5.0 / 12.0)) < 1e-9
    assert abs(s["antipodal_resistance"] - 0.5) < 1e-9
    assert abs(s["kirchhoff_index"] - 6.5) < 1e-9


def test_orbit_sizes_and_values() -> None:
    payload = build_bridge()
    pairs = payload["pair_orbits"]
    assert len(pairs["adjacent_pairs"]) == 12
    assert len(pairs["antipodal_pairs"]) == 3

    R = payload["operators"]["resistance_matrix"]
    i, j = pairs["adjacent_pairs"][0]
    assert abs(R[i][j] - (5.0 / 12.0)) < 1e-9
    i, j = pairs["antipodal_pairs"][0]
    assert abs(R[i][j] - 0.5) < 1e-9


def test_dipole_dirichlet_identity() -> None:
    payload = build_bridge()
    for d in payload["dipole_checks"].values():
        assert max(abs(v) for v in d["residual"]) < 1e-9
        assert abs(d["energy"] - d["work"]) < 1e-9
        assert abs(d["work"] - d["effective_resistance"]) < 1e-9
        assert abs(d["potential_mean"]) < 1e-9


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
