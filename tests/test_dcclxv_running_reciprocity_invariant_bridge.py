from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxv_running_reciprocity_invariant_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["base_x_num"] == 3
    assert s["base_x_den"] == 13
    assert s["base_K_num"] == 13
    assert s["base_K_den"] == 3
    assert s["invariant_num"] == 1
    assert s["invariant_den"] == 1
    assert s["sample_count"] == 7


def test_products() -> None:
    payload = build_bridge()
    for row in payload["samples"]:
        lam_num = row["lambda"]["num"]
        lam_den = row["lambda"]["den"]
        assert row["bare_product"] == {"num": lam_den, "den": lam_num}
        assert row["running_product"] == {"num": 1, "den": 1}


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
