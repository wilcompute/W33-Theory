#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_heawood_spread_pair_pgsp_equivariance import build_result as build_pgsp  # noqa: E402
from w33_heawood_spread_pair_stabilizer96_fingerprint import (  # noqa: E402
    build_result as build_stabilizer,
)


def test_full_pgsp_equivariance_closes_outer_coset() -> None:
    data = build_pgsp()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["outer_generator"]["similitude_multiplier"] == 2
    assert data["outer_generator"]["projective_order"] == 2
    assert data["outer_generator"]["commutes_with_bijection"] is True
    assert data["orbit_stabilizer"]["PSp_C6_orbit"] == 270
    assert data["orbit_stabilizer"]["PSp_C6_stabilizer"] == 96
    assert data["orbit_stabilizer"]["PGSp_C6_orbit"] == 270
    assert data["orbit_stabilizer"]["PGSp_C6_stabilizer"] == 192
    assert data["orbit_stabilizer"]["prior_Pass1996_full_stabilizer_structure"] == "D8 x S4"


def test_psp_stabilizer96_exact_fingerprint_and_tomotope_no_go() -> None:
    data = build_stabilizer()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    H = data["actual_stabilizer"]
    assert H["order"] == 96
    assert H["center_order"] == 2
    assert H["derived_order"] == 24
    assert H["abelianization_order"] == 4
    assert H["element_order_histogram"] == {
        "1": 1,
        "2": 27,
        "3": 8,
        "4": 36,
        "6": 24,
    }
    assert H["matched_index2_kernel_types"] == [
        "mixed fibre product with V4 D8-kernel"
    ]
    assert sorted(H["matching_character_rows"]) == [[1, 0, 1], [1, 1, 1]]
    assert data["tomotope_firewall"]["tomotope_derived_order_repo_certified"] == 48
    assert data["checks"]["tomotope_96_is_ruled_out_by_derived_order"] is True


if __name__ == "__main__":
    test_full_pgsp_equivariance_closes_outer_coset()
    test_psp_stabilizer96_exact_fingerprint_and_tomotope_no_go()
    print("PGSp and stabilizer-96 focused tests passed")
