from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_167_f4_e6_rank3_coset_quotient import (  # noqa: E402
    f4_e6_rank3_coset_quotient_packet,
)


PACKET = f4_e6_rank3_coset_quotient_packet()


def test_bt167_index_and_suborbits() -> None:
    assert PACKET["group_order"] == 51_840
    assert PACKET["normalizer_order"] == 1_152
    assert PACKET["index"] == 45
    assert PACKET["double_coset_suborbit_sizes"] == [1, 12, 32]


def test_bt167_orbital_12_is_srg_45_12_3_3() -> None:
    graph = PACKET["orbital_12_graph"]
    assert graph["v"] == 45
    assert graph["symmetric"] is True
    assert graph["degree_distribution"] == {12: 45}
    assert graph["lambda_distribution"] == {3: 270}
    assert graph["mu_distribution"] == {3: 720}
    assert graph["edge_count"] == 270


def test_bt167_orbital_32_is_complement() -> None:
    graph = PACKET["orbital_32_graph"]
    assert graph["v"] == 45
    assert graph["symmetric"] is True
    assert graph["degree_distribution"] == {32: 45}
    assert graph["lambda_distribution"] == {22: 720}
    assert graph["mu_distribution"] == {24: 270}
    assert graph["edge_count"] == 720


def test_bt167_tail_intersects_rank3_quotient_cleanly() -> None:
    assert PACKET["tail_by_orbit_size_polarization_diameter"] == {
        "(1, 'anti', 6)": 65,
        "(1, 'anti', 7)": 8,
        "(12, 'mixed', 6)": 4,
        "(32, 'mixed', 6)": 74,
    }


def test_bt167_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt167_index_and_suborbits()
    test_bt167_orbital_12_is_srg_45_12_3_3()
    test_bt167_orbital_32_is_complement()
    test_bt167_tail_intersects_rank3_quotient_cleanly()
    test_bt167_all_checks_pass()
