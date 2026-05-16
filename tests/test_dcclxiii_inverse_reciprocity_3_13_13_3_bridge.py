from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxiii_inverse_reciprocity_3_13_13_3_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["weak_scalar_num"] == 3
    assert s["weak_scalar_den"] == 13
    assert s["transport_scalar_num"] == 13
    assert s["transport_scalar_den"] == 3
    assert s["reciprocal_product_num"] == 1
    assert s["reciprocal_product_den"] == 1


def test_derived_invariants() -> None:
    payload = build_bridge()
    inv = payload["derived_invariants"]
    assert inv["x"] == {"num": 3, "den": 13}
    assert inv["K"] == {"num": 13, "den": 3}
    assert inv["product"] == {"num": 1, "den": 1}
    assert inv["x_times_13"] == 3
    assert inv["K_times_3"] == 13


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
