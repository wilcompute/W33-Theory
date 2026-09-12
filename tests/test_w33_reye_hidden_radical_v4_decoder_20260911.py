#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_reye_hidden_radical_v4_decoder import build_result  # noqa: E402


def test_reye_blocks_are_hidden_v4_radical_decoder() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["radical"]["order"] == 4
    assert data["radical"]["index_to_pauli_word"] == {
        "0": "III",
        "1": "IIX",
        "2": "IZI",
        "3": "IZX",
    }
    assert data["decoder"]["blocks"] == 16
    assert len(data["decoder"]["rows"]) == 16
    latin = data["Pass8909_Latin_resolution"]
    assert latin["semantic_law"] == "phi_symbol(L(i,j)) = phi_row(i) XOR phi_column(j)"
    assert latin["affine_offset"] == 3
    assert latin["stored_numeric_affine_law"] == "L(i,j) = i XOR j XOR 3"
    assert data["block_graph"]["parameters"] == [16, 9, 4, 6]
    info = data["uniform_finite_information_model"]
    assert info["hidden_bits_per_point_fibre"] == 2.0
    assert info["hidden_bits_to_select_exact_block"] == 4.0
    assert info["third_offset_rule"] == "t = r XOR s"


if __name__ == "__main__":
    test_reye_blocks_are_hidden_v4_radical_decoder()
    print("hidden V4 radical Reye decoder test passed")
