from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    forbidden_pocket_f4_packet,
)


PACKET = forbidden_pocket_f4_packet()


def test_bt159_forbidden_pocket_generates_f4_order() -> None:
    assert PACKET["forbidden_pocket_size"] == 8
    assert PACKET["generated_order"] == 1152
    assert "W(F4)" in PACKET["generated_order_reading"]


def test_bt159_polarization_split() -> None:
    assert PACKET["polarization_split"] == {
        "block_diagonal_preserving": 576,
        "anti_diagonal_swapping": 576,
    }


def test_bt159_order_distributions() -> None:
    assert PACKET["forbidden_order_distribution"] == {2: 4, 12: 4}
    assert PACKET["generated_order_distribution"] == {
        1: 1,
        2: 27,
        3: 80,
        4: 84,
        6: 432,
        8: 144,
        12: 384,
    }


def test_bt159_pair_products_leave_pocket() -> None:
    assert PACKET["forbidden_pair_products"] == {
        "identity": 8,
        "normalizer_other": 56,
    }


def test_bt159_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt159_forbidden_pocket_generates_f4_order()
    test_bt159_polarization_split()
    test_bt159_order_distributions()
    test_bt159_pair_products_leave_pocket()
    test_bt159_all_checks_pass()
