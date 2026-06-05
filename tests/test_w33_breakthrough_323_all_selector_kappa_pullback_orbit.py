from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_323_all_selector_kappa_pullback_orbit import (  # noqa: E402
    all_selector_kappa_pullback_orbit_packet,
)


PACKET = all_selector_kappa_pullback_orbit_packet()


def test_bt323_selector_counts_and_orbit() -> None:
    assert PACKET["q4_selector_count"] == 8
    assert PACKET["q4_mobius_kantor_count"] == 8
    assert PACKET["affine_automorphism_order"] == 384
    assert PACKET["q4_selector_orbit_sizes"] == [8]
    assert PACKET["q4_selector_stabilizer_order"] == 48


def test_bt323_each_row_has_q4_matching_and_mk_complement() -> None:
    for row in PACKET["selector_rows"]:
        assert len(row["q4_pullback_matching"]) == 8
        assert len(row["q4_mobius_kantor_layer"]) == 24
        assert row["q4_matching_xor_profile"] == {1: 2, 2: 2, 4: 2, 8: 2}
        assert row["q4_mk_girth"] == 6


def test_bt323_intersection_geometry() -> None:
    assert PACKET["pair_intersection_distribution"] == {0: 12, 2: 16}
    assert PACKET["disjointness_components"] == [[0, 3, 5, 6], [1, 2, 4, 7]]
    assert all(len(neighbors) == 3 for neighbors in PACKET["disjointness_graph"].values())
    assert all(len(neighbors) == 4 for neighbors in PACKET["two_overlap_graph"].values())


def test_bt323_coverage_frequencies() -> None:
    assert PACKET["coverage"]["q4_mk_edge_frequency_distribution"] == {6: 32}
    assert PACKET["coverage"]["source_selector_edge_frequency_distribution"] == {2: 32}
    assert PACKET["coverage"]["source_mk_edge_frequency_distribution"] == {6: 32}


def test_bt323_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 20
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt323_selector_counts_and_orbit()
    test_bt323_each_row_has_q4_matching_and_mk_complement()
    test_bt323_intersection_geometry()
    test_bt323_coverage_frequencies()
    test_bt323_all_checks_pass()
