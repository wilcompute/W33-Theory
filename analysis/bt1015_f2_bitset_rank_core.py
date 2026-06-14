#!/usr/bin/env python3
"""BT1015 core: exact F2 bitset rank reducer.

This small module is separated from the heavy K3 level-2 face iterator so the
row-generation stack can be accepted and tested in pieces.
"""
from __future__ import annotations

from typing import Iterable


def rank_mod2_integer_rows(rows: Iterable[int]) -> int:
    """Return exact row rank over F2 for rows encoded as Python integer bitsets."""
    basis: dict[int, int] = {}
    rank = 0
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            old = basis.get(pivot)
            if old is None:
                basis[pivot] = value
                rank += 1
                break
            value ^= old
    return rank


def row_weight(row: int) -> int:
    return row.bit_count()


if __name__ == "__main__":
    rows = [0b1011, 0b0110, 0b1101, 0b1011 ^ 0b0110]
    print({"rank": rank_mod2_integer_rows(rows), "weights": [row_weight(r) for r in rows]})
