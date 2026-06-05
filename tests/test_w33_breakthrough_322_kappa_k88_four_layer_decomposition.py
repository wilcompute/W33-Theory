from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_322_kappa_k88_four_layer_decomposition import (  # noqa: E402
    kappa_k88_four_layer_decomposition_packet,
)


PACKET = kappa_k88_four_layer_decomposition_packet()


def test_bt322_layer_counts() -> None:
    assert PACKET["layer_counts"] == {
        "MK_Q4": 24,
        "M8_Q4": 8,
        "MK_weight3": 24,
        "M8_weight3": 8,
        "total": 64,
    }


def test_bt322_weight_distributions() -> None:
    assert PACKET["layer_xor_weight_distributions"] == {
        "MK_Q4": {1: 24},
        "M8_Q4": {1: 8},
        "MK_weight3": {3: 24},
        "M8_weight3": {3: 8},
    }


def test_bt322_matching_direction_counts() -> None:
    assert PACKET["matching_direction_counts"]["M8_Q4"] == {1: 2, 2: 2, 4: 2, 8: 2}
    assert PACKET["matching_direction_counts"]["M8_weight3"] == {7: 2, 11: 2, 13: 2, 14: 2}


def test_bt322_kappa_orbit_quotient() -> None:
    quotient = PACKET["kappa_orbit_quotient"]
    assert quotient["orbit_count"] == 32
    assert quotient["mk_orbits"] == 24
    assert quotient["matching_orbits"] == 8
    assert quotient["quotient_split"] == "24 Mobius-Kantor orbits + 8 matching orbits"


def test_bt322_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 25
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt322_layer_counts()
    test_bt322_weight_distributions()
    test_bt322_matching_direction_counts()
    test_bt322_kappa_orbit_quotient()
    test_bt322_all_checks_pass()
