from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
for p in (str(ROOT), str(ANALYSIS)):
    if p not in sys.path:
        sys.path.insert(0, p)

from w33_boundary_singer_toroidal_84_bridge import build_result  # noqa: E402


def test_boundary_singer_toroidal_84_bridge_is_equivariant() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())

    singer = data["boundary_singer"]
    assert singer["PG24_points"] == 21
    assert singer["C21_order"] == 21
    assert singer["C7_orbit_count_on_PG24"] == 3
    assert singer["C7_orbit_sizes"] == [7, 7, 7]

    local = data["local12"]
    assert local["AGL14_order"] == 12
    assert local["AGL14_element_order_histogram"] == {"1": 1, "2": 3, "3": 8}
    assert "A4" in local["AGL14_isomorphism"]
    assert "A4" in local["cube_cover_match"]

    tor = data["toroidal_codec"]
    assert tor["flag_count"] == 84
    assert tor["C7_equivariance_checks"] == 84
    assert data["spectral_bridge"]["denominator_identity"] == "84 = 4*|PG(2,4)| = |PG(2,4)xGF(4)|"
