from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlii_closure_jordan_residue_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert s["unique_eigenvalue"] == 0
    assert s["jordan_chain_length"] == 6
    assert s["minimal_polynomial_degree"] == 6
    assert s["residue_tower_height"] == 6


def test_spectral_picture() -> None:
    payload = build_bridge()
    sp = payload["spectral_picture"]
    assert sp["eigenvalues"] == [0]
    assert sp["characteristic_polynomial"] == "lambda^6"
    assert sp["minimal_polynomial"] == "lambda^6"
    assert sp["jordan_blocks"] == [6]


def test_residue_orders_and_row_sums() -> None:
    payload = build_bridge()
    assert [item["order"] for item in payload["residue_tower"]] == [0, 1, 2, 3, 4, 5]
    assert payload["row_sums_at_z1"] == [
        {"numerator": 63, "denominator": 32},
        {"numerator": 31, "denominator": 16},
        {"numerator": 15, "denominator": 8},
        {"numerator": 7, "denominator": 4},
        {"numerator": 3, "denominator": 2},
        {"numerator": 1, "denominator": 1},
    ]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
