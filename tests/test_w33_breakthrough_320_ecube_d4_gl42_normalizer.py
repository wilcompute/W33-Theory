from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_320_ecube_d4_gl42_normalizer import (  # noqa: E402
    COMPLEMENT_INVOLUTION,
    DOUBLE_PAIR_SWAP,
    ecube_d4_gl42_normalizer_packet,
    mat_order,
)


PACKET = ecube_d4_gl42_normalizer_packet()


def test_bt320_sizes_and_indices() -> None:
    assert PACKET["gl42_order"] == 20160
    assert PACKET["d4_order"] == 8
    assert PACKET["coordinate_s4_order"] == 24
    assert PACKET["s4_normalizer_order"] == 8
    assert PACKET["s4_normalizer_index"] == 3
    assert PACKET["gl42_normalizer_order"] == 16
    assert PACKET["gl42_normalizer_index"] == 1260


def test_bt320_group_identifications() -> None:
    assert PACKET["group_identification"]["normalizer_in_s4"].startswith("D4")
    assert PACKET["group_identification"]["normalizer_in_gl42"] == "D4 x C2"
    assert PACKET["group_identification"]["centralizer_in_gl42"] == "C2 x C2"
    assert PACKET["normalizer_order_distribution"] == {1: 1, 2: 11, 4: 4}


def test_bt320_complement_involution() -> None:
    assert COMPLEMENT_INVOLUTION == (14, 13, 11, 7)
    assert PACKET["complement_involution"]["row_masks"] == [14, 13, 11, 7]
    assert PACKET["complement_involution"]["formula"] == "bit -> 15 xor bit"
    assert mat_order(COMPLEMENT_INVOLUTION) == 2
    assert [14, 13, 11, 7] in PACKET["nonpermutation_part"]


def test_bt320_centralizer_and_center() -> None:
    assert PACKET["gl42_centralizer_order"] == 4
    assert len(PACKET["normalizer_center"]) == 4
    assert list(DOUBLE_PAIR_SWAP) in PACKET["gl42_centralizer_elements"]
    assert [14, 13, 11, 7] in PACKET["gl42_centralizer_elements"]


def test_bt320_permutation_and_nonpermutation_parts() -> None:
    assert PACKET["permutation_part"] == PACKET["d4_elements"]
    assert len(PACKET["nonpermutation_part"]) == 8
    assert len(PACKET["gl42_normalizer_elements"]) == 16


def test_bt320_index_factorization() -> None:
    assert PACKET["index_factorization"]["value"] == 1260
    assert PACKET["index_factorization"]["substrate_form"] == "2^2 * q^2 * F5 * Phi6"
    assert PACKET["index_factorization"]["expanded"] == [4, 9, 5, 7]


def test_bt320_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 23
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt320_sizes_and_indices()
    test_bt320_group_identifications()
    test_bt320_complement_involution()
    test_bt320_centralizer_and_center()
    test_bt320_permutation_and_nonpermutation_parts()
    test_bt320_index_factorization()
    test_bt320_all_checks_pass()
