from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition import (  # noqa: E402
    k88_q4_mobius_kantor_decomposition_packet,
)


PACKET = k88_q4_mobius_kantor_decomposition_packet()


def test_bt271_edge_and_degree_splits() -> None:
    assert PACKET["edge_counts"] == {
        "K8_8": 64,
        "Q4": 32,
        "Mobius_Kantor": 24,
        "M8_matching": 8,
        "Q4_plus_MK": 56,
    }
    assert PACKET["degree_split"] == {
        "Q4": 4,
        "Mobius_Kantor": 3,
        "M8_matching": 1,
        "total": 8,
    }


def test_bt271_xor_weight_layers() -> None:
    assert PACKET["xor_weight_distributions"]["Q4"] == {1: 32}
    assert PACKET["xor_weight_distributions"]["cross_complement"] == {3: 32}
    assert PACKET["xor_weight_distributions"]["Mobius_Kantor"] == {3: 24}
    assert PACKET["xor_weight_distributions"]["M8_matching"] == {3: 8}
    assert PACKET["residual_xor_direction_counts"] == {7: 2, 11: 2, 13: 2, 14: 2}


def test_bt271_mobius_kantor_and_q4_girths() -> None:
    assert PACKET["girths"] == {"Mobius_Kantor": 6, "Q4": 4}
    assert len(PACKET["edge_parts"]["Mobius_Kantor"]) == 24
    assert len(PACKET["edge_parts"]["M8_matching"]) == 8


def test_bt271_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 15
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt271_edge_and_degree_splits()
    test_bt271_xor_weight_layers()
    test_bt271_mobius_kantor_and_q4_girths()
    test_bt271_all_checks_pass()
